# ISA-JSON field and comment reference

[Specification guide](README.md) · [Investigation](investigation.md) · [Study](study.md) · [Assay](assay.md)

This reference defines canonical ISA-PHM comment names for new exports and lists legacy names accepted when reading older exports. Array notation `[]` means an entry in that array; a comment is an object with `name` and `value`. Paths show JSON nesting, not filesystem paths. Examples on the linked pages show the surrounding objects. Current representation and agreed concepts do not mean every detail is finalized or validated.

## Investigation

| Information | JSON location | Current comment `name` / field |
| --- | --- | --- |
| Purpose | `comments[]` | `experiment_type` |
| Researcher identifier | `comments[]` | `ud_identifier` (separate from root `identifier`) |
| License | `comments[]` | `license` |

## Study and test setup

| Information | JSON location, under `studies[]` | Current comment `name` / field |
| --- | --- | --- |
| Run count | `comments[]` | `total_runs` |
| Setup image | `materials.sources[].comments[]` | `image` (one comment per file) |
| Component identifier | `materials.sources[].characteristics[].comments[]` | `component_id` (legacy: `component ID`) |
| Component datasheet | `materials.sources[].characteristics[].comments[]` or `materials.samples[].characteristics[].comments[]` | `datasheet` |
| Factor definition | `factors[]` | `factorName`, `factorType`, `@id` |
| Factor value | `materials.samples[].factorValues[]` | `category.@id`, `value`, optional `unit.@id` |
| Unit annotation | `unitCategories[]` | `@id`, `annotationValue`, optional `termAccession` |

## Sensor output and physical device

Paths below are under `studies[].assays[]`.

| Information | JSON location | Current comment `name` / field |
| --- | --- | --- |
| Sensor alias | `comments[]` | `sensor_alias` (legacy: `sensor alias`) |
| Sensor datasheet | `comments[]` | `datasheet` |
| Device identity | `comments[]` | `physical_device_id` (legacy: `physical device id`) |
| Device name, model and serial number | `comments[]` | `physical_device_name`, `physical_device_model`, `physical_device_serial_number` (legacy: the same words separated by spaces) |
| Device datasheet | `comments[]` | `physical_device_datasheet` (legacy: `physical device datasheet`) |
| Measured quantity | `measurementType` | `annotationValue`, optional `termAccession` |
| Technology type | `technologyType` | `annotationValue` |
| Sensor model | assay object | `technologyPlatform` |
| Measurement files | `dataFiles[]` | `@id`, `name`, `type` |

Device metadata is optional. An absent datasheet reference does not require a file; the directory itself is required. Whether comments are required and how conflicting device definitions are handled are not fully specified.

## Protocols and processes

| Information | JSON location | Current comment `name` / field |
| --- | --- | --- |
| Sensor identifier | `studies[].protocols[].comments[]` | `sensor_id` (legacy: `Sensor id`), on a measurement protocol |
| Parameter definition | `studies[].protocols[].parameters[]` | `@id`, `parameterName.annotationValue` |
| Process protocol | `studies[].assays[].processSequence[]` | `executesProtocol.@id` |
| Parameter value | `studies[].assays[].processSequence[].parameterValues[]` | `category.@id`, `value`, optional `unit.@id` |
| File association | `studies[].assays[].processSequence[]` | `inputs[].@id`, `outputs[].@id` |
| Unavailable raw input | `studies[].assays[].dataFiles[].comments[]` | `availability: not included` on the provisional pathless placeholder |

`Sampling Rate` and `Measured Unit` are parameter names, not comment names. See the [protocol example](protocols-and-data.md) for how the definitions and process values link.

## Comment naming

ISA-PHM-defined comment names use lowercase words separated by underscores. New exports use canonical names; readers accept the legacy spellings listed above for existing datasets. Unknown comments can contain researcher data and are not renamed. The handling of conflicting canonical and legacy values is not yet specified.
