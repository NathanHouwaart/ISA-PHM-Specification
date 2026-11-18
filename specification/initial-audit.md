# Initial audit: work to do

The first descriptive findings are recorded in
[the November 2026 interface audit](audits/2026-11-initial-interface-audit.md).

Agreed decisions are tracked separately from the audit. See
[Decision 0001](decisions/0001-first-serialization-scope.md). The user's
future global measurement-timeline idea is captured under
[future work](future-work/global-measurement-timeline.md).

Measurement-file format scope is recorded in
[Decision 0002](decisions/0002-measurement-file-formats.md).
The dataset root and internal paths are covered by
[Decision 0003](decisions/0003-dataset-root-and-internal-paths.md).
Required dataset directories are recorded in
[Decision 0004](decisions/0004-required-dataset-directories.md).
The investigation-file extension is covered by
[Decision 0005](decisions/0005-investigation-file-extension.md).
Scalar versus time-varying test factors are covered by
[Decision 0006](decisions/0006-scalar-and-time-varying-factors.md). The
zero-based sensor output time proposal in
[Decision 0007](decisions/0007-sensor-output-local-time.md) is provisional
pending the global timeline design.

Physical-device metadata is optional at the dataset level; see
[Decision 0008](decisions/0008-optional-physical-device-metadata.md).
Required answers for sampling rate and measured unit are recorded in
[Decision 0009](decisions/0009-sampling-rate-and-measured-unit.md).
The shared catalogue direction is captured in
[Decision 0010](decisions/0010-shared-unit-and-quantity-catalogues.md).
The measured-quantity answer is covered by
[Decision 0011](decisions/0011-measured-quantity-answer.md).
The first-release diagnostic/prognostic distinction is covered by
[Decision 0012](decisions/0012-diagnostic-or-prognostic-dataset.md).
One sensor output per CSV is recorded in
[Decision 0013](decisions/0013-one-sensor-output-per-csv.md).
The review and migration approach for existing comments is recorded in
[Decision 0014](decisions/0014-existing-comment-conventions.md).
Raw and processed measurement availability is covered by
[Decision 0015](decisions/0015-raw-and-processed-measurements.md).
Sensor technology and model answers are covered by
[Decision 0016](decisions/0016-sensor-technology-and-model.md).
The processing-history answer is covered by
[Decision 0017](decisions/0017-processing-history-answer.md).

This is a review checklist, not a normative specification or complete inventory.

1. Review the ISA-PHM paper and the applicable ISA-JSON model and version.
2. Inventory Backend output, Wrapper consumption, Wizard inputs, and existing
   datasets. For each convention record its location, meaning, data type,
   cardinality, producer, consumer and treatment when missing.
3. Compare the sources and resolve discrepancies before deciding which fields
   are required, optional or still undecided.
4. Define specification version identification and legacy-dataset handling.
5. Agree compact synthetic valid and invalid fixtures, then implement checks
   and document which rules each check actually covers.
6. Coordinate tagged specification releases with the independent tool repos.

Examples of conventions to investigate (not yet approved as requirements):

- Investigation comments `ud_identifier`, `experiment_type` and `license`.
- Study comment `total_runs`.
- Assay comments `sensor alias`, `physical device id`, `physical device name`,
  `physical device model`, `physical device serial number`,
  `physical device datasheet`, and `datasheet`.
- Measurement and processing protocol comments `Sensor id` and selected
  protocol identifiers.
- Quantity and unit identifiers, including any project-local terms.

The fact that a comment exists in the implementation does not prove the paper
does or does not specify it, nor establish whether the field belongs in the
eventual profile. Names may change during review.
