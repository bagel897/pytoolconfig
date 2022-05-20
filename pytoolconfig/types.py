"""PyToolConfig internal definitions and functions. Largely dealing with the type hinting system of pydantic/dataclasses."""
from datetime import date, datetime, time
from typing import Any, Dict, List, Literal, Optional, Tuple, Union

try:
    from pydantic.dataclasses import Dataclass, dataclass

except ImportError:
    from dataclasses import dataclass

    Dataclass = Literal["Dataclass"]
_base_types = Union[str, int, float, datetime, date, time, bool]
_base_types_with_list = Union[_base_types, List[_base_types]]
key = Union[Dict[str, _base_types_with_list], _base_types_with_list]


@dataclass
class ConfigField:
    """Dataclass store and validate fields in a configuration model."""

    description: Optional[str] = None
    universal_config: Optional[str] = None
    command_line: Optional[Union[Tuple[str]]] = None
    _type: Any = None
    _default: Any = None
