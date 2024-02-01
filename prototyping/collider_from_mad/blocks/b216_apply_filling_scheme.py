# ==================================================================================================
# --- Imports ---
# Some imports are optional as they're also declared in dict_imports, but it's
# helpful to declare them here for linting.
# ==================================================================================================
# Standard library imports
from collections import OrderedDict

import numpy as np

# Third party imports
import xtrack as xt

# Local imports
from study_gen.block import Block

# Imports needed for block to work (not detected by linting tools)
dict_imports = {"xt": "import xtrack as xt", "np": "import numpy as np"}


# ==================================================================================================
# --- Block function ---
# ==================================================================================================
def apply_filling_scheme_function(
    collider: xt.Multiline,
    array_b1: np.ndarray,
    array_b2: np.ndarray,
    i_bunch_b1: int,
    i_bunch_b2: int,
) -> xt.Multiline:
    collider.apply_filling_pattern(
        filling_pattern_cw=array_b1,
        filling_pattern_acw=array_b2,
        i_bunch_cw=i_bunch_b1,
        i_bunch_acw=i_bunch_b2,
    )

    return collider


# ==================================================================================================
# --- Block object ---
# ==================================================================================================

apply_filling_scheme = Block(
    "apply_filling_scheme",
    apply_filling_scheme_function,
    dict_imports=dict_imports,
    dict_output=OrderedDict([("output_apply_filling_scheme", xt.Multiline)]),
)
