# ==================================================================================================
# --- Imports ---
# ==================================================================================================
import importlib
from collections import OrderedDict

from ..block import Block

# This is needed to get the import and the import statement for code generation
dict_imports = {"math": "import math"}
for module, import_statement in dict_imports.items():
    exec(import_statement)


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
    dict_output=OrderedDict([("output_gamma", float)]),
)
