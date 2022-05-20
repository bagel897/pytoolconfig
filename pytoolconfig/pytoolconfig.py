"""Tool to configure Python tools."""
from argparse import SUPPRESS, ArgumentParser
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Type

from pytoolconfig.fields import _gather_config_fields
from pytoolconfig.sources.pyproject import PyProject
from pytoolconfig.sources.source import Source
from pytoolconfig.types import ConfigField, Dataclass
from pytoolconfig.universal_config import UniversalConfig
from pytoolconfig.utils import _dict_to_dataclass


class PyToolConfig:
    """Python Tool Configuration Aggregator."""

    sources: List[Source] = []
    tool: str
    working_directory: Path
    model: Type[Dataclass]
    arg_parser: Optional[ArgumentParser] = None
    _config_fields: Dict[str, ConfigField]

    def __init__(
        self,
        tool: str,
        working_directory: Path,
        model: Type[Dataclass],
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

        :param tool: str name of the tool to use.
        :param working_directory: Path working directory in use.
        :param model: Type[BaseModel] Model of configuration.
        :param arg_parser: ArgumentParser Arugument Parser.
        :param custom_sources: List[Source] custom sources
        :param global_config: List[Source] enable global configuration
        :param global_sources: List[Source] custom global sources
        :param bases: List[str] custom bases
        :param recursive: bool Recusively search for the pyproject.toml file
        """
        self.model = model
        self._config_fields = _gather_config_fields(model)
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

    def parse(self, args: List[str] = []) -> Dataclass:
        """
        Parse the configuration.

        args: any additional command line overwritesself.
        """
        configuration, universal = self._parse_sources()
        if self.arg_parser:
            parsed = self.arg_parser.parse_args(args)
            for name, value in parsed._get_kwargs():
                setattr(configuration, name, value)
        for name, field in self._config_fields.items():
            if field.universal_config:
                setattr(
                    configuration,
                    name,
                    vars(universal)[field.universal_config],
                )
        return configuration

    def _setup_arg_parser(self):
        for name, field in self._config_fields.items():
            if field.command_line:
                flags = field.command_line
                if not isinstance(flags, Tuple):
                    flags = (flags,)
                self.arg_parser.add_argument(
                    *flags,
                    type=field._type,
                    help=field.description,
                    default=SUPPRESS,
                    metavar=name,
                    dest=name,
                )

    def _parse_sources(self) -> Tuple[Dataclass, UniversalConfig]:
        for source in self.sources:
            configuration = source.parse()
            if configuration:
                return (
                    _dict_to_dataclass(self.model, configuration),
                    source.universalconfig(),
                )
        return self.model(), self.sources[0].universalconfig()
