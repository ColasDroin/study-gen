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
        name: str,
        function: Callable,
        dict_imports: dict[str, str] = OrderedDict(),
        set_deps: set[str] = set(),
        dict_output: OrderedDict[str, type] | None = None,
    ):
        self.name = name
        self._function = function
        self.dict_imports = dict_imports
        self.set_deps = set_deps
        self._l_arguments = []

        # Set output
        if dict_output is None:
            self._dict_output = self.initial_dic_output_setter_from_signature()
        else:
            self._dict_output = self.initial_dic_output_setter_from_output(dict_output)

    @property
    def function(self: Self) -> Callable:
        if self._function is None:
            logging.warning("No function defined for this block")
        return self._function

    @function.setter
    def function(self: Self, function: Callable):
        self._function = function

    @property
    def dict_output(self: Self) -> OrderedDict[str, type]:
        return self._dict_output

    def initial_dic_output_setter_from_signature(self: Self) -> OrderedDict[str, type]:
        # Get signature output as str
        signature_output_str = str(self.get_signature())

        # Check that output exists
        if "->" in signature_output_str:
            signature_output_str = signature_output_str.split("->")[1].strip()
        else:
            raise ValueError(f"Block {self.name} has no output signature")

        # Create empty dict_output
        dict_output = OrderedDict()

        # Get signature hint output
        signature_type_hint = self.get_output_type_from_signature()

        # Check if several outputs are defined
        if "tuple[" in signature_output_str:
            # Create each output name and type from the signature
            for type_output in signature_type_hint.__args__:  # type: ignore
                dict_output[f"output_{len(dict_output)}_{self.name}"] = type_output
        elif signature_type_hint is not None:
            # Create output name and type from the signature
            dict_output[f"output_{self.name}"] = signature_type_hint

        return dict_output

    def initial_dic_output_setter_from_output(
        self: Self, dict_output: OrderedDict[str, type]
    ) -> OrderedDict[str, type]:
        # Check that the output corresponds to the return statement
        if len(dict_output) == 0 and "return" in self.get_str():
            logging.warning(
                f"Block {self.name} has no output defined, but the function has a return statement"
            )

        # Get signature output as str
        signature_output_str = str(self.get_signature())

        # Check that output exists
        if "->" in signature_output_str:
            signature_output_str = signature_output_str.split("->")[1].strip()
        else:
            raise ValueError(f"Block {self.name} has no output signature")

        # Get signature hint output
        signature_type_hint = self.get_output_type_from_signature()

        # Check if several outputs are defined
        if "tuple[" in signature_output_str:
            # Check that the number of outputs is the same
            if len(dict_output) != len(signature_type_hint.__args__):  # type: ignore
                raise ValueError(
                    f"Number of outputs differs from type hint signature for block {self.name}."
                )

            # Check that the provided output(s) have the correct type
            if signature_type_hint is not None:
                # Compare the signature type hint of each output (unpacked) with the provided output type hints
                for output, type_output in zip(dict_output, signature_type_hint.__args__):  # type: ignore
                    if type_output != dict_output[output]:
                        raise ValueError(
                            f"Output {output} has a different type than expected:"
                            f" {type_output.__name__} Instead of:"
                            f" {dict_output[output].__name__} for block {self.name}"
                        )
        elif len(dict_output) > 1:
            raise ValueError(
                "Number of outputs differs from type hint signature for block {self.name}."
            )
        elif len(dict_output) == 0:
            if signature_type_hint is not None:
                raise ValueError(
                    f"No output provided in dict_output for block {self.name}, while signature"
                    f" shows one output of type {signature_type_hint.__name__}"
                )
        elif signature_type_hint != list(dict_output.values())[0]:
            raise ValueError(
                f"Output {list(dict_output.keys())[0]} has a different type than expected:"
                f" {signature_type_hint.__name__} Instead of:"  # type: ignore
                f" {list(dict_output.values())[0].__name__} for block {self.name}"
            )

        return dict_output

    @dict_output.setter
    def dict_output(self: Self, dict_output: OrderedDict[str, type]):
        # Ensure that the number of arguments is the same
        if len(dict_output) != len(self._dict_output):
            raise ValueError(
                f"Number of outputs is different for block {self.name}. Previous:"
                f" {len(self._dict_output)}. New: {len(dict_output)}"
            )
        # Ensure that the provided output(s) have the correct type
        for (new_output, new_type), (previous_output, previous_type) in zip(
            dict_output.items(), self._dict_output.items()
        ):
            if new_type != previous_type:
                raise ValueError(
                    f"Output {new_output} has a different type for block {self.name}. Previous"
                    f" type: {previous_type.__name__}. New type: {new_type.__name__}"
                )
        # Update output
        self._dict_output = dict_output

    def set_outputs_names(self: Self, l_outputs_names: list[str] | str | None):
        # Ensure that l_outputs_names is not just a string
        if not isinstance(l_outputs_names, list):
            # Ensure the user did not provide a string with a comma
            if l_outputs_names is None:
                l_outputs_names = []
            elif "," in l_outputs_names:
                l_outputs_names = [x.strip() for x in l_outputs_names.split(",")]
            else:
                l_outputs_names = [l_outputs_names]

        # Only update the names of the outputs, not types
        self.dict_output = OrderedDict(list(zip(l_outputs_names, self.dict_output.values())))

    def get_outputs_names(self: Self) -> list[str]:
        return [output for output, _ in self.dict_output.items()]

    @property
    def dict_parameters(self: Self) -> OrderedDict[str, type]:
        signature = self.get_signature()
        return OrderedDict(
            [
                (parameter, signature.parameters[parameter].annotation)
                for parameter in signature.parameters
            ]
        )

    def get_dict_parameters_names(self: Self) -> list[str]:
        return list(self.dict_parameters.keys())

    @dict_parameters.setter
    def dict_parameters(self: Self, dict_parameters: OrderedDict[str, type]):
        # Ensure that the number of arguments is the same
        if len(dict_parameters) != len(self.dict_parameters):
            raise ValueError(
                f"Number of parameters is different. Previous: {len(self.dict_parameters)}. New:"
                f" {len(dict_parameters)}"
            )

        # Update callable function
        function_header, function_body, docstring = self.prepare_function_str(
            dict_parameters=dict_parameters
        )

        # Build function string (return statement is already included in the function body)
        function_str = self.build_function_str(
            [self],
            function_header,
            function_body=function_body,
            docstring=docstring,
            output_str=None,
        )

        # Write string to temporary file and update
        self.function = self.write_and_load_temp_block(
            function_str, self.get_name_function_str(), self.dict_imports
        )

    def set_parameters_names(self: Self, l_parameters_names: list[str]):
        # Ensure that l_parameters_names is not just a string (from bad yaml parsing)
        if not isinstance(l_parameters_names, list):
            l_parameters_names = [l_parameters_names]

        # Only update the names of the parameters, not types
        self.dict_parameters = OrderedDict(
            list(zip(l_parameters_names, self.dict_parameters.values()))
        )

    @property
    def l_arguments(self: Self) -> list[tuple[str, type]]:
        # if self._l_arguments == []:
        #     logging.warning(f"No arguments defined for this block ({self.name})")
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

    def set_arguments_names(self: Self, l_arguments_names: list[str] | None):
        # Ensure that l_arguments_names is not just a string (from bad yaml parsing)
        if not isinstance(l_arguments_names, list):
            # Ensure the user did not provide a string with a comma
            if l_arguments_names is None:
                l_arguments_names = []
            elif "," in l_arguments_names:
                l_arguments_names = [x.strip() for x in l_arguments_names.split(",")]  # type: ignore
            else:
                l_arguments_names = [l_arguments_names]

        # Ensure that arguments_names has not more elements than the number of parameters
        if l_arguments_names is not None and len(l_arguments_names) > len(self.dict_parameters):
            raise ValueError(
                "Number of arguments is different from number of parameters. Number of parameters:"
                f" {len(self.dict_parameters)}. Number of arguments: {len(l_arguments_names)}"
            )

        # Only update the names of the parameters, not types (obtain the types from the parameters)
        self._l_arguments = list(zip(l_arguments_names, self.dict_parameters.values()))

    def get_arguments_names(self: Self) -> list[str]:
        return [arg for arg, _ in self.l_arguments]

    def get_arguments_as_dict(self: Self) -> OrderedDict[str, type]:
        return OrderedDict(self.l_arguments)

    def get_str(self: Self) -> str:
        return "" if self.function is None else inspect.getsource(self.function)

    def get_name_function_str(self: Self) -> str:
        return "" if self.function is None else self.function.__name__

    def get_docstring(self: Self) -> str:
        if self.function is None:
            return ""
        doc = inspect.getdoc(self.function)
        return "" if doc is None else doc

    def get_body_str(self: Self) -> str:
        if self.function is None:
            return ""
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
    def get_external_output_str(l_outputs: list[str] | None = None) -> str:
        if l_outputs is None:
            l_outputs = []
        if not l_outputs:
            return ""
        else:
            return l_outputs[0] if len(l_outputs) == 1 else ", ".join(l_outputs)

    def get_output_type_hint_str(self: Self):
        return self.get_external_output_type_hint_str(self.dict_output)

    # Static needed here when the output comes from a merge
    @staticmethod
    def get_external_output_type_hint_str(
        dict_output: OrderedDict[str, type] = OrderedDict(),
    ) -> str:
        if len(dict_output) == 0:
            return "None"
        elif len(dict_output) > 1:
            output_str = ", ".join([x.__name__ for x in dict_output.values()])
            return f"tuple[{output_str}]"
        else:
            return list(dict_output.values())[0].__name__

    def get_call_str(self: Self, l_external_arguments: list[str] | None = None) -> str:
        if self.function is None:
            logging.warning("No function defined for this block")
            return ""
        else:
            if l_external_arguments is None:
                l_external_arguments = self.get_arguments_names()
            if len(l_external_arguments) > len(self.dict_parameters):
                raise ValueError(
                    "Number of arguments is different from number of parameters. Number of parameters:"
                    f" {len(self.dict_parameters)}. Number of arguments: {len(l_external_arguments)}"
                )
            return f"{self.function.__name__}({', '.join(l_external_arguments)})"

    def get_assignation_call_str(self: Self) -> str:
        function_call_str = self.get_call_str()
        output_str = self.get_output_str()

        if output_str == "":
            return function_call_str
        else:
            return f"{output_str} = {function_call_str}"

    def get_signature(self: Self) -> inspect.Signature:
        if self.function is not None:
            return inspect.signature(self.function)
        logging.warning("No function defined for this block")
        return inspect.Signature()

    def get_output_type_from_signature(self: Self) -> type | None:
        if self.function is not None:
            return self.get_signature().return_annotation
        logging.warning("No function defined for this block")
        return None

    def get_l_imports_str(self: Self) -> str:
        return self.get_external_l_imports_str(self.dict_imports)

    @staticmethod
    def get_external_l_imports_str(dict_imports: dict[str, str]) -> str:
        # Write import statements (do not check for import repetitions across blocks)
        return "\n".join([import_statement for package, import_statement in dict_imports.items()])

    def prepare_function_str(
        self,
        name_function: str | None = None,
        docstring: str | None = None,
        dict_parameters: OrderedDict[str, type] | None = None,
    ) -> tuple[str, str, str]:
        # Get output type hint string and output name (can't modify the output type, and output name
        # must be modified through the corresponding setter)
        output_type_hint_str = self.get_output_type_hint_str()

        # Get function names and parameters
        if name_function is None:
            name_function = self.get_name_function_str()
        if dict_parameters is None:
            dict_parameters = self.dict_parameters

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

        return function_header, function_body, docstring

    @classmethod
    def build_function_str(
        cls,
        l_blocks: list[Self],
        function_header: str,
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
        if output_str is not None and output_str != "":
            function_output = f"\treturn {output_str}"
        else:
            function_output = ""

        # Write full function
        function_str = "\n".join([function_header, docstring, function_body, function_output])

        return function_str.replace("\t", "    ")

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
        spec.loader.exec_module(mod)  # type: ignore

        return getattr(mod, name_function)
