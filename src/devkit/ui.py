import typer

from devkit.commands.api import (
    api_delete,
    api_get,
    api_patch,
    api_post,
    api_put,
)

from devkit.commands.doctor import doctor

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

from devkit.commands.project import (
    project_health,
    project_info,
    project_stats,
    project_tree,
)

from devkit.commands.search import search_text

from devkit.terminal.components import (
    build_menu_table,
    footer_hint,
    section_title,
    show_banner,
)

from devkit.terminal.theme import console


def show_menu() -> None:
    """Display the main DevKit interactive menu."""

    console.print(
        "[devkit.secondary]PROJECT[/devkit.secondary]"
    )

    project_table = build_menu_table()

    project_table.add_row(
        "1",
        "🔍 Project Information",
    )

    project_table.add_row(
        "2",
        "📊 Project Statistics",
    )

    project_table.add_row(
        "3",
        "❤️ Project Health",
    )

    project_table.add_row(
        "4",
        "🌳 Project Tree",
    )

    console.print(project_table)

    # -----------------------------------------------------
    # Developer Tools
    # -----------------------------------------------------

    console.print()

    console.print(
        "[devkit.secondary]"
        "DEVELOPER TOOLS"
        "[/devkit.secondary]"
    )

    tools_table = build_menu_table()

    tools_table.add_row(
        "5",
        "🔎 Smart Search",
    )

    tools_table.add_row(
        "6",
        "🩺 Environment Doctor",
    )

    tools_table.add_row(
        "7",
        "🌿 Git Toolkit",
    )

    tools_table.add_row(
        "8",
        "🌐 API Tester",
    )

    console.print(tools_table)

    # -----------------------------------------------------
    # Coming Soon
    # -----------------------------------------------------

    console.print()

    console.print(
        "[devkit.secondary]"
        "COMING SOON"
        "[/devkit.secondary]"
    )

    future_table = build_menu_table()

    future_table.add_row(
        "9",
        "[dim]🤖 AI Assistant[/dim]",
    )

    console.print(future_table)

    # -----------------------------------------------------
    # Exit
    # -----------------------------------------------------

    console.print()

    exit_table = build_menu_table()

    exit_table.add_row(
        "0",
        "❌ Exit",
    )

    console.print(exit_table)


def run_search_menu() -> None:
    """Run Smart Search interactively."""

    console.clear()

    section_title(
        "🔎 Smart Search",
        "Search source code and filenames inside the current project.",
    )

    query = typer.prompt(
        "Search query"
    )

    console.print()

    console.print("1  Text Search")
    console.print("2  Filename Search")
    console.print("0  Back")

    mode = typer.prompt(
        "\nChoose search mode"
    )

    if mode == "0":
        return

    if mode not in {"1", "2"}:
        console.print(
            "[devkit.error]"
            "✗ Invalid search mode."
            "[/devkit.error]"
        )
        return

    extension = typer.prompt(
        "File extension filter (optional)",
        default="",
        show_default=False,
    )

    use_regex = False

    if mode == "1":
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
        filename=mode == "2",
        limit=50,
    )


def run_git_menu() -> None:
    """Run Git Toolkit submenu."""

    console.clear()

    section_title(
        "🌿 Git Toolkit",
        "Inspect repository state, history, remotes and synchronization.",
    )

    git_table = build_menu_table()

    git_table.add_row(
        "1",
        "Repository Status",
    )

    git_table.add_row(
        "2",
        "Changed Files",
    )

    git_table.add_row(
        "3",
        "Local Branches",
    )

    git_table.add_row(
        "4",
        "Recent Commits",
    )

    git_table.add_row(
        "5",
        "Repository Summary",
    )

    git_table.add_row(
        "6",
        "Remote Information",
    )

    git_table.add_row(
        "7",
        "Sync Status",
    )

    git_table.add_row(
        "8",
        "Git Health",
    )

    git_table.add_row(
        "0",
        "Back",
    )

    console.print(git_table)

    footer_hint(
        "Choose a Git tool · 0 to return"
    )

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
        git_log(
            limit=10
        )

    elif git_choice == "5":
        git_summary()

    elif git_choice == "6":
        git_remote()

    elif git_choice == "7":
        git_sync()

    elif git_choice == "8":
        git_health()

    elif git_choice == "0":
        return

    else:
        console.print(
            "[devkit.error]"
            "✗ Invalid Git option."
            "[/devkit.error]"
        )


