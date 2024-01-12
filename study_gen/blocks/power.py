# ==================================================================================================
# --- Import statements ---
# ==================================================================================================
import importlib
from collections import OrderedDict

from ..block import Block

# This is needed to get the import and the import statement for code generation
dict_imports = {"numpy": "import numpy as np"}
for module, import_statement in dict_imports.items():
    exec(import_statement)


# ==================================================================================================
# --- Block function ---
# ==================================================================================================
def power_function(b: float, c: float) -> float:
    # Returns a at the power of b
    return np.power(b, c)


# ==================================================================================================
# --- Block ---
# ==================================================================================================

power = Block(
    "power",
    power_function,
    dict_imports=dict_imports,
    dict_output=OrderedDict([("output_power", float)]),
)

# ==================================================================================================
# --- Script ---
# ==================================================================================================
# This is only for testing purposes
# Need to be run from the root directory with
# python -m prototyping_simple.src.blocks.power
# To prevent warning, comment out the corresponding import line in __init__.py
if __name__ == "__main__":
    print(power)
    print(power.function(2, 3))
