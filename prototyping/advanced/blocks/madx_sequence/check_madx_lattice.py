# ==================================================================================================
# --- Imports ---
# ==================================================================================================
import cpymad
import numpy as np


# ==================================================================================================
# --- Block ---
# ==================================================================================================
def check_madx_lattices(mad: cpymad.madx.Madx) -> None:

    # Assert that tune and chromaticities are the same for both beams
    assert mad.globals["qxb1"] == mad.globals["qxb2"]
    assert mad.globals["qyb1"] == mad.globals["qyb2"]
    assert mad.globals["qpxb1"] == mad.globals["qpxb2"]
    assert mad.globals["qpyb1"] == mad.globals["qpyb2"]

    # Assert that tune and chromaticities have the expected values
    assert np.isclose(mad.table.summ.q1, mad.globals["qxb1"], atol=1e-02)
    assert np.isclose(mad.table.summ.q2, mad.globals["qyb1"], atol=1e-02)
    assert np.isclose(mad.table.summ.dq1, mad.globals["qpxb1"], atol=1e-01)
    assert np.isclose(mad.table.summ.dq2, mad.globals["qpyb1"], atol=1e-01)

    # Assert that beta functions at IPs have the expected values
    df = mad.table.twiss.dframe()
    for my_ip in [1, 2, 5, 8]:
        assert np.isclose(df.loc[f"ip{my_ip}"].betx, mad.globals[f"betx_IP{my_ip}"], rtol=1e-02)
        assert np.isclose(df.loc[f"ip{my_ip}"].bety, mad.globals[f"bety_IP{my_ip}"], rtol=1e-02)

    # Assert that closed orbit at the IPs is zero
    assert df["x"].std() < 1e-6
    assert df["y"].std() < 1e-6
