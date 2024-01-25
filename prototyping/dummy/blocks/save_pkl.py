# ==================================================================================================
# --- Imports ---
# ==================================================================================================
import importlib
import pickle

from study_gen.block import Block

# This is needed to get the import and the import statement for code generation
dict_imports = {"pickle": "import pickle", "Any": "from typing import Any"}
for module, import_statement in dict_imports.items():
    exec(import_statement)


# ==================================================================================================
# --- Block function ---
# ==================================================================================================
def save_pkl_function(output: Any, path_output: str) -> None:
    # Get output name
    # output_str = f"{output=}".split("=")[0]
    with open(path_output, "wb") as f:
        pickle.dump(output, f)


# ==================================================================================================
# --- Block object ---
# ==================================================================================================

save_pkl = Block("save_pkl", save_pkl_function, dict_imports=dict_imports)
