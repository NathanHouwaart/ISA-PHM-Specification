"""Read-only check of an existing exported dataset and its first run per assay.

Requires the sibling ISA-PHM-Wrapper and its dependencies. It does not drive
the Wizard, regenerate the export, or claim complete dataset conformance.
"""
import argparse
import json
from pathlib import Path
import subprocess
import sys

SPEC = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SPEC / "../ISA-PHM-Wrapper"))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("investigation", type=Path)
    parser.add_argument("--root", type=Path, required=True)
    args = parser.parse_args()
    investigation, root = args.investigation.resolve(), args.root.resolve()
    validation = subprocess.run([sys.executable, "-m", "validator", str(investigation), "--root", str(root), "--isa-schema", "--isa", "--phm-protocols", "--color", "never"], cwd=SPEC)
    print(f"Validator exit code: {validation.returncode}", flush=True)

    from isa_phm import ISAWrapper
    from isa_phm.capabilities import resolve_measured_unit, resolve_sampling_frequency

    wrapper = ISAWrapper(investigation, data_root=root)
    findings = []
    for si, study in enumerate(wrapper._investigation.studies, 1):
        for ai, assay in enumerate(study.assays, 1):
            if not assay.runs:
                findings.append({"study": si, "assay": ai, "error": "no runs"})
                continue
            run = assay.runs[0]
            info = {"study": si, "assay": ai, "run": run.run_id,
                    "sampling_frequency": resolve_sampling_frequency(run.measurement_params).model_dump(),
                    "measured_unit": resolve_measured_unit(run.measurement_params).model_dump()}
            try:
                frame = wrapper.study(si).assay(ai).run(run.run_id).load_dataframe(file_type="raw")
                info.update(rows=len(frame), columns=list(frame.columns), first_time=float(frame.iloc[0]["time"]))
            except Exception as exc:
                info["error"] = f"{type(exc).__name__}: {exc}"
            findings.append(info)
    print(json.dumps(findings, indent=2, ensure_ascii=True))
    return 1 if validation.returncode or any("error" in x for x in findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
