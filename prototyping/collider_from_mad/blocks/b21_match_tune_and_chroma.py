# ==================================================================================================
# --- Imports ---
# Some imports are optional as they're also declared in dict_imports, but it's
# helpful to declare them here for linting.
# ==================================================================================================
# Standard library imports
from collections import OrderedDict

# Third party imports
import xmask as xm
import xtrack as xt

# Local imports
from study_gen.block import Block

# Imports needed for block to work (not detected by linting tools)
dict_imports = {"xt": "import xtrack as xt", "xm": "import xmask as xm"}


# ==================================================================================================
# --- Block function ---
# ==================================================================================================
def match_tune_and_chroma_function(
    collider: xt.Multiline,
    conf_knob_names: dict,
    conf_qx: dict,
    conf_qy: dict,
    conf_dqx: dict,
    conf_dqy: dict,
    conf_closed_orbit_correction: dict,
):
    # Tunings
    for line_name in ["lhcb1", "lhcb2"]:
        knob_names = conf_knob_names[line_name]

        targets = {
            "qx": conf_qx[line_name],
            "qy": conf_qy[line_name],
            "dqx": conf_dqx[line_name],
            "dqy": conf_dqy[line_name],
        }

        xm.machine_tuning(
            line=collider[line_name],
            enable_closed_orbit_correction=True,
            enable_linear_coupling_correction=True,
            enable_tune_correction=True,
            enable_chromaticity_correction=True,
            knob_names=knob_names,
            targets=targets,
            line_co_ref=collider[line_name + "_co_ref"],
            co_corr_config=conf_closed_orbit_correction[line_name],
        )

    return collider


# ==================================================================================================
# --- Block object ---
# ==================================================================================================

match_tune_and_chroma = Block(
    "match_tune_and_chroma",
    match_tune_and_chroma_function,
    dict_imports=dict_imports,
    dict_output=OrderedDict([("output_match_tune_and_chroma", xt.Multiline)]),
)
