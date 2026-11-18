import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from validator.phm_metadata import check_measurement_metadata

ROOT = Path(__file__).resolve().parents[2]


class MeasurementMetadataTests(unittest.TestCase):
    def setUp(self):
        self.doc = json.loads((ROOT / "fixtures/isa-core-valid/sample.isa-phm.json").read_text(encoding="utf-8"))
        study = self.doc["studies"][0]
        self.process = study["assays"][0]["processSequence"][0]
        protocol_id = self.process["executesProtocol"]["@id"]
        self.protocol = next(p for p in study["protocols"] if p["@id"] == protocol_id)

    def add_unit(self, value):
        self.protocol["parameters"].append({"@id": "#measured", "parameterName": {"annotationValue": "Measured Unit"}})
        self.process["parameterValues"].append({"category": {"@id": "#measured"}, "value": value})

    def test_missing_measured_unit_fails_presence_check(self):
        result = check_measurement_metadata(self.doc)
        self.assertTrue(any("measured unit" in x.message for x in result.errors))

    def test_explicit_catalogue_unit_and_statuses_count_as_answers(self):
        for value in ({"annotationValue": "g", "termAccession": "http://qudt.org/vocab/unit/G"}, "Unknown", "Not applicable"):
            with self.subTest(value=value):
                doc, protocol, process = copy.deepcopy((self.doc, self.protocol, self.process))
                protocol["parameters"].append({"@id": "#measured", "parameterName": {"annotationValue": "Measured Unit"}})
                process["parameterValues"].append({"category": {"@id": "#measured"}, "value": value})
                result = check_measurement_metadata(doc)
                self.assertEqual((result.errors, result.warnings), ([], []))

    def test_missing_rate_and_blank_unit_are_reported(self):
        self.process["parameterValues"].clear()
        self.add_unit("")
        result = check_measurement_metadata(self.doc)
        self.assertEqual(len(result.errors), 2)

    def test_unresolved_category_is_not_passed_as_valid(self):
        self.add_unit("g")
        self.process["parameterValues"].append({"category": {"@id": "#missing"}, "value": "something"})
        result = check_measurement_metadata(self.doc)
        self.assertTrue(result.warnings)

    def test_duplicate_conflicting_unit_values_are_not_silently_passed(self):
        self.add_unit("g")
        self.process["parameterValues"].append({"category": {"@id": "#measured"}, "value": "Unknown"})
        self.assertTrue(any(x.code == "phm-metadata-conflict" for x in check_measurement_metadata(self.doc).warnings))

    def test_acceleration_and_mass_warn_but_do_not_fail(self):
        self.doc["studies"][0]["assays"][0]["measurementType"]["termAccession"] = "http://qudt.org/vocab/quantitykind/Acceleration"
        self.add_unit({"annotationValue": "g", "termAccession": "http://qudt.org/vocab/unit/GM"})
        result = check_measurement_metadata(self.doc)
        self.assertEqual((result.errors, result.warnings), ([], []))
        self.assertEqual([x.code for x in result.advisories], ["phm-quantity-unit"])
        self.process["parameterValues"][-1]["value"]["termAccession"] = "http://qudt.org/vocab/unit/G"
        self.assertEqual(check_measurement_metadata(self.doc).advisories, [])
        self.process["parameterValues"][-1]["value"]["termAccession"] = "urn:custom:unit"
        self.assertEqual(check_measurement_metadata(self.doc).advisories, [])

    def test_wizard_pinned_rules_match_when_checkout_exists(self):
        wizard_rules = ROOT.parent / "ISA-PHM-Wizard/vendor/isa-phm-specification/specification/quantity-unit-warning-rules.json"
        if not wizard_rules.exists():
            self.skipTest("Wizard checkout unavailable")
        spec_rules = ROOT / "specification/quantity-unit-warning-rules.json"
        self.assertEqual(json.loads(spec_rules.read_text(encoding="utf-8")), json.loads(wizard_rules.read_text(encoding="utf-8")))

    def test_mismatch_is_a_nonblocking_cli_warning(self):
        self.doc["studies"][0]["assays"][0]["measurementType"]["termAccession"] = "http://qudt.org/vocab/quantitykind/Acceleration"
        self.add_unit({"annotationValue": "g", "termAccession": "http://qudt.org/vocab/unit/GM"})
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for folder in ("Data", "Datasheets", "Images"):
                (root / folder).mkdir()
            (root / "Data/signal.csv").write_text("time,value\n0,1\n", encoding="utf-8")
            path = root / "sample.isa-phm.json"
            path.write_text(json.dumps(self.doc), encoding="utf-8")
            run = subprocess.run([sys.executable, "-m", "validator", str(path), "--phm-metadata", "--color", "never"], capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
        self.assertIn("[WARN] [phm-quantity-unit]", run.stdout)


if __name__ == "__main__":
    unittest.main()
