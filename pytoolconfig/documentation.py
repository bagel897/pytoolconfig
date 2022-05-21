"""
Program to generate documentation for a given PyToolConfig object.
"""

from types import NoneType
from typing import Any, Generator, Optional, get_args

from docutils.statemachine import StringList
from sphinx.application import Sphinx
from sphinx.ext.autodoc import ClassDocumenter
from tabulate import tabulate

from .fields import _gather_config_fields
from .types import Dataclass
from .universal_config import UniversalConfig
from .utils import _is_dataclass


def _write_model(
    model: Dataclass,
) -> Generator[str, None, None]:
    header = ["name", "description", "type", "default"]
    model_fields = _gather_config_fields(model)
    universal_config = any(field.universal_config for field in model_fields.values())
    command_line = any(field.command_line for field in model_fields.values())
    if universal_config:
        header.append("universal key")
    if command_line:
        header.append("command line flag")
    extra = []
    table = []
    for name, field in model_fields.items():
        if _is_dataclass(field._type):
            extra.append((field._type, f"{name}.{name}"))
        else:
            type = field._type
            if type is not None:
                type = ",".join(
                    type.__name__ for type in get_args(type) if type is not NoneType
                )

            row = [
                f"{name}",
                field.description.replace("\n", " ") if field.description else None,
                type,
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
            table.append(row)
    for line in tabulate(table, tablefmt="rst", headers=header).split("\n"):
        yield line


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
