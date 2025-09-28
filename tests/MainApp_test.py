import platform

import pytest

from textual.widgets import Button

from dbrownell_CommitEmojis.MainApp import MainApp


# ----------------------------------------------------------------------
def test_Startup(snap_compare):
    assert snap_compare(MainApp(None))


# ----------------------------------------------------------------------
def test_StartupLarge(snap_compare):
    assert snap_compare(MainApp(None), terminal_size=(200, 60))


# ----------------------------------------------------------------------
def test_StartupWithMessage(snap_compare):
    assert snap_compare(MainApp("This is the initial message"))


# ----------------------------------------------------------------------
def test_Filtered(snap_compare):
    assert snap_compare(MainApp(None), terminal_size=(200, 60), press=["c", "i"])


# ----------------------------------------------------------------------
def test_FocusFilter(snap_compare):
    assert snap_compare(MainApp(None), press=["c", "i", "tab", "1"])


# ----------------------------------------------------------------------
def test_FocusCommitMessage(snap_compare):
    assert snap_compare(MainApp("This is the commit message"), press=["c", "i", "tab", "2"])


# ----------------------------------------------------------------------
@pytest.mark.skipif(
    platform.system() == "Linux",
    reason="Linux requires 3rd party dependencies for clipboard access.",
)
def test_CopyButton(snap_compare):
    # ----------------------------------------------------------------------
    async def Setup(pilot) -> None:
        await pilot.click(Button)

    # ----------------------------------------------------------------------

    assert snap_compare(MainApp("This is the commit message"), run_before=Setup)


# ----------------------------------------------------------------------
def test_CopyButtonNoContent(snap_compare):
    # ----------------------------------------------------------------------
    async def Setup(pilot) -> None:
        await pilot.click(Button)

    # ----------------------------------------------------------------------

    assert snap_compare(MainApp(None), run_before=Setup)


# ----------------------------------------------------------------------
def test_AddOneEmoji(snap_compare):
    assert snap_compare(MainApp(None), press=["tab", "tab", "tab", "down", "down", "enter"])


# ----------------------------------------------------------------------
def test_AddOneEmojiWithMessage(snap_compare):
    assert snap_compare(
        MainApp("This is the commit message"), press=["tab", "tab", "tab", "down", "down", "enter"]
    )


# ----------------------------------------------------------------------
def test_AddMultipleEmojis(snap_compare):
    assert snap_compare(
        MainApp("This is the commit message"),
        terminal_size=(200, 60),
        press=["tab", "tab", "tab", "down", "down", "enter", "down", "enter", "enter"],
    )
