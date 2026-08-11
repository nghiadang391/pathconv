"""pathconv — convert file paths between Windows and Unix conventions.

Handles separator swapping (``\\`` <-> ``/``), UNC/drive prefixes, and an
optional configurable *prefix mapping* (network share root <-> mount point).
"""

from .core import Mapping, convert, detect_direction

__all__ = ["Mapping", "convert", "detect_direction"]
__version__ = "0.1.0"
