# Contributing

Author is intentionally small. Contributions should strengthen provenance, recovery, portability, or the clarity of
the human authority boundary without turning the controller into an autonomous literary judge.

## Development

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e . pytest
pytest
```

## Pull requests

Please include:

- the failure mode or invariant being addressed;
- tests for behavioral changes;
- no unpublished manuscripts, real provider transcripts, credentials, or personal author data;
- an explanation if a change increases model authority over durable state.

The public synthetic corpus should remain sufficient to exercise new functionality.
