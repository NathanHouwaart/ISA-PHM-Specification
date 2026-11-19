"""Run preliminary dataset-layout checks, not complete conformance checks."""

import argparse
import json
from pathlib import Path
from .layout import check_dataset
from .terminal import label, use_color


def main() -> int:
    parser = argparse.ArgumentParser(description="Check selected draft ISA-PHM dataset-layout rules, not full conformance.")
    parser.add_argument("investigation", type=Path, help="Path to the investigation JSON file")
    parser.add_argument("--root", type=Path, help="Dataset root (defaults to the investigation's parent directory)")
    parser.add_argument("--isa-schema", action="store_true", help="Also check the pinned ISA 1.0 core JSON Schema (optional dependencies required)")
    parser.add_argument("--isa", action="store_true", help="Also run the ISA-tools validator with the experimental ISA-PHM configuration")
    parser.add_argument("--phm-protocols", action="store_true", help="Check experimental Backend-style measurement and processing relationships")
    parser.add_argument("--phm-metadata", action="store_true", help="Check for explicit measurement metadata answers in the current Backend mapping")
    parser.add_argument("--phm-experiment-type", action="store_true", help="Check experiment type in the current Wizard/Backend mapping")
    parser.add_argument("--phm-sensors", action="store_true", help="Check sensor quantity, technology and model answers in the current Backend mapping")
    parser.add_argument("--phm-sensor-csv", action="store_true", help="Stream referenced sensor CSV files and check their column counts")
    parser.add_argument("--color", choices=("auto", "always", "never"), default="auto", help="Terminal colors (default: auto)")
    args = parser.parse_args()
    result = check_dataset(args.investigation, dataset_root=args.root)
    isa_report = None
    isa_notes = []
    if args.phm_sensor_csv:
        from .phm_sensor_csv import check_sensor_csvs
        from .layout import Issue
        try:
            with args.investigation.open(encoding="utf-8-sig") as source:
                csv_result = check_sensor_csvs(json.load(source), args.root or args.investigation.parent)
            result.errors.extend(csv_result.errors)
            result.warnings.extend(csv_result.warnings)
        except (OSError, UnicodeError, json.JSONDecodeError):
            result.warnings.append(Issue("phm-csv-incomplete", "Document could not be read; sensor CSVs were not checked."))
    if args.phm_sensors:
        from .phm_sensors import check_sensor_answers
        from .layout import Issue
        try:
            with args.investigation.open(encoding="utf-8-sig") as source:
                sensor_result = check_sensor_answers(json.load(source))
            result.errors.extend(sensor_result.errors)
            result.warnings.extend(sensor_result.warnings)
        except (OSError, UnicodeError, json.JSONDecodeError):
            result.warnings.append(Issue("phm-sensors", "Document could not be read; sensor answers were not checked."))
    if args.phm_experiment_type:
        from .phm_experiment_type import check_experiment_type
        from .layout import Issue
        try:
            with args.investigation.open(encoding="utf-8-sig") as source:
                experiment_result = check_experiment_type(json.load(source))
            result.errors.extend(experiment_result.errors)
            result.warnings.extend(experiment_result.warnings)
        except (OSError, UnicodeError, json.JSONDecodeError):
            result.warnings.append(Issue("phm-experiment-type", "Document could not be read; experiment type was not checked."))
    if args.phm_metadata:
        from .phm_metadata import check_measurement_metadata
        try:
            with args.investigation.open(encoding="utf-8-sig") as source:
                metadata_result = check_measurement_metadata(json.load(source))
            result.errors.extend(metadata_result.errors)
            result.warnings.extend(metadata_result.warnings)
            result.advisories.extend(metadata_result.advisories)
        except (OSError, UnicodeError, json.JSONDecodeError):
            from .layout import Issue
            result.warnings.append(Issue("phm-metadata", "Document could not be read; measurement metadata was not checked."))
    if args.phm_protocols:
        from .phm_protocols import check_protocols
        try:
            with args.investigation.open(encoding="utf-8-sig") as source:
                phm_result = check_protocols(json.load(source))
            result.errors.extend(phm_result.errors)
            result.warnings.extend(phm_result.warnings)
        except (OSError, UnicodeError, json.JSONDecodeError):
            from .layout import Issue
            result.warnings.append(Issue("phm-protocols", "Document could not be read; protocol relationships were not checked."))
    schema_checked = False
    if args.isa_schema and not any(issue.code in {"json-read", "json-root"} for issue in result.errors):
        from .isa_core import SchemaUnavailable, check_isa_core
        from .layout import Issue
        try:
            with args.investigation.open(encoding="utf-8-sig") as source:
                errors = check_isa_core(json.load(source))
            schema_checked = True
            result.errors.extend(Issue("isa-core-schema", message) for message in errors)
        except (SchemaUnavailable, OSError, UnicodeError, json.JSONDecodeError) as exc:
            result.warnings.append(Issue("isa-core-schema", str(exc)))
    if args.isa:
        from .isa_core import SchemaUnavailable
        from .isa_tools import validate_isa
        from .layout import Issue
        if any(issue.code in {"json-read", "json-root"} for issue in result.errors):
            result.warnings.append(Issue("isa-tools", "Cannot run ISA-tools on an unreadable or invalid JSON document."))
        else:
            try:
                isa_report = validate_isa(args.investigation)
                for item in isa_report["errors"]:
                    message = f"{item.get('message', 'ISA-tools error')}: {item.get('supplemental', '')} (code {item.get('code')})"
                    # Missing configuration is not proof that the dataset is invalid.
                    target = result.warnings if item.get("code") == 4002 else result.errors
                    target.append(Issue("isa-tools", message))
                isa_notes = isa_report["warnings"]
                for message in isa_report.get("logged_errors", []):
                    result.warnings.append(Issue("isa-tools-log", f"ISA-tools reported: {message}"))
                if not isa_report["completed"]:
                    detail = isa_report.get("exception") or "ISA-tools stopped before its completion marker."
                    result.warnings.append(Issue("isa-tools", f"Validation incomplete: {detail}"))
            except SchemaUnavailable as exc:
                result.warnings.append(Issue("isa-tools", str(exc)))
    color = use_color(args.color)
    for issue in result.errors:
        print(f"{label('FAIL', color)} [{issue.code}]: {issue.message}")
    for issue in result.warnings:
        print(f"{label('NOT CHECKED', color)} [{issue.code}]: {issue.message}")
    for issue in result.advisories:
        print(f"{label('WARN', color)} [{issue.code}]: {issue.message}")
    for item in isa_notes:
        print(f"{label('WARN', color)} [isa-tools]: {item.get('message', 'Warning')}: {item.get('supplemental', '')} (code {item.get('code')})")
    layout_errors = [issue for issue in result.errors if issue.code != "isa-core-schema" and not issue.code.startswith(("phm-", "isa-tools"))]
    layout_unchecked = [issue for issue in result.warnings if issue.code != "isa-core-schema" and not issue.code.startswith(("phm-", "isa-tools"))]
    if not layout_errors and not layout_unchecked:
        print(f"{label('PASS', color)} Selected dataset-layout checks passed.")
    elif layout_unchecked and not layout_errors:
        print(f"{label('WARN', color)} Dataset-layout checks were incomplete.")
    if schema_checked and not any(issue.code == "isa-core-schema" for issue in result.errors):
        print(f"{label('PASS', color)} ISA 1.0 core JSON Schema passed.")
    if isa_report and isa_report["completed"] and not isa_report["errors"] and not isa_report.get("logged_errors"):
        print(f"{label('PASS', color)} ISA-tools validation completed without errors with the experimental PHM configuration.")
    if args.phm_protocols and not any(issue.code.startswith("phm-") and not issue.code.startswith(("phm-metadata", "phm-experiment-type", "phm-sensor", "phm-csv")) for issue in result.errors + result.warnings):
        print(f"{label('PASS', color)} Selected experimental ISA-PHM protocol relationship checks passed.")
    if args.phm_metadata and not any(issue.code.startswith("phm-metadata") for issue in result.errors + result.warnings):
        print(f"{label('PASS', color)} Selected experimental measurement metadata presence checks passed.")
    if args.phm_experiment_type and not any(issue.code == "phm-experiment-type" for issue in result.errors + result.warnings):
        print(f"{label('PASS', color)} Experimental experiment-type mapping check passed.")
    if args.phm_sensors and not any(issue.code.startswith("phm-sensor") for issue in result.errors + result.warnings):
        print(f"{label('PASS', color)} Experimental sensor answer presence checks passed.")
    if args.phm_sensor_csv and not any(issue.code.startswith("phm-csv") for issue in result.errors + result.warnings):
        print(f"{label('PASS', color)} Experimental sensor CSV column-count checks passed.")
    print(f"Selected checks: {len(result.errors)} error(s), {len(result.warnings)} item(s) not checked, {len(result.advisories)} advisory warning(s).")
    print(f"{label('NOT CHECKED', color)} Factor and other unrecognized file references; selected assay, source and characteristic references are checked.")
    if schema_checked:
        print("ISA 1.0 core JSON Schema was checked; ISA content, configuration, and process-graph rules were not checked by the schema check.")
    else:
        print(f"{label('NOT CHECKED', color)} Separate ISA core JSON Schema diagnostic (use --isa-schema with optional dependencies).")
    if not args.isa:
        print(f"{label('NOT CHECKED', color)} ISA-tools validator (use --isa with optional dependencies).")
    print(f"{label('NOT CHECKED', color)} Full ISA-PHM conformance and scientific correctness.")
    return 1 if result.errors else (2 if result.warnings else 0)


if __name__ == "__main__":
    raise SystemExit(main())
