# Engineering case study

## Problem

Long-form AI-assisted writing is not primarily a prompting problem. Over many sessions, the difficult failures are
state failures: stale rewrites, silent canon drift, lost provenance, accidental replacement of better source prose,
cross-contaminated reviewers, and expensive model context spent repeatedly reconstructing bookkeeping.

The design challenge was therefore:

> How can multiple nondeterministic creative systems contribute to one durable work without any model becoming the
> unobserved authority over the artifact?

## Constraints

The system was designed around several non-negotiable constraints:

1. The human author remains the final authority.
2. A model output is never authoritative merely because it exists.
3. Every candidate must be traceable to the exact source version it saw.
4. New world facts and preferred prose are different decisions.
5. Independent readers/writers should be isolatable from one another.
6. Deterministic work should not consume premium creative-model context.
7. The public portfolio must demonstrate the architecture without exposing the private production manuscript.

## Architecture

Author splits the workflow into two planes.

### Creative plane

External writers and readers — GPT, Gemini, Copilot, local models, or humans — receive bounded source packets and
return candidate prose or analysis.

### Custody plane

Local deterministic code owns:

- SHA-256 source identity
- assignment IDs
- packet construction
- candidate parsing
- return hashes
- durable state
- explicit human decisions
- parent/candidate compatibility checks
- canon-change quarantine

The custody plane deliberately makes no model calls.

## Why source hashes matter

A fluent rewrite can be completely valid against yesterday's chapter and destructive against today's chapter.
Each assignment therefore records the source SHA-256. Promotion re-hashes the current parent and fails closed if
the candidate was created against a different revision.

This converts a vague editorial risk — "is this response stale?" — into a deterministic invariant.

## Why canon is separate from prose

Creative models can improve a scene while quietly inventing a sibling, rank, object, relationship, date, or rule.
Aesthetically preferring the prose does not imply approval of that new fact.

Returns therefore declare `NEW_CANON`. A candidate containing new canon is quarantined from promotion until the
fact is separately ratified.

## Why the original is allowed to win

Generation itself creates selection pressure: once an alternative exists, teams often feel compelled to use it.
Author rejects that premise. The parent remains a first-class candidate, and "retain parent" is an explicit decision.

This is important in creative systems because optimization pressure can gradually make prose more homogeneous even
when every local rewrite appears defensible.

## Failure behavior

The reference implementation demonstrates fail-closed behavior for:

- parent-source mismatch
- malformed/duplicate candidate enclosures
- unratified canon proposals
- promotion without an explicit adoption decision

That is intentionally different from asking another model to "double check" the first model.

## Evidence

The public release includes seven deterministic tests and GitHub Actions runs them on Python 3.10–3.13.
CI also includes a privacy guard designed to fail if protected production names appear in the public repository.

The included source text and model return are synthetic, so the complete workflow is inspectable without publishing
the private work that motivated the design.

## What I would build next

The production architecture is substantially larger than this public reference implementation. Useful public
extensions would include:

- explicit canon-ratification objects
- neutral A/B/C comparison packet generation
- resumable provider-session ledgers
- richer malformed-return recovery
- content-addressed audit export
- a small local dashboard for assignment and candidate state

Those extensions should preserve the core rule:

> Models may propose increasingly sophisticated changes. Authority remains explicit, inspectable, and human.
