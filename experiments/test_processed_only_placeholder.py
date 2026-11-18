"""Cross-repository experiment, not a normative ISA-PHM fixture.

Run from the specification repository with the Backend and Wrapper checked out
as sibling directories and their dependencies installed:
    python -m unittest experiments.test_processed_only_placeholder
"""

import io
import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BACKEND = ROOT / "ISA-PHM-Backend"
WRAPPER = ROOT / "ISA-PHM-Wrapper"
sys.path.insert(0, str(BACKEND))
sys.path.insert(0, str(WRAPPER))

from app.converter.entrypoint import create_isa_data  # noqa: E402
from isatools import isajson  # noqa: E402
from isa_phm import ISAWrapper  # noqa: E402
from isa_phm.errors import DataFileError  # noqa: E402
from validator.layout import check_dataset  # noqa: E402
from validator.phm_protocols import check_protocols  # noqa: E402


class ProcessedOnlyPlaceholderExperiment(unittest.TestCase):
    def test_protocol_checks_against_backend_output_modes(self):
        payload = json.loads((BACKEND / "tests/fixtures/minimal_payload.json").read_text(encoding="utf-8-sig"))
        for raw, processed in (("Data/raw.csv", ""), ("Data/raw.csv", "Data/processed.csv"), ("", "Data/processed.csv")):
            with self.subTest(raw=raw, processed=processed):
                data = copy.deepcopy(payload)
                run = data["studies"][0]["assay_details"][0]["runs"][0]
                run["raw_file_name"] = raw
                run["processed_file_name"] = processed
                document = json.loads(json.dumps(create_isa_data(data), cls=isajson.ISAJSONEncoder))
                result = check_protocols(document)
                self.assertEqual((result.errors, result.warnings), ([], []))

    def test_round_trip_and_wrapper_public_loading(self):
        payload = json.loads((BACKEND / "tests/fixtures/minimal_payload.json").read_text(encoding="utf-8-sig"))
        run = payload["studies"][0]["assay_details"][0]["runs"][0]
        run["raw_file_name"] = ""
        run["processed_file_name"] = "Data/processed.csv"
        investigation = json.loads(json.dumps(create_isa_data(payload), cls=isajson.ISAJSONEncoder))
        assay = investigation["studies"][0]["assays"][0]
        placeholder = next(item for item in assay["dataFiles"] if item["type"] == "Raw Data File")
        self.assertEqual(placeholder["name"], "")
        self.assertIn({"name": "availability", "value": "not included"}, placeholder["comments"])
        baseline = copy.deepcopy(investigation)
        old_assay = baseline["studies"][0]["assays"][0]
        old_assay["dataFiles"] = [item for item in old_assay["dataFiles"] if item["@id"] != placeholder["@id"]]
        processed_ref = old_assay["processSequence"][1]["outputs"][0]
        old_assay["processSequence"][0]["outputs"] = [processed_ref]
        old_assay["processSequence"][1]["inputs"] = [processed_ref]

        reloaded = isajson.load(io.StringIO(json.dumps(investigation)))
        round_trip = json.loads(json.dumps(reloaded, cls=isajson.ISAJSONEncoder))
        files = round_trip["studies"][0]["assays"][0]["dataFiles"]
        self.assertIn(placeholder, files)

        with tempfile.TemporaryDirectory(prefix="isa_phm_placeholder_") as directory:
            root = Path(directory)
            (root / "Data").mkdir()
            (root / "Datasheets").mkdir()
            (root / "Images").mkdir()
            (root / "Data" / "processed.csv").write_text("time,value\n0,1\n0.0000390625,2\n", encoding="utf-8")
            path = root / "investigation.isa-phm.json"
            path.write_text(json.dumps(round_trip), encoding="utf-8")
            self.assertEqual(check_dataset(path).errors, [])
            baseline_path = root / "baseline.json"
            baseline_path.write_text(json.dumps(baseline), encoding="utf-8")
            with baseline_path.open(encoding="utf-8") as stream:
                baseline_report = isajson.validate(stream)
            with path.open(encoding="utf-8") as stream:
                report = isajson.validate(stream)
            # The installed default ISA configuration does not recognize the
            # fixture's Vibration/Accelerometer combination. Compare errors;
            # this does not establish full ISA conformance or graph validity.
            self.assertEqual(report["errors"], baseline_report["errors"])
            wrapper = ISAWrapper(path, data_root=root)
            sensor = wrapper.study(1).assay(1)
            self.assertEqual(sensor.load_dataframe(file_type="processed")["value"].tolist(), [1, 2])
            self.assertEqual(sensor.load_dataframe(file_type="auto")["value"].tolist(), [1, 2])
            with self.assertRaisesRegex(DataFileError, "no 'raw' data file"):
                sensor.load_dataframe(file_type="raw")
            record = wrapper._investigation.studies[0].assays[0].runs[0]
            self.assertTrue(any(p.parameter_name.lower() == "sampling rate" for p in record.measurement_params))
            self.assertTrue(record.processed_file.path.endswith("processed.csv"))


if __name__ == "__main__":
    unittest.main()
