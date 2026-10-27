"""PostToolUse hook: ask for a `_beautyfact` version of each newly written artifact.

Runs after the Write tool. When the written file is a .md inside a watched folder
(and is not itself a `_beautyfact` version), it tells the agent, through
additionalContext, to write `<name>_beautyfact.md` next to it following the
beautyfact skill. A hook cannot write the diagrams itself; the agent does. It never
blocks: any problem (unexpected input) is ignored silently.

Edit the two constants below to change which folders are watched.
"""

import json
import sys
from pathlib import Path

# Folders, relative to the project root, whose .md files get a companion.
# openspec = OpenSpec changes · .specify and specs = Spec Kit constitution and features.
WATCHED_ROOTS = ("openspec", ".specify", "specs")
# Folder names that count at any depth (for example acceptance checklists).
WATCHED_ANYWHERE = ("acceptance",)

ROOT = Path(__file__).resolve().parents[2]
SUFFIX = "_beautyfact"


def is_artifact(path: Path) -> bool:
    if path.suffix.lower() != ".md" or path.stem.endswith(SUFFIX):
        return False
    try:
        parts = path.resolve().relative_to(ROOT).parts
    except ValueError:
        return False
    return parts[:1] in [(r,) for r in WATCHED_ROOTS] or any(
        name in parts[:-1] for name in WATCHED_ANYWHERE
    )


def main() -> None:
    payload = json.load(sys.stdin)
    target = (payload.get("tool_input") or {}).get("file_path") or ""
    if not target or not is_artifact(Path(target)):
        return
    path = Path(target)
    companion = path.with_name(path.stem + SUFFIX + path.suffix)
    parts = path.resolve().relative_to(ROOT).parts
    kit = "OpenSpec" if parts[:1] == ("openspec",) else "Spec Kit" if parts[:1] in ((".specify",), ("specs",)) else ""
    formats = (
        f"This artifact follows {kit}, so also read .claude/skills/beautyfact/references/source-formats.md "
        f"({kit} section): it names the diagram to draw for each source section (for example one "
        f"small diagram per decision, trees for capabilities and impact). "
        if kit
        else ""
    )
    message = (
        f"Artifact written: {target}. Now write its beautyfact version to {companion}, "
        f"following .claude/skills/beautyfact/SKILL.md. Read that file fully first, then "
        f".claude/skills/beautyfact/references/examples/opener.md, entries.md and the other "
        f"example files its table lists for the sections you convert. {formats}Its 'Notation' section "
        f"(emoji icons, 💬 before UI text, bold «names», ──▶ arrows) and 'The _beautyfact version "
        f"of an existing artifact' section apply even if the source has none of them. "
        f"Same content, beautyfact format; leave the original untouched."
    )
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": message}}))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
