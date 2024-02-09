# ==================================================================================================
# --- Imports ---
# ==================================================================================================
# Standard library imports
from typing import Any

# Third party imports
import numpy as np

# Local imports
from study_gen.block import Block

# This is needed to get the import and the import statement for code generation
dict_imports = {"numpy": "import numpy as np", "Any": "from typing import Any"}


# ==================================================================================================
# --- Block function ---
# ==================================================================================================
def save_npy_function(output: Any, path_output: str) -> None:
    # path_output = f"{output=}".split("=")[0]
    np.save(path_output, output)


# ==================================================================================================
# --- Block object ---
# ==================================================================================================

save_npy = Block("save_npy", save_npy_function, dict_imports=dict_imports)
