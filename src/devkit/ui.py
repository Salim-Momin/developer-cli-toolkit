import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from devkit.commands.project import (
    project_info,
    project_stats,
    project_health,
    project_tree,
)

console = Console()


def show_banner() -> None:
    """Display the DevKit banner."""

    console.print()

    console.print(
        Panel.fit(
            "[bold cyan]⚡ DEVKIT[/bold cyan]\n"
            "[dim]Developer Command Center[/dim]",
            border_style="cyan",
            padding=(1, 6),
        )
    )


def show_menu() -> None:
    """Display available DevKit tools."""

    table = Table(
        show_header=False,
        box=None,
        padding=(0, 2),
    )

    table.add_column("Number", style="bold cyan")
    table.add_column("Tool")

    table.add_row("1", "🔍 Project Information")
    table.add_row("2", "📊 Project Statistics")
    table.add_row("3", "❤️  Project Health")
    table.add_row("4", "🌳 Project Tree")

    table.add_row("5", "[dim]🔎 Smart Search — Coming Soon[/dim]")
    table.add_row("6", "[dim]🩺 Environment Doctor — Coming Soon[/dim]")
    table.add_row("7", "[dim]🌿 Git Tools — Coming Soon[/dim]")
    table.add_row("8", "[dim]🌐 API Tester — Coming Soon[/dim]")
    table.add_row("9", "[dim]🤖 AI Assistant — Coming Soon[/dim]")

    table.add_row("0", "❌ Exit")

    console.print(table)


def run_interactive_menu() -> None:
    """Run the interactive DevKit command center."""

    while True:
        console.clear()

        show_banner()
        show_menu()

        console.print()

        choice = typer.prompt("Select an option")

        console.print()

        if choice == "1":
            project_info()

        elif choice == "2":
            project_stats()

        elif choice == "3":
            project_health()

        elif choice == "4":
            project_tree(
                depth=3,
                files=True,
                hidden=False,
                extension=None,
            )

        elif choice in {"5", "6", "7", "8", "9"}:
            console.print(
                "[yellow]⚠ This feature is coming in a future milestone.[/yellow]"
            )

        elif choice == "0":
            console.print(
                "\n[bold green]Goodbye from DevKit! 👋[/bold green]\n"
            )
            break

        else:
            console.print(
                "[red]✗ Invalid option. Choose a number from the menu.[/red]"
            )

        console.print()
        typer.prompt(
            "Press Enter to return to the menu",
            default="",
            show_default=False,
        )