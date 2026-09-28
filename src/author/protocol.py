from __future__ import annotations
import re
from .integrity import sha256_text

class ProtocolError(ValueError):
    pass


def extract_enclosure(text: str, tag: str = "CANDIDATE") -> str:
    start = f"<<<BEGIN_{tag}>>>"
    end = f"<<<END_{tag}>>>"
    if text.count(start) != 1 or text.count(end) != 1:
        raise ProtocolError(f"expected exactly one {start}/{end} enclosure")
    a = text.index(start) + len(start)
    b = text.index(end)
    if b <= a:
        raise ProtocolError("empty or reversed enclosure")
    return text[a:b].strip("\n")


def extract_new_canon(text: str) -> tuple[str, ...]:
    m = re.search(r"(?mi)^NEW_CANON:\s*(.+?)\s*$", text)
    if not m:
        return ("UNKNOWN",)
    raw = m.group(1).strip()
    if raw.upper() in {"NONE", "UNKNOWN"}:
        return (raw.upper(),)
    return tuple(x.strip() for x in raw.split(";") if x.strip())


def validate_return(text: str, source_sha256: str, tag: str = "CANDIDATE") -> dict:
    prose = extract_enclosure(text, tag)
    return {
        "prose": prose,
        "return_sha256": sha256_text(text),
        "new_canon": extract_new_canon(text),
        "source_sha256": source_sha256,
    }
