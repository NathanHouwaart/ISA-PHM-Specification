# First ISA-PHM release: readiness audit and backlog

Status: planning audit, not an approved standard or release. This document
summarizes the existing draft and implementation evidence; it does not turn
open questions into decisions. See the [draft profile](../draft-profile.md),
[decision index](../initial-audit.md), [implementation notes](../isa-json-implementation-notes.md),
and [Wrapper readiness audit](2026-11-wrapper-validation-readiness.md).

## Release outcome

Define a versioned ISA-PHM ISA-JSON baseline and a reference validator. A dataset
may be described as compliant with that version only when every required
automated check has completed successfully and the applicable non-automatable
requirements have been met by the responsible researcher. The validator must
distinguish pass, fail, and incomplete; it cannot establish scientific truth.
The version number and exact wording of claims remain to be chosen at release.

ISA-Tab and the global measurement timeline are outside this first baseline.
Deferral must not be represented as proof of synchronization or as an approval
of any particular diagnostic-window or timestamp convention.

## State of the draft

| Area | Established direction | What remains before release |
| --- | --- | --- |
| ISA foundation | ISA-JSON first; ISA model 1.0 core schema is a candidate baseline. | Approve baseline and define which ISA structural, content and graph checks are required; the experimental ISA-tools configuration supports only two measurement/technology pairs. |
| Dataset layout | Root investigation file ending `.isa-phm.json`; `Data/`, `Datasheets/`, `Images/`; internal relative references. | Define path separators, case and symlink policy, other documents and packaging of empty directories; cover all defined file references including factors. Layout validation exists for selected references. |
| Experiment type | Dataset is diagnostic or prognostic, not both. | Specify the JSON representation, accepted values, missing/conflicting behavior and automatic checks. Diagnostic windows are deferred, not equated to prognostic runs. |
| Sensor metadata | Included outputs answer measured quantity, technology, model, sampling rate and measured unit; unknown/not applicable are distinct where appropriate. | Finalize each field's representation, cardinality and permitted states; confirm run-specific behavior. The current metadata check covers presence of rate and measured unit, not full value validation. |
| Units and quantities | Shared draft catalogue with QUDT identifiers and documented local additions; no inferred measured units. | Specify supported identifier handling and units for numerical sampling rates. Custom units are a future workflow with limited support, not an implemented portable feature. Compatibility warning rules are deliberately incomplete. |
| Physical devices | Optional grouping with a dataset-unique device identifier when used. | Stabilize JSON mapping, duplicate/conflicting identifiers and interoperability tests. |
| Sensor-output files | First CSV convention: timestamp and one sensor output; multiple files per output. | Specify the checkable first-version CSV details, header and numeric handling and constraints on file/run association. Zero start and global synchronization remain provisional/deferred. |
| Factors | Scalar values are represented as factor values; time-varying conditions use referenced files. | Define file-valued factor paths and data format/time reference sufficiently for the first version, or explicitly defer support without declaring such datasets compliant. |
| Measurement/processing | Applicable measurement protocol required; processing protocol required for processed data; raw, processed, or both allowed. | Finalize graph mapping and unknown processing encoding, and validate associations. The selected processing description survived a real raw/processed XJTU export and Wrapper readback; processed-only placeholders remain provisional. |
| ISA extensions | Current comments and ontology annotations have been inventoried. | Adopt exact names, locations, types, multiplicity and missing/duplicate behavior for first-version fields; distinguish tool-specific comments from normative extensions. |
| Version and compatibility | New datasets should identify the version; older unversioned datasets must not silently acquire a conformance claim. | Define marker, values, placement, legacy assessment/migration, and unsupported versions. |
| Real examples | Current XJTU small subset passes selected checks. | Establish representative diagnostic, prognostic, raw/processed and factor examples, plus compact synthetic valid and invalid fixtures. A selected-check pass is not full compliance. |

## Implementation backlog, in dependency order

1. Write an explicit first-version rule inventory with stable rule IDs,
   normative wording, exact ISA-JSON mappings, severity and automatic versus
   researcher responsibilities. Reconcile the paper, existing decisions and
   Backend output; record disagreements rather than silently selecting one.
2. Resolve the material open decisions below and define version identification
   and legacy handling. Do not finalize future timeline design as a side effect.
3. Add a portable Python validator API and CLI sharing one implementation,
   with structured findings, rule IDs, version, checked scope, incomplete
   results and summarized repeated findings. Define how dependencies and pinned
   ISA schemas are installed and how unavailable checks affect results.
4. Implement every required machine-checkable rule and negative tests. Add
   compact fixtures for missing/unknown/not-applicable values, raw-only,
   raw-plus-processed and processed-only, versioning, references, CSVs,
   diagnostic and prognostic structures, and representative extensions.
   Distinguish synthetic fixtures from certified examples.
5. Test current Wizard/Backend exports and representative datasets against the
   reference validator, then fix the producer or profile when warranted.
   Include an end-to-end export-to-validator-to-Wrapper test. Tests must not
   require a developer's private local dataset or absolute path.
6. Integrate the same versioned validator in Wizard and Wrapper; Agent uses
   Wrapper results. Define safe behavior for invalid and legacy data, avoid
   silently inferring measurement metadata, and replace the misleading Wrapper
   `strict_validation` option only as part of a tested migration.
7. Release the specification, validator, fixtures and documentation together;
   pin consumer revisions and document upgrading and compatibility. Require a
   reproducible clean install and tests on supported platforms before release.

## Decisions requiring focused discussion

1. **Release scope and compatibility:** Which features are part of this first
   version, especially time-varying factors and processed-only data? How should
   unversioned legacy datasets be assessed or migrated?
2. **Conformance and version marker:** Where is the version recorded in ISA-JSON,
   and how do tools present an automated pass alongside researcher-attested
   requirements and unavailable checks?
3. **Minimum measurement-file contract:** What exactly can be required and
   checked now for CSVs without deciding the future global timeline? Local
   zero-start remains provisional, not a new requirement from this audit.
4. **ISA mapping for processed-only data:** Is the current marked pathless raw
   placeholder acceptable after ISA graph validation, or is another valid and
   semantically clearer representation needed?
5. **Required metadata and extensions:** Confirm the concrete encodings for
   mandatory answers, unknown/not-applicable and normative comment/annotation
   fields, including the boundary for custom units. Existing decisions specify
   intent, not all implementation details.

These are grouped decisions, not a requirement to ask every detail upfront.
Use existing evidence and make implementation-level choices where the intent is
already clear. Bring scientific or scope trade-offs to the maintainers.
