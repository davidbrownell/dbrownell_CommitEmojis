# noqa: INP001
# ----------------------------------------------------------------------
# |
# |  update_data.py
# |
# |  David Brownell <db@DavidBrownell.com>
# |      2025-05-10 10:05:00
# |
# ----------------------------------------------------------------------
# |
# |  Copyright David Brownell 2022-23
# |  Distributed under the Boost Software License, Version 1.0. See
# |  accompanying file LICENSE_1_0.txt or copy at
# |  http://www.boost.org/LICENSE_1_0.txt.
# |
# ----------------------------------------------------------------------
"""Updates the Gitmoji data."""

from pathlib import Path
from typing import Annotated

import requests
import typer

from typer.core import TyperGroup

from dbrownell_Common.Streams.DoneManager import DoneManager, Flags as DoneManagerFlags


# ----------------------------------------------------------------------
class NaturalOrderGrouper(TyperGroup):  # noqa: D101
    # ----------------------------------------------------------------------
    def list_commands(self, *args, **kwargs) -> list[str]:  # noqa: ARG002, D102
        return list(self.commands.keys())


# ----------------------------------------------------------------------
app = typer.Typer(
    cls=NaturalOrderGrouper,
    no_args_is_help=True,
    pretty_exceptions_show_locals=False,
    pretty_exceptions_enable=False,
)


# ----------------------------------------------------------------------
@app.command("Update", no_args_is_help=False)
def Update(
    url_base: Annotated[
        str,
        typer.Option("--url-base", help="Base url of the gitmoji data."),
    ] = "https://raw.githubusercontent.com/carloscuesta/gitmoji/master/packages/gitmojis/src",
    filenames: Annotated[
        list[str],
        typer.Option("--filename", help="gitmoji files to download."),
    ] = ["gitmojis.json", "schema.json"],  # noqa: B006
    verbose: Annotated[  # noqa: FBT002
        bool,
        typer.Option("--verbose", help="Write verbose information to the terminal."),
    ] = False,
    debug: Annotated[  # noqa: FBT002
        bool,
        typer.Option("--debug", help="Write debug information to the terminal."),
    ] = False,
) -> None:
    """Update the Gitmoji data."""

    with DoneManager.CreateCommandLine(
        flags=DoneManagerFlags.Create(verbose=verbose, debug=debug),
    ) as dm:
        output_dir = Path(__file__).parent.parent / "src" / "dbrownell_CommitEmojis"
        assert output_dir.is_dir(), output_dir

        for filename_index, filename in enumerate(filenames):
            with dm.Nested(
                "Downloading '{}' ({} of {})...".format(
                    filename,
                    filename_index + 1,
                    len(filenames),
                ),
            ):
                response = requests.get("{}/{}".format(url_base, filename))  # noqa: S113
                response.raise_for_status()

                content = response.text

                (output_dir / filename).write_text(content, encoding="UTF-8")

        dm.WriteLine(f"\nContent has been downloaded to '{output_dir}'.\n")


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
if __name__ == "__main__":
    app()
