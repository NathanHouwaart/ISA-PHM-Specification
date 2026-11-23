# Protocols, measurements and data files

[Specification guide](README.md) · [Assay](assay.md) · [Field reference](isa-json-field-inventory.md)

A measurement protocol describes how sensor data was acquired. Processed data also needs an applicable processing protocol describing the processing, or explicitly stating that it is unknown. A dataset may contain raw files, processed files, or both; a processed-only dataset need not provide its raw input.

## How the JSON connects them

This abbreviated example shows the current Backend convention. The protocol lives in a study, and the data file and process live in one of that study's assays. Matching `@id` values connect them.

```json
{
  "studies": [{
    "protocols": [{
      "@id": "#protocol/measurement",
      "protocolType": {"annotationValue": "Measurement Protocol"},
      "parameters": [
        {"@id": "#parameter/rate", "parameterName": {"annotationValue": "Sampling Rate"}},
        {"@id": "#parameter/unit", "parameterName": {"annotationValue": "Measured Unit"}}
      ]
    }],
    "assays": [{
      "dataFiles": [{"@id": "#file/raw", "name": "./Data/run-01.csv", "type": "Raw Data File"}],
      "processSequence": [{
        "executesProtocol": {"@id": "#protocol/measurement"},
        "parameterValues": [
          {"category": {"@id": "#parameter/rate"}, "value": 25600, "unit": {"@id": "#unit/hz"}},
          {"category": {"@id": "#parameter/unit"}, "value": {
            "annotationValue": "G", "termAccession": "http://qudt.org/vocab/unit/G"
          }}
        ],
        "outputs": [{"@id": "#file/raw"}]
      }]
    }]
  }]
}
```

The example omits required ISA fields and the referenced Hz unit definition, which is an annotation in the study's `unitCategories`. `Sampling Rate` and `Measured Unit` are separate parameters. Each included output needs an explicit answer for both; a known value, `Unknown` and `Not applicable` have different meanings. The Wrapper reads the measured-unit parameter rather than guessing from other fields. Variable-rate encoding and some answer encodings remain open.

## Raw and processed relationships

| Available data | Current process relationship |
| --- | --- |
| Raw only | Measurement outputs the raw file. |
| Raw and processed | Measurement outputs raw; processing takes raw as input and outputs processed. |
| Processed only | The Backend currently connects the processes using a pathless raw placeholder marked `availability: not included`; processing outputs the processed file. |

The processed-only placeholder is a current interoperability convention still under review; it does not assert that a raw file exists. When both files are present, the raw file is the processing input and the processed file the output. See [implementation notes](isa-json-implementation-notes.md) for the graph and validator coverage.

Recorded sensor timestamps should be preserved unless a transformation is explicit. A local time column does not by itself tell us when separate sensor files or operating-condition files overlap. Global timing and alignment are deferred to the [timeline work](future-work/global-measurement-timeline.md).
