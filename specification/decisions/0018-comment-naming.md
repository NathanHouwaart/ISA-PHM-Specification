# Decision 0018: ISA-PHM comment naming

Status: agreed decision. The specification has not yet been released.

ISA-PHM-defined comment names use lowercase words separated by underscores (`snake_case`). New exports use the canonical names in the [field reference](../isa-json-field-inventory.md). Readers accept the documented legacy spellings so existing datasets remain readable. Researcher-defined arbitrary comments are not renamed.

When both a canonical and a legacy name occur with different values, the Wrapper prefers the canonical value. Validator conflict reporting remains open. This decision does not change ISA-defined field names or protocol parameter names.
