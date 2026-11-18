"""Selected draft layout checks; no claim of ISA-PHM or ISA conformance."""

from dataclasses import dataclass, field
import json
from pathlib import Path, PurePosixPath, PureWindowsPath
import re


@dataclass(frozen=True)
class Issue:
    code: str
    message: str


@dataclass
class CheckResult:
    errors: list[Issue] = field(default_factory=list)
    warnings: list[Issue] = field(default_factory=list)
    advisories: list[Issue] = field(default_factory=list)


def _placeholder(entry: dict) -> bool:
    return (
        str(entry.get("type") or "").strip().lower() == "raw data file"
        and not str(entry.get("name") or "").strip()
        and not str(entry.get("filename") or "").strip()
        and isinstance(entry.get("comments", []), list)
        and any(
            isinstance(comment, dict)
            and str(comment.get("name") or "").strip().lower() == "availability"
            and str(comment.get("value") or "").strip().lower() == "not included"
            for comment in (entry.get("comments") or [])
        )
    )


def _check_data_path(result: CheckResult, root: Path, entry: dict, location: str) -> None:
    if _placeholder(entry):
        return
    name = entry.get("name")
    if not isinstance(name, str) or not name.strip():
        result.warnings.append(Issue("datafile-name", f"{location}: no usable data-file name; its reference was not checked."))
        return
    if re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", name) or PureWindowsPath(name).is_absolute() or PurePosixPath(name).is_absolute():
        result.errors.append(Issue("external-datafile", f"{location}: '{name}' is not a dataset-root-relative file path."))
        return
    components = PurePosixPath(name.replace("\\", "/"))
    if not components.parts or components.parts[0] != "Data":
        result.errors.append(Issue("datafile-directory", f"{location}: '{name}' must be under Data/."))
        return
    try:
        target = (root / Path(*components.parts)).resolve()
        target.relative_to((root / "Data").resolve())
        target.relative_to(root)
    except (ValueError, OSError, RuntimeError):
        result.errors.append(Issue("datafile-escape", f"{location}: '{name}' resolves outside Data/ or the dataset root."))
        return
    if not target.is_file():
        result.errors.append(Issue("datafile-missing", f"{location}: referenced file '{name}' does not exist or is not a file."))


def _check_attachment_comments(result: CheckResult, root: Path, obj: dict, location: str, mapping: dict) -> None:
    """Check known Backend attachment comments when present; absence is permitted."""
    comments = obj.get("comments", [])
    if not isinstance(comments, list):
        result.warnings.append(Issue("attachment-comments", f"{location}: comments are unreadable; attachment references were not checked."))
        return
    for comment in comments:
        if not isinstance(comment, dict):
            continue
        name = comment.get("name")
        if not isinstance(name, str) or name.strip().lower() not in mapping:
            continue
        folder, prefix = mapping[name.strip().lower()]
        value = comment.get("value")
        if not isinstance(value, str):
            result.warnings.append(Issue(f"{prefix}-reference", f"{location}: {name} is not a readable path."))
            continue
        if not value.strip():
            continue
        if re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", value) or PureWindowsPath(value).is_absolute() or PurePosixPath(value).is_absolute():
            result.errors.append(Issue(f"{prefix}-external", f"{location}: '{value}' is not a dataset-root-relative path."))
            continue
        components = PurePosixPath(value.replace("\\", "/"))
        if not components.parts or components.parts[0] != folder:
            result.errors.append(Issue(f"{prefix}-directory", f"{location}: '{value}' must be under {folder}/."))
            continue
        try:
            target = (root / Path(*components.parts)).resolve()
            target.relative_to((root / folder).resolve())
            target.relative_to(root)
        except (ValueError, OSError, RuntimeError):
            result.errors.append(Issue(f"{prefix}-escape", f"{location}: '{value}' resolves outside {folder}/ or the dataset root."))
            continue
        if not target.is_file():
            result.errors.append(Issue(f"{prefix}-missing", f"{location}: referenced {prefix} '{value}' does not exist or is not a file."))


