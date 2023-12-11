# ==================================================================================================
# --- Imports
# ==================================================================================================

import pickle
from typing import Any
import numpy as np

# ==================================================================================================
# --- Parameters
# ==================================================================================================

	# Declare parameters
b = 10
c = 4
a = 2
d = 0.5


# ==================================================================================================
# --- Blocks
# ==================================================================================================

def multiply_function(a: float, b: float) -> float:

    # Multiply a and b
    return a * b

def add_function(a: float, b: float) -> float:
    """Dummy docstring"""
    # Add a and b
    return a + b

def save_pkl_function(output: Any) -> None:
    # Get output name
    output_str = f"{output=}".split("=")[0]
    with open(output_str, "wb") as f:
        pickle.dump(output, f)

def power_function(b: float, c: float) -> float:
    # Returns a at the power of b
    return np.power(b, c)

def add_power_function(x: float, y: float, z: float) -> float:
    """This is a merge test.
    """

    x_y = power_function(x, y)
    x_y = power_function(x_y, x_y)
    x_y_z = add_function(x_y, z)
    return x_y_z


# ==================================================================================================
# --- Main
# ==================================================================================================

def main(b: float, c: float, a: float, d: float) -> None:


    bc_c = add_power_function(b, c, c)
    a_bc_c = multiply_function(a, bc_c)
    c_c_d = add_power_function(c, c, d)
    a_bc_c_c_d = add_function(a_bc_c, c_c_d)
    result = multiply_function(a_bc_c, a_bc_c_c_d)
    save_pkl_function(result)
    return 


# ==================================================================================================
# --- Script
# ==================================================================================================

if __name__ == "__main__":
    main()