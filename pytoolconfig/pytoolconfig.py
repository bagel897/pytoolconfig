from pathlib import Path
from typing import List

from pytoolconfig.sources.pyproject import PyProject
from pytoolconfig.sources.source import Source
from pytoolconfig.utils import ConfigKey


class PyToolConfig:
    sources: List[Source] = []
    global_sources: List[Source] = []
    tool: str
    working_directory: Path
    keys: List[ConfigKey]

    def __init__(self, tool: str, working_directory: Path, command_line: bool = False):
        self.sources = [PyProject(working_directory, tool)]
        self.command_line = command_line

    def add_source(self, source: Source):
        self.sources.append(source)


    def parse(self):
        if self.command_line:
            cli = something
        local = self._parse_sources()
        global_config = self._parse_global_sources()
        return local
    
    def _parse_sources(self):
        configuration = None
        for source in self.sources:
            if source.exists:
                configuration = source.parse()
                break
        return configuration

    def _parse_global_sources(self):
        pass
