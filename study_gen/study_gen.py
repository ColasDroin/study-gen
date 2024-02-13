# Standard library imports
import copy
import itertools
import os
import shutil
from collections import OrderedDict
from typing import Any, Self

# Third party imports
import numpy as np
from black import FileMode, format_str
from jinja2 import Environment, FileSystemLoader
from ruamel import yaml

# Local imports
from . import merge
from ._nested_dicts import nested_set
from .block import Block


class StudyGen:
    def __init__(
        self: Self,
        path_configuration: str,
        path_master: str,
        dict_ref_blocks: dict[str, Block],
        path_template: str | None = None,
        template_name: str = "default_template.txt",
    ):
        self.configuration = self.load_configuration(path_configuration)
        self.master = self.load_master(path_master)
        self.template_name = template_name
        self.dict_ref_blocks = dict_ref_blocks

        if path_template is None:
            self.path_template = f"{os.path.dirname(__file__)}/templates/"
        else:
            self.path_template = path_template

        self.set_alert_parameters = set()

    def load_configuration(self: Self, path_configuration: str) -> dict[str, Any]:
        ryaml = yaml.YAML()
        with open(path_configuration, "r") as f:
            dict_configuration = ryaml.load(f)
        return dict_configuration

    def load_master(self: Self, path_master: str) -> dict[str, Any]:
        ryaml = yaml.YAML()
        with open(path_master, "r") as f:
            try:
                master = ryaml.load(f)
            except yaml.YAMLError as e:
                print(
                    "It seems that you have duplicate keys in your master file. Please ensure that"
                    " no block is being called twice with the same name in a given scope. If that's"
                    " the case, please append '__x' to the end of the block name, where x"
                    " corresponds to the xth repetition of the block."
                )
                print(e)
                exit(1)
        return master

    def get_dict_blocks(self: Self, gen: str) -> OrderedDict[str, Block]:
        # Start with empty dict of blocks
        dict_blocks = OrderedDict()

        # Get set of new (merged) blocks names
        set_new_blocks = set()
        if "new_blocks" in self.master[gen]:
            set_new_blocks.update(self.master[gen]["new_blocks"].keys())

        # Get all blocks (except new blocks) objects
        for block in self.master[gen]["script"]:
            if "__" in block:
                # Don't want to declare twice the same block
                continue
            if block not in set_new_blocks:
                if block not in self.dict_ref_blocks:
                    raise ValueError(
                        f"Block {block} is in the master file but not in the reference blocks."
                    )

                # Get dependencies of the block first
                for dep in self.dict_ref_blocks[block].set_deps:
                    if dep not in dict_blocks:
                        dict_blocks[dep] = self.dict_ref_blocks[dep]
                # Then get the block itself
                dict_blocks[block] = self.dict_ref_blocks[block]
        # Get blocks objects used for new blocks
        for new_block in set_new_blocks:
            for block in self.master[gen]["new_blocks"][new_block]["blocks"]:
                if "__" in block:
                    # Don't want to declare twice the same block
                    continue
                if block in set_new_blocks:
                    # New blocks will be declared later
                    continue
                dict_blocks[block] = self.dict_ref_blocks[block]

        # Ensure that all blocks have valid dependencies
        for block in dict_blocks.values():
            for dep in block.set_deps:
                if dep not in dict_blocks:
                    raise ValueError(
                        f"Block {block.name} depends on block {dep} but this block is not defined"
                        " in the master file."
                    )
        return dict_blocks

    def build_merged_blocks(
        self: Self,
        new_block_name: str,
        new_block: OrderedDict[str, Any],
        dict_blocks: OrderedDict[str, Block],
        name_merged_function: str | None = None,
    ) -> Block:
        # Update arguments of each block to match the merged block specification
        l_blocks = []
        for block in new_block["blocks"]:
            true_block = block.split("__")[0] if "__" in block else block
            block_to_update = copy.deepcopy(dict_blocks[true_block])

            # Get arguments
            l_args = new_block["blocks"][block]["args"]
            block_to_update.set_arguments_names(l_args)

            # Get outputs
            l_outputs = new_block["blocks"][block]["output"]
            block_to_update.set_outputs_names(l_outputs)

            # Add to updated list of blocks
            l_blocks.append(block_to_update)

        # Get the dict of final output (with undefined type for now)
        if "output" in new_block:
            output_final = new_block["output"]
            if not isinstance(output_final, list):
                output_final = [output_final]
            dict_outputs_final = OrderedDict([(output, None) for output in output_final])

            # Find the type of output
            for block in l_blocks:
                for output in block.dict_output:
                    if output in dict_outputs_final:
                        dict_outputs_final[output] = block.dict_output[output]

            # Raise an error if some outputs are not defined
            if None in dict_outputs_final.values():
                raise ValueError("Some outputs are not defined")
        else:
            dict_outputs_final = OrderedDict()

        # Handle docstring
        if "docstring" not in new_block:
            new_block["docstring"] = ""

        # Name the block function
        if name_merged_function is None:
            name_merged_function = f"{new_block_name}_function"

        return merge.merge_blocks(
            new_block_name,
            l_blocks,
            name_merged_function,
            docstring=new_block["docstring"],
            dict_output=dict_outputs_final,  # type: ignore
        )

    def incorporate_merged_blocks(
        self: Self, new_blocks: OrderedDict[str, Any], dict_blocks: OrderedDict[str, Block]
    ) -> OrderedDict[str, Block]:
        # Build new blocks
        for new_block_name, new_block in new_blocks.items():
            # Compute the new block from merged blocks
            new_block_object = self.build_merged_blocks(new_block_name, new_block, dict_blocks)

            # Ensure parameters match the definition
            if "params" in new_block:
                # Ensure that the parameters are provided in a list
                if not isinstance(new_block["params"], list):
                    # If user provided several parameters separated by a comma
                    if new_block["params"] is None:
                        new_block["params"] = []
                    elif "," in new_block["params"]:
                        new_block["params"] = new_block["params"].split(",")
                    else:
                        new_block["params"] = [new_block["params"]]
                # Ensure that the parameters are as they should be
                if new_block_object.get_dict_parameters_names() != new_block["params"]:
                    for param in new_block["params"]:
                        if param not in new_block_object.get_dict_parameters_names():
                            raise ValueError(
                                f"Parameter {param} is not defined in the merged block"
                            )
                    for param in new_block_object.get_dict_parameters_names():
                        if param not in new_block["params"]:
                            raise ValueError(
                                f"Parameter {param} is defined in the merged block but not in the"
                                " master file"
                            )
                    # Reorder the parameters
                    new_block_object.dict_parameters = OrderedDict(
                        [
                            (param, new_block_object.dict_parameters[param])
                            for param in new_block["params"]
                        ]
                    )

            # Add dependencies of the new block to the dict of blocks
            for block_name in new_block_object.set_deps:
                if block_name not in dict_blocks:
                    try:
                        dict_blocks[block_name] = self.dict_ref_blocks[block_name]
                    except AttributeError as e:
                        raise ValueError(
                            f"Block {block_name} is used in block {new_block_name} but is not"
                            " defined anywhere."
                        ) from e
            # Ensure that the new block is not already defined
            if new_block_name in dict_blocks:
                raise ValueError(
                    f"Block {new_block_name} is already defined. Please ensure there are no"
                    " redefinition in the master file."
                )

            # Add new block to the dict of blocks
            dict_blocks[new_block_name] = new_block_object

        return dict_blocks

    def generate_main_block(
        self: Self,
        gen: str,
        dict_blocks: OrderedDict[str, Block],
    ):
        # Get script
        script = self.master[gen]["script"]

        # Convert script format to new_block format
        main_block_dict = OrderedDict([("blocks", script)])

        return self.build_merged_blocks(
            new_block_name="main",
            new_block=main_block_dict,  # type: ignore
            dict_blocks=dict_blocks,
            name_merged_function="main",
        )

    def get_parameters_assignation(
        self: Self,
        main_block: Block,
        dic_mutated_parameters: dict[str, Any] = {},
    ) -> str:
        def _finditem(obj, key):
            if key in obj:
                return obj[key]
            for k, v in obj.items():
                if isinstance(v, dict):
                    item = _finditem(v, key)
                    if item is not None:
                        return item

        str_parameters = "# Declare parameters\n"
        for param in main_block.dict_parameters:
            # Look recursively for the corresponding parameter value in the configuration
            value = _finditem(self.configuration, param)
            if value is None:
                if param not in dic_mutated_parameters:
                    raise ValueError(
                        f"Parameter {param} is not defined in the configuration, nor being scanned"
                    )
                else:
                    value = dic_mutated_parameters[param]
            else:
                if param in dic_mutated_parameters:
                    if param not in self.set_alert_parameters:
                        print(
                            f"Parameter {param} is defined in the configuration and being scanned."
                            " The value from the configuration will be used."
                        )
                        self.set_alert_parameters.add(param)
                    value = dic_mutated_parameters[param]
            if isinstance(value, str):
                value = f'"{value}"'
            str_parameters += f"{param} = {value}\n"

        return str_parameters

    def generate_gen(
        self: Self, gen: str, dic_mutated_parameters: dict[str, Any] = {}
    ) -> tuple[str, str, str, str, str]:  # sourcery skip: default-mutable-arg
        # Get dictionnary of blocks for writing the methods
        dict_blocks = self.get_dict_blocks(gen)

        # Get dictionnary of imports
        dict_imports_merge = merge.merge_imports(list(dict_blocks.values()))

        # Get string imports
        str_imports = Block.get_external_l_imports_str(dict_imports_merge)

        # Incorporate merged blocks if needed
        if "new_blocks" in self.master[gen]:
            dict_blocks = self.incorporate_merged_blocks(
                self.master[gen]["new_blocks"], dict_blocks
            )

        # Add main as ultimate block
        main_block = self.generate_main_block(gen, dict_blocks)

        # Declare parameters
        str_parameters = self.get_parameters_assignation(main_block, dic_mutated_parameters)

        # Get main block string
        str_main = main_block.get_str()

        # Get main call (use parameters as arguments, since parameters are built from arguments in this case)
        str_main_call = main_block.get_call_str(
            l_external_arguments=main_block.get_dict_parameters_names()
        )

        # Get the dictionnary of block strings
        dict_blocks_str = {k: v.get_str() for k, v in dict_blocks.items()}

        # Get corresponding block string
        str_blocks = "\n".join([f"{k}" for k in dict_blocks_str.values()])

        return str_imports, str_parameters, str_blocks, str_main, str_main_call

    def render(
        self: Self,
        str_imports: str,
        str_parameters: str,
        str_blocks: str,
        str_main: str,
        str_main_call: str,
    ) -> str:
        # Generate generations from template
        environment = Environment(loader=FileSystemLoader(self.path_template))
        template = environment.get_template(self.template_name)

        return template.render(
            imports=str_imports,
            parameters=str_parameters,
            blocks=str_blocks,
            main=str_main,
            main_call=str_main_call,
        )

    def write(self: Self, study_str: str, file_path: str, format_with_black: bool = True):
        if format_with_black:
            study_str = format_str(study_str, mode=FileMode())

        # Make folder if it doesn't exist
        folder = os.path.dirname(file_path)
        if folder != "":
            os.makedirs(folder, exist_ok=True)

        with open(file_path, mode="w", encoding="utf-8") as file:
            file.write(study_str)

    def generate_render_write(
        self: Self,
        gen_name: str,
        layer_name: str,
        study_path: str,
        dic_mutated_parameters: dict[str, Any] = {},
    ) -> tuple[str, list[str]]:  # sourcery skip: default-mutable-arg
        directory_path_gen = f"{study_path}{layer_name}/"
        file_path_gen = f"{directory_path_gen}{gen_name}.py"
        (
            str_imports,
            str_parameters,
            str_blocks,
            str_main,
            str_main_call,
        ) = self.generate_gen(gen_name, dic_mutated_parameters)
        study_str = self.render(str_imports, str_parameters, str_blocks, str_main, str_main_call)
        self.write(study_str, file_path_gen)
        return study_str, [directory_path_gen]

    def get_dic_parametric_scans(self: Self, layer) -> tuple[dict[str, Any], dict[str, Any]]:
        def test_convert_for_each_beam(parameter_dict: dict, parameter_list: list) -> list:
            if "for_each_beam" in parameter_dict and parameter_dict["for_each_beam"]:
                parameter_list = [{"lhcb1": value, "lhcb2": value} for value in parameter_list]
            return parameter_list

        dic_parameter_lists = {}
        dic_parameter_lists_for_naming = {}
        for parameter in self.master["structure"][layer]["scans"]:
            if "linspace" in self.master["structure"][layer]["scans"][parameter]:
                l_values_linspace = self.master["structure"][layer]["scans"][parameter]["linspace"]
                parameter_list = np.round(
                    np.linspace(
                        l_values_linspace[0],
                        l_values_linspace[1],
                        l_values_linspace[2],
                        endpoint=True,
                    ),
                    5,
                )
            elif "logspace" in self.master["structure"][layer]["scans"][parameter]:
                l_values_logspace = self.master["structure"][layer]["scans"][parameter]["logspace"]
                parameter_list = np.round(
                    np.logspace(
                        l_values_logspace[0],
                        l_values_logspace[1],
                        l_values_logspace[2],
                        endpoint=True,
                    ),
                    5,
                )
            elif "list" in self.master["structure"][layer]["scans"][parameter]:
                parameter_list = self.master["structure"][layer]["scans"][parameter]["list"]
            else:
                raise ValueError(f"Scanning method for parameter {parameter} is not recognized.")
            dic_parameter_lists_for_naming[parameter] = parameter_list
            parameter_list_updated = test_convert_for_each_beam(
                self.master["structure"][layer]["scans"][parameter], parameter_list
            )
            dic_parameter_lists[parameter] = parameter_list_updated

        return dic_parameter_lists, dic_parameter_lists_for_naming

    def create_scans(
        self: Self, gen: str, layer: str, layer_path: str
    ) -> tuple[list[str], list[str]]:
        # Get dictionnary of parametric values being scanned
        dic_parameter_lists, dic_parameter_lists_for_naming = self.get_dic_parametric_scans(layer)

        # Generate render write for cartesian product of all parameters
        l_study_str = []
        l_study_path = []
        for l_values, l_values_for_naming in zip(
            itertools.product(*dic_parameter_lists.values()),
            itertools.product(*dic_parameter_lists_for_naming.values()),
        ):
            dic_mutated_parameters = dict(zip(dic_parameter_lists.keys(), l_values))
            dic_mutated_parameters_for_naming = dict(
                zip(dic_parameter_lists.keys(), l_values_for_naming)
            )
            path = (
                layer_path
                + "_".join(
                    [
                        f"{parameter}_{value}"
                        for parameter, value in dic_mutated_parameters_for_naming.items()
                    ]
                )
                + "/"
            )
            l_study_path.append(path)
            l_study_str.append(
                self.generate_render_write(
                    gen,
                    "",
                    path,
                    dic_mutated_parameters=dic_mutated_parameters,
                )
            )
        return l_study_str, l_study_path

    def create_study(
        self: Self, tree_file: bool = True, force_overwrite: bool = False
    ) -> list[str]:
        l_study_str = []
        l_study_path = [self.master["name"] + "/"]
        dictionary_tree = {}

        # Remove existing study if force_overwrite
        if force_overwrite and os.path.exists(self.master["name"]):
            shutil.rmtree(self.master["name"])

        for idx, layer in enumerate(sorted(self.master["structure"].keys())):
            # Each generaration inside of a layer should yield the same l_study_path_next_layer
            l_study_path_next_layer = []
            for study_path in l_study_path:
                for gen in self.master["structure"][layer]["generations"]:
                    if "scans" in self.master["structure"][layer]:
                        l_study_scan_str, l_study_path_next_layer = self.create_scans(
                            gen, layer, study_path
                        )
                        l_study_str.extend(l_study_scan_str)

                    else:
                        # Always give the layer the name of the first generation file,
                        # except if very first layer
                        layer_temp = (
                            "base"
                            if idx == 0
                            else self.master["structure"][layer]["generations"][0]
                        )
                        study_str, l_study_path_next_layer = self.generate_render_write(
                            gen, layer_temp, study_path
                        )
                        l_study_str.append(study_str)

                    # Complete tree dictionnary
                    for path_next in l_study_path_next_layer:
                        nested_set(
                            dictionary_tree,
                            path_next.split("/")[1:-1] + [gen],
                            {"file": f"{path_next}{gen}.py"},
                        )

            # Update study path for next later
            l_study_path = l_study_path_next_layer

        if tree_file:
            ryaml = yaml.YAML()
            with open(self.master["name"] + "/" + "tree.yaml", "w") as yaml_file:
                ryaml.indent(sequence=4, offset=2)
                ryaml.dump(dictionary_tree, yaml_file)
        return l_study_str
