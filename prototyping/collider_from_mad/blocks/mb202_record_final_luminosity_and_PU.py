# ==================================================================================================
# --- Imports ---
# Some imports are optional as they're also declared in dict_imports, but it's
# helpful to declare them here for linting.
# ==================================================================================================
# Standard library imports
from collections import OrderedDict

# Third party imports
import xtrack as xt

# Local imports
from study_gen.block import Block

# Block dependencies
from .b210_compute_PU import compute_PU_function

# Imports needed for block to work (not detected by linting tools)
dict_imports = {"xt": "import xtrack as xt"}

# Block dependencies
set_deps = set(["compute_PU"])


# ==================================================================================================
# --- Block function ---
# ==================================================================================================
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
) -> list[float]:

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
        except:
            print(f"There was a problem during the luminosity computation in {ip}... Ignoring it.")
            L = 0
            PU = 0
        l_lumi.append(L)
        l_PU.append(PU)

    return l_lumi + l_PU


# ==================================================================================================
# --- Block object ---
# ==================================================================================================

add_linear_coupling = Block(
    "record_final_luminosity_and_PU",
    record_final_luminosity_and_PU_function,
    dict_imports=dict_imports,
    dict_output=OrderedDict([("output_record_final_luminosity_and_PU", list[float])]),
    set_deps=set_deps,
)
