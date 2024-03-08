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

    # Convert to dataframe
    particles_df = pd.DataFrame(particles_dict)

    # ! Very important, otherwise the particles will be mixed in each subset
    # Sort by parent_particle_id
    particles_df = particles_df.sort_values("parent_particle_id")

    # Assign the old id to the sorted dataframe
    particles_df["particle_id"] = particle_id

    # Save output
    particles_df.to_parquet(path_output_particles)


# ==================================================================================================
# --- Block object ---
# ==================================================================================================

dump_tracked_particles = Block(
    "dump_tracked_particles",
    dump_tracked_particles_function,
    dict_imports=dict_imports,
)
