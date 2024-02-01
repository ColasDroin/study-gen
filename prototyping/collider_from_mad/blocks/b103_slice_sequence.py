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
def slice_sequence_function(
    mad: Madx,
) -> Madx:
    mad.input("""
    ! Slice nominal sequence
    exec, myslice;
    """)

    return mad


# ==================================================================================================
# --- Block object ---
# ==================================================================================================

slice_sequence = Block(
    "slice_sequence",
    slice_sequence_function,
    dict_imports=dict_imports,
)
