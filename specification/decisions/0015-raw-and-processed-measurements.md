# Decision 0015: Raw and processed measurements

Status: agreed decision. The specification has not yet been released.

An included measurement may reference raw data, processed data, or both.
The metadata must distinguish raw from processed data. Researchers are not
required to invent or supply raw data when only processed data is available,
or processed data when only raw data is available.

Processed-only data still requires the applicable measurement and processing
protocols and their metadata; lack of the raw file is not an exemption. See
Decision 0017 for the open ISA representation of an unavailable raw input.

The detailed ISA-JSON mapping, how processing methods and lineage are recorded,
handling of multiple files or versions, and validation of referenced data are
not yet specified. This decision does not establish that the processing
history is known merely because a file is labelled processed.
