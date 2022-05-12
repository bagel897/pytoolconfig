import os
import sys
from argparse import ArgumentParser
from typing import Tuple

import pytest
from pydantic import BaseModel, Field

from pytoolconfig import PyToolConfig
from pytoolconfig.sources import IniConfig


class SimpleModel(BaseModel):
    formatter: str


class EmptyModel(BaseModel):
    pass


class SubTool(BaseModel):
    foo: str = Field(description="foobar", default="lo")


class NestedModel(BaseModel):
    subtool: SubTool = SubTool()
    foo_other: str = Field(description="w", default="no", command_line=("--foo", "-f"))

    target: Tuple[int, int] = Field(
        description="Minimum python version",
        default=(3, 1),
        universal_config="min_py_version",
    )


def test_simple(cwd):
    config = PyToolConfig("pytoolconfig", cwd, SimpleModel)
    result = config.parse()
    assert result.formatter == "black"


def test_invalid_key(cwd):
    config = PyToolConfig("pytoolconfig", cwd, EmptyModel)
    result = config.parse()
    with pytest.raises(AttributeError):
        assert result.formatter


def test_nested(cwd):
    config = PyToolConfig(
        "bogus",
        cwd,
        NestedModel,
        custom_sources=[IniConfig(cwd, "test_config.ini", "bogus")],
    )
    result = config.parse()
    assert result.subtool.foo == "barr"
    config = PyToolConfig(
        "bogus",
        cwd,
        NestedModel,
    )
    result = config.parse()
    # Default argument
    assert result.subtool.foo == "lo"
    assert result.target == (3, 7)


def test_cli(cwd):
    config = PyToolConfig("bogus", cwd, NestedModel, arg_parser=ArgumentParser())
    result = config.parse()
    assert result.subtool.foo == "lo"
    result = config.parse(["--foo", "bar"])
    assert result.foo_other == "bar"


def test_global(cwd):
    if sys.platform != "linux":
        pytest.skip()
    os.environ["XDG_CONFIG_HOME"] = cwd.as_posix()
    config = PyToolConfig("bogus", cwd, NestedModel, global_config=True)
    result = config.parse()
    assert result.subtool.foo == "ajf"
