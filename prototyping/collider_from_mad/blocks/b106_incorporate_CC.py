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
def incorporate_CC_function(
    mad: Madx,
) -> Madx:
    mad.input("""
    ! Install crab cavities (they are off)
    call, file='acc-models-lhc/toolkit/enable_crabcavities.madx';
    on_crab1 = 0;
    on_crab5 = 0;
    """)

    return mad


# ==================================================================================================
# --- Block object ---
# ==================================================================================================

incorporate_CC = Block(
    "incorporate_CC",
    incorporate_CC_function,
    dict_imports=dict_imports,
)
