"""Tool to configure Python tools."""
import sys
from argparse import SUPPRESS, ArgumentParser
from pathlib import Path
from typing import Dict, Generator, List, Optional, Tuple, Type

from pydantic import BaseModel
from pydantic.fields import ModelField

from pytoolconfig.sources.pyproject import PyProject
from pytoolconfig.sources.source import Source
from pytoolconfig.types import UniversalConfig, key


def _add_args(arg_parser, model):
    for field in model.__fields__.values():
        if isinstance(field.type_, BaseModel):
            _add_args(arg_parser, field)


class PyToolConfig:
    """Python Tool Configuration Aggregator."""

    sources: List[Source] = []
    tool: str
    working_directory: Path
    model: Type[BaseModel]
    arg_parser: Optional[ArgumentParser] = None

    def __init__(
        self,
        tool: str,
        working_directory: Path,
        model: Type[BaseModel],
        arg_parser: Optional[ArgumentParser] = None,
        custom_sources: List[Source] = [],
        global_config: bool = False,
        global_sources: List[Source] = [],
        universalconfig: bool = False,
        bases: List[str] = [".git", ".hg"],
        recursive: bool = True,
    ):
        """
        Initialize the configuration object.

        tool: name of the tool to use.
        working_directory: Path to working directory in use.
        model: Model of configuration.
        arg_parser: Arugument Parser.
        custom_sources: custom sources
        global_config: enable global configuration
        global_sources: custom global sources
        bases: custom bases
        """
        self.model = model
        self.tool = tool
        self.sources = [PyProject(working_directory, tool, bases, recursive=recursive)]
        self.sources.extend(custom_sources)
        if global_config:
            self.sources.append(
                PyProject(
                    working_directory, tool, bases, global_config=True, recursive=False
                )
            )
        self.sources.extend(global_sources)

        if arg_parser:
            self.arg_parser = arg_parser
            self._setup_arg_parser()

    def parse(self, args: List[str] = []) -> BaseModel:
        """
        Parse the configuration.

        args: any additional command line overwritesself.
        """
        raw_config, universal = self._parse_sources()
        if raw_config:
            configuration = self.model.parse_obj(raw_config)
        else:
            configuration = self.model()
        if self.arg_parser:
            parsed = self.arg_parser.parse_args(args)
            for field in self._fields_with_param("command_line"):
                if field.name in parsed:
                    setattr(configuration, field.name, vars(parsed)[field.name])
        for field in self._fields_with_param("universal_config"):
            if field.field_info.extra["universal_config"] in universal.__fields__:
                setattr(
                    configuration,
                    field.name,
                    vars(universal)[field.field_info.extra["universal_config"]],
                )
        return configuration

    def _fields_with_param(self, param: str) -> Generator[ModelField, None, None]:
        for field in self.model.__fields__.values():
            if param in field.field_info.extra:
                yield field

    def _setup_arg_parser(self):
        for field in self._fields_with_param("command_line"):
            flags = field.field_info.extra["command_line"]
            if not isinstance(flags, Tuple):
                flags = (flags,)
            self.arg_parser.add_argument(
                *flags,
                type=field.type_,
                help=field.field_info.description,
                default=SUPPRESS,
                metavar=field.name,
                dest=field.name,
            )

    def _parse_sources(self) -> Tuple[Optional[Dict[str, key]], UniversalConfig]:
        for source in self.sources:
            configuration = source.parse()
            if configuration:
                return configuration, source.universalconfig()
        return None, self.sources[0].universalconfig()
