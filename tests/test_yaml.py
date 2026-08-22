from pathlib import Path

from devkit.commands.yaml_tools import yaml_validate


def test_yaml_validation(
    tmp_path: Path,
):

    yaml_file = tmp_path / "test.yaml"

    yaml_file.write_text(
        """
name: DevKit
version: 1.0
""",
        encoding="utf-8",
    )

    result = yaml_validate(yaml_file)

    assert result is None
