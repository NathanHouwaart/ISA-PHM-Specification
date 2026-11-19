"""Command-line interface to the experimental shared validation API."""

import argparse
import json
from pathlib import Path

from . import validate_dataset
from .terminal import label, use_color


def main() -> int:
    parser = argparse.ArgumentParser(description="Check selected draft ISA-PHM rules, not full conformance.")
    parser.add_argument("investigation", type=Path, help="Path to the investigation JSON file")
    parser.add_argument("--root", type=Path, help="Dataset root (defaults to investigation's parent)")
    parser.add_argument("--isa-schema", action="store_true", help="Check the pinned ISA 1.0 core JSON Schema")
    parser.add_argument("--isa", action="store_true", help="Run ISA-tools with the experimental PHM configuration")
    parser.add_argument("--phm-protocols", action="store_true", help="Check experimental measurement and processing relationships")
    parser.add_argument("--phm-metadata", action="store_true", help="Check measurement metadata answers")
    parser.add_argument("--phm-experiment-type", action="store_true", help="Check current experiment-type mapping")
    parser.add_argument("--phm-sensors", action="store_true", help="Check sensor answer presence")
    parser.add_argument("--phm-sensor-csv", action="store_true", help="Stream sensor CSVs and check column counts")
    parser.add_argument("--profile", default="draft", choices=("draft",), help="Experimental profile (no released version yet)")
    parser.add_argument("--json", action="store_true", help="Output the structured report as JSON")
    parser.add_argument("--color", choices=("auto", "always", "never"), default="auto", help="Terminal colors (default: auto)")
    args = parser.parse_args()

    selected = ["layout"]
    for enabled, name in ((args.isa_schema, "isa_schema"), (args.isa, "isa_tools"),
                          (args.phm_protocols, "phm_protocols"), (args.phm_metadata, "phm_metadata"),
                          (args.phm_experiment_type, "phm_experiment_type"), (args.phm_sensors, "phm_sensors"),
                          (args.phm_sensor_csv, "phm_sensor_csv")):
        if enabled:
            selected.append(name)
    report = validate_dataset(args.investigation, dataset_root=args.root, checks=selected, profile=args.profile)
    if args.json:
        print(json.dumps(report.to_dict(), indent=2))
    else:
        _print_report(report, use_color(args.color))
    return {"pass": 0, "fail": 1, "incomplete": 2}[report.status]


def _print_report(report, color):
    titles = {
        "layout": "Selected dataset-layout checks passed.",
        "isa_schema": "ISA 1.0 core JSON Schema passed.",
        "isa_tools": "ISA-tools validation completed without errors with the experimental PHM configuration.",
        "phm_protocols": "Selected experimental ISA-PHM protocol relationship checks passed.",
        "phm_metadata": "Selected experimental measurement metadata presence checks passed.",
        "phm_experiment_type": "Experimental experiment-type mapping check passed.",
        "phm_sensors": "Experimental sensor answer presence checks passed.",
        "phm_sensor_csv": "Experimental sensor CSV column-count checks passed.",
    }
    for check in report.checks.values():
        for state, findings in (("FAIL", check.errors), ("NOT CHECKED", check.incomplete), ("WARN", check.advisories)):
            for issue in findings:
                print(f"{label(state, color)} [{issue.code}]: {issue.message}")
        if check.status == "pass":
            print(f"{label('PASS', color)} {titles[check.name]}")
    print(f"Selected checks: {sum(len(c.errors) for c in report.checks.values())} error(s), "
          f"{sum(len(c.incomplete) for c in report.checks.values())} item(s) not checked, "
          f"{sum(len(c.advisories) for c in report.checks.values())} advisory warning(s).")
    print(f"{label('NOT CHECKED', color)} Factor and other unrecognized file references; selected assay, source and characteristic references are checked.")
    if "isa_schema" in report.checks and report.checks["isa_schema"].status != "incomplete":
        print("ISA 1.0 core JSON Schema was checked; ISA content, configuration, and process-graph rules were not checked by the schema check.")
    else:
        print(f"{label('NOT CHECKED', color)} Separate ISA core JSON Schema diagnostic (use --isa-schema with optional dependencies).")
    if "isa_tools" not in report.checks:
        print(f"{label('NOT CHECKED', color)} ISA-tools validator (use --isa with optional dependencies).")
    print(f"{label('NOT CHECKED', color)} Full ISA-PHM conformance and scientific correctness.")


if __name__ == "__main__":
    raise SystemExit(main())
