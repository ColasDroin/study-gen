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
def configure_beam_beam_interactions_function(
    collider: xt.Multiline,
    num_particles_per_bunch: float,
    nemitt_x: float,
    nemitt_y: float,
) -> xt.Multiline:
    collider.configure_beambeam_interactions(
        num_particles=num_particles_per_bunch,
        nemitt_x=nemitt_x,
        nemitt_y=nemitt_y,
    )

    return collider


# ==================================================================================================
# --- Block object ---
# ==================================================================================================

configure_beam_beam_interactions = Block(
    "configure_beam_beam_interactions",
    configure_beam_beam_interactions_function,
    dict_imports=dict_imports,
    dict_output=OrderedDict([("output_configure_beam_beam_interactions", xt.Multiline)]),
)
