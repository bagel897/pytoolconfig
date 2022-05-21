from typing import Optional, Tuple

from pytoolconfig import dataclass, field
from pytoolconfig.documentation import _write_model


@dataclass
class SubTool:
    foo: str = field(description="foobar", default="lo")


@dataclass
class NestedModel:
    subtool: SubTool = SubTool()
    foo_other: Optional[str] = field(
        description="Tool One", default="no", command_line=("--foo", "-f")
    )
    min_py_ver: Tuple[int, int] = field(
        default=None, description="sauf", universal_config="min_py_version"
    )


def test_documentation():
    nodes = list(_write_model(NestedModel))
    assert "description" in nodes[1]
    assert "foo_other" in nodes[3]
    assert "Tool One" in nodes[3]
    assert "no" in nodes[3]
    assert "Optional" not in nodes[3]
