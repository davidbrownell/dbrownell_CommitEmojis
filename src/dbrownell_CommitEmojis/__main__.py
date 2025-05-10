"""Tools to create and display emojis used when committing changes to a repository."""

import sys

from pathlib import Path
from typing import Annotated

import typer

from dbrownell_Common.Streams.DoneManager import DoneManager, Flags as DoneManagerFlags
from typer.core import TyperGroup

from .Lib import Display as DisplayImpl, Transform as TransformImpl


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
@app.command("Display", no_args_is_help=False)
def Display(
    verbose: Annotated[  # noqa: FBT002
        bool,
        typer.Option("--verbose", help="Write verbose information to the terminal."),
    ] = False,
    debug: Annotated[  # noqa: FBT002
        bool,
        typer.Option("--debug", help="Write debug information to the terminal."),
    ] = False,
) -> None:
    """Display supported emojis."""

    with DoneManager.CreateCommandLine(
        flags=DoneManagerFlags.Create(verbose=verbose, debug=debug),
    ) as dm:
        DisplayImpl(dm)


# ----------------------------------------------------------------------
@app.command("Transform", no_args_is_help=True)
def Transform(
    message_or_filename: Annotated[
        str,
        typer.Argument(..., help="Message to transform (or filename that contains the message)."),
    ],
) -> None:
    """Transform a message that contains emoji text placeholders."""

    potential_path = Path(message_or_filename)
    if potential_path.is_file():
        with potential_path.open(encoding="UTF-8") as f:
            message = f.read()
    else:
        message = message_or_filename

    sys.stdout.write(TransformImpl(message))


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
if __name__ == "__main__":
    app()  # pragma: no cover
