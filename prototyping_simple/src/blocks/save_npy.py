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
def save_npy_function(output: Any) -> None:
    np.save(f"{output=}".split("=")[0], output)


# ==================================================================================================
# --- Block object ---
# ==================================================================================================

save_npy = Block("save_npy", save_npy_function, dict_imports=dict_imports)