def run_api_menu() -> None:
    """Run API Tester submenu."""

    console.clear()

    section_title(
        "🌐 API Tester",
        "Send and inspect HTTP requests from the terminal.",
    )

    api_table = build_menu_table()

    api_table.add_row(
        "1",
        "GET Request",
    )

    api_table.add_row(
        "2",
        "POST Request",
    )

    api_table.add_row(
        "3",
        "PUT Request",
    )

    api_table.add_row(
        "4",
        "PATCH Request",
    )

    api_table.add_row(
        "5",
        "DELETE Request",
    )

    api_table.add_row(
        "0",
        "Back",
    )

    console.print(api_table)

    footer_hint(
        "Choose an HTTP method · 0 to return"
    )

    api_choice = typer.prompt(
        "\nChoose HTTP method"
    )

    if api_choice == "0":
        return

    if api_choice not in {
        "1",
        "2",
        "3",
        "4",
        "5",
    }:
        console.print(
            "[devkit.error]"
            "✗ Invalid API option."
            "[/devkit.error]"
        )
        return

    url = typer.prompt(
        "Request URL"
    )

    # -----------------------------------------------------
    # GET
    # -----------------------------------------------------

    if api_choice == "1":
        api_get(
            url=url,
            header=None,
            timeout=10.0,
            param=None,
            save=None,
            show_headers=False,
        )

    # -----------------------------------------------------
    # POST
    # -----------------------------------------------------

    elif api_choice == "2":
        body = typer.prompt(
            "JSON body (optional)",
            default="",
            show_default=False,
        )

        api_post(
            url=url,
            json_body=body or None,
            header=None,
            timeout=10.0,
        )

    # -----------------------------------------------------
    # PUT
    # -----------------------------------------------------

    elif api_choice == "3":
        body = typer.prompt(
            "JSON body (optional)",
            default="",
            show_default=False,
        )

        api_put(
            url=url,
            json_body=body or None,
            header=None,
            timeout=10.0,
        )

    # -----------------------------------------------------
    # PATCH
    # -----------------------------------------------------

    elif api_choice == "4":
        body = typer.prompt(
            "JSON body (optional)",
            default="",
            show_default=False,
        )

        api_patch(
            url=url,
            json_body=body or None,
            header=None,
            timeout=10.0,
        )

    # -----------------------------------------------------
    # DELETE
    # -----------------------------------------------------

    elif api_choice == "5":
        api_delete(
            url=url,
            header=None,
            timeout=10.0,
        )


def pause_menu() -> None:
    """Pause before returning to the main menu."""

    console.print()

    typer.prompt(
        "Press Enter to return to the menu",
        default="",
        show_default=False,
    )


def run_interactive_menu() -> None:
    """Run the main interactive DevKit command center."""

    while True:
        console.clear()

        show_banner()
        show_menu()

        footer_hint(
            "Enter a number to run a command · 0 to exit"
        )

        choice = typer.prompt(
            "\nChoose a command"
        )

        # -----------------------------------------------------
        # Project Information
        # -----------------------------------------------------

        if choice == "1":
            console.clear()

            project_info()

            pause_menu()

        # -----------------------------------------------------
        # Project Statistics
        # -----------------------------------------------------

        elif choice == "2":
            console.clear()

            project_stats()

            pause_menu()

        # -----------------------------------------------------
        # Project Health
        # -----------------------------------------------------

        elif choice == "3":
            console.clear()

            project_health()

            pause_menu()

        # -----------------------------------------------------
        # Project Tree
        # -----------------------------------------------------

        elif choice == "4":
            console.clear()

            project_tree(
                depth=3,
                files=True,
                hidden=False,
                extension=None,
            )

            pause_menu()

        # -----------------------------------------------------
        # Smart Search
        # -----------------------------------------------------

        elif choice == "5":
            run_search_menu()

            pause_menu()

        # -----------------------------------------------------
        # Environment Doctor
        # -----------------------------------------------------

        elif choice == "6":
            console.clear()

            doctor()

            pause_menu()

        # -----------------------------------------------------
        # Git Toolkit
        # -----------------------------------------------------

        elif choice == "7":
            run_git_menu()

            pause_menu()

        # -----------------------------------------------------
        # API Tester
        # -----------------------------------------------------

        elif choice == "8":
            run_api_menu()

            pause_menu()

        # -----------------------------------------------------
        # AI Assistant
        # -----------------------------------------------------

        elif choice == "9":
            console.clear()

            section_title(
                "🤖 AI Assistant",
                "AI developer tools will be added in a later milestone.",
            )

            console.print(
                "[devkit.warning]"
                "⚠ AI Assistant is not available yet."
                "[/devkit.warning]"
            )

            pause_menu()

        # -----------------------------------------------------
        # Exit
        # -----------------------------------------------------

        elif choice == "0":
            console.clear()

            console.print(
                "\n[devkit.success]"
                "✓ DevKit session closed."
                "[/devkit.success]\n"
            )

            break

        # -----------------------------------------------------
        # Invalid
        # -----------------------------------------------------

        else:
            console.print(
                "\n[devkit.error]"
                "✗ Invalid option. "
                "Choose one of the listed commands."
                "[/devkit.error]"
            )

            pause_menu()