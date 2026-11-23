# Assay and sensor output

[Specification guide](README.md) · [Study](study.md) · Next: [Protocols and data](protocols-and-data.md)

An assay is an entry in `studies[].assays`. In the current ISA-PHM representation, an assay describes one sensor output, its measurement files and the processes connecting them. An accelerometer's X, Y and Z outputs are separate outputs; several files can belong to one output.

```json
{
  "measurementType": {
    "annotationValue": "Acceleration",
    "termAccession": "http://qudt.org/vocab/quantitykind/Acceleration"
  },
  "technologyType": {"annotationValue": "Accelerometer"},
  "technologyPlatform": "PCB 352C33",
  "comments": [
    {"name": "sensor_alias", "value": "Accel_Axial"},
    {"name": "datasheet", "value": "./Datasheets/sensor.pdf"},
    {"name": "physical_device_id", "value": "device-1"},
    {"name": "physical_device_name", "value": "Acquisition device"}
  ],
  "dataFiles": [],
  "processSequence": []
}
```

The fragment is abbreviated. The measurement type is the measured quantity; technology type and model describe the sensor output. An included output needs explicit answers for quantity, technology, model, sampling rate and measured unit. Appropriate `Unknown` or `Not applicable` answers are distinct from a known value; exact encoding and treatment in all cases remain open. The measurement rate and unit are recorded in protocol parameters, not inferred from arbitrary other parameters.

Physical-device grouping is optional. Outputs associated with the same device share a dataset-unique device identifier; it is not necessarily a serial number. A standalone output needs no parent device. The illustrated comments are the current representation, not a finalized mapping. See the [field reference](isa-json-field-inventory.md) for the full set.

Quantity and unit identifiers may refer to entries in the [shared catalogues](../catalogues/README.md). A quantity/unit mismatch may produce an advisory; compatibility coverage is incomplete.
