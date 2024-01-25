# ==================================================================================================
# --- Imports ---
# Some imports are optional as they're also declared in dict_imports, but it's
# helpful to declare them here for linting.
# ==================================================================================================
# Standard library imports
import json
from collections import OrderedDict

# Third party imports
import numpy as np

# Local imports
from study_gen.block import Block

# Imports needed for block to work (not detected by linting tools)
dict_imports = {"json": "import json", "np": "import numpy as np"}


# ==================================================================================================
# --- Block function ---
# ==================================================================================================
def load_filling_scheme_function(filling_scheme_path: str) -> tuple[np.ndarray, np.ndarray]:

    # Load the filling scheme
    if filling_scheme_path.endswith(".json"):
        with open(filling_scheme_path, "r") as fid:
            filling_scheme = json.load(fid)
    else:
        raise ValueError(
            f"Unknown filling scheme file format: {filling_scheme_path}. It you provided a csv"
            " file, it should have been automatically convert when running the script"
            " 001_make_folders.py. Something went wrong."
        )

    # Extract booleans beam arrays
    array_b1 = np.array(filling_scheme["beam1"])
    array_b2 = np.array(filling_scheme["beam2"])

    return array_b1, array_b2


# ==================================================================================================
# --- Block object ---
# ==================================================================================================

load_filling_scheme = Block(
    "load_filling_scheme",
    load_filling_scheme_function,
    dict_imports=dict_imports,
    dict_output=OrderedDict([("output_load_filling_scheme", tuple[np.ndarray, np.ndarray])]),
)
