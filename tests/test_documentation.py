from typing import Optional, Tuple

from pytoolconfig import UniversalKey, dataclass, field
from pytoolconfig.documentation import _type_to_str, _write_model


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
        default=None, description="sauf", universal_config=UniversalKey.min_py_version
    )


def test_type_to_str():
    assert _type_to_str(bool) == "bool"
    assert _type_to_str(int) == "int"
    assert _type_to_str(Tuple[int, int]) == "Tuple[int, int]"


def test_documentation():
    nodes = list(_write_model(NestedModel))
    assert "description" in nodes[1]
    assert "foo_other" in nodes[3]
    assert "Tool One" in nodes[3]
    assert "no" in nodes[3]
    assert "Optional" not in nodes[3]
