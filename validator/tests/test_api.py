import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from validator import validate_dataset
from validator.isa_core import SchemaUnavailable
from validator.layout import CheckResult, Issue


class ValidatorApiTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for folder in ("Data", "Datasheets", "Images"):
            (self.root / folder).mkdir()
        self.path = self.root / "example.isa-phm.json"
        self.path.write_text(json.dumps({"studies": []}), encoding="utf-8")

    def test_selected_pass_is_not_a_compliance_claim(self):
        report = validate_dataset(self.path)
        self.assertEqual(report.status, "pass")
        self.assertIsNone(report.specification_version)
        self.assertIsNone(report.conformant)
        self.assertEqual(report.checks["layout"].status, "pass")
        self.assertIn("isa_schema", report.not_selected)
        self.assertEqual(json.loads(json.dumps(report.to_dict()))["profile"], "draft")

    def test_failure_and_incomplete_are_distinct_and_failure_takes_precedence(self):
        missing = self.root / "missing.isa-phm.json"
        report = validate_dataset(missing, checks=("layout", "phm_sensors"))
        self.assertEqual(report.status, "fail")
        self.assertEqual(report.checks["layout"].status, "fail")
        self.assertEqual(report.checks["phm_sensors"].status, "incomplete")

    def test_missing_optional_dependency_does_not_pass(self):
        with patch("validator.isa_core.check_isa_core", side_effect=SchemaUnavailable("missing dependency")):
            report = validate_dataset(self.path, checks=("isa_schema",))
        self.assertEqual(report.status, "incomplete")
        self.assertIn("missing dependency", report.checks["isa_schema"].incomplete[0].message)

    def test_advisory_does_not_make_selected_check_incomplete(self):
        result = CheckResult(advisories=[Issue("example", "advice")])
        with patch("validator.phm_sensors.check_sensor_answers", return_value=result):
            report = validate_dataset(self.path, checks=("phm_sensors",))
        self.assertEqual(report.status, "pass")
        self.assertEqual(report.checks["phm_sensors"].advisories[0].code, "example")

    def test_rejects_unknown_profile_and_unknown_or_empty_checks(self):
        for kwargs in ({"profile": "1.0"}, {"checks": ("typo",)}, {"checks": ()}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                validate_dataset(self.path, **kwargs)

    def test_json_cli_agrees_with_api_and_never_claims_compliance(self):
        run = subprocess.run([sys.executable, "-m", "validator", str(self.path), "--json"], capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
        cli_report = json.loads(run.stdout)
        self.assertEqual(cli_report, validate_dataset(self.path).to_dict())
        self.assertIsNone(cli_report["conformant"])


if __name__ == "__main__":
    unittest.main()
