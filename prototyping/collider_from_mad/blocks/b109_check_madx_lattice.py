# ==================================================================================================
# --- Imports ---
# Some imports are optional as they're also declared in dict_imports, but it's
# helpful to declare them here for linting.
# ==================================================================================================
# Third party imports
import numpy as np
from cpymad.madx import Madx

# Local imports
from study_gen.block import Block

# Imports needed for block to work (not detected by linting tools)
dict_imports = {"Madx": "from cpymad.madx import Madx", "np": "import numpy as np"}


# ==================================================================================================
# --- Block function ---
# ==================================================================================================
def check_madx_lattice_function(
    mad: Madx,
    sequence_name: str,
) -> None:

    # Select correct sequence and twiss
    mad.use(sequence=sequence_name)
    mad.twiss()

    # Internal mad globals asserts
    assert mad.globals["qxb1"] == mad.globals["qxb2"]
    assert mad.globals["qyb1"] == mad.globals["qyb2"]
    assert mad.globals["qpxb1"] == mad.globals["qpxb2"]
    assert mad.globals["qpyb1"] == mad.globals["qpyb2"]

    # Check that the twiss table is correct
    try:
        assert np.isclose(mad.table.summ.q1, mad.globals["qxb1"], atol=1e-02)
        assert np.isclose(mad.table.summ.q2, mad.globals["qyb1"], atol=1e-02)
    except AssertionError:
        print("WARNING: tune check failed")
        print(f"mad.table.summ.q1 = {mad.table.summ.q1}")
        print(f"mad.globals['qxb1'] = {mad.globals['qxb1']}")
        print(f"mad.table.summ.q2 = {mad.table.summ.q2}")
        print(f"mad.globals['qyb1'] = {mad.globals['qyb1']}")

    try:
        assert np.isclose(mad.table.summ.dq1, mad.globals["qpxb1"], atol=1e-01)
        assert np.isclose(mad.table.summ.dq2, mad.globals["qpyb1"], atol=1e-01)
    except AssertionError:
        print("WARNING: chromaticity check failed")
        print(f"mad.table.summ.dq1 = {mad.table.summ.dq1}")
        print(f"mad.globals['qpxb1'] = {mad.globals['qpxb1']}")
        print(f"mad.table.summ.dq2 = {mad.table.summ.dq2}")
        print(f"mad.globals['qpyb1'] = {mad.globals['qpyb1']}")

    # Check beta at IPs
    df = mad.table.twiss.dframe()
    for my_ip in [1, 2, 5, 8]:
        try:
            assert np.isclose(df.loc[f"ip{my_ip}"].betx, mad.globals[f"betx_IP{my_ip}"], rtol=1e-02)
            assert np.isclose(df.loc[f"ip{my_ip}"].bety, mad.globals[f"bety_IP{my_ip}"], rtol=1e-02)
        except AssertionError:
            print(f"WARNING: beta check failed at IP{my_ip}")
            print(f"df.loc[f'ip{my_ip}'].betx = {df.loc[f'ip{my_ip}'].betx}")
            print(f"mad.globals['betx_IP{my_ip}'] = {mad.globals['betx_IP{my_ip}']}")
            print(f"df.loc[f'ip{my_ip}'].bety = {df.loc[f'ip{my_ip}'].bety}")
            print(f"mad.globals['bety_IP{my_ip}'] = {mad.globals['bety_IP{my_ip}']}")

    # Check that closed orbit is zero everywhere
    try:
        assert df["x"].std() < 1e-6
        assert df["y"].std() < 1e-6
    except AssertionError:
        print("WARNING: closed orbit check failed")
        print(f"df['x'].std() = {df['x'].std()}")
        print(f"df['y'].std() = {df['y'].std()}")


# ==================================================================================================
# --- Block object ---
# ==================================================================================================

check_madx_lattice = Block(
    "check_madx_lattice",
    check_madx_lattice_function,
    dict_imports=dict_imports,
)
