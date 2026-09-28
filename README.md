# Author

### A human-governed, multi-model writing room for long-form creative work.

**Author** treats AI-generated prose as a proposal, not as authority.

The system prepares source-bound assignments for outside models, records exactly which source revision each
candidate was generated against, validates structured returns, quarantines proposed canon changes, and requires
an explicit human decision before any prose can become authoritative.

It is a small public reference implementation of a larger private writing-room architecture built for long-horizon
creative projects where **provenance, continuity, independence, and human authorship** matter as much as generation quality.

> **Models propose. Deterministic infrastructure verifies. The human author decides.**

## Why this exists

Most AI writing workflows optimize the prompt. Long-form work eventually fails somewhere else:

- a rewrite was produced against stale context;
- a model invented a fact that later sessions quietly treated as canon;
- the newest output replaced better original prose simply because it was newer;
- multiple "independent" reviewers were primed by one another;
- nobody can reconstruct which model saw which version;
- a massive agent burns premium context doing bookkeeping instead of writing.

Author moves those problems out of the prompt and into an explicit control plane.

## Architecture

```text
                         HUMAN AUTHOR
                              │
                        adopt / retain
                              │
                 ┌────────────▼────────────┐
                 │   deterministic room    │
                 │ hashes · state · audit  │
                 └───────┬────────┬────────┘
                         │        │
              exact packet        validated return
                         │        │
          ┌──────────────▼─┐    ┌─▼──────────────┐
          │ ChatGPT / GPT │    │ Gemini / other │
          │ writer/reader │    │ writer/reader  │
          └────────────────┘    └────────────────┘
```

The controller itself makes **no model calls**. That is a feature: premium model context is spent on creative work,
while cheap deterministic code handles custody.

## Core guarantees

- **Source-bound work** — assignments include the exact SHA-256 of their parent source.
- **Fail-closed promotion** — a candidate cannot be applied to a different parent revision.
- **Human-only adoption** — receiving a model return never promotes it.
- **Canon quarantine** — newly invented facts block promotion until separately ratified.
- **Strict return boundaries** — only prose inside the expected enclosure becomes candidate text.
- **Provider independence** — ChatGPT, Gemini, Copilot, local models, or human writers can all use the same packet protocol.
- **Original can win** — generating an alternative does not create an obligation to use it.
- **Private-by-design portfolio** — the included novel and provider return are synthetic.

## Quick start

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -e . pytest
pytest

author-room demo --root .author-room
```

That creates a source-bound packet at `.author-room/DEMO_PACKET.md`. Send the packet to any writing model, bring
its complete return back, validate it, compare it with the parent, and record the human decision.

## Minimal Python example

```python
from author import WritingRoom

parent = "The original scene."
room = WritingRoom(".author-room")
assignment = room.prepare_assignment(
    source_label="chapter-01.md",
    source_text=parent,
    channel="chatgpt",
    brief="Write a genuinely different alternative. Preserve the outcome.",
)

packet = room.render_packet(assignment, parent)
print(packet)  # hand this packet to a model or human writer
```

Expected return protocol:

```text
<<<BEGIN_CANDIDATE>>>
replacement prose
<<<END_CANDIDATE>>>
NEW_CANON: NONE
```

The model has generated a **candidate**, not an edit to the book.

## What makes it different from a normal agent framework

Author intentionally keeps the most consequential authority **out of the model loop**. A model can write,
criticize, or propose. It cannot silently mutate the authoritative manuscript merely because it produced a plausible answer.

This pattern is useful anywhere a nondeterministic model proposes changes to a durable human-owned artifact:
long-form fiction, research drafts, policy documents, design systems, legal drafting workflows, and other
multi-session knowledge work.

## Repository map

```text
src/author/               deterministic controller
examples/synthetic_novel/ public, invented demonstration source
tests/                    provenance and fail-closed tests
docs/ARCHITECTURE.md      system model and invariants
docs/THREAT_MODEL.md      failure modes and controls
docs/DESIGN_DECISIONS.md  engineering rationale
docs/PORTFOLIO.md         what the project demonstrates
.github/workflows/ci.yml   multi-version test + privacy guard
```

## Privacy boundary

This repository intentionally contains **no unpublished production manuscript, personal author corpus, real
provider transcript, API credential, or production Writing Room state**. The public example is synthetic.

## Status

`v0.1.0` is the portfolio/reference implementation. It proves the custody protocol and the core authority boundary;
it is not a hosted SaaS product and does not claim to automate literary judgment.

## License

MIT. See [LICENSE](LICENSE).
