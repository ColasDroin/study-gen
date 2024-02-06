# ==================================================================================================
# --- Imports ---
# Some imports are optional as they're also declared in dict_imports, but it's
# helpful to declare them here for linting.
# ==================================================================================================
# Standard library imports
import os
import shutil

# Local imports
from study_gen.block import Block

# Imports needed for block to work (not detected by linting tools)
dict_imports = {"os": "import os", "shutil": "import shutil"}


# ==================================================================================================
# --- Block function ---
# ==================================================================================================
def clean_temp_files_function() -> None:
    # Remove all the temporaty files created in the process of building collider
    os.remove("mad_collider.log")
    os.remove("mad_b4.log")
    shutil.rmtree("temp")
    os.unlink("errors")
    os.unlink("acc-models-lhc")


# ==================================================================================================
# --- Block object ---
# ==================================================================================================

clean_temp_files = Block(
    "clean_temp_files",
    clean_temp_files_function,
    dict_imports=dict_imports,
)
