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

def get_tracking_branch(
    path: Path,
) -> str | None:
    """Return the upstream tracking branch."""

    return run_git_command(
        [
            "rev-parse",
            "--abbrev-ref",
            "--symbolic-full-name",
            "@{upstream}",
        ],
        cwd=path,
    )

def get_ahead_behind(
    path: Path,
    upstream: str,
) -> tuple[int, int]:
    """Return ahead and behind counts against upstream."""

    output = run_git_command(
        [
            "rev-list",
            "--left-right",
            "--count",
            f"HEAD...{upstream}",
        ],
        cwd=path,
    )

    if not output:
        return 0, 0

    parts = output.split()

    if len(parts) != 2:
        return 0, 0

    try:
        ahead = int(parts[0])
        behind = int(parts[1])
    except ValueError:
        return 0, 0

    return ahead, behind

def collect_git_health(
    path: Path,
) -> list[dict]:
    """Collect repository health checks."""

    checks = []

    branch = run_git_command(
        ["branch", "--show-current"],
        cwd=path,
    )

    checks.append(
        {
            "name": "Current Branch",
            "ok": bool(branch),
            "details": branch or "Detached HEAD",
        }
    )

    origin = run_git_command(
        ["remote", "get-url", "origin"],
        cwd=path,
    )

    checks.append(
        {
            "name": "Origin Remote",
            "ok": bool(origin),
            "details": origin or "Not configured",
        }
    )

    upstream = get_tracking_branch(path)

    checks.append(
        {
            "name": "Tracking Branch",
            "ok": bool(upstream),
            "details": upstream or "Not configured",
        }
    )

    username = run_git_command(
        ["config", "user.name"],
        cwd=path,
    ) or run_git_command(
        ["config", "--global", "user.name"],
        cwd=path,
    )

    email = run_git_command(
        ["config", "user.email"],
        cwd=path,
    ) or run_git_command(
        ["config", "--global", "user.email"],
        cwd=path,
    )

    identity_ok = bool(username and email)

    checks.append(
        {
            "name": "Git Identity",
            "ok": identity_ok,
            "details": (
                f"{username} <{email}>"
                if identity_ok
                else "Name or email missing"
            ),
        }
    )

    status = run_git_command(
        ["status", "--porcelain"],
        cwd=path,
    ) or ""

    checks.append(
        {
            "name": "Working Tree",
            "ok": not bool(status.strip()),
            "details": (
                "Clean"
                if not status.strip()
                else "Uncommitted changes detected"
            ),
        }
    )

    return checks

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

@git_app.command("changes")
def git_changes():
    """Show changed files in the working tree."""

    path = require_git_repository()

    output = run_git_command(
        ["status", "--short"],
        cwd=path,
    ) or ""

    if not output:
        console.print(
            "\n[bold green]✓ No changed files.[/bold green]"
        )
        return

    table = Table(
        title="Changed Files"
    )

    table.add_column("Status", style="yellow")
    table.add_column("File", style="cyan")

    for line in output.splitlines():
        if len(line) < 3:
            continue

        status = line[:2].strip() or "-"
        file_name = line[3:].strip()

        table.add_row(
            status,
            file_name,
        )

    console.print()
    console.print(table)    

@git_app.command("remote")
def git_remote():
    """Display Git remote configuration."""

    path = require_git_repository()

    output = run_git_command(
        ["remote", "-v"],
        cwd=path,
    )

    if not output:
        console.print(
            "\n[yellow]No Git remotes configured.[/yellow]"
        )
        return

    table = Table(
        title="Git Remotes"
    )

    table.add_column("Name", style="cyan")
    table.add_column("URL")
    table.add_column("Type", style="dim")

    for line in output.splitlines():
        parts = line.split()

        if len(parts) < 3:
            continue

        name = parts[0]
        url = parts[1]
        remote_type = parts[2].strip("()")

        table.add_row(
            name,
            url,
            remote_type,
        )

    console.print()
    console.print(table)

@git_app.command("sync")
def git_sync():
    """Show local branch synchronization status."""

    path = require_git_repository()

    branch = run_git_command(
        ["branch", "--show-current"],
        cwd=path,
    ) or "Unknown"

    upstream = get_tracking_branch(path)

    console.print(
        f"\n[bold cyan]Git Sync Status — {branch}[/bold cyan]\n"
    )

    if not upstream:
        console.print(
            "[yellow]⚠ No upstream tracking branch configured.[/yellow]"
        )
        return

    ahead, behind = get_ahead_behind(
        path,
        upstream,
    )

    table = Table(show_header=False)

    table.add_column("Property", style="bold")
    table.add_column("Value")

    table.add_row("Local Branch", branch)
    table.add_row("Upstream", upstream)
    table.add_row("Ahead", str(ahead))
    table.add_row("Behind", str(behind))

    console.print(table)

    if ahead == 0 and behind == 0:
        console.print(
            "\n[bold green]✓ Branch is synchronized.[/bold green]"
        )

    elif ahead > 0 and behind == 0:
        console.print(
            f"\n[yellow]Local branch has {ahead} unpushed commit(s).[/yellow]"
        )

    elif behind > 0 and ahead == 0:
        console.print(
            f"\n[yellow]Local branch is behind by {behind} commit(s).[/yellow]"
        )

    else:
        console.print(
            "\n[yellow]Local and remote branches have diverged.[/yellow]"
        )

@git_app.command("health")
def git_health():
    """Check Git repository configuration and health."""

    path = require_git_repository()

    checks = collect_git_health(path)

    score = round(
        (
            sum(1 for check in checks if check["ok"])
            / len(checks)
        )
        * 100
    )

    console.print(
        f"\n[bold cyan]Git Health — {path.name}[/bold cyan]\n"
    )

    console.print(
        f"[bold]{score}/100[/bold]\n"
    )

    table = Table(
        title="Repository Checks"
    )

    table.add_column("Check", style="bold")
    table.add_column("Status", justify="center")
    table.add_column("Details", style="cyan")

    for check in checks:
        status = (
            "[green]✓ Healthy[/green]"
            if check["ok"]
            else "[yellow]⚠ Attention[/yellow]"
        )

        table.add_row(
            check["name"],
            status,
            check["details"],
        )

    console.print(table)        