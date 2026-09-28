from __future__ import annotations
import json
from pathlib import Path
from .integrity import sha256_text

class Store:
    def __init__(self, root: str | Path):
        self.root = Path(root)
        for name in ["objects", "assignments", "returns", "candidates", "decisions", "working"]:
            (self.root / name).mkdir(parents=True, exist_ok=True)

    def put_object(self, text: str, suffix: str = ".txt") -> str:
        digest = sha256_text(text)
        path = self.root / "objects" / f"{digest}{suffix}"
        if not path.exists():
            path.write_text(text, encoding="utf-8")
        return digest

    def write_json(self, area: str, name: str, value: dict) -> Path:
        path = self.root / area / f"{name}.json"
        path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return path

    def read_json(self, area: str, name: str) -> dict:
        return json.loads((self.root / area / f"{name}.json").read_text(encoding="utf-8"))
