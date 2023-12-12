# ==================================================================================================
# --- Imports ---
# ==================================================================================================
import importlib

from ..block import Block

# This is needed to get the import and the import statement for code generation
dict_imports = {"numpy": "import numpy as np", "Any": "from typing import Any"}
for module, import_statement in dict_imports.items():
    exec(import_statement)


# ==================================================================================================
# --- Block function ---
# ==================================================================================================
def load_npy_function(path: str) -> Any:
    return np.load(path)


# ==================================================================================================
# --- Block object ---
# ==================================================================================================

load_npy = Block(
    "load_npy", load_npy_function, dict_imports=dict_imports, dict_output={"output_load_npy": Any}
)
