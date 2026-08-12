import json
from pathlib import Path

import typer
from rich.syntax import Syntax
from rich.table import Table

from devkit.terminal.components import (
    error,
    section_title,
    success,
    warning,
)
from devkit.terminal.theme import console


json_app = typer.Typer(
    help="Validate, format, inspect and manipulate JSON files."
)

def load_json_file(path: Path):
    """Safely load and parse a JSON file."""

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
        return json.loads(content)

    except json.JSONDecodeError as exc:
        error("Invalid JSON.")

        console.print(
            f"[devkit.secondary]"
            f"Line {exc.lineno}, column {exc.colno}"
            f"[/devkit.secondary]"
        )

        console.print(
            f"[devkit.secondary]"
            f"{exc.msg}"
            f"[/devkit.secondary]"
        )

        raise typer.Exit(code=1)

def describe_json_value(value) -> str:
    """Return a readable JSON value type."""

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

@json_app.command("validate")
def json_validate(
    file: Path = typer.Argument(
        ...,
        help="JSON file to validate.",
    ),
):
    """Validate JSON syntax."""

    section_title(
        "JSON Validator",
        str(file),
    )

    load_json_file(file)

    success(
        "JSON is valid."
    )    

@json_app.command("format")
def json_format(
    file: Path = typer.Argument(
        ...,
        help="JSON file to format.",
    ),
    indent: int = typer.Option(
        2,
        "--indent",
        "-i",
        min=1,
        max=8,
        help="Number of spaces used for indentation.",
    ),
    write: bool = typer.Option(
        False,
        "--write",
        "-w",
        help="Write formatted JSON back to the file.",
    ),
):
    """Pretty-format a JSON document."""

    data = load_json_file(file)

    formatted = json.dumps(
        data,
        indent=indent,
        ensure_ascii=False,
    )

    if write:
        try:
            file.write_text(
                formatted + "\n",
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
        "Formatted JSON",
        str(file),
    )

    syntax = Syntax(
        formatted,
        "json",
        theme="monokai",
        line_numbers=True,
        word_wrap=True,
    )

    console.print(syntax)

@json_app.command("minify")
def json_minify(
    file: Path = typer.Argument(
        ...,
        help="JSON file to minify.",
    ),
    write: bool = typer.Option(
        False,
        "--write",
        "-w",
        help="Write minified JSON back to the file.",
    ),
):
    """Remove unnecessary whitespace from JSON."""

    data = load_json_file(file)

    minified = json.dumps(
        data,
        separators=(",", ":"),
        ensure_ascii=False,
    )

    if write:
        try:
            file.write_text(
                minified,
                encoding="utf-8",
            )

        except (PermissionError, OSError) as exc:
            error(
                f"Could not write file: {exc}"
            )
            raise typer.Exit(code=1)

        success(
            f"Minified {file}."
        )

        return

    section_title(
        "Minified JSON",
        str(file),
    )

    console.print(minified)

@json_app.command("inspect")
def json_inspect(
    file: Path = typer.Argument(
        ...,
        help="JSON file to inspect.",
    ),
):
    """Inspect the top-level structure of a JSON document."""

    data = load_json_file(file)

    section_title(
        "JSON Inspector",
        str(file),
    )

    root_type = describe_json_value(data)

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
            value_type = describe_json_value(
                value
            )

            if isinstance(value, dict):
                summary = (
                    f"{len(value)} properties"
                )

            elif isinstance(value, list):
                summary = (
                    f"{len(value)} items"
                )

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