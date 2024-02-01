# ==================================================================================================
# --- Imports ---
# Some imports are optional as they're also declared in dict_imports, but it's
# helpful to declare them here for linting.
# ==================================================================================================
# Standard library imports
import json
import os

# Local imports
from study_gen.block import Block

# Imports needed for block to work (not detected by linting tools)
dict_imports = {"os": "import os", "json": "import json"}


# ==================================================================================================
# --- Block function ---
# ==================================================================================================


def dump_orbit_correction_files_function(
    correction_setup: dict, output_folder: str = "correction"
) -> str:
    os.makedirs(output_folder, exist_ok=True)
    for nn in ["lhcb1", "lhcb2"]:
        with open(f"{output_folder}/corr_co_{nn}.json", "w") as fid:
            json.dump(correction_setup[nn], fid, indent=4)
    return output_folder


# ==================================================================================================
# --- Block object ---
# ==================================================================================================

dump_orbit_correction_files = Block(
    "dump_orbit_correction_files",
    dump_orbit_correction_files_function,
    dict_imports=dict_imports,
)
