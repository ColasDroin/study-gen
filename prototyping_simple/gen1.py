# ==================================================================================================
# --- Imports
# ==================================================================================================

import math
import numpy as np
from typing import Any

# ==================================================================================================
# --- Parameters
# ==================================================================================================

	# Declare parameters
	b = 10
	c = 4
	a = 2


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

def gamma_function(a: float) -> float:
    """Dummy docstring"""
    # Compute gamma function of a
    return math.gamma(a)

def save_npy_function(output: Any) -> None:
    np.save(f"{output=}".split("=")[0], output)

def main_function(b: float, c: float, a: float) -> None:


    bc = multiply_function(b, c)
    a_bc = add_function(a, bc)
    fact_a_bc = gamma_function(a_bc)
    save_npy_function(fact_a_bc)
    return 


# ==================================================================================================
# --- Main
# ==================================================================================================



# ==================================================================================================
# --- Script
# ==================================================================================================

if __name__ == "__main__":
    main()