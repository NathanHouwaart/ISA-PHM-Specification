# Study

[Specification guide](README.md) · [Investigation](investigation.md) · Next: [Assay](assay.md)

A study is an entry in the investigation's `studies` array. It groups the test setup, factors, protocol definitions and assays relevant to the study. Its meaning depends on the experiment; the relationship between diagnostic measurement windows and runs remains open for later design.

```json
{
  "title": "Bearing 1_1",
  "comments": [{"name": "total_runs", "value": "123"}],
  "factors": [{"@id": "#factor/speed", "factorName": "Rotational speed"}],
  "materials": {
    "sources": [],
    "samples": [{
      "@id": "#sample/run-1",
      "factorValues": [{"category": {"@id": "#factor/speed"}, "value": "2100"}]
    }]
  },
  "protocols": [],
  "assays": []
}
```

This abbreviated fragment illustrates the current structure. A factor's definition is in `studies[].factors`; its value is in `studies[].materials.samples[].factorValues`. The value's `category.@id` refers to its factor definition. A unit can reference a study unit annotation. Source and sample characteristics can describe setup components; current exports store setup image paths in source comments and component datasheets in characteristic comments. See the [field reference](isa-json-field-inventory.md).

A scalar operating condition or fault label is recorded directly as a factor value. A time-varying operating condition is represented by a referenced CSV; the detailed file convention and reference-time semantics remain open. The present `total_runs` comment is metadata; the Wrapper derives runs from processes rather than verifying that count.

Study-level `protocols` define measurement and processing protocols; assay processes refer to them. See [protocols and data](protocols-and-data.md).
