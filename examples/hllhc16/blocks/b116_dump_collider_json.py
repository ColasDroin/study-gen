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
def dump_collider_json_function(
    collider: xt.Multiline,
    name_collider: str,
) -> None:
    if not name_collider.endswith(".json"):
        name_collider += ".json"
    collider.to_json(name_collider)


# ==================================================================================================
# --- Block object ---
# ==================================================================================================

dump_collider_json = Block(
    "dump_collider_json",
    dump_collider_json_function,
    dict_imports=dict_imports,
)
