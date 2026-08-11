from rich.console import Console
from rich.theme import Theme


DEVKIT_THEME = Theme(
    {
        "devkit.primary": "bold cyan",
        "devkit.secondary": "bright_black",
        "devkit.success": "bold green",
        "devkit.warning": "bold yellow",
        "devkit.error": "bold red",
        "devkit.info": "cyan",
        "devkit.muted": "dim",
        "devkit.title": "bold white",
    }
)


console = Console(
    theme=DEVKIT_THEME,
)