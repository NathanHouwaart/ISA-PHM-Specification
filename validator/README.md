# Experimental dataset-layout validator

This is an early standalone validator for selected draft layout rules, **not a
full ISA or ISA-PHM conformance validator**. It checks:

- A readable JSON object with an investigation filename ending in `.isa-phm.json`.
- The `Data/`, `Datasheets/`, and `Images/` directories at the dataset root.
- Recognizable `studies[].assays[].dataFiles[].name` references: relative to
  the dataset root, inside `Data/`, and pointing to an existing file.
- The provisional pathless raw-data placeholder is not treated as a missing file.
- When present, assay comments `datasheet`, `physical_device_datasheet` and its legacy spelling `physical device datasheet`
  reference existing files under `Datasheets/`. Blank or absent comments are
  allowed; these checks do not require a datasheet or inspect its content.
- Source `image` comments and source/sample characteristic `datasheet`
  comments are checked when present, under `Images/` and `Datasheets/` respectively.

If the investigation's parent is not the intended dataset root, supply `--root`
so the location check can identify that. The tool avoids following a reference
outside the root; the final specification's symbolic-link policy remains open.
Windows-style separators are interpreted for these preliminary checks; their
normative representation has not been decided.

```bash
python -m validator path/to/investigation.json
python -m validator path/to/investigation.json --root path/to/dataset-root
python -m validator path/to/investigation.json --isa-schema
python -m validator path/to/investigation.json --isa
python -m validator path/to/investigation.json --phm-protocols
python -m validator path/to/investigation.json --phm-metadata
python -m validator path/to/investigation.json --phm-experiment-type
python -m validator path/to/investigation.json --phm-sensors
python -m validator path/to/investigation.json --phm-sensor-csv
python -m validator path/to/investigation.json --isa-schema --phm-metadata --json
python -m validator path/to/investigation.json --color never
python -m unittest discover -s validator/tests
```

## Python API

Install from a checkout with `python -m pip install .`, or install a built
wheel with `python -m pip install path/to/isa_phm_validator-0.1.0.dev0-py3-none-any.whl`.
Use `python -m pip install ".[isa]"` from a checkout to include the pinned
optional ISA dependencies. Both the `isa-phm-validate` command and
`python -m validator` provide the CLI. The same implementation can be called
directly from Python:

```python
from validator import validate_dataset

report = validate_dataset(
    "path/to/dataset.isa-phm.json",
    checks=("layout", "isa_schema", "phm_protocols", "phm_metadata"),
    profile="draft",
)
print(report.status)  # pass, fail, or incomplete for the selected checks
print(report.checks["phm_metadata"].errors)
print(report.not_selected)
print(report.to_dict())  # JSON-serializable data
```

`checks` defaults to `("layout",)`; see `validator.CHECKS` for all check
names. Each result separates errors, incomplete findings and non-blocking
advisories. A failure takes precedence over incomplete checks in the overall
status, but both remain visible in the report. Unknown check names and profile
names are rejected. The CLI's `--json` emits the same structured report and
uses the same exit statuses as the text interface.

`draft` is a development profile, **not a specification release**: reports
currently set `specification_version` and `conformant` to `null`, including
when selected checks pass. The package version identifies the validator build,
not a released specification. The Wizard and Wrapper do not yet call this API. Optional ISA
checks still require the pinned dependencies described below.

The optional `--isa-schema` check requires the `isa` extra above (or, from a
checkout, `python -m pip install -r requirements-schema.txt`). It checks only the pinned ISA model 1.0 **core JSON
Schema**, offline, and reports an incomplete check if the pinned package or
schema fingerprint is unavailable. See [the baseline](../schemas/README.md).

The optional `--isa` runs the actual ISA-tools 0.14.3 validator with this
repository's **experimental** PHM configuration, including ISA content and
process-graph checks. It requires the same optional dependencies. It currently
recognizes only the declared Vibration/Accelerometer and
Acceleration/Accelerometer combinations: another combination is reported as
not checked, not as evidence that the dataset is invalid. The configuration
is a preliminary interoperability test, not a complete ISA-PHM profile.
ISA-tools warnings are displayed as warnings and do not alone change the exit
code. If ISA-tools stops before completion, the result is incomplete even if
its own `validation_finished` flag says otherwise.
Some ISA-tools checks log an error without including it in their returned error
list. These log-only findings are surfaced as not checked rather than silently
lost; they need investigation before being classified as profile violations.

