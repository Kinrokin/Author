from __future__ import annotations
from pathlib import Path
import uuid
from .integrity import sha256_text
from .models import Assignment, Candidate, Decision
from .protocol import validate_return
from .store import Store

class WritingRoom:
    """Deterministic controller. It never calls a model itself."""

    def __init__(self, root: str | Path):
        self.store = Store(root)

    def register_source(self, label: str, text: str) -> str:
        digest = self.store.put_object(text, ".md")
        self.store.write_json("working", "source", {"label": label, "sha256": digest})
        return digest

    def prepare_assignment(self, *, source_label: str, source_text: str, channel: str, brief: str,
                           context: tuple[str, ...] = (), assignment_id: str | None = None) -> Assignment:
        source_sha = self.store.put_object(source_text, ".md")
        assignment_id = assignment_id or f"A-{uuid.uuid4().hex[:10]}"
        a = Assignment(assignment_id, source_sha, source_label, channel, brief, context)
        self.store.write_json("assignments", a.id, a.as_dict())
        return a

    def render_packet(self, assignment: Assignment, source_text: str) -> str:
        if sha256_text(source_text) != assignment.source_sha256:
            raise ValueError("source text does not match the assignment source hash")
        context = "\n".join(f"- {x}" for x in assignment.context) or "- none"
        return f"""# SOURCE-BOUND WRITING ASSIGNMENT

Assignment: {assignment.id}
Channel: {assignment.channel}
Source: {assignment.source_label}
Source SHA-256: {assignment.source_sha256}

## Brief
{assignment.brief}

## Context constraints
{context}

## Source
<<<BEGIN_SOURCE>>>
{source_text}
<<<END_SOURCE>>>

Return replacement prose only inside:
<<<BEGIN_{assignment.expected_enclosure}>>>
...
<<<END_{assignment.expected_enclosure}>>>

After the enclosure, include exactly one line:
NEW_CANON: NONE
or
NEW_CANON: UNKNOWN
or
NEW_CANON: <semicolon-separated proposals>
"""

    def ingest_return(self, assignment: Assignment, raw_return: str) -> Candidate:
        checked = validate_return(raw_return, assignment.source_sha256, assignment.expected_enclosure)
        rid = self.store.put_object(raw_return, ".txt")
        cid = f"C-{uuid.uuid4().hex[:10]}"
        c = Candidate(cid, assignment.id, assignment.source_sha256, assignment.channel,
                      checked["prose"], rid, tuple(checked["new_canon"]))
        self.store.write_json("returns", rid, {"assignment_id": assignment.id, "sha256": rid})
        self.store.write_json("candidates", cid, c.as_dict())
        return c

    def decide(self, candidate: Candidate, *, action: str, human: str, reason: str) -> Decision:
        if action not in {"adopt", "retain_parent", "reject"}:
            raise ValueError("invalid decision")
        d = Decision(candidate.id, action, human, reason)
        self.store.write_json("decisions", candidate.id, d.__dict__)
        return d

    def promote(self, *, parent_text: str, candidate: Candidate, decision: Decision) -> str:
        if sha256_text(parent_text) != candidate.source_sha256:
            raise ValueError("candidate is not bound to this parent")
        if decision.candidate_id != candidate.id or decision.action != "adopt":
            raise ValueError("human adoption decision required")
        if candidate.new_canon not in {("NONE",), ("UNKNOWN",)}:
            raise ValueError("candidate proposes new canon; ratify separately before promotion")
        self.register_source("working", candidate.prose)
        return candidate.prose
