import json
import time
from pathlib import Path

import httpx
import typer
from rich.syntax import Syntax
from rich.table import Table

from devkit.terminal.components import (
    error,
    section_title,
    success,
    warning,
)
from devkit.terminal.theme import console


api_app = typer.Typer(
    help="Send and inspect HTTP API requests."
)

def parse_headers(
    headers: list[str] | None,
) -> dict[str, str]:
    """Convert CLI header values into a dictionary."""

    parsed = {}

    if not headers:
        return parsed

    for header in headers:
        if ":" not in header:
            raise ValueError(
                f"Invalid header: {header}. Use 'Name: Value'."
            )

        name, value = header.split(":", maxsplit=1)

        parsed[name.strip()] = value.strip()

    return parsed

def parse_json_body(
    json_body: str | None,
):
    """Parse JSON body supplied from the CLI."""

    if not json_body:
        return None

    try:
        return json.loads(json_body)

    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Invalid JSON body: {exc.msg}"
        ) from exc

def send_request(
    method: str,
    url: str,
    headers: dict[str, str] | None = None,
    json_body=None,
    timeout: float = 10.0,
) -> tuple[httpx.Response, float]:
    """Send an HTTP request and return response plus duration."""

    start = time.perf_counter()

    try:
        response = httpx.request(
            method=method,
            url=url,
            headers=headers,
            json=json_body,
            timeout=timeout,
            follow_redirects=True,
        )

    except httpx.TimeoutException as exc:
        raise RuntimeError(
            "Request timed out."
        ) from exc

    except httpx.RequestError as exc:
        raise RuntimeError(
            f"Request failed: {exc}"
        ) from exc

    duration_ms = (
        time.perf_counter() - start
    ) * 1000

    return response, duration_ms

def display_response(
    response: httpx.Response,
    duration_ms: float,
) -> None:
    """Display an HTTP response in a readable format."""

    status_style = (
        "green"
        if response.is_success
        else "yellow"
        if response.is_redirect
        else "red"
    )

    section_title(
        "API Response",
        str(response.url),
    )

    summary = Table(
        show_header=False
    )

    summary.add_column(
        "Property",
        style="bold",
    )

    summary.add_column("Value")

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

    console.print(
        "\n[devkit.secondary]Response Body[/devkit.secondary]\n"
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
        response.text or "[dim]<empty response>[/dim]"
    )

def execute_request(
    method: str,
    url: str,
    header: list[str] | None,
    json_body: str | None,
    timeout: float,
    json_file: str | None = None,
) -> None:
    """Execute and display an API request."""

    try:
        headers = parse_headers(header)

        if json_body and json_file:
            raise ValueError(
                "Use either --json or --json-file, not both."
            )

        if json_file:
            body = load_json_body_file(json_file)
        else:
            body = parse_json_body(json_body)

        response, duration = send_request(
            method=method,
            url=url,
            headers=headers,
            json_body=body,
            timeout=timeout,
        )

    except (ValueError, RuntimeError) as exc:
        error(str(exc))
        raise typer.Exit(code=1)

    display_response(
        response,
        duration,
    )

def load_json_body_file(
    path: str | None,
):
    """Load a JSON request body from a file."""

    if not path:
        return None

    file_path = Path(path)

    if not file_path.exists():
        raise ValueError(
            f"JSON body file not found: {path}"
        )

    try:
        content = file_path.read_text(
            encoding="utf-8-sig"
        )

        return json.loads(content)

    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Invalid JSON in {path}: "
            f"line {exc.lineno}, column {exc.colno}: "
            f"{exc.msg}"
        ) from exc

    except OSError as exc:
        raise ValueError(
            f"Could not read {path}: {exc}"
        ) from exc

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
    timeout: float = typer.Option(
        10.0,
        "--timeout",
        "-t",
        min=0.1,
        max=120,
    ),
):
    """Send an HTTP GET request."""

    execute_request(
        method="GET",
        url=url,
        header=header,
        json_body=None,
        timeout=timeout,
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
    header: list[str] | None = typer.Option(
        None,
        "--header",
        "-H",
        help="HTTP header in 'Name: Value' format.",
    ),
    timeout: float = typer.Option(
        10.0,
        "--timeout",
        "-t",
        min=0.1,
        max=120,
    ),
    json_file: str | None = typer.Option(
        None,
        "--json-file",
        "-J",
        help="Load JSON request body from a file.",
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
    )

@api_app.command("put")
def api_put(
    url: str,
    json_body: str | None = typer.Option(
        None,
        "--json",
        "-j",
    ),
    header: list[str] | None = typer.Option(
        None,
        "--header",
        "-H",
    ),
    timeout: float = typer.Option(
        10.0,
        "--timeout",
        "-t",
    ),
):
    """Send an HTTP PUT request."""

    execute_request(
        "PUT",
        url,
        header,
        json_body,
        timeout,
    )    

@api_app.command("patch")
def api_patch(
    url: str,
    json_body: str | None = typer.Option(
        None,
        "--json",
        "-j",
    ),
    header: list[str] | None = typer.Option(
        None,
        "--header",
        "-H",
    ),
    timeout: float = typer.Option(
        10.0,
        "--timeout",
        "-t",
    ),
):
    """Send an HTTP PATCH request."""

    execute_request(
        "PATCH",
        url,
        header,
        json_body,
        timeout,
    )    

@api_app.command("delete")
def api_delete(
    url: str,
    header: list[str] | None = typer.Option(
        None,
        "--header",
        "-H",
    ),
    timeout: float = typer.Option(
        10.0,
        "--timeout",
        "-t",
    ),
):
    """Send an HTTP DELETE request."""

    execute_request(
        "DELETE",
        url,
        header,
        None,
        timeout,
    )    