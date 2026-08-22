from pathlib import Path

from devkit.services.project_service import (
    analyze_project,
    count_tree_nodes,
    list_project_tree,
)


def test_analyze_project(
    tmp_path: Path,
):
    test_file = tmp_path / "main.py"

    test_file.write_text(
        "print('Hello')",
        encoding="utf-8",
    )

    result = analyze_project(tmp_path)

    assert result is not None


def test_list_project_tree(
    tmp_path: Path,
):
    test_file = tmp_path / "app.py"

    test_file.write_text(
        "print('DevKit')",
        encoding="utf-8",
    )

    tree = list_project_tree(tmp_path)

    assert tree is not None


def test_count_tree_nodes():

    tree = {
        "name": "root",
        "type": "directory",
        "children": [{"name": "file.py", "type": "file", "children": []}],
    }

    result = count_tree_nodes(tree)

    assert result == (1, 1)
