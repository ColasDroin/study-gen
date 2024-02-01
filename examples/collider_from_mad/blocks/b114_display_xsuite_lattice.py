# ==================================================================================================
# --- Imports ---
# Some imports are optional as they're also declared in dict_imports, but it's
# helpful to declare them here for linting.
# ==================================================================================================
# Third party imports
import xtrack as xt

# Local imports
from study_gen.block import Block

# Imports needed for block to work (not detected by linting tools)
dict_imports = {"xt": "import xtrack as xt"}


# ==================================================================================================
# --- Block function ---
# ==================================================================================================
def display_xsuite_lattice_function(collider: xt.Multiline) -> None:
    for sequence_name in ["lhcb1", "lhcb2"]:
        line = collider[sequence_name]
        tw = line.twiss(method="6d", matrix_stability_tol=100)
        print(f"--- Now displaying Twiss result at all IPS for line {line}---")
        print(tw[:, "ip.*"])
        print(f"--- Now displaying Qx and Qy for line {line}---")
        print(tw.qx, tw.qy)


# ==================================================================================================
# --- Block object ---
# ==================================================================================================

display_xsuite_lattice = Block(
    "display_xsuite_lattice",
    display_xsuite_lattice_function,
    dict_imports=dict_imports,
)
