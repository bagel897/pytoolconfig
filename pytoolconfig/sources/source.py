"""Base class for defining custom sources."""
from abc import ABC, abstractmethod
from typing import Dict, Optional

from pytoolconfig.types import key
from pytoolconfig.universal_config import UniversalConfig


class Source(ABC):
    """Base class for defining custom sources."""

    name: str  # The name of the tool for documentation
    description: Optional[str]  # The description, written as markdown.

    @abstractmethod
    def _read(self) -> bool:
        """Read the file.

        If file does not exist or the tool does not exist in the file, return False.
        Can be called multiple times and overwrite the existing cached configuration.
        """

    @abstractmethod
    def parse(self) -> Optional[Dict[str, key]]:
        """
        Parse the file for each property as a nested dict.

        Return None if tool is not configured in file.
        Otherwise, returns configuration pertaining to the tool.
        """
        pass

    def universalconfig(self) -> UniversalConfig:
        """
        Parse the file for the universal config object's fields.

        Only implement the relevant fields such as minimum python version.

        Pre: file was read but tool isn't necessarily in file.
        """
        return UniversalConfig()
