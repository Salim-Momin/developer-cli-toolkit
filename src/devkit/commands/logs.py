import typer

from devkit.core.logging import LOG_FILE
from devkit.terminal.components import (
    section_title,
    success,
    warning,
)
from devkit.terminal.theme import console

logs_app = typer.Typer(help="View and manage DevKit logs.")


@logs_app.command("show")
def show_logs(
    tail: int = typer.Option(
        50,
        "--tail",
        "-t",
        help="Number of recent log lines.",
        min=1,
        max=1000,
    ),
):
    """Display recent DevKit logs."""

    section_title(
        "📜 DevKit Logs",
        str(LOG_FILE),
    )

    if not LOG_FILE.exists():
        warning("No log file found.")
        return

    lines = LOG_FILE.read_text(
        encoding="utf-8",
        errors="ignore",
    ).splitlines()

    if not lines:
        warning("Log file is empty.")
        return

    console.print()

    for line in lines[-tail:]:
        console.print(line)


@logs_app.command("clear")
def clear_logs():
    """Delete all log entries."""

    if not LOG_FILE.exists():
        warning("No log file found.")
        return

    LOG_FILE.write_text(
        "",
        encoding="utf-8",
    )

    success("Logs cleared.")


@logs_app.command("path")
def log_path():
    """Show log file location."""

    section_title(
        "📁 Log Location",
        "",
    )

    console.print(LOG_FILE)
