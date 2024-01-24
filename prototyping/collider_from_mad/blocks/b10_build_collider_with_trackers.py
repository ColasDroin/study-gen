# ==================================================================================================
# --- Imports ---
# Some imports are optional as they're also declared in dict_imports, but it's
# helpful to declare them here for linting.
# ==================================================================================================
# Standard library imports
from collections import OrderedDict
from typing import Any

# Third party imports
import xmask as xm
import xtrack as xt
from cpymad.madx import Madx

# Local imports
from study_gen.block import Block

# Imports needed for block to work (not detected by linting tools)
dict_imports = {
    "Madx": "from cpymad.madx import Madx",
    "Any": "from typing import Any",
    "OrderedDict": "from collections import OrderedDict",
    "xm": "import xmask as xm",
    "xt": "import xtrack as xt",
}


# ==================================================================================================
# --- Block function ---
# ==================================================================================================
def build_collider_with_trackers_function(
    mad_b1b2: Madx,
    mad_b4: Madx,
    beam_config: OrderedDict[str, Any],
    enable_imperfections: bool,
    enable_knob_synthesis: bool,
    rename_coupling_knobs: bool,
    pars_for_imperfections: OrderedDict[str, int],
    ver_hllhc_optics: float,
) -> xt.Multiline:

    # Build collider
    collider = xm.lhc.build_xsuite_collider(
        sequence_b1=mad_b1b2.sequence.lhcb1,
        sequence_b2=mad_b1b2.sequence.lhcb2,
        sequence_b4=mad_b4.sequence.lhcb2,
        beam_config=beam_config,
        enable_imperfections=enable_imperfections,
        enable_knob_synthesis=enable_knob_synthesis,
        rename_coupling_knobs=rename_coupling_knobs,
        pars_for_imperfections=pars_for_imperfections,
        ver_lhc_run=None,
        ver_hllhc_optics=ver_hllhc_optics,
    )

    # Build trackers (CPU context by defaults)
    collider.build_trackers()

    return collider


# ==================================================================================================
# --- Block object ---
# ==================================================================================================

build_collider_with_trackers = Block(
    "build_collider_with_trackers",
    build_collider_with_trackers_function,
    dict_imports=dict_imports,
    dict_output=OrderedDict([("output_build_collider_with_trackers", xt.Multiline)]),
)
