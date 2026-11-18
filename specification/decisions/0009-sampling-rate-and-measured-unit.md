# Decision 0009: Sampling rate and measured unit answers

Status: agreed direction for the draft; not yet a released specification.

Each sensor output included in the dataset must explicitly answer both the sampling-rate and
measured-unit questions. An answer may provide a value where known and
applicable, or explicitly state `Unknown` or `Not applicable` as appropriate.
Known units may use a shared catalogue entry or a clearly defined custom unit,
subject to the catalogue rules and limitations described in Decision 0010.
Unknown, not applicable, and a known value are distinct states and must not be
silently treated as equivalent. The measured unit of a quaternion component is
an example of `Not applicable`.

This requirement does not compel a researcher to describe every unused sensor
or channel physically present in a device. Exactly how an output is marked as
included is still to be defined in the ISA-JSON mapping.

This decision does not yet define the exact ISA-JSON encoding, controlled
vocabularies, validation of numerical values or units, treatment of variable
or irregular sampling, or whether and how answers may differ by run. Those
details require review. It also does not impose a unit or zero-start rule on
timestamps; local/global time is being considered separately.
