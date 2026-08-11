import typer
from rich.console import Console
from devkit.commands.project import project_app
from devkit.ui import run_interactive_menu
from devkit.commands.search import search_text
from devkit.commands.doctor import doctor
from devkit.commands.git import git_app

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

app.command("search")(search_text)
app.command("doctor")(doctor)

@app.callback()
def main(ctx: typer.Context):
    """Developer CLI Toolkit."""

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
    console.print("Version: 0.1.0")


if __name__ == "__main__":
    app()