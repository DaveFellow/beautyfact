"""PostToolUse hook: ask for a `_beautyfact` version of each newly written artifact.

Runs after the Write tool. When the written file is a .md inside a watched folder
(and is not itself a `_beautyfact` version), it tells the parent agent, through
additionalContext, to delegate `<name>_beautyfact.md` to the beautyfact subagent.
The parent does not write it. A hook cannot write the diagrams itself. It never
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
        f"Tell the subagent this artifact follows {kit}, so it must also read "
        f"references/source-formats.md ({kit} section) beside the skill: it names the diagram "
        f"to draw for each source section (for example one small diagram per decision, trees "
        f"for capabilities and impact). "
        if kit
        else ""
    )
    message = (
        f"Artifact written: {target}. A beautyfact mirror is required at {companion}. "
        f"Do not write it yourself and do not read the beautyfact examples. "
        f"ALWAYS delegate to the beautyfact subagent and wait for it "
        f"(Cursor: Task tool, subagent_type beautyfact, foreground). "
        f"Pass paths, not the file body: source {target}, destination {companion}, "
        f"the original stays untouched, and the skill is .claude/skills/beautyfact/SKILL.md "
        f"(skills/beautyfact/SKILL.md in the kit repo). {formats}"
        f"The subagent reads the skill and writes the mirror."
    )
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": message}}))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
