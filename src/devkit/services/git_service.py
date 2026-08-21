import subprocess
from pathlib import Path
from devkit.core.logging import get_logger

logger = get_logger()

def run_git_command(
    args: list[str],
    cwd: Path | None = None,
) -> str | None:
    """Run a Git command and return cleaned output."""

    try:
        result = subprocess.run(
            ["git", *args],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=10,
            shell=False,
        )

        if result.returncode != 0:
            logger.debug(
                "Git command failed: git %s | stderr=%s",
                " ".join(args),
                result.stderr.strip(),
            )

            return None

        if result.returncode != 0:
            return None

        return result.stdout.strip()

    except (
        FileNotFoundError,
        subprocess.TimeoutExpired,
        OSError,
    ) as exc:
        logger.exception(
            "Git command execution failed: git %s",
            " ".join(args),
        )

        return None

def is_git_repository(
    path: Path,
) -> bool:
    """Return True if path belongs to a Git repository."""

    result = run_git_command(
        [
            "rev-parse",
            "--is-inside-work-tree",
        ],
        cwd=path,
    )

    return result == "true"

def get_current_branch(
    path: Path,
) -> str | None:
    """Return the current Git branch."""

    return run_git_command(
        [
            "branch",
            "--show-current",
        ],
        cwd=path,
    )    

def get_repository_root(
    path: Path,
) -> str | None:
    """Return repository root path."""

    return run_git_command(
        [
            "rev-parse",
            "--show-toplevel",
        ],
        cwd=path,
    )

def get_origin_url(
    path: Path,
) -> str | None:
    """Return origin remote URL."""

    return run_git_command(
        [
            "remote",
            "get-url",
            "origin",
        ],
        cwd=path,
    )

def get_status_lines(
    path: Path,
) -> list[str]:
    """Return Git porcelain status lines."""

    output = run_git_command(
        [
            "status",
            "--porcelain",
        ],
        cwd=path,
    )

    if not output:
        return []

    return [
        line
        for line in output.splitlines()
        if line.strip()
    ]

def get_status_summary(
    path: Path,
) -> dict:
    """Return summarized working-tree status."""

    lines = get_status_lines(
        path
    )

    staged = 0
    modified = 0
    untracked = 0
    deleted = 0

    for line in lines:
        status = line[:2]

        if status == "??":
            untracked += 1
            continue

        if status[0] not in {
            " ",
            "?",
        }:
            staged += 1

        if len(status) > 1 and status[1] == "M":
            modified += 1

        if "D" in status:
            deleted += 1

    return {
        "staged": staged,
        "modified": modified,
        "untracked": untracked,
        "deleted": deleted,
        "clean": len(lines) == 0,
    }

def get_changed_files(
    path: Path,
) -> list[dict]:
    """Return changed files with Git status codes."""

    output = run_git_command(
        [
            "status",
            "--short",
        ],
        cwd=path,
    )

    if not output:
        return []

    results = []

    for line in output.splitlines():
        if len(line) < 3:
            continue

        status = (
            line[:2].strip()
            or "-"
        )

        file_name = line[3:].strip()

        results.append(
            {
                "status": status,
                "file": file_name,
            }
        )

    return results

def get_local_branches(
    path: Path,
) -> list[dict]:
    """Return local Git branches."""

    output = run_git_command(
        [
            "for-each-ref",
            "--format=%(refname:short)|%(HEAD)",
            "refs/heads/",
        ],
        cwd=path,
    )

    if not output:
        return []

    branches = []

    for line in output.splitlines():
        if "|" not in line:
            continue

        branch, marker = line.split(
            "|",
            maxsplit=1,
        )

        branches.append(
            {
                "name": branch,
                "current": marker == "*",
            }
        )

    return branches

def get_recent_commits(
    path: Path,
    limit: int = 10,
) -> list[dict]:
    """Return recent Git commits."""

    output = run_git_command(
        [
            "log",
            f"-{limit}",
            "--pretty=format:%h|%an|%ar|%s",
        ],
        cwd=path,
    )

    if not output:
        return []

    commits = []

    for line in output.splitlines():
        parts = line.split(
            "|",
            maxsplit=3,
        )

        if len(parts) != 4:
            continue

        commit_hash, author, when, message = parts

        commits.append(
            {
                "hash": commit_hash,
                "author": author,
                "when": when,
                "message": message,
            }
        )

    return commits

def get_remotes(
    path: Path,
) -> list[dict]:
    """Return configured Git remotes."""

    output = run_git_command(
        [
            "remote",
            "-v",
        ],
        cwd=path,
    )

    if not output:
        return []

    remotes = []

    for line in output.splitlines():
        parts = line.split()

        if len(parts) < 3:
            continue

        remotes.append(
            {
                "name": parts[0],
                "url": parts[1],
                "type": parts[2].strip("()"),
            }
        )

    return remotes

