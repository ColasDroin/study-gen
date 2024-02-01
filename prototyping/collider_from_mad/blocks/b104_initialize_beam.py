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
def initialize_beam_function(
    mad: Madx,
) -> Madx:
    mad.input("""
    nrj=7000;
    beam,particle=proton,sequence=lhcb1,energy=nrj,npart=1.15E11,sige=4.5e-4;
    beam,particle=proton,sequence=lhcb2,energy=nrj,bv = -1,npart=1.15E11,sige=4.5e-4;
    """)

    return mad


# ==================================================================================================
# --- Block object ---
# ==================================================================================================

initialize_beam = Block(
    "initialize_beam",
    initialize_beam_function,
    dict_imports=dict_imports,
)
