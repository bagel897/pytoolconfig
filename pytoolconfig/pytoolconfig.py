"""Tool to configure Python tools."""
from argparse import SUPPRESS, ArgumentParser
from pathlib import Path
from typing import Dict, Generic, List, Optional, Type, TypeVar

from pytoolconfig.fields import _gather_config_fields
from pytoolconfig.sources.pyproject import PyProject
from pytoolconfig.sources.source import Source
from pytoolconfig.types import ConfigField, Dataclass
from pytoolconfig.universal_config import UniversalConfig
from pytoolconfig.utils import _dict_to_dataclass

T = TypeVar("T", bound="Dataclass")


class PyToolConfig(Generic[T]):
    """Python Tool Configuration Aggregator."""

    sources: List[Source] = []
    tool: str
    working_directory: Path
    model: Type[T]
    arg_parser: Optional[ArgumentParser] = None
    _config_fields: Dict[str, ConfigField]

    def __init__(
        self,
        tool: str,
        working_directory: Path,
        model: Type[T],
        arg_parser: Optional[ArgumentParser] = None,
        custom_sources: Optional[List[Source]] = None,
        global_config: bool = False,
        global_sources: Optional[List[Source]] = None,
        bases: List[str] = [".git", ".hg"],
        recursive: bool = True,
    ):
        """
        Initialize the configuration object.

        :param tool: name of the tool to use.
        :param working_directory: working directory in use.
        :param model: Model of configuration.
        :param arg_parser: Arugument Parser.
        :param custom_sources: Custom sources
        :param global_config: Enable global configuration
        :param global_sources: Custom global sources
        :param bases: Custom bases
        :param recursive: Recusively search for the pyproject.toml file
        """
        self.model = model
        self._config_fields = _gather_config_fields(model)
        self.tool = tool
        self.sources = [PyProject(working_directory, tool, bases, recursive=recursive)]
        if custom_sources:
            self.sources.extend(custom_sources)
        if global_config:
            self.sources.append(
                PyProject(
                    working_directory, tool, bases, global_config=True, recursive=False
                )
            )
        if global_sources:
            self.sources.extend(global_sources)

        self.arg_parser = arg_parser
        self._setup_arg_parser()

    def parse(self, args: List[str] = []) -> T:
        """
        Parse the configuration.

        :param args: any additional command line overwrites.
        """
        configuration = self._parse_sources()
        assert isinstance(self.sources[0], PyProject)
        universal: UniversalConfig = self.sources[0].universalconfig()
        if self.arg_parser:
            parsed = self.arg_parser.parse_args(args)
            for name, value in parsed._get_kwargs():
                setattr(configuration, name, value)
        for name, field in self._config_fields.items():
            if field.universal_config:
                universal_value = vars(universal)[field.universal_config.name]
                if universal_value is not None:
                    setattr(
                        configuration,
                        name,
                        universal_value,
                    )
        return configuration

    def _setup_arg_parser(self) -> None:
        if self.arg_parser:
            for name, field in self._config_fields.items():
                if field.command_line:
                    flags = field.command_line
                    self.arg_parser.add_argument(
                        *flags,
                        type=field._type,
                        help=field.description,
                        default=SUPPRESS,
                        metavar=name,
                        dest=name,
                    )

    def _parse_sources(self) -> T:
        for source in self.sources:
            configuration = source.parse()
            if configuration:
                return _dict_to_dataclass(self.model, configuration)
        return self.model()
