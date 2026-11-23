# ISA-JSON representation and validation notes

This page supplements the [specification guide](README.md) with details of the current ISA-JSON representation and selected validation checks. It describes a representation under development; it does not imply that every detail is finalized or checked.

## Measurement and processing relationships

A study declares protocols in `protocols[]`. An assay process in `processSequence[]` points to a protocol through `executesProtocol.@id`; its `inputs` and `outputs` refer to objects by `@id`. Protocol types include `Measurement Protocol` and `Processing Protocol`; assay file types include `Raw Data File` and `Derived Data File`.

| Dataset contents | Current relationship |
| --- | --- |
| Raw only | The measurement process outputs the raw file. |
| Raw and processed | Measurement outputs raw; processing takes raw as input and outputs derived. |
| Processed only | Measurement outputs a pathless raw placeholder; processing takes that placeholder and outputs derived. |

The processed-only placeholder has `type: Raw Data File`, an empty `name`, and the comment `availability: not included`. It is a provisional interoperability convention, not a real file or a finalized representation. See [Decision 0017](decisions/0017-processing-history-answer.md).

The optional `--phm-protocols` check checks selected relationships under this mapping. It does not verify the meaning of a processing method or prove that files are associated with the correct run or sensor. Unsupported or unreadable graphs can be reported as not checked. See the [validator guide](../validator/README.md).

## Sampling rate and measured unit

`Sampling Rate` and `Measured Unit` are measurement protocol parameters. Their definitions are in `studies[].protocols[].parameters[]`; a process references the protocol, and each process parameter value points to its definition through `category.@id`. See the complete nesting and an illustrative example in [protocols and data](protocols-and-data.md).

Known values, `Unknown` and `Not applicable` are distinct answers. A measured unit is read from its explicit parameter; it is not inferred from an unrelated parameter. Numeric parameter units can reference study unit annotations with a `termAccession`. Text-only units must not silently be assigned an identifier by inference.

The optional `--phm-metadata` check checks answer presence for supported processes and warns about a limited set of incompatible quantity/unit identifier pairs. It does not comprehensively validate quantities, units, or scientific correctness. The advisory rules are in `quantity-unit-warning-rules.json`; the custom-unit workflow remains open.

## File references and other fields

The dataset layout requires local references. The validator checks recognized assay data-file references, assay datasheet comments, source image comments and characteristic datasheet comments. It does not yet check factor-file references or every other possible reference. See [dataset layout](dataset-layout.md) and the [validator guide](../validator/README.md).

The [field and comment reference](isa-json-field-inventory.md) lists canonical names, legacy names and exact JSON locations. Quantity identifiers use ISA ontology annotations. Unknown comments may contain researcher data and are not automatically ISA-PHM fields.
