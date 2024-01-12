# ==================================================================================================
# --- Imports ---
# ==================================================================================================
import cpymad


# ==================================================================================================
# --- Block ---
# ==================================================================================================
def build_madx_sequence(mad: cpymad.madx.Madx) -> cpymad.madx.Madx:

    # Build sequence
    mad.input("""
      ! Build sequences
      option, -echo,-warn,-info;
      if (mylhcbeam==4){
        call,file="acc-models-lhc/lhcb4.seq";
      } else {
        call,file="acc-models-lhc/lhc.seq";
      };
      !Install HL-LHC
      call, file="acc-models-lhc/hllhc_sequence.madx";
      ! Get the toolkit
      call,file="acc-models-lhc/toolkit/macro.madx";
      option, -echo, warn,-info;
      """)

    return mad
