from pathlib import Path

from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from devkit.terminal.theme import console


def show_banner() -> None:
    """Display the main DevKit application banner."""

    project = Path.cwd().name

    content = Text()

    content.append("⚡ DEVKIT\n", style="devkit.primary")
    content.append(
        "Developer Command Center\n\n",
        style="devkit.title",
    )

    content.append(
        "Current Project  ",
        style="devkit.secondary",
    )

    content.append(
        project,
        style="devkit.info",
    )

    console.print()

    console.print(
        Panel(
            content,
            border_style="cyan",
            padding=(1, 4),
        )
    )


def section_title(
    title: str,
    subtitle: str | None = None,
) -> None:
    """Display a standardized section heading."""

    console.print()

    console.print(
        f"[devkit.primary]{title}[/devkit.primary]"
    )

    if subtitle:
        console.print(
            f"[devkit.secondary]{subtitle}[/devkit.secondary]"
        )

    console.print()


def success(message: str) -> None:
    """Display a success message."""

    console.print(
        f"[devkit.success]✓ {message}[/devkit.success]"
    )


def warning(message: str) -> None:
    """Display a warning message."""

    console.print(
        f"[devkit.warning]⚠ {message}[/devkit.warning]"
    )


def error(message: str) -> None:
    """Display an error message."""

    console.print(
        f"[devkit.error]✗ {message}[/devkit.error]"
    )


def info(message: str) -> None:
    """Display an informational message."""

    console.print(
        f"[devkit.info]• {message}[/devkit.info]"
    )


def command_hint(command: str) -> None:
    """Display a command hint."""

    console.print(
        f"[devkit.secondary]Try:[/devkit.secondary] "
        f"[bold]{command}[/bold]"
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