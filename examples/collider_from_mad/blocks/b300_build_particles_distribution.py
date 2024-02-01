# ==================================================================================================
# --- Imports ---
# Some imports are optional as they're also declared in dict_imports, but it's
# helpful to declare them here for linting.
# ==================================================================================================
# Standard library imports
import itertools

# Third party imports
import numpy as np

# Local imports
from study_gen.block import Block

# Imports needed for block to work (not detected by linting tools)
dict_imports = {"numpy": "import numpy as np", "itertools": "import itertools"}
for module, import_statement in dict_imports.items():
    exec(import_statement)


# ==================================================================================================
# --- Block function ---
# ==================================================================================================
def build_particles_distribution_function(
    r_min: float, r_max: float, n_r: int, n_angles: int, n_split: int
) -> list[list[tuple[int, float, float]]]:
    radial_list = np.linspace(r_min, r_max, n_r, endpoint=False)

    # Define angle distribution
    theta_list = np.linspace(0, 90, n_angles + 2)[1:-1]

    # Define particle distribution as a cartesian product of the above
    particle_list = np.array(
        [
            (particle_id, ii[1], ii[0])
            for particle_id, ii in enumerate(itertools.product(theta_list, radial_list))
        ]
    )

    # Split distribution into several chunks for parallelization
    particle_list = [list(x) for x in np.array_split(particle_list, n_split)]

    # Return distribution
    return particle_list


# ==================================================================================================
# --- Block object ---
# ==================================================================================================

build_particles_distribution = Block(
    "build_particles_distribution",
    build_particles_distribution_function,
    dict_imports=dict_imports,
)
