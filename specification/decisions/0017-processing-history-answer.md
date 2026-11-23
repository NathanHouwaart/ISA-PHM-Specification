# Decision 0017: Processing history answer

Status: agreed decision. The specification has not yet been released.

When processed data is included, an applicable processing protocol is required.
It must be associated with the processed data it describes and explicitly
answer how the data was processed. When known, the method is described through
the protocol and its parameters or description. When the method is unknown,
that must be expressible explicitly within the protocol; a researcher should
not invent a method. A free-text description by itself does not replace the
requirement for a protocol.

An applicable measurement protocol is also required for sensor measurement
data, including processed-only datasets. A missing raw file does not remove
the need for measurement metadata such as sampling-rate and measured-unit
answers. Exact associations for raw-only, processed-only and combined output
remain to be mapped and verified against the ISA model.

When raw and processed files are both available, the processing process should
identify the raw file as its input and the processed file as its output. It
must not describe the processed file as its own raw input. A processed-only
dataset need not contain its raw input. How to represent the unavailable raw
input remains undecided and must be checked against ISA; a nonexistent raw
file must not be invented.

The exact minimum description, unknown-state encoding, granularity, per-run
differences, multiple steps and ISA-JSON mapping are not yet specified. A
protocol's presence or name alone does not establish that its contents describe
the actual processing. Validation can check that structured information is
present and internally consistent, but cannot generally prove an arbitrary
human-written protocol accurately or sufficiently describes real processing.

Current implementation needs review before claiming support for this rule.
The Wizard supports creating and selecting processing protocols and validates
that a selection exists for studies with processed output. The inspected
Backend converter constructs the emitted processing protocol's description
from the sensor description, while also mapping processing parameters; whether
and how the selected protocol's own description survives the complete export
path needs an end-to-end check. An explicit unknown-state workflow also needs
to be verified.

## Converter experiment: three output modes

The Backend converter was run in memory with its synthetic
`tests/fixtures/minimal_payload.json`, changing only raw and processed
filenames. This inspected the resulting ISA-JSON, not the complete browser
workflow or every possible dataset:

- Raw-only: measurement outputs the raw file; no processing process appears
  in the assay sequence.
- Raw + processed: measurement outputs the raw file; processing takes it as
  input and outputs the processed file.
- Processed-only: measurement outputs the processed file; the processing
  process has that same processed file as both input and output.

The last behavior is confirmed for this synthetic case and does not express
the intended relationship. It needs correction, but the appropriate
ISA-compatible representation of an unavailable raw input must be decided and
tested first. This experiment alone does not establish whether the JSON passes
the upstream ISA schema or how every Wrapper function interprets it.

## Preliminary placeholder experiments

Using the same synthetic processed-only example, three in-memory alternatives
were compared with the current output. `isatools.isajson.load` read them. An
earlier claim that `isatools.isajson.validate` reported no errors was incorrect:
the first experiment used a simulated filename rather than a real file, so the
validator did not run its checks. A corrected test using real temporary files
found that the baseline and placeholder both failed the installed default
configuration's `Vibration`/`Accelerometer` type check; validation stopped
before final graph checks. The placeholder introduced no additional reported
errors in that comparison. This is not proof of ISA conformance or semantic
appropriateness.

| Case | In-memory representation | Current Wrapper extraction |
| --- | --- | --- |
| Current output | Processed file is both input and output. | Reports the same processed path as raw and processed. |
| Missing input | Measurement output and processing input lists are empty. | Does not identify either the raw or processed output in this case. |
| Empty-name raw placeholder | A `Raw Data File` object with empty `name` connects the processes. | Extracts a raw file object with empty path and the processed path separately. |
| Placeholder with status | Same placeholder plus illustrative `availability: not included` comment. | Extracts the same paths; no special interpretation of that status was tested or established. |

For the status placeholder, ISA-tools serialization and readback retained its
empty name, status comment, and the two references in the synthetic sample;
Wrapper preprocessing and extraction retained the separate paths. Some
Wrapper summaries already count only nonempty paths, but other consumers may
interpret the mere presence of a data-file object differently. Further work
must explicitly test raw loading, public APIs, status interpretation and ISA
semantics, and must distinguish an unavailable file from an empty file or a
file with unknown name. The example comment name is illustrative, not an
adopted extension or specification decision.

The executable cross-repository experiment is
`experiments/test_processed_only_placeholder.py`. With a temporary processed
CSV, the current Wrapper loads processed and auto modes, rejects an explicit
raw request as unavailable, and retains the sampling-rate parameter. The
Originally, the Wrapper did not interpret the illustrative availability comment;
an empty path led to its existing no-raw-file behavior.

## Provisional implementation

The Backend now emits the explicit pathless raw placeholder with comment
`availability: not included` for processed-only output. The Wrapper recognizes
that marker as unavailable raw data and avoids treating it as a file to load.
Raw-only and raw-plus-processed exports retain their actual file links. Existing
previously exported self-referential JSON is not automatically repaired. This
remains provisional; the default ISA configuration mismatch and incomplete
ISA graph validation described above are not resolved by this implementation.
