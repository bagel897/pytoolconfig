"""Utility functions and classes."""
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Type, Union


@dataclass
class ConfigKey:
    name: str
    value: Optional[Union[str, int, List[str]]]
    description: str
    type: Type


def find_config_file(
    working_directory: Path, filename: str, bases: List[str] = [".git", ".hg"]
) -> Optional[Path]:
    """Recursively find the configuration file."""
    target = working_directory / filename
    if target.exists():
        return target
    for base in bases:
        if (working_directory / base).exists():
            return None
    if working_directory == working_directory.anchor:
        return None
    return find_config_file(working_directory.parent, filename, bases)
