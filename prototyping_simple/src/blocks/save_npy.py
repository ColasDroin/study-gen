# ==================================================================================================
# --- Imports ---
# ==================================================================================================
import importlib

from ..block import Block

# This is needed to get the import and the import alias for code generation
dict_imports = {"numpy": "np"}
for module, alias in dict_imports.items():
    vars()[alias] = importlib.import_module(module)


# ==================================================================================================
# --- Block function ---
# ==================================================================================================
def save_npy_function(output: np.ndarray) -> None:
    np.save(f"{output=}".split("=")[0], output)


# ==================================================================================================
# --- Block object ---
# ==================================================================================================

save_npy = Block(save_npy_function)
