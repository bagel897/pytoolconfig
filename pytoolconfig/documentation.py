"""
Program to generate documentation for a given PyToolConfig object.
"""

from io import TextIOBase
from pathlib import Path
from typing import Dict, List, Tuple, Type

from pydantic.main import ModelMetaclass
from tabulate import tabulate

from .pytoolconfig import PyToolConfig
from .types import ConfigField, Dataclass, UniversalConfig, _gather_config_fields


def write_model(
    model_fields: Dict[str, ConfigField],
    file: TextIOBase,
    name: str,
    universal_config: bool = False,
    command_line: bool = False,
) -> List[Tuple[Type[Dataclass], str]]:
    file.writelines(f"## {name}\n")
    header = ["name", "description", "type", "default"]

    if universal_config:
        header.append("universal key")
    if command_line:
        header.append("command line flag")

    data = []
    extra = []
    for name, field in model_fields.items():
        if isinstance(field._type, ModelMetaclass):
            extra.append((field._type, f"{name}.{name}"))
        else:
            row = [
                f"{name}.{name}",
                field.description.replace("\n", " ") if field.description else None,
                field._type.__name__,
                field._default,
            ]
            if universal_config:
                key_doc = None
                if field.universal_config:
                    key = field.universal_config
                    universal_key = _gather_config_fields(UniversalConfig)[key]
                    row[1] = "This field is set via an universal key."
                    row[3] = universal_key._default
                    key_doc = universal_key.description
                row.append(key_doc)
            if command_line:
                cli_doc = field.command_line
                if isinstance(cli_doc, tuple):
                    key_doc = ", ".join(cli_doc)
                row.append(cli_doc)
            data.append(row)
    file.writelines(tabulate(data, tablefmt="github", headers=header))
    file.write("\n")
    return extra


def generate_documentation(config: PyToolConfig, file: Path):
    """
    Generate documentation for the given configuration.

    :param config: PyToolConfig Configuration Object
    :param file: Path Path to write to.
    """
    assert (
        len(config._config_fields) > 0
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
        universal_config = any(
            field.universal_config for field in config._config_fields.values()
        )
        command_line = config.arg_parser is not None
        for model, name in write_model(
            config._config_fields, f, config.tool, universal_config, command_line
        ):
            write_model(_gather_config_fields(model), f, name, False, False)
