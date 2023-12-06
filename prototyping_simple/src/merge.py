import copy
from collections import OrderedDict

from .block import Block


def get_multiple_merge_parameters(
    l_blocks: list[Block], output: OrderedDict[str, type] = OrderedDict()
) -> OrderedDict[str, type]:

    # Start with empty dictionnary of parameters
    dict_parameters = OrderedDict()

    # Progressively merge all parameters (two by two)
    for idx, block1 in enumerate(l_blocks):
        for block2 in l_blocks[idx + 1 :]:

            # Check that identical parameters have identical type
            for key in set(block1.parameters).intersection(block2.parameters):
                if block1.parameters[key] != block2.parameters[key]:
                    raise ValueError(f"Parameter {key} has different types in the two blocks")

            dict_parameters = dict_parameters | block1.parameters | block2.parameters

    # If an output has been provided, remove it from the list of parameters
    # Except if it's modified inplace (inside of a block)
    for block in l_blocks:
        for key in block.output:
            if key not in block.parameters and key in dict_parameters:
                del dict_parameters[key]

    # Return the merged parameters
    return dict_parameters


def check_external_merge_output(
    l_blocks: list[Block],
    dict_parameters: OrderedDict[str, type],
    output: OrderedDict[str, type],
):
    # If the output is not None, ensure that the elements in it are either
    # - in the parameters (inplace operation)
    # - in the outputs
    if len(output) > 0:
        # Merge all output and parameters
        dic_block_parameters_and_outputs = copy.deepcopy(dict_parameters)
        for block in l_blocks:
            dic_block_parameters_and_outputs = dic_block_parameters_and_outputs | block.output

        # Check that all outputs are in the parameters or the outputs
        for key in output:
            if key not in dic_block_parameters_and_outputs:
                raise ValueError(f"Output {key} is not in the parameters nor the outputs")


def build_external_merge_str(
    l_blocks: list[Block],
    name_function: str,
    docstring: str = "",
    output: OrderedDict[str, type] = OrderedDict(),
    dict_parameters: OrderedDict[str, type] = OrderedDict(),
) -> str:

    # Get output type hint string
    output_type_hint_str = Block.get_external_output_type_hint_str(output)

    # Get output string
    output_str = Block.get_external_output_str(output)

    # Get function header with the merged parameters
    parameters_header = ", ".join(
        [f"{parameter}: {dict_parameters[parameter].__name__}" for parameter in dict_parameters]
    )
    function_header = f"def {name_function}({parameters_header}) -> {output_type_hint_str}:"

    # Build function string
    function_str = Block.build_function_str(
        l_blocks, function_header, docstring=docstring, output_str=output_str
    )

    return function_str


def get_multiple_merge_str(
    l_blocks: list[Block],
    name_function: str,
    docstring: str = "",
    output: OrderedDict[str, type] = OrderedDict(),
) -> str:

    # Get merged parameters
    dict_parameters = get_multiple_merge_parameters(l_blocks, output)

    # Ensure that the output is accessible
    check_external_merge_output(l_blocks, dict_parameters, output)

    # Build function string
    function_str = build_external_merge_str(
        l_blocks, name_function, docstring, output, dict_parameters
    )

    return function_str


def merge_multiple_imports(l_blocks: list[Block]) -> dict[str, str]:

    # Merge imports, ensuring that there are no conflicts
    dic_imports = OrderedDict()
    for block in l_blocks:
        for module, alias in block.dic_imports.items():
            if module in dic_imports:
                if dic_imports[module] != alias:
                    raise ValueError(
                        f"Import conflict for module {module}. Aliases are not consistent"
                    )
            else:
                dic_imports[module] = alias

    return dic_imports


def merge_multiple_dependencies(l_blocks: list[Block]) -> set[str]:
    set_imports = set()
    for block in l_blocks:
        set_imports.add(block.get_name_str())
    return set_imports


def merge_blocks(
    l_blocks: list[Block], name_function: str, docstring: str = "", output=OrderedDict()
) -> Block:

    # Build function string
    function_str = get_multiple_merge_str(l_blocks, name_function, docstring, output)

    # Write string to temporary file
    function = Block.write_temp_block(function_str, name_function)

    # Merge imports
    dic_imports = merge_multiple_imports(l_blocks)

    # Add dependencies
    set_deps = merge_multiple_dependencies(l_blocks)

    return Block(function=function, dic_imports=dic_imports, set_deps=set_deps, output=output)
