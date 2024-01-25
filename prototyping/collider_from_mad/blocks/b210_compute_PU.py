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
def compute_PU_function(
    luminosity: float, num_colliding_bunches: int, T_rev0: float, cross_section=81e-27
) -> float:
    return luminosity / num_colliding_bunches * cross_section * T_rev0


# ==================================================================================================
# --- Block object ---
# ==================================================================================================

compute_PU = Block(
    "compute_PU",
    compute_PU_function,
    dict_output=OrderedDict([("output_compute_PU", float)]),
)
