# ==================================================================================================
# --- Imports ---
# Some imports are optional as they're also declared in dict_imports, but it's
# helpful to declare them here for linting.
# ==================================================================================================
# Standard library imports
from collections import OrderedDict

# Third party imports
from cpymad.madx import Madx

# Local imports
from study_gen.block import Block

# Imports needed for block to work (not detected by linting tools)
dict_imports = {"Madx": "from cpymad.madx import Madx"}


# ==================================================================================================
# --- Block function ---
# ==================================================================================================
def set_twiss_function(
    mad: Madx,
) -> Madx:
    mad.input("""
    ! Set twiss formats for MAD-X parts (macro from opt. toolkit)
    exec, twiss_opt;
    """)

    return mad


# ==================================================================================================
# --- Block object ---
# ==================================================================================================

set_twiss = Block(
    "set_twiss",
    set_twiss_function,
    dict_imports=dict_imports,
)
