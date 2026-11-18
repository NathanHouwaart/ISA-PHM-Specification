import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from validator.isa_core import SchemaUnavailable
from validator.isa_tools import validate_isa
from test_isa_core import HAVE_DEPS

ROOT = Path(__file__).resolve().parents[2]
VALID = ROOT / "fixtures/isa-core-valid/sample.isa-phm.json"
INVALID = ROOT / "fixtures/isa-core-invalid/sample.isa-phm.json"


class WorkerFailureTests(unittest.TestCase):
    def test_unreadable_worker_result_is_unavailable(self):
        with patch("validator.isa_tools._schema_directory"), patch("validator.isa_tools.subprocess.run") as run:
            run.return_value.returncode = 0
            run.return_value.stdout = "not json"
            with self.assertRaises(SchemaUnavailable):
                validate_isa(VALID)

    def test_incomplete_worker_result_is_not_a_pass(self):
        report = {"errors": [], "warnings": [], "completed": False, "exception": "unexpected error"}
        with patch("validator.isa_tools.validate_isa", return_value=report), patch.object(sys, "argv", ["validator", str(VALID), "--isa"]):
            from validator.__main__ import main
            self.assertEqual(main(), 2)

    def test_log_only_error_is_not_silently_lost(self):
        report = {"errors": [], "warnings": [], "completed": False, "exception": None,
                  "logged_errors": ["(E) unit was not declared"]}
        with patch("validator.isa_tools.validate_isa", return_value=report), patch.object(sys, "argv", ["validator", str(VALID), "--isa"]), patch("builtins.print") as output:
            from validator.__main__ import main
            self.assertEqual(main(), 2)
        self.assertIn("unit was not declared", "\n".join(str(call) for call in output.call_args_list))


@unittest.skipUnless(HAVE_DEPS, "optional ISA dependencies are not installed")
class OfficialValidatorTests(unittest.TestCase):
    def test_valid_fixture_completes_and_surfaces_warnings(self):
        report = validate_isa(VALID)
        self.assertTrue(report["completed"], report)
        self.assertEqual(report["errors"], [])
        self.assertTrue(report["warnings"])

    def test_invalid_fixture_fails(self):
        result = subprocess.run([sys.executable, "-m", "validator", str(INVALID), "--isa", "--color", "never"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("[FAIL] [isa-tools]", result.stdout)
        self.assertNotIn("ISA-tools validation completed without errors", result.stdout)

    def test_unknown_configuration_is_incomplete_not_invalid(self):
        document = json.loads(VALID.read_text(encoding="utf-8"))
        document["studies"][0]["assays"][0]["measurementType"]["annotationValue"] = "Unknown measurement"
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sample.isa-phm.json"
            path.write_text(json.dumps(document), encoding="utf-8")
            report = validate_isa(path)
        self.assertFalse(report["completed"])
        self.assertTrue(any(item.get("code") == 4002 for item in report["errors"]), report)


if __name__ == "__main__":
    unittest.main()
