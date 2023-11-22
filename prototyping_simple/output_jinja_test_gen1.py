def add(a: int, b: int) -> int:
    """Dummy docstring"""
    # Add a and b
    return a + b

def multiply(a: int, b: int) -> int:

    # Multiply a and b
    return a * b

def power(a: int, b: int) -> int:
    import numpy as np

    # Returns a at the power of b
    return np.power(a, b)

def print_result(result: int) -> None:
    print(f"Result: {result}")
