from contextlib import contextmanager

from rich.rule import Rule
from rich.table import Table

from devkit.terminal.theme import console


def show_banner():

    console.print(
        """
[bold cyan]
██████╗ ███████╗██╗   ██╗██╗  ██╗██╗████████╗
██╔══██╗██╔════╝██║   ██║██║ ██╔╝██║╚══██╔══╝
██║  ██║█████╗  ██║   ██║█████╔╝ ██║   ██║
██║  ██║██╔══╝  ╚██╗ ██╔╝██╔═██╗ ██║   ██║
██████╔╝███████╗ ╚████╔╝ ██║  ██╗██║   ██║
╚═════╝ ╚══════╝  ╚═══╝  ╚═╝  ╚═╝╚═╝   ╚═╝
[/bold cyan]

[bold white]
Developer CLI Toolkit
[/bold white]

[dim]
Build • Debug • Analyze • Automate

DevKit v0.1.0
[/dim]

"""
    )

def section_title(
    title: str,
    subtitle: str | None = None,
) -> None:
    """Display a standardized section heading."""

    console.print()

    console.print(f"[devkit.primary]{title}[/devkit.primary]")

    if subtitle:
        console.print(f"[devkit.secondary]{subtitle}[/devkit.secondary]")

    console.print()


def success(message: str) -> None:
    """Display a success message."""

    console.print(f"[devkit.success]✓ {message}[/devkit.success]")


def warning(message: str) -> None:
    """Display a warning message."""

    console.print(f"[devkit.warning]⚠ {message}[/devkit.warning]")


def error(message: str) -> None:
    """Display an error message."""

    console.print(f"[devkit.error]✗ {message}[/devkit.error]")


def info(message: str) -> None:
    """Display an informational message."""

    console.print(f"[devkit.info]• {message}[/devkit.info]")


def command_hint(command: str) -> None:
    """Display a command hint."""

    console.print(
        f"[devkit.secondary]Try:[/devkit.secondary] " f"[bold]{command}[/bold]"
    )


def build_menu_table() -> Table:
    """Create the main DevKit menu."""

    table = Table(
        show_header=False,
        box=None,
        padding=(0, 2),
    )

    table.add_column(
        "Option",
        style="devkit.primary",
        width=4,
    )

    table.add_column(
        "Command",
    )

    return table


def divider(
    title: str | None = None,
) -> None:
    """Print a subtle DevKit divider."""

    console.print(
        Rule(
            title or "",
            style="bright_black",
        )
    )


def result_summary(
    title: str,
    values: list[tuple[str, str]],
) -> None:
    """Display a compact result summary."""

    from devkit.terminal.tables import (
        create_key_value_table,
    )

    table = create_key_value_table(title=title)

    for label, value in values:
        table.add_row(
            label,
            value,
        )

    console.print(table)


def footer_hint(
    text: str,
) -> None:
    """Display a subtle terminal usage hint."""

    console.print()

    console.print(f"[bright_black]{text}[/bright_black]")


@contextmanager
def loading(
    message: str,
):
    """Display a DevKit loading spinner."""

    with console.status(
        f"[cyan]{message}[/cyan]",
        spinner="dots",
    ):
        yield


def debug_error(
    message: str,
    exception: Exception | None = None,
    debug: bool = False,
) -> None:
    """Display a clean error and optional debug details."""

    error(message)

    if debug and exception:
        console.print()

        console.print_exception(show_locals=False)
