# ==================================================================================================
# --- Imports ---
# ==================================================================================================
# Imports for typing and output
import itertools
from collections import OrderedDict

# Optional imports, but helpful for linting
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
def build_distribution_function(
    r_min: float, r_max: float, n_r: int, n_angles: int, n_split: int
) -> list[list[tuple[int, float, float]]]:
    radial_list = np.linspace(r_min, r_max, n_r, endpoint=False)

    # Define angle distribution
    theta_list = np.linspace(0, 90, n_angles + 2)[1:-1]

    # Define particle distribution as a cartesian product of the above
    particle_list = [
        (particle_id, ii[1], ii[0])
        for particle_id, ii in enumerate(itertools.product(theta_list, radial_list))
    ]

    # Split distribution into several chunks for parallelization
    particle_list = list(np.array_split(particle_list, n_split))

    # Return distribution
    return particle_list


# ==================================================================================================
# --- Block object ---
# ==================================================================================================

build_distribution = Block(
    "build_distribution",
    build_distribution_function,
    dict_output=OrderedDict([("output_build_distribution", float)]),
)
