"""Abstractions over dataclass fields."""
from __future__ import annotations

import dataclasses
from dataclasses import fields
from typing import TYPE_CHECKING, Callable, TypeVar, overload

from .types import ConfigField, UniversalKey

if TYPE_CHECKING:
    from _typeshed import DataclassInstance
_METADATA_KEY = "pytoolconfig"

T = TypeVar("T")


@overload
def field(  # noqa: PLR0913
    default: T,
    description: str | None = None,
    command_line: tuple[str] | None = None,
    universal_config: UniversalKey | None = None,
    default_factory: None = None,
    init: bool = True,
) -> T:
    pass


@overload
def field(
    *,
    default_factory: Callable[[], T],
    description: str | None = None,
    command_line: tuple[str] | None = None,
    universal_config: UniversalKey | None = None,
    init: bool = True,
) -> T:
    pass


def field(  # noqa: PLR0913
    default: T | None = None,
    description: str | None = None,
    command_line: tuple[str] | None = None,
    universal_config: UniversalKey | None = None,
    default_factory: Callable[[], T] | None = None,
    init: bool = True,
) -> T:
    """Create a dataclass field with metadata."""
    metadata = {
        _METADATA_KEY: ConfigField(
            description=description,
            universal_config=universal_config,
            command_line=command_line,
            _default=default,
        ),
    }

    if default_factory is not None:
        metadata[_METADATA_KEY]._default = default_factory()
        return dataclasses.field(
            default_factory=default_factory,
            metadata=metadata,
            init=init,
        )
    assert default is not None
    return dataclasses.field(default=default, metadata=metadata, init=init)


def _gather_config_fields(
    model: type[DataclassInstance] | DataclassInstance,
) -> dict[str, ConfigField]:
    # First try PyToolConfig Annotated Fields
    result = {}
    for dataclass_field in fields(model):
        if dataclass_field.init:
            if _METADATA_KEY in dataclass_field.metadata:
                result[dataclass_field.name] = dataclass_field.metadata[_METADATA_KEY]
            else:
                result[dataclass_field.name] = ConfigField(
                    _default=dataclass_field.default,
                )
            result[dataclass_field.name]._type = dataclass_field.type
    # Then use pydantic annotated fields
    if hasattr(model, "__pydantic_model__"):
        for pydantic_field in model.__pydantic_model__.__fields__.values():
            if pydantic_field.init:
                result[pydantic_field.name] = ConfigField(
                    description=pydantic_field.field_info.description,
                    _type=pydantic_field.type_,
                    _default=pydantic_field.default,
                )
                if "universal_config" in pydantic_field.field_info.extra:
                    result[
                        pydantic_field.name
                    ].universal_config = pydantic_field.field_info.extra[
                        "universal_config"
                    ]
                if "command_line" in pydantic_field.field_info.extra:
                    result[
                        pydantic_field.name
                    ].command_line = pydantic_field.field_info.extra["command_line"]
    return result
