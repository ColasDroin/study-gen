# ==================================================================================================
# --- Imports ---
# Some imports are optional as they're also declared in dict_imports, but it's
# helpful to declare them here for linting.
# ==================================================================================================
# Standard library imports
from collections import OrderedDict
from typing import Any

# Third party imports
import xtrack as xt

# Local imports
from study_gen.block import Block

# Imports needed for block to work (not detected by linting tools)
dict_imports = {"xt": "import xtrack as xt", "Any": "from typing import Any"}


# ==================================================================================================
# --- Block function ---
# ==================================================================================================
def build_trackers_function(
    collider: xt.Multiline,
    context: Any = None,
) -> xt.Multiline:

    if context is None:
        # Build trackers (CPU context by defaults)
        collider.build_trackers()

    else:
        # Build trackers (GPU context)
        collider.build_trackers(_context=context)

    return collider


# ==================================================================================================
# --- Block object ---
# ==================================================================================================

build_trackers = Block(
    "build_trackers",
    build_trackers_function,
    dict_imports=dict_imports,
    dict_output=OrderedDict([("output_build_trackers", xt.Multiline)]),
)
