from configparser import ConfigParser
from pathlib import Path
from typing import Dict, Optional

from pytoolconfig.sources.source import Source
from pytoolconfig.types import key
from pytoolconfig.utils import find_config_file


class IniConfig(Source):
    """Source for INI configuration files via configparser."""

    def __init__(self, working_directory: Path, filename: str, base_table: str):
        self.file = find_config_file(working_directory, filename)
        self.base_table = base_table

    def parse(self) -> Optional[Dict[str, key]]:
        if self.file is None:
            return None
        config = ConfigParser()
        config.read_string(self.file.read_text())
        output: Dict[str, key] = {}
        for table in config:
            split = table.split(".")
            if len(split) == 1 and split[0] == self.base_table:
                for table_key in config[table]:
                    output[table_key] = config[table][table_key]
            print(table)
        return output
