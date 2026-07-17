import platform
import time

import pytest

from textual.widgets import Button, Label

from dbrownell_CommitEmojis.MainApp import MainApp


# ----------------------------------------------------------------------
async def _WaitFor(pilot, condition, timeout: float = 5.0) -> None:
    """Pump the message loop until condition() is truthy or the timeout expires."""
    deadline = time.monotonic() + timeout
    while not condition() and time.monotonic() < deadline:
        await pilot.pause(0.01)


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
        await pilot.pause(0.5)

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


# ----------------------------------------------------------------------
@pytest.mark.asyncio
async def test_CharCounterUpdates():
    app = MainApp(None)
    async with app.run_test() as pilot:
        char_counter = app.query_one("#char_counter", Label)
        assert str(char_counter.render()) == "0"

        app._commit_message_input.value = "test"
        await _WaitFor(pilot, lambda: str(char_counter.render()) == "4")
        assert str(char_counter.render()) == "4"


# ----------------------------------------------------------------------
@pytest.mark.asyncio
async def test_CharCounterWithInitialMessage():
    message = "Initial message"
    app = MainApp(message)
    async with app.run_test() as pilot:
        char_counter = app.query_one("#char_counter", Label)
        await _WaitFor(pilot, lambda: str(char_counter.render()) == str(len(message)))
        assert str(char_counter.render()) == str(len(message))


# ----------------------------------------------------------------------
@pytest.mark.asyncio
async def test_CharCounterOverLimit():
    app = MainApp(None)
    async with app.run_test() as pilot:
        char_counter = app.query_one("#char_counter", Label)

        # Under limit - no over_limit class
        app._commit_message_input.value = "x" * 70
        await _WaitFor(pilot, lambda: str(char_counter.render()) == "70")
        assert "over_limit" not in char_counter.classes

        # Over limit - has over_limit class
        app._commit_message_input.value = "x" * 71
        await _WaitFor(pilot, lambda: "over_limit" in char_counter.classes)
        assert "over_limit" in char_counter.classes

        # Back under limit - class removed
        app._commit_message_input.value = "x" * 50
        await _WaitFor(pilot, lambda: "over_limit" not in char_counter.classes)
        assert "over_limit" not in char_counter.classes
