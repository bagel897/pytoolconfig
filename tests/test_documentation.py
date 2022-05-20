from argparse import ArgumentParser
from typing import Tuple

from pytoolconfig import PyToolConfig, dataclass, field
from pytoolconfig.documentation import generate_documentation
from pytoolconfig.sources import IniConfig


@dataclass
class SubTool:
    foo: str = field(description="foobar", default="lo")


@dataclass
class NestedModel:
    subtool: SubTool = SubTool()
    foo_other: str = field(
        description="Tool One", default="no", command_line=("--foo", "-f")
    )
    min_py_ver: Tuple[int, int] = field(
        default=None, description="sauf", universal_config="min_py_version"
    )


def test_documentation(cwd):
    config = PyToolConfig("pytoolconfig", cwd, NestedModel)
    generate_documentation(config, cwd / "test_documentation.md")
    config = PyToolConfig(
        "pytoolconfig",
        cwd,
        NestedModel,
        custom_sources=[IniConfig(cwd, "setup.cfg", "pytoolconfig")],
        arg_parser=ArgumentParser(),
        global_config=True,
    )
    generate_documentation(config, cwd / "test_documentation_ini.md")
