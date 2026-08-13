from collections import Counter
from pathlib import Path


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


def detect_project_type(path: Path) -> str:
    if (
        (path / "next.config.js").exists()
        or (path / "next.config.mjs").exists()
        or (path / "next.config.ts").exists()
    ):
        return "Next.js"

    if (
        (path / "vite.config.js").exists()
        or (path / "vite.config.ts").exists()
    ):
        package_json = path / "package.json"

        if package_json.exists():
            content = package_json.read_text(
                encoding="utf-8-sig",
                errors="ignore",
            ).lower()

            if "react" in content:
                return "React + Vite"

        return "Vite"

    if (path / "manage.py").exists():
        return "Django"

    python_content = ""

    for file in [
        path / "requirements.txt",
        path / "pyproject.toml",
    ]:
        if file.exists():
            python_content += file.read_text(
                encoding="utf-8-sig",
                errors="ignore",
            ).lower()

    if "fastapi" in python_content:
        return "FastAPI"

    if "flask" in python_content:
        return "Flask"

    if "django" in python_content:
        return "Django"

    if (
        (path / "pyproject.toml").exists()
        or (path / "requirements.txt").exists()
    ):
        return "Python"

    if (path / "package.json").exists():
        content = (path / "package.json").read_text(
            encoding="utf-8-sig",
            errors="ignore",
        ).lower()

        if "react" in content:
            return "React"

        return "Node.js"

    return "Unknown"

def count_project_items(
    path: Path,
) -> tuple[int, int]:
    file_count = 0
    directory_count = 0

    for item in path.rglob("*"):
        if any(
            part in IGNORED_DIRECTORIES
            for part in item.parts
        ):
            continue

        if item.is_file():
            file_count += 1

        elif item.is_dir():
            directory_count += 1

    return file_count, directory_count

def get_file_extension_stats(
    path: Path,
) -> Counter:
    extensions = Counter()

    for item in path.rglob("*"):
        if any(
            part in IGNORED_DIRECTORIES
            for part in item.parts
        ):
            continue

        if item.is_file():
            extension = item.suffix.lower()

            extensions[
                extension or "[no extension]"
            ] += 1

    return extensions

def get_language_stats(
    extension_stats: Counter,
) -> Counter:
    languages = Counter()

    for extension, count in extension_stats.items():
        language = LANGUAGE_MAP.get(
            extension
        )

        if language:
            languages[language] += count

    return languages

def get_primary_language(
    path: Path,
) -> str:
    extensions = get_file_extension_stats(
        path
    )

    languages = get_language_stats(
        extensions
    )

    if not languages:
        return "Unknown"

    return languages.most_common(1)[0][0]

def get_project_size(
    path: Path,
) -> int:
    total_size = 0

    for item in path.rglob("*"):
        if any(
            part in IGNORED_DIRECTORIES
            for part in item.parts
        ):
            continue

        if item.is_file():
            try:
                total_size += item.stat().st_size
            except OSError:
                pass

    return total_size

def format_size(
    size_bytes: int,
) -> str:
    units = [
        "B",
        "KB",
        "MB",
        "GB",
        "TB",
    ]

    size = float(size_bytes)

    for unit in units:
        if size < 1024:
            return f"{size:.2f} {unit}"

        size /= 1024

    return f"{size:.2f} PB"

def detect_project_health_items(
    path: Path,
) -> dict[str, bool]:
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
        ".gitignore": (
            path / ".gitignore"
        ).exists(),
        "Tests": has_tests,
        "Environment Template": (
            (path / ".env.example").exists()
            or (path / ".env.sample").exists()
        ),
        "Docker": (
            (path / "Dockerfile").exists()
            or (
                path
                / "docker-compose.yml"
            ).exists()
            or (
                path
                / "compose.yml"
            ).exists()
        ),
        "Git Repository": (
            path / ".git"
        ).exists(),
    }

def calculate_health_score(
    health_items: dict[str, bool],
) -> tuple[int, list[str]]:
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
            score += weights.get(
                item,
                0,
            )
            continue

        if item == "README":
            recommendations.append(
                "Add a README with setup and usage instructions."
            )

        elif item == ".gitignore":
            recommendations.append(
                "Add a .gitignore file."
            )

        elif item == "Tests":
            recommendations.append(
                "Add automated tests."
            )

        elif item == "Environment Template":
            recommendations.append(
                "Add a .env.example file."
            )

        elif item == "Docker":
            recommendations.append(
                "Consider Docker support if deployment requires it."
            )

        elif item == "Git Repository":
            recommendations.append(
                "Initialize a Git repository."
            )

    return score, recommendations

def analyze_project(
    path: Path,
) -> dict:
    """Return complete project analysis data."""

    file_count, directory_count = (
        count_project_items(path)
    )

    extension_stats = (
        get_file_extension_stats(path)
    )

    language_stats = (
        get_language_stats(
            extension_stats
        )
    )

    health_items = (
        detect_project_health_items(
            path
        )
    )

    health_score, recommendations = (
        calculate_health_score(
            health_items
        )
    )

    return {
        "name": path.name,
        "path": str(path),
        "type": detect_project_type(
            path
        ),
        "primary_language": (
            get_primary_language(
                path
            )
        ),
        "size_bytes": (
            get_project_size(
                path
            )
        ),
        "file_count": file_count,
        "directory_count": (
            directory_count
        ),
        "extension_stats": (
            extension_stats
        ),
        "language_stats": (
            language_stats
        ),
        "health_items": (
            health_items
        ),
        "health_score": (
            health_score
        ),
        "recommendations": (
            recommendations
        ),
    }

def list_project_tree(
    path: Path,
    current_depth: int = 0,
    max_depth: int = 3,
    show_files: bool = True,
    show_hidden: bool = False,
    extension_filter: str | None = None,
) -> dict:
    """Return project tree data as plain Python structures."""

    node = {
        "name": path.name,
        "type": "directory",
        "children": [],
    }

    if current_depth >= max_depth:
        return node

    try:
        items = sorted(
            path.iterdir(),
            key=lambda item: (
                item.is_file(),
                item.name.lower(),
            ),
        )

    except (
        PermissionError,
        OSError,
    ):
        return node

    normalized_extension = None

    if extension_filter:
        normalized_extension = (
            extension_filter.lower()
        )

        if not normalized_extension.startswith("."):
            normalized_extension = (
                f".{normalized_extension}"
            )

    for item in items:
        if item.name in IGNORED_DIRECTORIES:
            continue

        if (
            not show_hidden
            and item.name.startswith(".")
        ):
            continue

        if item.is_dir():
            child = list_project_tree(
                path=item,
                current_depth=current_depth + 1,
                max_depth=max_depth,
                show_files=show_files,
                show_hidden=show_hidden,
                extension_filter=extension_filter,
            )

            node["children"].append(
                child
            )

        elif show_files:
            if (
                normalized_extension
                and item.suffix.lower()
                != normalized_extension
            ):
                continue

            node["children"].append(
                {
                    "name": item.name,
                    "type": "file",
                    "children": [],
                }
            )

    return node    

def count_tree_nodes(
    node: dict,
) -> tuple[int, int]:
    """Count files and directories in tree data."""

    files = 0
    directories = 0

    if node["type"] == "file":
        return 1, 0

    directories += 1

    for child in node.get(
        "children",
        [],
    ):
        child_files, child_directories = (
            count_tree_nodes(
                child
            )
        )

        files += child_files
        directories += child_directories

    return files, directories