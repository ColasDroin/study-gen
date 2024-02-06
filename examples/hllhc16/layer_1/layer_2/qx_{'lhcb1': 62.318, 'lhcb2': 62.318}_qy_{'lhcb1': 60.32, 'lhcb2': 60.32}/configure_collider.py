# ==================================================================================================
# --- Imports
# ==================================================================================================

import os
import json
import xtrack as xt
from typing import Any
import xmask as xm
import numpy as np
from scipy.optimize import minimize_scalar
from scipy.constants import c as clight

# ==================================================================================================
# --- Blocks
# ==================================================================================================


def load_collider_json_function(path_base_collider: str) -> xt.Multiline:
    collider = xt.Multiline.from_json(path_base_collider)
    return collider


def generate_orbit_correction_setup_function() -> dict:
    correction_setup = {}
    correction_setup["lhcb1"] = {
        "IR1 left": dict(
            ref_with_knobs={"on_corr_co": 0, "on_disp": 0},
            start="e.ds.r8.b1",
            end="e.ds.l1.b1",
            vary=(
                "corr_co_acbh14.l1b1",
                "corr_co_acbh12.l1b1",
                "corr_co_acbv15.l1b1",
                "corr_co_acbv13.l1b1",
            ),
            targets=("e.ds.l1.b1",),
        ),
        "IR1 right": dict(
            ref_with_knobs={"on_corr_co": 0, "on_disp": 0},
            start="s.ds.r1.b1",
            end="s.ds.l2.b1",
            vary=(
                "corr_co_acbh13.r1b1",
                "corr_co_acbh15.r1b1",
                "corr_co_acbv12.r1b1",
                "corr_co_acbv14.r1b1",
            ),
            targets=("s.ds.l2.b1",),
        ),
        "IR5 left": dict(
            ref_with_knobs={"on_corr_co": 0, "on_disp": 0},
            start="e.ds.r4.b1",
            end="e.ds.l5.b1",
            vary=(
                "corr_co_acbh14.l5b1",
                "corr_co_acbh12.l5b1",
                "corr_co_acbv15.l5b1",
                "corr_co_acbv13.l5b1",
            ),
            targets=("e.ds.l5.b1",),
        ),
        "IR5 right": dict(
            ref_with_knobs={"on_corr_co": 0, "on_disp": 0},
            start="s.ds.r5.b1",
            end="s.ds.l6.b1",
            vary=(
                "corr_co_acbh13.r5b1",
                "corr_co_acbh15.r5b1",
                "corr_co_acbv12.r5b1",
                "corr_co_acbv14.r5b1",
            ),
            targets=("s.ds.l6.b1",),
        ),
        "IP1": dict(
            ref_with_knobs={"on_corr_co": 0, "on_disp": 0},
            start="e.ds.l1.b1",
            end="s.ds.r1.b1",
            vary=(
                "corr_co_acbch6.l1b1",
                "corr_co_acbcv5.l1b1",
                "corr_co_acbch5.r1b1",
                "corr_co_acbcv6.r1b1",
                "corr_co_acbyhs4.l1b1",
                "corr_co_acbyhs4.r1b1",
                "corr_co_acbyvs4.l1b1",
                "corr_co_acbyvs4.r1b1",
            ),
            targets=("ip1", "s.ds.r1.b1"),
        ),
        "IP2": dict(
            ref_with_knobs={"on_corr_co": 0, "on_disp": 0},
            start="e.ds.l2.b1",
            end="s.ds.r2.b1",
            vary=(
                "corr_co_acbyhs5.l2b1",
                "corr_co_acbchs5.r2b1",
                "corr_co_acbyvs5.l2b1",
                "corr_co_acbcvs5.r2b1",
                "corr_co_acbyhs4.l2b1",
                "corr_co_acbyhs4.r2b1",
                "corr_co_acbyvs4.l2b1",
                "corr_co_acbyvs4.r2b1",
            ),
            targets=("ip2", "s.ds.r2.b1"),
        ),
        "IP5": dict(
            ref_with_knobs={"on_corr_co": 0, "on_disp": 0},
            start="e.ds.l5.b1",
            end="s.ds.r5.b1",
            vary=(
                "corr_co_acbch6.l5b1",
                "corr_co_acbcv5.l5b1",
                "corr_co_acbch5.r5b1",
                "corr_co_acbcv6.r5b1",
                "corr_co_acbyhs4.l5b1",
                "corr_co_acbyhs4.r5b1",
                "corr_co_acbyvs4.l5b1",
                "corr_co_acbyvs4.r5b1",
            ),
            targets=("ip5", "s.ds.r5.b1"),
        ),
        "IP8": dict(
            ref_with_knobs={"on_corr_co": 0, "on_disp": 0},
            start="e.ds.l8.b1",
            end="s.ds.r8.b1",
            vary=(
                "corr_co_acbch5.l8b1",
                "corr_co_acbyhs4.l8b1",
                "corr_co_acbyhs4.r8b1",
                "corr_co_acbyhs5.r8b1",
                "corr_co_acbcvs5.l8b1",
                "corr_co_acbyvs4.l8b1",
                "corr_co_acbyvs4.r8b1",
                "corr_co_acbyvs5.r8b1",
            ),
            targets=("ip8", "s.ds.r8.b1"),
        ),
    }

    correction_setup["lhcb2"] = {
        "IR1 left": dict(
            ref_with_knobs={"on_corr_co": 0, "on_disp": 0},
            start="e.ds.l1.b2",
            end="e.ds.r8.b2",
            vary=(
                "corr_co_acbh13.l1b2",
                "corr_co_acbh15.l1b2",
                "corr_co_acbv12.l1b2",
                "corr_co_acbv14.l1b2",
            ),
            targets=("e.ds.r8.b2",),
        ),
        "IR1 right": dict(
            ref_with_knobs={"on_corr_co": 0, "on_disp": 0},
            start="s.ds.l2.b2",
            end="s.ds.r1.b2",
            vary=(
                "corr_co_acbh12.r1b2",
                "corr_co_acbh14.r1b2",
                "corr_co_acbv13.r1b2",
                "corr_co_acbv15.r1b2",
            ),
            targets=("s.ds.r1.b2",),
        ),
        "IR5 left": dict(
            ref_with_knobs={"on_corr_co": 0, "on_disp": 0},
            start="e.ds.l5.b2",
            end="e.ds.r4.b2",
            vary=(
                "corr_co_acbh13.l5b2",
                "corr_co_acbh15.l5b2",
                "corr_co_acbv12.l5b2",
                "corr_co_acbv14.l5b2",
            ),
            targets=("e.ds.r4.b2",),
        ),
        "IR5 right": dict(
            ref_with_knobs={"on_corr_co": 0, "on_disp": 0},
            start="s.ds.l6.b2",
            end="s.ds.r5.b2",
            vary=(
                "corr_co_acbh12.r5b2",
                "corr_co_acbh14.r5b2",
                "corr_co_acbv13.r5b2",
                "corr_co_acbv15.r5b2",
            ),
            targets=("s.ds.r5.b2",),
        ),
        "IP1": dict(
            ref_with_knobs={"on_corr_co": 0, "on_disp": 0},
            start="s.ds.r1.b2",
            end="e.ds.l1.b2",
            vary=(
                "corr_co_acbch6.r1b2",
                "corr_co_acbcv5.r1b2",
                "corr_co_acbch5.l1b2",
                "corr_co_acbcv6.l1b2",
                "corr_co_acbyhs4.l1b2",
                "corr_co_acbyhs4.r1b2",
                "corr_co_acbyvs4.l1b2",
                "corr_co_acbyvs4.r1b2",
            ),
            targets=(
                "ip1",
                "e.ds.l1.b2",
            ),
        ),
        "IP2": dict(
            ref_with_knobs={"on_corr_co": 0, "on_disp": 0},
            start="s.ds.r2.b2",
            end="e.ds.l2.b2",
            vary=(
                "corr_co_acbyhs5.l2b2",
                "corr_co_acbchs5.r2b2",
                "corr_co_acbyvs5.l2b2",
                "corr_co_acbcvs5.r2b2",
                "corr_co_acbyhs4.l2b2",
                "corr_co_acbyhs4.r2b2",
                "corr_co_acbyvs4.l2b2",
                "corr_co_acbyvs4.r2b2",
            ),
            targets=("ip2", "e.ds.l2.b2"),
        ),
        "IP5": dict(
            ref_with_knobs={"on_corr_co": 0, "on_disp": 0},
            start="s.ds.r5.b2",
            end="e.ds.l5.b2",
            vary=(
                "corr_co_acbch6.r5b2",
                "corr_co_acbcv5.r5b2",
                "corr_co_acbch5.l5b2",
                "corr_co_acbcv6.l5b2",
                "corr_co_acbyhs4.l5b2",
                "corr_co_acbyhs4.r5b2",
                "corr_co_acbyvs4.l5b2",
                "corr_co_acbyvs4.r5b2",
            ),
            targets=(
                "ip5",
                "e.ds.l5.b2",
            ),
        ),
        "IP8": dict(
            ref_with_knobs={"on_corr_co": 0, "on_disp": 0},
            start="s.ds.r8.b2",
            end="e.ds.l8.b2",
            vary=(
                "corr_co_acbchs5.l8b2",
                "corr_co_acbyhs5.r8b2",
                "corr_co_acbcvs5.l8b2",
                "corr_co_acbyvs5.r8b2",
                "corr_co_acbyhs4.l8b2",
                "corr_co_acbyhs4.r8b2",
                "corr_co_acbyvs4.l8b2",
                "corr_co_acbyvs4.r8b2",
            ),
            targets=(
                "ip8",
                "e.ds.l8.b2",
            ),
        ),
    }
    return correction_setup


