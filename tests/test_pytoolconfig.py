from pytoolconfig.pytoolconfig import PyToolConfig


def test_simple(cwd):
    config = PyToolConfig("pytoolconfig", cwd)
    result = config.parse()
    assert result["formatter"] == "black"
