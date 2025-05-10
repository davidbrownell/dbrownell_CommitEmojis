import os

import pytest

from dbrownell_CommitEmojis.Lib import *


# ----------------------------------------------------------------------
def test_CreateEmojis():
    emojis = CreateEmojis()
    assert emojis


# ----------------------------------------------------------------------
def test_Display(snapshot):
    console = Console(
        force_terminal=True,
        width=100,
    )

    with console.capture() as capture:
        Display(console)

    output = capture.get()

    # The last line of the output contains a link, which includes a random id. Remove this link
    # so comparisons work as expected.
    output = output.rstrip()

    output_lines = output.splitlines()
    assert "This functionality uses emojis defined by" in output_lines[-1]

    output = "\n".join(output_lines[:-1])

    # Extra unicode characters are displayed when running on Windows in GitHub Actions; it works as
    # expected when running on a Windows machine locally.
    if os.environ.get("GITHUB_ACTIONS", None) == "true" and os.name == "nt":
        assert output
    else:
        assert output == snapshot


# ----------------------------------------------------------------------
class TestTransform:
    # ----------------------------------------------------------------------
    def test_NoValues(self):
        assert Transform("No embedded emojis") == "No embedded emojis"

    # ----------------------------------------------------------------------
    def test_NoMatches(self):
        assert Transform(":smile:") == ":smile:"

    # ----------------------------------------------------------------------
    def test_Emoji(self):
        assert Transform("___ :tada: ___") == "___ 🎉 ___"

    # ----------------------------------------------------------------------
    def test_Alias(self):
        assert Transform("___ :+project: ___") == "___ 🎉 [+project] ___"
