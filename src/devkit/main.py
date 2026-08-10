import typer
from rich.console import Console

app = typer.Typer(
    name="devkit",
    help="Developer CLI Toolkit — useful tools for developers.",
    no_args_is_help=True,
)

console = Console()


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