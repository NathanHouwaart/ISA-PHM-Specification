"""Experimental sensor answer checks for the current ISA-PHM assay representation."""

from .layout import CheckResult, Issue


def check_sensor_answers(document):
    """Check answer presence, not catalogue membership or scientific truth."""
    result = CheckResult()
    studies = document.get("studies") if isinstance(document, dict) else None
    if not isinstance(studies, list) or not studies:
        result.warnings.append(Issue("phm-sensors", "No readable studies; sensor answers were not checked."))
        return result
    for si, study in enumerate(studies, 1):
        assays = study.get("assays") if isinstance(study, dict) else None
        if not isinstance(assays, list) or not assays:
            result.warnings.append(Issue("phm-sensors", f"Study {si}: no readable assays; sensor answers were not checked."))
            continue
        for ai, assay in enumerate(assays, 1):
            loc = f"Study {si}, assay {ai}"
            if not isinstance(assay, dict):
                result.warnings.append(Issue("phm-sensors", f"{loc}: assay cannot be read."))
                continue
            for field, label, annotation in (("measurementType", "measured quantity", True), ("technologyType", "technology type", True), ("technologyPlatform", "sensor model", False)):
                value = assay.get(field)
                if value is None:
                    result.errors.append(Issue("phm-sensor-answer", f"{loc}: {label} has no explicit answer."))
                    continue
                if annotation:
                    if not isinstance(value, dict):
                        result.warnings.append(Issue("phm-sensors", f"{loc}: {label} is not a readable ontology annotation."))
                        continue
                    value = value.get("annotationValue")
                    if value is None:
                        result.errors.append(Issue("phm-sensor-answer", f"{loc}: {label} has no explicit answer."))
                        continue
                if not isinstance(value, str):
                    result.warnings.append(Issue("phm-sensors", f"{loc}: {label} is not readable text."))
                elif not value.strip():
                    result.errors.append(Issue("phm-sensor-answer", f"{loc}: {label} has no explicit answer."))
                elif field == "measurementType" and value.strip().casefold() == "not applicable":
                    result.warnings.append(Issue("phm-sensors", f"{loc}: not-applicable measured quantity is outside the current draft decision; its treatment is not checked."))
    return result
