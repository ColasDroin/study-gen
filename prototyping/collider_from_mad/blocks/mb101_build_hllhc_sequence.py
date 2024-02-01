# ==================================================================================================
# --- Imports ---
# Some imports are optional as they're also declared in dict_imports, but it's
# helpful to declare them here for linting.
# ==================================================================================================
# Standard library imports
from collections import OrderedDict

# Third party imports
import xmask as xm
from cpymad.madx import Madx

# Local imports
from study_gen.block import Block

# Block dependencies
from .b101_build_initial_hllhc_sequence import build_initial_hllhc_sequence_function
from .b102_apply_acsca_fix_hllhc import apply_acsca_fix_hllhc_function
from .b103_slice_sequence import slice_sequence_function
from .b104_initialize_beam import initialize_beam_function
from .b105_cycle_to_IP3 import cycle_to_IP3_function
from .b106_incorporate_CC import incorporate_CC_function
from .b107_set_twiss import set_twiss_function

# Imports needed for block to work (not detected by linting tools)
dict_imports = {"Madx": "from cpymad.madx import Madx", "xm": "import xmask as xm"}

# Block dependencies
set_deps = set(
    [
        "apply_acsca_fix_hllhc",
        "build_initial_hllhc_sequence",
        "cycle_to_IP3",
        "incorporate_CC",
        "initialize_beam",
        "set_twiss",
        "slice_sequence",
    ]
)


# ==================================================================================================
# --- Block function ---
# ==================================================================================================
def build_hllhc_sequence_function(
    beam_name: str,
    mad: Madx,
    apply_acsca_fix: bool,
    cycle_to_IP3: bool,
    incorporate_CC: bool,
) -> Madx:

    # Get beam number
    if beam_name == "b1b2":
        beam = 1
    elif beam_name == "b4":
        beam = 4
    else:
        raise ValueError("Beam name not recognized.")

    # Build initial sequence
    mad = build_initial_hllhc_sequence_function(mad, beam)

    # Apply asca fix, doesn't work otherwise
    if apply_acsca_fix:
        mad = apply_acsca_fix_hllhc_function(mad)

    # Slice nominal sequence for tracking
    mad = slice_sequence_function(mad)

    # Define beam (for b1/b2)
    if beam < 3:
        mad = initialize_beam_function(mad)

    # Install error placeholders (configured later)
    xm.lhc.install_errors_placeholders_hllhc(mad)

    # Get IP3 as position 0
    if cycle_to_IP3:
        mad = cycle_to_IP3_function(mad)

    # Incorporate crab cavities (off by default)
    if incorporate_CC:
        mad = incorporate_CC_function(mad)

    # Set twiss format
    mad = set_twiss_function(mad)

    return mad


# ==================================================================================================
# --- Block object ---
# ==================================================================================================

build_hllhc_sequence = Block(
    "build_hllhc_sequence",
    build_hllhc_sequence_function,
    dict_imports=dict_imports,
    set_deps=set_deps,
)
