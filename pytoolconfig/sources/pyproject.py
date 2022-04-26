from pathlib import Path
from typing import Dict

from pytoolconfig.sources.source import Source

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib


def PyProject(Source):
    tool: str
    toml_dict: Dict

    def __init__(self, filename: Path, tool: str):
        self.toml_dict = tomllib.load(filename.read_bytes())
        self.tool = tool

    @property
    def exists(self) -> bool:
        return self.tool in self.toml_dict.keys()

