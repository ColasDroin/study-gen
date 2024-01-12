# ==================================================================================================
# --- Imports ---
# ==================================================================================================
import cpymad


# ==================================================================================================
# --- Block ---
# ==================================================================================================
def cycle_madx_sequence(mad: cpymad.madx.Madx) -> cpymad.madx.Madx:

    # Cycle w.r.t. to IP3 (mandatory to find closed orbit in collision in the presence of errors)
    mad.input("""
    if (mylhcbeam<3){
    seqedit, sequence=lhcb1; flatten; cycle, start=IP3; flatten; endedit;
    };
    seqedit, sequence=lhcb2; flatten; cycle, start=IP3; flatten; endedit;
    """)

    return mad
