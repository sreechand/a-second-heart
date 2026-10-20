# Build tools

`validate_corpus.py` checks the five required columns, valid 24-hour times,
and an optional record count before rendering:

```sh
python3 tools/validate_corpus.py --expected-records 11276
```

`build_clean_corpus.py` combines a base corpus with rows expanded for every
distinct timestamp in a quote. It removes the matching original quote before
adding the distinct expanded rows:

```sh
python3 tools/build_clean_corpus.py base.csv expanded.csv output.csv \
  --expected-records 11276
```

Rendered images belong in a local build folder or `timelit/images/`; they are
not committed to GitHub.
