# ==================================================================================================
# --- Imports
# ==================================================================================================
# Standard library imports
import importlib.metadata

# Local imports
from .block import Block
from .merge import merge_blocks, merge_imports
from .study_gen import StudyGen

__all__ = ["Block", "merge_blocks", "merge_imports", "StudyGen"]

# ==================================================================================================
# --- Package version
# ==================================================================================================
try:
    __version__ = importlib.metadata.version("study-gen")
except importlib.metadata.PackageNotFoundError:
    __version__ = "unknown"
