# ==================================================================================================
# --- Imports ---
# ==================================================================================================
import importlib
import pickle

from ..block import Block

# This is needed to get the import and the import statement for code generation
dict_imports = {"pickle": "import pickle", "Any": "from typing import Any"}
for module, import_statement in dict_imports.items():
    exec(import_statement)


# ==================================================================================================
# --- Block function ---
# ==================================================================================================
def save_pkl_function(output: Any) -> None:
    # Get output name
    output_str = f"{output=}".split("=")[0]
    with open(output_str, "wb") as f:
        pickle.dump(output, f)


# ==================================================================================================
# --- Block object ---
# ==================================================================================================

save_pkl = Block(save_pkl_function)
