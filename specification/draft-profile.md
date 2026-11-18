# ISA-PHM profile: working draft

**Draft, not a released standard or an approved ISA-PHM version.** This page
brings together decisions reached so far. Some rules still need an ISA-JSON
mapping, validation design, compatibility assessment or implementation in the
tools. Where this draft and the current code differ, neither is silently
assumed to be correct: the difference must be reviewed.

## Relationship to ISA

ISA-PHM is a PHM-specific profile built on ISA. Its conceptual model is not
tied to one serialization. ISA-JSON will be the first fully specified and
testable serialization. ISA-Tab is outside the first release's scope, not
declared invalid. The candidate baseline for structural experiments is the
ISA model 1.0 core JSON Schema bundled with ISA-tools 0.14.3; see the
[schema baseline](../schemas/README.md). This is a pinned implementation
baseline for testing, not yet a finalized profile release.

## Dataset layout

```text
dataset-root/
├── <chosen-name>.isa-phm.json
├── Data/
├── Datasheets/
└── Images/
```

The investigation file is at the dataset root. The three directories are
required even when empty. Referenced dataset files must be within the root and
paths to them are relative to it. `Data/` contains measurement and other data
files; its subfolder layout is flexible. Datasheets go in `Datasheets/` and
images in `Images/`. External file references are out of scope in the first
release; this does not prohibit publication DOIs or ontology identifiers.

The investigation filename may vary but ends in `.isa-phm.json`. Multiple
investigation files, separators, case rules, symbolic links, other documents,
and how empty directories are preserved in packages remain open decisions.

## Experiment and measurement concepts

A dataset is classified as diagnostic or prognostic, not both. Detailed rules
for studies and runs, especially diagnostic measurement windows, remain open
for review with domain colleagues and the global timeline design.

The first sensor-output CSV convention uses two columns: time first and the
value of one sensor output second. An XYZ accelerometer has separate outputs.
An output can have several files, associated with runs where applicable. CSV
headers, timestamp units, references and zero-start behavior are not yet
specified. The profile is not inherently restricted to CSV; conventions for
other file formats may be specified later.

Scalar operating conditions and fault labels are represented directly as study
factor values. Time-varying operating conditions are represented by referenced
time-series CSV files. Their detailed format and time reference remain open.

## Sensor metadata and physical devices

For each sensor output included in the dataset, explicit answers are intended
for measured quantity, technology type, model, sampling rate and measured unit.
Unknown and not-applicable states may be used where appropriate; their exact
encodings and validation rules remain open. An unused channel physically
present in a device need not be described.

Physical-device metadata is optional. Where grouping is provided, outputs of
the same physical device share a dataset-unique device identifier, which a
tool may generate automatically. The exact ISA representation remains open.

Versioned unit and quantity catalogues are planned in this repository, based on
an adopted QUDT version with clearly labelled local additions. Custom units or
quantities are an exceptional option and should travel with the dataset with
their name, description and identifier. Automated support may be limited.
Quantity–unit relationships should guide suggestions and warnings; a missing
catalogue relationship alone should not automatically invalidate a combination.

## Raw and processed data

An included measurement may have raw data, processed data, or both. Measurement
metadata remains necessary for processed-only data; processed data also needs
an applicable processing protocol. When raw and processed files are available,
the raw file is the processing input and the processed file is its output.

A provisional Backend/Wrapper convention represents an unavailable raw input
using a marked placeholder. It remains under review and is not established as
a final ISA representation. Processing that changes units or sampling rate is
also an open modelling question.

## Validation and compatibility

Format checks, data-reference checks, and scientific correctness are distinct.
No tool can establish the accuracy of all researcher-provided metadata from
JSON structure alone. The validator checks selected layout rules described in
[its README](../validator/README.md), and optionally the pinned ISA core JSON
Schema or ISA-tools validator with an experimental PHM configuration. These
checks do not yet cover the full ISA-PHM profile.

New datasets are intended to declare a specification version, but the marker
and versioning details are not yet final. Existing unversioned datasets must
not silently be treated as conforming to a particular specification version.
Tools may offer compatibility handling separately from conformance checks.

## Sources and open work

See the [decision index](initial-audit.md), [interface audit](audits/2026-11-initial-interface-audit.md)
and [timeline note](future-work/global-measurement-timeline.md). The current
Wizard, Backend and Wrapper need alignment and have not yet been certified
against this draft.
