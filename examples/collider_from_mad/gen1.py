# ==================================================================================================
# --- Imports
# ==================================================================================================

from cpymad.madx import Madx
import xmask as xm
from typing import Any
import numpy as np
import xtrack as xt
import os
import shutil

# ==================================================================================================
# --- Blocks
# ==================================================================================================


def prepare_mad_environment_function(
    links: dict[str, Any]
) -> tuple[str, str, Madx, str, Madx]:
    # Make mad environment
    xm.make_mad_environment(links=links)

    # Start mad for all beams
    sequence_name_b1 = "lhcb1"
    sequence_name_b2 = "lhcb2"
    sequence_name_b4 = "lhcb4"
    mad_b1b2 = Madx(command_log="mad_b1b2.log")
    mad_b4 = Madx(command_log="mad_b4.log")

    return sequence_name_b1, sequence_name_b2, mad_b1b2, sequence_name_b4, mad_b4


def build_initial_hllhc_sequence_function(
    mad: Madx,
    beam: int,
) -> Madx:

    # Select beam
    mad.input(f"mylhcbeam = {beam}")

    # Build sequence
    mad.input(
        """
    ! Build sequence
    option, -echo,-warn,-info;
    if (mylhcbeam==4){
        call,file="acc-models-lhc/lhcb4.seq";
    }
    else {
        call,file="acc-models-lhc/lhc.seq";
    };
    !Install HL-LHC
    call, file="acc-models-lhc/hllhc_sequence.madx";
    ! Get the toolkit
    call,file="acc-models-lhc/toolkit/macro.madx";
    option, -echo, warn,-info;
    """
    )

    return mad


def initialize_beam_function(
    mad: Madx,
) -> Madx:
    mad.input(
        """
    nrj=7000;
    beam,particle=proton,sequence=lhcb1,energy=nrj,npart=1.15E11,sige=4.5e-4;
    beam,particle=proton,sequence=lhcb2,energy=nrj,bv = -1,npart=1.15E11,sige=4.5e-4;
    """
    )

    return mad


def set_twiss_function(
    mad: Madx,
) -> Madx:
    mad.input(
        """
    ! Set twiss formats for MAD-X parts (macro from opt. toolkit)
    exec, twiss_opt;
    """
    )

    return mad


def apply_acsca_fix_hllhc_function(
    mad: Madx,
) -> Madx:
    mad.input(
        """
    l.mbh = 0.001000;
    ACSCA, HARMON := HRF400;
    
    ACSCA.D5L4.B1, VOLT := VRF400/8, LAG := LAGRF400.B1, HARMON := HRF400;
    ACSCA.C5L4.B1, VOLT := VRF400/8, LAG := LAGRF400.B1, HARMON := HRF400;
    ACSCA.B5L4.B1, VOLT := VRF400/8, LAG := LAGRF400.B1, HARMON := HRF400;
    ACSCA.A5L4.B1, VOLT := VRF400/8, LAG := LAGRF400.B1, HARMON := HRF400;
    ACSCA.A5R4.B1, VOLT := VRF400/8, LAG := LAGRF400.B1, HARMON := HRF400;
    ACSCA.B5R4.B1, VOLT := VRF400/8, LAG := LAGRF400.B1, HARMON := HRF400;
    ACSCA.C5R4.B1, VOLT := VRF400/8, LAG := LAGRF400.B1, HARMON := HRF400;
    ACSCA.D5R4.B1, VOLT := VRF400/8, LAG := LAGRF400.B1, HARMON := HRF400;
    ACSCA.D5L4.B2, VOLT := VRF400/8, LAG := LAGRF400.B2, HARMON := HRF400;
    ACSCA.C5L4.B2, VOLT := VRF400/8, LAG := LAGRF400.B2, HARMON := HRF400;
    ACSCA.B5L4.B2, VOLT := VRF400/8, LAG := LAGRF400.B2, HARMON := HRF400;
    ACSCA.A5L4.B2, VOLT := VRF400/8, LAG := LAGRF400.B2, HARMON := HRF400;
    ACSCA.A5R4.B2, VOLT := VRF400/8, LAG := LAGRF400.B2, HARMON := HRF400;
    ACSCA.B5R4.B2, VOLT := VRF400/8, LAG := LAGRF400.B2, HARMON := HRF400;
    ACSCA.C5R4.B2, VOLT := VRF400/8, LAG := LAGRF400.B2, HARMON := HRF400;
    ACSCA.D5R4.B2, VOLT := VRF400/8, LAG := LAGRF400.B2, HARMON := HRF400;
    """
    )

    return mad


