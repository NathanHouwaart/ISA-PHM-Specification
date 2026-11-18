# Decision 0008: Physical-device metadata is optional

Status: agreed direction for the draft; not yet a released specification.

An ISA-PHM dataset is not required to describe a physical measurement device.
For example, simulated measurements may have no corresponding physical device.
Where relevant, describing a device can preserve the relationship between it
and one or more sensor outputs.

When physical-device grouping is provided, sensor outputs belonging to the
same device share a device identifier. The identifier is unique within the
dataset and is used to preserve that grouping; it is not necessarily a serial
number. Software such as the Wizard may generate the identifier automatically,
so a researcher does not need to type it. A standalone sensor does not need a
parent device.

This decision does not establish which other device fields are required when a
device is described, or the final ISA-JSON representation.
The Backend's current assay comments are implementation behavior to review,
not automatically a normative mapping.
