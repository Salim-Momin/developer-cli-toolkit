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

from devkit.terminal.components import (
    build_menu_table,
    section_title,
    show_banner,
)
from devkit.terminal.theme import console

def show_menu() -> None:
    """Display the main DevKit command menu."""

    console.print(
        "[devkit.secondary]PROJECT[/devkit.secondary]"
    )

    project_table = build_menu_table()

    project_table.add_row(
        "1",
        "Project Information",
    )

    project_table.add_row(
        "2",
        "Project Statistics",
    )

    project_table.add_row(
        "3",
        "Project Health",
    )

    project_table.add_row(
        "4",
        "Project Tree",
    )

    console.print(project_table)

    console.print()
    console.print(
        "[devkit.secondary]DEVELOPER TOOLS[/devkit.secondary]"
    )

    tools_table = build_menu_table()

    tools_table.add_row(
        "5",
        "Smart Search",
    )

    tools_table.add_row(
        "6",
        "Environment Doctor",
    )

    tools_table.add_row(
        "7",
        "Git Toolkit",
    )

    console.print(tools_table)

    console.print()
    console.print(
        "[devkit.secondary]COMING SOON[/devkit.secondary]"
    )

    future_table = build_menu_table()

    future_table.add_row(
        "8",
        "[dim]API Tester[/dim]",
    )

    future_table.add_row(
        "9",
        "[dim]AI Assistant[/dim]",
    )

    console.print(future_table)

    console.print()

    exit_table = build_menu_table()

    exit_table.add_row(
        "0",
        "Exit",
    )

    console.print(exit_table)

def run_interactive_menu() -> None:
    """Run the interactive DevKit command center."""

    while True:
        console.clear()

        show_banner()
        show_menu()

        console.print()

        choice = typer.prompt(
            "\nChoose a command"
        )

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
            console.clear()

            section_title(
                "🌿 Git Toolkit",
                "Inspect repository state, history and synchronization.",
            )

            git_table = build_menu_table()

            git_table.add_row("1", "Repository Status")
            git_table.add_row("2", "Changed Files")
            git_table.add_row("3", "Local Branches")
            git_table.add_row("4", "Recent Commits")
            git_table.add_row("5", "Repository Summary")
            git_table.add_row("6", "Remote Information")
            git_table.add_row("7", "Sync Status")
            git_table.add_row("8", "Git Health")
            git_table.add_row("0", "Back")

            console.print(git_table)

            git_choice = typer.prompt(
                "\nChoose Git command"
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
                    "[devkit.error]✗ Invalid Git option.[/devkit.error]"
                )
        elif choice in {"8", "9"}:
            console.print(
                "[yellow]⚠ This feature is coming in a future milestone.[/yellow]"
            )       

        elif choice == "0":
            console.print(
                "\n[devkit.success]"
                "✓ DevKit session closed."
                "[/devkit.success]\n"
            )
            break

        else:
            console.print(
                "[devkit.error]"
                "✗ Invalid option. Choose one of the listed commands."
                "[/devkit.error]"
            )

        console.print()
        typer.prompt(
            "Press Enter to return to the menu",
            default="",
            show_default=False,
        )