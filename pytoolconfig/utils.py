"""Utility functions and classes."""
import sys
from dataclasses import fields
from pathlib import Path
from typing import (
    Any,
    Callable,
    Dict,
    Generator,
    List,
    Mapping,
    Optional,
    Tuple,
    TypeVar,
)

from packaging.requirements import Requirement
from packaging.specifiers import SpecifierSet

from .types import Dataclass, Key, _is_dataclass


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
    """Return the minimum python 3 version. Between 3.4 and interpreter version."""
    parsed = SpecifierSet(specifier)
    for i in range(4, sys.version_info.minor):
        if parsed.contains(f"3.{i}"):
            return (3, i)
    return (3, sys.version_info.minor)


def max_py_version(specifier: str) -> Tuple[int, int]:
    """Return the maximum python 3 version. Between 3.4 and interpreter version."""
    parsed = SpecifierSet(specifier)
    for i in range(sys.version_info.minor, 4, -1):
        if parsed.contains(f"3.{i}"):
            return (3, i)
    return (3, 4)  # Please don't cap your project at python3.4


def parse_dependencies(dependencies: List[str]) -> Generator[Requirement, None, None]:
    """Parse the dependencies from TOML using packaging."""
    for dependency in dependencies:
        yield Requirement(dependency)


T = TypeVar("T", bound="Dataclass")


def _dict_to_dataclass(dataclass: Callable[..., T], dictionary: Mapping[str, Key]) -> T:
    field_set = set()
    filtered_arg_dict: Dict[str, Any] = {}
    sub_tables = {}
    for field in fields(dataclass):
        if field.init:
            if _is_dataclass(field.type):
                sub_tables[field.name] = field.type
            else:
                field_set.add(field.name)
    for key_name, value in dictionary.items():
        if key_name in field_set:
            filtered_arg_dict[key_name] = value
        elif key_name in sub_tables:
            sub_table = sub_tables[key_name]
            assert isinstance(value, Mapping)
            filtered_arg_dict[key_name] = _dict_to_dataclass(sub_table, value)
    return dataclass(**filtered_arg_dict)
