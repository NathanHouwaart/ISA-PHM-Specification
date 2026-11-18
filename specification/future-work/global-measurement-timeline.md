# Future idea: global measurement timeline

Status: user-described future Wizard direction, not an approved format rule or
implementation plan. No implementation or visual design has been agreed yet.

Replace or rethink the measurement-output grid as one global timeline:

- Sensor outputs appear on the vertical axis; file measurement windows appear
  along the horizontal time axis shared across sensors.
- A user can describe measurement windows, sampling rate, duration and
  intervals to help infer and display time slots.
- Bulk editing should support horizontal, vertical and cross-sensor workflows.
- Explore a timestamp or time-reference parameter associated with the data
  representation; its exact placement and semantics remain undecided.

A shared visual axis does not prove that files are synchronized. A future
design must distinguish recorded timestamps and references from times entered
or inferred by users, and represent the underlying time reference clearly.
Sampling rate or duration alone cannot determine an absolute or shared start
time. Uncertainty, gaps and incompatible clocks may need to be represented.

Explore this later using visual designs and an ISA-PHM model review; do not
assume that a timestamp belongs in a comment or protocol parameter until the
appropriate representation is assessed.

## Diagnostic measurement windows: open question

A diagnostic experiment may have repeated measurement windows while its
condition is not degrading. Whether such windows belong to one study, how they
relate to independent diagnostic experiments, and how they should be encoded in
ISA-PHM are not decided. Discuss these cases with domain colleagues as part of
the timeline redesign and review the paper's study/run interpretation before
choosing a representation. Do not automatically equate diagnostic windows with
prognostic runs.
