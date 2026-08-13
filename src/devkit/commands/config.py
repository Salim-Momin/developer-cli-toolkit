from pathlib import Path

import typer

from devkit.core.config import (
    CONFIG_FILENAME,
    DEFAULT_CONFIG,
    get_config_path,
    load_config,
)
from devkit.terminal.components import (
    error,
    section_title,
    success,
    warning,
)
from devkit.terminal.tables import (
    create_key_value_table,
)
from devkit.terminal.theme import console


config_app = typer.Typer(
    help="Manage DevKit configuration."
)


def build_default_config_text() -> str:
    """Return the default .devkit.toml content."""

    ignored = DEFAULT_CONFIG[
        "project"
    ]["ignore"]

    ignored_lines = ",\n".join(
        f'    "{name}"'
        for name in ignored
    )

    return f"""[project]

ignore = [
{ignored_lines}
]


[tree]

depth = 3
show_files = true
show_hidden = false


[search]

limit = 50
case_sensitive = false


[api]

timeout = 10.0
history_limit = 100
"""

@config_app.command("init")
def config_init(
    force: bool = typer.Option(
        False,
        "--force",
        "-f",
        help="Overwrite an existing configuration file.",
    ),
):
    """Create a default .devkit.toml in the current directory."""

    path = (
        Path.cwd()
        / CONFIG_FILENAME
    )

    if path.exists() and not force:
        warning(
            f"{CONFIG_FILENAME} already exists."
        )

        console.print(
            "[devkit.secondary]"
            "Use --force to replace it."
            "[/devkit.secondary]"
        )

        raise typer.Exit(
            code=1
        )

    try:
        path.write_text(
            build_default_config_text(),
            encoding="utf-8",
        )

    except OSError as exc:
        error(
            f"Could not create configuration: {exc}"
        )

        raise typer.Exit(
            code=1
        )

    success(
        f"Created {path}."
    )

@config_app.command("show")
def config_show():
    """Display the effective DevKit configuration."""

    try:
        config = load_config()

    except (
        ValueError,
        RuntimeError,
    ) as exc:
        error(
            str(exc)
        )
        raise typer.Exit(
            code=1
        )

    config_path = get_config_path()

    section_title(
        "⚙ DevKit Configuration",
        (
            str(config_path)
            if config_path
            else "Using built-in defaults"
        ),
    )

    project_table = create_key_value_table(
        title="Project"
    )

    project_table.add_row(
        "Ignored Directories",
        ", ".join(
            config["project"]["ignore"]
        ),
    )

    console.print(
        project_table
    )

    tree_table = create_key_value_table(
        title="Tree"
    )

    tree_table.add_row(
        "Depth",
        str(
            config["tree"]["depth"]
        ),
    )

    tree_table.add_row(
        "Show Files",
        str(
            config["tree"]["show_files"]
        ),
    )

    tree_table.add_row(
        "Show Hidden",
        str(
            config["tree"]["show_hidden"]
        ),
    )

    console.print()
    console.print(
        tree_table
    )

    search_table = create_key_value_table(
        title="Search"
    )

    search_table.add_row(
        "Limit",
        str(
            config["search"]["limit"]
        ),
    )

    search_table.add_row(
        "Case Sensitive",
        str(
            config["search"]["case_sensitive"]
        ),
    )

    console.print()
    console.print(
        search_table
    )

    api_table = create_key_value_table(
        title="API"
    )

    api_table.add_row(
        "Timeout",
        str(
            config["api"]["timeout"]
        ),
    )

    api_table.add_row(
        "History Limit",
        str(
            config["api"]["history_limit"]
        ),
    )

    console.print()
    console.print(
        api_table
    )    