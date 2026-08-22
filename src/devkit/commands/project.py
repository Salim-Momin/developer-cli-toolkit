from collections import Counter
from pathlib import Path

import typer
from rich.console import Console
from rich.tree import Tree

from devkit.core.config import get_tree_defaults
from devkit.services.project_service import (
    analyze_project,
    count_tree_nodes,
    list_project_tree,
)
from devkit.terminal.components import (
    section_title,
    success,
)
from devkit.terminal.progress import score_bar
from devkit.terminal.status import status_badge, yes_no
from devkit.terminal.tables import create_key_value_table, create_table

project_app = typer.Typer(help="Inspect and analyze development projects.")

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
    if (path / "vite.config.js").exists() or (path / "vite.config.ts").exists():
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
    if (path / "pyproject.toml").exists() or (path / "requirements.txt").exists():
        return "Python"

    # Generic Node.js
    if (path / "package.json").exists():
        package_content = (
            (path / "package.json")
            .read_text(
                encoding="utf-8",
                errors="ignore",
            )
            .lower()
        )

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
            (path / "requirements.txt").exists() or (path / "pyproject.toml").exists()
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

    has_tests = any((path / directory).exists() for directory in test_directories)

    return {
        "README": ((path / "README.md").exists() or (path / "README.rst").exists()),
        ".gitignore": (path / ".gitignore").exists(),
        "Tests": has_tests,
        "Environment Template": (
            (path / ".env.example").exists() or (path / ".env.sample").exists()
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
            recommendations.append(
                "Add a .env.example file for required environment variables."
            )
        elif item == "Docker":
            recommendations.append(
                "Consider adding Docker support if deployment needs it."
            )
        elif item == "Git Repository":
            recommendations.append("Initialize a Git repository.")

    return score, recommendations


def build_score_bar(score: int, width: int = 20) -> str:
    """Create a simple Rich-compatible project health bar."""

    filled = round((score / 100) * width)
    empty = width - filled

    return f"[green]{'█' * filled}[/green][dim]{'░' * empty}[/dim]"


@project_app.command("info")
def project_info():
    """Display information about the current project."""

    project_path = Path.cwd()

    data = analyze_project(project_path)

    section_title(
        "📦 Project Information",
        data["name"],
    )

    table = create_key_value_table(title="Project Overview")

    table.add_row(
        "Name",
        data["name"],
    )

    table.add_row(
        "Path",
        data["path"],
    )

    table.add_row(
        "Type",
        data["type"],
    )

    table.add_row(
        "Primary Language",
        data["primary_language"],
    )

    table.add_row(
        "Project Size",
        format_size(data["size_bytes"]),
    )

    table.add_row(
        "Files",
        str(data["file_count"]),
    )

    table.add_row(
        "Directories",
        str(data["directory_count"]),
    )

    for item, detected in data["health_items"].items():
        table.add_row(
            item,
            yes_no(detected),
        )

    console.print(table)


@project_app.command("stats")
def project_stats():
    """Display project language and file statistics."""

    project_path = Path.cwd()

    data = analyze_project(project_path)

    section_title(
        "📊 Project Statistics",
        data["name"],
    )

    language_table = create_table(title="Language Statistics")

    language_table.add_column(
        "Language",
        style="cyan",
    )

    language_table.add_column(
        "Files",
        justify="right",
    )

    for language, count in data["language_stats"].most_common():
        language_table.add_row(
            language,
            str(count),
        )

    console.print(language_table)

    extension_table = create_table(title="Top File Extensions")

    extension_table.add_column(
        "Extension",
        style="cyan",
    )

    extension_table.add_column(
        "Files",
        justify="right",
    )

    for extension, count in data["extension_stats"].most_common(10):
        extension_table.add_row(
            extension,
            str(count),
        )

    console.print()
    console.print(extension_table)


@project_app.command("health")
def project_health():
    """Analyze project health and best practices."""

    project_path = Path.cwd()

    data = analyze_project(project_path)

    score = data["health_score"]

    section_title(
        "❤️ Project Health",
        data["name"],
    )

    console.print(f"{score_bar(score)} " f"[bold]{score}/100[/bold]\n")

    table = create_table(title="Project Health Checks")

    table.add_column("Check")

    table.add_column(
        "Status",
        justify="center",
    )

    for item, detected in data["health_items"].items():
        table.add_row(
            item,
            status_badge("pass" if detected else "warning"),
        )

    console.print(table)

    recommendations = data["recommendations"]

    if recommendations:
        console.print("\n[devkit.warning]" "Recommendations" "[/devkit.warning]")

        for recommendation in recommendations:
            console.print(f"  • {recommendation}")

    else:
        console.print()
        success("No major project health issues detected.")


def render_tree_node(
    node: dict,
    rich_tree: Tree,
) -> None:
    """Render service tree data with Rich."""

    for child in node.get(
        "children",
        [],
    ):
        if child["type"] == "directory":
            branch = rich_tree.add(f"[bold cyan]📁 {child['name']}[/bold cyan]")

            render_tree_node(
                child,
                branch,
            )

        else:
            rich_tree.add(f"📄 {child['name']}")


@project_app.command("tree")
def project_tree(
    depth: int | None = typer.Option(
        None,
        "--depth",
        "-d",
        help="Maximum tree depth.",
        min=1,
        max=10,
    ),
    files: bool | None = typer.Option(
        None,
        "--files/--no-files",
        help="Show or hide files.",
    ),
    hidden: bool | None = typer.Option(
        None,
        "--hidden/--no-hidden",
        help="Show or hide hidden files.",
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

    # Load defaults from .devkit.toml
    defaults = get_tree_defaults(project_path)

    resolved_depth = (
        depth
        if depth is not None
        else int(
            defaults.get(
                "depth",
                3,
            )
        )
    )

    resolved_files = (
        files
        if files is not None
        else bool(
            defaults.get(
                "show_files",
                True,
            )
        )
    )

    resolved_hidden = (
        hidden
        if hidden is not None
        else bool(
            defaults.get(
                "show_hidden",
                False,
            )
        )
    )

    section_title(
        "🌳 Project Tree",
        project_path.name,
    )

    # Generate plain tree data using Project Service
    tree_data = list_project_tree(
        path=project_path,
        max_depth=resolved_depth,
        show_files=resolved_files,
        show_hidden=resolved_hidden,
        extension_filter=extension,
    )

    # Render it using Rich
    root = Tree(f"[bold green]📦 {project_path.name}[/bold green]")

    render_tree_node(
        tree_data,
        root,
    )

    console.print(root)

    # Calculate summary
    file_count, directory_count = count_tree_nodes(tree_data)

    # Root project folder shouldn't count as child directory
    directory_count = max(
        0,
        directory_count - 1,
    )

    console.print(
        f"\n[devkit.secondary]"
        f"Summary: "
        f"{directory_count} directories, "
        f"{file_count} files"
        f"[/devkit.secondary]"
    )
