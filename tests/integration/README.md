# Optional cross-repository test

`test_processed_only_placeholder.py` exercises raw-only, raw-and-processed,
and processed-only data through the Backend converter, selected specification
checks, and the Wrapper. It uses generated temporary CSVs and a synthetic
Backend test payload; it is not a conformance test or part of the validator's
self-contained test suite.

To run it, check out `ISA-PHM-Backend` and `ISA-PHM-Wrapper` alongside this
repository and install their dependencies, including ISA-tools, in the same
Python environment. From the specification repository root:

```bash
python -m unittest discover -s tests/integration -p test_processed_only_placeholder.py
```

The test skips when its optional imports are unavailable. Its results depend
on the checked-out revisions of the other repositories. The representation of
the processed-only placeholder remains provisional.
