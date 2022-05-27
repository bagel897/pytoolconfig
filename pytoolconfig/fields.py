"""Abstractions over dataclass fields."""
from __future__ import annotations

import dataclasses
from dataclasses import fields
from typing import Any, Callable, Dict, Optional, Tuple, Type, Union

from .types import ConfigField, Dataclass, UniversalKey

_METADATA_KEY = "pytoolconfig"


def field(
    default: Any = None,
    description: Optional[str] = None,
    command_line: Optional[Tuple[str]] = None,
    universal_config: Optional[UniversalKey] = None,
    default_factory: Optional[Callable[[], Any]] = None,
    init: bool = True,
) -> dataclasses.Field:
    """Create a dataclass field with metadata."""
    metadata = {
        _METADATA_KEY: ConfigField(
            description=description,
            universal_config=universal_config,
            command_line=command_line,
            _default=default,
        )
    }

    if default_factory:
        metadata[_METADATA_KEY]._default = default_factory()
        return dataclasses.field(
            default_factory=default_factory, metadata=metadata, init=init
        )
    return dataclasses.field(default=default, metadata=metadata, init=init)


def _gather_config_fields(
    model: Union[Type[Dataclass], Dataclass],
) -> Dict[str, ConfigField]:
    # First try PyToolConfig Annotated Fields
    result = {}
    for dataclass_field in fields(model):
        if _METADATA_KEY in dataclass_field.metadata:
            result[dataclass_field.name] = dataclass_field.metadata[_METADATA_KEY]
        else:
            result[dataclass_field.name] = ConfigField(_default=dataclass_field.default)
        result[dataclass_field.name]._type = dataclass_field.type
    # Then use pydantic annotated fields
    if hasattr(model, "__pydantic_model__"):
        for pydantic_field in model.__pydantic_model__.__fields__.values():
            result[pydantic_field.name] = ConfigField(
                description=pydantic_field.field_info.description,
                _type=pydantic_field.type_,
                _default=pydantic_field.default,
            )
            if "universal_config" in pydantic_field.field_info.extra:
                result[
                    pydantic_field.name
                ].universal_config = pydantic_field.field_info.extra["universal_config"]
            if "command_line" in pydantic_field.field_info.extra:
                result[
                    pydantic_field.name
                ].command_line = pydantic_field.field_info.extra["command_line"]
    return result
