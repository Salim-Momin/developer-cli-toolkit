import json
from pathlib import Path

import typer
import yaml
from rich.syntax import Syntax

from devkit.commands.json_tools import load_json_file
from devkit.commands.yaml_tools import load_yaml_file
from devkit.terminal.components import (
    error,
    section_title,
    success,
)
from devkit.terminal.theme import console


convert_app = typer.Typer(
    help="Convert developer data formats."
)

@convert_app.command("json-to-yaml")
def json_to_yaml(
    file: Path = typer.Argument(
        ...,
        help="JSON file to convert.",
    ),
    output: Path | None = typer.Option(
        None,
        "--output",
        "-o",
        help="Optional output YAML file.",
    ),
):
    """Convert JSON into YAML."""

    data = load_json_file(file)

    converted = yaml.safe_dump(
        data,
        sort_keys=False,
        allow_unicode=True,
        default_flow_style=False,
    )

    if output:
        try:
            output.write_text(
                converted,
                encoding="utf-8",
            )

        except (PermissionError, OSError) as exc:
            error(
                f"Could not write output file: {exc}"
            )
            raise typer.Exit(code=1)

        success(
            f"Created {output}."
        )

        return

    section_title(
        "JSON → YAML",
        str(file),
    )

    console.print(
        Syntax(
            converted,
            "yaml",
            line_numbers=True,
        )
    )

@convert_app.command("yaml-to-json")
def yaml_to_json(
    file: Path = typer.Argument(
        ...,
        help="YAML file to convert.",
    ),
    output: Path | None = typer.Option(
        None,
        "--output",
        "-o",
        help="Optional output JSON file.",
    ),
    indent: int = typer.Option(
        2,
        "--indent",
        "-i",
        min=1,
        max=8,
        help="JSON indentation size.",
    ),
):
    """Convert YAML into JSON."""

    data = load_yaml_file(file)

    converted = json.dumps(
        data,
        indent=indent,
        ensure_ascii=False,
    )

    if output:
        try:
            output.write_text(
                converted + "\n",
                encoding="utf-8",
            )

        except (PermissionError, OSError) as exc:
            error(
                f"Could not write output file: {exc}"
            )
            raise typer.Exit(code=1)

        success(
            f"Created {output}."
        )

        return

    section_title(
        "YAML → JSON",
        str(file),
    )

    console.print(
        Syntax(
            converted,
            "json",
            line_numbers=True,
        )
    )