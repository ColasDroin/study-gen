# ==================================================================================================
# --- Imports ---
# Some imports are optional as they're also declared in dict_imports, but it's
# helpful to declare them here for linting.
# ==================================================================================================
# Standard library imports

# Local imports
from study_gen.block import Block


# ==================================================================================================
# --- Block function ---
# ==================================================================================================
def get_CC_bool_function(
    crab1_val: float,
    crab5_val: float,
) -> bool:

    return abs(crab1_val) > 0 or abs(crab5_val) > 0


# ==================================================================================================
# --- Block object ---
# ==================================================================================================

get_CC_bool = Block(
    "get_CC_bool",
    get_CC_bool_function,
)