The pinned ISA-tools version has an assay study-group logging defect: it reads
an identifier that its assay model does not provide. The isolated worker gives
the assay a display label derived from its filename so that check can complete;
it does not change the input or disable the check. The validator runs in a
separate process because ISA-tools uses global state.

`--phm-protocols` selects preliminary measurement and processing relationship
checks for the current Backend mapping. It is not a complete PHM validator;
its exact scope and limitations are documented in the [implementation notes](../specification/isa-json-implementation-notes.md).

`--phm-metadata` checks for explicit sampling-rate and measured-unit answers
on measurement processes using the current Backend mapping. `Unknown` and
`Not applicable` count as explicit answers, not known numerical values or
units. A narrow set of known incompatible identifier pairs produces
non-blocking warnings (currently acceleration with gram/kilogram). Missing,
unlisted and custom identifiers are not assumed compatible or invalid. The
check does not comprehensively validate sampling rates, unit identifiers,
quantity/unit compatibility, or scientific correctness.

`--phm-experiment-type` checks the investigation's `experiment_type` comment
against the current Wizard values `diagnostic-experiment` and
`prognostics-experiment`. Missing, blank or conflicting recognized answers
fail this experimental mapping check. Unknown legacy values, malformed
comments and duplicate identical answers are reported as not checked: aliases
and duplicate policy have not been decided. This does not inspect study design
descriptors or establish that the recorded research purpose is correct; the
mapping is not yet an approved versioned requirement.

`--phm-sensors` checks for explicit answers in each assay's current Backend
mapping: measured quantity in `measurementType.annotationValue`, technology
type in `technologyType.annotationValue`, and model in `technologyPlatform`.
Missing or blank answers fail the check. Unknown is accepted for all three;
not applicable is accepted for technology and model, but is not checked for
quantity because its treatment is not established. Malformed or unreadable
structures are reported as not checked. The check does not determine which
outputs are included, verify ontology identifiers, confirm the answers are
scientifically correct, or validate optional physical-device grouping.

`--phm-sensor-csv` streams referenced raw and derived sensor CSV files and
checks that each nonblank row has exactly two columns. It detects a single
unambiguous comma, semicolon, tab or pipe delimiter from the first nonblank
line; this is an experimental reader choice, not a finalized delimiter rule.
Empty, non-CSV, missing, unreadable, ambiguous and unsupported references are
reported as not checked. The marked unavailable-raw placeholder is skipped.
Files are read only after resolving them within the dataset's `Data/` directory.
This check can take time on large datasets. It does not establish whether the
first column is time, the second is the correct sensor, whether a header is
present, numeric format, timestamp units, zero-start, sampling regularity or
synchronization. It does not inspect CSV files referenced by study factors.

Exit status is 0 when the selected checks find no errors or uninspectable
entries; 1 means at least one checked rule failed; 2 means a selected check
could not be completed and no checked rule failed. Output identifies unchecked
areas. In particular, this tool does not check the
study-factor file paths or other unrecognized references, most CSV content,
protocol content, quantities, units, timing, or scientific
correctness. ISA content and process-graph checks run only with `--isa`;
`--isa-schema` is a separate structural diagnostic. A zero exit status does **not** mean a complete or ISA-PHM-conforming
dataset. The default layout checks require no third-party Python packages.

## Terminal colors

Interactive terminals show green `[PASS]`, red `[FAIL]`, and yellow `[WARN]`
or `[NOT CHECKED]` labels. Color is disabled automatically for redirected
output, terminals that do not support it, and when `NO_COLOR` is set. Use
`--color always` to force ANSI color or `--color never` to disable it; these
explicit options override automatic detection. Status labels and exit codes
remain available without color.
