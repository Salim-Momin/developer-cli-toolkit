import json
import time
from pathlib import Path
from datetime import datetime

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
from devkit.terminal.tables import (
    create_key_value_table,
    create_table,
)

api_app = typer.Typer(
    help="Send and inspect HTTP API requests."
)

HISTORY_FILE = (
    Path.home()
    / ".devkit"
    / "api_history.json"
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
    params: dict[str, str] | None = None,
    json_body=None,
    raw_body: str | None = None,
    timeout: float = 10.0,
) -> tuple[httpx.Response, float]:
    """Send an HTTP request and return response plus duration."""

    start = time.perf_counter()

    try:
        response = httpx.request(
            method=method,
            url=url,
            headers=headers,
            params=params,
            json=json_body,
            content=raw_body,
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
    show_headers: bool = False,
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

    header_table = create_table(
        title="Response Headers"
    )

    summary = create_key_value_table(
        title="Request Summary"
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

    if show_headers:
        header_table = Table(
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
    param: list[str] | None = None,
    raw_body: str | None = None,
    save: str | None = None,
    show_headers: bool = False,
) -> None:
    """Execute and display an API request."""

    try:
        headers = parse_headers(header)
        params = parse_params(param)

        if json_body and json_file:
            raise ValueError(
                "Use either --json or --json-file, not both."
            )

        if raw_body and (json_body or json_file):
            raise ValueError(
                "Use raw body or JSON body, not both."
            )

        if json_file:
            body = load_json_body_file(json_file)
        else:
            body = parse_json_body(json_body)

        response, duration = send_request(
            method=method,
            url=url,
            headers=headers,
            params=params,
            json_body=body,
            raw_body=raw_body,
            timeout=timeout,
        )

    except (ValueError, RuntimeError) as exc:
        error(str(exc))
        raise typer.Exit(code=1)

    display_response(
        response,
        duration,
        show_headers=show_headers,
    )

    if save:
        save_response(
            response,
            save,
        )

    save_request_history(
        method=method,
        url=str(response.url),
        status=response.status_code,
        duration_ms=duration,
    )

def save_response(
    response: httpx.Response,
    output: str,
) -> None:
    """Save response body to a file."""

    path = Path(output)

    try:
        path.write_bytes(
            response.content
        )

    except OSError as exc:
        error(
            f"Could not save response: {exc}"
        )
        return

    success(
        f"Response saved to {path}."
    )

def save_request_history(
    method: str,
    url: str,
    status: int,
    duration_ms: float,
) -> None:
    """Store API request metadata locally."""

    HISTORY_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    history = []

    if HISTORY_FILE.exists():
        try:
            history = json.loads(
                HISTORY_FILE.read_text(
                    encoding="utf-8-sig"
                )
            )

        except (
            json.JSONDecodeError,
            OSError,
        ):
            history = []

    history.append(
        {
            "time": datetime.now().isoformat(
                timespec="seconds"
            ),
            "method": method,
            "url": url,
            "status": status,
            "duration_ms": round(
                duration_ms,
                2,
            ),
        }
    )

    history = history[-100:]

    try:
        HISTORY_FILE.write_text(
            json.dumps(
                history,
                indent=2,
            ),
            encoding="utf-8",
        )

    except OSError:
        pass

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

def parse_params(
    params: list[str] | None,
) -> dict[str, str]:
    """Convert CLI query parameters into a dictionary."""

    parsed = {}

    if not params:
        return parsed

    for param in params:
        if "=" not in param:
            raise ValueError(
                f"Invalid query parameter: {param}. Use 'key=value'."
            )

        key, value = param.split("=", maxsplit=1)

        parsed[key.strip()] = value.strip()

    return parsed

@api_app.command("history")
def api_history(
    limit: int = typer.Option(
        10,
        "--limit",
        "-l",
        min=1,
        max=100,
    ),
):
    """Show recent API requests."""

    if not HISTORY_FILE.exists():
        warning(
            "No API history found."
        )
        return

    try:
        history = json.loads(
            HISTORY_FILE.read_text(
                encoding="utf-8-sig"
            )
        )

    except (
        json.JSONDecodeError,
        OSError,
    ):
        error(
            "Could not read API history."
        )
        raise typer.Exit(code=1)

    rows = history[-limit:][::-1]

    table = Table(
        title="API Request History"
    )

    table.add_column("Time")
    table.add_column(
        "Method",
        style="cyan",
    )
    table.add_column("Status")
    table.add_column("Time")
    table.add_column("URL")

    for item in rows:
        table.add_row(
            item["time"],
            item["method"],
            str(item["status"]),
            f'{item["duration_ms"]} ms',
            item["url"],
        )

    console.print()
    console.print(table)

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
    param: list[str] | None = typer.Option(
        None,
        "--param",
        "-p",
        help="Query parameter in key=value format.",
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
    raw_body: str | None = typer.Option(
        None,
        "--raw",
        help="Send a raw text request body.",
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
        raw_body=raw_body,
    )

@api_app.command("put")
def api_put(
    json_file: str | None,
    param: list[str] | None,
    raw_body: str | None,
    save: str | None,
    show_headers: bool,
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
        json_file,
        param,
        raw_body,
        save,
        show_headers,
    )    

@api_app.command("patch")
def api_patch(
    json_file: str | None,
    param: list[str] | None,
    raw_body: str | None,
    save: str | None,
    show_headers: bool, 
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
        json_file,
        param,
        raw_body,
        save,
        show_headers,
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