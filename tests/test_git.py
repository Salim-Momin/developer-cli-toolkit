from pathlib import Path

from devkit.services.git_service import (
    is_git_repository,
    run_git_command,
)


def test_git_command_runs():

    result = run_git_command(["--version"])

    assert result is not None


def test_git_repository_detection(
    tmp_path: Path,
):

    result = is_git_repository(tmp_path)

    assert result is False
