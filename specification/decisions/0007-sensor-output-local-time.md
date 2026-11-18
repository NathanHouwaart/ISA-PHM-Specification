# Decision 0007: Zero-based local time for sensor outputs

Status: **provisional proposal**, pending the global timeline design; not an
agreed conformance requirement or a released specification.

The researcher expressed a preference for sensor-output files to use local
timestamps starting at zero as a possible simplification. Whether to require
that, and how to handle files whose recorded timestamps do not start at zero,
is deferred until the global timeline and its data model are designed. No
conformance judgment about non-zero-based timestamps follows from this note.

The local timestamps describe time within the file. A separate relationship
to a shared global timeline is envisioned for future work; local zero does not
by itself establish a global start time or synchronization across sensors.
The global reference, its representation, clock uncertainty and any inference
rules remain undecided. See the future global measurement-timeline note.

Tools must not silently rewrite recorded timestamps and represent the result
as original measurements. Any conversion or preprocessing of existing
timestamps should be explicit and traceable; the procedure and its provenance
are not yet specified.

The timestamp unit, precision/tolerance, monotonicity and ordering rules,
handling of missing or irregular samples, exact CSV layout, and behavior of
file-valued study factors still need decisions. This rule does not imply that
all source data is synchronized or that timestamps can be reconstructed from
sampling rate alone.
