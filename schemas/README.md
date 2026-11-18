# ISA-JSON schema baseline

**Candidate testing baseline; not yet a released ISA-PHM specification.**
The [ISA Model and Serialization Specifications](https://isa-tools.org/format/specification.html)
describe ISA model and serialization version 1.0. The ISA-tools documentation
identifies its [model 1.0 core JSON schemas](https://isa-tools.org/isa-api/content/isamodel.html).

For reproducible initial tests, this repository uses the 21 ISA model 1.0 core
JSON schemas bundled with the Python package `isatools==0.14.3`, together with
`jsonschema==4.23.0`. These are the versions currently pinned by the Backend.
The validator verifies the schema-file count and this SHA-256 fingerprint:

```text
473b30c6033e743ddd6c571474854187d6736515983387994475037b8ec8786f
```

The digest is computed from the core schema files sorted by filename, adding
each UTF-8 filename, a NUL byte, its raw bytes, and another NUL byte. The
validator reads schemas from the installed pinned package; it does not download
schemas during validation. This fingerprint pins the tested package contents;
it does not establish that they are byte-identical to every published version
of the ISA specification.

## What this check means

`--isa-schema` runs the bundled core JSON Schema with Draft 2020-12 and format
checking, using local references in the same manner as the ISA-tools schema
checker. It verifies structural constraints only. It does not perform the
other ISA content, graph, or configuration checks, and it does not establish
ISA-PHM conformance or scientific validity.

The ISA-tools default configuration rejects the synthetic PHM fixture's
`Vibration`/`Accelerometer` combination. The experimental `isa-tools-phm/`
configuration supplies this combination and an acceleration counterpart, plus
preliminary protocol sequences. `--isa` runs ISA-tools with this configuration;
unsupported measurement/technology pairs are reported as not checked. These
configuration entries and graph checks are not a complete ISA-PHM profile.

Full ISA-PHM-specific schemas and machine-checkable profile rules have not
yet been defined. No release version should be claimed on the basis of a core
schema pass alone.
