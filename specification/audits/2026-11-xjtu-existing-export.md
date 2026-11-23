# Existing XJTU-SY export: exploratory check

> **Historical audit:** This is a snapshot of an earlier investigation. Findings and tool behavior may have changed. See the [specification guide](../README.md) and [open questions](../open-questions.md) for current information.

This is an exploratory, read-only check of the local existing
`XJTU-SY_Bearing_Datasets/ISA-PHM-Out.json` and its sibling `Data/` folder.
It is **not** a fresh Wizard-to-Backend export or a certification of the XJTU
dataset. The current local Wizard, Backend, Wrapper and specification working
trees are not all represented by released commits. Dataset content is not
copied into this repository.

## Findings

- The existing JSON passed the pinned ISA core JSON Schema and the selected
  experimental Backend-style measurement/processing relationship checks.
- It failed the draft filename and folder checks: its name does not end in
  `.isa-phm.json`, and `Datasheets/` and `Images/` are missing. The JSON
  references specific datasheets and images that are not in these directories.
  We did not infer whether those files were absent from the original export or
  subsequently moved; we did not alter the dataset.
- ISA-tools did not finish its full check. It logged undeclared unit-reference
  errors for RPM and N but did not include them in its returned errors list.
  The IDs in the log use `#ontology_annotation/...` while declared study unit
  categories use `#unit/...`; the cause and whether this is an exporter or
  ISA-tools compatibility issue require further investigation.
- The Wrapper loaded the first raw run of each of the four assays: each CSV
  had 32,768 rows, `time` and `value` columns, and first timestamp 0. It
  required an explicit run ID because each assay has multiple runs. This
  confirms only those four loads, not the rest of the files or their meaning.
- At the time of the initial check, the Wrapper resolved the first run's sampling frequency from `25.6 kHz` to
  `25600 Hz`. It also returned `°` as the measured unit, citing the `Sensor
  Orientation` parameter, even though that is the unit of orientation and not
  an explicitly declared measured unit for the vibration output. This is a
  confirmed false inference in the current Wrapper's `resolve_measured_unit`
  fallback. The Wrapper has since been changed to accept only the explicit
  `Measured Unit` parameter; a repeat check now reports this unit as not
  provided and does not add it to plot labels. The dataset itself is unchanged.
- Wrapper preprocessing logged duplicate unit IDs. Their cause and impact
  were not established in this check.

Run `scripts/check-existing-dataset.py` with the investigation path and
`--root <dataset-root>` to repeat the selected validator and first-run Wrapper
checks. This script reads files only; its Wrapper inspection currently uses
internal objects and is a diagnostic, not a stable public API example.

## Still needed

Generate a fresh export from an actual Wizard project, run it through the
Backend, validator and Wrapper, and retain an appropriate small reproducible
fixture if permitted. Separately investigate the ISA-tools unit-reference
finding. Do not normalize, rename or fabricate
files in the existing dataset merely to make the checks pass.
