# ==================================================================================================
# --- Import statements ---
# ==================================================================================================
import importlib

from ..block import Block

# This is needed to get the import and the import alias for code generation
dic_imports = {"numpy": "np"}
for module, alias in dic_imports.items():
    vars()[alias] = importlib.import_module(module)


# ==================================================================================================
# --- Block function ---
# ==================================================================================================
def power_function(a: int, b: int) -> int:
    # Returns a at the power of b
    return np.power(a, b)


# ==================================================================================================
# --- Block ---
# ==================================================================================================

power = Block(power_function, dic_imports=dic_imports)

# ==================================================================================================
# --- Script ---
# ==================================================================================================
# This is only for testing purposes
if __name__ == "__main__":
    print(power)
    print(power.function(2, 3))
