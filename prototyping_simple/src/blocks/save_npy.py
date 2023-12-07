# ==================================================================================================
# --- Imports ---
# ==================================================================================================
import importlib

from ..block import Block

# This is needed to get the import and the import statement for code generation
dict_imports = {"numpy": "import numpy as np"}
for module, import_statement in dict_imports.items():
    exec(import_statement)


# ==================================================================================================
# --- Block function ---
# ==================================================================================================
def save_npy_function(output: np.ndarray) -> None:
    np.save(f"{output=}".split("=")[0], output)


# ==================================================================================================
# --- Block object ---
# ==================================================================================================

save_npy = Block(save_npy_function)
