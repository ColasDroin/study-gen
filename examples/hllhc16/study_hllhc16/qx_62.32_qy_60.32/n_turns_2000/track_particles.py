# ==================================================================================================
# --- Imports
# ==================================================================================================

import xobjects as xo
from typing import Any
import xtrack as xt
import xpart as xp
import numpy as np
import pandas as pd
import time as time
import os

# ==================================================================================================
# --- Blocks
# ==================================================================================================


def get_context_function(
    context_str: str,
) -> Any:
    if context_str == "cpu":
        return xo.ContextCpu()
    elif context_str == "cupy":
        return xo.ContextCupy()
    elif context_str == "opencl":
        return xo.ContextPyopencl()
    else:
        print("Context not recognized, using cpu")
        return xo.ContextCpu()


def load_collider_json_function(path_base_collider: str) -> xt.Multiline:
    return xt.Multiline.from_json(path_base_collider)


def build_trackers_function(
    collider: xt.Multiline,
    context: Any = None,
) -> xt.Multiline:

    if context is None:
        # Build trackers (CPU context by defaults)
        collider.build_trackers()

    else:
        # Build trackers (GPU context)
        collider.build_trackers(_context=context)

    return collider


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


def track_function(
    collider: xt.Multiline,
    particles: xp.particles.particles.Particles,
    beam: str,
    n_turns: int,
    save_input_particles: bool,
    optimize_for_tracking: bool,
    path_input_particles: str,
) -> xp.particles.particles.Particles:
    # Optimize line for tracking
    if optimize_for_tracking:
        collider[beam].optimize_for_tracking()

    # Save initial coordinates if requested
    if save_input_particles:
        pd.DataFrame(particles.to_dict()).to_parquet(path_input_particles)

    # Track
    a = time.time()
    collider[beam].track(particles, turn_by_turn_monitor=False, num_turns=n_turns)
    b = time.time()

    print(f"Elapsed time: {b-a} s")
    print(
        f"Elapsed time per particle per turn: {(b-a)/particles._capacity/n_turns*1e6} us"
    )

    return particles


def dump_tracked_particles_function(
    particles: xp.particles.particles.Particles,
    particle_id: list[int],
    path_output_particles: str,
) -> None:
    # Get particles dictionnary
    particles_dict = particles.to_dict()
    particles_dict["particle_id"] = particle_id  # type: ignore

    # Save output
    pd.DataFrame(particles_dict).to_parquet(path_output_particles)


def clean_after_tracking_function() -> None:
    # Remote the correction folder, and potential C files remaining
    with contextlib.suppress(Exception):
        os.system("rm -rf correction")
        os.system("rm -f *.cc")


# ==================================================================================================
# --- Main
# ==================================================================================================


def main(
    context_str: str,
    path_configured_collider: str,
    beam_sequence: str,
    path_input_distribution: str,
    delta_max: float,
    nemitt_x: float,
    nemitt_y: float,
    n_turns: int,
    save_input_particles: bool,
    optimize_for_tracking: bool,
    path_input_particles: str,
    path_output_particles: str,
) -> None:

    context = get_context_function(context_str)
    collider = load_collider_json_function(path_configured_collider)
    collider = build_trackers_function(collider, context)
    particles, particles_id = prepare_distribution_for_tracking_function(
        collider,
        context,
        beam_sequence,
        path_input_distribution,
        delta_max,
        nemitt_x,
        nemitt_y,
    )
    particles = track_function(
        collider,
        particles,
        beam_sequence,
        n_turns,
        save_input_particles,
        optimize_for_tracking,
        path_input_particles,
    )
    dump_tracked_particles_function(particles, particles_id, path_output_particles)
    clean_after_tracking_function()


# ==================================================================================================
# --- Parameters
# ==================================================================================================

# Declare parameters
context_str = "cpu"
path_configured_collider = "configured_collider.json"
beam_sequence = "lhcb1"
path_input_distribution = "../1_build_distr_and_collider/particles/00.parquet"
delta_max = 0.00027
nemitt_x = 2.5e-06
nemitt_y = 2.5e-06
n_turns = 2000
save_input_particles = True
optimize_for_tracking = False
path_input_particles = "input_particles.parquet"
path_output_particles = "output_particles.parquet"


# ==================================================================================================
# --- Script
# ==================================================================================================

if __name__ == "__main__":
    main(
        context_str,
        path_configured_collider,
        beam_sequence,
        path_input_distribution,
        delta_max,
        nemitt_x,
        nemitt_y,
        n_turns,
        save_input_particles,
        optimize_for_tracking,
        path_input_particles,
        path_output_particles,
    )