def check_dataset(investigation: Path, *, dataset_root: Path | None = None) -> CheckResult:
    """Check layout and discoverable assay dataFiles; other references are not checked."""
    result = CheckResult()
    path = Path(investigation).absolute()
    root = Path(dataset_root).resolve() if dataset_root is not None else path.parent.resolve()
    if path.parent.resolve() != root:
        result.errors.append(Issue("investigation-location", "Investigation must be directly inside the dataset root."))
    elif path.is_symlink() and not path.resolve().is_relative_to(root):
        result.errors.append(Issue("investigation-escape", "Investigation resolves outside the dataset root."))
    if not path.name.endswith(".isa-phm.json") or path.name == ".isa-phm.json":
        result.errors.append(Issue("investigation-name", "Investigation filename must have a name followed by .isa-phm.json."))
    for name in ("Data", "Datasheets", "Images"):
        folder = root / name
        if not folder.is_dir():
            result.errors.append(Issue("required-directory", f"Required directory '{name}/' is missing."))
        elif not folder.resolve().is_relative_to(root):
            result.errors.append(Issue("directory-escape", f"Required directory '{name}/' resolves outside the dataset root."))
    try:
        with path.open(encoding="utf-8-sig") as source:
            document = json.load(source)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        result.errors.append(Issue("json-read", f"Cannot read the investigation JSON: {exc}"))
        return result
    if not isinstance(document, dict):
        result.errors.append(Issue("json-root", "The investigation JSON root must be an object."))
        return result
    studies = document.get("studies")
    if not isinstance(studies, list):
        result.warnings.append(Issue("assay-files", "No studies list was found; assay data-file references were not checked."))
        return result
    for study_index, study in enumerate(studies):
        if not isinstance(study, dict) or not isinstance(study.get("assays"), list):
            result.warnings.append(Issue("assay-files", f"Study {study_index + 1} has no readable assays list; its data-file references were not checked."))
            continue
        materials = study.get("materials", {})
        if isinstance(materials, dict):
            for material_type in ("sources", "samples"):
                entries = materials.get(material_type, [])
                if not isinstance(entries, list):
                    result.warnings.append(Issue("attachment-comments", f"Study {study_index + 1}: {material_type} cannot be read for attachment references."))
                    continue
                for material in entries:
                    if not isinstance(material, dict):
                        result.warnings.append(Issue("attachment-comments", f"Study {study_index + 1}: a material is unreadable."))
                        continue
                    location = f"study {study_index + 1}, {material_type}"
                    if material_type == "sources":
                        _check_attachment_comments(result, root, material, location, {"image": ("Images", "image")})
                    characteristics = material.get("characteristics", [])
                    if not isinstance(characteristics, list):
                        result.warnings.append(Issue("attachment-comments", f"{location}: characteristics cannot be read."))
                        continue
                    for characteristic in characteristics:
                        if isinstance(characteristic, dict):
                            _check_attachment_comments(result, root, characteristic, location + " characteristic", {"datasheet": ("Datasheets", "datasheet")})
        else:
            result.warnings.append(Issue("attachment-comments", f"Study {study_index + 1}: materials cannot be read for attachment references."))
        for assay_index, assay in enumerate(study["assays"]):
            location = f"study {study_index + 1}, assay {assay_index + 1}"
            if isinstance(assay, dict):
                _check_attachment_comments(result, root, assay, location, {"datasheet": ("Datasheets", "datasheet"), "physical device datasheet": ("Datasheets", "datasheet")})
            if not isinstance(assay, dict) or not isinstance(assay.get("dataFiles"), list):
                result.warnings.append(Issue("assay-files", f"{location}: no readable dataFiles list; references were not checked."))
                continue
            for entry in assay["dataFiles"]:
                if not isinstance(entry, dict):
                    result.warnings.append(Issue("datafile-entry", f"{location}: a data-file entry is not an object and was not checked."))
                    continue
                _check_data_path(result, root, entry, location)
    return result
