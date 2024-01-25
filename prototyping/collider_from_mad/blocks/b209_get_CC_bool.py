# ==================================================================================================
# --- Imports ---
# Some imports are optional as they're also declared in dict_imports, but it's
# helpful to declare them here for linting.
# ==================================================================================================
# Standard library imports
from collections import OrderedDict

# Local imports
from study_gen.block import Block


# ==================================================================================================
# --- Block function ---
# ==================================================================================================
def get_CC_bool_function(
    crab1_val: float,
    crab2_val: float,
) -> bool:

    # Get crab cavities as boolean
    crab = False
    if abs(crab1_val) > 0 or abs(crab2_val) > 0:
        crab = True
    return crab


# ==================================================================================================
# --- Block object ---
# ==================================================================================================

get_CC_bool = Block(
    "get_CC_bool",
    get_CC_bool_function,
    dict_output=OrderedDict([("output_get_CC_bool", bool)]),
)
