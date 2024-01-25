# ==================================================================================================
# --- Imports ---
# Some imports are optional as they're also declared in dict_imports, but it's
# helpful to declare them here for linting.
# ==================================================================================================
# Standard library imports
from collections import OrderedDict
from typing import Any

# Third party imports
import xmask as xm
from cpymad.madx import Madx

# Local imports
from study_gen.block import Block

# Imports needed for block to work (not detected by linting tools)
dict_imports = {
    "Madx": "from cpymad.madx import Madx",
    "xm": "import xmask as xm",
    "Any": "from typing import Any",
    "OrderedDict": "from collections import OrderedDict",
}


# ==================================================================================================
# --- Block function ---
# ==================================================================================================
def prepare_mad_environment_function(links: OrderedDict[str, Any]) -> tuple[str, Madx, str, Madx]:

    # Make mad environment
    xm.make_mad_environment(links=links)

    # Start mad for all beams
    b1b2_name = "b1b2"
    b4_name = "b4"
    mad_b1b2 = Madx(command_log="mad" + b1b2_name + ".log")
    mad_b4 = Madx(command_log="mad" + b4_name + ".log")

    return b1b2_name, mad_b1b2, b4_name, mad_b4


# ==================================================================================================
# --- Block object ---
# ==================================================================================================

prepare_mad_environment = Block(
    "prepare_mad_environment",
    prepare_mad_environment_function,
    dict_imports=dict_imports,
    dict_output=OrderedDict([("output_prepare_mad_environment", Madx)]),
)
