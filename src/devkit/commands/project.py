from pathlib import Path
from collections import Counter

import typer
from rich.console import Console
from rich.table import Table


project_app = typer.Typer(
    help="Inspect and analyze development projects."
)

console = Console()

def detect_project_type(path: Path) -> str:
    """Detect the type of development project."""

    if (path / "next.config.js").exists():
        return "Next.js"

    if (path / "next.config.mjs").exists():
        return "Next.js"

    if (path / "next.config.ts").exists():
        return "Next.js"

    if (path / "vite.config.js").exists():
        return "Vite"

    if (path / "vite.config.ts").exists():
        return "Vite"

    if (path / "manage.py").exists():
        return "Django"

    if (path / "pyproject.toml").exists():
        return "Python"

    if (path / "requirements.txt").exists():
        return "Python"

    if (path / "package.json").exists():
        return "Node.js"

    return "Unknown"


def detect_technologies(path: Path) -> dict[str, bool]:
    """Detect common technologies used by the project."""

    return {
        "Git": (path / ".git").exists(),
        "Python": (
            (path / "requirements.txt").exists()
            or (path / "pyproject.toml").exists()
        ),
        "Node.js": (path / "package.json").exists(),
        "Docker": (
            (path / "Dockerfile").exists()
            or (path / "docker-compose.yml").exists()
            or (path / "compose.yml").exists()
        ),
    }

IGNORED_DIRECTORIES = {
    ".git",
    ".venv",
    "venv",
    "node_modules",
    "__pycache__",
    ".next",
    "dist",
    "build",
}

def count_project_items(path: Path) -> tuple[int, int]:
    """Count files and directories while ignoring generated folders."""

    file_count = 0
    directory_count = 0

    for item in path.rglob("*"):
        if any(part in IGNORED_DIRECTORIES for part in item.parts):
            continue

        if item.is_file():
            file_count += 1

        elif item.is_dir():
            directory_count += 1

    return file_count, directory_count

def get_file_extension_stats(path: Path) -> Counter:
    """Count file extensions in the project."""

    extensions = Counter()

    for item in path.rglob("*"):
        if any(part in IGNORED_DIRECTORIES for part in item.parts):
            continue

        if item.is_file():
            extension = item.suffix.lower()

            if extension:
                extensions[extension] += 1
            else:
                extensions["[no extension]"] += 1

    return extensions

LANGUAGE_MAP = {
    ".py": "Python",
    ".js": "JavaScript",
    ".jsx": "JavaScript",
    ".ts": "TypeScript",
    ".tsx": "TypeScript",
    ".html": "HTML",
    ".css": "CSS",
    ".scss": "SCSS",
    ".java": "Java",
    ".cpp": "C++",
    ".c": "C",
    ".cs": "C#",
    ".go": "Go",
    ".rs": "Rust",
    ".php": "PHP",
    ".rb": "Ruby",
    ".sql": "SQL",
    ".json": "JSON",
    ".yaml": "YAML",
    ".yml": "YAML",
    ".md": "Markdown",
}

def get_language_stats(extension_stats: Counter) -> Counter:
    """Convert extension statistics into language statistics."""

    languages = Counter()

    for extension, count in extension_stats.items():
        language = LANGUAGE_MAP.get(extension)

        if language:
            languages[language] += count

    return languages

@project_app.command("info")
def project_info():
    """Display information about the current project."""

    project_path = Path.cwd()

    project_type = detect_project_type(project_path)
    technologies = detect_technologies(project_path)

    file_count, directory_count = count_project_items(project_path)

    table = Table(
        title="Project Information",
        show_header=False,
    )

    table.add_column("Property", style="bold cyan")
    table.add_column("Value")

    table.add_row("Name", project_path.name)
    table.add_row("Path", str(project_path))
    table.add_row("Type", project_type)
    table.add_row("Files", str(file_count))
    table.add_row("Directories", str(directory_count))

    for technology, detected in technologies.items():
        status = "[green]Yes[/green]" if detected else "[red]No[/red]"
        table.add_row(technology, status)

    console.print(table)


@project_app.command("stats")
def project_stats():
    """Display project file and language statistics."""

    project_path = Path.cwd()

    extension_stats = get_file_extension_stats(project_path)
    language_stats = get_language_stats(extension_stats)

    console.print(
        f"\n[bold]Project:[/bold] {project_path.name}\n"
    )

    language_table = Table(title="Language Statistics")

    language_table.add_column("Language", style="bold cyan")
    language_table.add_column("Files", justify="right")

    for language, count in language_stats.most_common():
        language_table.add_row(language, str(count))

    console.print(language_table)

    extension_table = Table(title="Top File Extensions")

    extension_table.add_column("Extension", style="bold magenta")
    extension_table.add_column("Files", justify="right")

    for extension, count in extension_stats.most_common(10):
        extension_table.add_row(extension, str(count))

    console.print(extension_table)