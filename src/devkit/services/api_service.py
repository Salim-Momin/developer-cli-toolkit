import json
import time
from datetime import datetime
from pathlib import Path
from devkit.core.exceptions import APIError
from devkit.core.logging import get_logger
import httpx


HISTORY_FILE = (
    Path.home()
    / ".devkit"
    / "api_history.json"
)

logger = get_logger()

def parse_headers(
    headers: list[str] | None,
) -> dict[str, str]:
    """Convert CLI-style headers into a dictionary."""

    parsed = {}

    if not headers:
        return parsed

    for header in headers:
        if ":" not in header:
            raise ValueError(
                f"Invalid header: {header}. Use 'Name: Value'."
            )

        name, value = header.split(
            ":",
            maxsplit=1,
        )

        parsed[name.strip()] = value.strip()

    return parsed


def parse_params(
    params: list[str] | None,
) -> dict[str, str]:
    """Convert key=value parameters into a dictionary."""

    parsed = {}

    if not params:
        return parsed

    for param in params:
        if "=" not in param:
            raise ValueError(
                f"Invalid query parameter: {param}. Use 'key=value'."
            )

        key, value = param.split(
            "=",
            maxsplit=1,
        )

        parsed[key.strip()] = value.strip()

    return parsed


def parse_json_body(
    json_body: str | None,
):
    """Parse a JSON body string."""

    if not json_body:
        return None

    try:
        return json.loads(
            json_body
        )

    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Invalid JSON body: {exc.msg}"
        ) from exc


def load_json_body_file(
    path: str | None,
):
    """Load a JSON request body from a file."""

    if not path:
        return None

    file_path = Path(
        path
    )

    if not file_path.exists():
        raise ValueError(
            f"JSON body file not found: {path}"
        )

    try:
        content = file_path.read_text(
            encoding="utf-8-sig"
        )

    except OSError as exc:
        raise ValueError(
            f"Could not read {path}: {exc}"
        ) from exc

    try:
        return json.loads(
            content
        )

    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Invalid JSON in {path}: "
            f"line {exc.lineno}, "
            f"column {exc.colno}: "
            f"{exc.msg}"
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
        logger.exception(
            "API request timed out: %s %s",
            method,
            url,
        )

        raise APIError(
            "Request timed out."
        ) from exc

    except httpx.RequestError as exc:
        logger.exception(
            "API request failed: %s %s",
            method,
            url,
        )

        raise APIError(
            f"Request failed: {exc}"
        ) from exc

    duration_ms = (
        time.perf_counter()
        - start
    ) * 1000

    return response, duration_ms    

def save_response(
    response: httpx.Response,
    output: str,
) -> Path:
    """Save response body to disk."""

    path = Path(
        output
    )

    try:
        path.write_bytes(
            response.content
        )

    except OSError as exc:
        raise ValueError(
            f"Could not save response: {exc}"
        ) from exc

    return path

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

def get_request_history(
    limit: int = 10,
) -> list[dict]:
    """Return recent API request history."""

    if not HISTORY_FILE.exists():
        return []

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
        return []

    return history[
        -limit:
    ][::-1]

def execute_api_request(
    method: str,
    url: str,
    headers: list[str] | None = None,
    params: list[str] | None = None,
    json_body: str | None = None,
    json_file: str | None = None,
    raw_body: str | None = None,
    timeout: float = 10.0,
    save: str | None = None,
) -> dict:
    """Execute a complete API request workflow."""

    parsed_headers = parse_headers(
        headers
    )

    parsed_params = parse_params(
        params
    )

    if json_body and json_file:
        raise ValueError(
            "Use either --json or --json-file, not both."
        )

    if raw_body and (
        json_body
        or json_file
    ):
        raise ValueError(
            "Use raw body or JSON body, not both."
        )

    if json_file:
        body = load_json_body_file(
            json_file
        )
    else:
        body = parse_json_body(
            json_body
        )

    response, duration_ms = send_request(
        method=method,
        url=url,
        headers=parsed_headers,
        params=parsed_params,
        json_body=body,
        raw_body=raw_body,
        timeout=timeout,
    )

    saved_path = None

    if save:
        saved_path = save_response(
            response,
            save,
        )

    save_request_history(
        method=method,
        url=str(response.url),
        status=response.status_code,
        duration_ms=duration_ms,
    )

    return {
        "response": response,
        "duration_ms": duration_ms,
        "saved_path": saved_path,
    }    