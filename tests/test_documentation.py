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

    test_truth: bool = False


def test_type_to_str():
    assert _type_to_str(bool) == "bool"
    assert _type_to_str(int) == "int"
    assert _type_to_str(Tuple[int, int]) == "Tuple[int, int]"


def test_documentation():
    lines = list(_write_model(NestedModel))
    assert "description" in lines[1]
    assert "foo_other" in lines[3]
    assert "Tool One" in lines[3]
    assert "no" in lines[3]
    assert "Optional" in lines[3]
    assert "bool" in lines[5]
