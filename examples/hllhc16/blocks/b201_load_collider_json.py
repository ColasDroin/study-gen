# ==================================================================================================
# --- Imports ---
# Some imports are optional as they're also declared in dict_imports, but it's
# helpful to declare them here for linting.
# ==================================================================================================
# Standard library imports

# Third party imports
import xtrack as xt

# Local imports
from study_gen.block import Block

# Imports needed for block to work (not detected by linting tools)
dict_imports = {"xt": "import xtrack as xt"}
# ==================================================================================================
# --- Block function ---
# ==================================================================================================


def load_collider_json_function(path_base_collider: str) -> xt.Multiline:
    return xt.Multiline.from_json(path_base_collider)


# ==================================================================================================
# --- Block object ---
# ==================================================================================================

load_collider_json = Block(
    "load_collider_json",
    load_collider_json_function,
)
