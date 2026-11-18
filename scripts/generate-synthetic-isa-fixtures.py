"""Generate non-normative ISA-JSON schema fixtures from the sibling Backend.

This is a development helper, not required to use the saved fixtures. It
requires ISA-PHM-Backend and isatools 0.14.3; UUIDs change on regeneration.
The deliberately invalid example differs only by a non-string comment value.
"""
import copy
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT.parent / "ISA-PHM-Backend"
sys.path.insert(0, str(BACKEND))
from app.converter.entrypoint import create_isa_data  # noqa: E402
from isatools import isajson  # noqa: E402

payload = json.loads((BACKEND / "tests/fixtures/minimal_payload.json").read_text(encoding="utf-8-sig"))
payload["title"] = "Synthetic diagnostic bearing example"
assay = payload["studies"][0]["assay_details"][0]
assay["runs"][0]["raw_file_name"] = "Data/signal.csv"
assay["runs"][0]["processed_file_name"] = ""
investigation = json.loads(json.dumps(create_isa_data(payload), cls=isajson.ISAJSONEncoder))
invalid = copy.deepcopy(investigation)
invalid["comments"][0]["value"] = 42  # ISA comments require a string.
for folder, document in (("isa-core-valid", investigation), ("isa-core-invalid", invalid)):
    target = ROOT / "fixtures" / folder / "sample.isa-phm.json"
    target.write_text(json.dumps(document, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Generated {target.relative_to(ROOT)}")
