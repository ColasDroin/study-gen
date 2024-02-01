# ==================================================================================================
# --- Imports ---
# Some imports are optional as they're also declared in dict_imports, but it's
# helpful to declare them here for linting.
# ==================================================================================================
# Standard library imports
from collections import OrderedDict

# Third party imports
import xtrack as xt

# Local imports
from study_gen.block import Block

# Imports needed for block to work (not detected by linting tools)
dict_imports = {"xt": "import xtrack as xt"}


# ==================================================================================================
# --- Block function ---
# ==================================================================================================
def set_knobs_function(
    collider: xt.Multiline,
    knob_settings: dict,
) -> xt.Multiline:

    # Set all knobs (crossing angles, dispersion correction, rf, crab cavities,
    # experimental magnets, etc.)
    for kk, vv in knob_settings.items():
        collider.vars[kk] = vv

    return collider


# ==================================================================================================
# --- Block object ---
# ==================================================================================================

set_knobs = Block(
    "set_knobs",
    set_knobs_function,
    dict_imports=dict_imports,
)
