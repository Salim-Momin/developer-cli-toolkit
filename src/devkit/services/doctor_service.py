import shutil
import subprocess
import sys

TOOLS = [
    {
        "name": "Python",
        "executables": ["python", "python3"],
        "version_command": ["python", "--version"],
    },
    {
        "name": "pip",
        "executables": ["pip", "pip3"],
        "version_command": ["pip", "--version"],
    },
    {
        "name": "Node.js",
        "executables": ["node"],
        "version_command": ["node", "--version"],
    },
    {
        "name": "npm",
        "executables": ["npm"],
        "version_command": ["npm", "--version"],
    },
    {
        "name": "Git",
        "executables": ["git"],
        "version_command": ["git", "--version"],
    },
    {
        "name": "Docker",
        "executables": ["docker"],
        "version_command": ["docker", "--version"],
    },
    {
        "name": "Java",
        "executables": ["java"],
        "version_command": ["java", "--version"],
    },
    {
        "name": "PostgreSQL",
        "executables": ["psql"],
        "version_command": ["psql", "--version"],
    },
    {
        "name": "VS Code",
        "executables": ["code"],
        "version_command": ["code", "--version"],
    },
    {
        "name": "GitHub CLI",
        "executables": ["gh"],
        "version_command": ["gh", "--version"],
    },
]


def run_command(command: list[str]) -> str | None:
    """Run a command safely and return output."""

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=5,
            shell=False,
            check=False,
        )

        output = result.stdout.strip() or result.stderr.strip()

        if result.returncode != 0:
            return None

        return output

    except (
        FileNotFoundError,
        subprocess.TimeoutExpired,
        OSError,
    ):
        return None


def first_line(value: str | None) -> str:
    """Return only the first output line."""

    if not value:
        return "Unknown"

    return value.splitlines()[0].strip()


def find_executable(
    executables: list[str],
) -> str | None:
    """Return the first executable found on PATH."""

    for executable in executables:
        if shutil.which(executable):
            return executable

    return None


def inspect_tools() -> list[dict]:
    """Inspect installed development tools."""

    results = []

    for tool in TOOLS:
        executable = find_executable(tool["executables"])

        if not executable:
            results.append(
                {
                    "name": tool["name"],
                    "installed": False,
                    "version": "-",
                    "path": "-",
                }
            )
            continue

        version_command = list(tool["version_command"])

        version_command[0] = executable

        version = first_line(run_command(version_command))

        results.append(
            {
                "name": tool["name"],
                "installed": True,
                "version": version,
                "path": (shutil.which(executable) or "-"),
            }
        )

    return results


def calculate_environment_score(
    results: list[dict],
) -> int:
    """Calculate environment readiness score."""

    if not results:
        return 0

    installed_count = sum(1 for result in results if result["installed"])

    return round(installed_count / len(results) * 100)


def detect_virtual_environment() -> dict:
    """Detect active Python virtual environment."""

    active = sys.prefix != sys.base_prefix

    return {
        "active": active,
        "path": (sys.prefix if active else "-"),
    }


def get_git_config() -> dict:
    """Read global Git identity."""

    username = run_command(
        [
            "git",
            "config",
            "--global",
            "user.name",
        ]
    )

    email = run_command(
        [
            "git",
            "config",
            "--global",
            "user.email",
        ]
    )

    return {
        "username": (first_line(username) if username else "-"),
        "email": (first_line(email) if email else "-"),
    }


def detect_package_managers() -> list[str]:
    """Detect installed Node package managers."""

    managers = [
        "npm",
        "pnpm",
        "yarn",
        "bun",
    ]

    return [manager for manager in managers if shutil.which(manager)]


def check_docker_daemon() -> bool:
    """Check whether Docker daemon is reachable."""

    if not shutil.which("docker"):
        return False

    result = run_command(
        [
            "docker",
            "info",
        ]
    )

    return result is not None


def build_diagnostics(
    tool_results: list[dict],
) -> list[dict]:
    """Build development environment diagnostics."""

    diagnostics = []

    virtual_env = detect_virtual_environment()

    diagnostics.append(
        {
            "check": "Python Virtual Environment",
            "ok": virtual_env["active"],
            "details": (
                virtual_env["path"]
                if virtual_env["active"]
                else "No virtual environment detected"
            ),
        }
    )

    git_installed = any(
        result["name"] == "Git" and result["installed"] for result in tool_results
    )

    if git_installed:
        git_config = get_git_config()

        git_configured = git_config["username"] != "-" and git_config["email"] != "-"

        diagnostics.append(
            {
                "check": "Git Identity",
                "ok": git_configured,
                "details": (
                    f'{git_config["username"]} ' f'<{git_config["email"]}>'
                    if git_configured
                    else "Git username or email is missing"
                ),
            }
        )

    package_managers = detect_package_managers()

    diagnostics.append(
        {
            "check": "Node Package Manager",
            "ok": bool(package_managers),
            "details": (
                ", ".join(package_managers)
                if package_managers
                else "No Node package manager detected"
            ),
        }
    )

    docker_installed = any(
        result["name"] == "Docker" and result["installed"] for result in tool_results
    )

    if docker_installed:
        daemon_running = check_docker_daemon()

        diagnostics.append(
            {
                "check": "Docker Daemon",
                "ok": daemon_running,
                "details": (
                    "Running"
                    if daemon_running
                    else "Docker installed but daemon unavailable"
                ),
            }
        )

    python_path = shutil.which("python") or sys.executable

    diagnostics.append(
        {
            "check": "Python Executable",
            "ok": bool(python_path),
            "details": (python_path or "Python executable not found"),
        }
    )

    return diagnostics


def build_recommendations(
    tool_results: list[dict],
    diagnostics: list[dict],
) -> list[str]:
    """Build actionable environment recommendations."""

    recommendations = []

    for result in tool_results:
        if not result["installed"]:
            recommendations.append(f'{result["name"]} is not available on PATH.')

    for diagnostic in diagnostics:
        if diagnostic["ok"]:
            continue

        if diagnostic["check"] == "Python Virtual Environment":
            recommendations.append(
                "Use a Python virtual environment for project isolation."
            )

        elif diagnostic["check"] == "Git Identity":
            recommendations.append(
                "Configure Git user.name and user.email before committing."
            )

        elif diagnostic["check"] == "Node Package Manager":
            recommendations.append(
                "Install npm, pnpm, yarn, or bun for Node.js projects."
            )

        elif diagnostic["check"] == "Docker Daemon":
            recommendations.append("Start Docker Desktop or the Docker daemon.")

    return recommendations


def analyze_environment() -> dict:
    """Return complete environment analysis."""

    tools = inspect_tools()

    diagnostics = build_diagnostics(tools)

    recommendations = build_recommendations(
        tools,
        diagnostics,
    )

    return {
        "tools": tools,
        "score": (calculate_environment_score(tools)),
        "diagnostics": diagnostics,
        "recommendations": recommendations,
    }
