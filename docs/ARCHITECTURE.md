# Architecture

Sovereign Author separates **creative generation** from **authoritative custody**.

```text
                     HUMAN AUTHOR
                         │
                  explicit decision
                         │
        ┌────────────────▼────────────────┐
        │ Deterministic Writing Room      │
        │ source hashes · state · audit   │
        └───────┬──────────────┬──────────┘
                │              │
        source-bound packet    │ validated return
                │              │
          ┌─────▼─────┐  ┌─────▼─────┐
          │ Model A   │  │ Model B   │     ...
          │ writer    │  │ reader    │
          └───────────┘  └───────────┘
```

## Core invariants

1. **Source binding.** Every assignment carries the SHA-256 of the source it was prepared against.
2. **Model outputs are candidates.** Receipt is not adoption.
3. **Human-only promotion.** Promotion requires an explicit human decision object.
4. **Canon quarantine.** A candidate that proposes new canon cannot be promoted until that canon is separately ratified.
5. **Parent mismatch fails closed.** A candidate cannot be applied to a different source revision.
6. **Provider independence.** The controller does not require a particular model provider.
7. **Deterministic custody.** Hashing, storage, parsing, and promotion rules do not depend on model judgment.

## Why this architecture

Long-form creative work has a different failure mode from ordinary chat: a plausible sentence can silently
change continuity, erase a better parent passage, or become "canon" merely because later models saw it.
Sovereign Author treats creative model output as an external proposal and keeps the authoritative state local.
