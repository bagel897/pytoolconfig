from abc import ABCMeta, abstractmethod, abstractproperty
from pathlib import Path
from typing import List, Optional


class Source(ABCMeta):
    @abstractmethod
    def __init__(self, filename: Path, tool: str):
        pass

    @abstractproperty
    def exists(self) -> bool:
        pass

    @abstractmethod
    def is_present(self, table: Optional[str] = None) -> bool:
        pass

    @abstractmethod
    def get_key(self, key: str, table: Optional[str] = None) -> str:
        pass

    @staticmethod
    @abstractmethod
    def get_filenames(self, tool: str) -> List[str]:
        pass
