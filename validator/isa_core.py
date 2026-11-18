"""Optional, offline ISA-tools 0.14.3 ISA 1.0 core JSON Schema check.

This checks JSON structure only. It does not run the ISA-tools configuration,
content, process-graph, or ISA-PHM checks.
"""

import hashlib
import importlib.metadata
import importlib.util
import json
from pathlib import Path

ISA_TOOLS_VERSION = "0.14.3"
JSONSCHEMA_VERSION = "4.23.0"
CORE_SCHEMA_SHA256 = "473b30c6033e743ddd6c571474854187d6736515983387994475037b8ec8786f"
CORE_SCHEMA_COUNT = 21


class SchemaUnavailable(Exception):
    """The pinned schema checker could not run; this is not a validation pass."""


def _schema_directory() -> Path:
    try:
        actual_isa = importlib.metadata.version("isatools")
        actual_jsonschema = importlib.metadata.version("jsonschema")
    except importlib.metadata.PackageNotFoundError as exc:
        raise SchemaUnavailable("Install the optional pinned dependencies from requirements-schema.txt.") from exc
    if actual_isa != ISA_TOOLS_VERSION or actual_jsonschema != JSONSCHEMA_VERSION:
        raise SchemaUnavailable(
            f"Expected isatools {ISA_TOOLS_VERSION} and jsonschema {JSONSCHEMA_VERSION}; "
            f"found {actual_isa} and {actual_jsonschema}."
        )
    spec = importlib.util.find_spec("isatools")
    if not spec or not spec.origin:
        raise SchemaUnavailable("The pinned isatools package could not be located.")
    path = Path(spec.origin).parent / "resources/schemas/isa_model_version_1_0_schemas/core"
    files = sorted(path.glob("*.json"))
    digest = hashlib.sha256()
    for item in files:
        digest.update(item.name.encode("utf-8"))
        digest.update(b"\0")
        digest.update(item.read_bytes())
        digest.update(b"\0")
    if len(files) != CORE_SCHEMA_COUNT or digest.hexdigest() != CORE_SCHEMA_SHA256:
        raise SchemaUnavailable("Installed ISA core schema files differ from the pinned 0.14.3 baseline.")
    return path


def check_isa_core(document: object) -> list[str]:
    """Return core-schema errors; raise SchemaUnavailable if checks cannot run."""
    try:
        from jsonschema import Draft202012Validator, FormatChecker
        from referencing import Registry
        from referencing.jsonschema import DRAFT202012
        directory = _schema_directory()
        resources = []
        for path in sorted(directory.glob("*.json")):
            content = json.loads(path.read_text(encoding="utf-8"))
            resources.append((path.resolve().as_uri(), DRAFT202012.create_resource(content)))
        registry = Registry().with_resources(resources)
        # Mirror ISA-tools' own local file-URI schema resolution. No remote
        # retrieval is configured, including for unresolved references.
        schema = {"$ref": (directory / "investigation_schema.json").resolve().as_uri(),
                  "$schema": "https://json-schema.org/draft/2020-12/schema"}
        validator = Draft202012Validator(schema, registry=registry, format_checker=FormatChecker())
        messages = []
        for error in validator.iter_errors(document):
            location = "$" + "".join(f"[{part}]" if isinstance(part, int) else f".{part}" for part in error.absolute_path)
            messages.append(f"{location}: {error.message}")
        return sorted(messages)
    except SchemaUnavailable:
        raise
    except Exception as exc:
        raise SchemaUnavailable(f"ISA core schema checks could not be completed: {type(exc).__name__}: {exc}") from exc
