# ==================================================================================================
# --- Imports ---
# Some imports are optional as they're also declared in dict_imports, but it's
# helpful to declare them here for linting.
# ==================================================================================================
# Standard library imports
from collections import OrderedDict
from typing import Any

# Third party imports
import xobjects as xo

# Local imports
from study_gen.block import Block

# Imports needed for block to work (not detected by linting tools)
dict_imports = {"xo": "import xobjects as xo", "Any": "from typing import Any"}


# ==================================================================================================
# --- Block function ---
# ==================================================================================================
def get_context_function(
    context_str: str,
) -> Any:

    if context_str == "cupy":
        context = xo.ContextCupy()
    elif context_str == "opencl":
        context = xo.ContextPyopencl()
    elif context_str == "cpu":
        context = xo.ContextCpu()
    else:
        print("Context not recognized, using cpu")
        context = xo.ContextCpu()
    return context


# ==================================================================================================
# --- Block object ---
# ==================================================================================================

get_context = Block(
    "get_context",
    get_context_function,
    dict_imports=dict_imports,
)
