from pathlib import Path

import typer
import re
from rich.console import Console
from rich.table import Table
from rich.markup import escape
from devkit.terminal.components import section_title, loading
from devkit.terminal.tables import create_table

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
    regex: bool = False,
) -> list[dict]:
    """Search text inside project files."""

    results = []

    extension = normalize_extension(extension)

    flags = 0 if case_sensitive else re.IGNORECASE

    pattern = None

    if regex:
        try:
            pattern = re.compile(query, flags)
        except re.error as error:
            raise ValueError(f"Invalid regular expression: {error}") from error

    for file_path in root.rglob("*"):
        if should_ignore(file_path):
            continue

        if not file_path.is_file():
            continue

        if extension and file_path.suffix.lower() != extension:
            continue

        if is_binary_file(file_path):
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
            matched = False

            if regex and pattern:
                matched = bool(pattern.search(line))

            else:
                searchable_line = (
                    line if case_sensitive else line.lower()
                )

                search_query = (
                    query if case_sensitive else query.lower()
                )

                matched = search_query in searchable_line

            if matched:
                results.append(
                    {
                        "file": file_path,
                        "line": line_number,
                        "text": line.strip(),
                    }
                )

    return results

def is_binary_file(path: Path) -> bool:
    """Detect whether a file appears to be binary."""

    try:
        with path.open("rb") as file:
            chunk = file.read(1024)

        return b"\x00" in chunk

    except OSError:
        return True

def search_filenames(
    root: Path,
    query: str,
    case_sensitive: bool = False,
) -> list[Path]:
    """Search for files by filename."""

    results = []

    search_query = query if case_sensitive else query.lower()

    for path in root.rglob("*"):
        if should_ignore(path):
            continue

        if not path.is_file():
            continue

        filename = path.name if case_sensitive else path.name.lower()

        if search_query in filename:
            results.append(path)

    return results

def highlight_match(
    text: str,
    query: str,
    case_sensitive: bool = False,
) -> str:
    """Highlight matching text for Rich output."""

    safe_text = escape(text)

    flags = 0 if case_sensitive else re.IGNORECASE

    try:
        pattern = re.compile(re.escape(query), flags)

        return pattern.sub(
            lambda match: f"[bold yellow]{escape(match.group(0))}[/bold yellow]",
            safe_text,
        )

    except re.error:
        return safe_text

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
    regex: bool = typer.Option(
        False,
        "--regex",
        "-r",
        help="Treat the query as a regular expression.",
    ),
    filename: bool = typer.Option(
        False,
        "--filename",
        "-f",
        help="Search filenames instead of file contents.",
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
    """Search project files and source code."""

    project_path = Path.cwd()

    if filename:
        results = search_filenames(
            root=project_path,
            query=query,
            case_sensitive=case_sensitive,
        )

        if not results:
            console.print(
                "\n[yellow]No matching filenames found.[/yellow]"
            )
            return

        table = Table(
            title=f"Filename Results ({len(results)} matches)"
        )

        table.add_column("File", style="cyan")

        for result in results[:limit]:
            table.add_row(
                str(result.relative_to(project_path))
            )

        console.print()
        console.print(table)

        return

    section_title(
        "🔎 Smart Search",
        f'Searching current project for "{query}"',
    )

    try:
        with loading(
            "Searching project..."
        ):
            results = search_project(
                root=project_path,
                query=query,
                extension=extension,
                case_sensitive=case_sensitive,
                regex=regex,
            )

    except ValueError as error:
        console.print(
            f"\n[bold red]Search error:[/bold red] {error}"
        )
        raise typer.Exit(code=1)

    if not results:
        console.print(
            "\n[yellow]No matching text found.[/yellow]"
        )
        return

    table = create_table(
        title=f"Search Results ({len(results)} matches)"
    )

    table.add_column("File", style="cyan")
    table.add_column("Line", justify="right")
    table.add_column("Match")

    for result in results[:limit]:
        relative_path = result["file"].relative_to(project_path)

        text = result["text"]

        if len(text) > 120:
            text = text[:117] + "..."

        if not regex:
            text = highlight_match(
                text=text,
                query=query,
                case_sensitive=case_sensitive,
            )
        else:
            text = escape(text)

        table.add_row(
            str(relative_path),
            str(result["line"]),
            text,
        )

    console.print()
    console.print(table)

    if len(results) > limit:
        console.print(
            f"\n[dim]Showing {limit} of "
            f"{len(results)} matches.[/dim]"
        )