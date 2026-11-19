# Candidate first-release rule inventory

**Working inventory, not a released or complete standard.** IDs below are
provisional traceability labels; they are not yet public validator codes.
"Direction" refers to an existing project decision, not finalized normative
wording. Observed Backend fields are not automatically mandatory. The release
must define its complete scope, mappings, and human responsibilities before a
compliance claim is possible.

Coverage describes the current validator, not what a future validator will do.
Checks behind `--isa-schema`, `--phm-protocols`, or `--phm-metadata` are
optional today. An incomplete check must not be counted as a pass. See
[validator documentation](../validator/README.md), [field inventory](isa-json-field-inventory.md),
[implementation notes](isa-json-implementation-notes.md), and the
[release backlog](audits/2026-11-first-release-backlog.md).

## Dataset, ISA and version

| Candidate ID and direction | ISA-JSON / filesystem mapping | Current coverage and remaining work |
| --- | --- | --- |
| `BASE-01` Investigation is readable ISA-JSON. | JSON document; candidate ISA model 1.0 core schema. | Layout checks readability and JSON object; optional `--isa-schema` checks the pinned core schema only. Decide required ISA content and graph validation and baseline version. |
| `BASE-02` Declare a supported ISA-PHM version. | Marker and placement undecided. | Not checked. Define exact marker, unknown/newer version behavior, legacy assessment and release wording. |
| `BASE-03` Classify a dataset as diagnostic or prognostic, not both. | Current Backend uses investigation comment `experiment_type` and a study design descriptor. | Optional `--phm-experiment-type` checks the current Wizard comment values; legacy values and duplicate identical comments are incomplete. Study descriptor consistency, normative aliases and research purpose are not checked. Decision 0012. |
| `LAY-01` Place the investigation at the dataset root with a nonempty name ending `.isa-phm.json`. | Dataset root and filename, not a JSON field. | Layout checks `investigation-location` and `investigation-name`; an explicit root is needed to detect a wrong root. Decisions 0003 and 0005. |
| `LAY-02` Include root directories `Data/`, `Datasheets/`, `Images/`, including when empty. | Filesystem, not JSON. | Layout checks `required-directory` and directory escape; packaging of empty directories and portable case handling need specification. Decision 0004. |
| `LAY-03` Dataset file references are internal and root-relative. | Assay `dataFiles[].name`; selected source, characteristic and assay attachment comments; file-valued factors. | Checks known assay and attachment references for path, containment and existence; factor and unrecognized references remain unchecked. Define separator and symbolic-link policy. Decisions 0003 and 0004. |

## Studies, factors and sensor outputs

| Candidate ID and direction | Observed mapping | Current coverage and remaining work |
| --- | --- | --- |
| `STU-01` Model studies and runs appropriate to experiment purpose. | `studies`, `assays`, processes and current `total_runs` comment. | ISA core schema covers structure only; detailed diagnostic/prognostic study/run semantics and mappings remain unresolved. Do not treat diagnostic windows as prognostic runs. |
| `FAC-01` Record scalar operating conditions and fault labels directly as factor values. | Sample `factorValues`, study factor definitions and unit annotations. | No dedicated check; settle mappings, scalar types and association rules. Decision 0006. |
| `FAC-02` Reference a CSV for a time-varying operating condition. | File-valued factor mapping still needs specification. | Not checked. Define first-release scope, references, content and time reference or explicitly defer support. Decision 0006. |
| `SEN-01` Each included output has an explicit measured-quantity answer. | Assay `measurementType.annotationValue`, optionally `termAccession`. | Optional `--phm-sensors` checks answer presence on each assay under the current mapping, but not inclusion, identifiers or custom-quantity policy. Not-applicable quantity remains incomplete. Decision 0011. |
| `SEN-02` Each included output has explicit technology and model answers. | Assay `technologyType.annotationValue` and `technologyPlatform`. | Optional `--phm-sensors` checks answer presence on each assay; exact state encodings and consistency with physical devices remain open. Decision 0016. |
| `SEN-03` Each included output has explicit sampling-rate and measured-unit answers; distinguish known, unknown and not applicable. | Measurement protocol definitions and process `parameterValues` by category `@id`; `Sampling Rate`, `Measured Unit`. | `--phm-metadata` checks presence for recognizable measurement processes, reports ambiguous/unreadable structures as incomplete, and does not validate numerical rate, units, variable sampling or comprehensive identifiers. Decision 0009. |
| `SEN-04` Use recorded measured unit, not inference from unrelated parameters. | Current measured-unit parameter value and optional `termAccession`; rate unit is separate. | Wrapper reads measured unit explicitly; validator has limited known quantity/unit advisories. Define missing/custom identifier handling and check consumer behavior. Decision 0010. |
| `SEN-05` Physical-device grouping is optional; where provided, outputs share a dataset-unique device identifier. | Assay `physical device id` and related comments in current Backend output. | Not checked for uniqueness/consistency. Finalize mapping and identity semantics. Decision 0008. |
| `CSV-01` In the first CSV convention, each sensor-output CSV has time first and one sensor output second. | Measurement files under `Data/`, linked through assay data files. | Optional `--phm-sensor-csv` streams recognizable files and checks column count, not column meaning. Define header, numeric format, malformed/empty files, local timestamps and run association; don't assume global synchronization. Decision 0013. |
| `CSV-02` Preserve recorded timestamps unless a transformation is explicitly identified. | Timestamp column and potential processing provenance; exact encoding open. | No validator check for transformations or timing. Zero-start and global reference are provisional/deferred. Decision 0007. |

