# ==================================================================================================
# --- Imports ---
# ==================================================================================================
import importlib
from collections import OrderedDict

from ..block import Block

# This is needed to get the import and the import alias for code generation
dict_imports = {"math": "math"}
for module, alias in dict_imports.items():
    vars()[alias] = importlib.import_module(module)


# ==================================================================================================
# --- Block function ---
# ==================================================================================================
def factorial_function(a: int) -> int:
    """Dummy docstring"""
    # Compute factorial of a
    return math.factorial(a)


# ==================================================================================================
# --- Block object ---
# ==================================================================================================

factorial = Block(
    factorial_function,
    dict_imports=dict_imports,
    dict_output=OrderedDict([("output_factorial", int)]),
)
