from pathlib import Path

from typer.testing import CliRunner

from devkit.commands.json_tools import json_app

runner = CliRunner()


def create_json_file(tmp_path: Path):
    json_file = tmp_path / "test.json"

    json_file.write_text(
        '{"name":"DevKit","version":"1.0"}',
        encoding="utf-8",
    )

    return json_file


def test_json_validate(
    tmp_path: Path,
):
    json_file = create_json_file(tmp_path)

    result = runner.invoke(
        json_app,
        [
            "validate",
            str(json_file),
        ],
    )

    assert result.exit_code == 0


def test_json_format(
    tmp_path: Path,
):
    json_file = create_json_file(tmp_path)

    result = runner.invoke(
        json_app,
        [
            "format",
            str(json_file),
        ],
    )

    assert result.exit_code == 0


def test_json_minify(
    tmp_path: Path,
):
    json_file = create_json_file(tmp_path)

    result = runner.invoke(
        json_app,
        [
            "minify",
            str(json_file),
        ],
    )

    assert result.exit_code == 0


def test_json_inspect(
    tmp_path: Path,
):
    json_file = create_json_file(tmp_path)

    result = runner.invoke(
        json_app,
        [
            "inspect",
            str(json_file),
        ],
    )

    assert result.exit_code == 0
