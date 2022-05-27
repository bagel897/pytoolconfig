"""PyToolConfig internal definitions and functions."""

import sys
from dataclasses import dataclass
from datetime import date, datetime, time
from enum import Enum, auto
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple, Union

if sys.version_info < (3, 10, 0):
    from typing_extensions import TypeGuard
else:
    from typing import TypeGuard


if TYPE_CHECKING:
    try:
        from pydantic.dataclasses import Dataclass
    except ModuleNotFoundError:

        class Dataclass:
            """Dataclass stub for type checking purposes."""

            pass

else:
    Dataclass = "Dataclass"


_BaseType = Union[str, int, float, datetime, date, time, bool]
_BaseTypeWithList = Union[_BaseType, List[_BaseType]]
Key = Union[Dict[str, _BaseTypeWithList], _BaseTypeWithList]


def _is_dataclass(field_type: Any) -> TypeGuard[Dataclass]:
    return hasattr(field_type, "__dataclass_params__")


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