def slice_sequence_function(
    mad: Madx,
) -> Madx:
    mad.input(
        """
    ! Slice nominal sequence
    exec, myslice;
    """
    )

    return mad


def cycle_to_IP3_function(
    mad: Madx,
) -> Madx:
    mad.input(
        """
    !Cycling w.r.t. to IP3 (mandatory to find closed orbit in collision in the presence of errors)
    if (mylhcbeam<3){
    seqedit, sequence=lhcb1; flatten; cycle, start=IP3; flatten; endedit;
    };
    seqedit, sequence=lhcb2; flatten; cycle, start=IP3; flatten; endedit;
    """
    )

    return mad


def incorporate_CC_function(
    mad: Madx,
) -> Madx:
    mad.input(
        """
    ! Install crab cavities (they are off)
    call, file='acc-models-lhc/toolkit/enable_crabcavities.madx';
    on_crab1 = 0;
    on_crab5 = 0;
    """
    )

    return mad


def build_hllhc_sequence_function(
    beam_name: str,
    mad: Madx,
    apply_acsca_fix: bool,
    cycle_to_IP3: bool,
    incorporate_CC: bool,
) -> Madx:

    # Get beam number
    if beam_name == "b1b2":
        beam = 1
    elif beam_name == "b4":
        beam = 4
    else:
        raise ValueError("Beam name not recognized.")

    # Build initial sequence
    mad = build_initial_hllhc_sequence_function(mad, beam)

    # Apply asca fix, doesn't work otherwise
    if apply_acsca_fix:
        mad = apply_acsca_fix_hllhc_function(mad)

    # Slice nominal sequence for tracking
    mad = slice_sequence_function(mad)

    # Define beam (for b1/b2)
    if beam < 3:
        mad = initialize_beam_function(mad)

    # Install error placeholders (configured later)
    xm.lhc.install_errors_placeholders_hllhc(mad)

    # Get IP3 as position 0
    if cycle_to_IP3:
        mad = cycle_to_IP3_function(mad)

    # Incorporate crab cavities (off by default)
    if incorporate_CC:
        mad = incorporate_CC_function(mad)

    # Set twiss format
    mad = set_twiss_function(mad)

    return mad


def apply_optics_function(
    mad: Madx,
    optics_file: str,
) -> Madx:
    mad.call(optics_file)
    # A knob redefinition
    mad.input("on_alice := on_alice_normalized * 7000./nrj;")
    mad.input("on_lhcb := on_lhcb_normalized * 7000./nrj;")

    return mad


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
            assert np.isclose(
                df.loc[f"ip{my_ip}"].betx, mad.globals[f"betx_IP{my_ip}"], rtol=1e-02
            )
            assert np.isclose(
                df.loc[f"ip{my_ip}"].bety, mad.globals[f"bety_IP{my_ip}"], rtol=1e-02
            )
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


def build_collider_function(
    mad_b1b2: Madx,
    mad_b4: Madx,
    beam_config: dict[str, Any],
    enable_imperfections: bool,
    enable_knob_synthesis: bool,
    rename_coupling_knobs: bool,
    pars_for_imperfections: dict[str, int],
    ver_hllhc_optics: float,
) -> xt.Multiline:
    # Build collider
    collider = xm.lhc.build_xsuite_collider(
        sequence_b1=mad_b1b2.sequence.lhcb1,
        sequence_b2=mad_b1b2.sequence.lhcb2,
        sequence_b4=mad_b4.sequence.lhcb2,
        beam_config=beam_config,
        enable_imperfections=enable_imperfections,
        enable_knob_synthesis=enable_knob_synthesis,
        rename_coupling_knobs=rename_coupling_knobs,
        pars_for_imperfections=pars_for_imperfections,
        ver_lhc_run=None,
        ver_hllhc_optics=ver_hllhc_optics,
    )

    return collider


def build_trackers_function(
    collider: xt.Multiline,
    context: Any = None,
) -> xt.Multiline:

    if context is None:
        # Build trackers (CPU context by defaults)
        collider.build_trackers()

    else:
        # Build trackers (GPU context)
        collider.build_trackers(_context=context)

    return collider


def check_xsuite_twiss_function(collider: xt.Multiline) -> None:
    # Twiss in 4D just to ensure no error is raised at this point
    collider["lhcb1"].twiss(method="4d")
    collider["lhcb2"].twiss(method="4d")


def activate_RF_function(
    collider: xt.Multiline,
) -> xt.Multiline:

    # Define a RF system for twissing (values are not so immportant as they're defined later)
    dic_rf = {"vrf400": 16.0, "lagrf400.b1": 0.5, "lagrf400.b2": 0.5}
    print("Now Computing Twiss assuming:")
    for knob, val in dic_rf.items():
        print(f"\t{knob} = {val}")

    # Apply the RF system
    for knob, val in dic_rf.items():
        collider.vars[knob] = val

    return collider


