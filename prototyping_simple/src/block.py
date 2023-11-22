import inspect
from dataclasses import dataclass
from typing import Callable


@dataclass
class Block:
    function: Callable
    dic_imports: dict[str, str] | None = None

    def get_function_str(self):
        return inspect.getsource(self.function)

    # def get_function_signature(self):
    #     return inspect.signature(self.function)

    def get_function_params(self):
        return inspect.signature(self.function).parameters
