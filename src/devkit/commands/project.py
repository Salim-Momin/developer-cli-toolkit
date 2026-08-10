import os
from pathlib import Path
from collections import Counter
from rich.tree import Tree

import typer
from rich.console import Console
from rich.table import Table


project_app = typer.Typer(
    help="Inspect and analyze development projects."
)

console = Console()

def detect_project_type(path: Path) -> str:
    """Detect the primary project framework or runtime."""

    # Next.js
    if (
        (path / "next.config.js").exists()
        or (path / "next.config.mjs").exists()
        or (path / "next.config.ts").exists()
    ):
        return "Next.js"

    # Vite / React
    if (
        (path / "vite.config.js").exists()
        or (path / "vite.config.ts").exists()
    ):
        package_json = path / "package.json"

        if package_json.exists():
            content = package_json.read_text(
                encoding="utf-8",
                errors="ignore",
            ).lower()

            if "react" in content:
                return "React + Vite"

        return "Vite"

    # Django
    if (path / "manage.py").exists():
        return "Django"

    # Python dependency/config detection
    dependency_files = [
        path / "requirements.txt",
        path / "pyproject.toml",
    ]

    python_content = ""

    for file in dependency_files:
        if file.exists():
            python_content += file.read_text(
                encoding="utf-8",
                errors="ignore",
            ).lower()

    if "fastapi" in python_content:
        return "FastAPI"

    if "flask" in python_content:
        return "Flask"

    if "django" in python_content:
        return "Django"

    # Generic Python
    if (
        (path / "pyproject.toml").exists()
        or (path / "requirements.txt").exists()
    ):
        return "Python"

    # Generic Node.js
    if (path / "package.json").exists():
        package_content = (path / "package.json").read_text(
            encoding="utf-8",
            errors="ignore",
        ).lower()

        if "react" in package_content:
            return "React"

        return "Node.js"

    return "Unknown"

def detect_project_files(path: Path) -> list[str]:
    """Detect important configuration and dependency files."""

    important_files = [
        "pyproject.toml",
        "requirements.txt",
        "package.json",
        "package-lock.json",
        "pnpm-lock.yaml",
        "yarn.lock",
        "Dockerfile",
        "docker-compose.yml",
        "compose.yml",
        ".env",
        ".env.example",
        "README.md",
        "manage.py",
        "next.config.js",
        "next.config.mjs",
        "next.config.ts",
        "vite.config.js",
        "vite.config.ts",
    ]

    detected = []

    for filename in important_files:
        if (path / filename).exists():
            detected.append(filename)

    return detected

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

def get_project_size(path: Path) -> int:
    """Return total project size in bytes, ignoring generated directories."""

    total_size = 0

    for item in path.rglob("*"):
        if any(part in IGNORED_DIRECTORIES for part in item.parts):
            continue

        if item.is_file():
            try:
                total_size += item.stat().st_size
            except OSError:
                pass

    return total_size

def format_size(size_bytes: int) -> str:
    """Convert bytes into a human-readable size."""

    units = ["B", "KB", "MB", "GB"]

    size = float(size_bytes)

    for unit in units:
        if size < 1024:
            return f"{size:.2f} {unit}"

        size /= 1024

    return f"{size:.2f} TB"

def get_primary_language(path: Path) -> str:
    """Return the most common programming language in the project."""

    extension_stats = get_file_extension_stats(path)
    language_stats = get_language_stats(extension_stats)

    if not language_stats:
        return "Unknown"

    return language_stats.most_common(1)[0][0]

def detect_project_health_items(path: Path) -> dict[str, bool]:
    """Detect common project quality indicators."""

    test_directories = [
        "tests",
        "test",
        "__tests__",
    ]

    has_tests = any(
        (path / directory).exists()
        for directory in test_directories
    )

    return {
        "README": (
            (path / "README.md").exists()
            or (path / "README.rst").exists()
        ),
        ".gitignore": (path / ".gitignore").exists(),
        "Tests": has_tests,
        "Environment Template": (
            (path / ".env.example").exists()
            or (path / ".env.sample").exists()
        ),
        "Docker": (
            (path / "Dockerfile").exists()
            or (path / "docker-compose.yml").exists()
            or (path / "compose.yml").exists()
        ),
        "Git Repository": (path / ".git").exists(),
    }

def calculate_health_score(health_items: dict[str, bool]) -> tuple[int, list[str]]:
    """Calculate a basic project health score and recommendations."""

    weights = {
        "README": 15,
        ".gitignore": 15,
        "Tests": 30,
        "Environment Template": 15,
        "Docker": 5,
        "Git Repository": 20,
    }

    score = 0
    recommendations = []

    for item, detected in health_items.items():
        if detected:
            score += weights.get(item, 0)
            continue

        if item == "README":
            recommendations.append("Add a README with setup and usage instructions.")
        elif item == ".gitignore":
            recommendations.append("Add a .gitignore file.")
        elif item == "Tests":
            recommendations.append("Add automated tests.")
        elif item == "Environment Template":
            recommendations.append("Add a .env.example file for required environment variables.")
        elif item == "Docker":
            recommendations.append("Consider adding Docker support if deployment needs it.")
        elif item == "Git Repository":
            recommendations.append("Initialize a Git repository.")

    return score, recommendations

