# ISA-PHM specification guide

Start here to understand how a dataset is organized and how its information appears in ISA-JSON. ISA-PHM uses ISA's investigation, study and assay concepts; its first specified serialization is ISA-JSON. ISA-Tab is outside the current scope.

```text
Dataset root
├── <name>.isa-phm.json        Investigation
├── Data/                      Sensor and other data files
├── Datasheets/                Referenced datasheets
└── Images/                    Referenced images

Investigation
└── studies[]                  Studies: setup, factors, protocols
    └── assays[]               Assays: sensor output, files, processes
```

The hierarchy is a navigation aid: protocols and factor definitions live at study level, while process references connect them to assay-level measurements. IDs are references, not a guarantee of time synchronization.

## Read the specification

1. [Dataset layout](dataset-layout.md) — folders, paths and file formats.
2. [Investigation](investigation.md) — dataset identity, contacts and diagnostic or prognostic purpose.
3. [Study](study.md) — test setup, factors, samples, protocols and runs.
4. [Assay](assay.md) — sensor output, measured quantity and device information.
5. [Protocols and data](protocols-and-data.md) — sampling rate, measured unit and raw/processed relationships.
6. [ISA-JSON field reference](isa-json-field-inventory.md) — exact current comment names and locations.

The examples are illustrative fragments, not complete valid investigations. They show the current Wizard/Backend representation and distinguish that representation from agreed conceptual rules. Some details are still being specified; the pages say where. No versioned specification has been released.

## Validation and schemas

- [ISA schema baseline](../schemas/README.md): structural ISA-JSON schemas supplied by ISA-tools, not a complete ISA-PHM schema.
- [Validator](../validator/README.md): selected ISA-PHM and optional ISA checks, their coverage and installation.
- [Catalogues](../catalogues/README.md): shared quantities and units.
- [Fixtures](../fixtures/README.md): examples for selected checks, not complete conformance certificates.

The validator cannot check every rule or scientific claim. See its guide before interpreting a result. [Implementation notes](isa-json-implementation-notes.md) give more detail about the current graph and validation.

## Decisions and development history

[Decisions](decisions/) record the reasons behind agreed directions and identify details that remain open. They are supporting history, not the main reading path. The [rule inventory](first-release-rule-inventory.md) tracks coverage and remaining work; [audits](audits/) record historical observations that may have since changed. The [timeline proposal](future-work/global-measurement-timeline.md) is future work. The earlier [profile summary](draft-profile.md) is retained for reference.
