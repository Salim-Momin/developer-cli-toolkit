import re
from pathlib import Path

from devkit.core.config import get_ignored_directories
from devkit.core.logging import get_logger

logger = get_logger()


def should_ignore(
    path: Path,
    root: Path,
) -> bool:
    """Return True when path belongs to an ignored directory."""

    ignored = get_ignored_directories(root)

    try:
        relative = path.relative_to(root)

    except ValueError:
        relative = path

    return any(part in ignored for part in relative.parts)


def normalize_extension(
    extension: str | None,
) -> str | None:
    """Normalize extension values such as py -> .py."""

    if not extension:
        return None

    extension = extension.lower()

    if not extension.startswith("."):
        extension = f".{extension}"

    return extension


def is_binary_file(
    path: Path,
) -> bool:
    """Detect whether a file appears to be binary."""

    try:
        with path.open("rb") as file:
            chunk = file.read(1024)

        return b"\x00" in chunk

    except OSError:
        return True


def search_project(
    root: Path,
    query: str,
    extension: str | None = None,
    case_sensitive: bool = False,
    regex: bool = False,
) -> list[dict]:
    """Search text inside project files."""

    results = []

    normalized_extension = normalize_extension(extension)

    flags = 0 if case_sensitive else re.IGNORECASE

    pattern = None

    if regex:
        try:
            pattern = re.compile(
                query,
                flags,
            )

        except re.error as exc:
            raise ValueError(f"Invalid regular expression: {exc}") from exc

    search_query = query if case_sensitive else query.lower()

    for file_path in root.rglob("*"):
        if should_ignore(
            file_path,
            root,
        ):
            continue

        if not file_path.is_file():
            continue

        if normalized_extension and file_path.suffix.lower() != normalized_extension:
            continue

        if is_binary_file(file_path):
            continue

        try:
            content = file_path.read_text(
                encoding="utf-8-sig",
                errors="ignore",
            )

        except (
            PermissionError,
            OSError,
        ) as exc:

            logger.debug(
                "Could not read file %s: %s",
                file_path,
                exc,
            )

            continue

        for line_number, line in enumerate(
            content.splitlines(),
            start=1,
        ):
            if regex and pattern:
                matched = bool(pattern.search(line))

            else:
                searchable_line = line if case_sensitive else line.lower()

                matched = search_query in searchable_line

            if not matched:
                continue

            results.append(
                {
                    "file": file_path,
                    "line": line_number,
                    "text": line.strip(),
                }
            )

    return results


def search_filenames(
    root: Path,
    query: str,
    case_sensitive: bool = False,
) -> list[Path]:
    """Search project files by filename."""

    results = []

    search_query = query if case_sensitive else query.lower()

    for path in root.rglob("*"):
        if should_ignore(
            path,
            root,
        ):
            continue

        if not path.is_file():
            continue

        filename = path.name if case_sensitive else path.name.lower()

        if search_query in filename:
            results.append(path)

    return results


def find_match_ranges(
    text: str,
    query: str,
    case_sensitive: bool = False,
) -> list[tuple[int, int]]:
    """Return match ranges for non-regex text search."""

    if not query:
        return []

    flags = 0 if case_sensitive else re.IGNORECASE

    pattern = re.compile(
        re.escape(query),
        flags,
    )

    return [
        (
            match.start(),
            match.end(),
        )
        for match in pattern.finditer(text)
    ]
