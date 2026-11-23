# Fixtures

Reserved for small, synthetic, non-sensitive datasets and focused examples.
Each future fixture should document the specification version and the rules it
illustrates, including whether it is expected to pass or fail particular checks.

`layout-valid/` passes the currently implemented layout checks;
`layout-invalid/` deliberately refers to a missing measurement file. These
small JSON fragments are **not complete ISA-JSON investigations** and are not
evidence of ISA-PHM conformance. `.gitkeep` files merely preserve otherwise
empty folders in Git and are not a dataset-format requirement. Real research
datasets do not need to be included in this public-facing repository.

`isa-core-valid/` is a synthetic, structurally complete investigation generated
from the sibling Backend's minimal test payload. It passes the selected layout
checks and the pinned ISA 1.0 core JSON Schema. `isa-core-invalid/` is a copy
with a comment value intentionally changed to a number; it should fail that
schema. These are **not certified ISA-PHM datasets**: experimental ISA-tools
and PHM checks do not cover the complete evolving ISA-PHM profile. The
examples are synthetic and contain no research data.
The checked-in examples can be used without other repositories or a generator.
