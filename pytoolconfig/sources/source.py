from abc import ABC, abstractmethod
from typing import Dict, Optional

from pytoolconfig.types import key


class Source(ABC):
    @abstractmethod
    def parse(self) -> Optional[Dict[str, key]]:
        pass
