"""Experimental, streaming column-count check for referenced sensor CSVs."""

import csv
from pathlib import Path, PurePosixPath, PureWindowsPath
import re

from .layout import CheckResult, Issue, _placeholder


def _check_file(result, path, name):
    try:
        with path.open(encoding="utf-8-sig", newline="") as stream:
            first = next((line for line in stream if line.strip()), None)
            if first is None:
                result.warnings.append(Issue("phm-csv-incomplete", f"'{name}' is empty; CSV convention was not checked."))
                return
            # Detect only an unambiguous separator in the first nonempty line.
            choices = []
            for delimiter in (",", ";", "\t", "|"):
                fields = next(csv.reader([first], delimiter=delimiter))
                if len(fields) > 1:
                    choices.append(delimiter)
            if len(choices) != 1:
                result.warnings.append(Issue("phm-csv-incomplete", f"'{name}': delimiter could not be determined unambiguously."))
                return
            stream.seek(0)
            reader = csv.reader(stream, delimiter=choices[0], strict=True)
            for row in reader:
                if not row or all(not cell.strip() for cell in row):
                    continue
                if len(row) != 2:
                    result.errors.append(Issue("phm-csv-columns", f"'{name}', line {reader.line_num}: expected two columns (time and one output), found {len(row)}."))
                    return
    except (OSError, UnicodeError, csv.Error) as exc:
        result.warnings.append(Issue("phm-csv-incomplete", f"'{name}' could not be fully read as UTF-8 CSV: {exc}"))


def check_sensor_csvs(document, dataset_root):
    """Inspect referenced raw/derived CSVs; do not infer time or value semantics."""
    result = CheckResult()
    root = Path(dataset_root).resolve()
    studies = document.get("studies") if isinstance(document, dict) else None
    if not isinstance(studies, list) or not studies:
        result.warnings.append(Issue("phm-csv-incomplete", "No readable studies; sensor CSVs were not checked."))
        return result
    seen = set()
    for si, study in enumerate(studies, 1):
        assays = study.get("assays") if isinstance(study, dict) else None
        if not isinstance(assays, list) or not assays:
            result.warnings.append(Issue("phm-csv-incomplete", f"Study {si}: no readable assays."))
            continue
        for ai, assay in enumerate(assays, 1):
            entries = assay.get("dataFiles") if isinstance(assay, dict) else None
            if not isinstance(entries, list) or not entries:
                result.warnings.append(Issue("phm-csv-incomplete", f"Study {si}, assay {ai}: no readable data files."))
                continue
            for entry in entries:
                if isinstance(entry, dict) and _placeholder(entry):
                    continue
                if not isinstance(entry, dict) or entry.get("type") not in ("Raw Data File", "Derived Data File"):
                    result.warnings.append(Issue("phm-csv-incomplete", f"Study {si}, assay {ai}: unsupported or unreadable file type."))
                    continue
                name = entry.get("name")
                if not isinstance(name, str) or not name.strip() or re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", name) or PureWindowsPath(name).is_absolute() or PurePosixPath(name).is_absolute():
                    result.warnings.append(Issue("phm-csv-incomplete", f"Study {si}, assay {ai}: unsafe or unreadable file reference; CSV not checked."))
                    continue
                parts = PurePosixPath(name.replace("\\", "/"))
                try:
                    if not parts.parts or parts.parts[0] != "Data":
                        raise ValueError("not under Data")
                    path = (root / Path(*parts.parts)).resolve()
                    path.relative_to((root / "Data").resolve())
                    path.relative_to(root)
                except (ValueError, OSError, RuntimeError):
                    result.warnings.append(Issue("phm-csv-incomplete", f"Study {si}, assay {ai}: unsafe or out-of-scope file reference; CSV not checked."))
                    continue
                if path in seen:
                    continue
                seen.add(path)
                if path.suffix.casefold() != ".csv" or not path.is_file():
                    result.warnings.append(Issue("phm-csv-incomplete", f"'{name}' is missing or not a CSV; content not checked."))
                    continue
                _check_file(result, path, name)
    if not seen and not result.warnings:
        result.warnings.append(Issue("phm-csv-incomplete", "No sensor files were available to check."))
    return result
