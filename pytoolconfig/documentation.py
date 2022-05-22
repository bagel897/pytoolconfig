"""
Program to generate documentation for a given PyToolConfig object.
"""

from types import NoneType
from typing import Any, Generator, Optional, Type, get_args, get_origin

from docutils.statemachine import StringList
from sphinx.application import Sphinx
from sphinx.ext.autodoc import ClassDocumenter
from tabulate import tabulate

from .fields import _gather_config_fields
from .types import Dataclass
from .universal_config import UniversalConfig
from .utils import _is_dataclass


def _type_to_str(type: Type) -> Optional[str]:
    if type is None:
        return None
    if get_origin(type) is None:
        return type.__name__
    else:
        return str(type).replace("typing.", "")


def _write_model(
    model: Dataclass,
) -> Generator[str, None, None]:
    header = ["name", "description", "type", "default"]
    model_fields = _gather_config_fields(model)
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
                universal_key = _gather_config_fields(UniversalConfig)[key.name]
                row[1] = universal_key.description
                row[3] = universal_key._default
            if command_line:
                cli_doc = field.command_line
                if isinstance(cli_doc, tuple):
                    key_doc = ", ".join(cli_doc)
                row.append(cli_doc)
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
        pass

    def add_content(
        self, more_content: Optional[StringList], no_docstring: bool = False
    ):
        """Create simple table to document configuration options."""
        source = self.get_sourcename()
        config = self.object
        for line in _write_model(config):
            self.add_line(line, source)


def setup(app: Sphinx):
    """Register automatic documenter."""
    app.setup_extension("sphinx.ext.autodoc")
    app.add_autodocumenter(PyToolConfigAutoDocumenter)
