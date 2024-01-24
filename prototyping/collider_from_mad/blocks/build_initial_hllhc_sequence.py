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
for module, import_statement in dict_imports.items():
    exec(import_statement)


# ==================================================================================================
# --- Block function ---
# ==================================================================================================
def build_initial_hllhc_sequence_function(
    mad: Madx,
    beam: int,
) -> Madx:

    # Select beam
    mad.input(f"mylhcbeam = {beam}")

    # Build sequence
    mad.input("""
    ! Build sequence
    option, -echo,-warn,-info;
    if (mylhcbeam==4){
        call,file="acc-models-lhc/lhcb4.seq";
    }
    else {
        call,file="acc-models-lhc/lhc.seq";
    };
    !Install HL-LHC
    call, file="acc-models-lhc/hllhc_sequence.madx";
    ! Get the toolkit
    call,file="acc-models-lhc/toolkit/macro.madx";
    option, -echo, warn,-info;
    """)

    return mad


# ==================================================================================================
# --- Block object ---
# ==================================================================================================

build_initial_hllhc_sequence = Block(
    "build_initial_hllhc_sequence",
    function=build_initial_hllhc_sequence_function,
    dict_imports=dict_imports,
    dict_output=OrderedDict([("output_build_initial_hllhc_sequence", Madx)]),
)