def display_xsuite_lattice_function(collider: xt.Multiline) -> None:
    for sequence_name in ["lhcb1", "lhcb2"]:
        line = collider[sequence_name]
        tw = line.twiss(method="6d", matrix_stability_tol=100)
        print(f"--- Now displaying Twiss result at all IPS for line {line}---")
        print(tw[:, "ip.*"])
        print(f"--- Now displaying Qx and Qy for line {line}---")
        print(tw.qx, tw.qy)


def clean_temp_files_function() -> None:
    # Remove all the temporaty files created in the process of building collider
    os.remove("mad_collider.log")
    os.remove("mad_b4.log")
    shutil.rmtree("temp")
    os.unlink("errors")
    os.unlink("acc-models-lhc")


def dump_collider_json_function(
    collider: xt.Multiline,
    name_collider: str,
) -> None:
    collider.to_json(name_collider + ".json")


# ==================================================================================================
# --- Main
# ==================================================================================================


def main(
    links: dict,
    apply_acsca_fix: bool,
    cycle_to_IP3: bool,
    incorporate_CC: bool,
    optics_file: str,
    beam_config: dict,
    enable_imperfections: bool,
    enable_knob_synthesis: bool,
    rename_coupling_knobs: bool,
    pars_for_imperfections: dict,
    ver_hllhc_optics: float,
    path_base_collider: str,
) -> None:

    sequence_name_b1, sequence_name_b2, mad_b1b2, sequence_name_b4, mad_b4 = (
        prepare_mad_environment_function(links)
    )
    mad_b1b2 = build_hllhc_sequence_function(
        sequence_name_b1, mad_b1b2, apply_acsca_fix, cycle_to_IP3, incorporate_CC
    )
    mad_b4 = build_hllhc_sequence_function(
        sequence_name_b4, mad_b4, apply_acsca_fix, cycle_to_IP3, incorporate_CC
    )
    mad_b1b2 = apply_optics_function(mad_b1b2, optics_file)
    check_madx_lattice_function(mad_b1b2, sequence_name_b1)
    check_madx_lattice_function(mad_b1b2, sequence_name_b2)
    mad_b4 = apply_optics_function(mad_b4, optics_file)
    check_madx_lattice_function(mad_b4, sequence_name_b2)
    collider = build_collider_function(
        mad_b1b2,
        mad_b4,
        beam_config,
        enable_imperfections,
        enable_knob_synthesis,
        rename_coupling_knobs,
        pars_for_imperfections,
        ver_hllhc_optics,
    )
    collider = build_trackers_function(collider)
    check_xsuite_twiss_function(collider)
    collider = activate_RF_function(collider)
    display_xsuite_lattice_function(collider)
    clean_temp_files_function()
    dump_collider_json_function(collider, path_base_collider)


# ==================================================================================================
# --- Parameters
# ==================================================================================================

# Declare parameters
links = {"acc-models-lhc": "../../../modules/hllhc16"}
apply_acsca_fix = True
cycle_to_IP3 = True
incorporate_CC = True
optics_file = "acc-models-lhc/strengths/flat/opt_flathv_500_2000_thin.madx"
beam_config = {"lhcb1": {"beam_energy_tot": 7000}, "lhcb2": {"beam_energy_tot": 7000}}
enable_imperfections = False
enable_knob_synthesis = True
rename_coupling_knobs = True
pars_for_imperfections = {
    "par_myseed": 1,
    "par_correct_for_D2": 0,
    "par_correct_for_MCBX": 0,
    "par_on_errors_LHC": 1,
    "par_off_errors_Q4_inIP15": 0,
    "par_off_errors_Q5_inIP15": 0,
    "par_on_errors_MBH": 1,
    "par_on_errors_Q4": 1,
    "par_on_errors_D2": 1,
    "par_on_errors_D1": 1,
    "par_on_errors_IT": 1,
    "par_on_errors_MCBRD": 0,
    "par_on_errors_MCBXF": 0,
    "par_on_errors_NLC": 0,
    "par_write_errortable": 1,
}
ver_hllhc_optics = 1.6
path_base_collider = "base_collider.json"


# ==================================================================================================
# --- Script
# ==================================================================================================

if __name__ == "__main__":
    main(
        links,
        apply_acsca_fix,
        cycle_to_IP3,
        incorporate_CC,
        optics_file,
        beam_config,
        enable_imperfections,
        enable_knob_synthesis,
        rename_coupling_knobs,
        pars_for_imperfections,
        ver_hllhc_optics,
        path_base_collider,
    )
