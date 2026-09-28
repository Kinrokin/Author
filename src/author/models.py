from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Literal

Channel = Literal["chatgpt", "gemini", "copilot", "human", "other"]

@dataclass(frozen=True)
class Assignment:
    id: str
    source_sha256: str
    source_label: str
    channel: Channel
    brief: str
    context: tuple[str, ...] = ()
    expected_enclosure: str = "CANDIDATE"

    def as_dict(self):
        d = asdict(self)
        d["context"] = list(self.context)
        return d

@dataclass(frozen=True)
class Candidate:
    id: str
    assignment_id: str
    source_sha256: str
    channel: Channel
    prose: str
    return_sha256: str
    new_canon: tuple[str, ...] = ()

    def as_dict(self):
        d = asdict(self)
        d["new_canon"] = list(self.new_canon)
        return d

@dataclass(frozen=True)
class Decision:
    candidate_id: str
    action: Literal["adopt", "retain_parent", "reject"]
    human: str
    reason: str