## Protocols and provenance

| Candidate ID and direction | Observed mapping | Current coverage and remaining work |
| --- | --- | --- |
| `PRO-01` Measurement data has an applicable measurement protocol. | Study `protocols`, assay `processSequence[].executesProtocol` and file `@id` references. | `--phm-protocols` checks raw outputs under the current mapping; unreadable graphs and some missing structures are incomplete, not full proof of this rule. Define required association for every supported mode. Decision 0017. |
| `PRO-02` Raw, processed, or both may be included and must be distinguishable. | `Raw Data File` and `Derived Data File`; provisional marked pathless raw placeholder in processed-only case. | Experimental protocol and path checks cover parts of this mapping. Confirm placeholder's ISA semantics and required support; never claim an unavailable raw file exists. Decisions 0015 and 0017. |
| `PRO-03` Processed data has an applicable processing protocol with an explicit account of processing or an explicit unknown answer. | Current processing protocol and process parameters/description. | Checks that derived files have a processing output and are not their own inputs under the observed mapping. The selected description survived a real XJTU export and Wrapper readback; meaningful content and unknown-state encoding are not validated. Decision 0017. |
| `PRO-04` When both are present, link the processing input to the raw output and its output to the processed file. | Process `inputs`/`outputs` by `@id`. | `--phm-protocols` flags self-input and reports unestablished raw lineage as incomplete; does not prove correct sensor/run linkage or handle all multistep graphs. Decision 0017. |

## Conformance and verification

| Candidate ID and direction | Mapping / report | Current coverage and remaining work |
| --- | --- | --- |
| `VAL-01` Report the version and all required checks, failures, warnings and incomplete checks without claiming unverified conformance. | Structured API and report not yet standardized. | CLI reports selected checks and exit status; a reusable version-aware compliance result and complete required check set do not yet exist. |
| `VAL-02` Scientific and provenance statements must be accurate; do not fabricate unknown metadata. | Researcher and data-provider responsibility. | A validator may detect structural contradictions but cannot generally prove values, synchronization, processing descriptions or research purpose are true. Define responsibilities in release documentation. |
| `VAL-03` Support reproducible validation and common results across tools. | Specification validator consumed by Wizard and Wrapper; Agent via Wrapper. | Today tools consume selected shared catalogues/advisories, not the complete validator. Package an API, pin versions and dependencies, and test clean installations and end-to-end exports. |

## Minimum evidence for each rule before release

For each accepted rule, record normative wording, exact scope and ISA-JSON
location, accepted and unknown values, severity, validator implementation,
passing and failing fixtures, handling of incomplete checks and the person or
process responsible for assertions that cannot be automated. Where the rule
is intentionally deferred, state the supported subset and avoid interpreting
deferred material as automatically compliant or invalid.
