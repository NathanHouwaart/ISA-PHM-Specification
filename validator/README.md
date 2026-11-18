# Experimental dataset-layout validator

This is an early standalone validator for selected draft layout rules, **not a
full ISA or ISA-PHM conformance validator**. It checks:

- A readable JSON object with an investigation filename ending in `.isa-phm.json`.
- The `Data/`, `Datasheets/`, and `Images/` directories at the dataset root.
- Recognizable `studies[].assays[].dataFiles[].name` references: relative to
  the dataset root, inside `Data/`, and pointing to an existing file.
- The provisional pathless raw-data placeholder is not treated as a missing file.
- When present, assay comments `datasheet` and `physical device datasheet`
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
python -m validator path/to/investigation.json --color never
python -m unittest discover -s validator/tests
```

The optional `--isa-schema` check requires `python -m pip install -r
requirements-schema.txt`. It checks only the pinned ISA model 1.0 **core JSON
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

Exit status is 0 when the selected checks find no errors or uninspectable
entries; 1 means at least one checked rule failed; 2 means a selected check
could not be completed and no checked rule failed. Output identifies unchecked
areas. In particular, this tool does not check the
study-factor file paths or other unrecognized references, CSV content,
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
