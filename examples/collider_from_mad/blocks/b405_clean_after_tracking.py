# ==================================================================================================
# --- Imports ---
# Some imports are optional as they're also declared in dict_imports, but it's
# helpful to declare them here for linting.
# ==================================================================================================
# Standard library imports

# Third party imports
import os

# Local imports
from study_gen.block import Block

dict_imports = {
    "os": "import os",
}


# ==================================================================================================
# --- Block function ---
# ==================================================================================================
def clean_after_tracking_function() -> None:
    # Remote the correction folder, and potential C files remaining
    try:
        os.system("rm -rf correction")
        os.system("rm -f *.cc")
    except Exception:
        pass


# ==================================================================================================
# --- Block object ---
# ==================================================================================================

clean_after_tracking = Block(
    "clean_after_tracking",
    clean_after_tracking_function,
    dict_imports=dict_imports,
)
