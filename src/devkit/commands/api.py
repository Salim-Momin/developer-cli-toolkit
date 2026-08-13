import json

import httpx
import typer
from rich.syntax import Syntax

from devkit.services.api_service import (
    execute_api_request,
    get_request_history,
)

from devkit.terminal.components import (
    error,
    section_title,
    success,
    warning,
)

from devkit.terminal.tables import (
    create_key_value_table,
    create_table,
)

from devkit.terminal.theme import console


api_app = typer.Typer(
    help="Send and inspect HTTP API requests."
)


def display_response(
    response: httpx.Response,
    duration_ms: float,
    show_headers: bool = False,
) -> None:
    """Display an HTTP response in the terminal."""

    status_style = (
        "green"
        if response.is_success
        else "yellow"
        if response.is_redirect
        else "red"
    )

    section_title(
        "🌐 API Response",
        str(response.url),
    )

    summary = create_key_value_table(
        title="Request Summary"
    )

    summary.add_row(
        "Status",
        f"[{status_style}]"
        f"{response.status_code} "
        f"{response.reason_phrase}"
        f"[/{status_style}]",
    )

    summary.add_row(
        "Time",
        f"{duration_ms:.2f} ms",
    )

    summary.add_row(
        "Content Type",
        response.headers.get(
            "content-type",
            "Unknown",
        ),
    )

    summary.add_row(
        "Size",
        f"{len(response.content)} bytes",
    )

    console.print(summary)

    if show_headers:
        header_table = create_table(
            title="Response Headers"
        )

        header_table.add_column(
            "Header",
            style="cyan",
        )

        header_table.add_column(
            "Value",
        )

        for name, value in response.headers.items():
            header_table.add_row(
                name,
                value,
            )

        console.print()
        console.print(header_table)

    console.print(
        "\n[devkit.secondary]"
        "Response Body"
        "[/devkit.secondary]\n"
    )

    content_type = response.headers.get(
        "content-type",
        "",
    ).lower()

    if "application/json" in content_type:
        try:
            parsed = response.json()

            formatted = json.dumps(
                parsed,
                indent=2,
                ensure_ascii=False,
            )

            console.print(
                Syntax(
                    formatted,
                    "json",
                    line_numbers=True,
                    word_wrap=True,
                )
            )

            return

        except ValueError:
            pass

    console.print(
        response.text
        or "[dim]<empty response>[/dim]"
    )


def execute_request(
    method: str,
    url: str,
    header: list[str] | None,
    json_body: str | None,
    timeout: float,
    json_file: str | None = None,
    param: list[str] | None = None,
    raw_body: str | None = None,
    save: str | None = None,
    show_headers: bool = False,
) -> None:
    """Execute an API request through the shared service."""

    try:
        result = execute_api_request(
            method=method,
            url=url,
            headers=header,
            params=param,
            json_body=json_body,
            json_file=json_file,
            raw_body=raw_body,
            timeout=timeout,
            save=save,
        )

    except (
        ValueError,
        RuntimeError,
    ) as exc:
        error(
            str(exc)
        )

        raise typer.Exit(
            code=1
        )

    response = result[
        "response"
    ]

    duration_ms = result[
        "duration_ms"
    ]

    display_response(
        response=response,
        duration_ms=duration_ms,
        show_headers=show_headers,
    )

    saved_path = result[
        "saved_path"
    ]

    if saved_path:
        console.print()

        success(
            f"Response saved to {saved_path}."
        )


@api_app.command("get")
def api_get(
    url: str = typer.Argument(
        ...,
        help="Request URL.",
    ),
    header: list[str] | None = typer.Option(
        None,
        "--header",
        "-H",
        help="HTTP header in 'Name: Value' format.",
    ),
    param: list[str] | None = typer.Option(
        None,
        "--param",
        "-p",
        help="Query parameter in key=value format.",
    ),
    timeout: float = typer.Option(
        10.0,
        "--timeout",
        "-t",
        min=0.1,
        max=120,
    ),
    save: str | None = typer.Option(
        None,
        "--save",
        "-s",
        help="Save response body to a file.",
    ),
    show_headers: bool = typer.Option(
        False,
        "--headers",
        help="Show response headers.",
    ),
):
    """Send an HTTP GET request."""

    execute_request(
        method="GET",
        url=url,
        header=header,
        json_body=None,
        timeout=timeout,
        param=param,
        save=save,
        show_headers=show_headers,
    )


@api_app.command("post")
def api_post(
    url: str = typer.Argument(
        ...,
        help="Request URL.",
    ),
    json_body: str | None = typer.Option(
        None,
        "--json",
        "-j",
        help="JSON request body.",
    ),
    json_file: str | None = typer.Option(
        None,
        "--json-file",
        "-J",
        help="Load JSON request body from a file.",
    ),
    raw_body: str | None = typer.Option(
        None,
        "--raw",
        help="Send a raw text request body.",
    ),
    header: list[str] | None = typer.Option(
        None,
        "--header",
        "-H",
        help="HTTP header in 'Name: Value' format.",
    ),
    param: list[str] | None = typer.Option(
        None,
        "--param",
        "-p",
        help="Query parameter in key=value format.",
    ),
    timeout: float = typer.Option(
        10.0,
        "--timeout",
        "-t",
        min=0.1,
        max=120,
    ),
    save: str | None = typer.Option(
        None,
        "--save",
        "-s",
        help="Save response body to a file.",
    ),
    show_headers: bool = typer.Option(
        False,
        "--headers",
        help="Show response headers.",
    ),
):
    """Send an HTTP POST request."""

    execute_request(
        method="POST",
        url=url,
        header=header,
        json_body=json_body,
        timeout=timeout,
        json_file=json_file,
        param=param,
        raw_body=raw_body,
        save=save,
        show_headers=show_headers,
    )


