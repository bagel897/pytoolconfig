"""Source for pyproject.toml files or more generally toml files."""
from pathlib import Path
from typing import Dict, List, Optional

from pytoolconfig.sources.source import Source
from pytoolconfig.types import key
from pytoolconfig.universal_config import UniversalConfig
from pytoolconfig.utils import (
    _dict_to_dataclass,
    find_config_file,
    max_py_version,
    min_py_version,
    parse_dependencies,
)

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib


class PyProject(Source):
    """
    Source for pyproject.toml and pytool.toml files.

    Can be extended to other toml files.
    """

    tool: str
    toml_dict: Optional[Dict] = None
    name: str = "pyproject.toml"
    description: str = """
    PEP 518 defines pyproject.toml as a configuration file to store build system requirements for Python projects. With the help of tools like Poetry or Flit it can fully replace the need for setup.py and setup.cfg files.
    """  # taken from black.
    file: Optional[Path]

    def __init__(
        self,
        working_directory: Path,
        tool: str,
        bases: List[str],
        global_config: bool = False,
        recursive: bool = True,
    ):
        """
        :param working_directory: Working Directory
        :param tool: name of your tool. Will read configuration from [tool.yourtool]
        :param bases: Base files/folders to look for (besides pyproject.toml)
        :param global_config: use the global pytool.toml file instead
        :param recursive: search recursively up the directory tree for the file.
        """
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
        if "pytoolconfig" in self.toml_dict["tool"].keys():
            config = _dict_to_dataclass(
                UniversalConfig, self.toml_dict["tool"]["pytoolconfig"]
            )
        else:
            config = UniversalConfig()
        if "project" in self.toml_dict.keys():
            if "requires-python" in self.toml_dict["project"].keys():
                raw_python_ver = self.toml_dict["project"]["requires-python"]
                config.min_py_version = min_py_version(raw_python_ver)
                config.max_py_version = max_py_version(raw_python_ver)
            if "dependencies" in self.toml_dict["project"]:
                dependencies = parse_dependencies(
                    self.toml_dict["project"]["dependencies"]
                )
                config.dependencies = dependencies
            if "optional-dependencies" in self.toml_dict["project"]:
                optional_deps = {}
                for group, deps in self.toml_dict["project"][
                    "optional-dependencies"
                ].items():
                    optional_deps[group] = parse_dependencies(deps)
                config.optional_dependencies = optional_deps
        return config
