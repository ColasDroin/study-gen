from collections import OrderedDict

from ._merge_blocks import get_multiple_merge_str, merge_dependencies
from .block import Block


def merge_imports(l_blocks: list[Block]) -> dict[str, str]:

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


def merge_blocks(
    l_blocks: list[Block], name_function: str, docstring: str = "", output=OrderedDict()
) -> Block:

    # Build function string
    function_str = get_multiple_merge_str(l_blocks, name_function, docstring, output)

    # Write string to temporary file
    function = Block.write_temp_block(function_str, name_function)

    # Merge imports
    dic_imports = merge_imports(l_blocks)

    # Add dependencies
    set_deps = merge_dependencies(l_blocks)

    return Block(function=function, dic_imports=dic_imports, set_deps=set_deps, output=output)
