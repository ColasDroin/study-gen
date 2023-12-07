# ==================================================================================================
# --- Imports
# ==================================================================================================

import numpy as np
import pickle as pickle

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

def power_function(b: float, c: float) -> float:
    # Returns a at the power of b
    return np.power(b, c)

def add_power(x: float, y: float, z: float) -> float:
    """This is a merge test.
    """

    x_y = power_function(x, y)
    x_y_z = add_function(x_y, z)
    return x_y_z


# ==================================================================================================
# --- Main
# ==================================================================================================

def main():
    # Declare parameters
    d = 0.5

    # Declare blocks
    bc_c = add_power(b, c, c)
    a_bc_c = multiply_function(a, bc_c)
    c_c_d = add_power(c, c, d)
    a_bc_c_c_d = add_function(a_bc_c, c_c_d)
    result = multiply_function(fact_a_bc, a_bc_c_c_d)

    # Save output


# ==================================================================================================
# --- Script
# ==================================================================================================

if __name__ == "__main__":
    main()