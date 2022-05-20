"""Utility functions and classes."""
import sys
from dataclasses import fields
from pathlib import Path
from typing import List, Mapping, Optional, Tuple, Type

from packaging.specifiers import SpecifierSet

from .types import Dataclass, key


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


def _is_dataclass(field_type) -> bool:
    return hasattr(field_type, "__dataclass_params__")


def _dict_to_dataclass(dataclass: Type[Dataclass], dictionary: Mapping[str, key]):
    field_set = set()
    filtered_arg_dict = {}
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
