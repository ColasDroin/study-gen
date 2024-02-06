# ==================================================================================================
# --- Imports ---
# Some imports are optional as they're also declared in dict_imports, but it's
# helpful to declare them here for linting.
# ==================================================================================================
# Standard library imports
from typing import Any

import numpy as np
import pandas as pd
import xpart as xp

# Third party imports
import xtrack as xt

# Local imports
from study_gen.block import Block

# Imports needed for block to work (not detected by linting tools)
dict_imports = {
    "xo": "import xobjects as xo",
    "xp": "import xpart as xp",
    "Any": "from typing import Any",
    "np": "import numpy as np",
}


# ==================================================================================================
# --- Block function ---
# ==================================================================================================
def prepare_distribution_for_tracking_function(
    collider: xt.Multiline,
    context: Any,
    beam: str,
    path_input_distribution: str,
    delta_max: float,
    nemitt_x: float,
    nemitt_y: float,
) -> tuple[xp.particles.particles.Particles, list[int]]:
    particle_df = pd.read_parquet(path=path_input_distribution)

    r_vect = particle_df["normalized amplitude in xy-plane"].values
    theta_vect = particle_df["angle in xy-plane [deg]"].values * np.pi / 180  # type: ignore # [rad]

    A1_in_sigma = r_vect * np.cos(theta_vect)
    A2_in_sigma = r_vect * np.sin(theta_vect)

    particles = collider[beam].build_particles(
        x_norm=A1_in_sigma,
        y_norm=A2_in_sigma,
        delta=delta_max,
        nemitt_x=nemitt_x,
        nemitt_y=nemitt_y,
        _context=context,
    )

    particle_id = list(particle_df.particle_id.values)
    return particles, particle_id


# ==================================================================================================
# --- Block object ---
# ==================================================================================================

prepare_distribution_for_tracking = Block(
    "prepare_distribution_for_tracking",
    prepare_distribution_for_tracking_function,
    dict_imports=dict_imports,
)
