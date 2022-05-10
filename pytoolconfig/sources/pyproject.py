import sys
from pathlib import Path
from typing import Dict, Optional, Tuple

from packaging.specifiers import SpecifierSet

from pytoolconfig.sources.source import Source
from pytoolconfig.types import key
from pytoolconfig.utils import find_config_file

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib


class PyProject(Source):
    tool: str
    toml_dict: Optional[Dict]
    file_exists: bool = True
    name: str = "pyproject.toml"

    def __init__(self, working_directory: Path, tool: str, global_config: bool = False):
        filename: Optional[Path]
        if global_config:
            import appdirs

            filename = Path(appdirs.user_config_dir()) / "pytool.toml"
            self.name = "pytool.toml"
        else:
            filename = find_config_file(working_directory, "pyproject.toml")
        if not filename or not filename.exists():
            self.file_exists = False
            return
        self.toml_dict = tomllib.loads(filename.read_text())
        self.tool = tool

    @property
    def exists(self) -> bool:
        if not self.file_exists:
            return False
        assert self.toml_dict
        if not "tool" in self.toml_dict.keys():
            return False
        return self.tool in self.toml_dict["tool"].keys()

    def parse(self) -> Optional[Dict[str, key]]:
        if not self.exists:
            return None
        assert self.toml_dict
        return self.toml_dict["tool"][self.tool]

    @property
    def min_py_version(self) -> Optional[Tuple[int, int]]:
        """Return the minimum python 3 version. Will go up to interpreter version."""
        if not self.exists:
            return None
        assert self.toml_dict
        if (
            "project" not in self.toml_dict.keys()
            or "requires-python" not in self.toml_dict["project"].keys()
        ):
            return None
        raw_python_ver = self.toml_dict["project"]["requires-python"]
        parsed = SpecifierSet(raw_python_ver)
        for i in range(0, sys.version_info.minor ):
            if parsed.contains(f"3.{i}"):
                return (3, i)
        return (3, sys.version_info.minor)
