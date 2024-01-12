# ==================================================================================================
# --- Imports ---
# ==================================================================================================
import xtrack


# ==================================================================================================
# --- Block ---
# ==================================================================================================
def check_xsuite_lattices(line: xtrack.Line) -> None:

    # Twiss line
    tw = line.twiss(method="6d", matrix_stability_tol=100)
    print(f"--- Now displaying Twiss result at all IPS for line {line}---")
    print(tw[:, "ip.*"])
    # Print qx and qy
    print(f"--- Now displaying Qx and Qy for line {line}---")
    print(tw.qx, tw.qy)
