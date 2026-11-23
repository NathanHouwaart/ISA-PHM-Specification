# Initial ISA-PHM interface audit — November 2026

> **Historical audit:** This is a snapshot of an earlier investigation. Findings and tool behavior may have changed. See the [specification guide](../README.md) and [open questions](../open-questions.md) for current information.

**Status: descriptive, incomplete, and non-normative.** This records observed
behavior and questions; it is not specification version 0.1 or a conformance
assessment. It does not conclude that a convention is absent from every part
of the paper or from ISA merely because this first review did not find it.

## Sources and scope

- Local paper `G:/ISA/Docs/ISA-PHM paper_final.pdf`, especially section 3.2
  (PDF pages 6–9) and Appendix A tables 2–3 (PDF pages 18–19).
- Backend working tree, branch `feature/measurement-metadata-units`, base
  commit `277c6c8`; particularly `app/converter/entrypoint.py`,
  `assay_graph.py`, `factor_mapping.py` and `normalization.py`.
- Wrapper working tree, same branch name, base commit `38c17a3`; particularly
  `isa_phm/extractor.py`, `parser.py`, `preprocessor.py`, and `integrator.py`.
- Wizard working tree, same branch name, base commit `ed2649d`; particularly
  `src/utils/conversionPayload.js` and measurement metadata validation.

**All three working trees contained uncommitted changes at audit time.** The
commit identifiers alone do not reproduce these observations. A reproducible
baseline requires deciding which changes to retain and recording released
versions. The Agent repository, complete Wizard behavior, all examples,
upstream ISA schemas and all downstream tools have not yet been audited.

The local paper is a project document and is not bundled into this repository.
Page numbers here refer to the PDF page numbers, which match its printed pages.

## 1. Paper: model and data conventions

| Topic | What the paper describes | Where |
| --- | --- | --- |
| Scope | PHM interpretation of ISA entities; distinguishes diagnostic and prognostic tests. | §3.2, p. 6 |
| Diagnostic study | An experiment is a study; its configuration, fault and operating conditions are represented using the source/sample and study factors. An assay describes a sensor/measurement for that study. | §3.2.2, pp. 7–8; Table 2 |
| Prognostic study and runs | A study may comprise multiple sequential runs on the same sample. Per-run data and evolving factor values are discussed. | §3.2.3, pp. 8–9; Table 3 |
| Measurement metadata | A measurement protocol provides sensor or measurement details; parameter values are associated with measurements. Examples include sampling rate, location and processing. | §3.2.2, p. 8; Tables 2–3 |
| Time references | The paper calls for a common time reference and consistent units across related time series; it describes a separate `<factor>_time_reference` study factor for a factor that refers to a file. | §3.2.3, p. 9 |
| Data files | The paper uses a CSV, timestamp-plus-single-measurement convention for explanation and tooling, but explicitly says ISA-PHM is not dependent on that measurement format and discusses pointers into larger files. | §3.2.1, pp. 6–7 |
| Serialization | The paper discusses both ISA-Tab and ISA-JSON. | §3.2.4, p. 9 |

These summaries are not a complete transcription of the paper. In particular,
the paper's examples of sampling rate or units do not by themselves settle
whether a particular JSON field is mandatory or how unknown values are encoded.

## 2. Observed Backend output and Wrapper consumption

The exact names below are **current implementation observations**, not approved
contract rules. Locations mean the ISA object containing `comments`. Values
are stored as strings in the observed generated JSON; `total_runs`, for
example, is serialized as `"1"`. The Backend sometimes emits empty comments.
No universal requirement or rule for duplicates, capitalization, absent values,
or unknown comments has been decided.

| ISA location and comment name | Backend currently writes | Wrapper observation | Review |
| --- | --- | --- | --- |
| Investigation: `ud_identifier` | User-provided investigation identifier; separate from the generated ISA `identifier`. | Extracted investigation `identifier` is the ISA `identifier`; no direct extraction of this comment was found in the inspected extractor. | Decide which identifier(s) are needed and semantics. |
| Investigation: `experiment_type` | Input experiment type, including empty text if absent. | Reads this exact name, defaulting to `unknown` if absent/empty. | Define values, scope and relation to study design descriptors. |
| Investigation: `license` | License text, including empty text if absent. | No direct extraction found in inspected extractor. | Decide representation and whether Wrapper should expose it. |
| Person: `orcid`, `author_id` | Contact ORCID and app contact ID. | Reads `orcid`; contact linkage also involves ISA identifiers. No direct `author_id` extraction found in inspected contact extractor. | Define identifier formats and linkage; compare existing ISA facilities. |
| Publication: `Corresponding author ID` | Corresponding contact ID. | Reads name case-insensitively after trimming and strips a leading `#` from the value. | Define references, casing, and missing/unresolvable contacts. |
| Study: `total_runs` | Run count encoded as a string. | No direct consumption found in inspected extractor; it builds runs from assay process sequences. | Define its relationship to actual runs and conflict behavior. |
| Measurement/processing protocol: `Sensor id` | Sensor identifier. | Reads this exact, case-sensitive spelling from protocol comments; measurement protocol is used for sensor identity. | Decide location, casing and whether this is needed in both protocols. |
| Protocol: `selected_measurement_protocol_id`, `selected_processing_protocol_id` | ID of the selected Wizard protocol, respectively, as text. | No direct extraction found in inspected protocol extractor. | Determine whether these app identifiers belong in a public format. |
| Assay: `sensor alias` | Sensor alias, falling back to its ID, if present. | Uses comment when nonempty; otherwise falls back to assay filename. Name is matched case-insensitively after trimming. | Decide identity versus display name and fallback rules. |
| Assay: `physical device id`, `physical device name`, `physical device model`, `physical device serial number`, `physical device datasheet` | Nonempty physical-device fields, when a device with an ID is supplied. | Exposes fields as sensor metadata; empty or missing values become `None`. Names are normalized to lowercase and trimmed. | Define grouping, identifier scope, conflict rules and optionality. |
| Assay: `datasheet` | Nonempty sensor datasheet path. | Exposes as sensor datasheet; missing/empty becomes `None`. | Decide path semantics and distinguish sensor and device datasheets. |
| Study factor: `description` | Nonempty description. | Reads it into factor metadata. Wrapper also supports a `unit` factor comment, but current Backend factor units use ISA unit annotations/factor values. | Decide preferred unit representation and legacy handling. |
| Source: `description`, `image` | Setup description and image references. | Not audited comprehensively. | Decide if and how these references form part of the profile. |
| Sample characteristics: `description`, `datasheet`, `component ID`, plus user comments | Component information and supplied free-form comments. | Not audited comprehensively. | Separate standardized fields from arbitrary user-defined comments. |

