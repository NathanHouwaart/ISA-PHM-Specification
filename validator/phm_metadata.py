"""Experimental presence checks for the current ISA-PHM measurement representation."""

from .layout import CheckResult, Issue
from .quantity_unit import quantity_unit_warnings


def _answer(value):
    if isinstance(value, dict):
        value = value.get("annotationValue")
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return str(value)
    return ""


def check_measurement_metadata(document):
    """Check explicit answers; do not validate numerical values or catalogue semantics."""
    result = CheckResult()
    studies = document.get("studies") if isinstance(document, dict) else None
    if not isinstance(studies, list) or not studies:
        result.warnings.append(Issue("phm-metadata", "No readable studies; measurement metadata was not checked."))
        return result
    for si, study in enumerate(studies, 1):
        if not isinstance(study, dict) or not isinstance(study.get("protocols"), list) or not isinstance(study.get("assays"), list):
            result.warnings.append(Issue("phm-metadata", f"Study {si}: protocols or assays cannot be read."))
            continue
        protocols = {}
        duplicate = False
        for protocol in study["protocols"]:
            if not isinstance(protocol, dict) or not isinstance(protocol.get("@id"), str) or not protocol["@id"] or protocol["@id"] in protocols:
                duplicate = True
                continue
            protocols[protocol["@id"]] = protocol
        if not study["assays"]:
            result.warnings.append(Issue("phm-metadata", f"Study {si}: no assays available to check."))
        for ai, assay in enumerate(study["assays"], 1):
            loc = f"Study {si}, assay {ai}"
            if duplicate or not isinstance(assay, dict) or not isinstance(assay.get("processSequence"), list):
                result.warnings.append(Issue("phm-metadata", f"{loc}: process or protocol references are ambiguous."))
                continue
            count = 0
            mismatch_reported = set()
            for pi, process in enumerate(assay["processSequence"], 1):
                ref = process.get("executesProtocol") if isinstance(process, dict) else None
                ref = ref.get("@id") if isinstance(ref, dict) else None
                if not isinstance(ref, str) or ref not in protocols:
                    result.warnings.append(Issue("phm-metadata", f"{loc}, process {pi}: protocol reference cannot be resolved."))
                    continue
                protocol = protocols[ref]
                kind = protocol.get("protocolType")
                kind = kind.get("annotationValue") if isinstance(kind, dict) else None
                if not isinstance(kind, str) or not kind:
                    result.warnings.append(Issue("phm-metadata", f"{loc}, process {pi}: protocol type cannot be read."))
                    continue
                if kind != "Measurement Protocol":
                    continue
                count += 1
                parameters, values = protocol.get("parameters"), process.get("parameterValues")
                if not isinstance(parameters, list) or not isinstance(values, list):
                    result.warnings.append(Issue("phm-metadata", f"{loc}, process {pi}: parameter definitions or values cannot be read."))
                    continue
                definitions = {}
                malformed = False
                for item in parameters:
                    if not isinstance(item, dict) or not isinstance(item.get("@id"), str) or not item["@id"] or item["@id"] in definitions:
                        malformed = True
                        break
                    name = item.get("parameterName")
                    name = name.get("annotationValue") if isinstance(name, dict) else None
                    if not isinstance(name, str):
                        malformed = True
                        break
                    definitions[item["@id"]] = " ".join(name.casefold().split())
                answers = {"sampling rate": [], "measured unit": []}
                for item in values:
                    category = item.get("category") if isinstance(item, dict) else None
                    category = category.get("@id") if isinstance(category, dict) else None
                    if not isinstance(category, str) or category not in definitions:
                        malformed = True
                        break
                    name = definitions[category]
                    if name == "sampling frequency":
                        name = "sampling rate"
                    if name in answers:
                        answers[name].append(_answer(item.get("value")))
                        if name == "measured unit" and isinstance(item.get("value"), dict) and _answer(item["value"]).casefold() not in {"", "unknown", "not applicable"}:
                            quantity = assay.get("measurementType")
                            quantity_id = quantity.get("termAccession") if isinstance(quantity, dict) else None
                            unit_id = item["value"].get("termAccession")
                            for message in quantity_unit_warnings(quantity_id, unit_id):
                                if (quantity_id, unit_id) not in mismatch_reported:
                                    result.advisories.append(Issue("phm-quantity-unit", f"{loc}: {message}"))
                                    mismatch_reported.add((quantity_id, unit_id))
                if malformed:
                    result.warnings.append(Issue("phm-metadata", f"{loc}, process {pi}: parameter references cannot be resolved unambiguously."))
                    continue
                for name, entries in answers.items():
                    if not entries or any(not entry for entry in entries):
                        result.errors.append(Issue("phm-metadata-answer", f"{loc}, process {pi}: {name} has no explicit answer."))
                    elif len({entry.casefold() for entry in entries}) > 1:
                        result.warnings.append(Issue("phm-metadata-conflict", f"{loc}, process {pi}: multiple {name} answers need review."))
            if not count:
                result.warnings.append(Issue("phm-metadata", f"{loc}: no readable measurement process was found."))
    return result
