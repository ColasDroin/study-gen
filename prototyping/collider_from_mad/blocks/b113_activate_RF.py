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
def activate_RF_function(
    collider: xt.Multiline,
) -> xt.Multiline:

    # Define a RF system for twissing (values are not so immportant as they're defined later)
    dic_rf = {"vrf400": 16.0, "lagrf400.b1": 0.5, "lagrf400.b2": 0.5}
    print("Now Computing Twiss assuming:")
    for knob, val in dic_rf.items():
        print(f"\t{knob} = {val}")

    # Apply the RF system
    for knob, val in dic_rf.items():
        collider.vars[knob] = val

    return collider


# ==================================================================================================
# --- Block object ---
# ==================================================================================================

activate_RF = Block(
    "activate_RF",
    activate_RF_function,
    dict_imports=dict_imports)
