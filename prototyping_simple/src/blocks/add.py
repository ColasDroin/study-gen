# ==================================================================================================
# --- Imports ---
# ==================================================================================================
from collections import OrderedDict

from ..block import Block


# ==================================================================================================
# --- Block function ---
# ==================================================================================================
def add_function(a: float, b: float) -> float:
    """Dummy docstring"""
    # Add a and b
    return a + b


# ==================================================================================================
# --- Block object ---
# ==================================================================================================

add = Block("add", add_function, dict_output=OrderedDict([("output_add", float)]))
