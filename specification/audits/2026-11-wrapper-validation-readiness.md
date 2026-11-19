# Wrapper validation readiness: exploratory audit

These results exercise the current working draft, not a released ISA-PHM
standard. They are not a complete assessment of the datasets. The selected
checks were layout, ISA 1.0 core JSON Schema, experimental PHM protocol
relationships, and experimental measurement metadata presence. ISA-tools
content/graph validation and scientific correctness were not checked.

## Results

| Export | Selected checks | Observation |
| --- | --- | --- |
| XJTU-SY small subset, current Wizard export | 0 errors; 0 selected items not checked; 0 advisory warnings | All selected checks passed. Other areas remain unchecked. |
| Legacy diagnostic example | 12 errors | Old investigation filename, missing draft layout directories and eight files outside `Data/`. Core schema and selected protocol and metadata checks passed. |
| Legacy milling example | 3,988 errors; 996 items not checked | Many layout findings and incomplete protocol-lineage checks. Core schema passed. Repeated findings were not individually audited. |
| Legacy Sietze export (known unsuitable structure) | 7,696 errors; 7,693 items not checked | Old layout and repeated processing self-input findings. Core schema and selected metadata-presence checks passed; the repeated lineage findings were not individually audited. |

The Wrapper opened the XJTU small subset and the legacy diagnostic export with
both values of `strict_validation`. With the latter, its first measurement also
loaded (90,388 rows), but the Wrapper warned that the median timestamp spacing
was inconsistent with a 19,000 Hz sampling-rate declaration if timestamps are
in seconds. It preserved the timestamps. Their units and the cause have not
been established; successful loading is not evidence of valid analysis.

## Proposed handling (not yet implemented)

- Reject unreadable JSON, an unusable root, and unsafe file access where
  necessary for safe operation. Missing metadata needed for a particular
  analysis should prevent that analysis rather than be invented.
- Run the shared draft checks in normal use and report their findings with
  rule names and actionable context. Show incomplete checks separately;
  never describe a partial pass as full conformance.
- Whether an older filename, an absent attachment directory, or files outside
  `Data/` should prevent all Wrapper access is a policy decision, not a
  technical prerequisite for opening metadata. Test compatibility and document
  migration before making such findings unconditional blockers.
- A self-referential processing input is a serious provenance defect; establish
  whether the experimental mapping correctly identifies it before enforcing a
  global block. Missing files can block operations that need those files;
  inspection of other metadata may still be useful.
- Do not silently infer sampling rate, measured unit, timestamps, or conversion
  factors. Incompatible known quantity/unit identifiers are currently advisory;
  analysis requiring a trustworthy unit or sampling rate needs its own checks.
- An explicit inspection mode for nonconforming or legacy data is a proposed
  design, not permission to describe it as valid or to run unsafe analysis.

The Wrapper currently consumes shared catalogues and advisory rules but does
not invoke the shared validator. `strict_validation` calls ISA-tools model
loading, not the separate ISA core schema validator or full ISA-PHM checks.
Before changing defaults, define a reusable validator interface, package its
dependencies and rules, test missing dependencies and report/exit semantics,
and add Wrapper and Agent integration tests. Avoid printing one line for each
of thousands of identical findings without a summarized view.
