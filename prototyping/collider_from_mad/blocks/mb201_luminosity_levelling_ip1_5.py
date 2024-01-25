# ==================================================================================================
# --- Imports ---
# Some imports are optional as they're also declared in dict_imports, but it's
# helpful to declare them here for linting.
# ==================================================================================================
# Standard library imports
from collections import OrderedDict

# Third party imports
import xtrack as xt
from scipy.optimize import minimize_scalar

# Local imports
from study_gen.block import Block

# Block dependencies
from .b210_compute_PU import compute_PU_function

# Imports needed for block to work (not detected by linting tools)
dict_imports = {
    "minimize_scalar": "from scipy.optimize import minimize_scalar",
    "xt": "import xtrack as xt",
}

# Block dependencies
set_deps = set(["compute_PU"])


# ==================================================================================================
# --- Block function ---
# ==================================================================================================
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

        return (luminosity - target_lumi_ip1_and_5) ** 2 + penalty_excess_PU + penalty_excess_lumi

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
        print("WARNING: Optimization for levelling in IP 1/5 failed. Please check the constraints.")
    else:
        print(
            f"Optimization for levelling in IP 1/5 succeeded with I={res.x:.2e} particles per bunch"
        )
    return res.x


# ==================================================================================================
# --- Block object ---
# ==================================================================================================

luminosity_levelling_ip1_5 = Block(
    "luminosity_levelling_ip1_5",
    luminosity_levelling_ip1_5_function,
    dict_imports=dict_imports,
    dict_output=OrderedDict([("output_luminosity_levelling_ip1_5", float)]),
    set_deps=set_deps,
)
