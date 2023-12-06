import importlib.util
import inspect
import logging
import sys
import tempfile
from collections import OrderedDict
from typing import Any, Callable, Self


class Block:
    def __init__(
        self,
        function: Callable | None = None,
        dict_imports: dict[str, str] = OrderedDict(),
        set_deps: set[str] = set(),
        dict_output: OrderedDict[str, type] = OrderedDict(),
    ):
        self.function = function
        self.dict_imports = dict_imports
        self.set_deps = set_deps
        self._dict_output = dict_output

    @property
    def dict_output(self: Self):
        return self._dict_output

    @dict_output.setter
    def dict_output(self: Self, dict_output: OrderedDict[str, type]):
        # Ensure that the number of arguments is the same
        if len(dict_output) != len(self._dict_output):
            raise ValueError(
                f"Number of outputs is different. Previous: {len(self._dict_output)}. New:"
                f" {len(dict_output)}"
            )
        # Ensure that the provided output(s) have the correct type
        for (new_output, new_type), (previous_output, previous_type) in zip(
            dict_output.items(), self._dict_output.items()
        ):
            if new_type != previous_type:
                raise ValueError(
                    f"Output {new_output} has a different type. Previous type:"
                    f" {previous_type.__name__}. New type: {new_type.__name__}"
                )
        # Update output
        self._dict_output = dict_output

    def set_outputs_names(self: Self, l_outputs_names: list[str]):
        # Ensure that l_outputs_names is not just a string
        if not isinstance(l_outputs_names, list):
            l_outputs_names = [l_outputs_names]

        # Only update the names of the outputs, not types
        self.dict_output = OrderedDict(
            [
                (output, type_output)
                for output, type_output in zip(l_outputs_names, self.dict_output.values())
            ]
        )

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
        self.function = self.write_and_load_temp_block(function_str, self.get_name_str())

    def set_parameters_names(self: Self, l_parameters_names: list[str]):
        # Ensure that l_parameters_names is not just a string
        if not isinstance(l_parameters_names, list):
            l_parameters_names = [l_parameters_names]

        # Only update the names of the parameters, not types
        self.parameters = OrderedDict(
            [
                (param, type_param)
                for param, type_param in zip(l_parameters_names, self.parameters.values())
            ]
        )

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

    def get_output_str(self: Self, l_outputs: list[str] | None = None) -> str:
        if l_outputs is None:
            l_outputs = list(self.dict_output.keys())
        return self.get_external_output_str(l_outputs)

    @staticmethod
    def get_external_output_str(l_outputs: list[str] = []) -> str:
        if len(l_outputs) == 0:
            return ""
        else:
            if len(l_outputs) == 1:
                return l_outputs[0]
            else:
                return ", ".join(l_outputs)

    def get_output_type_hint_str(self: Self):
        return self.get_external_output_type_hint_str(self.dict_output)

    # Static needed here when the output comes from a merge
    @staticmethod
    def get_external_output_type_hint_str(
        dict_output: OrderedDict[str, type] = OrderedDict()
    ) -> str:

        if len(dict_output) == 0:
            output_hint_str = "None"
        else:
            if len(dict_output) > 1:
                output_str = ", ".join([x.__name__ for x in dict_output.values()])
                output_hint_str = f"tuple[{output_str}]"
            else:
                output_hint_str = list(dict_output.values())[0].__name__

        return output_hint_str

    def get_call_str(self: Self, l_arguments: list[str] | None = None) -> str:
        if self.function is None:
            logging.warning("No function defined for this block")
            return ""
        else:
            if l_arguments is None:
                l_arguments = list(self.parameters.keys())
            return f"{self.function.__name__}({', '.join(l_arguments)})"

    def get_assignation_call_str(
        self: Self,
        l_arguments: list[str] | None = None,
        l_outputs: list[str] | None = None,
    ) -> str:
        function_call_str = self.get_call_str(l_arguments)
        output_str = self.get_output_str(l_outputs)

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

    def get_l_imports_str(self: Self) -> str:
        return self.get_external_l_imports_str(self.dict_imports)

    @staticmethod
    def get_external_l_imports_str(dict_imports: dict[str, str]) -> str:
        # Write import statements (do not check for import repetitions across blocks)
        return "\n".join(
            [f"import {package} as {alias}" for package, alias in dict_imports.items()]
        )

    @classmethod
    def build_function_str(
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
        function_str = self.build_function_str(
            [self],
            function_header,
            parameters_assignation_str=parameters_assignation_str,
            function_body=function_body,
            docstring=docstring,
            output_str=None,
        )

        return function_str

    @staticmethod
    def write_and_load_temp_block(function_str: str, name_function: str) -> Callable:

        # Write string to temporary file
        tmp = tempfile.NamedTemporaryFile(suffix=".py", delete=False)

        # Open the file for writing.
        with open(tmp.name, "w") as f:
            f.write(function_str)
            tmp.flush()

        # Load the function
        spec = importlib.util.spec_from_file_location("mod", tmp.name)
        mod = importlib.util.module_from_spec(spec)  # type: ignore
        sys.modules["mod"] = mod
        spec.loader.exec_module(mod)

        return getattr(mod, name_function)
