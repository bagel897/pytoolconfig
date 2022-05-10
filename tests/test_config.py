from pytoolconfig.sources import IniConfig, PyProject


def test_base_pyproject(cwd):
    pyproject = PyProject(cwd, "pytoolconfig")
    assert pyproject.exists
    assert pyproject.parse()["formatter"] == "black"
    assert pyproject.min_py_version == (3, 7)


def test_base_ini(cwd):
    config = IniConfig(cwd, "test_config.ini", "pytoolconfig").parse()
    assert config["formatter"] == "yapf"
