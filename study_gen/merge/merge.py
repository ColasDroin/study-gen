from collections import OrderedDict

from ..block import Block
from ._merge_blocks import get_multiple_merge_str, merge_dependencies


def merge_imports(l_blocks: list[Block]) -> OrderedDict[str, str]:
    """
    Merges the imports from multiple blocks, ensuring there are no conflicts.

    Args:
        l_blocks (list[Block]): A list of Block objects to be merged.

    Returns:
        OrderedDict[str, str]: A dictionary of merged imports, where the keys are module names and the values are import statements.

    Raises:
        ValueError: If there is an import conflict for a module, where import statements are not consistent.
    """
    # Merge imports, ensuring that there are no conflicts
    dict_imports = OrderedDict()
    for block in l_blocks:
        for module, import_statement in block.dict_imports.items():
            if module in dict_imports:
                if dict_imports[module] != import_statement:
                    raise ValueError(
                        f"Import conflict for module {module}. Import statements are not consistent"
                    )
            else:
                dict_imports[module] = import_statement

    return dict_imports


def merge_blocks(
    name_merged_block: str,
    l_blocks: list[Block],
    name_merged_function: str,
    docstring: str = "",
    dict_output: OrderedDict[str, type] = OrderedDict(),
) -> Block:
    """
    Merges multiple blocks into a single Block object.

    Args:
        name_merged_block (str): The name of the merged Block.
        l_blocks (list[Block]): A list of Block objects to be merged.
        name_merged_function (str): The name of the merged function.
        docstring (str, optional): The docstring for the merged function. Defaults to "".
        dict_output (OrderedDict[str, type], optional): A dictionary of output names and types for the merged function. Defaults to OrderedDict().

    Returns:
        Block: The merged Block object.

    Examples:
        name_merged_block = "merged_block"
        l_blocks = [block1, block2, block3]
        name_merged_function = "merged_function"
        docstring = "This is a merged function."
        dict_output = OrderedDict([('output1', int), ('output2', str)])
        merged_block = merge_blocks(name_merged_block, l_blocks, name_merged_function, docstring, dict_output)
    """
    # Build function string
    function_str = get_multiple_merge_str(l_blocks, name_merged_function, docstring, dict_output)

    # Merge imports
    dict_imports = merge_imports(l_blocks)

    # Add dependencies
    set_deps = merge_dependencies(l_blocks)

    # Write string to temporary file
    function = Block.write_and_load_temp_block(function_str, name_merged_function, dict_imports)

    return Block(
        name_merged_block,
        function=function,
        dict_imports=dict_imports,
        set_deps=set_deps,
        dict_output=dict_output,
    )
