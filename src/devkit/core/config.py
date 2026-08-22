from copy import deepcopy
from pathlib import Path

try:
    import tomllib
except ImportError:
    tomllib = None


CONFIG_FILENAME = ".devkit.toml"


DEFAULT_CONFIG = {
    "project": {
        "ignore": [
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
        ],
    },
    "tree": {
        "depth": 3,
        "show_files": True,
        "show_hidden": False,
    },
    "search": {
        "limit": 50,
        "case_sensitive": False,
    },
    "api": {
        "timeout": 10.0,
        "history_limit": 100,
    },
}


def get_config_path(
    start_path: Path | None = None,
) -> Path | None:
    """Search current directory and parents for .devkit.toml."""

    current = (start_path or Path.cwd()).resolve()

    for directory in [
        current,
        *current.parents,
    ]:
        candidate = directory / CONFIG_FILENAME

        if candidate.exists():
            return candidate

    return None


def deep_merge(
    base: dict,
    override: dict,
) -> dict:
    """Recursively merge configuration dictionaries."""

    result = deepcopy(base)

    for key, value in override.items():
        if (
            key in result
            and isinstance(
                result[key],
                dict,
            )
            and isinstance(
                value,
                dict,
            )
        ):
            result[key] = deep_merge(
                result[key],
                value,
            )

        else:
            result[key] = value

    return result


def load_config(
    start_path: Path | None = None,
) -> dict:
    """Load DevKit configuration with defaults."""

    config = deepcopy(DEFAULT_CONFIG)

    config_path = get_config_path(start_path)

    if not config_path:
        return config

    if tomllib is None:
        raise RuntimeError("TOML configuration requires Python 3.11 or newer.")

    try:
        with config_path.open("rb") as file:
            user_config = tomllib.load(file)

    except (
        OSError,
        tomllib.TOMLDecodeError,
    ) as exc:
        raise ValueError(f"Could not read {config_path}: {exc}") from exc

    return deep_merge(
        config,
        user_config,
    )


def get_ignored_directories(
    start_path: Path | None = None,
) -> set[str]:
    """Return configured ignored directories."""

    config = load_config(start_path)

    values = config.get(
        "project",
        {},
    ).get(
        "ignore",
        [],
    )

    return {str(value) for value in values}


def get_tree_defaults(
    start_path: Path | None = None,
) -> dict:
    """Return default tree settings."""

    config = load_config(start_path)

    return config.get(
        "tree",
        {},
    )


def get_search_defaults(
    start_path: Path | None = None,
) -> dict:
    """Return default search settings."""

    config = load_config(start_path)

    return config.get(
        "search",
        {},
    )


def get_api_defaults(
    start_path: Path | None = None,
) -> dict:
    """Return default API settings."""

    config = load_config(start_path)

    return config.get(
        "api",
        {},
    )
