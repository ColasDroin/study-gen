from collections import OrderedDict

from ..block import Block
from ._merge_blocks import get_multiple_merge_str, merge_dependencies


def merge_imports(l_blocks: list[Block]) -> OrderedDict[str, str]:

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
