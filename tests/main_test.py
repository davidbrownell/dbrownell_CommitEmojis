from pathlib import Path

from dbrownell_CommitEmojis import __main__
from typer.testing import CliRunner


class TestDisplay:
    # ----------------------------------------------------------------------
    def test_Standard(self, monkeypatch):
        # ----------------------------------------------------------------------
        def MockDisplay(dm):
            assert dm is not None
            assert dm.is_verbose is False
            assert dm.is_debug is False

        # ----------------------------------------------------------------------

        monkeypatch.setattr(__main__, "DisplayImpl", MockDisplay)

        result = CliRunner().invoke(__main__.app, ["Display"])
        assert result.exit_code == 0, result.output

    # ----------------------------------------------------------------------
    def test_Verbose(self, monkeypatch):
        # ----------------------------------------------------------------------
        def MockDisplay(dm):
            assert dm is not None
            assert dm.is_verbose is True
            assert dm.is_debug is False

        # ----------------------------------------------------------------------

        monkeypatch.setattr(__main__, "DisplayImpl", MockDisplay)

        result = CliRunner().invoke(__main__.app, ["Display", "--verbose"])
        assert result.exit_code == 0, result.output

    # ----------------------------------------------------------------------
    def test_Debug(self, monkeypatch):
        # ----------------------------------------------------------------------
        def MockDisplay(dm):
            assert dm is not None
            assert dm.is_verbose is True
            assert dm.is_debug is True

        # ----------------------------------------------------------------------

        monkeypatch.setattr(__main__, "DisplayImpl", MockDisplay)

        result = CliRunner().invoke(__main__.app, ["Display", "--debug"])
        assert result.exit_code == 0, result.output

    # ----------------------------------------------------------------------
    def test_VerboseDebug(self, monkeypatch):
        # ----------------------------------------------------------------------
        def MockDisplay(dm):
            assert dm is not None
            assert dm.is_verbose is True
            assert dm.is_debug is True

        # ----------------------------------------------------------------------

        monkeypatch.setattr(__main__, "DisplayImpl", MockDisplay)

        result = CliRunner().invoke(__main__.app, ["Display", "--verbose", "--debug"])
        assert result.exit_code == 0, result.output


# ----------------------------------------------------------------------
class TestTransform:
    # ----------------------------------------------------------------------
    def test_Standard(self, monkeypatch):
        # ----------------------------------------------------------------------
        def MockTransform(message):
            assert message == "Before :+feature: After"
            return "Mocked value"

        # ----------------------------------------------------------------------

        monkeypatch.setattr(__main__, "TransformImpl", MockTransform)

        result = CliRunner().invoke(__main__.app, ["Transform", "Before :+feature: After"])
        assert result.exit_code == 0, result.output
        assert result.stdout == "Mocked value", result.output

    # ----------------------------------------------------------------------
    def test_FileInput(self, monkeypatch):
        # ----------------------------------------------------------------------
        def MockTransform(message):
            assert message.startswith("from pathlib import Path"), message
            return "Mocked value"

        # ----------------------------------------------------------------------

        monkeypatch.setattr(__main__, "TransformImpl", MockTransform)

        result = CliRunner().invoke(__main__.app, ["Transform", str(Path(__file__))])
        assert result.exit_code == 0, result.output
        assert result.stdout == "Mocked value", result.output
