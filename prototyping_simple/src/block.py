import copy
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

    @property
    def parameters(self: Self) -> OrderedDict[str, type]:
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

    @parameters.setter
    def parameters(self: Self, dict_parameters: OrderedDict[str, type]):
        # Ensure that the number of arguments is the same
        if len(dict_parameters) != len(self.parameters):
            raise ValueError(
                f"Number of parameters is different. Previous: {len(self.parameters)}. New:"
                f" {len(dict_parameters)}"
            )

        # Ensure that the provided parameters have the correct type
        for (new_parameter, new_type), (previous_parameter, previous_type) in zip(
            dict_parameters.items(), self.parameters.items()
        ):
            if new_type != previous_type:
                raise ValueError(
                    f"Parameter {new_parameter} has a different type. Previous type:"
                    f" {previous_type.__name__}. New type: {new_type.__name__}"
                )

        # Update callable function
        function_str = self.prepare_function_str(dict_parameters=dict_parameters)

        # Write string to temporary file and update
        self.function = self.write_temp_block(function_str, self.get_name_str())

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

    def get_docstring(self: Self) -> str:
        if self.function is None:
            logging.warning("No function defined for this block")
            return ""
        else:
            doc = inspect.getdoc(self.function)
            if doc is None:
                return ""
            else:
                return doc

    def get_body_str(self: Self) -> str:
        if self.function is None:
            logging.warning("No function defined for this block")
            return ""
        else:
            body = inspect.getsource(self.function)
            # Remove header
            body = "\n".join(body.split(":\n")[1:])
            if self.get_docstring() != "":
                # Remove docstring
                body = body.replace(self.get_docstring(), "")
                # Remove remaining quotes
                body = body.replace('"""', "")
                body = body.replace("'''", "")

            return body

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
            return f"{self.function.__name__}({', '.join(self.parameters.keys())})"

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

    def get_parameters_assignation_str(self: Self, dict_parameters: OrderedDict[str, type]) -> str:
        old_dict_parameters = self.parameters
        return "\n".join(
            [
                f"\t{old_name} = {name}"
                for old_name, name in zip(old_dict_parameters, dict_parameters)
                if old_name != name
            ]
        )

    @classmethod
    def get_multiple_merge_parameters(
        cls, l_blocks: list[Self], output: OrderedDict[str, type] = OrderedDict()
    ) -> OrderedDict[str, type]:

        # Start with empty dictionnary of parameters
        dict_parameters = OrderedDict()

        # Progressively merge all parameters (two by two)
        for idx, block1 in enumerate(l_blocks):
            for block2 in l_blocks[idx + 1 :]:

                # Check that identical parameters have identical type
                for key in set(block1.parameters).intersection(block2.parameters):
                    if block1.parameters[key] != block2.parameters[key]:
                        raise ValueError(f"Parameter {key} has different types in the two blocks")

                dict_parameters = dict_parameters | block1.parameters | block2.parameters

        # If an output has been provided, remove it from the list of parameters
        # Except if it's modified inplace (inside of a block)
        for block in l_blocks:
            for key in block.output:
                if key not in block.parameters and key in dict_parameters:
                    del dict_parameters[key]

        # Return the merged parameters
        return dict_parameters

    @classmethod
    def check_external_merge_output(
        cls,
        l_blocks: list[Self],
        dict_parameters: OrderedDict[str, type],
        output: OrderedDict[str, type],
    ):
        # If the output is not None, ensure that the elements in it are either
        # - in the parameters (inplace operation)
        # - in the outputs
        if len(output) > 0:
            # Merge all output and parameters
            dic_block_parameters_and_outputs = copy.deepcopy(dict_parameters)
            for block in l_blocks:
                dic_block_parameters_and_outputs = dic_block_parameters_and_outputs | block.output

            # Check that all outputs are in the parameters or the outputs
            for key in output:
                if key not in dic_block_parameters_and_outputs:
                    raise ValueError(f"Output {key} is not in the parameters nor the outputs")

    @classmethod
    def build_funtion_str(
        cls,
        l_blocks: list[Self],
        function_header: str,
        parameters_assignation_str: str = "",
        function_body: str | None = None,
        docstring: str = "",
        output_str: str | None = None,
    ):

        # Write docstring
        docstring = '''\t"""''' + "\n".join([f"{x}" for x in docstring.split("\n")]) + '''\n\t"""'''

        # Write function body: call all functions successively
        if function_body is None:
            function_body = "\n".join(
                [f"\t{block.get_assignation_call_str()}" for block in l_blocks]
            )

        # Write function output
        if output_str is not None:
            function_output = f"\treturn {output_str}"
        else:
            function_output = ""

        # Write full function
        function_str = "\n".join(
            [function_header, docstring, parameters_assignation_str, function_body, function_output]
        )

        # Replace tabs by spaces to prevent inconsistent indentation
        function_str = function_str.replace("\t", "    ")

        return function_str

    def prepare_function_str(
        self,
        name_function: str | None = None,
        docstring: str | None = None,
        dict_parameters: OrderedDict[str, type] | None = None,
    ) -> str:

        # Get output type hint string and output name (can't modify the output type, and output name
        # must be modified through the corresponding setter)
        output_type_hint_str = self.get_output_type_hint_str()

        # Get function names and parameters, with a flag for the updated parameters
        if name_function is None:
            name_function = self.get_name_str()
        if dict_parameters is None:
            parameters_assignation_str = ""
            dict_parameters = self.parameters
        else:
            # Update parameters assignation at the beginning of the function body
            parameters_assignation_str = self.get_parameters_assignation_str(dict_parameters)

        # Get function header with the (potentially updated) function name and parameters
        parameters_header = ", ".join(
            [f"{parameter}: {dict_parameters[parameter].__name__}" for parameter in dict_parameters]
        )
        function_header = f"def {name_function}({parameters_header}) -> {output_type_hint_str}:"

        # Get potentially updated docstring
        if docstring is None:
            docstring = self.get_docstring()

        # Get function body (including return statement)
        function_body = self.get_body_str()

        # Build function string
        function_str = self.build_funtion_str(
            [self],
            function_header,
            parameters_assignation_str=parameters_assignation_str,
            function_body=function_body,
            docstring=docstring,
            output_str=None,
        )

        return function_str

    @classmethod
    def build_external_merge_str(
        cls,
        l_blocks: list[Self],
        name_function: str,
        docstring: str = "",
        output: OrderedDict[str, type] = OrderedDict(),
        dict_parameters: OrderedDict[str, type] = OrderedDict(),
    ) -> str:

        # Get output type hint string
        output_type_hint_str = cls.get_external_output_type_hint_str(output)

        # Get output string
        output_str = cls.get_external_output_str(output)

        # Get function header with the merged parameters
        parameters_header = ", ".join(
            [f"{parameter}: {dict_parameters[parameter].__name__}" for parameter in dict_parameters]
        )
        function_header = f"def {name_function}({parameters_header}) -> {output_type_hint_str}:"

        # Build function string
        function_str = cls.build_funtion_str(
            l_blocks, function_header, docstring=docstring, output_str=output_str
        )

        return function_str

    @classmethod
    def get_multiple_merge_str(
        cls,
        l_blocks: list[Self],
        name_function: str,
        docstring: str = "",
        output: OrderedDict[str, type] = OrderedDict(),
    ) -> str:

        # Get merged parameters
        dict_parameters = cls.get_multiple_merge_parameters(l_blocks, output)

        # Ensure that the output is accessible
        cls.check_external_merge_output(l_blocks, dict_parameters, output)

        # Build function string
        function_str = cls.build_external_merge_str(
            l_blocks, name_function, docstring, output, dict_parameters
        )

        return function_str

    @classmethod
    def merge_multiple_imports(cls, l_blocks: list[Self]) -> dict[str, str]:

        # Merge imports, ensuring that there are no conflicts
        dic_imports = OrderedDict()
        for block in l_blocks:
            for module, alias in block.dic_imports.items():
                if module in dic_imports:
                    if dic_imports[module] != alias:
                        raise ValueError(
                            f"Import conflict for module {module}. Aliases are not consistent"
                        )
                else:
                    dic_imports[module] = alias

        return dic_imports

    @classmethod
    def merge_multiple_dependencies(cls, l_blocks: list[Self]) -> set[str]:
        set_imports = set()
        for block in l_blocks:
            set_imports.add(block.get_name_str())
        return set_imports

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
        return self.merge_blocks([self, block], name_function, docstring, output)

    @classmethod
    def merge_blocks(
        cls, l_blocks: list[Self], name_function: str, docstring: str = "", output=OrderedDict()
    ) -> Self:

        # Build function string
        function_str = cls.get_multiple_merge_str(l_blocks, name_function, docstring, output)

        # Write string to temporary file
        function = cls.write_temp_block(function_str, name_function)

        # Merge imports
        dic_imports = cls.merge_multiple_imports(l_blocks)

        # Add dependencies
        set_deps = cls.merge_multiple_dependencies(l_blocks)

        return Block(function=function, dic_imports=dic_imports, set_deps=set_deps, output=output)
