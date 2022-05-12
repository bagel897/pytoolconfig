from pathlib import Path
from typing import Optional, Tuple

from pytoolconfig.types import UniversalConfig
from pytoolconfig.utils import min_py_version

from .ini import IniConfig


class SetupConfig(IniConfig):
    """Source for setup.cfg configuration files via ini config."""

    name: str = "setup.cfg"

    def __init__(self, working_directory: Path, base_table: str):
        super().__init__(working_directory, "setup.cfg", base_table)

    def universalconfig(self) -> UniversalConfig:
        config = UniversalConfig()
        min_py_version = self._min_py_version
        if min_py_version:
            config.min_py_version = min_py_version
        return config

    @property
    def _min_py_version(self) -> Optional[Tuple[int, int]]:
        """Return the minimum python 3 version. Will go up to interpreter version."""
        if (
            "options" not in self._config.keys()
            or "python_requires" not in self._config["options"].keys()
        ):
            return None
        raw_python_ver = self._config["options"]["python_requires"].strip('"')
        return min_py_version(raw_python_ver)
