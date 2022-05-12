from configparser import ConfigParser, SectionProxy
from pathlib import Path
from typing import Dict, List, Optional

from pytoolconfig.sources.source import Source
from pytoolconfig.types import key
from pytoolconfig.utils import find_config_file


def _add_split_to_dict(dest: Dict, table_to_add: List[str], table: SectionProxy):
    if len(table_to_add) == 0:
        for table_key in table:
            dest[table_key] = table[table_key]
    else:
        first = table_to_add[0]
        dest.setdefault(first, {})
        assert isinstance(dest[first], Dict)
        _add_split_to_dict(dest[first], table_to_add[1:], table)


class IniConfig(Source):
    """Source for INI configuration files via configparser."""

    _config: ConfigParser

    def __init__(self, working_directory: Path, filename: str, base_table: str):
        self.file = find_config_file(working_directory, filename)
        self.base_table = base_table
        self.name = filename
        self._config = ConfigParser()

    def _read(self) -> bool:
        if self.file is None:
            return False
        self._config.read_string(self.file.read_text())
        for table in self._config:
            split = table.split(".")
            if split[0] == self.base_table:
                return True
        return False

    def parse(self) -> Optional[Dict[str, key]]:
        if not self._read():
            return None
        output: Dict[str, key] = {}
        for table in self._config:
            split = table.split(".")
            if split[0] == self.base_table:
                _add_split_to_dict(output, split[1:], self._config[table])
        return output
