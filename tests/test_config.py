from pytoolconfig.sources import IniConfig, PyProject, SetupConfig


def test_base_pyproject(cwd):
    pyproject = PyProject(cwd, "pytoolconfig", [])
    assert pyproject.parse()["formatter"] == "black"
    assert pyproject._min_py_version == (3, 7)
    universal = pyproject.universalconfig()
    assert universal.min_py_version == (3, 7)
    assert universal.formatter == "black"


def test_base_ini(cwd):
    config = IniConfig(cwd, "test_config.ini", "pytoolconfig").parse()
    assert config["formatter"] == "yapf"


def test_setup_cfg(cwd):
    setup_cfg = SetupConfig(cwd, "pytoolconfig")
    assert setup_cfg.parse()
    assert setup_cfg._min_py_version == (3, 8)
    universal = setup_cfg.universalconfig()
    assert universal.min_py_version == (3, 8)