def dump_orbit_correction_files_function(
    correction_setup: dict, output_folder: str = "correction"
) -> str:
    os.makedirs(output_folder, exist_ok=True)
    for nn in ["lhcb1", "lhcb2"]:
        with open(f"{output_folder}/corr_co_{nn}.json", "w") as fid:
            json.dump(correction_setup[nn], fid, indent=4)
    return output_folder


def install_beam_beam_function(
    collider: xt.Multiline,
    num_long_range_encounters_per_side: dict[str, int],
    num_slices_head_on: int,
    bunch_spacing_buckets: int,
    sigma_z: float,
) -> xt.Multiline:

    # Install beam-beam lenses (inactive and not configured)
    collider.install_beambeam_interactions(
        clockwise_line="lhcb1",
        anticlockwise_line="lhcb2",
        ip_names=["ip1", "ip2", "ip5", "ip8"],
        delay_at_ips_slots=[0, 891, 0, 2670],
        num_long_range_encounters_per_side=num_long_range_encounters_per_side,
        num_slices_head_on=num_slices_head_on,
        harmonic_number=35640,
        bunch_spacing_buckets=bunch_spacing_buckets,
        sigmaz=sigma_z,
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


def set_knobs_function(
    collider: xt.Multiline,
    knob_settings: dict,
) -> xt.Multiline:

    # Set all knobs (crossing angles, dispersion correction, rf, crab cavities,
    # experimental magnets, etc.)
    for kk, vv in knob_settings.items():
        collider.vars[kk] = vv

    return collider


def match_tune_and_chroma_function(
    collider: xt.Multiline,
    conf_knob_names: dict,
    conf_qx: dict,
    conf_qy: dict,
    conf_dqx: dict,
    conf_dqy: dict,
    conf_closed_orbit_correction: dict,
) -> xt.Multiline:
    # Tunings
    for line_name in ["lhcb1", "lhcb2"]:
        knob_names = conf_knob_names[line_name]

        targets = {
            "qx": conf_qx[line_name],
            "qy": conf_qy[line_name],
            "dqx": conf_dqx[line_name],
            "dqy": conf_dqy[line_name],
        }

        xm.machine_tuning(
            line=collider[line_name],
            enable_closed_orbit_correction=True,
            enable_linear_coupling_correction=True,
            enable_tune_correction=True,
            enable_chromaticity_correction=True,
            knob_names=knob_names,
            targets=targets,
            line_co_ref=collider[line_name + "_co_ref"],
            co_corr_config=conf_closed_orbit_correction[line_name],
        )

    return collider


def load_filling_scheme_function(
    filling_scheme_path: str,
) -> tuple[np.ndarray, np.ndarray]:

    # Load the filling scheme
    if filling_scheme_path.endswith(".json"):
        with open(filling_scheme_path, "r") as fid:
            filling_scheme = json.load(fid)
    else:
        raise ValueError(
            f"Unknown filling scheme file format: {filling_scheme_path}. It you provided a csv"
            " file, it should have been automatically convert when running the script"
            " 001_make_folders.py. Something went wrong."
        )

    # Extract booleans beam arrays
    array_b1 = np.array(filling_scheme["beam1"])
    array_b2 = np.array(filling_scheme["beam2"])

    return array_b1, array_b2


def compute_collision_schedule_function(
    array_b1: np.ndarray, array_b2: np.ndarray
) -> tuple[int, int, int]:

    # Assert that the arrays have the required length, and do the convolution
    assert len(array_b1) == len(array_b2) == 3564
    n_collisions_ip1_and_5 = int(array_b1 @ array_b2)
    n_collisions_ip2 = int(np.roll(array_b1, 891) @ array_b2)
    n_collisions_ip8 = int(np.roll(array_b1, 2670) @ array_b2)

    return n_collisions_ip1_and_5, n_collisions_ip2, n_collisions_ip8


def get_CC_bool_function(
    crab1_val: float,
    crab5_val: float,
) -> bool:

    # Get crab cavities as boolean
    crab = False
    if abs(crab1_val) > 0 or abs(crab5_val) > 0:
        crab = True
    return crab


def compute_PU_function(
    luminosity: float, num_colliding_bunches: int, T_rev0: float, cross_section=81e-27
) -> float:
    return luminosity / num_colliding_bunches * cross_section * T_rev0


def luminosity_levelling_ip1_5_function(
    collider: xt.Multiline,
    n_collisions_ip1_and_5: int,
    nemitt_x: float,
    nemitt_y: float,
    sigma_z: float,
    crab: bool,
    max_PU: float,
    max_lumi_ip1_and_5: float,
    max_bunch_intensity: float,
    target_lumi_ip1_and_5: float,
) -> float:

    # Get Twiss
    twiss_b1 = collider["lhcb1"].twiss()
    twiss_b2 = collider["lhcb2"].twiss()

    # Internal function to optimize
    def f(bunch_intensity: float):
        luminosity = xt.lumi.luminosity_from_twiss(
            n_colliding_bunches=n_collisions_ip1_and_5,
            num_particles_per_bunch=bunch_intensity,
            ip_name="ip1",
            nemitt_x=nemitt_x,
            nemitt_y=nemitt_y,
            sigma_z=sigma_z,
            twiss_b1=twiss_b1,
            twiss_b2=twiss_b2,
            crab=crab,
        )

        PU = compute_PU_function(
            luminosity,
            n_collisions_ip1_and_5,
            twiss_b1["T_rev0"],
        )

        # Compute penalties for exceeding constraints
        penalty_excess_PU = max(
            0,
            (PU - max_PU) * 1e35,
        )  # in units of 1e-35
        penalty_excess_lumi = max(
            0,
            (luminosity - max_lumi_ip1_and_5) * 10,
        )  # in units of 1e-35 if luminosity is in units of 1e34

        return (
            (luminosity - target_lumi_ip1_and_5) ** 2
            + penalty_excess_PU
            + penalty_excess_lumi
        )

    # Do the optimization
    res = minimize_scalar(
        f,
        bounds=(
            1e10,
            max_bunch_intensity,
        ),
        method="bounded",
        options={"xatol": 1e7},
    )
    if not res.success:
        print(
            "WARNING: Optimization for levelling in IP 1/5 failed. Please check the constraints."
        )
    else:
        print(
            f"Optimization for levelling in IP 1/5 succeeded with I={res.x:.2e} particles per bunch"
        )
    return res.x


def luminosity_levelling_ip2_8_function(
    collider: xt.Multiline,
    config_lumi_leveling_ip2_8: dict,
    num_particles_per_bunch: float,
    sigma_z: float,
    nemitt_x: float,
    nemitt_y: float,
    num_colliding_bunches_ip8: int,
    additional_targets_lumi: list = [],
) -> xt.Multiline:
    for ip_name in config_lumi_leveling_ip2_8.keys():
        print(f"\n --- Leveling in {ip_name} ---")

        config_this_ip = config_lumi_leveling_ip2_8[ip_name]
        bump_range = config_this_ip["bump_range"]

        assert config_this_ip[
            "preserve_angles_at_ip"
        ], "Only preserve_angles_at_ip=True is supported for now"
        assert config_this_ip[
            "preserve_bump_closure"
        ], "Only preserve_bump_closure=True is supported for now"

        beta0_b1 = collider.lhcb1.particle_ref.beta0[0]
        f_rev = 1 / (collider.lhcb1.get_length() / (beta0_b1 * clight))

        targets = []
        vary = []

        if "luminosity" in config_this_ip.keys() and ip_name == "ip8":
            targets.append(
                xt.TargetLuminosity(
                    ip_name=ip_name,
                    luminosity=config_this_ip["target_luminosity"],
                    crab=False,
                    tol=1e30,  # 0.01 * config_this_ip["luminosity"],
                    f_rev=f_rev,
                    num_colliding_bunches=num_colliding_bunches_ip8,
                    num_particles_per_bunch=num_particles_per_bunch,
                    sigma_z=sigma_z,
                    nemitt_x=nemitt_x,
                    nemitt_y=nemitt_y,
                    log=True,
                )
            )

            # Added this line for constraints
            targets.extend(additional_targets_lumi)

        elif "separation_in_sigmas" in config_this_ip.keys() and ip_name == "ip2":
            targets.append(
                xt.TargetSeparation(
                    ip_name=ip_name,
                    separation_norm=config_this_ip["separation_in_sigmas"],
                    tol=1e-4,  # in sigmas
                    plane=config_this_ip["plane"],
                    nemitt_x=nemitt_x,
                    nemitt_y=nemitt_y,
                )
            )
        else:
            raise ValueError(
                "Either `luminosity` or `separation_in_sigmas` must be specified"
            )

        if config_this_ip["impose_separation_orthogonal_to_crossing"]:
            targets.append(xt.TargetSeparationOrthogonalToCrossing(ip_name="ip8"))
        vary.append(xt.VaryList(config_this_ip["knobs"], step=1e-4))

        # Target and knobs to rematch the crossing angles and close the bumps
        for line_name in ["lhcb1", "lhcb2"]:
            targets += [
                # Preserve crossing angle
                xt.TargetList(
                    ["px", "py"],
                    at=ip_name,
                    line=line_name,
                    value="preserve",
                    tol=1e-7,
                    scale=1e3,
                ),
                # Close the bumps
                xt.TargetList(
                    ["x", "y"],
                    at=bump_range[line_name][-1],
                    line=line_name,
                    value="preserve",
                    tol=1e-5,
                    scale=1,
                ),
                xt.TargetList(
                    ["px", "py"],
                    at=bump_range[line_name][-1],
                    line=line_name,
                    value="preserve",
                    tol=1e-5,
                    scale=1e3,
                ),
            ]

        vary.append(xt.VaryList(config_this_ip["corrector_knob_names"], step=1e-7))

        # Match
        collider.match(
            lines=["lhcb1", "lhcb2"],
            ele_start=[bump_range["lhcb1"][0], bump_range["lhcb2"][0]],
            ele_stop=[bump_range["lhcb1"][-1], bump_range["lhcb2"][-1]],
            twiss_init="preserve",
            targets=targets,
            vary=vary,
        )

    return collider


def add_linear_coupling_hllhc_function(
    collider: xt.Multiline,
    delta_cmr: float,
    # delta_cmi: float,
) -> xt.Multiline:

    # Add linear coupling as the target in the tuning of the base collider was 0
    # (not possible to set it the target to 0.001 for now)
    collider.vars["c_minus_re_b1"] += delta_cmr
    collider.vars["c_minus_re_b2"] += delta_cmr

    # ! Only handle real coupling for now
    # collider.vars["c_minus_im_b1"] += delta_cmi
    # collider.vars["c_minus_im_b2"] += delta_cmi

    return collider


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


def configure_beam_beam_interactions_function(
    collider: xt.Multiline,
    num_particles_per_bunch: float,
    nemitt_x: float,
    nemitt_y: float,
) -> xt.Multiline:
    collider.configure_beambeam_interactions(
        num_particles=num_particles_per_bunch,
        nemitt_x=nemitt_x,
        nemitt_y=nemitt_y,
    )

    return collider


def apply_filling_scheme_function(
    collider: xt.Multiline,
    array_b1: np.ndarray,
    array_b2: np.ndarray,
    i_bunch_b1: int,
    i_bunch_b2: int,
) -> xt.Multiline:
    collider.apply_filling_pattern(
        filling_pattern_cw=array_b1,
        filling_pattern_acw=array_b2,
        i_bunch_cw=i_bunch_b1,
        i_bunch_acw=i_bunch_b2,
    )

    return collider


def record_final_luminosity_and_PU_function(
    collider: xt.Multiline,
    num_particles_per_bunch: float,
    nemitt_x: float,
    nemitt_y: float,
    sigma_z: float,
    crab: bool,
    num_colliding_bunches_ip1_and_5: int,
    num_colliding_bunches_ip2: int,
    num_colliding_bunches_ip8: int,
) -> tuple[float, ...]:
    # Get the final luminoisty in all IPs
    twiss_b1 = collider["lhcb1"].twiss()
    twiss_b2 = collider["lhcb2"].twiss()
    l_lumi = []
    l_PU = []
    l_ip = ["ip1", "ip2", "ip5", "ip8"]
    l_n_collisions = [
        num_colliding_bunches_ip1_and_5,
        num_colliding_bunches_ip2,
        num_colliding_bunches_ip1_and_5,
        num_colliding_bunches_ip8,
    ]
    for n_col, ip in zip(l_n_collisions, l_ip):
        try:
            L = xt.lumi.luminosity_from_twiss(
                n_colliding_bunches=n_col,
                num_particles_per_bunch=num_particles_per_bunch,
                ip_name=ip,
                nemitt_x=nemitt_x,
                nemitt_y=nemitt_y,
                sigma_z=sigma_z,
                twiss_b1=twiss_b1,
                twiss_b2=twiss_b2,
                crab=crab,
            )
            PU = compute_PU_function(L, n_col, twiss_b1["T_rev0"])
        except Exception as e:
            print(f"There was a problem during the luminosity computation in {ip}... ")
            print(f"Error message: {e}")
            print("Continuing with L=0 and PU=0...")
            L = 0
            PU = 0
        l_lumi.append(L)
        l_PU.append(PU)

    return tuple(l_lumi + l_PU)


def dump_collider_json_function(
    collider: xt.Multiline,
    name_collider: str,
) -> None:
    collider.to_json(name_collider + ".json")


# ==================================================================================================
# --- Main
# ==================================================================================================


def main(
    path_base_collider: str,
    num_long_range_encounters_per_side: dict,
    num_slices_head_on: int,
    bunch_spacing_buckets: int,
    sigma_z: float,
    knob_settings: dict,
    knob_names: dict,
    qx: dict,
    qy: dict,
    dqx: dict,
    dqy: dict,
    closed_orbit_correction: dict,
    pattern_fname: str,
    on_crab1: float,
    on_crab5: float,
    nemitt_x: float,
    nemitt_y: float,
    max_PU_ip1_5: float,
    max_luminosity_ip1_5: float,
    max_intensity_ip1_5: float,
    target_luminosity_ip1_5: float,
    config_lumi_leveling_ip2_8: dict,
    num_particles_per_bunch: float,
    delta_cmr: float,
    i_bunch_b1: int,
    i_bunch_b2: int,
    path_configured_collider: str,
) -> None:

    collider = load_collider_json_function(path_base_collider)
    correction_setup = generate_orbit_correction_setup_function()
    path_correction_setup = dump_orbit_correction_files_function(correction_setup)
    collider = install_beam_beam_function(
        collider,
        num_long_range_encounters_per_side,
        num_slices_head_on,
        bunch_spacing_buckets,
        sigma_z,
    )
    collider = build_trackers_function(collider)
    collider = set_knobs_function(collider, knob_settings)
    collider = match_tune_and_chroma_function(
        collider, knob_names, qx, qy, dqx, dqy, closed_orbit_correction
    )
    array_b1, array_b2 = load_filling_scheme_function(pattern_fname)
    n_collisions_ip1_and_5, n_collisions_ip2, n_collisions_ip8 = (
        compute_collision_schedule_function(array_b1, array_b2)
    )
    crab_bool = get_CC_bool_function(on_crab1, on_crab5)
    luminosity_ip1_and_5_after_optimization_before_bb = (
        luminosity_levelling_ip1_5_function(
            collider,
            n_collisions_ip1_and_5,
            nemitt_x,
            nemitt_y,
            sigma_z,
            crab_bool,
            max_PU_ip1_5,
            max_luminosity_ip1_5,
            max_intensity_ip1_5,
            target_luminosity_ip1_5,
        )
    )
    collider = luminosity_levelling_ip2_8_function(
        collider,
        config_lumi_leveling_ip2_8,
        num_particles_per_bunch,
        sigma_z,
        nemitt_x,
        nemitt_y,
        n_collisions_ip8,
    )
    collider = add_linear_coupling_hllhc_function(collider, delta_cmr)
    collider = match_tune_and_chroma_function(
        collider, knob_names, qx, qy, dqx, dqy, closed_orbit_correction
    )
    assert_tune_chroma_coupling_function(collider, qx, qy, dqx, dqy, delta_cmr)
    collider = configure_beam_beam_interactions_function(
        collider, num_particles_per_bunch, nemitt_x, nemitt_y
    )
    collider = apply_filling_scheme_function(
        collider, array_b1, array_b2, i_bunch_b1, i_bunch_b2
    )
    lumi_ip1, lumi_ip2 = record_final_luminosity_and_PU_function(
        collider,
        num_particles_per_bunch,
        nemitt_x,
        nemitt_y,
        sigma_z,
        crab_bool,
        n_collisions_ip1_and_5,
        n_collisions_ip2,
        n_collisions_ip8,
    )
    dump_collider_json_function(collider, path_configured_collider)


# ==================================================================================================
# --- Parameters
# ==================================================================================================

# Declare parameters
path_base_collider = "base_collider.json"
num_long_range_encounters_per_side = {"ip1": 25, "ip2": 20, "ip5": 25, "ip8": 20}
num_slices_head_on = 11
bunch_spacing_buckets = 10
sigma_z = 0.0761
knob_settings = {
    "on_x1": 250,
    "on_sep1": 0,
    "on_x2": -170,
    "on_sep2": 0.138,
    "on_x5": 250,
    "on_sep5": 0,
    "on_x8h": 0.0,
    "on_x8v": 170,
    "on_sep8h": -0.01,
    "on_sep8v": 0.01,
    "on_a1": 0,
    "on_o1": 0,
    "on_a2": 0,
    "on_o2": 0,
    "on_a5": 0,
    "on_o5": 0,
    "on_a8": 0,
    "on_o8": 0,
    "on_disp": 1,
    "on_crab1": -190,
    "on_crab5": -190,
    "on_alice_normalized": 1,
    "on_lhcb_normalized": 1,
    "on_sol_atlas": 0,
    "on_sol_cms": 0,
    "on_sol_alice": 0,
    "vrf400": 16.0,
    "lagrf400.b1": 0.5,
    "lagrf400.b2": 0.5,
    "i_oct_b1": 60.0,
    "i_oct_b2": 60.0,
}
knob_names = {
    "lhcb1": {
        "q_knob_1": "kqtf.b1",
        "q_knob_2": "kqtd.b1",
        "dq_knob_1": "ksf.b1",
        "dq_knob_2": "ksd.b1",
        "c_minus_knob_1": "c_minus_re_b1",
        "c_minus_knob_2": "c_minus_im_b1",
    },
    "lhcb2": {
        "q_knob_1": "kqtf.b2",
        "q_knob_2": "kqtd.b2",
        "dq_knob_1": "ksf.b2",
        "dq_knob_2": "ksd.b2",
        "c_minus_knob_1": "c_minus_re_b2",
        "c_minus_knob_2": "c_minus_im_b2",
    },
}
qx = {"lhcb1": 62.318, "lhcb2": 62.318}
qy = {"lhcb1": 60.32, "lhcb2": 60.32}
dqx = {"lhcb1": 15, "lhcb2": 15}
dqy = {"lhcb1": 15, "lhcb2": 15}
closed_orbit_correction = {
    "lhcb1": "correction/corr_co_lhcb1.json",
    "lhcb2": "correction/corr_co_lhcb2.json",
}
pattern_fname = (
    "../filling_scheme/8b4e_1972b_1960_1178_1886_224bpi_12inj_800ns_bs200ns.json"
)
on_crab1 = -190
on_crab5 = -190
nemitt_x = 2.5e-06
nemitt_y = 2.5e-06
max_PU_ip1_5 = 160
max_luminosity_ip1_5 = 5e34
max_intensity_ip1_5 = 230000000000.0
target_luminosity_ip1_5 = 5e34
config_lumi_leveling_ip2_8 = {
    "ip2": {
        "separation_in_sigmas": 5,
        "plane": "x",
        "impose_separation_orthogonal_to_crossing": False,
        "knobs": ["on_sep2"],
        "bump_range": {
            "lhcb1": ["e.ds.l2.b1", "s.ds.r2.b1"],
            "lhcb2": ["s.ds.r2.b2", "e.ds.l2.b2"],
        },
        "preserve_angles_at_ip": True,
        "preserve_bump_closure": True,
        "corrector_knob_names": [
            "corr_co_acbyvs4.l2b1",
            "corr_co_acbyhs4.l2b1",
            "corr_co_acbyvs4.r2b2",
            "corr_co_acbyhs4.r2b2",
            "corr_co_acbyvs4.l2b2",
            "corr_co_acbyhs4.l2b2",
            "corr_co_acbyvs4.r2b1",
            "corr_co_acbyhs4.r2b1",
            "corr_co_acbyhs5.l2b2",
            "corr_co_acbyvs5.l2b2",
            "corr_co_acbchs5.r2b1",
            "corr_co_acbcvs5.r2b1",
        ],
    },
    "ip8": {
        "luminosity": 2e33,
        "num_colliding_bunches": None,
        "impose_separation_orthogonal_to_crossing": True,
        "knobs": ["on_sep8h", "on_sep8v"],
        "bump_range": {
            "lhcb1": ["e.ds.l8.b1", "s.ds.r8.b1"],
            "lhcb2": ["s.ds.r8.b2", "e.ds.l8.b2"],
        },
        "preserve_angles_at_ip": True,
        "preserve_bump_closure": True,
        "corrector_knob_names": [
            "corr_co_acbyvs4.l8b1",
            "corr_co_acbyhs4.l8b1",
            "corr_co_acbyvs4.r8b2",
            "corr_co_acbyhs4.r8b2",
            "corr_co_acbyvs4.l8b2",
            "corr_co_acbyhs4.l8b2",
            "corr_co_acbyvs4.r8b1",
            "corr_co_acbyhs4.r8b1",
            "corr_co_acbcvs5.l8b2",
            "corr_co_acbchs5.l8b2",
            "corr_co_acbyvs5.r8b1",
            "corr_co_acbyhs5.r8b1",
        ],
    },
    "path_configured_collider": "configured_collider.json",
}
num_particles_per_bunch = 140000000000.0
delta_cmr = 0.001
i_bunch_b1 = 1963
i_bunch_b2 = 1963
path_configured_collider = "configured_collider.json"


# ==================================================================================================
# --- Script
# ==================================================================================================

if __name__ == "__main__":
    main(
        path_base_collider,
        num_long_range_encounters_per_side,
        num_slices_head_on,
        bunch_spacing_buckets,
        sigma_z,
        knob_settings,
        knob_names,
        qx,
        qy,
        dqx,
        dqy,
        closed_orbit_correction,
        pattern_fname,
        on_crab1,
        on_crab5,
        nemitt_x,
        nemitt_y,
        max_PU_ip1_5,
        max_luminosity_ip1_5,
        max_intensity_ip1_5,
        target_luminosity_ip1_5,
        config_lumi_leveling_ip2_8,
        num_particles_per_bunch,
        delta_cmr,
        i_bunch_b1,
        i_bunch_b2,
        path_configured_collider,
    )
