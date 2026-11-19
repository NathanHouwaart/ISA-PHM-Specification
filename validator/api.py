"""Structured API for selected experimental checks, not conformance claims."""

from dataclasses import asdict, dataclass
import json
from pathlib import Path

from .layout import CheckResult, Issue

CHECKS = ("layout", "isa_schema", "isa_tools", "phm_protocols", "phm_metadata",
          "phm_experiment_type", "phm_sensors", "phm_sensor_csv")


@dataclass
class CheckOutcome:
    name: str
    status: str
    errors: list[Issue]
    incomplete: list[Issue]
    advisories: list[Issue]

    @classmethod
    def from_result(cls, name, result):
        status = "fail" if result.errors else "incomplete" if result.warnings else "pass"
        return cls(name, status, result.errors, result.warnings, result.advisories)


@dataclass
class ValidationReport:
    profile: str
    specification_version: str | None
    status: str
    conformant: None
    checks: dict[str, CheckOutcome]
    not_selected: list[str]
    limitations: list[str]

    def to_dict(self):
        """Return JSON-serializable report data, including per-check findings."""
        return asdict(self)


def validate_dataset(investigation, *, dataset_root=None, checks=("layout",), profile="draft"):
    """Run explicitly selected draft checks; a selected-check pass is not compliance.

    ``profile='draft'`` is the only supported profile and has no released
    specification version. Errors outrank incomplete results; advisory warnings
    do not change status. Unknown profile/check names are rejected.
    """
    if profile != "draft":
        raise ValueError(f"Unsupported profile {profile!r}; only 'draft' exists.")
    if isinstance(checks, str):
        raise ValueError("checks must be a non-empty iterable of check names, not a string.")
    selected = tuple(checks)
    if not selected or len(set(selected)) != len(selected) or any(name not in CHECKS for name in selected):
        raise ValueError(f"Choose distinct check names from {CHECKS}.")

    path = Path(investigation)
    root = Path(dataset_root) if dataset_root is not None else path.parent
    document = None
    read_error = None
    if any(name not in ("layout", "isa_tools") for name in selected):
        try:
            with path.open(encoding="utf-8-sig") as stream:
                document = json.load(stream)
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            read_error = f"Document could not be read: {exc}"

    outcomes = {}
    for name in selected:
        if name == "layout":
            from .layout import check_dataset
            result = check_dataset(path, dataset_root=root)
        elif name == "isa_tools":
            result = _check_isa_tools(path)
        elif read_error:
            result = CheckResult(warnings=[Issue(name, read_error)])
        elif name == "isa_schema":
            result = _check_isa_schema(document)
        elif name == "phm_protocols":
            from .phm_protocols import check_protocols
            result = check_protocols(document)
        elif name == "phm_metadata":
            from .phm_metadata import check_measurement_metadata
            result = check_measurement_metadata(document)
        elif name == "phm_experiment_type":
            from .phm_experiment_type import check_experiment_type
            result = check_experiment_type(document)
        elif name == "phm_sensors":
            from .phm_sensors import check_sensor_answers
            result = check_sensor_answers(document)
        else:
            from .phm_sensor_csv import check_sensor_csvs
            result = check_sensor_csvs(document, root)
        outcomes[name] = CheckOutcome.from_result(name, result)

    status = ("fail" if any(c.status == "fail" for c in outcomes.values()) else
              "incomplete" if any(c.status == "incomplete" for c in outcomes.values()) else "pass")
    return ValidationReport(
        profile=profile, specification_version=None, status=status, conformant=None,
        checks=outcomes, not_selected=[name for name in CHECKS if name not in outcomes],
        limitations=["Only selected experimental checks were run.",
                     "Full ISA-PHM conformance and scientific correctness were not checked.",
                     "Factor and other unrecognized file references are not checked."],
    )


def _check_isa_schema(document):
    from .isa_core import SchemaUnavailable, check_isa_core
    try:
        return CheckResult(errors=[Issue("isa-core-schema", message) for message in check_isa_core(document)])
    except SchemaUnavailable as exc:
        return CheckResult(warnings=[Issue("isa-core-schema", str(exc))])


def _check_isa_tools(path):
    from .isa_core import SchemaUnavailable
    from .isa_tools import validate_isa
    result = CheckResult()
    try:
        report = validate_isa(path)
        for item in report["errors"]:
            message = f"{item.get('message', 'ISA-tools error')}: {item.get('supplemental', '')} (code {item.get('code')})"
            (result.warnings if item.get("code") == 4002 else result.errors).append(Issue("isa-tools", message))
        for item in report["warnings"]:
            result.advisories.append(Issue("isa-tools", f"{item.get('message', 'Warning')}: {item.get('supplemental', '')} (code {item.get('code')})"))
        for message in report.get("logged_errors", []):
            result.warnings.append(Issue("isa-tools-log", f"ISA-tools reported: {message}"))
        if not report["completed"]:
            result.warnings.append(Issue("isa-tools", f"Validation incomplete: {report.get('exception') or 'ISA-tools stopped before its completion marker.'}"))
    except SchemaUnavailable as exc:
        result.warnings.append(Issue("isa-tools", str(exc)))
    return result
