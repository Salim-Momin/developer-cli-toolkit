from pathlib import Path

from devkit.core.config import (
    get_config_path,
)


def test_config_path_exists():
    path = get_config_path()

    assert isinstance(
        path,
        Path,
    )
