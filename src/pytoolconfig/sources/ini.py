"""Source for INI configuration files via configparser."""

from __future__ import annotations

from configparser import ConfigParser, SectionProxy
from pathlib import Path

from pytoolconfig.sources.source import Source
from pytoolconfig.types import JSON_DICT
from pytoolconfig.utils import assert_mapping, find_config_file


def _add_split_to_dict(
    dest: JSON_DICT,
    table_to_add: list[str],
    table: SectionProxy,
) -> None:
    if len(table_to_add) == 0:
        for table_key in table:
            dest[table_key] = table[table_key]
    else:
        first = table_to_add[0]
        dest.setdefault(first, {})
        to_add = dest[first]
        if assert_mapping(to_add):
            _add_split_to_dict(to_add, table_to_add[1:], table)


class IniConfig(Source):
    """Source for INI configuration files via configparser."""

    _config: ConfigParser
    name: str
    description: str | None

    def __init__(
        self,
        working_directory: Path,
        filename: str,
        base_table: str,
        description: str | None = None,
    ) -> None:
        """Initialize the Ini Configuration.

        :param working_directory: the working directory to search.
        :param filename: the filename to search for.
        :param base_table: The table to search for.
            The file will only be used if this is present.
            The base_table will not be included in the parsed output.
        :param description: The description used in documentation.
        """
        self.file = find_config_file(working_directory, filename)
        self.base_table = base_table
        self.name = filename
        self.description = description
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

    def parse(self) -> JSON_DICT | None:
        """Parse the INI file."""
        if not self._read():
            return None
        output: JSON_DICT = {}
        for table in self._config:
            split = table.split(".")
            if split[0] == self.base_table:
                _add_split_to_dict(output, split[1:], self._config[table])
        return output
