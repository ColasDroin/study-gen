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
def compute_constraints_ip8_function(
    l_contraints_ip8: list[str],
) -> list:

    # Set up the constraints for lumi optimization in IP8
    additional_targets_lumi = []
    for constraint in l_contraints_ip8:
        obs, beam, sign, val, at = constraint.split("_")
        target = xt.TargetInequality(obs, sign, float(val), at=at, line=beam, tol=1e-6)
        additional_targets_lumi.append(target)

    return additional_targets_lumi


# ==================================================================================================
# --- Block object ---
# ==================================================================================================

compute_constraints_ip8 = Block(
    "compute_constraints_ip8",
    compute_constraints_ip8_function,
    dict_imports=dict_imports,
)
