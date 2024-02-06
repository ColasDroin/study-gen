# ==================================================================================================
# --- Imports ---
# Some imports are optional as they're also declared in dict_imports, but it's
# helpful to declare them here for linting.
# ==================================================================================================
# Standard library imports

# Third party imports
import numpy as np

# Local imports
from study_gen.block import Block

# Imports needed for block to work (not detected by linting tools)
dict_imports = {"np": "import numpy as np"}


# ==================================================================================================
# --- Block function ---
# ==================================================================================================
def compute_collision_schedule_function(
    array_b1: np.ndarray, array_b2: np.ndarray
) -> tuple[int, int, int]:

    # Assert that the arrays have the required length, and do the convolution
    assert len(array_b1) == len(array_b2) == 3564
    n_collisions_ip1_and_5 = int(array_b1 @ array_b2)
    n_collisions_ip2 = int(np.roll(array_b1, 891) @ array_b2)
    n_collisions_ip8 = int(np.roll(array_b1, 2670) @ array_b2)

    return n_collisions_ip1_and_5, n_collisions_ip2, n_collisions_ip8


# ==================================================================================================
# --- Block object ---
# ==================================================================================================

compute_collision_schedule = Block(
    "compute_collision_schedule",
    compute_collision_schedule_function,
    dict_imports=dict_imports,
)
