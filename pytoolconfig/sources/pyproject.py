from pathlib import Path
from typing import Dict, List, Optional, Tuple

from pytoolconfig.sources.source import Source
from pytoolconfig.types import UniversalConfig, key
from pytoolconfig.utils import find_config_file, min_py_version

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib


class PyProject(Source):
    tool: str
    toml_dict: Optional[Dict] = None
    name: str = "pyproject.toml"
    file: Optional[Path]

    def __init__(
        self,
        working_directory: Path,
        tool: str,
        bases: List[str],
        global_config: bool = False,
        recursive: bool = True,
    ):
        filename: Optional[Path]
        if global_config:
            import appdirs

            self.file = Path(appdirs.user_config_dir()) / "pytool.toml"
            self.name = "pytool.toml"
        elif recursive:
            self.file = find_config_file(working_directory, "pyproject.toml", bases)
        else:
            self.file = working_directory / "pyproject.toml"
        self.tool = tool

    def _read(self) -> bool:
        if not self.file or not self.file.exists():
            return False
        self.toml_dict = tomllib.loads(self.file.read_text())
        assert self.toml_dict
        if "tool" not in self.toml_dict.keys():
            return False
        return self.tool in self.toml_dict["tool"].keys()

    def parse(self) -> Optional[Dict[str, key]]:
        if not self._read():
            return None
        assert self.toml_dict
        return self.toml_dict["tool"][self.tool]

    def universalconfig(self) -> UniversalConfig:
        if not self.toml_dict:
            return UniversalConfig()
        min_py_version = self._min_py_version
        if "pytoolconfig" in self.toml_dict["tool"].keys():
            config = UniversalConfig.parse_obj(self.toml_dict["tool"]["pytoolconfig"])
        else:
            config = UniversalConfig()
        if min_py_version:
            config.min_py_version = min_py_version
        return config

    @property
    def _min_py_version(self) -> Optional[Tuple[int, int]]:
        """Return the minimum python 3 version. Will go up to interpreter version."""
        assert self.toml_dict
        if (
            "project" not in self.toml_dict.keys()
            or "requires-python" not in self.toml_dict["project"].keys()
        ):
            return None
        raw_python_ver = self.toml_dict["project"]["requires-python"]
        return min_py_version(raw_python_ver)
