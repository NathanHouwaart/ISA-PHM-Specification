# Decision 0004: Required dataset directories

Status: agreed decision. The specification has not yet been released.

The dataset root must contain the ISA-JSON investigation file and these three
directories, with the names and capitalization shown:

```text
dataset-root/
├── <investigation>.isa-phm.json
├── Data/
├── Datasheets/
└── Images/
```

All three directories are required even if one or more is empty. `Data/` is the
home for the dataset's measurement and other data files; `Datasheets/` holds
datasheets, and `Images/` holds relevant images. The organization within
`Data/` is flexible: researchers may group files by study, run, sensor, or
another suitable layout, and ISA-JSON references identify the correct files.
The organization within the other directories is not yet prescribed. The exact
investigation filename and the treatment of other kinds of documents remain
undecided.

This is an intended first-release rule, not a description of all current
Wizard behavior: the Wizard currently permits data files elsewhere below the
indexed root. The Backend's conversion archive places attached datasheets and
images in `Datasheets/` and `Images/` when present, but does not include the
measurement files. Tooling must be aligned with the agreed format.

A dataset packaging or transfer method must preserve required empty directories
if they are to be checked after transfer. How this is achieved for ZIP, Git,
object storage and other media needs to be specified; placeholder files are
not mandated by this decision. Legacy datasets and tool compatibility must be
reported separately from conformance to this rule.
