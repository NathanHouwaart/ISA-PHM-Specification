"""Experimental check of the current Wizard/Backend experiment-type mapping."""

from .layout import CheckResult, Issue


def check_experiment_type(document):
    """Check current exported values without guessing legacy classifications."""
    result = CheckResult()
    if not isinstance(document, dict) or not isinstance(document.get("comments", []), list):
        result.warnings.append(Issue("phm-experiment-type", "Investigation comments cannot be read; experiment type was not checked."))
        return result
    comments = document.get("comments", [])
    if any(not isinstance(item, dict) or not isinstance(item.get("name"), str) for item in comments):
        result.warnings.append(Issue("phm-experiment-type", "Investigation comments are malformed; experiment type cannot be checked unambiguously."))
        return result
    values = [item.get("value") for item in comments if item["name"] == "experiment_type"]
    if not values:
        result.errors.append(Issue("phm-experiment-type", "No experiment_type answer was recorded in the current Backend mapping."))
        return result
    if any(not isinstance(value, str) for value in values):
        result.warnings.append(Issue("phm-experiment-type", "An experiment_type answer is not readable text."))
        return result
    if any(not value.strip() for value in values):
        result.errors.append(Issue("phm-experiment-type", "An experiment_type answer is blank."))
        return result
    recognized = {"diagnostic-experiment", "prognostics-experiment"}
    if len(set(values) & recognized) == 2:
        result.errors.append(Issue("phm-experiment-type", "Conflicting diagnostic and prognostic experiment_type answers were recorded."))
    elif any(value not in recognized for value in values):
        result.warnings.append(Issue("phm-experiment-type", "An experiment_type value is outside the current Wizard mapping; legacy classification was not inferred."))
    elif len(values) > 1:
        result.warnings.append(Issue("phm-experiment-type", "Duplicate experiment_type answers need review; duplicate policy is not yet defined."))
    return result
