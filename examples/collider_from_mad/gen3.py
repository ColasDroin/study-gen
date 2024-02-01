# ==================================================================================================
# --- Imports
# ==================================================================================================

import numpy as np
import itertools
import os
import pandas as pd

# ==================================================================================================
# --- Blocks
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


def write_particles_distribution_function(
    particle_list: list[list[tuple[int, float, float]]]
) -> None:
    # Write distribution to parquet files
    distributions_folder = "particles"
    os.makedirs(distributions_folder, exist_ok=True)
    for idx_chunk, my_list in enumerate(particle_list):
        pd.DataFrame(
            my_list,
            columns=[
                "particle_id",
                "normalized amplitude in xy-plane",
                "angle in xy-plane [deg]",
            ],
        ).to_parquet(f"{distributions_folder}/{idx_chunk:02}.parquet")


# ==================================================================================================
# --- Main
# ==================================================================================================


def main(r_min: float, r_max: float, n_r: int, n_angles: int, n_split: int) -> None:

    particle_list = build_particles_distribution_function(
        r_min, r_max, n_r, n_angles, n_split
    )
    write_particles_distribution_function(particle_list)


# ==================================================================================================
# --- Parameters
# ==================================================================================================

# Declare parameters
r_min = 2.0
r_max = 10.0
n_r = 256
n_angles = 5
n_split = 15


# ==================================================================================================
# --- Script
# ==================================================================================================

if __name__ == "__main__":
    main(r_min, r_max, n_r, n_angles, n_split)
