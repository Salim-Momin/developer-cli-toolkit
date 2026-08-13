from devkit.services.doctor_service import analyze_environment
from devkit.terminal.components import (
    loading,
    section_title,
    success,
)
from devkit.terminal.progress import score_bar
from devkit.terminal.status import status_badge
from devkit.terminal.tables import create_table
from devkit.terminal.theme import console


def doctor():
    """Inspect the local development environment."""

    section_title(
        "🩺 Environment Doctor",
        "Inspect installed developer tools and environment health.",
    )

    with loading(
        "Checking development environment..."
    ):
        data = analyze_environment()

    score = data["score"]
    tools = data["tools"]
    diagnostics = data["diagnostics"]
    recommendations = data["recommendations"]

    console.print(
        f"{score_bar(score)} "
        f"[bold]{score}/100[/bold]\n"
    )

    # -----------------------------------------------------
    # Development Tools
    # -----------------------------------------------------

    tools_table = create_table(
        title="Development Environment"
    )

    tools_table.add_column(
        "Tool",
        style="bold",
    )

    tools_table.add_column(
        "Status",
        justify="center",
    )

    tools_table.add_column(
        "Version",
        style="cyan",
    )

    tools_table.add_column(
        "Path",
        style="dim",
    )

    for tool in tools:
        tools_table.add_row(
            tool["name"],
            status_badge(
                "installed"
                if tool["installed"]
                else "missing"
            ),
            tool["version"],
            tool["path"],
        )

    console.print(
        tools_table
    )

    # -----------------------------------------------------
    # Diagnostics
    # -----------------------------------------------------

    diagnostics_table = create_table(
        title="Environment Diagnostics"
    )

    diagnostics_table.add_column(
        "Check",
        style="bold",
    )

    diagnostics_table.add_column(
        "Status",
        justify="center",
    )

    diagnostics_table.add_column(
        "Details",
        style="cyan",
    )

    for diagnostic in diagnostics:
        diagnostics_table.add_row(
            diagnostic["check"],
            status_badge(
                "healthy"
                if diagnostic["ok"]
                else "attention"
            ),
            diagnostic["details"],
        )

    console.print()
    console.print(
        diagnostics_table
    )

    # -----------------------------------------------------
    # Recommendations
    # -----------------------------------------------------

    if recommendations:
        console.print(
            "\n[devkit.warning]"
            "Recommendations"
            "[/devkit.warning]"
        )

        for recommendation in recommendations:
            console.print(
                f"  • {recommendation}"
            )

    else:
        console.print()

        success(
            "Development environment looks healthy."
        )