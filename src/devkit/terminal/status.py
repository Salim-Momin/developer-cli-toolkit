def status_badge(
    status: str,
) -> str:
    """Return a consistent Rich status badge."""

    normalized = status.lower()

    if normalized in {
        "ok",
        "pass",
        "healthy",
        "installed",
        "success",
        "clean",
        "yes",
    }:
        return "[bold green]● PASS[/bold green]"

    if normalized in {
        "warning",
        "attention",
        "missing",
        "dirty",
        "partial",
    }:
        return "[bold yellow]● WARN[/bold yellow]"

    if normalized in {
        "error",
        "failed",
        "fail",
        "unhealthy",
        "no",
    }:
        return "[bold red]● FAIL[/bold red]"

    return "[dim]● UNKNOWN[/dim]"

def yes_no(
    value: bool,
) -> str:
    """Render boolean values consistently."""

    return (
        "[green]✓ Yes[/green]"
        if value
        else "[dim]✗ No[/dim]"
    )