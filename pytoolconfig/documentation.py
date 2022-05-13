"""
Program to generate documentation for a given PyToolConfig object.
"""

from io import TextIOBase
from pathlib import Path
from typing import List, Tuple, Type

from pydantic import BaseModel
from pydantic.main import ModelMetaclass
from tabulate import tabulate

from .pytoolconfig import PyToolConfig
from .types import UniversalConfig


def write_model(
    model: Type[BaseModel],
    file: TextIOBase,
    name: str,
    universal_config: bool = False,
    command_line: bool = False,
) -> List[Tuple[Type[BaseModel], str]]:
    file.writelines(f"## {name}\n")
    header = ["name", "description", "type", "default"]

    if universal_config:
        header.append("universal key")
    if command_line:
        header.append("command line flag")

    data = []
    extra = []
    for field in model.__fields__.values():
        if isinstance(field.type_, ModelMetaclass):
            extra.append((field.type_, f"{name}.{field.name}"))
        else:
            row = [
                f"{name}.{field.name}",
                field.field_info.description.replace("\n", " ")
                if field.field_info.description
                else None,
                field.type_.__name__,
                field.default,
            ]
            if universal_config:
                key_doc = None
                if "universal_config" in field.field_info.extra:
                    key = field.field_info.extra["universal_config"]
                    universal_key = UniversalConfig.__fields__[key]
                    row[1] = "This field is set via an universal key."
                    assert row[2] == universal_key.type_.__name__
                    row[3] = universal_key.default
                    key_doc = universal_key.field_info.description
                row.append(key_doc)
            if command_line:
                key_doc = None
                if "command_line" in field.field_info.extra:
                    key_doc = field.field_info.extra["command_line"]
                    if isinstance(key_doc, tuple):
                        key_doc = ", ".join(key_doc)
                row.append(key_doc)
            data.append(row)
    file.writelines(tabulate(data, tablefmt="github", headers=header))
    file.write("\n")
    return extra


def generate_documentation(config: PyToolConfig, file: Path):
    assert (
        len(config.model.__fields__) > 0
    )  # There must be at least one entry for configuration
    with file.open("w") as f:
        f.write("# Configuration\n")
        if len(config.sources) == 1:
            f.write(f"{config.tool} supports the pyproject.toml configuration file\n")
        else:
            f.write(f"{config.tool} supports the following configuration files\n")
            for idx, source in enumerate(config.sources):
                f.write(f" {idx + 1}. {source.name}  \n")
            f.write("\n")
        universal_config = len(list(config._fields_with_param("universal_config"))) > 0
        command_line = config.arg_parser is not None
        for model, name in write_model(
            config.model, f, config.tool, universal_config, command_line
        ):
            write_model(model, f, name, False, False)
