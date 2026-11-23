# Decision 0006: Scalar and time-varying test factors

Status: agreed decision. The specification has not yet been released.

A single scalar operating-condition or fault-label value is recorded directly
as an ISA study-factor value, rather than requiring a separate one-value CSV.
When an operating condition varies over time, the time series is stored in a
CSV file and referenced from the relevant factor. Details of its column format,
time reference, and handling of varying fault severity remain to be specified.

This decision does not define sensor output representation; see Decision 0007.
It does not assert that a file-backed study factor is itself a sensor assay.
