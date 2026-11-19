import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from validator.phm_sensors import check_sensor_answers

ROOT = Path(__file__).resolve().parents[2]


class SensorAnswersTests(unittest.TestCase):
    def setUp(self):
        self.doc = json.loads((ROOT / "fixtures/isa-core-valid/sample.isa-phm.json").read_text(encoding="utf-8"))
        self.assay = self.doc["studies"][0]["assays"][0]

    def test_current_fixture_has_all_answers(self):
        result = check_sensor_answers(self.doc)
        self.assertEqual((result.errors, result.warnings), ([], []))

    def test_missing_or_blank_answers_fail(self):
        for field, value in (("measurementType", {"annotationValue": ""}), ("technologyType", None), ("technologyPlatform", "  ")):
            with self.subTest(field=field):
                doc = copy.deepcopy(self.doc)
                doc["studies"][0]["assays"][0][field] = value
                self.assertEqual(len(check_sensor_answers(doc).errors), 1)

    def test_explicit_unknown_and_technology_model_not_applicable(self):
        self.assay["measurementType"]["annotationValue"] = "Unknown"
        self.assay["technologyType"]["annotationValue"] = "Not applicable"
        self.assay["technologyPlatform"] = "Unknown"
        result = check_sensor_answers(self.doc)
        self.assertEqual((result.errors, result.warnings), ([], []))

    def test_quantity_not_applicable_and_malformed_fields_are_incomplete(self):
        for field, value in (("measurementType", {"annotationValue": "Not applicable"}), ("technologyType", "Accelerometer"), ("technologyPlatform", 7)):
            with self.subTest(field=field):
                doc = copy.deepcopy(self.doc)
                doc["studies"][0]["assays"][0][field] = value
                self.assertTrue(check_sensor_answers(doc).warnings)

    def test_unreadable_or_empty_studies_and_assays_are_incomplete(self):
        for doc in ({}, {"studies": []}, {"studies": [{"assays": []}]}, {"studies": [{"assays": [None]}]}):
            with self.subTest(doc=doc):
                self.assertTrue(check_sensor_answers(doc).warnings)

    def test_cli_reports_missing_sensor_answer(self):
        del self.assay["technologyPlatform"]
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for name in ("Data", "Datasheets", "Images"):
                (root / name).mkdir()
            (root / "Data/signal.csv").write_text("time,value\n0,1\n", encoding="utf-8")
            path = root / "sample.isa-phm.json"
            path.write_text(json.dumps(self.doc), encoding="utf-8")
            run = subprocess.run([sys.executable, "-m", "validator", str(path), "--phm-sensors", "--color", "never"], capture_output=True, text=True)
        self.assertEqual(run.returncode, 1, run.stdout + run.stderr)
        self.assertIn("[FAIL] [phm-sensor-answer]", run.stdout)


if __name__ == "__main__":
    unittest.main()
