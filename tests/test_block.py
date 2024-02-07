# Stndard library imports
import math

# Third party imports
import numpy as np
import pytest

# Local application imports
from study_gen import Block


@pytest.fixture
def example_block():
    def example_function(a: float, b: float) -> float:
        # Returns a at the power of b
        return np.power(a, math.gamma(b))

    dict_imports = {"math": "import math", "np": "import numpy as np"}
    return Block(
        "example_function",
        example_function,
        dict_imports=dict_imports,
    )
