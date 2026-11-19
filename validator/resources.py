"""Resolve the same canonical inputs in a checkout or installed distribution."""

from pathlib import Path


def resource_path(relative_path: str) -> Path:
    package = Path(__file__).resolve().parent
    installed = package / "_assets" / relative_path
    if installed.exists():
        return installed
    return package.parent / relative_path
