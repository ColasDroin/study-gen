# ==================================================================================================
# --- Imports ---
# Some imports are optional as they're also declared in dict_imports, but it's
# helpful to declare them here for linting.
# ==================================================================================================
# Standard library imports

# Third party imports
import xtrack as xt

# Local imports
from study_gen.block import Block

# Imports needed for block to work (not detected by linting tools)
dict_imports = {"xt": "import xtrack as xt"}


# ==================================================================================================
# --- Block function ---
# ==================================================================================================
def install_beam_beam_function(
    collider: xt.Multiline,
    num_long_range_encounters_per_side: dict[str, int],
    num_slices_head_on: int,
    bunch_spacing_buckets: int,
    sigma_z: float,
) -> xt.Multiline:

    # Install beam-beam lenses (inactive and not configured)
    collider.install_beambeam_interactions(
        clockwise_line="lhcb1",
        anticlockwise_line="lhcb2",
        ip_names=["ip1", "ip2", "ip5", "ip8"],
        delay_at_ips_slots=[0, 891, 0, 2670],
        num_long_range_encounters_per_side=num_long_range_encounters_per_side,
        num_slices_head_on=num_slices_head_on,
        harmonic_number=35640,
        bunch_spacing_buckets=bunch_spacing_buckets,
        sigmaz=sigma_z,
    )

    return collider


# ==================================================================================================
# --- Block object ---
# ==================================================================================================

install_beam_beam = Block(
    "install_beam_beam",
    install_beam_beam_function,
    dict_imports=dict_imports,
)
