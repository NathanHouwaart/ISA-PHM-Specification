"""Experimental checks for the current ISA-JSON protocol representation."""

from .layout import CheckResult, Issue, _placeholder


def _ids(value):
    if not isinstance(value, list):
        return None
    if any(not isinstance(item, dict) or not isinstance(item.get("@id"), str) or not item["@id"] for item in value):
        return None
    return {item["@id"] for item in value}


def check_protocols(document):
    result = CheckResult()
    studies = document.get("studies") if isinstance(document, dict) else None
    if not isinstance(studies, list):
        result.warnings.append(Issue("phm-protocols", "Studies cannot be read; protocol relationships were not checked."))
        return result
    if not studies:
        result.warnings.append(Issue("phm-protocols", "No studies were available to check."))
    for si, study in enumerate(studies, 1):
        if not isinstance(study, dict) or not isinstance(study.get("protocols"), list) or not isinstance(study.get("assays"), list):
            result.warnings.append(Issue("phm-protocols", f"Study {si}: protocols or assays cannot be read."))
            continue
        if not study["assays"]:
            result.warnings.append(Issue("phm-protocols", f"Study {si}: no assays were available to check."))
        protocols = {}
        malformed_protocols = False
        for protocol in study["protocols"]:
            if not isinstance(protocol, dict) or not isinstance(protocol.get("@id"), str) or not protocol["@id"] or protocol["@id"] in protocols:
                malformed_protocols = True
                continue
            kind = protocol.get("protocolType")
            kind = kind.get("annotationValue") if isinstance(kind, dict) else None
            if not isinstance(kind, str) or not kind.strip():
                malformed_protocols = True
            protocols[protocol["@id"]] = kind
        for ai, assay in enumerate(study["assays"], 1):
            location = f"Study {si}, assay {ai}"
            malformed = malformed_protocols
            if malformed or not isinstance(assay, dict) or not isinstance(assay.get("dataFiles"), list) or not isinstance(assay.get("processSequence"), list):
                result.warnings.append(Issue("phm-protocols", f"{location}: files, processes or protocol identifiers cannot be read unambiguously."))
                continue
            files = {}
            for item in assay["dataFiles"]:
                if not isinstance(item, dict) or not isinstance(item.get("@id"), str) or not item["@id"] or item["@id"] in files:
                    malformed = True
                    break
                files[item["@id"]] = item
            if not files and not malformed:
                result.warnings.append(Issue("phm-protocols", f"{location}: no data files were available to check."))
            processes = []
            for process in assay["processSequence"]:
                if not isinstance(process, dict):
                    malformed = True
                    break
                ref = process.get("executesProtocol")
                ref = ref.get("@id") if isinstance(ref, dict) else None
                inputs, outputs = _ids(process.get("inputs")), _ids(process.get("outputs"))
                if not isinstance(ref, str) or ref not in protocols or inputs is None or outputs is None:
                    malformed = True
                    break
                processes.append((protocols[ref], inputs, outputs))
            if malformed:
                result.warnings.append(Issue("phm-protocols", f"{location}: files or process references cannot be read unambiguously."))
                continue
            measurements = [outputs for kind, _, outputs in processes if kind == "Measurement Protocol"]
            processing = [(inputs, outputs) for kind, inputs, outputs in processes if kind == "Processing Protocol"]
            for file_id, item in files.items():
                kind = item.get("type")
                if kind == "Raw Data File" and not _placeholder(item):
                    if not any(file_id in outputs for outputs in measurements):
                        result.errors.append(Issue("phm-measurement", f"{location}: raw file {file_id} has no measurement process output under the current mapping."))
                elif kind == "Derived Data File":
                    producers = [(inputs, outputs) for inputs, outputs in processing if file_id in outputs]
                    if not producers:
                        result.errors.append(Issue("phm-processing", f"{location}: derived file {file_id} has no processing process output under the current mapping."))
                        continue
                    for inputs, _ in producers:
                        if file_id in inputs:
                            result.errors.append(Issue("phm-processing-self-input", f"{location}: derived file {file_id} is its own processing input."))
                        raw_inputs = {key for key in inputs if key in files and files[key].get("type") == "Raw Data File"}
                        if not raw_inputs or not any(raw_inputs & outputs for outputs in measurements):
                            result.warnings.append(Issue("phm-lineage", f"{location}: cannot establish a measurement-to-processing raw input for {file_id} under the current mapping."))
                elif kind != "Raw Data File" and kind != "Derived Data File":
                    result.warnings.append(Issue("phm-file-type", f"{location}: file type {kind!r} is outside the current mapping and was not checked."))
    return result
