# ==================================================================================================
# --- Imports
# ==================================================================================================

import math as math
import numpy as np

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
    # Compute factorial of a
    return math.gamma(a)


# ==================================================================================================
# --- Main
# ==================================================================================================

def main():
    # Declare parameters
    a = 2
    b = 10
    c = 4

    # Declare blocks
    bc = multiply_function(b, c)
    a_bc = add_function(a, bc)
    fact_a_bc = gamma_function(a_bc)

    # Save output
    np.save('fact_a_bc', fact_a_bc)


# ==================================================================================================
# --- Script
# ==================================================================================================

if __name__ == "__main__":
    main()