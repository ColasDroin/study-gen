# ==================================================================================================
# --- Imports ---
# ==================================================================================================
from ..block import Block


# ==================================================================================================
# --- Block function ---
# ==================================================================================================
def print_result_function(d: float) -> None:
    print(f"Result: {float}")


# ==================================================================================================
# --- Block object ---
# ==================================================================================================

print_result = Block(print_result_function)
