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
dict_imports = {
    "xt": "import xtrack as xt",
}


# ==================================================================================================
# --- Block function ---
# ==================================================================================================
def check_xsuite_twiss_function(collider: xt.Multiline) -> None:
    # Twiss in 4D just to ensure no error is raised at this point
    collider["lhcb1"].twiss(method="4d")
    collider["lhcb2"].twiss(method="4d")
    return None


# ==================================================================================================
# --- Block object ---
# ==================================================================================================

check_xsuite_twiss = Block(
    "check_xsuite_twiss",
    check_xsuite_twiss_function,
    dict_imports=dict_imports,
)
