import inspect
import logging
from collections import OrderedDict
from dataclasses import dataclass
from typing import Callable, Self

from matplotlib.pylab import f


@dataclass
class Block:
    function: Callable | None = None
    dic_imports: dict[str, str] | None = None
    output: OrderedDict[str, type] = OrderedDict()

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

    def get_function_call_str(self: Self) -> str:
        if self.function is None:
            logging.warning("No function defined for this block")
            return ""
        else:
            return f"{self.function.__name__}({', '.join(self.get_parameters().keys())})"

    def get_assignation_call_str(self: Self) -> str:
        function_call_str = self.get_function_call_str()
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

    def get_add_block_function_str(
        self: Self,
        block: Self,
        name_function: str,
        docstring: str = "",
        output: OrderedDict[str, type] = OrderedDict(),
    ) -> str:

        ### Establish complete list of parameters
        self_parameters = self.get_parameters()
        block_parameters = block.get_parameters()

        # First check that identical parameters have identical type
        for key in set(self_parameters).intersection(block_parameters):
            if self_parameters[key] != block_parameters[key]:
                raise ValueError(f"Parameter {key} has different types in the two blocks")

        # Then merge parameters
        self_parameters.update(block_parameters)

        # Remove output parameters from the list of parameters
        for key in self.output:
            if key in self_parameters:
                del self_parameters[key]

        # If the output is not None, ensure that the elements in it are either
        # - in the parameters (inplace operation)
        # - in the outputs
        if len(output) > 0:
            for key in output:
                if (
                    key not in self_parameters
                    and key not in self.output
                    and key not in block.output
                ):
                    raise ValueError(f"Output {key} is not in the parameters or the outputs")

        output_str = self.get_output_type_hint_str(output)

        # Get function header with the merged parameters
        parameters_header = ", ".join(
            [f"{parameter}: {self_parameters[parameter]}" for parameter in self_parameters]
        )
        function_header = f"def {name_function}({parameters_header}) -> {output_str}:"

        # Write function body: call the two functions
        function_body = f"{self.get_assignation_call_str()}\n{block.get_assignation_call_str()}"

        # Write function output
        function_output = f"return {output_str}"

        # Write full function
        function_str = "\n".join([function_header, docstring, function_body, function_output])

        return function_str

    def add_block(
        self: Self,
        block: Self,
        name_function: str,
        docstring: str = "",
        output: OrderedDict[str, type] = OrderedDict(),
    ) -> Self:

        # Build function string
        function_str = self.get_add_block_function_str(block, name_function, docstring, output)

        # Convert into Python function
        function = eval(function_str)

        # Merge imports, ensuring that there are no conflicts
        if self.dic_imports is None and block.dic_imports is None:
            dic_imports = None
        elif self.dic_imports is None:
            dic_imports = block.dic_imports.copy()
        else:
            dic_imports = self.dic_imports.copy()
            if block.dic_imports is not None:
                for module, alias in block.dic_imports.items():
                    if module in dic_imports and dic_imports[module] != alias:
                        raise ValueError(
                            f"Import conflict for module {module}. Aliases are not consistent"
                        )
                    else:
                        dic_imports[module] = alias

        #
        return Block(function=function, dic_imports=dic_imports, output=output)