def get_tracking_branch(
    path: Path,
) -> str | None:
    """Return upstream tracking branch."""

    return run_git_command(
        [
            "rev-parse",
            "--abbrev-ref",
            "--symbolic-full-name",
            "@{upstream}",
        ],
        cwd=path,
    )

def get_ahead_behind(
    path: Path,
    upstream: str,
) -> tuple[int, int]:
    """Return commits ahead and behind upstream."""

    output = run_git_command(
        [
            "rev-list",
            "--left-right",
            "--count",
            f"HEAD...{upstream}",
        ],
        cwd=path,
    )

    if not output:
        return 0, 0

    parts = output.split()

    if len(parts) != 2:
        return 0, 0

    try:
        return (
            int(parts[0]),
            int(parts[1]),
        )

    except ValueError:
        return 0, 0    

def get_sync_status(
    path: Path,
) -> dict:
    """Return branch synchronization details."""

    branch = (
        get_current_branch(path)
        or "Unknown"
    )

    upstream = get_tracking_branch(
        path
    )

    if not upstream:
        return {
            "branch": branch,
            "upstream": None,
            "ahead": 0,
            "behind": 0,
            "state": "no-upstream",
        }

    ahead, behind = get_ahead_behind(
        path,
        upstream,
    )

    if ahead == 0 and behind == 0:
        state = "synced"

    elif ahead > 0 and behind == 0:
        state = "ahead"

    elif behind > 0 and ahead == 0:
        state = "behind"

    else:
        state = "diverged"

    return {
        "branch": branch,
        "upstream": upstream,
        "ahead": ahead,
        "behind": behind,
        "state": state,
    }    

def get_git_identity(
    path: Path,
) -> dict:
    """Return Git name and email configuration."""

    username = (
        run_git_command(
            [
                "config",
                "user.name",
            ],
            cwd=path,
        )
        or run_git_command(
            [
                "config",
                "--global",
                "user.name",
            ],
            cwd=path,
        )
    )

    email = (
        run_git_command(
            [
                "config",
                "user.email",
            ],
            cwd=path,
        )
        or run_git_command(
            [
                "config",
                "--global",
                "user.email",
            ],
            cwd=path,
        )
    )

    return {
        "name": username,
        "email": email,
        "configured": bool(
            username and email
        ),
    }

def get_repository_summary(
    path: Path,
) -> dict:
    """Return high-level repository information."""

    commit_count = (
        run_git_command(
            [
                "rev-list",
                "--count",
                "HEAD",
            ],
            cwd=path,
        )
        or "0"
    )

    latest_commit = (
        run_git_command(
            [
                "log",
                "-1",
                "--pretty=format:%h - %s",
            ],
            cwd=path,
        )
        or "No commits"
    )

    status = get_status_summary(
        path
    )

    return {
        "root": (
            get_repository_root(path)
            or str(path)
        ),
        "branch": (
            get_current_branch(path)
            or "Unknown"
        ),
        "commit_count": commit_count,
        "origin": (
            get_origin_url(path)
            or "Not configured"
        ),
        "latest_commit": latest_commit,
        "clean": status["clean"],
    }    

def get_git_health(
    path: Path,
) -> dict:
    """Return Git repository health information."""

    branch = get_current_branch(
        path
    )

    origin = get_origin_url(
        path
    )

    upstream = get_tracking_branch(
        path
    )

    identity = get_git_identity(
        path
    )

    status = get_status_summary(
        path
    )

    checks = [
        {
            "name": "Current Branch",
            "ok": bool(branch),
            "details": (
                branch
                or "Detached HEAD"
            ),
        },
        {
            "name": "Origin Remote",
            "ok": bool(origin),
            "details": (
                origin
                or "Not configured"
            ),
        },
        {
            "name": "Tracking Branch",
            "ok": bool(upstream),
            "details": (
                upstream
                or "Not configured"
            ),
        },
        {
            "name": "Git Identity",
            "ok": identity["configured"],
            "details": (
                f'{identity["name"]} <{identity["email"]}>'
                if identity["configured"]
                else "Name or email missing"
            ),
        },
        {
            "name": "Working Tree",
            "ok": status["clean"],
            "details": (
                "Clean"
                if status["clean"]
                else "Uncommitted changes detected"
            ),
        },
    ]

    score = round(
        (
            sum(
                1
                for check in checks
                if check["ok"]
            )
            / len(checks)
        )
        * 100
    )

    return {
        "score": score,
        "checks": checks,
    }