@api_app.command("put")
def api_put(
    url: str = typer.Argument(
        ...,
        help="Request URL.",
    ),
    json_body: str | None = typer.Option(
        None,
        "--json",
        "-j",
    ),
    json_file: str | None = typer.Option(
        None,
        "--json-file",
        "-J",
    ),
    raw_body: str | None = typer.Option(
        None,
        "--raw",
    ),
    header: list[str] | None = typer.Option(
        None,
        "--header",
        "-H",
    ),
    param: list[str] | None = typer.Option(
        None,
        "--param",
        "-p",
    ),
    timeout: float = typer.Option(
        10.0,
        "--timeout",
        "-t",
        min=0.1,
        max=120,
    ),
    save: str | None = typer.Option(
        None,
        "--save",
        "-s",
    ),
    show_headers: bool = typer.Option(
        False,
        "--headers",
    ),
):
    """Send an HTTP PUT request."""

    execute_request(
        method="PUT",
        url=url,
        header=header,
        json_body=json_body,
        timeout=timeout,
        json_file=json_file,
        param=param,
        raw_body=raw_body,
        save=save,
        show_headers=show_headers,
    )


@api_app.command("patch")
def api_patch(
    url: str = typer.Argument(
        ...,
        help="Request URL.",
    ),
    json_body: str | None = typer.Option(
        None,
        "--json",
        "-j",
    ),
    json_file: str | None = typer.Option(
        None,
        "--json-file",
        "-J",
    ),
    raw_body: str | None = typer.Option(
        None,
        "--raw",
    ),
    header: list[str] | None = typer.Option(
        None,
        "--header",
        "-H",
    ),
    param: list[str] | None = typer.Option(
        None,
        "--param",
        "-p",
    ),
    timeout: float = typer.Option(
        10.0,
        "--timeout",
        "-t",
        min=0.1,
        max=120,
    ),
    save: str | None = typer.Option(
        None,
        "--save",
        "-s",
    ),
    show_headers: bool = typer.Option(
        False,
        "--headers",
    ),
):
    """Send an HTTP PATCH request."""

    execute_request(
        method="PATCH",
        url=url,
        header=header,
        json_body=json_body,
        timeout=timeout,
        json_file=json_file,
        param=param,
        raw_body=raw_body,
        save=save,
        show_headers=show_headers,
    )


@api_app.command("delete")
def api_delete(
    url: str = typer.Argument(
        ...,
        help="Request URL.",
    ),
    header: list[str] | None = typer.Option(
        None,
        "--header",
        "-H",
    ),
    param: list[str] | None = typer.Option(
        None,
        "--param",
        "-p",
    ),
    timeout: float = typer.Option(
        10.0,
        "--timeout",
        "-t",
        min=0.1,
        max=120,
    ),
    save: str | None = typer.Option(
        None,
        "--save",
        "-s",
    ),
    show_headers: bool = typer.Option(
        False,
        "--headers",
    ),
):
    """Send an HTTP DELETE request."""

    execute_request(
        method="DELETE",
        url=url,
        header=header,
        json_body=None,
        timeout=timeout,
        param=param,
        save=save,
        show_headers=show_headers,
    )


@api_app.command("history")
def api_history(
    limit: int = typer.Option(
        10,
        "--limit",
        "-l",
        min=1,
        max=100,
        help="Number of requests to display.",
    ),
):
    """Show recent API requests."""

    history = get_request_history(
        limit=limit
    )

    section_title(
        "🌐 API Request History",
        f"Showing up to {limit} recent requests.",
    )

    if not history:
        warning(
            "No API history found."
        )
        return

    table = create_table(
        title="Recent API Requests"
    )

    table.add_column(
        "Timestamp",
        style="dim",
    )

    table.add_column(
        "Method",
        style="cyan",
    )

    table.add_column(
        "Status",
        justify="right",
    )

    table.add_column(
        "Time",
        justify="right",
    )

    table.add_column(
        "URL",
    )

    for item in history:
        status = int(
            item["status"]
        )

        if 200 <= status < 300:
            status_display = (
                f"[green]{status}[/green]"
            )

        elif 300 <= status < 400:
            status_display = (
                f"[yellow]{status}[/yellow]"
            )

        else:
            status_display = (
                f"[red]{status}[/red]"
            )

        table.add_row(
            item["time"],
            item["method"],
            status_display,
            f'{item["duration_ms"]} ms',
            item["url"],
        )

    console.print(table)