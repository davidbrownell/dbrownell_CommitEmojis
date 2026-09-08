import json

from dataclasses import asdict
from pathlib import Path
from unittest.mock import Mock

from dbrownell_CommitEmojis import __main__, __version__
from dbrownell_CommitEmojis.Lib import CreateEmojis
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
class TestDisplayJson:
    # ----------------------------------------------------------------------
    def test_Standard(self, monkeypatch):
        # ----------------------------------------------------------------------
        def MockDisplayJson(console):
            assert console is not None
            console.print("Mocked value")

        # ----------------------------------------------------------------------

        monkeypatch.setattr(__main__, "DisplayJsonImpl", MockDisplayJson)

        result = CliRunner().invoke(__main__.app, ["DisplayJson"])
        assert result.exit_code == 0, result.output
        assert "Mocked value" in result.stdout, result.output

    # ----------------------------------------------------------------------
    def test_ValidJson(self):
        result = CliRunner().invoke(__main__.app, ["DisplayJson"])
        assert result.exit_code == 0, result.output

        content = json.loads(result.stdout)

        assert content

        for category in content:
            assert set(category.keys()) == {"category", "items"}

            for item in category["items"]:
                assert set(item.keys()) == {
                    "name",
                    "emoji",
                    "code",
                    "description",
                    "aliases",
                }

    # ----------------------------------------------------------------------
    def test_MatchesCreateEmojis(self):
        result = CliRunner().invoke(__main__.app, ["DisplayJson"])
        assert result.exit_code == 0, result.output

        content = json.loads(result.stdout)
        emojis = CreateEmojis()

        assert len(content) == len(emojis)

        for category, (category_name, items) in zip(content, emojis.items(), strict=True):
            assert category["category"] == category_name
            assert len(category["items"]) == len(items)

            for item, expected in zip(category["items"], items, strict=True):
                assert item == asdict(expected)


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
            assert message.startswith("import json"), message
            return "Mocked value"

        # ----------------------------------------------------------------------

        monkeypatch.setattr(__main__, "TransformImpl", MockTransform)

        result = CliRunner().invoke(__main__.app, ["Transform", str(Path(__file__))])
        assert result.exit_code == 0, result.output
        assert result.stdout == "Mocked value", result.output


# ----------------------------------------------------------------------
class TestUx:
    # ----------------------------------------------------------------------
    def test_Standard(self, monkeypatch):
        main_app_mock = Mock()

        monkeypatch.setattr(__main__, "MainApp", main_app_mock)

        result = CliRunner().invoke(__main__.app, [])
        assert result.exit_code == 0, result.output

        assert main_app_mock.call_count == 1, result.output
        assert main_app_mock.call_args == ((None,), {}), result.output

    # ----------------------------------------------------------------------
    def test_WithString(self, monkeypatch):
        main_app_mock = Mock()

        monkeypatch.setattr(__main__, "MainApp", main_app_mock)

        result = CliRunner().invoke(__main__.app, ["UX", "This is a test"])
        assert result.exit_code == 0, result.output

        assert main_app_mock.call_count == 1, result.output
        assert main_app_mock.call_args == (("This is a test",), {}), result.output

    # ----------------------------------------------------------------------
    def test_WithFile(self, monkeypatch):
        main_app_mock = Mock()

        monkeypatch.setattr(__main__, "MainApp", main_app_mock)

        result = CliRunner().invoke(__main__.app, ["UX", str(Path(__file__))])
        assert result.exit_code == 0, result.output

        assert main_app_mock.call_count == 1, result.output
        assert len(main_app_mock.call_args.args[0]) > 100, result.output


# ----------------------------------------------------------------------
class TestVersion:
    # ----------------------------------------------------------------------
    def test_Standard(self):
        result = CliRunner().invoke(__main__.app, ["--version"])
        assert result.exit_code == 0, result.output
        assert result.stdout.strip() == f"commit_emojis v{__version__}", result.output

    # ----------------------------------------------------------------------
    def test_IsEager(self, monkeypatch):
        # The version should be displayed even when other arguments are provided.
        main_app_mock = Mock()

        monkeypatch.setattr(__main__, "MainApp", main_app_mock)

        result = CliRunner().invoke(__main__.app, ["UX", "This is a test", "--version"])
        assert result.exit_code == 0, result.output
        assert result.stdout.strip() == f"commit_emojis v{__version__}", result.output

        assert main_app_mock.call_count == 0, result.output
