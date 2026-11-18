"""Adapter for the official ISA-tools validator and our experimental config."""

import json
from pathlib import Path
import subprocess
import sys

from .isa_core import SchemaUnavailable, _schema_directory

CONFIG = Path(__file__).resolve().parents[1] / "schemas" / "isa-tools-phm"


def validate_isa(path: Path) -> dict:
    _schema_directory()
    try:
        process = subprocess.run(
            [sys.executable, "-m", "validator.isa_worker", str(path.resolve()), str(CONFIG)],
            capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60,
        )
        if process.returncode:
            raise SchemaUnavailable(f"ISA-tools worker failed: {process.stderr[-1000:]}")
        report = json.loads(process.stdout)
        if not isinstance(report, dict) or not isinstance(report.get("errors"), list) or not isinstance(report.get("warnings"), list) or not isinstance(report.get("completed"), bool):
            raise ValueError("unexpected worker response")
        return report
    except (OSError, subprocess.TimeoutExpired, ValueError) as exc:
        raise SchemaUnavailable(f"ISA-tools validation could not complete: {exc}") from exc
