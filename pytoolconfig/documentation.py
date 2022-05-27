"""Program to generate documentation for a given PyToolConfig object."""


import sys
from typing import Any, Dict, Generator, Optional, Type

if sys.version_info < (3, 8, 0):
    from typing_extensions import get_origin
else:
    from typing import get_origin

from docutils.statemachine import StringList
from sphinx.application import Sphinx
from sphinx.ext.autodoc import ClassDocumenter
from tabulate import tabulate

from .fields import _gather_config_fields
from .types import ConfigField, Dataclass, _is_dataclass
from .universal_config import UniversalConfig


def _type_to_str(type_to_print: Type[Any]) -> Optional[str]:
    if type_to_print is None:
        return None
    if get_origin(type_to_print) is None:
        return type_to_print.__name__
    return str(type_to_print).replace("typing.", "")


def _write_model(
    model: Dataclass,
) -> Generator[str, None, None]:
    header = ["name", "description", "type", "default"]
    model_fields: Dict[str, ConfigField] = _gather_config_fields(model)
    command_line = any(field.command_line for field in model_fields.values())
    if command_line:
        header.append("command line flag")
    extra = []
    table = []
    for name, field in model_fields.items():
        if _is_dataclass(field._type):
            extra.append((field._type, f"{name}.{name}"))
        else:
            row = [
                f"{name}",
                field.description.replace("\n", " ") if field.description else None,
                _type_to_str(field._type),
                field._default,
            ]
            if field.universal_config:
                key = field.universal_config
                assert _is_dataclass(UniversalConfig)
                universal_key = _gather_config_fields(UniversalConfig)[key.name]
                row[1] = universal_key.description
                row[3] = universal_key._default
            if command_line:
                cli_doc = field.command_line
                if cli_doc is not None:
                    row.append(", ".join(cli_doc))
                else:
                    row.append(None)
            table.append(row)
    yield from tabulate(table, tablefmt="rst", headers=header).split("\n")


class PyToolConfigAutoDocumenter(ClassDocumenter):
    """Sphinx autodocumenter for pytoolconfig models."""

    objtype = "pytoolconfigtable"
    content_indent = ""
    titles_allowed = True

    @classmethod
    def can_document_member(
        cls, member: Any, membername: str, isattr: bool, parent: Any
    ) -> bool:
        """Check if member is dataclass."""
        return _is_dataclass(member)

    def add_directive_header(self, sig: str) -> None:
        """Remove directive headers."""

    def add_content(
        self, more_content: Optional[StringList], no_docstring: bool = False
    ) -> None:
        """Create simple table to document configuration options."""
        source = self.get_sourcename()
        config = self.object
        for line in _write_model(config):
            self.add_line(line, source)


def setup(app: Sphinx) -> None:
    """Register automatic documenter."""
    app.setup_extension("sphinx.ext.autodoc")
    app.add_autodocumenter(PyToolConfigAutoDocumenter)