def build_score_bar(score: int, width: int = 20) -> str:
    """Create a simple Rich-compatible project health bar."""

    filled = round((score / 100) * width)
    empty = width - filled

    return f"[green]{'█' * filled}[/green][dim]{'░' * empty}[/dim]"

def build_project_tree(
    path: Path,
    tree: Tree,
    current_depth: int = 0,
    max_depth: int = 3,
    show_files: bool = True,
    show_hidden: bool = False,
    extension_filter: str | None = None,
) -> tuple[int, int]:
    """Recursively build a Rich project tree."""

    if current_depth >= max_depth:
        return 0, 0

    file_count = 0
    directory_count = 0

    try:
        items = sorted(
            path.iterdir(),
            key=lambda item: (
                item.is_file(),
                item.name.lower(),
            ),
        )
    except (PermissionError, OSError):
        return 0, 0

    for item in items:
        if item.name in IGNORED_DIRECTORIES:
            continue

        if not show_hidden and item.name.startswith("."):
            continue

        if item.is_dir():
            directory_count += 1

            branch = tree.add(
                f"[bold cyan]📁 {item.name}[/bold cyan]"
            )

            child_files, child_dirs = build_project_tree(
                path=item,
                tree=branch,
                current_depth=current_depth + 1,
                max_depth=max_depth,
                show_files=show_files,
                show_hidden=show_hidden,
                extension_filter=extension_filter,
            )

            file_count += child_files
            directory_count += child_dirs

        elif show_files:
            if extension_filter:
                normalized_extension = extension_filter.lower()

                if not normalized_extension.startswith("."):
                    normalized_extension = f".{normalized_extension}"

                if item.suffix.lower() != normalized_extension:
                    continue

            file_count += 1
            tree.add(f"📄 {item.name}")

    return file_count, directory_count

@project_app.command("info")
def project_info():
    """Display information about the current project."""

    project_path = Path.cwd()

    project_type = detect_project_type(project_path)
    technologies = detect_technologies(project_path)
    project_files = detect_project_files(project_path)
    project_size = get_project_size(project_path)
    primary_language = get_primary_language(project_path)
    health_items = detect_project_health_items(project_path)

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
    table.add_row("Primary Language", primary_language)
    table.add_row("Project Size", format_size(project_size))
    table.add_row("Files", str(file_count))
    table.add_row("Directories", str(directory_count))

    for technology, detected in technologies.items():
        status = "[green]Yes[/green]" if detected else "[red]No[/red]"
        table.add_row(technology, status)

    for item, detected in health_items.items():
        status = "[green]Yes[/green]" if detected else "[yellow]No[/yellow]"
        table.add_row(item, status)

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

@project_app.command("health")
def project_health():
    """Analyze basic project health and best-practice indicators."""

    project_path = Path.cwd()

    health_items = detect_project_health_items(project_path)
    score, recommendations = calculate_health_score(health_items)

    console.print(
        f"\n[bold cyan]Project Health — {project_path.name}[/bold cyan]\n"
    )

    console.print(
        f"{build_score_bar(score)} [bold]{score}/100[/bold]\n"
    )

    table = Table(
        title="Health Checks",
        show_header=True,
    )

    table.add_column("Check", style="bold")
    table.add_column("Status", justify="center")

    for item, detected in health_items.items():
        status = "[green]✓ Pass[/green]" if detected else "[yellow]⚠ Missing[/yellow]"
        table.add_row(item, status)

    console.print(table)

    if recommendations:
        console.print("\n[bold yellow]Recommendations[/bold yellow]")

        for recommendation in recommendations:
            console.print(f"  • {recommendation}")

    else:
        console.print(
            "\n[bold green]✓ No major project health issues detected.[/bold green]"
        )

@project_app.command("tree")
def project_tree(
    depth: int = typer.Option(
        3,
        "--depth",
        "-d",
        help="Maximum tree depth.",
        min=1,
        max=10,
    ),
    files: bool = typer.Option(
        True,
        "--files/--no-files",
        help="Show or hide files.",
    ),
    hidden: bool = typer.Option(
        False,
        "--hidden",
        help="Include hidden files and folders.",
    ),
    extension: str | None = typer.Option(
        None,
        "--ext",
        "-e",
        help="Show only files with a specific extension.",
    ),
):
    """Display a clean project directory tree."""

    project_path = Path.cwd()

    root = Tree(
        f"[bold green]📦 {project_path.name}[/bold green]"
    )

    file_count, directory_count = build_project_tree(
        path=project_path,
        tree=root,
        max_depth=depth,
        show_files=files,
        show_hidden=hidden,
        extension_filter=extension,
    )

    console.print()
    console.print(root)

    console.print(
        f"\n[dim]Summary:[/dim] "
        f"[bold]{directory_count}[/bold] directories, "
        f"[bold]{file_count}[/bold] files"
    )