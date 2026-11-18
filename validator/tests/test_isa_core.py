import importlib.util
import importlib.metadata
import json
import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

from validator.isa_core import JSONSCHEMA_VERSION, ISA_TOOLS_VERSION, SchemaUnavailable, check_isa_core

ROOT = Path(__file__).resolve().parents[2]
def has_pinned_dependencies():
    try:
        return (all(importlib.util.find_spec(name) for name in ("isatools", "jsonschema", "referencing"))
                and importlib.metadata.version("isatools") == ISA_TOOLS_VERSION
                and importlib.metadata.version("jsonschema") == JSONSCHEMA_VERSION)
    except importlib.metadata.PackageNotFoundError:
        return False


HAVE_DEPS = has_pinned_dependencies()


class SchemaAvailabilityTests(unittest.TestCase):
    def test_missing_pinned_dependency_is_not_a_pass(self):
        with patch("validator.isa_core.importlib.metadata.version", side_effect=importlib.metadata.PackageNotFoundError("isatools")):
            with self.assertRaises(SchemaUnavailable):
                check_isa_core({})


@unittest.skipUnless(HAVE_DEPS, "optional ISA schema dependencies are not installed")
class ISACoreTests(unittest.TestCase):
    def test_complete_example_passes_core_and_invalid_comment_fails(self):
        valid = json.loads((ROOT / "fixtures/isa-core-valid/sample.isa-phm.json").read_text(encoding="utf-8"))
        invalid = json.loads((ROOT / "fixtures/isa-core-invalid/sample.isa-phm.json").read_text(encoding="utf-8"))
        self.assertEqual(check_isa_core(valid), [])
        self.assertTrue(any("$.comments[0].value" in message for message in check_isa_core(invalid)))

    def test_modified_baseline_is_not_reported_as_a_pass(self):
        with patch("validator.isa_core.CORE_SCHEMA_SHA256", "0" * 64):
            with self.assertRaisesRegex(SchemaUnavailable, "differ from the pinned"):
                check_isa_core({})

    def test_command_reports_core_only_not_full_conformance(self):
        path = ROOT / "fixtures/isa-core-valid/sample.isa-phm.json"
        result = subprocess.run([sys.executable, "-m", "validator", str(path), "--isa-schema"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("process-graph rules were not checked", result.stdout)
        self.assertIn("Full ISA-PHM conformance", result.stdout)

    def test_command_returns_error_for_isa_schema_violation(self):
        path = ROOT / "fixtures/isa-core-invalid/sample.isa-phm.json"
        result = subprocess.run([sys.executable, "-m", "validator", str(path), "--isa-schema"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn("isa-core-schema", result.stdout)


if __name__ == "__main__":
    unittest.main()
