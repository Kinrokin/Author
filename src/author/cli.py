from __future__ import annotations
import argparse
from pathlib import Path
from .room import WritingRoom


def demo(root: Path):
    source = (Path(__file__).parents[2] / "examples" / "synthetic_novel" / "chapter.md")
    if not source.exists():
        source = Path("examples/synthetic_novel/chapter.md")
    text = source.read_text(encoding="utf-8")
    room = WritingRoom(root)
    assignment = room.prepare_assignment(
        source_label="synthetic/chapter.md",
        source_text=text,
        channel="chatgpt",
        brief="Write a genuinely different alternative that preserves the scene outcome. Do not invent new world facts.",
        context=("The parent remains a valid candidate.", "Human approval is required for promotion."),
        assignment_id="DEMO-001",
    )
    packet = room.render_packet(assignment, text)
    out = root / "DEMO_PACKET.md"
    out.write_text(packet, encoding="utf-8")
    print(out)


def main():
    p = argparse.ArgumentParser(prog="author-room")
    sub = p.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("demo", help="prepare a source-bound synthetic writing packet")
    d.add_argument("--root", default=".author-room")
    args = p.parse_args()
    if args.cmd == "demo":
        demo(Path(args.root))


if __name__ == "__main__":
    main()
