# ==================================================================================================
# --- Imports
# ==================================================================================================
# Stndard library imports
import math
from collections import OrderedDict

# Third party imports
import numpy as np
import pytest

# Local application imports
from study_gen import Block


# ==================================================================================================
# --- Fixtures
# ==================================================================================================
@pytest.fixture(scope="function")
def example_block_with_no_function():
    return Block("example_block", None)  # type: ignore


# Should pass
@pytest.fixture(scope="function")
def example_block_with_no_output():
    def example_function() -> None:
        pass

    return Block("example_block", example_function)


# Should not pass as '->' must be here
@pytest.fixture(scope="function")
def example_block_with_no_output_alt():
    def example_function():
        pass

    return Block("example_block", example_function)


# Should pass
@pytest.fixture(scope="function")
def example_block_with_no_output_alt2():
    def example_function() -> None:
        return None

    return Block("example_block", example_function)


@pytest.fixture(scope="function")
def example_block_with_one_output():
    def example_function(a: float, b: float) -> float:
        return a + b

    return Block("example_block", example_function)


@pytest.fixture(scope="function")
def example_block_with_two_outputs():
    def example_function(a: float, b: float) -> tuple[float, int]:
        """Example function to test the block class."""
        # Returns a at the power of b
        return np.power(a, math.gamma(b)), int(math.gamma(a))

    dict_imports = {"math": "import math", "np": "import numpy as np"}
    return Block("example_block", example_function, dict_imports=dict_imports)


@pytest.fixture(scope="function")
def example_block_with_one_import():
    def example_function(a: float, b: float) -> None:
        a = np.power(a, b)

    dict_imports = {"np": "import numpy as np"}
    return Block("example_block", example_function, dict_imports=dict_imports)


@pytest.fixture(scope="function")
def example_block_with_missing_output():
    def example_function(a: float, b: float):
        """Example function to test the block class."""
        # Returns a at the power of b
        return np.power(a, b)

    dict_imports = {"np": "import numpy as np"}
    return Block("example_block", example_function, dict_imports=dict_imports)


@pytest.fixture(scope="function")
def example_block_with_manual_output():
    def example_function(a: float, b: float) -> float:
        """Example function to test the block class."""
        # Returns a at the power of b
        return np.power(a, b)

    dict_imports = {"np": "import numpy as np"}
    return Block(
        "example_block",
        example_function,
        dict_imports=dict_imports,
        dict_output=OrderedDict({"output_example_block": float}),
    )


@pytest.fixture(scope="function")
def example_block_with_two_manual_output():
    def example_function(a: float, b: float) -> tuple[float, int]:
        """Example function to test the block class."""
        # Returns a at the power of b
        return np.power(a, b), int(np.power(a, b))

    dict_imports = {"np": "import numpy as np"}
    return Block(
        "example_block",
        example_function,
        dict_imports=dict_imports,
        dict_output=OrderedDict(
            [("output_0_example_block", float), ("output_1_example_block", int)]
        ),
    )


@pytest.fixture(scope="function")
def example_block_with_wrong_manual_output():
    def example_function(a: float, b: float) -> int:
        """Example function to test the block class."""
        # Returns a at the power of b
        return np.power(a, b)

    dict_imports = {"np": "import numpy as np"}
    return Block(
        "example_block",
        example_function,
        dict_imports=dict_imports,
        dict_output=OrderedDict({"output_example_block": float}),
    )


@pytest.fixture(scope="function")
def example_block_with_manual_output_no_signature():
    def example_function(a: float, b: float):
        """Example function to test the block class."""
        # Returns a at the power of b
        return np.power(a, b)

    dict_imports = {"np": "import numpy as np"}
    return Block(
        "example_block",
        example_function,
        dict_imports=dict_imports,
        dict_output=OrderedDict({"output_example_block": float}),
    )


@pytest.fixture(scope="function")
def example_block_with_wrong_signature():
    def example_function(a: float, b: float) -> int:
        """Example function to test the block class."""
        # Returns a at the power of b
        return np.power(a, b)

    dict_imports = {"np": "import numpy as np"}
    return Block(
        "example_block",
        example_function,
        dict_imports=dict_imports,
        dict_output=OrderedDict({"output_example_block": float}),
    )


# ==================================================================================================
# --- Tests
# ==================================================================================================
# Check that error is raised when no function is provided
@pytest.mark.parametrize(
    "block_func",
    [
        example_block_with_no_function,
    ],
)
def test_no_function(block_func, request):
    with pytest.raises(ValueError):
        request.getfixturevalue(block_func.__name__)


# Check for all sorts of non-existing outputs
@pytest.mark.parametrize(
    "block_func",
    [
        example_block_with_no_output,
        example_block_with_no_output_alt2,
    ],
)
def test_no_output(block_func, request):
    block = request.getfixturevalue(block_func.__name__)
    assert block.dict_output == OrderedDict()


# Check for all sorts of outputs issues
@pytest.mark.parametrize(
    "block_func",
    [
        example_block_with_no_output_alt,
        example_block_with_missing_output,
        example_block_with_wrong_manual_output,
        example_block_with_manual_output_no_signature,
        example_block_with_wrong_signature,
    ],
)
def test_output_failed(block_func, request):
    with pytest.raises(ValueError):
        request.getfixturevalue(block_func.__name__)


# Check for all sorts of outputs
@pytest.mark.parametrize(
    "block_func,output",
    [
        (block_func, output)
        for block_func, output in zip(
            [
                example_block_with_one_output,
                example_block_with_two_outputs,
                example_block_with_manual_output,
                example_block_with_two_manual_output,
            ],
            [
                OrderedDict({"output_example_block": float}),
                OrderedDict({"output_0_example_block": float, "output_1_example_block": int}),
                OrderedDict({"output_example_block": float}),
            ],
        )
    ],
)
def test_dict_output(block_func, output, request):
    block = request.getfixturevalue(block_func.__name__)
    assert block.dict_output == output


@pytest.mark.parametrize(
    "block_func",
    [
        example_block_with_two_outputs,
    ],
)
def test_dict_output_setter(block_func, request):
    block = request.getfixturevalue(block_func.__name__)

    # Check for wrong number of outputs
    with pytest.raises(ValueError):
        block.dict_output = OrderedDict({"output_example_block": float})

    # Check for wrong type
    with pytest.raises(ValueError):
        block.dict_output = OrderedDict(
            [("output_0_example_block", int), ("output_1_example_block", int)]
        )

    # Check for proper setting
    block.dict_output = OrderedDict(
        [("output_0_example_block", float), ("output_1_example_block", int)]
    )
    assert block.dict_output == OrderedDict(
        [("output_0_example_block", float), ("output_1_example_block", int)]
    )


# ! How to test for missing imports?
# @pytest.fixture(scope="function")
# def example_block_with_two_import():
#     def example_function(a: float, b: float) -> None:
#         a = np.power(a, math.acos(b))

#     dict_imports = {"np": "import numpy as np", "math": "import math"}
#     return Block("example_block", example_function, dict_imports=dict_imports)


# @pytest.fixture(scope="function")
# def example_block_with_missing_import():
#     def example_function(a: float, b: float) -> None:
#         c = np.power(a, b)

#     return Block("example_block", example_function)
