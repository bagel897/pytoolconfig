from pytoolconfig.utils import find_config_file


def test_find_pyproject(cwd):
    result = find_config_file(cwd.parent, "pyproject.toml", [".git"])
    assert result
    assert result == cwd.parent.parent / "pyproject.toml"
