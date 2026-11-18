# ISA-PHM Specification (working draft)

This repository is intended to become the shared home of the ISA-PHM dataset
specification, examples, schemas and a standalone reference validator.

**Status: early draft. No specification version has been released.** The paper,
existing datasets and tool implementations still need to be reviewed together.
Repository contents do not yet establish ISA or ISA-PHM conformance.

ISA-PHM is intended as a PHM-specific profile of ISA-JSON. The intended scope
includes the dataset model, ISA-JSON representation, measurement files and
their relationships. The specification will distinguish requirements that can
be checked automatically from scientific judgments that remain the researcher's
responsibility.

## Contents

- [Specification work](specification/README.md)
- [Readable working draft](specification/draft-profile.md)
- [ISA-JSON implementation notes](specification/isa-json-implementation-notes.md)
- [Current ISA-JSON field inventory](specification/isa-json-field-inventory.md)
- [Schema work](schemas/README.md)
- [Fixture work](fixtures/README.md)
- [Experimental validator](validator/README.md)
- [Initial audit](specification/initial-audit.md)
- [First interface audit](specification/audits/2026-11-initial-interface-audit.md)
- [Exploratory XJTU-SY export check](specification/audits/2026-11-xjtu-existing-export.md)
- [XJTU-SY measured-unit identifier finding](specification/audits/2026-11-xjtu-unit-identifier.md)

The included synthetic fixtures exercise selected layout and ISA core-schema
checks; they are not certified ISA-PHM examples. No ISA-PHM conformance schemas have been agreed yet. The
Backend's existing input schemas validate its Wizard-to-Backend payload; they
are not a substitute for a schema for exported ISA-JSON.

## Development

The early layout-checking utility uses Python's standard library. Run its tests:

```bash
python -m unittest discover -s validator/tests
```

For the optional offline ISA core-schema check, install the pinned dependencies
from `requirements-schema.txt` and run `python -m validator <file> --isa-schema`.
The schema check does not include ISA content or graph validation. To run the
ISA-tools validator with the experimental PHM configuration, use
`python -m validator <file> --isa`. See
[the validator guide](validator/README.md).

The Wizard and Wrapper can pin a draft revision of this repository as a Git
submodule for shared experimental rules. A pinned commit makes the inputs
reproducible; it does not turn the draft into a released standard. Consumers
must update their pinned revisions deliberately when adopting changes.
