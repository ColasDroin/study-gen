import copy
from collections import OrderedDict
from typing import Any, Callable, Self

from jinja2 import Environment, FileSystemLoader
from ruamel import yaml

from . import blocks, merge
from .block import Block


class StudyGen:
    def __init__(
        self: Self,
        path_configuration: str,
        path_master: str,
        path_template: str = "templates/",
        template_name: str = "default_template.txt",
    ):
        self.configuration = self.load_configuration(path_configuration)
        self.master = self.load_master(path_master)
        self.path_template = path_template
        self.template_name = template_name

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

        # Get set of new (merged) blocks
        set_new_blocks = set()
        if "new_blocks" in self.master[gen]:
            set_new_blocks.update(self.master[gen]["new_blocks"].keys())

        # Get all blocks (except new blocks)
        for block in self.master[gen]["script"]:
            if "__" in block:
                # Don't want to declare twice the same block
                continue
            if block not in set_new_blocks:
                dict_blocks[block] = getattr(blocks, block)

        # Get blocks used for new blocks
        for new_block in set_new_blocks:
            for block in self.master[gen]["new_blocks"][new_block]["blocks"]:
                if "__" in block:
                    # Don't want to declare twice the same block
                    continue
                dict_blocks[block] = getattr(blocks, block)

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
            if "__" in block:
                # Don't want to declare twice the same block
                true_block = block.split("__")[0]
            else:
                true_block = block
            block_to_update = copy.deepcopy(dict_blocks[true_block])
            l_args = new_block["blocks"][block]["args"]
            l_outputs = new_block["blocks"][block]["output"]
            block_to_update.set_arguments_names(l_args)
            # ! SOMETHING FISHY HERE
            block_to_update.set_outputs_names(l_outputs)
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

        new_block_function = merge.merge_blocks(
            new_block_name,
            l_blocks,
            name_merged_function,
            docstring=new_block["docstring"],
            dict_output=dict_outputs_final,
        )

        return new_block_function

    def incorporate_merged_blocks(
        self: Self, new_blocks: OrderedDict[str, Any], dict_blocks: OrderedDict[str, Block]
    ) -> OrderedDict[str, Block]:
        # Build new blocks
        for new_block_name, new_block in new_blocks.items():

            # Compute the new block from merged blocks
            new_block_object = self.build_merged_blocks(new_block_name, new_block, dict_blocks)

            # Add dependencies of the new block to the dict of blocks
            for block_name in new_block_object.set_deps:
                if block_name not in dict_blocks:
                    try:
                        dict_blocks[block_name] = getattr(blocks, block_name)
                    except AttributeError:
                        raise ValueError(
                            f"Block {block_name} is used in block {new_block_name} but is not"
                            " defined anywhere."
                        )
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
        main_block_dict = OrderedDict([(str("blocks"), script)])

        main_block = self.build_merged_blocks(
            new_block_name="main",
            new_block=main_block_dict,
            dict_blocks=dict_blocks,
            name_merged_function="main",
        )

        return main_block

    def get_parameters_assignation(self: Self, main_block: Block) -> str:
        def _finditem(obj, key):
            if key in obj:
                return obj[key]
            for k, v in obj.items():
                if isinstance(v, dict):
                    item = _finditem(v, key)
                    if item is not None:
                        return item

        str_parameters = "\t# Declare parameters\n"
        for param in main_block.dict_parameters:
            # Look recursively for the corresponding parameter value in the configuration
            value = _finditem(self.configuration, param)
            if value is None:
                raise ValueError(f"Parameter {param} is not defined in the configuration")
            str_parameters += param + " = " + str(value) + "\n"

        return str_parameters

    def generate_gen(self: Self, gen: str) -> tuple[str, str, str, str, str]:

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
        str_parameters = self.get_parameters_assignation(main_block)

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

        # Render template
        study_str = template.render(
            imports=str_imports,
            parameters=str_parameters,
            blocks=str_blocks,
            main=str_main,
            main_call=str_main_call,
        )
        return study_str

    def write(self: Self, study_str: str, file_path: str):
        # TODO: handle file path
        with open(file_path, mode="w", encoding="utf-8") as file:
            file.write(study_str)

    def generate_all(self: Self) -> list[str]:
        l_study_str = []
        for gen in sorted(self.master.keys()):
            file_path_gen = f"{gen}.py"
            str_imports, str_parameters, str_blocks, str_main, str_main_call = self.generate_gen(
                gen
            )
            study_str = self.render(
                str_imports, str_parameters, str_blocks, str_main, str_main_call
            )
            self.write(study_str, file_path_gen)
            l_study_str.append(study_str)
        return l_study_str
