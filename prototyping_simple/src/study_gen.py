from collections import OrderedDict

from .block import Block


def compose_blocks(*blocks: Block, output: OrderedDict[str, type]) -> Block:
    """Compose blocks into a single block

    Args:
        *blocks (Block): Blocks to compose

    Returns:
        Block: Composed block
    """
    # Create a new block
    composed_block = Block()

    # Add all blocks to the composed block
    for block in blocks:
        composed_block.merge_block(
            block, "test_merge_function", "This is a test for a merge function", output
        )

    # Return the composed block
    return composed_block
