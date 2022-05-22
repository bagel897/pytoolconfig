"""Version of pytoolconfig."""
from pathlib import Path

from pytoolconfig import PyToolConfig, UniversalKey, dataclass, field


@dataclass
class Version:
    version: str = field("UNKNOWN", universal_config=UniversalKey.version)


config = PyToolConfig("pytoolconfig", Path(__file__).parent, model=Version).parse()
version = config.version
