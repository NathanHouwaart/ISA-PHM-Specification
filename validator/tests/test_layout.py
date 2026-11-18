import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from validator.layout import check_dataset


class LayoutTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for name in ("Data", "Datasheets", "Images"):
            (self.root / name).mkdir()
        (self.root / "Data" / "file.csv").write_text("time,value\n0,1\n", encoding="utf-8")
        self.path = self.root / "example.isa-phm.json"
        self.write({"studies": [{"assays": [{"dataFiles": [{"name": "Data/file.csv", "type": "Raw Data File"}]}]}]})

    def write(self, value):
        self.path.write_text(json.dumps(value), encoding="utf-8")

    def test_good_layout_does_not_claim_full_validity(self):
        self.assertEqual(check_dataset(self.path).errors, [])
        result = subprocess.run([sys.executable, "-m", "validator", str(self.path)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        self.assertIn("Full ISA-PHM conformance", result.stdout)

    def test_color_is_optional_and_exit_codes_are_unchanged(self):
        normal = subprocess.run([sys.executable, "-m", "validator", str(self.path)], capture_output=True, text=True)
        colored = subprocess.run([sys.executable, "-m", "validator", str(self.path), "--color", "always"], capture_output=True, text=True)
        plain = subprocess.run([sys.executable, "-m", "validator", str(self.path), "--color", "never"], capture_output=True, text=True)
        self.assertEqual([normal.returncode, colored.returncode, plain.returncode], [0, 0, 0])
        self.assertNotIn("\033[", normal.stdout)
        self.assertIn("\033[32m[PASS]\033[0m", colored.stdout)
        self.assertIn("\033[33m[NOT CHECKED]\033[0m", colored.stdout)
        self.assertNotIn("\033[", plain.stdout)
        self.write({"studies": [{"assays": [{"dataFiles": [{"name": "Data/missing.csv"}]}]}]})
        failed = subprocess.run([sys.executable, "-m", "validator", str(self.path), "--color", "always"], capture_output=True, text=True)
        self.assertEqual(failed.returncode, 1)
        self.assertIn("\033[31m[FAIL]\033[0m", failed.stdout)

    def test_no_color_environment_is_respected_in_auto_mode(self):
        from validator.terminal import use_color
        from unittest.mock import patch
        with patch.dict(os.environ, {"NO_COLOR": "1"}), patch("sys.stdout.isatty", return_value=True):
            self.assertFalse(use_color("auto"))
            self.assertTrue(use_color("always"))

    def test_missing_folders_and_name_are_reported(self):
        (self.root / "Images").rmdir()
        other = self.root / "old.json"
        other.write_text("{}", encoding="utf-8")
        codes = [item.code for item in check_dataset(other).errors]
        self.assertIn("required-directory", codes)
        self.assertIn("investigation-name", codes)

    def test_explicit_root_rejects_nested_investigation(self):
        nested = self.root / "Data" / "nested.isa-phm.json"
        nested.write_text("{}", encoding="utf-8")
        self.assertIn("investigation-location", [item.code for item in check_dataset(nested, dataset_root=self.root).errors])

    def test_bad_and_nonobject_json(self):
        for text in ("{", "[]"):
            self.path.write_text(text, encoding="utf-8")
            self.assertTrue(check_dataset(self.path).errors)

    def test_documented_fixtures(self):
        fixtures = Path(__file__).resolve().parents[2] / "fixtures"
        self.assertEqual(check_dataset(fixtures / "layout-valid" / "sample.isa-phm.json").errors, [])
        self.assertIn("datafile-missing", [item.code for item in check_dataset(fixtures / "layout-invalid" / "sample.isa-phm.json").errors])

    def test_missing_external_wrong_directory_and_escape(self):
        for name, code in [("Data/missing.csv", "datafile-missing"), ("https://host/data.csv", "external-datafile"), (r"C:\data.csv", "external-datafile"), ("elsewhere/file.csv", "datafile-directory"), ("Data/../../outside.csv", "datafile-escape")]:
            with self.subTest(name=name):
                self.write({"studies": [{"assays": [{"dataFiles": [{"name": name}]}]}]})
                self.assertIn(code, [item.code for item in check_dataset(self.path).errors])

    def test_placeholder_does_not_require_a_fake_file(self):
        placeholder = {"name": "", "type": "Raw Data File", "comments": [{"name": "availability", "value": "not included"}]}
        self.write({"studies": [{"assays": [{"dataFiles": [placeholder, {"name": "Data/file.csv"}]}]}]})
        result = check_dataset(self.path)
        self.assertEqual(result.errors, [])
        self.assertEqual(result.warnings, [])

    def test_assay_datasheet_paths(self):
        (self.root / "Datasheets" / "sensor.pdf").write_bytes(b"example")
        for value, expected in [("./Datasheets/sensor.pdf", None), ("", None), ("Datasheets/missing.pdf", "datasheet-missing"), ("https://example.com/sensor.pdf", "datasheet-external"), (r"C:\sensor.pdf", "datasheet-external"), ("Data/file.csv", "datasheet-directory"), ("Datasheets/../../outside.pdf", "datasheet-escape")]:
            for name in ("datasheet", "physical device datasheet"):
                with self.subTest(value=value, name=name):
                    self.write({"studies": [{"assays": [{"dataFiles": [{"name": "Data/file.csv"}], "comments": [{"name": name, "value": value}]}]}]})
                    result = check_dataset(self.path)
                    codes = [issue.code for issue in result.errors]
                    self.assertIn(expected, codes) if expected else self.assertEqual(codes, [])

    def test_unreadable_assay_datasheet_value_is_not_silently_accepted(self):
        self.write({"studies": [{"assays": [{"dataFiles": [], "comments": [{"name": "datasheet", "value": {}}]}]}]})
        self.assertIn("datasheet-reference", [issue.code for issue in check_dataset(self.path).warnings])

    def test_source_image_and_characteristic_datasheet(self):
        image = self.root / "Images" / "setup.png"
        sheet = self.root / "Datasheets" / "part.pdf"
        image.write_bytes(b"image")
        sheet.write_bytes(b"sheet")
        source = {"comments": [{"name": "image", "value": "./Images/setup.png"}], "characteristics": [{"comments": [{"name": "datasheet", "value": "./Datasheets/part.pdf"}]}]}
        self.write({"studies": [{"assays": [], "materials": {"sources": [source], "samples": []}}]})
        self.assertEqual(check_dataset(self.path).errors, [])
        image.unlink()
        sheet.unlink()
        self.assertEqual({x.code for x in check_dataset(self.path).errors}, {"image-missing", "datasheet-missing"})

    def test_unreadable_assay_structure_is_reported_not_checked(self):
        self.write({"studies": [{}]})
        self.assertIn("assay-files", [item.code for item in check_dataset(self.path).warnings])
        result = subprocess.run([sys.executable, "-m", "validator", str(self.path)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)

    @unittest.skipUnless(hasattr(os, "symlink"), "symlinks unavailable")
    def test_symlink_outside_root_is_not_followed(self):
        with tempfile.TemporaryDirectory() as outside:
            (Path(outside) / "outside.csv").write_text("0,1", encoding="utf-8")
            try:
                (self.root / "Data" / "link.csv").symlink_to(Path(outside) / "outside.csv")
            except OSError as exc:
                self.skipTest(f"Cannot create symlinks: {exc}")
            self.write({"studies": [{"assays": [{"dataFiles": [{"name": "Data/link.csv"}]}]}]})
            self.assertIn("datafile-escape", [item.code for item in check_dataset(self.path).errors])


if __name__ == "__main__":
    unittest.main()
