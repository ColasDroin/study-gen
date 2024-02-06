# ==================================================================================================
# --- Imports ---
# Some imports are optional as they're also declared in dict_imports, but it's
# helpful to declare them here for linting.
# ==================================================================================================
# Standard library imports
import time

# Third party imports
import pandas as pd
import xpart as xp
import xtrack as xt

from study_gen.block import Block

dict_imports = {
    "pd": "import pandas as pd",
    "xp": "import xpart as xp",
    "time": "import time as time",
    "xt": "import xtrack as xt",
}


# ==================================================================================================
# --- Block function ---
# ==================================================================================================
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
    print(f"Elapsed time per particle per turn: {(b-a)/particles._capacity/n_turns*1e6} us")

    return particles


# ==================================================================================================
# --- Block object ---
# ==================================================================================================

track = Block(
    "track",
    track_function,
    dict_imports=dict_imports,
)
