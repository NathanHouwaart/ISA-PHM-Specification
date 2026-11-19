import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from validator.phm_experiment_type import check_experiment_type


class ExperimentTypeTests(unittest.TestCase):
    def test_current_wizard_values_pass(self):
        for value in ("diagnostic-experiment", "prognostics-experiment"):
            with self.subTest(value=value):
                result = check_experiment_type({"comments": [{"name": "experiment_type", "value": value}]})
                self.assertEqual((result.errors, result.warnings), ([], []))

    def test_missing_blank_and_conflicting_answers_fail(self):
        for comments in ([], [{"name": "experiment_type", "value": ""}], [
            {"name": "experiment_type", "value": "diagnostic-experiment"},
            {"name": "experiment_type", "value": "prognostics-experiment"},
        ]):
            with self.subTest(comments=comments):
                self.assertTrue(check_experiment_type({"comments": comments}).errors)

    def test_unknown_and_malformed_values_are_not_silently_classified(self):
        for comments in ([{"name": "experiment_type", "value": "Diagnostics"}],
                         [{"name": "experiment_type", "value": 3}],
                         [{"name": "experiment_type", "value": "diagnostic-experiment"}, 42],
                         None):
            with self.subTest(comments=comments):
                self.assertTrue(check_experiment_type({"comments": comments}).warnings)

    def test_identical_duplicate_is_incomplete_until_policy_is_decided(self):
        item = {"name": "experiment_type", "value": "diagnostic-experiment"}
        self.assertTrue(check_experiment_type({"comments": [item, item]}).warnings)

    def test_cli_explicit_option_fails_for_missing_type(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for name in ("Data", "Datasheets", "Images"):
                (root / name).mkdir()
            path = root / "sample.isa-phm.json"
            path.write_text(json.dumps({"comments": [], "studies": []}), encoding="utf-8")
            run = subprocess.run([sys.executable, "-m", "validator", str(path), "--phm-experiment-type", "--color", "never"], capture_output=True, text=True)
        self.assertEqual(run.returncode, 1, run.stdout + run.stderr)
        self.assertIn("[FAIL] [phm-experiment-type]", run.stdout)


if __name__ == "__main__":
    unittest.main()
