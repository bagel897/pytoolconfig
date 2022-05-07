from pytoolconfig.sources.ini import IniConfig
from pytoolconfig.sources.pyproject import PyProject


def test_base_pyproject(cwd):
    pyproject = PyProject(cwd, "pytoolconfig")
    assert pyproject.exists
    assert pyproject.parse()["formatter"] == "black"


def test_base_ini(cwd):
    config = IniConfig(cwd, "test_config.ini", "pytoolconfig").parse()
    assert config["formatter"] == "yapf"
