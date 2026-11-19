# ISA-JSON implementation notes (working draft)

This is a descriptive, provisional interoperability guide, not a released
ISA-PHM specification. It records current Backend output and the selected
checks in this repository. See the [interface audit](audits/2026-11-initial-interface-audit.md)
for comments, consumer behavior, evidence and unresolved questions.

## Measurement and processing relationships

The current Backend declares protocols in each study's `protocols` array.
Assay `processSequence` entries point to a protocol through
`executesProtocol.@id`; `inputs` and `outputs` refer to objects through
`@id`. Protocol types currently use `Measurement Protocol` and `Processing
Protocol`. Assay files use `Raw Data File` and `Derived Data File` types.

| Dataset contents | Current Backend graph |
| --- | --- |
| Raw only | Measurement process outputs the raw file. |
| Raw and processed | Measurement outputs raw; processing takes raw as input and outputs derived. |
| Processed only | Measurement outputs a pathless raw placeholder; processing takes that placeholder and outputs derived. |

The placeholder uses `type: Raw Data File`, an empty `name`, and a comment
`availability: not included`. It is a provisional interoperability mechanism,
not a final representation or a real file. See [Decision 0017](decisions/0017-processing-history-answer.md).

The optional `--phm-protocols` check applies only this current mapping. It
checks that raw files are measurement outputs, derived files are processing
outputs, and that a derived file is not its own input. It reports lineage it
cannot establish as not checked. Unknown types, unreadable graphs and unknown
protocol references are not treated as conformance passes. It does not verify
the meaning or adequacy of a processing method, sampling rate or measured unit;
nor does it prove that the correct run or sensor was associated with a file.
Different or multistep ISA representations may need additional mapping before
these rules are appropriate for them.

## Explicit measurement metadata in the current mapping

The Wizard defines `Sampling Rate` and `Measured Unit` as measurement
protocol parameters. The Backend places their definitions in the study's
`protocols[].parameters`; a measurement process points to that protocol and
its `parameterValues[].category.@id` points to a parameter definition. A
minimal illustrative fragment (not a standalone ISA investigation) is:

```json
{
  "parameters": [
    {"@id": "#rate", "parameterName": {"annotationValue": "Sampling Rate"}},
    {"@id": "#unit", "parameterName": {"annotationValue": "Measured Unit"}}
  ],
  "parameterValues": [
    {"category": {"@id": "#rate"}, "value": 25.6, "unit": {"@id": "#khz"}},
    {"category": {"@id": "#unit"}, "value": {
      "annotationValue": "G", "termAccession": "http://qudt.org/vocab/unit/G"
    }}
  ]
}
```

In the complete JSON, the definitions and values occur in separate protocol
and process objects, and `#khz` refers to a unit annotation. Some values are
plain text rather than ontology annotations; `Unknown` and `Not applicable`
are explicit answers, not known quantities. The optional `--phm-metadata`
check checks answer presence under this mapping and warns for a small explicit
list of known incompatible quantity/unit identifier pairs. It does not
comprehensively verify unit compatibility or scientific correctness. The Wrapper reads
`Measured Unit` directly and does not infer it from other parameter units.

For a numeric measurement or processing parameter, its `unit` reference can
point to a study unit annotation whose `termAccession` holds the selected unit
identifier. The same ISA unit annotation mechanism applies to numeric or
text-valued component characteristics where the Backend emits a unit. The
Wizard-to-Backend payload's `unitIdentifier` field is an application-level
transport field, not an ISA-JSON field. Existing text-only units remain
readable; they must not be silently assigned an identifier by inference.

Symbols alone are not sufficient identifiers: QUDT's `g`/`unit:GM` is gram,
whereas its gravity acceleration unit is `G`/`unit:G`. A real XJTU export
previously recorded acceleration with the gram identifier; see the
[dataset audit](audits/2026-11-xjtu-unit-identifier.md). The check now warns on
that particular mismatch, but many combinations remain unchecked.

The experimental warning rules are recorded in
`quantity-unit-warning-rules.json`. Consumers should pin an exact revision of
this repository, rather than maintain independently edited rule copies.
The current Wizard's separate measurement-metadata export validation requires
an identified measured unit to be in its catalogue. The new compatibility
warning does not add that restriction, but also does not implement the agreed
custom-unit workflow; that remains open work.

## File references

The draft requires dataset-local paths. The validator currently checks assay
`dataFiles[].name` under `Data/`, plus present assay `datasheet` and `physical
device datasheet` comment values under `Datasheets/`. It also checks source
`image` comments under `Images/`, and datasheet comments on source and sample
characteristics under `Datasheets/`. A datasheet or image is not required
merely because the directory is required. Factor and other unrecognized file
references remain unchecked; their mappings need further coverage.

## Other extensions

Comments such as `experiment_type`, `total_runs`, `Sensor id`, `sensor alias`,
and physical-device fields are current implementation conventions, not yet
all approved normative requirements. Quantity identifiers are represented in
ISA ontology annotations rather than comments. Required states, name matching,
versioning and legacy behavior must be settled before strict validation.
