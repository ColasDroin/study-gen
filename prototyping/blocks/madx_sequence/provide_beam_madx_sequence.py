# ==================================================================================================
# --- Imports ---
# ==================================================================================================
import cpymad


# ==================================================================================================
# --- Block ---
# ==================================================================================================
def provide_beam_madx_sequence(mad: cpymad.madx.Madx) -> cpymad.madx.Madx:

    # Provide beam energy, number of particles and bunch length
    mad.input("""
      nrj=7000;
      beam,particle=proton,sequence=lhcb1,energy=nrj,npart=1.15E11,sige=4.5e-4;
      beam,particle=proton,sequence=lhcb2,energy=nrj,bv = -1,npart=1.15E11,sige=4.5e-4;
      """)

    return mad
