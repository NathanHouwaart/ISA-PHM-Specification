# Open questions and release work

[Specification guide](README.md) · [Rule and validation inventory](first-release-rule-inventory.md) · [Historical audits](audits/README.md)

The pages in the specification guide describe the agreed direction and current representation. The points below still need decisions or verification before a versioned release. A validator pass covers only the checks selected; see the [validator guide](../validator/README.md).

- **Version and compatibility:** Define a specification version marker, release scope and how unversioned or older datasets are assessed. Decide how conflicting canonical and legacy comment values are reported.
- **ISA and validation:** Confirm the ISA schema and content/graph validation requirements, complete ISA-PHM-specific checks and fixtures, and distinguish errors, warnings and checks that could not be completed. An earlier export exposed ISA-tools unit-reference errors; their cause and applicability to current exports need a reproducible recheck ([historical evidence](audits/2026-11-xjtu-existing-export.md)).
- **Measurements and units:** Finalize representations for known, unknown and not-applicable answers; validate numerical rates and identifiers; and decide how variable sampling and custom units are represented. Do not infer a measured unit from unrelated metadata.
- **Files and references:** Define remaining CSV details, factor-file references, path portability, symlinks and packaging of empty directories. Existing checks do not cover every reference or CSV meaning.
- **Time and study structure:** Define time references and time-varying factor files, and review the paper's `<factor>_time_reference` convention. The global timeline, local zero-start requirement and diagnostic measurement-window semantics remain open; matching timestamps alone does not establish synchronization. See [timeline future work](future-work/global-measurement-timeline.md).
- **Processing provenance:** Verify the processed-only placeholder against ISA graph requirements; define an explicit unknown-processing answer and the representation of changes to sampling rate or units. Test raw-only, processed-only and combined cases from dataset creation through reading, including multiple runs. A previously observed processing-description loss was fixed in the tested implementation; older exports are not automatically repaired ([historical evidence](audits/2026-11-processing-mode-pipeline.md)).
- **Physical devices and extensions:** Finalize device identity consistency, comment cardinality, missing and duplicate values, and which application-specific information belongs in the portable format.
- **Examples and interoperability:** Provide compact, redistributable positive and negative fixtures and representative diagnostic, prognostic and raw/processed examples. Test the full pipeline and clean installations without requiring private datasets.

These items are a navigation summary, not a claim that every topic has equal priority. The [rule inventory](first-release-rule-inventory.md) has more detail on individual rules and current coverage.
