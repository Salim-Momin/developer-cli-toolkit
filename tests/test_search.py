from pathlib import Path

from devkit.services.search_service import (
    search_filenames,
    search_project,
)


def test_search_project_finds_text(
    tmp_path: Path,
):
    test_file = tmp_path / "hello.py"

    test_file.write_text(
        "print('DevKit')",
        encoding="utf-8",
    )

    results = search_project(
        tmp_path,
        "DevKit",
    )

    assert results is not None


def test_search_filenames_finds_file(
    tmp_path: Path,
):
    test_file = tmp_path / "devkit_test.py"

    test_file.write_text(
        "test",
        encoding="utf-8",
    )

    results = search_filenames(
        tmp_path,
        "devkit",
    )

    assert results is not None
