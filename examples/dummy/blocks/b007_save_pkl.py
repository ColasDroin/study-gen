# ==================================================================================================
# --- Imports ---
# ==================================================================================================
# Standard library imports
import pickle
from typing import Any

# Third party imports
# Local imports
from study_gen.block import Block

# This is needed to get the import and the import statement for code generation
dict_imports = {"pickle": "import pickle", "Any": "from typing import Any"}


# ==================================================================================================
# --- Block function ---
# ==================================================================================================
def save_pkl_function(output: Any, path_output: str) -> None:
    # Get output name
    # output_str = f"{output=}".split("=")[0]
    with open(path_output, "wb") as f:
        pickle.dump(output, f)


# ==================================================================================================
# --- Block object ---
# ==================================================================================================

save_pkl = Block("save_pkl", save_pkl_function, dict_imports=dict_imports)
