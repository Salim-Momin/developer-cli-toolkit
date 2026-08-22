def score_bar(
    score: int,
    width: int = 24,
) -> str:
    """Create a standardized score bar."""

    score = max(
        0,
        min(score, 100),
    )

    filled = round(score / 100 * width)

    empty = width - filled

    if score >= 80:
        style = "green"

    elif score >= 50:
        style = "yellow"

    else:
        style = "red"

    return (
        f"[{style}]"
        f"{'█' * filled}"
        f"[/{style}]"
        f"[bright_black]"
        f"{'░' * empty}"
        f"[/bright_black]"
    )
