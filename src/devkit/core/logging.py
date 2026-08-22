import logging
from pathlib import Path


LOG_DIRECTORY = (
    Path.home()
    / ".devkit"
    / "logs"
)

LOG_FILE = (
    LOG_DIRECTORY
    / "devkit.log"
)


def setup_logging(
    debug: bool = False,
) -> logging.Logger:
    """Configure DevKit application logging."""

    LOG_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True,
    )

    logger = logging.getLogger("devkit")

    logger.setLevel(
        logging.DEBUG
        if debug
        else logging.INFO
    )

    # Don't add handlers twice
    if logger.handlers:
        return logger

    file_handler = logging.FileHandler(
        LOG_FILE,
        encoding="utf-8",
    )

    file_handler.setLevel(
        logging.DEBUG
    )

    formatter = logging.Formatter(
        "%(asctime)s | "
        "%(levelname)s | "
        "%(name)s | "
        "%(message)s"
    )

    file_handler.setFormatter(
        formatter
    )

    logger.addHandler(
        file_handler
    )

    logger.info(
        "========== DevKit Started =========="
    )

    return logger

def get_logger() -> logging.Logger:
    """Return the DevKit logger."""

    return logging.getLogger(
        "devkit"
    )