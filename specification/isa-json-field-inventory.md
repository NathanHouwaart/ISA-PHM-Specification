# ISA-JSON field inventory: current implementation

Working documentation, not an approved specification. Names below describe
the inspected Wizard/Backend/Wrapper implementations; do not assume all are
mandatory, stable or prescribed by the paper. See the [interface audit](audits/2026-11-initial-interface-audit.md)
for sources, scope and unresolved decisions.

| Information | Observed ISA-JSON location | Consumer / caveat |
| --- | --- | --- |
| Experiment type | Investigation `comments`: `experiment_type`; also study design descriptor | Wrapper reads the exact comment name; relationship and allowed values need specification. |
| Researcher identifier, license | Investigation comments `ud_identifier`, `license` | Separate from ISA's generated investigation `identifier`; not comprehensively audited downstream. |
| Run count | Study comment `total_runs`, string | Wrapper derives runs from processes; agreement with the comment is not verified. |
| Sensor alias | Assay comment `sensor alias` | Wrapper falls back to assay filename if missing. |
| Sensor identifier | Protocol comment `Sensor id` | Wrapper uses measurement protocol for sensor identity. Exact name currently matters. |
| Sensor quantity | Assay `measurementType.annotationValue`, optionally `termAccession` | Wrapper exposes the text and identifier; not a comment. |
| Sensor technology/model | Assay `technologyType.annotationValue` / `technologyPlatform` | Current mappings; catalog restrictions and full required-state rules remain to be defined. |
| Physical device | Assay comments `physical device id`, `physical device name`, `physical device model`, `physical device serial number`, `physical device datasheet` | Optional grouping; Wrapper exposes these values. Identifier scope and conflict rules are open. |
| Sensor datasheet | Assay `datasheet` comment | Optional; current layout checker verifies nonempty local paths. |
| Setup image | Study source `image` comment, repeated per file | Current layout checker verifies nonempty local paths. |
| Component datasheet | Source or sample characteristic `datasheet` comment | Current layout checker verifies nonempty local paths. |
| Sampling rate / measured unit | Measurement protocol parameters and process `parameterValues` | Parameter `category.@id` links values to protocol parameter definitions; units and identifiers have distinct representations. The Wrapper now reads the explicit measured-unit parameter without inferring it from unrelated parameters. |
| Factor value and unit | Sample `factorValues` with ISA unit annotation/reference | Scalar versus file-valued interpretation and reference validation are incomplete. |
| Selected Wizard protocol | Protocol comments `selected_measurement_protocol_id`, `selected_processing_protocol_id` | Application identifiers; whether they belong in the public contract is open. |

The [implementation notes](isa-json-implementation-notes.md) explain process
and file links. ISA comments may also hold arbitrary researcher data: an
unknown comment must not automatically be treated as a standardized field.
