from pathlib import Path

import typer
from rich.markup import escape

from devkit.services.search_service import (
    find_match_ranges,
    search_filenames,
    search_project,
)
from devkit.terminal.components import (
    error,
    loading,
    section_title,
)
from devkit.terminal.tables import create_table
from devkit.terminal.theme import console


def highlight_match(
    text: str,
    query: str,
    case_sensitive: bool = False,
) -> str:
    """Highlight text matches for terminal output."""

    ranges = find_match_ranges(
        text=text,
        query=query,
        case_sensitive=case_sensitive,
    )

    if not ranges:
        return escape(text)

    parts: list[str] = []
    position = 0

    for start, end in ranges:
        parts.append(
            escape(
                text[position:start]
            )
        )

        parts.append(
            "[bold yellow]"
            + escape(text[start:end])
            + "[/bold yellow]"
        )

        position = end

    parts.append(
        escape(
            text[position:]
        )
    )

    return "".join(parts)


def search_text(
    query: str = typer.Argument(
        ...,
        help="Text or filename to search for.",
    ),
    extension: str | None = typer.Option(
        None,
        "--ext",
        "-e",
        help="Only search files with this extension.",
    ),
    case_sensitive: bool = typer.Option(
        False,
        "--case-sensitive",
        "-c",
        help="Enable case-sensitive searching.",
    ),
    regex: bool = typer.Option(
        False,
        "--regex",
        "-r",
        help="Treat the search query as a regular expression.",
    ),
    filename: bool = typer.Option(
        False,
        "--filename",
        "-f",
        help="Search filenames instead of file contents.",
    ),
    limit: int = typer.Option(
        50,
        "--limit",
        "-l",
        min=1,
        max=500,
        help="Maximum number of results to display.",
    ),
):
    """Search project source code and filenames."""

    project_path = Path.cwd()

    section_title(
        "🔎 Smart Search",
        f'Searching current project for "{query}"',
    )

    # ---------------------------------------------------------
    # Filename Search
    # ---------------------------------------------------------

    if filename:
        with loading(
            "Searching filenames..."
        ):
            results = search_filenames(
                root=project_path,
                query=query,
                case_sensitive=case_sensitive,
            )

        if not results:
            console.print(
                "\n[devkit.warning]"
                "⚠ No matching filenames found."
                "[/devkit.warning]"
            )
            return

        table = create_table(
            title=(
                f"Filename Results · "
                f"{len(results)} matches"
            )
        )

        table.add_column(
            "File",
            style="cyan",
        )

        for result in results[:limit]:
            try:
                relative_path = result.relative_to(
                    project_path
                )
            except ValueError:
                relative_path = result

            table.add_row(
                str(relative_path)
            )

        console.print()
        console.print(table)

        if len(results) > limit:
            console.print(
                f"\n[devkit.secondary]"
                f"Showing {limit} of "
                f"{len(results)} matches."
                f"[/devkit.secondary]"
            )

        return

    # ---------------------------------------------------------
    # Text Search
    # ---------------------------------------------------------

    try:
        with loading(
            "Searching project..."
        ):
            results = search_project(
                root=project_path,
                query=query,
                extension=extension,
                case_sensitive=case_sensitive,
                regex=regex,
            )

    except ValueError as exc:
        error(
            str(exc)
        )
        raise typer.Exit(code=1)

    if not results:
        console.print(
            "\n[devkit.warning]"
            "⚠ No matching text found."
            "[/devkit.warning]"
        )
        return

    table = create_table(
        title=(
            f"Search Results · "
            f"{len(results)} matches"
        )
    )

    table.add_column(
        "File",
        style="cyan",
    )

    table.add_column(
        "Line",
        justify="right",
        style="bright_black",
    )

    table.add_column(
        "Match",
    )

    for result in results[:limit]:
        file_path = result["file"]

        try:
            relative_path = file_path.relative_to(
                project_path
            )
        except ValueError:
            relative_path = file_path

        text = result["text"]

        if len(text) > 120:
            text = text[:117] + "..."

        if regex:
            display_text = escape(
                text
            )

        else:
            display_text = highlight_match(
                text=text,
                query=query,
                case_sensitive=case_sensitive,
            )

        table.add_row(
            str(relative_path),
            str(result["line"]),
            display_text,
        )

    console.print()
    console.print(table)

    if len(results) > limit:
        console.print(
            f"\n[devkit.secondary]"
            f"Showing {limit} of "
            f"{len(results)} matches."
            f"[/devkit.secondary]"
        )