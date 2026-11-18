# Decision 0002: Measurement file formats

Status: agreed direction for the draft; not yet a released specification.

The ISA-PHM conceptual model is not limited to a particular measurement-file
format. The first concrete, testable file convention will cover CSV. Its
columns, time semantics and other details are not yet specified by this
decision.

Other file formats may be represented by ISA-PHM in principle; their detailed
conventions and validation may be specified later. Individual tools must be
able to state which formats they support. A tool not supporting a particular
format does not by itself make the dataset incompatible with ISA-PHM.

This decision does not settle file-path rules, in-file pointers, references to
external resources, or how compatibility with unspecified formats is assessed.
