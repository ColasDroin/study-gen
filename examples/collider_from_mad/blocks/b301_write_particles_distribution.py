# ==================================================================================================
# --- Imports ---
# Some imports are optional as they're also declared in dict_imports, but it's
# helpful to declare them here for linting.
# ==================================================================================================
# Standard library imports
import os

# Third party imports
import pandas as pd

# Local imports
from study_gen.block import Block

# Imports needed for block to work (not detected by linting tools)
dict_imports = {"os": "import os", "pandas": "import pandas as pd"}
for module, import_statement in dict_imports.items():
    exec(import_statement)


# ==================================================================================================
# --- Block function ---
# ==================================================================================================
def write_particles_distribution_function(
    particle_list: list[list[tuple[int, float, float]]]
) -> None:
    # Write distribution to parquet files
    distributions_folder = "particles"
    os.makedirs(distributions_folder, exist_ok=True)
    for idx_chunk, my_list in enumerate(particle_list):
        pd.DataFrame(
            my_list,
            columns=["particle_id", "normalized amplitude in xy-plane", "angle in xy-plane [deg]"],
        ).to_parquet(f"{distributions_folder}/{idx_chunk:02}.parquet")


# ==================================================================================================
# --- Block object ---
# ==================================================================================================

write_particles_distribution = Block(
    "write_particles_distribution",
    write_particles_distribution_function,
    dict_imports=dict_imports,
)
