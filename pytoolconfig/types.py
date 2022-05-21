"""PyToolConfig internal definitions and functions."""
from datetime import date, datetime, time
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Tuple, Union

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal
try:
    from pydantic.dataclasses import Dataclass, dataclass

except ImportError:
    from dataclasses import dataclass

    Dataclass = Literal["Dataclass"]
_base_types = Union[str, int, float, datetime, date, time, bool]
_base_types_with_list = Union[_base_types, List[_base_types]]
key = Union[Dict[str, _base_types_with_list], _base_types_with_list]


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
    command_line: Optional[Union[Tuple[str]]] = None
    _type: Any = None
    _default: Any = None
