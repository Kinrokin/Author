# Threat model

| Threat | Failure | Control |
|---|---|---|
| Stale-context rewrite | Candidate targets an older manuscript | SHA-256 source binding |
| Silent canon invention | Plausible new fact becomes accepted | `NEW_CANON` quarantine |
| Model self-approval | Generator promotes its own prose | separate human decision required |
| Malformed return | Commentary leaks into prose | strict begin/end enclosure parser |
| Cross-provider contamination | Writers converge on leaked alternatives | packet isolation by workflow |
| Lost provenance | Cannot prove where prose came from | immutable content hashes + assignment IDs |
| Accidental private publishing | Manuscript reaches portfolio repo | public synthetic corpus + CI privacy guard |

The system does not claim to prove literary quality or truthfulness of a model's statements about what it read.
It narrows the mechanical trust surface so literary judgment stays visible and human.
