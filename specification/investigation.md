# Investigation

[Specification guide](README.md) · [Dataset layout](dataset-layout.md) · Next: [Study](study.md)

The investigation is the top-level JSON object for the dataset. It records its title, description, people, publications and studies. A dataset has a diagnostic **or** prognostic purpose; it is not classified as both.

```json
{
  "title": "Bearing investigation",
  "identifier": "investigation-identifier",
  "comments": [
    {"name": "experiment_type", "value": "prognostics-experiment"},
    {"name": "license", "value": "MIT License"}
  ],
  "people": [],
  "publications": [],
  "studies": []
}
```

This abbreviated fragment illustrates the current export, not a standalone valid ISA document. The current Wizard values for `experiment_type` are `diagnostic-experiment` and `prognostics-experiment`. An experimental validator checks that comment, with limitations described in the [validator guide](../validator/README.md). It does not establish the scientific purpose of a dataset.

The investigation identifier and the user-provided identifier in the `ud_identifier` comment are different fields. Comment spellings are listed in the [field reference](isa-json-field-inventory.md). A specification version marker has not yet been selected; an unversioned dataset must not be assumed to claim a particular version.
