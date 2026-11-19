import tempfile
import unittest
import json
import subprocess
import sys
from pathlib import Path

from validator.phm_sensor_csv import check_sensor_csvs


class SensorCsvTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "Data").mkdir()
        self.path = self.root / "Data/signal.csv"
        self.doc = {"studies": [{"assays": [{"dataFiles": [{"name": "Data/signal.csv", "type": "Raw Data File"}]}]}]}

    def check(self, text):
        self.path.write_text(text, encoding="utf-8")
        return check_sensor_csvs(self.doc, self.root)

    def test_two_columns_with_or_without_headers_and_nonzero_times(self):
        for text in ("timestamp,value\n01:39:00.000,2\n", "12,4\n13,5\n", "time;value\n12;4\n"):
            with self.subTest(text=text):
                result = self.check(text)
                self.assertEqual((result.errors, result.warnings), ([], []))

    def test_three_columns_and_ragged_rows_fail(self):
        for text in ("time,x,y\n0,1,2\n", "time,value\n0,1\n1,2,3\n"):
            with self.subTest(text=text):
                self.assertTrue(self.check(text).errors)

    def test_empty_and_ambiguous_files_are_incomplete(self):
        for text in ("", "time\n1\n"):
            with self.subTest(text=text):
                self.assertTrue(self.check(text).warnings)

    def test_unavailable_placeholder_is_not_a_file(self):
        self.doc['studies'][0]['assays'][0]['dataFiles'].append({"name": "", "type": "Raw Data File", "comments": [{"name": "availability", "value": "not included"}]})
        self.assertFalse(self.check("time,value\n0,1\n").warnings)

    def test_external_paths_are_not_opened(self):
        for name in ("../outside.csv", "Data/../../outside.csv", "C:/outside.csv", "https://example.org/a.csv"):
            with self.subTest(name=name):
                self.doc['studies'][0]['assays'][0]['dataFiles'][0]['name'] = name
                self.assertTrue(check_sensor_csvs(self.doc, self.root).warnings)

    def test_non_csv_missing_and_unknown_type_are_incomplete(self):
        for entry in ({"name": "Data/x.wav", "type": "Raw Data File"}, {"name": "Data/missing.csv", "type": "Raw Data File"}, {"name": "Data/signal.csv", "type": "Other"}):
            with self.subTest(entry=entry):
                self.doc['studies'][0]['assays'][0]['dataFiles'] = [entry]
                self.assertTrue(check_sensor_csvs(self.doc, self.root).warnings)

    def test_cli_reports_column_failure(self):
        for name in ("Datasheets", "Images"):
            (self.root / name).mkdir()
        self.path.write_text("time,x,y\n0,1,2\n", encoding="utf-8")
        investigation = self.root / "sample.isa-phm.json"
        investigation.write_text(json.dumps(self.doc), encoding="utf-8")
        run = subprocess.run([sys.executable, "-m", "validator", str(investigation), "--phm-sensor-csv", "--color", "never"], capture_output=True, text=True)
        self.assertEqual(run.returncode, 1, run.stdout + run.stderr)
        self.assertIn("[FAIL] [phm-csv-columns]", run.stdout)


if __name__ == '__main__':
    unittest.main()
