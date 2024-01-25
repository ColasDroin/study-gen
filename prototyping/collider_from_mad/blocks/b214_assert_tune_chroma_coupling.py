# ==================================================================================================
# --- Imports ---
# Some imports are optional as they're also declared in dict_imports, but it's
# helpful to declare them here for linting.
# ==================================================================================================
# Standard library imports

# Third party imports
import numpy as np
import xtrack as xt

# Local imports
from study_gen.block import Block

# Imports needed for block to work (not detected by linting tools)
dict_imports = {"xt": "import xtrack as xt", "np": "import numpy as np"}


# ==================================================================================================
# --- Block function ---
# ==================================================================================================
def assert_tune_chroma_coupling_function(
    collider: xt.Multiline,
    conf_qx: dict,
    conf_qy: dict,
    conf_dqx: dict,
    conf_dqy: dict,
    delta_cmr: float,
) -> None:

    for line_name in ["lhcb1", "lhcb2"]:
        tw = collider[line_name].twiss()
        assert np.isclose(
            tw.qx, conf_qx[line_name], atol=1e-4
        ), f"tune_x is not correct for {line_name}. Expected {conf_qx[line_name]}, got {tw.qx}"
        assert np.isclose(
            tw.qy, conf_qy[line_name], atol=1e-4
        ), f"tune_y is not correct for {line_name}. Expected {conf_qy[line_name]}, got {tw.qy}"
        assert np.isclose(
            tw.dqx,
            conf_dqx[line_name],
            rtol=1e-2,
        ), (
            f"chromaticity_x is not correct for {line_name}. Expected"
            f" {conf_dqx[line_name]}, got {tw.dqx}"
        )
        assert np.isclose(
            tw.dqy,
            conf_dqy[line_name],
            rtol=1e-2,
        ), (
            f"chromaticity_y is not correct for {line_name}. Expected"
            f" {conf_dqy[line_name]}, got {tw.dqy}"
        )

        assert np.isclose(
            tw.c_minus,
            delta_cmr,
            atol=5e-3,
        ), f"linear coupling is not correct for {line_name}. Expected {delta_cmr}, got {tw.c_minus}"


# ==================================================================================================
# --- Block object ---
# ==================================================================================================

add_linear_coupling = Block(
    "assert_tune_chroma_coupling",
    assert_tune_chroma_coupling_function,
    dict_imports=dict_imports,
)
