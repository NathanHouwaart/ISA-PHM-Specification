# Decision 0011: Measured quantity answer

Status: agreed decision. The specification has not yet been released.

Each sensor output included in the dataset must have an explicit measured-quantity answer, describing
what its values represent. The answer may select a quantity from the adopted
catalogue, define a custom quantity according to Decision 0010, or explicitly
state `Unknown` when the quantity is not known. A researcher must not invent
a quantity merely to satisfy the requirement.

Unused sensors or channels physically present in a device need not all be
described. The exact ISA-JSON representation of dataset inclusion remains open.

The precise ISA-JSON encoding, catalogue membership, unknown-state encoding,
and checks for quantity–unit relationships still need to be specified.
