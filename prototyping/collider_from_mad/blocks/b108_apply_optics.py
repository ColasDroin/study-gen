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
def apply_optics_function(
    mad: Madx,
    optics_file: str,
) -> Madx:
    mad.call(optics_file)
    # A knob redefinition
    mad.input("on_alice := on_alice_normalized * 7000./nrj;")
    mad.input("on_lhcb := on_lhcb_normalized * 7000./nrj;")

    return mad


# ==================================================================================================
# --- Block object ---
# ==================================================================================================

apply_optics = Block(
    "apply_optics",
    apply_optics_function,
    dict_imports=dict_imports,
)
