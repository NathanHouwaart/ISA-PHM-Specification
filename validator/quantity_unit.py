"""Load the draft compatibility advisory rules for the validator."""

import json
from .resources import resource_path

_RULES_PATH = resource_path("specification/quantity-unit-warning-rules.json")
RULES = json.loads(_RULES_PATH.read_text(encoding="utf-8"))["rules"]


def quantity_unit_warnings(quantity_identifier, unit_identifier):
    """Return explicit matching advisories; an empty result does not prove compatibility."""
    return [rule["message"] for rule in RULES
            if quantity_identifier in rule["quantityIdentifiers"] and unit_identifier in rule["unitIdentifiers"]]
