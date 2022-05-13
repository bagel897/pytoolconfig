from argparse import ArgumentParser

from pydantic import BaseModel, Field

from pytoolconfig import PyToolConfig
from pytoolconfig.documentation import generate_documentation
from pytoolconfig.sources import IniConfig
from typing import Tuple


class SubTool(BaseModel):
    foo: str = Field(description="foobar", default="lo")


class NestedModel(BaseModel):
    subtool: SubTool = SubTool()
    foo_other: str = Field(
        description="Tool One", default="no", command_line=("--foo", "-f")
    )
    min_py_ver: Tuple[int, int] = Field(
        description="sauf", universal_config="min_py_version"
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
