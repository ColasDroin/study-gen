from collections import OrderedDict

from ._merge_blocks import get_multiple_merge_str, merge_dependencies
from .block import Block


def merge_imports(l_blocks: list[Block]) -> dict[str, str]:

    # Merge imports, ensuring that there are no conflicts
    dict_imports = OrderedDict()
    for block in l_blocks:
        for module, alias in block.dict_imports.items():
            if module in dict_imports:
                if dict_imports[module] != alias:
                    raise ValueError(
                        f"Import conflict for module {module}. Aliases are not consistent"
                    )
            else:
                dict_imports[module] = alias

    return dict_imports


def merge_blocks(
    l_blocks: list[Block],
    name_function: str,
    docstring: str = "",
    dict_output: OrderedDict[str, type] = OrderedDict(),
) -> Block:

    # Build function string
    function_str = get_multiple_merge_str(l_blocks, name_function, docstring, dict_output)

    # Write string to temporary file
    function = Block.write_and_load_temp_block(function_str, name_function)

    # Merge imports
    dict_imports = merge_imports(l_blocks)

    # Add dependencies
    set_deps = merge_dependencies(l_blocks)

    return Block(
        function=function, dict_imports=dict_imports, set_deps=set_deps, dict_output=dict_output
    )
