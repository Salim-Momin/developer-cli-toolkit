import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from devkit.commands.search import search_text
from devkit.commands.doctor import doctor

from devkit.commands.project import (
    project_info,
    project_stats,
    project_health,
    project_tree,
)

from devkit.commands.git import (
    git_branches,
    git_changes,
    git_health,
    git_log,
    git_remote,
    git_status,
    git_summary,
    git_sync,
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

    table.add_row("5", "🔎 Smart Search")
    table.add_row("6", "🩺 Environment Doctor")
    table.add_row("7", "🌿 Git Tools")
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

        elif choice == "5":
            query = typer.prompt("Search query")

            mode = typer.prompt(
                "Search mode: text or filename",
                default="text",
            ).lower()

            extension = typer.prompt(
                "File extension filter (optional)",
                default="",
                show_default=False,
            )

            use_regex = False

            if mode == "text":
                regex_choice = typer.prompt(
                    "Use regex? y/n",
                    default="n",
                ).lower()

                use_regex = regex_choice == "y"

            search_text(
                query=query,
                extension=extension or None,
                case_sensitive=False,
                regex=use_regex,
                filename=mode == "filename",
                limit=50,
            )

        elif choice == "6":
            doctor()

        elif choice == "7":
            console.print(
                "\n[bold cyan]🌿 Git Tools[/bold cyan]\n"
            )

            console.print("1  Status")
            console.print("2  Changed Files")
            console.print("3  Branches")
            console.print("4  Recent Commits")
            console.print("5  Repository Summary")
            console.print("6  Remote Information")
            console.print("7  Sync Status")
            console.print("8  Git Health")
            console.print("0  Back")

            git_choice = typer.prompt(
                "\nSelect Git option"
            )

            if git_choice == "1":
                git_status()

            elif git_choice == "2":
                git_changes()

            elif git_choice == "3":
                git_branches()

            elif git_choice == "4":
                git_log(limit=10)

            elif git_choice == "5":
                git_summary()

            elif git_choice == "6":
                git_remote()

            elif git_choice == "7":
                git_sync()

            elif git_choice == "8":
                git_health()

            elif git_choice == "0":
                continue

            else:
                console.print(
                    "[red]✗ Invalid Git option.[/red]"
                )

        elif choice in {"8", "9"}:
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