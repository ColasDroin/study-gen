# ==================================================================================================
# --- Imports ---
# ==================================================================================================
import cpymad


# ==================================================================================================
# --- Block ---
# ==================================================================================================
def apply_fix_asca_madx_sequence(mad: cpymad.madx.Madx) -> cpymad.madx.Madx:
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
