import inspect
import logging
from collections import OrderedDict
from typing import Callable, Self

from matplotlib.pylab import f


class Block:
    def __init__(
        self,
        function: Callable | None = None,
        dic_imports: dict[str, str] = OrderedDict(),
        output: OrderedDict[str, type] = OrderedDict(),
    ):
        self.function = function
        self.dic_imports = dic_imports
        self.output = output

    def get_str(self: Self) -> str:
        if self.function is None:
            logging.warning("No function defined for this block")
            return ""
        else:
            return inspect.getsource(self.function)

    @staticmethod
    def get_output_str(output: OrderedDict[str, type] = OrderedDict()) -> str:
        if len(output) == 0:
            return ""
        else:
            if len(output) == 1:
                return list(output.keys())[0]
            else:
                return ", ".join([x for x in output.keys()])

    @staticmethod
    def get_output_type_hint_str(output: OrderedDict[str, type] = OrderedDict()) -> str:

        if len(output) == 0:
            output_hint_str = "None"
        else:
            if len(output) > 1:
                output_str = ", ".join([x.__name__ for x in output.values()])
                output_hint_str = f"tuple[{output_str}]"
            else:
                output_hint_str = list(output.values())[0].__name__

        return output_hint_str

    def get_call_str(self: Self) -> str:
        if self.function is None:
            logging.warning("No function defined for this block")
            return ""
        else:
            return f"{self.function.__name__}({', '.join(self.get_parameters().keys())})"

    def get_assignation_call_str(self: Self) -> str:
        function_call_str = self.get_call_str()
        output_str = self.get_output_str(self.output)

        if output_str == "":
            return function_call_str
        else:
            return f"{output_str} = {function_call_str}"

    def get_signature(self: Self) -> inspect.Signature:
        if self.function is None:
            logging.warning("No function defined for this block")
            return inspect.Signature()
        else:
            return inspect.signature(self.function)

    def get_parameters(self: Self) -> OrderedDict[str, type]:
        if self.function is None:
            logging.warning("No function defined for this block")
            return OrderedDict()
        else:
            signature = self.get_signature()
            dict_parameters = OrderedDict(
                [
                    (parameter, signature.parameters[parameter].annotation)
                    for parameter in signature.parameters
                ]
            )
            return dict_parameters

    def get_merge_parameters(
        self: Self, block: Self, output: OrderedDict[str, type] = OrderedDict()
    ) -> OrderedDict[str, type]:

        ### Establish complete list of parameters
        self_parameters = self.get_parameters().copy()
        block_parameters = block.get_parameters()

        # First check that identical parameters have identical type
        for key in set(self_parameters).intersection(block_parameters):
            if self_parameters[key] != block_parameters[key]:
                raise ValueError(f"Parameter {key} has different types in the two blocks")

        # Then merge parameters
        parameters = self_parameters | block_parameters

        # If an output has been provided, remove it from the list of parameters
        # Except if it's modified inplace (inside of a block)
        # Start with self block
        for key in self.output:
            if key not in self_parameters and key in parameters:
                del self_parameters[key]
        # Then do the same for the argument block
        for key in block.output:
            if key not in block_parameters and key in parameters:
                del block_parameters[key]

        return parameters

    def check_merge_output(
        self: Self, block: Self, output: OrderedDict[str, type] = OrderedDict()
    ) -> None:
        # If the output is not None, ensure that the elements in it are either
        # - in the parameters (inplace operation)
        # - in the outputs
        if len(output) > 0:
            for key in output:
                if (
                    key not in self.get_parameters()
                    and key not in self.output
                    and key not in block.output
                ):
                    raise ValueError(f"Output {key} is not in the parameters or the outputs")

    def build_merge_str(
        self: Self,
        block: Self,
        name_function: str,
        docstring: str = "",
        output: OrderedDict[str, type] = OrderedDict(),
        parameters: OrderedDict[str, type] = OrderedDict(),
    ) -> str:

        # Get output type hint string
        output_str = self.get_output_type_hint_str(output)

        # Get function header with the merged parameters
        parameters_header = ", ".join(
            [f"{parameter}: {parameters[parameter].__name__}" for parameter in parameters]
        )
        function_header = f"def {name_function}({parameters_header}) -> {output_str}:"

        # Write function body: call the two functions
        function_body = f"\t{self.get_assignation_call_str()}\n\t{block.get_assignation_call_str()}"

        # Write function output
        function_output = f"\treturn {output_str}"

        # Write full function
        function_str = "\n".join([function_header, docstring, function_body, function_output])

        return function_str

    def get_merge_str(
        self: Self,
        block: Self,
        name_function: str,
        docstring: str = "",
        output: OrderedDict[str, type] = OrderedDict(),
    ) -> str:

        # Get merged parameters
        parameters = self.get_merge_parameters(block)

        # Ensure that the output is accessible
        self.check_merge_output(block, output)

        # Build function string
        function_str = self.build_merge_str(block, name_function, docstring, output, parameters)

        return function_str

    def merge_imports(self: Self, block: Self) -> dict[str, str]:

        # Merge imports, ensuring that there are no conflicts
        dic_imports = self.dic_imports.copy()
        for module, alias in block.dic_imports.items():
            if module in dic_imports and dic_imports[module] != alias:
                raise ValueError(f"Import conflict for module {module}. Aliases are not consistent")
            else:
                dic_imports[module] = alias

        return dic_imports

    def merge_block(
        self: Self,
        block: Self,
        name_function: str,
        docstring: str = "",
        output: OrderedDict[str, type] = OrderedDict(),
    ) -> Self:
        print("ICICCI", name_function)

        # Build function string
        function_str = self.get_merge_str(block, name_function, docstring, output)

        print("ICICCI2", name_function)
        print(function_str)

        print(locals().keys())
        # Convert into Python function
        exec(function_str, globals())

        print("ICICCI3", name_function)
        # add_multiply(2, 3)
        print(locals().keys())
        # print("ici", locals()[name_function](2, 3))

        # Merge imports
        dic_imports = self.merge_imports(block)

        return Block(function=globals()[name_function], dic_imports=dic_imports, output=output)
