import subprocess
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

git_app = typer.Typer(
    help="Inspect and work with Git repositories."
)

console = Console()

def run_git_command(
    args: list[str],
    cwd: Path | None = None,
) -> str | None:
    """Run a Git command and return cleaned output."""

    try:
        result = subprocess.run(
            ["git", *args],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=10,
            shell=False,
        )

        if result.returncode != 0:
            return None

        return result.stdout.strip()

    except (
        FileNotFoundError,
        subprocess.TimeoutExpired,
        OSError,
    ):
        return None

def is_git_repository(path: Path) -> bool:
    """Return True if path is inside a Git repository."""

    result = run_git_command(
        ["rev-parse", "--is-inside-work-tree"],
        cwd=path,
    )

    return result == "true"    

def require_git_repository() -> Path:
    """Validate that the current folder belongs to a Git repository."""

    path = Path.cwd()

    if not is_git_repository(path):
        console.print(
            "\n[bold red]✗ Not a Git repository.[/bold red]"
        )
        console.print(
            "[dim]Run this command inside a Git project.[/dim]"
        )
        raise typer.Exit(code=1)

    return path    

@git_app.command("status")
def git_status():
    """Show a clean summary of Git working-tree changes."""

    path = require_git_repository()

    branch = run_git_command(
        ["branch", "--show-current"],
        cwd=path,
    ) or "Unknown"

    porcelain = run_git_command(
        ["status", "--porcelain"],
        cwd=path,
    ) or ""

    lines = [
        line
        for line in porcelain.splitlines()
        if line.strip()
    ]

    staged = 0
    modified = 0
    untracked = 0
    deleted = 0

    for line in lines:
        status = line[:2]

        if status == "??":
            untracked += 1
            continue

        if status[0] not in {" ", "?"}:
            staged += 1

        if status[1] == "M":
            modified += 1

        if "D" in status:
            deleted += 1

    console.print(
        f"\n[bold cyan]Git Status — {path.name}[/bold cyan]\n"
    )

    table = Table(show_header=False)

    table.add_column("Property", style="bold")
    table.add_column("Value")

    table.add_row("Branch", branch)
    table.add_row("Staged", str(staged))
    table.add_row("Modified", str(modified))
    table.add_row("Untracked", str(untracked))
    table.add_row("Deleted", str(deleted))

    console.print(table)

    if not lines:
        console.print(
            "\n[bold green]✓ Working tree is clean.[/bold green]"
        )

@git_app.command("branches")
def git_branches():
    """List local Git branches."""

    path = require_git_repository()

    output = run_git_command(
        [
            "for-each-ref",
            "--format=%(refname:short)|%(HEAD)",
            "refs/heads/",
        ],
        cwd=path,
    )

    if not output:
        console.print(
            "\n[yellow]No local branches found.[/yellow]"
        )
        return

    table = Table(
        title="Local Branches"
    )

    table.add_column("Branch", style="cyan")
    table.add_column("Current", justify="center")

    for line in output.splitlines():
        branch, marker = line.split("|", maxsplit=1)

        current = (
            "[green]✓[/green]"
            if marker == "*"
            else ""
        )

        table.add_row(
            branch,
            current,
        )

    console.print()
    console.print(table)        

@git_app.command("branches")
def git_branches():
    """List local Git branches."""

    path = require_git_repository()

    output = run_git_command(
        [
            "for-each-ref",
            "--format=%(refname:short)|%(HEAD)",
            "refs/heads/",
        ],
        cwd=path,
    )

    if not output:
        console.print(
            "\n[yellow]No local branches found.[/yellow]"
        )
        return

    table = Table(
        title="Local Branches"
    )

    table.add_column("Branch", style="cyan")
    table.add_column("Current", justify="center")

    for line in output.splitlines():
        branch, marker = line.split("|", maxsplit=1)

        current = (
            "[green]✓[/green]"
            if marker == "*"
            else ""
        )

        table.add_row(
            branch,
            current,
        )

    console.print()
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

    output = run_git_command(
        [
            "log",
            f"-{limit}",
            "--pretty=format:%h|%an|%ar|%s",
        ],
        cwd=path,
    )

    if not output:
        console.print(
            "\n[yellow]No commits found.[/yellow]"
        )
        return

    table = Table(
        title=f"Recent Commits ({limit})"
    )

    table.add_column("Hash", style="cyan")
    table.add_column("Author")
    table.add_column("When")
    table.add_column("Message")

    for line in output.splitlines():
        parts = line.split("|", maxsplit=3)

        if len(parts) != 4:
            continue

        commit_hash, author, when, message = parts

        table.add_row(
            commit_hash,
            author,
            when,
            message,
        )

    console.print()
    console.print(table)

@git_app.command("summary")
def git_summary():
    """Display a high-level Git repository summary."""

    path = require_git_repository()

    branch = run_git_command(
        ["branch", "--show-current"],
        cwd=path,
    ) or "Unknown"

    root = run_git_command(
        ["rev-parse", "--show-toplevel"],
        cwd=path,
    ) or str(path)

    remote = run_git_command(
        ["remote", "get-url", "origin"],
        cwd=path,
    ) or "Not configured"

    commit_count = run_git_command(
        ["rev-list", "--count", "HEAD"],
        cwd=path,
    ) or "0"

    latest_commit = run_git_command(
        [
            "log",
            "-1",
            "--pretty=format:%h - %s",
        ],
        cwd=path,
    ) or "No commits"

    porcelain = run_git_command(
        ["status", "--porcelain"],
        cwd=path,
    ) or ""

    clean = not bool(porcelain.strip())

    console.print(
        f"\n[bold cyan]Git Repository Summary — {path.name}[/bold cyan]\n"
    )

    table = Table(show_header=False)

    table.add_column("Property", style="bold")
    table.add_column("Value")

    table.add_row("Repository Root", root)
    table.add_row("Branch", branch)
    table.add_row("Commits", commit_count)
    table.add_row("Origin", remote)
    table.add_row("Latest Commit", latest_commit)

    table.add_row(
        "Working Tree",
        (
            "[green]Clean[/green]"
            if clean
            else "[yellow]Changes detected[/yellow]"
        ),
    )

    console.print(table)