# tests/test_yudownloader.py

from typer.testing import CliRunner

from yudownloader import __app_name__, __version__, main

runner = CliRunner()

def test_version():
    result = runner.invoke(main.app, ["--version"])
    assert result.exit_code == 0
    assert f"{__app_name__} v{__version__}\n" in result.stdout