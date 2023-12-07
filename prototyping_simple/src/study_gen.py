import copy
from collections import OrderedDict
from typing import Any, Callable, Self

import blocks
import merge
from jinja2 import Environment, FileSystemLoader
from ruamel import yaml

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
                # ! I need to find a way to do this iteratively, as there might be several levels of new blocks
                dict_blocks[block] = getattr(blocks, block)

        return dict_blocks

    def build_merged_blocks(
        self: Self,
        new_block_name: str,
        new_block: OrderedDict[str, Any],
        dict_blocks: OrderedDict[str, Block],
    ) -> Block:

        # Update parameters of each block to match the merged block specification
        l_blocks = []
        for block in new_block["blocks"]:
            block_to_update = copy.deepcopy(dict_blocks[block])
            l_params = new_block["blocks"][block]["params"]
            l_outputs = new_block["blocks"][block]["output"]
            block_to_update.set_parameters_names(l_params)
            block_to_update.set_outputs_names(l_outputs)
            l_blocks.append(block_to_update)

        # Get the dict of final output (with undefined type for now)
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

        new_block_function = merge.merge_blocks(
            l_blocks,
            new_block_name,
            docstring=new_block["docstring"],
            dict_output=dict_outputs_final,
        )

        return new_block_function

    def incorporte_merged_blocks(
        self: Self, gen: str, dict_blocks: OrderedDict[str, Block]
    ) -> OrderedDict[str, Block]:
        # Build new blocks
        for new_block_name, new_block in self.master[gen]["new_blocks"].items():
            dict_blocks[new_block_name] = self.build_merged_blocks(
                new_block_name, new_block, dict_blocks
            )

        return dict_blocks

    def generate_main_block(
        self: Self,
        gen: str,
        dict_blocks: OrderedDict[str, Block],
    ):
        # Get script
        script = self.master[gen]["script"]

        # Generate header
        header_str = "def main():\n"

        # Declare blocks
        blocks_str = "\n\t# Declare blocks\n"
        for block, dict_block in script.items():
            # Get block arguments
            l_args = dict_block["args"]
            if not isinstance(l_args, list):
                l_args = [l_args]
            # Get block outputs
            l_outputs = dict_block["output"]
            if not isinstance(l_outputs, list):
                l_outputs = [l_outputs]
            # Get true block in case of repeaded key
            if "__" in block:
                true_block = block.split("__")[0]
            else:
                true_block = block
            # Write blocks string
            blocks_str += (
                "\t" + dict_blocks[true_block].get_assignation_call_str(l_args, l_outputs) + "\n"
            )

        main_str = header_str + blocks_str

        # Replace tabs by spaces to prevent inconsistent indentation
        main_str = main_str.replace("\t", "    ")

        return dict_blocks

    def get_parameters_assignation(self: Self, main_block: Block) -> str:
        str_parameters = "\t# Declare parameters\n"
        # TODO: look for parameters used by main block and declare them
        for param, value in self.configuration.items():
            str_parameters += "\t" + param + " = " + str(value) + "\n"

        return str_parameters

    def generate_gen(self: Self, gen: str) -> list[str]:

        # Get dictionnary of blocks for writing the methods
        dict_blocks = self.get_dict_blocks(gen)

        # Get dictionnary of imports
        dict_imports_merge = merge.merge_imports(list(dict_blocks.values()))

        # Get string imports
        str_imports = Block.get_external_l_imports_str(dict_imports_merge)

        # Incorporate merged blocks if needed
        if "new_blocks" in self.master[gen]:
            dict_blocks = self.incorporte_merged_blocks(gen, dict_blocks)

        # Add main as ultimate block
        dict_blocks = self.generate_main_block(gen, dict_blocks)

        # Declare parameters
        str_parameters = self.get_parameters_assignation(dict_blocks["main"])

        # Get the dictionnary of block strings
        dict_blocks_str = {k: v.get_str() for k, v in dict_blocks.items()}

        # Get corresponding block string
        str_blocks = "\n".join([f"{k}" for k in dict_blocks_str.values()])

        return str_imports, str_parameters, str_blocks

    def render(self: Self, str_imports: str, str_parameters: str, str_blocks: str) -> str:

        # Generate generations from template
        environment = Environment(loader=FileSystemLoader(self.path_template))
        template = environment.get_template(self.template_name)

        # Render template
        study_str = template.render(
            imports=str_imports,
            parameters=str_parameters,
            blocks=str_blocks,
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
            str_main, str_blocks, str_imports = self.generate_gen(gen)
            study_str = self.render(str_main, str_blocks, str_imports)
            self.write(study_str, file_path_gen)
            l_study_str.append(study_str)
        return l_study_str
