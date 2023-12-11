import importlib.util
import inspect
import logging
import sys
import tempfile
from ast import Or
from collections import OrderedDict
from typing import Any, Callable, Self


class Block:
    def __init__(
        self,
        name: str,
        function: Callable | None = None,
        dict_imports: dict[str, str] = OrderedDict(),
        set_deps: set[str] = set(),
        dict_output: OrderedDict[str, type] = OrderedDict(),
    ):
        self.name = name
        self._function = function
        self.dict_imports = dict_imports
        self.set_deps = set_deps
        self._dict_output = dict_output
        self._l_arguments = []

    @property
    def function(self: Self) -> Callable | None:
        if self._function is None:
            logging.warning("No function defined for this block")
        return self._function

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

    def get_outputs_names(self: Self) -> list[str]:
        return [output for output, _ in self.dict_output.items()]

    @property
    def dict_parameters(self: Self) -> OrderedDict[str, type]:
        signature = self.get_signature()
        dict_parameters = OrderedDict(
            [
                (parameter, signature.parameters[parameter].annotation)
                for parameter in signature.parameters
            ]
        )
        return dict_parameters

    # @dict_parameters.setter
    # def dict_parameters(self: Self, dict_parameters: OrderedDict[str, type]):

    #     # Ensure that the number of arguments is the same
    #     if len(dict_parameters) != len(self.dict_parameters):
    #         raise ValueError(
    #             f"Number of parameters is different. Previous: {len(self.dict_parameters)}. New:"
    #             f" {len(dict_parameters)}"
    #         )

    #     # Ensure that the provided parameters have the correct type
    #     for (new_parameter, new_type), (previous_parameter, previous_type) in zip(
    #         dict_parameters.items(), self.dict_parameters.items()
    #     ):
    #         if new_type != previous_type:
    #             raise ValueError(
    #                 f"Parameter {new_parameter} has a different type. Previous type:"
    #                 f" {previous_type.__name__}. New type: {new_type.__name__}"
    #             )

    #     # Update callable function
    #     function_header, parameters_assignation_str, function_body, docstring = (
    #         self.prepare_function_str(dict_parameters=dict_parameters)
    #     )

    #     # Build function string
    #     function_str = self.build_function_str(
    #         [self],
    #         function_header,
    #         parameters_assignation_str=parameters_assignation_str,
    #         function_body=function_body,
    #         docstring=docstring,
    #         output_str=None,
    #     )

    #     # Write string to temporary file and update
    #     self.function = self.write_and_load_temp_block(
    #         function_str, self.get_name_str(), self.dict_imports
    #     )

    # def set_parameters_names(self: Self, l_parameters_names: list[str]):
    #     # Ensure that l_parameters_names is not just a string (from bad yaml parsing)
    #     if not isinstance(l_parameters_names, list):
    #         l_parameters_names = [l_parameters_names]

    #     # Only update the names of the parameters, not types
    #     self.dict_parameters = OrderedDict(
    #         [
    #             (param, type_param)
    #             for param, type_param in zip(l_parameters_names, self.dict_parameters.values())
    #         ]
    #     )

    @property
    def l_arguments(self: Self) -> list[tuple[str, type]]:
        if self._l_arguments == []:
            logging.warning("No arguments defined for this block")
        return self._l_arguments

    @l_arguments.setter
    def l_arguments(self: Self, l_arguments: list[tuple[str, type]]):

        # Ensure that the number of arguments is the same
        if len(l_arguments) != len(self.dict_parameters):
            raise ValueError(
                "Number of arguments is different from number of parameters. Number of parameters:"
                f" {len(self.dict_parameters)}. Number of arguments: {len(l_arguments)}"
            )

        # Ensure that the provided arguments have the correct type
        for (argument, argument_type), (parameter, parameter_type) in zip(
            l_arguments, self.dict_parameters.items()
        ):
            if argument_type != parameter_type:
                raise ValueError(
                    f"Argument {argument} has a different type than expected:"
                    f" {argument_type.__name__}. Instead of: {parameter_type.__name__}"
                )

        # Update list of arguments
        self._l_arguments = l_arguments

    def set_arguments_names(self: Self, l_arguments_names: list[str]):

        # Ensure that l_arguments_names is not just a string (from bad yaml parsing)
        if not isinstance(l_arguments_names, list):
            l_arguments_names = [l_arguments_names]

        # Only update the names of the parameters, not types (obtain the types from the parameters)
        self._l_arguments = [
            (arg, type_param)
            for arg, type_param in zip(l_arguments_names, self.dict_parameters.values())
        ]

    def get_arguments_names(self: Self) -> list[str]:
        return [arg for arg, _ in self.l_arguments]

    def get_arguments_as_dict(self: Self) -> OrderedDict[str, type]:
        return OrderedDict(self.l_arguments)

    def get_str(self: Self) -> str:
        if self.function is None:
            return ""
        else:
            return inspect.getsource(self.function)

    def get_name_function_str(self: Self) -> str:
        if self.function is None:
            return ""
        else:
            return self.function.__name__

    def get_docstring(self: Self) -> str:
        if self.function is None:
            return ""
        else:
            doc = inspect.getdoc(self.function)
            if doc is None:
                return ""
            else:
                return doc

    def get_body_str(self: Self) -> str:
        if self.function is None:
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
        l_outputs = self.get_outputs_names()
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

    def get_call_str(self: Self) -> str:
        if self.function is None:
            logging.warning("No function defined for this block")
            return ""
        else:
            return f"{self.function.__name__}({', '.join(self.get_arguments_names())})"

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

    # # ! Hopefully using arguments instead of parameters will fix this unelegant function as well
    # def get_parameters_assignation_str(self: Self, dict_parameters: OrderedDict[str, type]) -> str:
    #     old_dict_parameters = self.dict_parameters
    #     return "\n".join(
    #         [
    #             f"\t{old_name} = {name}"
    #             for old_name, name in zip(old_dict_parameters, dict_parameters)
    #             if old_name != name
    #         ]
    #     )

    def get_l_imports_str(self: Self) -> str:
        return self.get_external_l_imports_str(self.dict_imports)

    @staticmethod
    def get_external_l_imports_str(dict_imports: dict[str, str]) -> str:
        # Write import statements (do not check for import repetitions across blocks)
        return "\n".join([import_statement for package, import_statement in dict_imports.items()])

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
        if docstring != "":
            docstring = (
                '''\t"""''' + "\n".join([f"{x}" for x in docstring.split("\n")]) + '''\n\t"""'''
            )

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

    # def prepare_function_str(
    #     self,
    #     name_function: str | None = None,
    #     docstring: str | None = None,
    #     dict_parameters: OrderedDict[str, type] | None = None,
    # ) -> tuple[str, str, str, str]:

    #     # Get output type hint string and output name (can't modify the output type, and output name
    #     # must be modified through the corresponding setter)
    #     output_type_hint_str = self.get_output_type_hint_str()

    #     # Get function names and parameters
    #     if name_function is None:
    #         name_function = self.get_name_str()
    #     if dict_parameters is None:
    #         parameters_assignation_str = ""
    #         dict_parameters = self.dict_parameters
    #     else:
    #         # Update parameters assignation at the beginning of the function body
    #         parameters_assignation_str = self.get_parameters_assignation_str(dict_parameters)

    #     # Get function header with the (potentially updated) function name and parameters
    #     parameters_header = ", ".join(
    #         [f"{parameter}: {dict_parameters[parameter].__name__}" for parameter in dict_parameters]
    #     )
    #     function_header = f"def {name_function}({parameters_header}) -> {output_type_hint_str}:"

    #     # Get potentially updated docstring
    #     if docstring is None:
    #         docstring = self.get_docstring()

    #     # Get function body (including return statement)
    #     function_body = self.get_body_str()

    #     return function_header, parameters_assignation_str, function_body, docstring

    @classmethod
    def write_and_load_temp_block(
        cls, function_str: str, name_function: str, dict_imports: dict[str, str]
    ) -> Callable:

        # Write string to temporary file
        tmp = tempfile.NamedTemporaryFile(suffix=".py", delete=False)

        # Open the file for writing.
        with open(tmp.name, "w") as f:
            f.write(cls.get_external_l_imports_str(dict_imports))
            f.write("\n")
            f.write(function_str)
            tmp.flush()

        # Load the function
        spec = importlib.util.spec_from_file_location("mod", tmp.name)
        mod = importlib.util.module_from_spec(spec)  # type: ignore
        sys.modules["mod"] = mod
        spec.loader.exec_module(mod)

        return getattr(mod, name_function)
