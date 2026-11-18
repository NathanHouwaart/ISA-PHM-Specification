# Decision 0005: Investigation file extension

Status: agreed direction for the draft; not yet a released specification.

An ISA-PHM investigation file for the first release must be located in the
dataset root and its filename must end in `.isa-phm.json`. The portion before
that suffix is chosen by the researcher, for example
`bearing-experiment.isa-phm.json`. Keeping `.json` as the final extension lets
ordinary JSON tooling recognize the file.

The current Backend emits `ISA-PHM-Out.json`, so new-export tooling needs to be
aligned. Tools may support legacy investigation files with other names, but
such compatibility must be distinguished from first-release conformance.

This decision does not yet settle how many investigation files may appear at
one dataset root, filename case sensitivity, or name-character restrictions.
