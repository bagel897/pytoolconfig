from pathlib import Path
from typing import Dict, Optional

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

    def __init__(self, working_directory: Path, tool: str, global_config: bool = False):
        filename = find_config_file(working_directory, "pyproject.toml")
        if not filename:
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
