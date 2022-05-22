"""PyToolConfig internal definitions and functions."""
from datetime import date, datetime, time
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional, Tuple, Type, Union

dataclass: Callable
Dataclass: Type
try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal
try:
    from pydantic.dataclasses import Dataclass, dataclass

except ImportError:
    from dataclasses import dataclass

    Dataclass = Literal["Dataclass"]
_BaseType = Union[str, int, float, datetime, date, time, bool]
_BaseTypeWithList = Union[_BaseType, List[_BaseType]]
Key = Union[Dict[str, _BaseTypeWithList], _BaseTypeWithList]


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

    description: Optional[str] = None
    universal_config: Optional[UniversalKey] = None
    command_line: Optional[Tuple[str]] = None
    _type: Any = None
    _default: Any = None
