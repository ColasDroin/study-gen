# ==================================================================================================
# --- Imports ---
# ==================================================================================================
# Standard library imports
import math

# Third party imports
# Local imports
from study_gen.block import Block

# This is needed to get the import and the import statement for code generation
dict_imports = {"math": "import math"}


# ==================================================================================================
# --- Block function ---
# ==================================================================================================
def gamma_function(a: float) -> float:
    """Dummy docstring"""
    # Compute gamma function of a
    return math.gamma(a)


# ==================================================================================================
# --- Block object ---
# ==================================================================================================

gamma = Block(
    "gamma_function",
    gamma_function,
    dict_imports=dict_imports,
)
