# ==================================================================================================
# --- Imports ---
# ==================================================================================================
from collections import OrderedDict

from ..block import Block


# ==================================================================================================
# --- Block function ---
# ==================================================================================================
def multiply_function(a: int, b: int) -> int:

    # Multiply a and b
    return a * b


# ==================================================================================================
# --- Block object ---
# ==================================================================================================

multiply = Block(multiply_function, output=OrderedDict([("output_multiply", int)]))