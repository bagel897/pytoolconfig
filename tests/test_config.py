import sys

from pytoolconfig.sources import IniConfig, PyProject, SetupConfig


def test_base_pyproject(cwd):
    pyproject = PyProject(cwd, "pytoolconfig", [])
    assert pyproject.parse()["formatter"] == "black"
    universal = pyproject.universalconfig()
    assert universal.min_py_version == (3, 7)
    assert universal.max_py_version == (sys.version_info.major, sys.version_info.minor)
    assert universal.formatter == "black"
    assert "sphinx" in [dep.name for dep in universal.optional_dependencies["doc"]]


def test_base_ini(cwd):
    config = IniConfig(cwd, "test_config.ini", "pytoolconfig").parse()
    assert config["formatter"] == "yapf"


def test_setup_cfg(cwd):
    setup_cfg = SetupConfig(cwd, "pytoolconfig")
    assert setup_cfg.parse()
