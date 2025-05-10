# noqa: D100
import json
import re
import textwrap

from collections.abc import Generator
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path

from dbrownell_Common.Streams.DoneManager import DoneManager
from rich.console import Console, Group
from rich.table import Table
from rich.text import Text


# ----------------------------------------------------------------------
@dataclass(frozen=True)
class EmojiInfo:  # noqa: D101
    name: str
    emoji: str
    code: str
    description: str
    aliases: list[str]


# ----------------------------------------------------------------------
def CreateEmojis() -> dict[str | None, list[EmojiInfo]]:
    """Create emojis."""

    this_path = Path(__file__).parent

    # Read the emoji data
    data_filename = this_path / "gitmojis.json"
    assert data_filename.is_file(), data_filename

    with data_filename.open("r", encoding="UTF-8") as f:
        data_content = json.load(f)

    assert "gitmojis" in data_content, data_content.keys()
    data_content = data_content["gitmojis"]

    # ----------------------------------------------------------------------
    @dataclass(frozen=True)
    class RawEmojiInfo:
        name: str
        emoji: str
        description: str

    # ----------------------------------------------------------------------

    raw_emojis: dict[str, RawEmojiInfo] = {
        data["code"]: RawEmojiInfo(
            data["code"].replace(":", ""),
            data["emoji"],
            data["description"],
        )
        for data in data_content
    }

    # Read the category data
    categories_filename = this_path / "catagories.json"
    assert categories_filename.is_file(), categories_filename

    with categories_filename.open("r", encoding="UTF-8") as f:
        category_content = json.load(f)

    # Produce the results
    results: dict[str | None, list[EmojiInfo]] = {}

    for category_item in category_content:
        category_name = category_item["category"]

        these_emojis: list[EmojiInfo] = []

        for item in category_item["items"]:
            code = item["code"]

            raw_emoji = raw_emojis.pop(code, None)
            assert raw_emoji is not None, (category_name, code)

            these_emojis.append(
                EmojiInfo(
                    raw_emoji.name,
                    raw_emoji.emoji,
                    code,
                    raw_emoji.description,
                    item["aliases"],
                ),
            )

        assert these_emojis
        results[category_name] = these_emojis

    # Collect all of the items that didn't have an explicit category
    results[None] = [
        EmojiInfo(
            raw_emoji.name,
            raw_emoji.emoji,
            code,
            raw_emoji.description,
            [],
        )
        for code, raw_emoji in raw_emojis.items()
    ]

    return results


# ----------------------------------------------------------------------
def Display(
    done_manager_or_console: DoneManager | Console,
) -> None:
    """Display supported emojis."""

    with _YieldConsole(done_manager_or_console) as console:
        emojis = CreateEmojis()

        for category_name, items in emojis.items():
            if not items:
                continue

            should_display_aliases = category_name != "Intentionally Skipped"

            console.rule(
                f"[bold white]{category_name}[/]",
                align="left",
            )

            table = Table(
                show_footer=True,
            )

            for col_name, justify, footer in [
                ("Emoji", "center", None),
                (
                    "Emoji Name",
                    "center",
                    Text(
                        'add ":<name>:" to the commit message (e.g. ":tada:")',
                        style="italic",
                    ),
                ),
                ("Description", "left", None),
                (
                    "Aliases",
                    "left",
                    Text(
                        'add ":<alias>:" to the commit message (e.g. ":+project:")',
                        style="italic",
                    ),
                ),
            ]:
                if not should_display_aliases and col_name == "Aliases":
                    continue

                table.add_column(
                    col_name,
                    footer or "",
                    justify=justify,
                )

            for item in items:
                args = [item.code, item.name, item.description]

                if should_display_aliases:
                    args.append(", ".join(item.aliases))

                table.add_row(*args)

            console.print(Group("", table, ""))

        console.rule("This functionality uses emojis defined by [link=https://gitmoji.dev/]gitmoji[/]")


# ----------------------------------------------------------------------
def Transform(
    message: str,
) -> str:
    """Transform a message that contains emoji text placeholders."""

    emojis = CreateEmojis()

    emojis_regex = re.compile(
        textwrap.dedent(
            """\
            (?P<whole_match>:               # Whole match [start]
            (?P<value>[^:]+)                # Value
            :)                              # Whole match [end]
            """,
        ),
        re.VERBOSE,
    )

    # Populate aliases
    aliases: dict[str, str] = {}

    for items in emojis.values():
        for item in items:
            for alias in item.aliases:
                aliases[alias] = item.code

    # ----------------------------------------------------------------------
    def SubstituteAlias(
        match: re.Match,
    ) -> str:
        alias = match.group("value")

        emoji = aliases.get(alias)
        if emoji is None:
            return match.group("whole_match")

        return f"{emoji} [{alias}]"

    # ----------------------------------------------------------------------

    message = emojis_regex.sub(SubstituteAlias, message)

    # Populate emojis
    emoji_codes: dict[str, str] = {}

    for items in emojis.values():
        for item in items:
            assert item.code not in emojis, item.code
            emoji_codes[item.code] = item.emoji

    # ----------------------------------------------------------------------
    def SubstituteEmojis(
        match: re.Match,
    ) -> str:
        whole_match = match.group("whole_match")

        emoji = emoji_codes.get(whole_match)
        if emoji is None:
            return whole_match

        return emoji

    # ----------------------------------------------------------------------

    return emojis_regex.sub(SubstituteEmojis, message)


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
@contextmanager
def _YieldConsole(
    done_manager_or_console: DoneManager | Console,
) -> Generator[Console]:
    """Yield a console object.

    This is here to make testing easier.
    """

    if isinstance(done_manager_or_console, Console):
        yield done_manager_or_console
        return

    with done_manager_or_console.YieldStdout() as stdout_stream:
        console = Console(file=stdout_stream.stream)
        yield console
