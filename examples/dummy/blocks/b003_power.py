# ==================================================================================================
# --- Import statements ---
# ==================================================================================================
# Standard library imports

# Third party imports
import numpy as np

# Local imports
from study_gen.block import Block

# This is needed to get the import and the import statement for code generation
dict_imports = {"numpy": "import numpy as np"}


# ==================================================================================================
# --- Block function ---
# ==================================================================================================
def power_function(b: float, c: float) -> float:
    # Returns a at the power of b
    return np.power(b, c)


# ==================================================================================================
# --- Block ---
# ==================================================================================================

power = Block("power", power_function, dict_imports=dict_imports)
