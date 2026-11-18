# Experiments

These are provisional, non-normative cross-repository experiments. They use
the adjacent Backend and Wrapper working trees, so results depend on their
uncommitted changes and installed dependencies. They are not yet the shared
fixture suite or an ISA-PHM conformance test.

Run the processed-only placeholder experiment from the repository root:

```bash
python -m unittest experiments.test_processed_only_placeholder
```

It generates temporary synthetic data only and removes it afterward. The
placeholder field names are illustrative and have not been approved as a
specification rule.

The installed default ISA validator configuration rejects the baseline
fixture's Vibration/Accelerometer combination and stops before graph checks.
The experiment compares the baseline and placeholder errors rather than
claiming full ISA validation succeeded.
