# Decision 0013: One sensor output per CSV

Status: agreed decision. The specification has not yet been released.

In the first sensor-output CSV convention, each measurement CSV describes one
sensor output. For example, an XYZ accelerometer has separate X, Y and Z
outputs and corresponding separate CSV files. This does not prevent an output
from having multiple files, for example across measurement windows.

The first sensor-output CSV convention uses two columns: timestamps first and
the values of that one sensor output second. This decision does not yet settle
whether a header is mandatory, exact column names, numeric formats, timestamp
units or time references. It does not prescribe the format of CSV files used
for time-varying study factors.

Where an experiment uses runs, the preferred direction is for the measurement
file's association with the relevant run to be defined. The exact ISA mapping,
whether a file can be associated with more than one run, and the interpretation
of diagnostic measurement windows are not yet decided. In particular, this
decision does not automatically equate a diagnostic window with a prognostic
run. Timestamp columns, CSV layout and global time are addressed separately.

This decision covers the first CSV convention; it does not declare arbitrary
source data with multiple channels invalid before conversion, nor resolve the
paper's discussion of other file formats and pointers into larger files.
