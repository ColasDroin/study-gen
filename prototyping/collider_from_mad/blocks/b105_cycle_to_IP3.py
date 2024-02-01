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
def cycle_to_IP3_function(
    mad: Madx,
) -> Madx:
    mad.input("""
    !Cycling w.r.t. to IP3 (mandatory to find closed orbit in collision in the presence of errors)
    if (mylhcbeam<3){
    seqedit, sequence=lhcb1; flatten; cycle, start=IP3; flatten; endedit;
    };
    seqedit, sequence=lhcb2; flatten; cycle, start=IP3; flatten; endedit;
    """)

    return mad


# ==================================================================================================
# --- Block object ---
# ==================================================================================================

cycle_to_IP3 = Block(
    "cycle_to_IP3",
    cycle_to_IP3_function,
    dict_imports=dict_imports,
)
