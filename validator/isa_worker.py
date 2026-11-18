"""Run ISA-tools in a separate process; its validator uses global state."""

import io
import json
import logging
import sys


def main():
    from isatools import isajson
    from isatools.model import Assay

    # 0.14.3's study-group checker formats assay.identifier, but its Assay
    # model only exposes filename. Supply a display label, without changing
    # the dataset or the study-group checks. This is confined to the worker.
    if not hasattr(Assay, "identifier"):
        Assay.identifier = property(lambda assay: assay.filename or "(unnamed assay)")

    messages = io.StringIO()
    logger = isajson.validate.__globals__["log"]
    handler = logging.StreamHandler(messages)
    logger.addHandler(handler)
    exceptions = []

    def trace(frame, event, argument):
        if frame.f_code is isajson.validate.__code__ and event == "exception":
            exc_type, exc, _ = argument
            exceptions.append(f"{exc_type.__name__}: {exc}")
        return trace

    try:
        # ISA-tools 0.14.3 suppresses uncaught exceptions in a finally return.
        # Capture the last one so an aborted validator is never called a pass.
        sys.settrace(trace)
        with open(sys.argv[1], encoding="utf-8-sig") as source:
            report = isajson.validate(source, config_dir=sys.argv[2], log_level=logging.INFO)
    finally:
        sys.settrace(None)
        logger.removeHandler(handler)
    output = {
        "errors": report.get("errors", []),
        "warnings": report.get("warnings", []),
        "completed": "Finished validation..." in messages.getvalue(),
        "exception": exceptions[-1] if exceptions else None,
        # Some ISA-tools 0.14.3 checks log errors without adding them to the
        # returned errors list. Preserve these diagnostics for the caller.
        "logged_errors": list(dict.fromkeys(line.strip() for line in messages.getvalue().splitlines() if "(E)" in line)),
    }
    print(json.dumps(output))


if __name__ == "__main__":
    main()
