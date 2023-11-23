from .block import Block

def compose_blocks(*blocks: Block) -> Block:
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
        composed_block.add(block)

    # Return the composed block
    return composed_block