# ==================================================================================================
# --- Imports ---
# ==================================================================================================
import cpymad


# ==================================================================================================
# --- Block ---
# ==================================================================================================
def apply_optics_madx_sequence(mad: cpymad.madx.Madx, optics_file_path: str) -> cpymad.madx.Madx:

    # Apply optics
    mad.call(optics_file_path)

    # A knob redefinition
    mad.input("on_alice := on_alice_normalized * 7000./nrj;")
    mad.input("on_lhcb := on_lhcb_normalized * 7000./nrj;")

    return mad
