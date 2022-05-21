"""Abstractions over dataclass fields."""
import dataclasses
from dataclasses import fields
from typing import Any, Callable, Dict, Optional, Tuple, Type

from .types import ConfigField, Dataclass

_metadata_key = "pytoolconfig"


def field(
    default: Any = None,
    description: Optional[str] = None,
    command_line: Optional[Tuple[str]] = None,
    universal_config: Optional[str] = None,
    default_factory: Optional[Callable] = None,
) -> dataclasses.Field:
    """Create a dataclass field with metadata."""
    metadata = {
        _metadata_key: ConfigField(
            description=description,
            universal_config=universal_config,
            command_line=command_line,
            _default=default,
        )
    }

    if default_factory:
        metadata[_metadata_key]._default = default_factory()
        return dataclasses.field(default_factory=default_factory, metadata=metadata)
    return dataclasses.field(default=default, metadata=metadata)


def _gather_config_fields(
    model: Type[Dataclass],
) -> Dict[str, ConfigField]:
    # First try PyToolConfig Annotated Fields
    result = {}
    for field in fields(model):
        if _metadata_key in field.metadata:
            result[field.name] = field.metadata[_metadata_key]
        else:
            result[field.name] = ConfigField(_default=field.default)
        result[field.name]._type = field.type
    # Then use pydantic annotated fields
    if hasattr(model, "__pydantic_model__"):
        for pydantic_field in model.__pydantic_model__.__fields__.values():
            result[field.name] = ConfigField(
                description=pydantic_field.field_info.description,
                _type=pydantic_field.type_,
                _default=pydantic_field.default,
            )
            if "universal_config" in pydantic_field.field_info.extra:
                result[field.name].universal_config = pydantic_field.field_info.extra[
                    "universal_config"
                ]
            if "command_line" in pydantic_field.field_info.extra:
                result[field.name].command_line = pydantic_field.field_info.extra[
                    "command_line"
                ]
    return result
