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
    list(
        zip(
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
    ),
)
def test_dict_output(block_func, output, request):
    block = request.getfixturevalue(block_func.__name__)
    assert block.dict_output == output


# Check for output setter
def test_dict_output_setter(example_block_with_two_outputs):
    # Check for wrong number of outputs
    with pytest.raises(ValueError):
        example_block_with_two_outputs.dict_output = OrderedDict({"output_example_block": float})

    # Check for wrong type
    with pytest.raises(ValueError):
        example_block_with_two_outputs.dict_output = OrderedDict(
            [("output_0_example_block", int), ("output_1_example_block", int)]
        )

    # Check for proper setting
    example_block_with_two_outputs.dict_output = OrderedDict(
        [("output_0_example_block", float), ("output_1_example_block", int)]
    )
    assert example_block_with_two_outputs.dict_output == OrderedDict(
        [("output_0_example_block", float), ("output_1_example_block", int)]
    )

    # Update name of outputs
    example_block_with_two_outputs.set_outputs_names(["better_name", "even_better_name"])
    assert example_block_with_two_outputs.dict_output == OrderedDict(
        [("better_name", float), ("even_better_name", int)]
    )
    assert example_block_with_two_outputs.get_outputs_names() == ["better_name", "even_better_name"]


def test_arguments(example_block_with_two_outputs):
    # Check for default arguments
    assert example_block_with_two_outputs.l_arguments == []

    # Check setter for wrong number of arguments
    with pytest.raises(ValueError):
        example_block_with_two_outputs.l_arguments = [("a", float)]

    # Check setter for wrong types of arguments
    with pytest.raises(ValueError):
        example_block_with_two_outputs.l_arguments = [("a", float), ("b", int)]

    # Check for setter with correct arguments
    example_block_with_two_outputs.l_arguments = [("a", float), ("b", float)]
    assert example_block_with_two_outputs.l_arguments == [("a", float), ("b", float)]

    # Check for arguments names change
    example_block_with_two_outputs.set_arguments_names(["better_name", "even_better_name"])
    assert example_block_with_two_outputs.get_arguments_names() == [
        "better_name",
        "even_better_name",
    ]


def test_docstring(example_block_with_two_outputs):
    assert (
        example_block_with_two_outputs.get_docstring()
        == "Example function to test the block class."
    )


def test_get_body(example_block_with_two_outputs):
    # Need to adapt the string for wrong fixture tabbing
    assert (
        example_block_with_two_outputs.get_body_str()
        == "        \n        # Returns a at the power of b\n        return np.power(a, math.gamma(b)), int(math.gamma(a))\n"
    )


def test_get_output_str(example_block_with_two_outputs):
    assert (
        example_block_with_two_outputs.get_output_str()
        == "output_0_example_block, output_1_example_block"
    )


def test_get_output_type_hint_str(example_block_with_two_outputs):
    assert example_block_with_two_outputs.get_output_type_hint_str() == "tuple[float, int]"


def test_get_call_str(example_block_with_two_outputs):
    # Must provide the arguments first
    example_block_with_two_outputs.set_arguments_names(["a", "b"])
    assert example_block_with_two_outputs.get_call_str() == "example_function(a, b)"

    # Try to provide too many arguments
    with pytest.raises(ValueError):
        example_block_with_two_outputs.set_arguments_names(["a", "b", "c"])

    # Providing too few arguments doesn't do anything as some arguments are optional
    example_block_with_two_outputs.set_arguments_names(["a"])


@pytest.mark.parametrize(
    "block_func, expected_assignation_call",
    list(
        zip(
            [
                example_block_with_no_output,
                example_block_with_no_output_alt2,
                example_block_with_one_output,
                example_block_with_two_outputs,
                example_block_with_manual_output,
                example_block_with_two_manual_output,
            ],
            [
                "example_function()",
                "example_function()",
                "output_example_block = example_function()",
                "output_0_example_block, output_1_example_block = example_function()",
                "output_example_block = example_function()",
                "output_0_example_block, output_1_example_block = example_function()",
            ],
        )
    ),
)
def test_get_assignation_call_str(block_func, expected_assignation_call, request):
    block = request.getfixturevalue(block_func.__name__)
    assert block.get_assignation_call_str() == expected_assignation_call


@pytest.mark.parametrize(
    "block_func, expected_signature",
    list(
        zip(
            [
                example_block_with_no_output,
                example_block_with_two_outputs,
            ],
            [
                "() -> None",
                "(a: float, b: float) -> tuple[float, int]",
            ],
        )
    ),
)
def test_get_signature(block_func, expected_signature, request):
    block = request.getfixturevalue(block_func.__name__)
    # Easier to test as string
    assert str(block.get_signature()) == expected_signature


@pytest.mark.parametrize(
    "block_func, expected_signature",
    list(
        zip(
            [
                example_block_with_no_output,
                example_block_with_two_outputs,
            ],
            [
                None,
                tuple[float, int],
            ],
        )
    ),
)
def test_get_output_type_fromsignature(block_func, expected_signature, request):
    block = request.getfixturevalue(block_func.__name__)
    # Easier to test as string
    assert block.get_output_type_from_signature() == expected_signature


def test_get_l_imports_str(example_block_with_two_outputs):
    assert example_block_with_two_outputs.get_l_imports_str() == "import math\nimport numpy as np"


def test_prepare_function_str(example_block_with_two_outputs):
    function_header, function_body, docstring = example_block_with_two_outputs.prepare_function_str(
        name_function="test_function",
        docstring="Let's test this function",
        dict_parameters={"aa": int, "bb": float},
    )

    assert function_header == "def test_function(aa: int, bb: float) -> tuple[float, int]:"
    # Need to adapt tabbing for fixture
    assert (
        function_body
        == """        \n        # Returns a at the power of b
        return np.power(a, math.gamma(b)), int(math.gamma(a))\n"""
    )
    assert docstring == """Let's test this function"""


# ? block.build_function_str()is tested in test_study_gen.py

# ==================================================================================================
# --- Problematic tests
# ==================================================================================================


def test_parameters(example_block_with_two_outputs):
    # Check for default parameters
    assert example_block_with_two_outputs.dict_parameters == OrderedDict(
        [("a", float), ("b", float)]
    )

    # Check setter for wrong number of parameters
    with pytest.raises(ValueError):
        example_block_with_two_outputs.dict_parameters = OrderedDict([("a", float)])

    # Check for setter
    # ! Bug here, seems to be due to the way the fixture is defined
    # example_block_with_two_outputs.dict_parameters = OrderedDict([("a", int), ("b", int)])

    # Check for parameter names change
    # example_block_with_two_outputs.set_parameters_names(["better_name", "even_better_name"])
    # assert example_block_with_two_outputs.dict_parameters == OrderedDict(
    #     [("better_name", float), ("even_better_name", float)]
    # )


# ! Testing for missing imports is also tricky
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
