from pathlib import Path

import typer
import yaml
from rich.syntax import Syntax
from rich.table import Table

from devkit.terminal.components import (
    error,
    section_title,
    success,
)
from devkit.terminal.theme import console


yaml_app = typer.Typer(
    help="Validate, format and inspect YAML files."
)

def load_yaml_file(path: Path):
    """Safely load and parse a YAML file."""

    if not path.exists():
        error(f"File not found: {path}")
        raise typer.Exit(code=1)

    if not path.is_file():
        error(f"Path is not a file: {path}")
        raise typer.Exit(code=1)

    try:
        content = path.read_text(
            encoding="utf-8-sig"
        )

    except (PermissionError, OSError) as exc:
        error(f"Could not read file: {exc}")
        raise typer.Exit(code=1)

    try:
        return yaml.safe_load(content)

    except yaml.YAMLError as exc:
        error("Invalid YAML.")

        console.print(
            f"[devkit.secondary]{exc}[/devkit.secondary]"
        )

        raise typer.Exit(code=1)

def describe_yaml_value(value) -> str:
    """Return a readable YAML value type."""

    if value is None:
        return "null"

    if isinstance(value, bool):
        return "boolean"

    if isinstance(value, dict):
        return "object"

    if isinstance(value, list):
        return "array"

    if isinstance(value, str):
        return "string"

    if isinstance(value, int):
        return "integer"

    if isinstance(value, float):
        return "number"

    return type(value).__name__

@yaml_app.command("validate")
def yaml_validate(
    file: Path = typer.Argument(
        ...,
        help="YAML file to validate.",
    ),
):
    """Validate YAML syntax."""

    section_title(
        "YAML Validator",
        str(file),
    )

    load_yaml_file(file)

    success(
        "YAML is valid."
    )    

@yaml_app.command("format")
def yaml_format(
    file: Path = typer.Argument(
        ...,
        help="YAML file to format.",
    ),
    write: bool = typer.Option(
        False,
        "--write",
        "-w",
        help="Write formatted YAML back to the file.",
    ),
):
    """Pretty-format a YAML document."""

    data = load_yaml_file(file)

    formatted = yaml.safe_dump(
        data,
        sort_keys=False,
        allow_unicode=True,
        default_flow_style=False,
    )

    if write:
        try:
            file.write_text(
                formatted,
                encoding="utf-8",
            )

        except (PermissionError, OSError) as exc:
            error(
                f"Could not write file: {exc}"
            )
            raise typer.Exit(code=1)

        success(
            f"Formatted {file}."
        )

        return

    section_title(
        "Formatted YAML",
        str(file),
    )

    syntax = Syntax(
        formatted,
        "yaml",
        line_numbers=True,
        word_wrap=True,
    )

    console.print(syntax)    

@yaml_app.command("inspect")
def yaml_inspect(
    file: Path = typer.Argument(
        ...,
        help="YAML file to inspect.",
    ),
):
    """Inspect top-level YAML structure."""

    data = load_yaml_file(file)

    section_title(
        "YAML Inspector",
        str(file),
    )

    root_type = describe_yaml_value(data)

    console.print(
        f"[devkit.secondary]Root Type:[/devkit.secondary] "
        f"[devkit.info]{root_type}[/devkit.info]\n"
    )

    if isinstance(data, dict):
        table = Table(
            title="Top-Level Properties"
        )

        table.add_column(
            "Key",
            style="cyan",
        )

        table.add_column(
            "Type",
        )

        table.add_column(
            "Summary",
            style="dim",
        )

        for key, value in data.items():
            value_type = describe_yaml_value(
                value
            )

            if isinstance(value, dict):
                summary = f"{len(value)} properties"

            elif isinstance(value, list):
                summary = f"{len(value)} items"

            elif isinstance(value, str):
                summary = (
                    value[:40]
                    + ("..." if len(value) > 40 else "")
                )

            else:
                summary = str(value)

            table.add_row(
                str(key),
                value_type,
                summary,
            )

        console.print(table)

    elif isinstance(data, list):
        console.print(
            f"[devkit.info]"
            f"Array contains {len(data)} item(s)."
            f"[/devkit.info]"
        )

    else:
        console.print(
            f"[devkit.info]"
            f"Value: {data}"
            f"[/devkit.info]"
        )    