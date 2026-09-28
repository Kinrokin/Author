# Design decisions

## The original prose is always a valid candidate
The purpose of a writing model is not to justify its invocation. A generated alternative may lose to the parent.

## No numeric literary winner
Scores are useful for tests, not for deciding whether a paragraph lives. Comparison belongs to the author/editor.

## Models generate; local code remembers
Expensive model context is reserved for reading and writing. Deterministic code handles hashing, provenance,
state, and validation.

## New facts require a different kind of approval
A sentence can be beautiful and still smuggle in a world fact. Prose preference and canon ratification are therefore
separate decisions.

## Public demo is synthetic
The portfolio must demonstrate the architecture without publishing the private manuscript that motivated it.
