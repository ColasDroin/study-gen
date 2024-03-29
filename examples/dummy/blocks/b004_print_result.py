# ==================================================================================================
# --- Imports ---
# ==================================================================================================
# Standard library imports

# Third party imports

# Local imports
from study_gen.block import Block


# ==================================================================================================
# --- Block function ---
# ==================================================================================================
def print_result_function(d: float) -> None:
    print(f"Result: {float}")


# ==================================================================================================
# --- Block object ---
# ==================================================================================================

print_result = Block("print_result", print_result_function)
