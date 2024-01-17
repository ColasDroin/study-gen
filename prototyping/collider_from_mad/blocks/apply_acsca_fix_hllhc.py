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
def apply_acsca_fix_hllhc_function(
    mad: Madx,
) -> Madx:
    mad.input("""
    l.mbh = 0.001000;
    ACSCA, HARMON := HRF400;
    
    ACSCA.D5L4.B1, VOLT := VRF400/8, LAG := LAGRF400.B1, HARMON := HRF400;
    ACSCA.C5L4.B1, VOLT := VRF400/8, LAG := LAGRF400.B1, HARMON := HRF400;
    ACSCA.B5L4.B1, VOLT := VRF400/8, LAG := LAGRF400.B1, HARMON := HRF400;
    ACSCA.A5L4.B1, VOLT := VRF400/8, LAG := LAGRF400.B1, HARMON := HRF400;
    ACSCA.A5R4.B1, VOLT := VRF400/8, LAG := LAGRF400.B1, HARMON := HRF400;
    ACSCA.B5R4.B1, VOLT := VRF400/8, LAG := LAGRF400.B1, HARMON := HRF400;
    ACSCA.C5R4.B1, VOLT := VRF400/8, LAG := LAGRF400.B1, HARMON := HRF400;
    ACSCA.D5R4.B1, VOLT := VRF400/8, LAG := LAGRF400.B1, HARMON := HRF400;
    ACSCA.D5L4.B2, VOLT := VRF400/8, LAG := LAGRF400.B2, HARMON := HRF400;
    ACSCA.C5L4.B2, VOLT := VRF400/8, LAG := LAGRF400.B2, HARMON := HRF400;
    ACSCA.B5L4.B2, VOLT := VRF400/8, LAG := LAGRF400.B2, HARMON := HRF400;
    ACSCA.A5L4.B2, VOLT := VRF400/8, LAG := LAGRF400.B2, HARMON := HRF400;
    ACSCA.A5R4.B2, VOLT := VRF400/8, LAG := LAGRF400.B2, HARMON := HRF400;
    ACSCA.B5R4.B2, VOLT := VRF400/8, LAG := LAGRF400.B2, HARMON := HRF400;
    ACSCA.C5R4.B2, VOLT := VRF400/8, LAG := LAGRF400.B2, HARMON := HRF400;
    ACSCA.D5R4.B2, VOLT := VRF400/8, LAG := LAGRF400.B2, HARMON := HRF400;
    """)

    return mad


# ==================================================================================================
# --- Block object ---
# ==================================================================================================

apply_acsca_fix_hllhc = Block(
    "apply_acsca_fix_hllhc",
    apply_acsca_fix_hllhc_function,
    dict_imports=dict_imports,
    dict_output=OrderedDict([("output_apply_acsca_fix_hllhc", Madx)]),
)
