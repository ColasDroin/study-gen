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
def add_linear_coupling_hllhc_function(
    collider: xt.Multiline,
    delta_cmr: float,
    # delta_cmi: float,
) -> xt.Multiline:

    # Add linear coupling as the target in the tuning of the base collider was 0
    # (not possible to set it the target to 0.001 for now)
    collider.vars["c_minus_re_b1"] += delta_cmr
    collider.vars["c_minus_re_b2"] += delta_cmr

    # ! Only handle real coupling for now
    # collider.vars["c_minus_im_b1"] += delta_cmi
    # collider.vars["c_minus_im_b2"] += delta_cmi

    return collider


# ==================================================================================================
# --- Block object ---
# ==================================================================================================

add_linear_coupling_hllhc = Block(
    "add_linear_coupling_hllhc",
    add_linear_coupling_hllhc_function,
    dict_imports=dict_imports,
    dict_output=OrderedDict([("output_add_linear_coupling_hllhc", xt.Multiline)]),
)
