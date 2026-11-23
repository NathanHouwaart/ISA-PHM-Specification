# Dataset layout

[Specification guide](README.md) · Next: [Investigation](investigation.md)

An ISA-PHM dataset has an investigation JSON at its root and separate folders for data, datasheets and images:

```text
my-dataset/
├── bearing-study.isa-phm.json
├── Data/
│   └── bearing-1/run-01.csv
├── Datasheets/
└── Images/
```

The investigation filename is chosen by the author and ends in `.isa-phm.json`. The three folders are required even if empty. Dataset files are referenced by paths relative to the root and remain inside it. The layout under `Data/` is flexible. A required folder does not mean that an image or datasheet must exist.

```json
{"name": "./Data/bearing-1/run-01.csv", "type": "Raw Data File"}
```

This is one entry of an assay's `dataFiles` array, not a complete file. External file references are outside the current dataset-layout scope; publication links and ontology identifiers are different kinds of reference.

A sensor-output CSV contains a time column and one sensor-output value column. The format and reference time of time-varying operating-condition files are not fully specified. Timestamps do not establish synchronization. See [protocols and data](protocols-and-data.md) and [timeline future work](future-work/global-measurement-timeline.md).

The [validator guide](../validator/README.md) lists which references and folders are checked. Factor-file references and some other file references are not yet checked.
