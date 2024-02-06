# ==================================================================================================
# --- Imports ---
# Some imports are optional as they're also declared in dict_imports, but it's
# helpful to declare them here for linting.
# ==================================================================================================
# Standard library imports

# Third party imports
import pandas as pd
import xpart as xp

# Local imports
from study_gen.block import Block

dict_imports = {
    "pd": "import pandas as pd",
    "xp": "import xpart as xp",
}


# ==================================================================================================
# --- Block function ---
# ==================================================================================================
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


# ==================================================================================================
# --- Block object ---
# ==================================================================================================

dump_tracked_particles = Block(
    "dump_tracked_particles",
    dump_tracked_particles_function,
    dict_imports=dict_imports,
)
