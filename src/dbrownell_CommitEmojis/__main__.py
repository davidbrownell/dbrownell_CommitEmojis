"""Tools to create and display emojis used when committing changes to a repository."""

import sys

from enum import Enum
from pathlib import Path
from typing import Annotated

import typer

from dbrownell_Common.Streams.DoneManager import DoneManager, Flags as DoneManagerFlags
from typer.core import TyperGroup

from dbrownell_CommitEmojis.Lib import Display as DisplayImpl, Transform as TransformImpl
from dbrownell_CommitEmojis.MainApp import MainApp


# ----------------------------------------------------------------------
class NaturalOrderGrouper(TyperGroup):  # noqa: D101
    # ----------------------------------------------------------------------
    def list_commands(self, *args, **kwargs) -> list[str]:  # noqa: ARG002, D102
        return list(self.commands.keys())  # pragma: no cover


# ----------------------------------------------------------------------
app = typer.Typer(
    cls=NaturalOrderGrouper,
    no_args_is_help=True,
    pretty_exceptions_show_locals=False,
    pretty_exceptions_enable=False,
)


# ----------------------------------------------------------------------
class Command(Enum):
    """Enum values to invoke legacy functionality."""

    UX = "UX"
    LegacyDisplay = "Display"
    LegacyTransform = "Transform"


# ----------------------------------------------------------------------
@app.command("EntryPoint", help=__doc__, no_args_is_help=False)
def EntryPoint(
    command: Annotated[
        Command,
        typer.Argument(help="Command to invoke."),
    ] = "UX",
    message_or_filename: Annotated[
        str,
        typer.Argument(..., help="Message to transform (or filename that contains the message)."),
    ] = "",
    verbose: Annotated[  # noqa: FBT002
        bool,
        typer.Option("--verbose", help="Write verbose information to the terminal."),
    ] = False,
    debug: Annotated[  # noqa: FBT002
        bool,
        typer.Option("--debug", help="Write debug information to the terminal."),
    ] = False,
) -> None:
    """Entry point for the application."""

    if command == Command.LegacyDisplay:
        _Display(verbose=verbose, debug=debug)
        return

    if command == Command.LegacyTransform:
        _Transform(message_or_filename)
        return

    assert command == Command.UX, command
    _Ux(message_or_filename)


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
def _Display(
    *,
    verbose: bool,
    debug: bool,
) -> None:
    """Display supported emojis."""

    with DoneManager.CreateCommandLine(
        flags=DoneManagerFlags.Create(verbose=verbose, debug=debug),
    ) as dm:
        DisplayImpl(dm)


# ----------------------------------------------------------------------
def _Transform(message_or_filename: str) -> None:
    """Transform a message that contains emoji text placeholders."""

    potential_path = Path(message_or_filename)
    if potential_path.is_file():
        with potential_path.open(encoding="UTF-8") as f:
            message = f.read()
    else:
        message = message_or_filename

    sys.stdout.write(TransformImpl(message))


# ----------------------------------------------------------------------
def _Ux(message_or_filename: str) -> None:
    """Run the UX."""

    message: str | None = None

    potential_path = Path(message_or_filename)
    if potential_path.is_file():
        with potential_path.open(encoding="UTF-8") as f:
            message = f.read()
    else:
        message = message_or_filename

    message = message or None

    MainApp(message).run()


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
if __name__ == "__main__":
    app()  # pragma: no cover
