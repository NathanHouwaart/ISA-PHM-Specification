import copy
import json
import unittest
from pathlib import Path

from validator.phm_protocols import check_protocols

ROOT = Path(__file__).resolve().parents[2]


class ProtocolTests(unittest.TestCase):
    def setUp(self):
        self.document = json.loads((ROOT / "fixtures/isa-core-valid/sample.isa-phm.json").read_text(encoding="utf-8"))
        self.study = self.document["studies"][0]
        self.assay = self.study["assays"][0]

    def add_processed(self):
        raw = self.assay["dataFiles"][0]
        self.assay["dataFiles"].append({"@id": "#derived", "name": "Data/processed.csv", "type": "Derived Data File"})
        protocol = next(p for p in self.study["protocols"] if p["protocolType"]["annotationValue"] == "Processing Protocol")
        self.assay["processSequence"].append({"executesProtocol": {"@id": protocol["@id"]}, "inputs": [{"@id": raw["@id"]}], "outputs": [{"@id": "#derived"}]})

    def test_raw_and_raw_plus_processed(self):
        self.assertEqual(check_protocols(self.document).errors, [])
        self.add_processed()
        result = check_protocols(self.document)
        self.assertEqual((result.errors, result.warnings), ([], []))

    def test_processed_only_with_provisional_placeholder(self):
        self.add_processed()
        raw = self.assay["dataFiles"][0]
        raw.update(name="", comments=[{"name": "availability", "value": "not included"}])
        result = check_protocols(self.document)
        self.assertEqual((result.errors, result.warnings), ([], []))

    def test_missing_measurement_and_processing_are_failures(self):
        self.assay["processSequence"] = []
        self.assay["dataFiles"].append({"@id": "#derived", "name": "Data/proc.csv", "type": "Derived Data File"})
        self.assertEqual({x.code for x in check_protocols(self.document).errors}, {"phm-measurement", "phm-processing"})

    def test_self_input_and_missing_lineage(self):
        self.add_processed()
        self.assay["processSequence"][-1]["inputs"] = [{"@id": "#derived"}]
        result = check_protocols(self.document)
        self.assertIn("phm-processing-self-input", [x.code for x in result.errors])
        self.assertIn("phm-lineage", [x.code for x in result.warnings])

    def test_unresolved_protocol_and_unknown_type_are_incomplete(self):
        self.assay["processSequence"][0]["executesProtocol"]["@id"] = "#missing"
        self.assertIn("phm-protocols", [x.code for x in check_protocols(self.document).warnings])
        document = copy.deepcopy(self.document)
        document["studies"][0]["assays"][0]["dataFiles"][0]["type"] = "Other"
        document["studies"][0]["assays"][0]["processSequence"] = []
        self.assertIn("phm-file-type", [x.code for x in check_protocols(document).warnings])


if __name__ == "__main__":
    unittest.main()
