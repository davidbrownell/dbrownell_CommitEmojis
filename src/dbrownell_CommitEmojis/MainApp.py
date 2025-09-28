# noqa: D100
import re

from pathlib import Path

import pyperclip  # type: ignore[import-untyped]

from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.widgets import Button, Collapsible, DataTable, Footer, Header, Input, Label

from dbrownell_CommitEmojis import __version__
from dbrownell_CommitEmojis.Lib import CreateEmojis, EmojiInfo


# ----------------------------------------------------------------------
class MainApp(App):
    """Main application."""

    CSS_PATH = Path(__file__).with_suffix(".tcss").name

    BINDINGS = [  # noqa: RUF012
        ("q", "quit", "Quit"),
        ("ctrl+c", "copy_commit_message", "Copy Commit Message"),
    ]

    # ----------------------------------------------------------------------
    def __init__(
        self,
        message: str | None,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)

        self.title = "CommitEmojis"

        self._message = message

        self._emojis = CreateEmojis()
        self._collapsibles: list[Collapsible] = []

        for key in self._emojis:
            self._collapsibles.append(
                # These values will be populated later
                Collapsible(
                    Label(""),
                    title="",
                    collapsed=key in {None, "Intentionally Skipped"},
                ),
            )

        self._filter_input = Input(id="filter", placeholder="Content Filter")
        self._commit_message_input = Input(
            id="text_input",
            placeholder="Enter commit message",
            select_on_focus=False,
        )

        self._commit_regex = re.compile(
            r"""
            ^                               # Start of string
            (?P<emojis>[^a-zA-Z0-9 \t\[]*)  # Detect emojis; this expression should work in this specific scenario, but is a bit of a hack
            \s*(?P<aliases>\[[^\]]*\])?\s*  # Aliases within []
            (?P<message>.*?)                # The message
            $                               # End of string
            """,
            re.VERBOSE,
        )

        self._copy_button = Button("copy", variant="primary", id="copy_button")

    # ----------------------------------------------------------------------
    def compose(self) -> ComposeResult:  # noqa: D102
        yield Header()

        with Vertical():
            with Horizontal(id="filter_row"):
                yield Label("[1]", classes="focus_shortcut")
                yield self._filter_input

            yield VerticalScroll(*self._collapsibles, id="main_content")

            with Horizontal(id="commit_message"):
                yield Label("[2]", classes="focus_shortcut")
                yield self._commit_message_input
                yield self._copy_button

        with Horizontal(id="footer"):
            yield Footer()
            yield Label(__version__)

    # ----------------------------------------------------------------------
    def on_mount(self) -> None:  # noqa: D102
        if self._message:
            self._commit_message_input.value = self._message

        self._copy_button.disabled = not bool(self._commit_message_input.value)

        self._PopulateEmojis()

    # ----------------------------------------------------------------------
    def key_1(self) -> None:  # noqa: D102
        self._filter_input.focus()

    # ----------------------------------------------------------------------
    def key_2(self) -> None:  # noqa: D102
        self._commit_message_input.focus()

    # ----------------------------------------------------------------------
    def on_input_changed(self, event: Input.Changed) -> None:  # noqa: D102
        if event.input.id == "filter":
            self._PopulateEmojis()
        elif event.input.id == "text_input":
            self._copy_button.label = "copy"
            self._copy_button.disabled = not bool(self._commit_message_input.value)

    # ----------------------------------------------------------------------
    def on_button_pressed(self, event: Button.Pressed) -> None:  # noqa: D102
        if event.button.id == "copy_button" and self._commit_message_input.value:
            self.action_copy_commit_message()

            # Change button text, disable it, and restore after a change
            self._copy_button.label = "copied!"
            self._copy_button.disabled = True

    # ----------------------------------------------------------------------
    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:  # noqa: D102
        emoji, alias = event.row_key.value  # type: ignore[attr-defined, misc]

        match = self._commit_regex.match(self._commit_message_input.value)
        assert match

        emojis = match.group("emojis")
        aliases = match.group("aliases") or ""
        message = match.group("message")

        emojis += emoji

        if alias:
            if aliases:
                assert aliases[0] == "[", aliases
                assert aliases[-1] == "]", aliases

                aliases = aliases[1:-1].strip()
                aliases += ", "
            aliases += alias

        self._commit_message_input.replace(
            f"{emojis} [{aliases}] {message}", 0, len(self._commit_message_input.value)
        )

    # ----------------------------------------------------------------------
    def action_copy_commit_message(self) -> None:  # noqa: D102
        if self._commit_message_input.value:
            pyperclip.copy(self._commit_message_input.value)

    # ----------------------------------------------------------------------
    def _PopulateEmojis(self) -> None:
        emoji_filter = self._filter_input.value.strip().lower()

        # ----------------------------------------------------------------------
        def ShouldInclude(info: EmojiInfo) -> bool:
            return (
                not emoji_filter
                or emoji_filter in info.name.lower()
                or emoji_filter in info.emoji.lower()
                or emoji_filter in info.description.lower()
                or any(emoji_filter in alias.lower() for alias in info.aliases)
            )

        # ----------------------------------------------------------------------

        with self.app.prevent():
            for (emojis_title, emojis), collapsible in zip(
                self._emojis.items(), self._collapsibles, strict=True
            ):
                items: list[EmojiInfo] = [info for info in emojis if ShouldInclude(info)]

                if emoji_filter:
                    collapsible.title = f"{emojis_title} ({len(items)} of {len(emojis)} displayed)"
                else:
                    collapsible.title = emojis_title or "Uncategorized"

                collapsible.children[1].remove_children()

                if not items:
                    continue

                dt: DataTable = DataTable(cursor_type="row")

                dt.add_columns("Emoji", "Name", "Description", "Aliases")
                for item in items:
                    dt.add_row(
                        item.code,
                        item.name,
                        item.description,
                        ", ".join(item.aliases),
                        key=(item.emoji, item.aliases[0] if item.aliases else ""),  # type: ignore[arg-type]
                    )

                collapsible.children[1].mount(dt)
