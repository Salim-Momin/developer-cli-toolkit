import typer
from rich.console import Console

from devkit.commands.api import api_app
from devkit.commands.config import config_app
from devkit.commands.convert import convert_app
from devkit.commands.doctor import doctor
from devkit.commands.git import git_app
from devkit.commands.json_tools import json_app
from devkit.commands.logs import logs_app
from devkit.commands.project import project_app
from devkit.commands.search import search_text
from devkit.commands.yaml_tools import yaml_app
from devkit.core.logging import get_logger, setup_logging
from devkit.ui import run_interactive_menu

app = typer.Typer(
    name="devkit",
    help="Developer CLI Toolkit — useful tools for developers.",
    invoke_without_command=True,
)

console = Console()

app.add_typer(
    project_app,
    name="project",
)

app.add_typer(
    git_app,
    name="git",
)

app.add_typer(
    json_app,
    name="json",
)

app.add_typer(
    yaml_app,
    name="yaml",
)

app.add_typer(
    convert_app,
    name="convert",
)

app.add_typer(
    api_app,
    name="api",
)

app.add_typer(
    config_app,
    name="config",
)

app.add_typer(logs_app, name="logs")

app.command("search")(search_text)
app.command("doctor")(doctor)


@app.callback()
def main(
    ctx: typer.Context,
    debug: bool = typer.Option(
        False,
        "--debug",
        help="Enable detailed debug output and logging.",
    ),
):
    """Developer CLI Toolkit."""

    setup_logging(debug=debug)

    logger = get_logger()

    command = " ".join(["devkit"] + ctx.args)

    logger.info(
        "Executing command: %s",
        command,
    )

    ctx.ensure_object(dict)

    ctx.obj["debug"] = debug

    if ctx.invoked_subcommand is None:
        run_interactive_menu()


@app.command()
def hello():
    """Test whether DevKit is working."""
    console.print("[bold green]DevKit is working! 🚀[/bold green]")


@app.command()
def version():
    """Show the installed DevKit version."""
    console.print("[bold]Developer CLI Toolkit[/bold]")
    from devkit.version import VERSION

    console.print(f"Version: {VERSION}")


if __name__ == "__main__":
    app()
