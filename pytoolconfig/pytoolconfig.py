"""Tool to configure Python tools."""
from argparse import SUPPRESS, ArgumentParser
from pathlib import Path
from typing import Dict, Generator, List, Optional, Tuple, Type

from pydantic import BaseModel, Field
from pydantic.fields import ModelField

from pytoolconfig.sources.pyproject import PyProject
from pytoolconfig.sources.source import Source
from pytoolconfig.types import key


class UniversalConfig(BaseModel):
    """Universal Configuration base model."""

    formatter: Optional[str] = Field(
        default=None, description="Formatter used to format this File."
    )
    max_line_length: int = Field(
        default=80, gt=5, description="Minimum Number of Lines in the File"
    )


def _add_args(arg_parser, model):
    for field in model.__fields__.values():
        if isinstance(field.type_, BaseModel):
            _add_args(arg_parser, field)

        # if "command_line" in field.extras:
        #     print(field)


class PyToolConfig:
    """Python Tool Configuration Aggregator."""

    sources: List[Source] = []
    global_sources: List[Source] = []
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
        """
        self.model = model
        self.sources = [PyProject(working_directory, tool)]
        self.sources.extend(custom_sources)
        self.global_sources = []
        if global_config:
            self.global_sources.append(
                PyProject(working_directory, tool, global_config=True)
            )
        self.global_sources.extend(global_sources)

        if arg_parser:
            self.arg_parser = arg_parser
            self._setup_arg_parser()

    def parse(self, args: List[str] = []) -> BaseModel:
        """
        Parse the configuration.

        args: any additional command line overwritesself.
        """
        sources = self.sources
        sources.extend(self.global_sources)
        raw_config = self._parse_sources(sources)
        if raw_config:
            configuration = self.model.parse_obj(raw_config)
        else:
            configuration = self.model()
        if self.arg_parser:
            parsed = self.arg_parser.parse_args(args)
            for field in self._arg_fields():
                if field.name in parsed:
                    setattr(configuration, field.name, vars(parsed)[field.name])
        return configuration

    def _arg_fields(self) -> Generator[ModelField, None, None]:
        for field in self.model.__fields__.values():
            if "command_line" in field.field_info.extra:
                yield field

    def _setup_arg_parser(self):
        for field in self._arg_fields():
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
            print(field.field_info.extra["command_line"])

    def _parse_sources(self, sources) -> Optional[Dict[str, key]]:
        for source in self.sources:
            configuration = source.parse()
            if configuration:
                return configuration
        return None
