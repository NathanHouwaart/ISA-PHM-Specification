# Decision 0016: Sensor technology and model answers

Status: agreed decision. The specification has not yet been released.

Each sensor output included in a dataset must have explicit answers for its
technology type and sensor model, in addition to its measured quantity.
`Unknown` and `Not applicable` are acceptable when appropriate, such as when
the model is not known or a simulated output has no physical sensor model.
These states are distinct and a researcher must not invent information.

The exact ISA-JSON representation, vocabulary constraints, relationship to
physical device metadata, and how existing datasets are reported remain open.
The current Wizard's readiness validation and editor behavior must be reviewed
and aligned with any adopted representation of these explicit states.
