"""PyToolConfig internal definitions and functions."""

from __future__ import annotations

import sys
from dataclasses import dataclass
from enum import Enum, auto
from typing import TYPE_CHECKING, Any, Dict

if sys.version_info >= (3, 10):
    from typing import TypeAlias
else:
    from typing_extensions import TypeAlias
if TYPE_CHECKING:
    JSON: TypeAlias = dict[str, "JSON"] | list["JSON"] | str | int | float | bool | None
else:
    JSON = Dict[str, Any]
JSON_DICT = Dict[str, JSON]


# We have a circular dependency preventing us from generating universal keys from
# universal_config. Universal Config requires field, which requires Universal Key.
class UniversalKey(Enum):
    """See universal config documentation."""

    formatter = auto()
    max_line_length = auto()
    min_py_version = auto()
    max_py_version = auto()
    dependencies = auto()
    optional_dependencies = auto()
    version = auto()


@dataclass
class ConfigField:
    """Dataclass store and validate fields in a configuration model."""

    description: str | None = None
    universal_config: UniversalKey | None = None
    command_line: tuple[str, ...] | None = None
    _type: Any = None
    _default: Any = None


class ValidationError(BaseException):
    """Raised when the configuration is invalid."""

    def __init__(self, message: str) -> None:
        """Raise a validation error."""
        super().__init__(message)


__alll__ = [
    "JSON",
    "JSON_DICT",
    "UniversalKey",
    "ConfigField",
    "ValidationError",
]
