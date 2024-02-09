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
def load_npy_function(path: str) -> Any:
    return np.load(path)


# ==================================================================================================
# --- Block object ---
# ==================================================================================================

load_npy = Block("load_npy", load_npy_function, dict_imports=dict_imports)
