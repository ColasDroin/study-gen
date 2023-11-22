# ==================================================================================================
# --- Imports ---
# ==================================================================================================
# Third party imports
from xmask.lhc import install_errors_placeholders_hllhc

# Import blocks
from prototyping.blocks.madx_sequence.apply_fix_asca_madx_sequence import (
    apply_fix_asca_madx_sequence,
)
from prototyping.blocks.madx_sequence.build_madx_sequence import build_madx_sequence
from prototyping.blocks.madx_sequence.cycle_madx_sequence import cycle_madx_sequence
from prototyping.blocks.madx_sequence.install_cc_madx_sequence import install_cc_madx_sequence
from prototyping.blocks.madx_sequence.provide_beam_madx_sequence import provide_beam_madx_sequence
from prototyping.blocks.madx_sequence.set_twiss_madx_sequence import set_twiss_madx_sequence
from prototyping.blocks.madx_sequence.slice_madx_sequence import slice_madx_sequence

# ==================================================================================================
# --- Block ---
# ==================================================================================================


def build_sequence(mad: cpymad.madx.Madx, beam: int) -> cpymad.madx.Madx:

    # Select beam
    mad.input(f"mylhcbeam = {beam}")

    # Build sequence
    mad = build_madx_sequence(mad)

    # Apply fix
    mad = apply_fix_asca_madx_sequence(mad)

    # Slice nominal sequence
    mad = slice_madx_sequence(mad)

    # Provide beam
    if beam < 3:
        mad = provide_beam_madx_sequence(mad)

    # Install errors placeholders
    mad = install_errors_placeholders_hllhc(mad)

    # Cycle w.r.t. to IP3
    mad = cycle_madx_sequence(mad)

    # Install crab-cavities
    mad = install_cc_madx_sequence(mad)

    # Set twiss format
    mad = set_twiss_madx_sequence(mad)

    return mad
