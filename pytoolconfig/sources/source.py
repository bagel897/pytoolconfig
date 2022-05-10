from abc import ABC, abstractmethod
from typing import Dict, Optional, Tuple

from pytoolconfig.types import key


class Source(ABC):
    name: str  # The name of the tool for documentation
    description: str  # The description, written as markdown.

    @abstractmethod
    def parse(self) -> Optional[Dict[str, key]]:
        """
        Parse the file.

        Return None if tool is not configured in file.
        Otherwise, returns configuration pertaining to the tool.
        """
        pass

    @property
    def min_py_version(self) -> Optional[Tuple[int, int]]:
        """Return the minimum python version."""
        return None
