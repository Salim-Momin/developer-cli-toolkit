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
    """
    Display DevKit main interactive menu.
    """

    console.print(
        "[devkit.secondary]"
        "PROJECT"
        "[/devkit.secondary]"
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

    tools_table.add_row(
        "10",
        "📚 Command Reference",
    )


    console.print(tools_table)



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



    console.print()


    exit_table = build_menu_table()


    exit_table.add_row(
        "0",
        "❌ Exit",
    )


    console.print(exit_table)

def run_search_menu() -> None:
    """
    Run Smart Search interactively.
    """

    console.clear()

    section_title(
        "🔎 Smart Search",
        "Search source code and filenames inside the current project.",
    )

    query = typer.prompt(
        "Search query"
    )

    console.print()

    console.print(
        "1  Text Search"
    )

    console.print(
        "2  Filename Search"
    )

    console.print(
        "0  Back"
    )


    mode = typer.prompt(
        "\nChoose search mode"
    )


    if mode == "0":
        return


    if mode not in {
        "1",
        "2",
    }:
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


        use_regex = (
            regex_choice == "y"
        )


    search_text(
        query=query,
        extension=extension or None,
        case_sensitive=None,
        regex=use_regex,
        filename=mode == "2",
        limit=None,
    )



def run_git_menu() -> None:
    """
    Run Git Toolkit submenu.
    """

    console.clear()


    section_title(
        "🌿 Git Toolkit",
        "Inspect repository state, history, remotes and synchronization.",
    )


    git_table = build_menu_table()


    options = [
        ("1", "Repository Status"),
        ("2", "Changed Files"),
        ("3", "Local Branches"),
        ("4", "Recent Commits"),
        ("5", "Repository Summary"),
        ("6", "Remote Information"),
        ("7", "Sync Status"),
        ("8", "Git Health"),
        ("0", "Back"),
    ]


    for key, value in options:
        git_table.add_row(
            key,
            value,
        )


    console.print(
        git_table
    )


    footer_hint(
        "Choose a Git tool · 0 to return"
    )


    choice = typer.prompt(
        "\nChoose Git command"
    )


    if choice == "1":
        git_status()


    elif choice == "2":
        git_changes()


    elif choice == "3":
        git_branches()


    elif choice == "4":
        git_log(
            limit=10
        )


    elif choice == "5":
        git_summary()


    elif choice == "6":
        git_remote()


    elif choice == "7":
        git_sync()


    elif choice == "8":
        git_health()


    elif choice == "0":
        return


    else:
        console.print(
            "[devkit.error]"
            "✗ Invalid Git option."
            "[/devkit.error]"
        )



def run_api_menu() -> None:
    """
    Run API Tester submenu.
    """

    console.clear()


    section_title(
        "🌐 API Tester",
        "Send and inspect HTTP requests from terminal.",
    )


    api_table = build_menu_table()


    options = [
        ("1", "GET Request"),
        ("2", "POST Request"),
        ("3", "PUT Request"),
        ("4", "PATCH Request"),
        ("5", "DELETE Request"),
        ("0", "Back"),
    ]


    for key, value in options:
        api_table.add_row(
            key,
            value,
        )


    console.print(
        api_table
    )


    footer_hint(
        "Choose HTTP method · 0 to return"
    )


    choice = typer.prompt(
        "\nChoose HTTP method"
    )


    if choice == "0":
        return


    if choice not in {
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


    if choice == "1":

        api_get(
            url=url,
            header=None,
            timeout=10.0,
            param=None,
            save=None,
            show_headers=False,
        )


    elif choice == "2":

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


    elif choice == "3":

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


    elif choice == "4":

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


    elif choice == "5":

        api_delete(
            url=url,
            header=None,
            timeout=10.0,
        )



def pause_menu() -> None:
    """
    Pause before returning to menu.
    """

    console.print()

    typer.prompt(
        "Press Enter to return to menu",
        default="",
        show_default=False,
    )

def show_command_reference() -> None:
    """
    Display all DevKit commands.
    """

    console.clear()

    section_title(
        "📚 DevKit Command Reference",
        "All available commands grouped by tool.",
    )


    sections = {

        "PROJECT TOOLS": [
            "devkit project info",
            "devkit project stats",
            "devkit project health",
            "devkit project tree",
            "devkit project tree -d 2",
            "devkit project tree --no-files",
        ],


        "SMART SEARCH": [
            'devkit search "TODO"',
            'devkit search "import" -e py',
            'devkit search "project" -f',
            'devkit search "TODO|FIXME" -r',
        ],


        "ENVIRONMENT DOCTOR": [
            "devkit doctor",
        ],


        "GIT TOOLKIT": [
            "devkit git status",
            "devkit git changes",
            "devkit git branches",
            "devkit git log",
            "devkit git summary",
            "devkit git remote",
            "devkit git sync",
            "devkit git health",
        ],


        "JSON TOOLS": [
            "devkit json validate file.json",
            "devkit json format file.json",
            "devkit json minify file.json",
            "devkit json inspect file.json",
        ],


        "YAML TOOLS": [
            "devkit yaml validate file.yaml",
            "devkit yaml format file.yaml",
            "devkit yaml inspect file.yaml",
        ],


        "API TESTER": [
            "devkit api get URL",
            "devkit api post URL",
            "devkit api put URL",
            "devkit api patch URL",
            "devkit api delete URL",
        ],
    }


    for title, commands in sections.items():

        console.print(
            f"\n[devkit.primary]{title}[/devkit.primary]"
        )


        table = build_menu_table()


        for command in commands:

            table.add_row(
                "",
                command,
            )


        console.print(table)


    footer_hint(
        "Use --help after any command for more options."
    )



def run_interactive_menu() -> None:
    """
    Run DevKit command center.
    """

    while True:

        console.clear()

        show_banner()

        show_menu()


        footer_hint(
            "Enter number · h for help · q to quit"
        )


        choice = typer.prompt(
            "\nChoose a command",
            default="0",
        )


        # Help shortcut

        if choice.lower() == "h":

            show_command_reference()

            pause_menu()

            continue



        # Quit shortcut

        if choice.lower() == "q":

            break



        # Project Info

        if choice == "1":

            console.clear()

            project_info()

            pause_menu()



        elif choice == "2":

            console.clear()

            project_stats()

            pause_menu()



        elif choice == "3":

            console.clear()

            project_health()

            pause_menu()



        elif choice == "4":

            console.clear()

            project_tree(
                depth=None,
                files=None,
                hidden=None,
                extension=None,
            )

            pause_menu()



        elif choice == "5":

            run_search_menu()

            pause_menu()



        elif choice == "6":

            console.clear()

            doctor()

            pause_menu()



        elif choice == "7":

            run_git_menu()

            pause_menu()



        elif choice == "8":

            run_api_menu()

            pause_menu()



        elif choice == "9":

            console.clear()


            section_title(
                "🤖 AI Assistant",
                "Future DevKit AI features.",
            )


            console.print(
                "[devkit.warning]"
                "⚠ AI Assistant is planned for a future milestone."
                "[/devkit.warning]"
            )


            pause_menu()



        elif choice == "10":

            show_command_reference()

            pause_menu()



        elif choice == "0":

            console.clear()

            console.print(
                "\n[devkit.success]"
                "✓ DevKit session closed."
                "[/devkit.success]\n"
            )

            break



        else:

            console.print(
                "[devkit.error]"
                "✗ Invalid option."
                "[/devkit.error]"
            )

            pause_menu()