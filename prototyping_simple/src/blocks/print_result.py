# ==================================================================================================
# --- Imports ---
# ==================================================================================================
from ..block import Block


# ==================================================================================================
# --- Block function ---
# ==================================================================================================
def print_result_function(result: int) -> None:
    print(f"Result: {result}")


# ==================================================================================================
# --- Block object ---
# ==================================================================================================

print_result = Block(print_result_function)