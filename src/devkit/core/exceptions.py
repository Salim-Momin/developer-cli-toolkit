class DevKitError(Exception):
    """Base exception for DevKit."""


class ConfigError(DevKitError):
    """Raised for configuration problems."""


class ProjectError(DevKitError):
    """Raised for project inspection problems."""


class SearchError(DevKitError):
    """Raised for search-related problems."""


class GitError(DevKitError):
    """Raised for Git-related problems."""


class DoctorError(DevKitError):
    """Raised for environment diagnostic problems."""


class APIError(DevKitError):
    """Raised for API request problems."""


class FileOperationError(DevKitError):
    """Raised for filesystem read/write problems."""