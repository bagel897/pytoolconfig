from dataclasses import fields
from datetime import date, datetime, time
from typing import Any, Dict, List, Optional, Tuple, Type, Union

try:
    from typing import Annotated, get_args, get_origin, get_type_hints
except ImportError:
    from typing_extensions import Annotated
try:
    from pydantic.dataclasses import BaseModel, Dataclass, dataclass

    pydantic = True
except ImportError:
    from dataclasses import dataclass

    Dataclass = Type["Dataclass"]
    pydantic = False
_base_types = Union[str, int, float, datetime, date, time, bool]
_base_types_with_list = Union[_base_types, List[_base_types]]
key = Union[Dict[str, _base_types_with_list], _base_types_with_list]


@dataclass
class ConfigField:
    """Dataclass store and validate fields in a configuration model."""

    description: Optional[str] = None
    universal_config: Optional[str] = None
    command_line: Optional[Union[Tuple[str], str]] = None
    _type: Any = None
    _default: Any = None


@dataclass
class UniversalConfig:
    """Universal Configuration base model."""

    formatter: Annotated[
        Optional[str], ConfigField("Formatter used to format this File")
    ] = None
    max_line_length: Annotated[
        Optional[int], ConfigField(description="Maximum line length")
    ] = None

    min_py_version: Annotated[
        Optional[Tuple[int, int]],
        ConfigField("Mimimum target python version. Requires PEP 621."),
    ] = None
    max_py_version: Annotated[
        Optional[Tuple[int, int]],
        ConfigField("Maximum target python version. Requires PEP 621."),
    ] = None
    dependencies: Annotated[
        Optional[List[str]], ConfigField("Dependencies of project. Requires PEP 621.")
    ] = None


def _gather_config_fields(
    model: Type[Dataclass],
) -> Dict[str, ConfigField]:
    # First try PyToolConfig Annotated Fields
    result = {}
    for field in fields(model):
        description = None
        command_line = None
        universal_config = None
        type = field.type
        if get_origin(type) is Annotated:
            type = get_args(type)[0]
            annotations = [
                annotation
                for annotation in get_args(field)[1:]
                if isinstance(annotation, ConfigField)
            ]
            if len(annotations) == 1:
                annotation: ConfigField = annotations[0]
                description = annotation.description
                universal_config = annotation.universal_config
                command_line = annotation.command_line
        result[field.name] = ConfigField(
            description, universal_config, command_line, type, field.default
        )
    # Then use pydantic annotated fields
    if hasattr(model, "__pydantic_model__"):
        for pydantic_field in model.__pydantic_model__.__fields__.values():
            universal_config = None
            if "universal_config" in pydantic_field.field_info.extra:
                universal_config = pydantic_field.field_info.extra["universal_config"]
            command_line = None
            if "command_line" in pydantic_field.field_info.extra:
                command_line = pydantic_field.field_info.extra["command_line"]
            result[field.name] = ConfigField(
                pydantic_field.field_info.description,
                universal_config,
                command_line,
                pydantic_field.type_,
                pydantic_field.default,
            )
    return result
