# Shared unit and quantity catalogues (draft)

These files are the single shared input for ISA-PHM tools. The first snapshot
is the shared unit catalogue, based on QUDT with local additions.
It is an experimental implementation baseline, not a released ISA-PHM profile
or proof that every entry is suitable for a particular measurement.

- `qudt-units-3.5.2.json`: identifiers, symbols, English names, aliases and
  quantity-kind relationships generated from QUDT 3.5.2.
- `qudt-quantities-3.5.2.json`: QUDT 3.5.2 quantity-kind identifiers and names.
- `isa-phm-quantities.json`: project-defined additions, not QUDT terms.
  Quaternion component is a dimensionless component of an orientation
  quaternion; its identifier is an ISA-PHM URN.
- `../specification/quantity-unit-warning-rules.json`: a separate, deliberately
  narrow set of experimental warnings, not a compatibility catalogue.

QUDT is available under CC BY 4.0; see https://qudt.org/ and the pinned source
URLs in `tools/generate_unit_catalogue.py` and
`tools/generate_quantity_catalogue.py`. The generators require `rdflib`
and network access; generated snapshots and tools using them work offline.
Review generated diffs and run tests before committing an update. Consumers
pin a specification Git commit and update it deliberately; this does not yet
establish a released profile version.

To rebuild the snapshots from the repository root, install `rdflib` and run:

```bash
python catalogues/tools/generate_unit_catalogue.py
python catalogues/tools/generate_quantity_catalogue.py
python -m unittest validator.tests.test_catalogues
```

These maintenance commands download the pinned QUDT source and overwrite the
corresponding JSON snapshots. They are not needed to use the catalogues or
run the validator.

An identifier's presence does not imply that a tool supports conversion,
analysis, or scientific validation for that unit or quantity. Unknown and
not-applicable answers and the custom-term workflow remain separate decisions.
