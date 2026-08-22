from pathlib import Path

import typer

from devkit.services.git_service import (
    get_changed_files,
    get_current_branch,
    get_git_health,
    get_local_branches,
    get_recent_commits,
    get_remotes,
    get_repository_summary,
    get_status_summary,
    get_sync_status,
    is_git_repository,
)
from devkit.terminal.components import (
    error,
    section_title,
    success,
    warning,
)
from devkit.terminal.progress import score_bar
from devkit.terminal.status import status_badge
from devkit.terminal.tables import (
    create_key_value_table,
    create_table,
)
from devkit.terminal.theme import console

git_app = typer.Typer(help="Inspect and work with Git repositories.")


def require_git_repository() -> Path:
    """Validate that the current directory belongs to a Git repository."""

    path = Path.cwd()

    if not is_git_repository(path):
        error("This directory is not inside a Git repository.")

        console.print(
            "[devkit.secondary]"
            "Run this command from inside a Git project."
            "[/devkit.secondary]"
        )

        raise typer.Exit(code=1)

    return path


@git_app.command("status")
def git_status():
    """Show a clean summary of Git working-tree changes."""

    path = require_git_repository()

    data = get_status_summary(path)

    branch = get_current_branch(path) or "Unknown"

    section_title(
        "🌿 Git Status",
        path.name,
    )

    table = create_key_value_table(title="Working Tree")

    table.add_row(
        "Branch",
        branch,
    )

    table.add_row(
        "Staged",
        str(data["staged"]),
    )

    table.add_row(
        "Modified",
        str(data["modified"]),
    )

    table.add_row(
        "Untracked",
        str(data["untracked"]),
    )

    table.add_row(
        "Deleted",
        str(data["deleted"]),
    )

    console.print(table)

    if data["clean"]:
        console.print()

        success("Working tree is clean.")


@git_app.command("changes")
def git_changes():
    """Show changed files in the working tree."""

    path = require_git_repository()

    changes = get_changed_files(path)

    section_title(
        "🌿 Changed Files",
        path.name,
    )

    if not changes:
        success("No changed files.")
        return

    table = create_table(title="Changed Files")

    table.add_column(
        "Status",
        style="yellow",
    )

    table.add_column(
        "File",
        style="cyan",
    )

    for change in changes:
        table.add_row(
            change["status"],
            change["file"],
        )

    console.print(table)


@git_app.command("branches")
def git_branches():
    """List local Git branches."""

    path = require_git_repository()

    branches = get_local_branches(path)

    section_title(
        "🌿 Local Branches",
        path.name,
    )

    if not branches:
        warning("No local branches found.")
        return

    table = create_table(title="Branches")

    table.add_column(
        "Branch",
        style="cyan",
    )

    table.add_column(
        "Current",
        justify="center",
    )

    for branch in branches:
        table.add_row(
            branch["name"],
            ("[green]✓[/green]" if branch["current"] else ""),
        )

    console.print(table)


@git_app.command("log")
def git_log(
    limit: int = typer.Option(
        10,
        "--limit",
        "-l",
        min=1,
        max=100,
        help="Number of commits to display.",
    ),
):
    """Display recent Git commits."""

    path = require_git_repository()

    commits = get_recent_commits(
        path,
        limit=limit,
    )

    section_title(
        "🌿 Recent Commits",
        path.name,
    )

    if not commits:
        warning("No commits found.")
        return

    table = create_table(title=f"Recent Commits · {len(commits)}")

    table.add_column(
        "Hash",
        style="cyan",
    )

    table.add_column(
        "Author",
    )

    table.add_column(
        "When",
    )

    table.add_column(
        "Message",
    )

    for commit in commits:
        table.add_row(
            commit["hash"],
            commit["author"],
            commit["when"],
            commit["message"],
        )

    console.print(table)


@git_app.command("summary")
def git_summary():
    """Display a high-level Git repository summary."""

    path = require_git_repository()

    data = get_repository_summary(path)

    section_title(
        "🌿 Repository Summary",
        path.name,
    )

    table = create_key_value_table(title="Repository")

    table.add_row(
        "Repository Root",
        data["root"],
    )

    table.add_row(
        "Branch",
        data["branch"],
    )

    table.add_row(
        "Commits",
        str(data["commit_count"]),
    )

    table.add_row(
        "Origin",
        data["origin"],
    )

    table.add_row(
        "Latest Commit",
        data["latest_commit"],
    )

    table.add_row(
        "Working Tree",
        (
            "[green]Clean[/green]"
            if data["clean"]
            else "[yellow]Changes detected[/yellow]"
        ),
    )

    console.print(table)


@git_app.command("remote")
def git_remote():
    """Display Git remote configuration."""

    path = require_git_repository()

    remotes = get_remotes(path)

    section_title(
        "🌿 Git Remotes",
        path.name,
    )

    if not remotes:
        warning("No Git remotes configured.")
        return

    table = create_table(title="Git Remotes")

    table.add_column(
        "Name",
        style="cyan",
    )

    table.add_column(
        "URL",
    )

    table.add_column(
        "Type",
        style="dim",
    )

    for remote in remotes:
        table.add_row(
            remote["name"],
            remote["url"],
            remote["type"],
        )

    console.print(table)


@git_app.command("sync")
def git_sync():
    """Show local branch synchronization status."""

    path = require_git_repository()

    data = get_sync_status(path)

    section_title(
        "🌿 Git Sync Status",
        data["branch"],
    )

    if not data["upstream"]:
        warning("No upstream tracking branch configured.")
        return

    table = create_key_value_table(title="Synchronization")

    table.add_row(
        "Local Branch",
        data["branch"],
    )

    table.add_row(
        "Upstream",
        data["upstream"],
    )

    table.add_row(
        "Ahead",
        str(data["ahead"]),
    )

    table.add_row(
        "Behind",
        str(data["behind"]),
    )

    console.print(table)

    state = data["state"]

    console.print()

    if state == "synced":
        success("Branch is synchronized.")

    elif state == "ahead":
        warning(f'Local branch has {data["ahead"]} unpushed commit(s).')

    elif state == "behind":
        warning(f'Local branch is behind by {data["behind"]} commit(s).')

    elif state == "diverged":
        warning("Local and remote branches have diverged.")

    else:
        warning("Unable to determine synchronization state.")


@git_app.command("health")
def git_health():
    """Check Git repository configuration and health."""

    path = require_git_repository()

    data = get_git_health(path)

    score = data["score"]

    section_title(
        "🌿 Git Health",
        path.name,
    )

    console.print(f"{score_bar(score)} " f"[bold]{score}/100[/bold]\n")

    table = create_table(title="Repository Checks")

    table.add_column(
        "Check",
    )

    table.add_column(
        "Status",
        justify="center",
    )

    table.add_column(
        "Details",
        style="cyan",
    )

    for check in data["checks"]:
        table.add_row(
            check["name"],
            status_badge("healthy" if check["ok"] else "attention"),
            check["details"],
        )

    console.print(table)
