# ==================================================================================================
# --- Imports ---
# Some imports are optional as they're also declared in dict_imports, but it's
# helpful to declare them here for linting.
# ==================================================================================================
# Standard library imports
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
}


# ==================================================================================================
# --- Block function ---
# ==================================================================================================
def prepare_mad_environment_function(links: dict[str, Any]) -> tuple[str, str, Madx, str, Madx]:
    # Make mad environment
    xm.make_mad_environment(links=links)

    # Start mad for all beams
    sequence_name_b1 = "lhcb1"
    sequence_name_b2 = "lhcb2"
    sequence_name_b4 = "lhcb4"
    mad_b1b2 = Madx(command_log="mad_b1b2.log")
    mad_b4 = Madx(command_log="mad_b4.log")

    return sequence_name_b1, sequence_name_b2, mad_b1b2, sequence_name_b4, mad_b4


# ==================================================================================================
# --- Block object ---
# ==================================================================================================

prepare_mad_environment = Block(
    "prepare_mad_environment",
    prepare_mad_environment_function,
    dict_imports=dict_imports,
)
