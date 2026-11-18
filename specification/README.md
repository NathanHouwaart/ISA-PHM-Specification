# Specification

The [working draft](draft-profile.md) collects the directions agreed so far.
This directory will contain the human-readable, versioned ISA-PHM profile.
The intended coverage includes concepts, ISA-JSON mappings, data-file paths,
and validation rules. The human-readable specification and its fixtures
must be updated alongside machine-checkable rules.

The published paper and existing implementations are inputs to the initial
review. If they disagree, the disagreement needs an explicit decision; neither
is automatically treated as correct. See [initial-audit.md](initial-audit.md).

We intend new datasets to declare the specification version they follow, but
the exact field name, placement and encoding are not yet finalized. A version
claim will not itself demonstrate conformance. Unversioned existing datasets
must not silently be treated as conforming to a particular version.
