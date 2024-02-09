import copy
from collections import OrderedDict

from ..block import Block


def _get_multiple_merge_parameters(l_blocks: list[Block]) -> OrderedDict[str, type]:
    # Start with empty dictionnary of parameters
    dict_parameters = OrderedDict()

    # Progressively merge all parameters (two by two)
    for idx, block1 in enumerate(l_blocks):
        for block2 in l_blocks[idx + 1 :]:
            # Check that identical parameters have identical type
            dict_arguments_block1 = block1.get_arguments_as_dict()
            dict_arguments_block2 = block2.get_arguments_as_dict()
            for key in set(dict_arguments_block1).intersection(dict_arguments_block2):
                if dict_arguments_block1[key] != dict_arguments_block2[key]:
                    raise ValueError(f"Parameter {key} has different types in the two blocks")

            # Add to dictionnary of parameters
            dict_parameters = dict_parameters | dict_arguments_block1 | dict_arguments_block2

    # If an output has been provided, remove it from the list of parameters
    # Except if it's modified inplace (inside of a block)
    for block in l_blocks:
        for key in block.dict_output:
            if key not in block.get_arguments_names() and key in dict_parameters:
                del dict_parameters[key]

    # Return the merged parameters
    return dict_parameters


def _check_external_merge_output(
    l_blocks: list[Block],
    dict_parameters: OrderedDict[str, type],
    dict_output: OrderedDict[str, type],
):
    # If the output is not None, ensure that the elements in it are either
    # - in the parameters (inplace operation)
    # - in the outputs
    if len(dict_output) > 0:
        # Merge all output and parameters
        dic_block_parameters_and_outputs = copy.deepcopy(dict_parameters)
        for block in l_blocks:
            dic_block_parameters_and_outputs = dic_block_parameters_and_outputs | block.dict_output

        # Check that all outputs are in the parameters or the outputs
        for key in dict_output:
            if key not in dic_block_parameters_and_outputs:
                raise ValueError(f"Output {key} is not in the parameters nor the outputs")


def _build_external_merge_str(
    l_blocks: list[Block],
    name_function: str,
    docstring: str = "",
    dict_output: OrderedDict[str, type] = OrderedDict(),
    dict_parameters: OrderedDict[str, type] = OrderedDict(),
) -> str:
    # Get output type hint string
    output_type_hint_str = Block.get_external_output_type_hint_str(dict_output)

    # Get output string
    output_str = Block.get_external_output_str(list(dict_output.keys()))

    # Get function header with the merged parameters
    parameters_header = ", ".join(
        [f"{parameter}: {dict_parameters[parameter].__name__}" for parameter in dict_parameters]
    )
    function_header = f"def {name_function}({parameters_header}) -> {output_type_hint_str}:"

    return Block.build_function_str(
        l_blocks, function_header, docstring=docstring, output_str=output_str
    )


def get_multiple_merge_str(
    l_blocks: list[Block],
    name_function: str,
    docstring: str = "",
    dict_output: OrderedDict[str, type] = OrderedDict(),
) -> str:
    # Get merged parameters
    dict_parameters = _get_multiple_merge_parameters(l_blocks)

    # Ensure that the output is accessible
    _check_external_merge_output(l_blocks, dict_parameters, dict_output)

    return _build_external_merge_str(
        l_blocks, name_function, docstring, dict_output, dict_parameters
    )


def merge_dependencies(l_blocks: list[Block]) -> set[str]:
    return {block.name for block in l_blocks}
