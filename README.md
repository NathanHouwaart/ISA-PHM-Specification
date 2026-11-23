# ISA-PHM specification

ISA-PHM describes prognostics and diagnostics datasets using the ISA model. This repository documents the dataset structure, its ISA-JSON representation, shared catalogues and validation checks.

ISA-PHM builds on the original [ISA Model and Serialization Specifications](https://isa-specs.readthedocs.io/en/latest/), maintained in the [ISA specification GitHub repository](https://github.com/ISA-tools/isa-specs). For the underlying JSON format, see the [ISA-JSON specification](https://isa-specs.readthedocs.io/en/latest/isajson.html). ISA-PHM adds PHM-specific requirements and conventions to that foundation.

**Start with the [specification guide](specification/README.md).** It walks through the investigation, studies, assays, protocols and data files, with JSON examples.

Several rules have been agreed, but no versioned specification has been released. Some serialization details and validation rules remain open. Passing the validator's selected checks does not establish complete conformance.

- [Dataset layout](specification/dataset-layout.md)
- [Investigation](specification/investigation.md)
- [Study, test setup and factors](specification/study.md)
- [Assay and sensor outputs](specification/assay.md)
- [Protocols, measurements and processing](specification/protocols-and-data.md)
- [ISA-JSON field and comment reference](specification/isa-json-field-inventory.md)
- [Schema baseline](schemas/README.md), [catalogues](catalogues/README.md), [fixtures](fixtures/README.md) and [validator](validator/README.md)
- [Decisions and development history](specification/README.md#decisions-and-development-history)

Install and run the validator with `python -m pip install .` and `isa-phm-validate path/to/dataset.isa-phm.json`. See the [validator guide](validator/README.md) for optional checks and their limitations. The [ISA-PHM Wizard](https://github.com/NathanHouwaart/ISA-PHM-Wizard) helps researchers create datasets and abstracts the underlying ISA-JSON structure.
