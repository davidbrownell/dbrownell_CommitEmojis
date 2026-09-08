import json
import os

from dataclasses import asdict

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
def test_DisplayJson():
    console = Console(width=100)

    with console.capture() as capture:
        DisplayJson(console)

    content = json.loads(capture.get())
    emojis = CreateEmojis()

    assert len(content) == len(emojis)

    for category, (category_name, items) in zip(content, emojis.items(), strict=True):
        assert category["category"] == category_name
        assert category["items"] == [asdict(item) for item in items]


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
