# Decision 0010: Shared unit and quantity catalogues

Status: agreed direction for the draft; not yet a released specification.

The specification repository provides a shared, versioned home
for the unit and measured-quantity catalogues used by ISA-PHM tools and
validators. The intended foundation is a pinned QUDT vocabulary version,
with any ISA-PHM-defined additions clearly distinguished from QUDT entries.
The Wizard's existing QUDT 3.5.2 snapshot is the initial shared draft catalogue,
alongside explicitly identified ISA-PHM additions. This centralization does
not by itself make the snapshot a released specification requirement.

A unit recognized by the specification is not automatically supported by
every tool or analysis. Tools should identify the units and operations they
support. Catalogues and identifiers should not imply automatic numerical unit
conversion, nor prove that metadata correctly describes the measured data.

The initial approach is to use known quantity–unit relationships to suggest
appropriate units and warn about suspicious combinations. A missing or
unrecognized relationship is not by itself grounds to reject a combination:
catalogue relationships can be incomplete. The specific warning conditions
and how unknown compatibility is reported still need to be specified.

When a known unit is missing from the catalogue, a researcher may define a
clearly labelled custom unit and record its meaning. A custom unit must not
be represented as though it were a QUDT entry. It is distinct from an
`Unknown` answer. The interface and documentation should warn that custom
units may have limited automated compatibility checks, unit conversion and
analysis support; the exact features affected depend on the tool and unit.
Custom definitions can be considered for later inclusion in the shared
catalogue. The details of identity, required definition fields, review,
serialization and tool behavior remain open.

The same exception is available for a known measured quantity missing from the
catalogue: a researcher may define a clearly labelled custom quantity and
record its meaning. It must not be presented as a QUDT or shared-catalogue term
unless it actually is one. Automated compatibility checks and analyses may be
limited until tools understand the definition. Its identifier, representation,
workflow, and any later catalogue-adoption process remain undecided.

Each custom unit or quantity definition must travel with the dataset, including
at least its name, a human-readable description and an identifier. Tools may
generate the identifier automatically. This helps recipients interpret the
metadata without relying on a private Wizard catalogue. The exact ISA-JSON
encoding, identifier scope and any additional machine-readable details remain
to be specified.

The exact included units, how quantity–unit compatibility is determined,
the treatment of unknown or not-applicable answers, versioning and update
policy and a mechanism for exceptional or project-defined terms remain to be
decided. The current snapshot and attribution are recorded in
[the catalogue guide](../../catalogues/README.md).
