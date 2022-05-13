"""Utility functions and classes."""
import sys
from pathlib import Path
from typing import List, Optional, Tuple

from packaging.specifiers import SpecifierSet


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
    if working_directory == working_directory.parent:
        return None
    return find_config_file(working_directory.parent, filename, bases)


def min_py_version(specifier: str) -> Tuple[int, int]:
    """Return the minimum python 3 version. Will go up to interpreter version."""
    parsed = SpecifierSet(specifier)
    for i in range(0, sys.version_info.minor):
        if parsed.contains(f"3.{i}"):
            return (3, i)
    return (3, sys.version_info.minor)
