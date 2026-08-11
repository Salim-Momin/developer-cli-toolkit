import shutil
import subprocess

import typer
from rich.console import Console
from rich.table import Table

console = Console()

def run_command(command: list[str]) -> str | None:
    """Run a command safely and return its output."""

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=5,
            shell=False,
        )

        output = result.stdout.strip() or result.stderr.strip()

        if result.returncode != 0:
            return None

        return output

    except (
        FileNotFoundError,
        subprocess.TimeoutExpired,
        OSError,
    ):
        return None

def first_line(value: str | None) -> str:
    """Return only the first line of command output."""

    if not value:
        return "Unknown"

    return value.splitlines()[0].strip()    

TOOLS = [
    {
        "name": "Python",
        "executables": ["python", "python3"],
        "version_command": ["python", "--version"],
    },
    {
        "name": "pip",
        "executables": ["pip", "pip3"],
        "version_command": ["pip", "--version"],
    },
    {
        "name": "Node.js",
        "executables": ["node"],
        "version_command": ["node", "--version"],
    },
    {
        "name": "npm",
        "executables": ["npm"],
        "version_command": ["npm", "--version"],
    },
    {
        "name": "Git",
        "executables": ["git"],
        "version_command": ["git", "--version"],
    },
    {
        "name": "Docker",
        "executables": ["docker"],
        "version_command": ["docker", "--version"],
    },
    {
        "name": "Java",
        "executables": ["java"],
        "version_command": ["java", "--version"],
    },
    {
        "name": "PostgreSQL",
        "executables": ["psql"],
        "version_command": ["psql", "--version"],
    },
    {
        "name": "VS Code",
        "executables": ["code"],
        "version_command": ["code", "--version"],
    },
    {
        "name": "GitHub CLI",
        "executables": ["gh"],
        "version_command": ["gh", "--version"],
    },
]

def find_executable(executables: list[str]) -> str | None:
    """Return the first executable found on PATH."""

    for executable in executables:
        if shutil.which(executable):
            return executable

    return None

def inspect_tools() -> list[dict]:
    """Inspect installed development tools."""

    results = []

    for tool in TOOLS:
        executable = find_executable(tool["executables"])

        if not executable:
            results.append(
                {
                    "name": tool["name"],
                    "installed": False,
                    "version": "-",
                    "path": "-",
                }
            )
            continue

        version_command = list(tool["version_command"])
        version_command[0] = executable

        version = first_line(
            run_command(version_command)
        )

        results.append(
            {
                "name": tool["name"],
                "installed": True,
                "version": version,
                "path": shutil.which(executable) or "-",
            }
        )

    return results    

def calculate_environment_score(results: list[dict]) -> int:
    """Calculate a simple environment readiness score."""

    if not results:
        return 0

    installed_count = sum(
        1 for result in results if result["installed"]
    )

    return round(
        (installed_count / len(results)) * 100
    )

def build_environment_bar(
    score: int,
    width: int = 20,
) -> str:
    """Build a Rich-compatible environment score bar."""

    filled = round((score / 100) * width)
    empty = width - filled

    return (
        f"[green]{'█' * filled}[/green]"
        f"[dim]{'░' * empty}[/dim]"
    )

def doctor():
    """Inspect the local development environment."""

    console.print(
        "\n[bold cyan]🩺 DevKit Environment Doctor[/bold cyan]\n"
    )

    with console.status(
        "[cyan]Checking development tools...[/cyan]"
    ):
        results = inspect_tools()

    score = calculate_environment_score(results)

    console.print(
        f"{build_environment_bar(score)} "
        f"[bold]{score}%[/bold]\n"
    )

    table = Table(
        title="Development Environment",
    )

    table.add_column(
        "Tool",
        style="bold",
    )

    table.add_column(
        "Status",
        justify="center",
    )

    table.add_column(
        "Version",
        style="cyan",
    )

    for result in results:
        status = (
            "[green]✓ Installed[/green]"
            if result["installed"]
            else "[yellow]⚠ Missing[/yellow]"
        )

        table.add_row(
            result["name"],
            status,
            result["version"],
        )

    console.print(table)

    missing = [
        result["name"]
        for result in results
        if not result["installed"]
    ]

    if missing:
        console.print(
            "\n[bold yellow]Missing tools[/bold yellow]"
        )

        for tool in missing:
            console.print(
                f"  • {tool}"
            )
    else:
        console.print(
            "\n[bold green]"
            "✓ All checked development tools are available."
            "[/bold green]"
        )    