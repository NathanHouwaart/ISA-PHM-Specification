# Decision 0003: Dataset root and internal file paths

Status: agreed direction for the draft; not yet a released specification.

The ISA-JSON investigation file must be located at the root of the ISA-PHM
dataset. References to files contained in the dataset are relative to that
dataset root. This supports moving a dataset as a whole between machines
without embedding machine-specific absolute paths.

For the first specification release, referenced files that are part of the
dataset must be contained within the dataset root. External file references,
such as network paths or URLs to measurement data, are out of scope. This
decision concerns dataset files; it does not prohibit external identifiers,
ontology URLs, publication DOIs, or other descriptive links.

For example, `Data/measurement.csv` refers to a file under `Data` at the
dataset root, not a path relative to an individual study, assay, or the
program's current working directory.

This decision does not yet prescribe the investigation filename, how many
investigation files a dataset may contain, path separator and case rules,
symbolic-link behavior, or future rules for external file references. Legacy
data with absolute paths should remain readable where possible, but a
compatibility mechanism must not silently be presented as conformance to this
rule. The exact way validators handle containment and symbolic links remains
to be specified.
