from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

search_app = typer.Typer(
    help="Search files and source code inside the current project."
)

console = Console()

IGNORED_DIRECTORIES = {
    ".git",
    ".venv",
    "venv",
    "env",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "node_modules",
    ".next",
    ".nuxt",
    ".cache",
    "coverage",
    "htmlcov",
    "dist",
    "build",
    "target",
}

def should_ignore(path: Path) -> bool:
    """Return True when the path belongs to an ignored directory."""

    return any(
        part in IGNORED_DIRECTORIES
        for part in path.parts
    )

def normalize_extension(extension: str | None) -> str | None:
    """Normalize extension filters such as py -> .py."""

    if not extension:
        return None

    extension = extension.lower()

    if not extension.startswith("."):
        extension = f".{extension}"

    return extension

def search_project(
    root: Path,
    query: str,
    extension: str | None = None,
    case_sensitive: bool = False,
) -> list[dict]:
    """Search text inside files in the current project."""

    results = []

    extension = normalize_extension(extension)

    search_query = query if case_sensitive else query.lower()

    for file_path in root.rglob("*"):
        if should_ignore(file_path):
            continue

        if not file_path.is_file():
            continue

        if extension and file_path.suffix.lower() != extension:
            continue

        try:
            content = file_path.read_text(
                encoding="utf-8",
                errors="ignore",
            )
        except (PermissionError, OSError):
            continue

        for line_number, line in enumerate(
            content.splitlines(),
            start=1,
        ):
            searchable_line = line if case_sensitive else line.lower()

            if search_query in searchable_line:
                results.append(
                    {
                        "file": file_path,
                        "line": line_number,
                        "text": line.strip(),
                    }
                )

    return results

@search_app.command("text")
def search_text(
    query: str = typer.Argument(
        ...,
        help="Text to search for.",
    ),
    extension: str | None = typer.Option(
        None,
        "--ext",
        "-e",
        help="Only search files with this extension.",
    ),
    case_sensitive: bool = typer.Option(
        False,
        "--case-sensitive",
        "-c",
        help="Enable case-sensitive searching.",
    ),
    limit: int = typer.Option(
        50,
        "--limit",
        "-l",
        help="Maximum number of results to display.",
        min=1,
        max=500,
    ),
):
    """Search for text inside project files."""

    project_path = Path.cwd()

    console.print(
        f'\n[bold cyan]Searching for:[/bold cyan] "{query}"'
    )

    results = search_project(
        root=project_path,
        query=query,
        extension=extension,
        case_sensitive=case_sensitive,
    )

    if not results:
        console.print(
            "\n[yellow]No matching text found.[/yellow]"
        )
        return

    table = Table(
        title=f"Search Results ({len(results)} matches)",
    )

    table.add_column("File", style="cyan")
    table.add_column("Line", justify="right")
    table.add_column("Match")

    for result in results[:limit]:
        relative_path = result["file"].relative_to(project_path)

        text = result["text"]

        if len(text) > 100:
            text = text[:97] + "..."

        table.add_row(
            str(relative_path),
            str(result["line"]),
            text,
        )

    console.print(table)

    if len(results) > limit:
        console.print(
            f"\n[dim]Showing {limit} of {len(results)} matches.[/dim]"
        )