Evidence: Backend `entrypoint.py` and `assay_graph.py`; Wrapper `extractor.py`
(`_extract_protocol`, `_extract_assay`, `_extract_contact`, `_extract_publication`,
`_extract_factor`, `_extract_comment`). The observations about *no direct
extraction* are limited to these inspected paths, not a claim that no other
tool or raw-JSON access can retrieve the information.

### Example: currently generated comments

Serializing the Backend's `tests/fixtures/minimal_payload.json` produced this
illustrative fragment (the full ISA document contains additional fields):

```json
{
  "comments": [
    {"name": "ud_identifier", "value": "INV-001"},
    {"name": "experiment_type", "value": "Diagnostics"},
    {"name": "license", "value": ""}
  ]
}
```

Its first study included `{"name": "total_runs", "value": "1"}`;
its first assay included `{"name": "sensor alias", "value": "S1"}`.
This is evidence of serialization, **not a valid complete dataset fixture**.

## 3. Other interface details already visible

- A sensor's measured quantity is exported as the assay's ISA
  `measurementType` annotation. The optional quantity identifier is written
  to `termAccession`; the Wrapper reads it. This is not a comment field.
- Study-variable unit identifiers are serialized via ISA unit annotations;
  Wrapper extraction also supports a legacy factor `unit` comment. Exact
  interoperability and conflicting values need more audit.
- The Wizard currently uses an application-defined quaternion-component
  identifier alongside catalogue identifiers. Whether and how project-local
  terms are governed is undecided; it must not be described as a QUDT term.
- The Backend `IsaPhmInfo` schemas describe the **input payload**, not a full
  output ISA-PHM dataset schema. The Wrapper parser has optional ISA-tools
  structural validation, but that is not by itself a complete ISA-PHM or
  scientific-validity check.
- The Wrapper preprocessor resolves relative paths against a data root and
  contains compatibility logic for absolute Windows paths. The intended
  portable path contract, permissible external references, and behavior on
  ambiguity have not been agreed.
- The current Wrapper working tree preserves loaded CSV timestamps and may log
  a sampling-rate discrepancy assuming timestamps are in seconds. This does not
  establish that a time reference is shared, nor prove synchronization.

## 4. Decisions and investigations to queue

These are questions, not proposed retroactive requirements:

1. **Version and scope:** identify the ISA-JSON schema/version to build on;
   decide whether the first profile covers only ISA-JSON or also ISA-Tab,
   which is discussed in the paper.
2. **Data access:** define a portable path/reference contract and whether the
   profile allows file formats and in-file pointers beyond the current tools'
   common CSV workflow.
3. **Metadata contract:** review each comment and annotation above, including
   required versus optional, aliases, duplicates, identifiers, unknown values,
   and whether standardized ISA mechanisms offer better representations.
4. **Time and factors:** decide how to capture and validate common time
   references and file-valued study-factor references; compare the paper's
   `<factor>_time_reference` convention with current Wizard/Backend/Wrapper
   behavior before declaring a discrepancy resolved.
5. **Study/run semantics:** compare diagnostic and prognostic handling across
   the paper and tools, including multiple runs and per-run factor values.
6. **Validation:** define which checks require an ISA schema, profile rules,
   data access, or human judgment. The current experimental inspection utility
   is not yet a validator for any of these.
7. **Examples and compatibility:** build synthetic fixtures after decisions;
   record how unversioned existing datasets and old comment spellings are
   reported and handled.

## 5. Limitations

This audit has not yet proved ISA schema validity, measured paper-to-code
coverage, inspected every case in the real datasets, audited the Agent, or
run a full cross-repository conformance suite. The paper describes test
structure and use cases; the current code describes implementation behavior.
Both need a more systematic review before a normative profile can be released.
