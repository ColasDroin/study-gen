import importlib.util
import inspect
import logging
import sys
import tempfile
from collections import OrderedDict
from typing import Callable, Self


class Block:
    def __init__(
        self,
        function: Callable | None = None,
        dic_imports: dict[str, str] = OrderedDict(),
        set_deps: set[str] = set(),
        output: OrderedDict[str, type] = OrderedDict(),
    ):
        self.function = function
        self.dic_imports = dic_imports
        self.set_deps = set_deps
        self._output = output

    @property
    def output(self: Self):
        return self._output

    @output.setter
    def output(self: Self, dict_output: OrderedDict[str, type]):
        # Ensure that the number of arguments is the same
        if len(dict_output) != len(self._output):
            raise ValueError(
                f"Number of outputs is different. Previous: {len(self._output)}. New:"
                f" {len(dict_output)}"
            )
        # Ensure that the provided output(s) have the correct type
        for (new_output, new_type), (previous_output, previous_type) in zip(
            dict_output.items(), self._output.items()
        ):
            if new_type != previous_type:
                raise ValueError(
                    f"Output {new_output} has a different type. Previous type:"
                    f" {previous_type.__name__}. New type: {new_type.__name__}"
                )
        # Update output
        self._output = dict_output

    def get_str(self: Self) -> str:
        if self.function is None:
            logging.warning("No function defined for this block")
            return ""
        else:
            return inspect.getsource(self.function)

    def get_name_str(self: Self) -> str:
        if self.function is None:
            logging.warning("No function defined for this block")
            return ""
        else:
            return self.function.__name__

    def get_output_str(self: Self) -> str:
        return self.get_external_output_str(self.output)

    @staticmethod
    def get_external_output_str(output: OrderedDict[str, type] = OrderedDict()) -> str:
        if len(output) == 0:
            return ""
        else:
            if len(output) == 1:
                return list(output.keys())[0]
            else:
                return ", ".join([x for x in output.keys()])

    def get_output_type_hint_str(self: Self):
        return self.get_external_output_type_hint_str(self.output)

    # Static needed here when the output comes from a merge
    @staticmethod
    def get_external_output_type_hint_str(output: OrderedDict[str, type] = OrderedDict()) -> str:

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
        output_str = self.get_output_str()

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
                del parameters[key]
        # Then do the same for the argument block
        for key in block.output:
            if key not in block_parameters and key in parameters:
                del parameters[key]

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
        output_type_hint_str = self.get_external_output_type_hint_str(output)

        # Get output string
        output_str = self.get_output_str()

        # Get function header with the merged parameters
        parameters_header = ", ".join(
            [f"{parameter}: {parameters[parameter].__name__}" for parameter in parameters]
        )
        function_header = f"def {name_function}({parameters_header}) -> {output_type_hint_str}:"

        # Write docstring
        docstring = '''\t"""''' + "\n".join([f"{x}" for x in docstring.split("\n")]) + '''\n\t"""'''

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
    
    # ! TO FINISH
    # @classmethod
    # def get_multiple_merge_str(
    #     cls,
    #     l_blocks: Self,
    #     name_function: str,
    #     docstring: str = "",
    #     output: OrderedDict[str, type] = OrderedDict(),
    # ) -> str:

    #     # Get merged parameters
    #     parameters = self.get_merge_parameters(block)

    #     # Ensure that the output is accessible
    #     self.check_merge_output(block, output)

    #     # Build function string
    #     function_str = self.build_merge_str(block, name_function, docstring, output, parameters)

    #     return function_str

    def merge_imports(self: Self, block: Self) -> dict[str, str]:

        # Merge imports, ensuring that there are no conflicts
        dic_imports = self.dic_imports.copy()
        for module, alias in block.dic_imports.items():
            if module in dic_imports and dic_imports[module] != alias:
                raise ValueError(f"Import conflict for module {module}. Aliases are not consistent")
            else:
                dic_imports[module] = alias

        return dic_imports

    @staticmethod
    def write_temp_block(function_str: str, name_function: str) -> Callable:

        # Write string to temporary file
        tmp = tempfile.NamedTemporaryFile(suffix=".py", delete=False)

        # Open the file for writing.
        with open(tmp.name, "w") as f:
            f.write(function_str)
            tmp.flush()

        # Load the function
        spec = importlib.util.spec_from_file_location("mod", tmp.name)
        mod = importlib.util.module_from_spec(spec)
        sys.modules["mod"] = mod
        spec.loader.exec_module(mod)

        return getattr(mod, name_function)

    def merge_block(
        self: Self,
        block: Self,
        name_function: str,
        docstring: str = "",
        output: OrderedDict[str, type] = OrderedDict(),
    ) -> Self:

        # Build function string
        function_str = self.get_merge_str(block, name_function, docstring, output)

        # Write string to temporary file
        function = self.write_temp_block(function_str, name_function)

        # Merge imports
        dic_imports = self.merge_imports(block)

        # Add dependencies
        set_deps = set((self.get_name_str(), block.get_name_str()))

        return Block(function=function, dic_imports=dic_imports, set_deps=set_deps, output=output)

    # @classmethod
    # def merge_blocks(
    #     cls, l_blocks: list[Self], name_function: str, docstring: str = "", output=OrderedDict()
    # ) -> Self:
        
    #     # Build function string
        
