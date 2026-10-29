"""PostToolUse hook: ask for a `_beautyfact` version of each newly written artifact.

Runs after the Write tool. When the written file is a document the user reviews
(see is_artifact; never a `_beautyfact` version), it tells the parent agent, through
additionalContext, to delegate `<name>_beautyfact.md` to the beautyfact subagent.
The parent does not write it. A hook cannot write the diagrams itself. It never
blocks: any problem (unexpected input) is ignored silently.

Edit the constants below to change which documents get a mirror.
"""

import json
import sys
from pathlib import Path

# Folders, relative to the project root, where review documents are looked for.
# openspec = OpenSpec changes · .specify and specs = Spec Kit constitution and features.
WATCHED_ROOTS = ("openspec", ".specify", "specs")
# Folder names whose .md files all count, at any depth (for example acceptance checklists).
WATCHED_ANYWHERE = ("acceptance",)
# Only documents the user reviews get a mirror. Inside the watched roots, that is
# these file names (OpenSpec change and Spec Kit feature artifacts)…
REVIEW_NAMES = (
    "proposal.md", "design.md", "tasks.md", "spec.md",  # OpenSpec (+ Spec Kit spec/tasks)
    "constitution.md", "plan.md", "research.md", "data-model.md", "quickstart.md",  # Spec Kit
)
# …plus any .md in these folders (Spec Kit contracts and checklists).
REVIEW_DIRS = ("contracts", "checklists")
# Never mirrored: finished work, scaffolding, and instructions for agents
# (openspec/changes/archive, .specify/templates, openspec/AGENTS.md, project.md…).
SKIP_DIRS = ("archive", "templates", "scripts", "node_modules")

ROOT = Path(__file__).resolve().parents[2]
SUFFIX = "_beautyfact"


def is_artifact(path: Path) -> bool:
    if path.suffix.lower() != ".md" or path.stem.endswith(SUFFIX):
        return False
    try:
        parts = path.resolve().relative_to(ROOT).parts
    except ValueError:
        return False
    folders = parts[:-1]
    if any(name in folders for name in SKIP_DIRS):
        return False
    if any(name in folders for name in WATCHED_ANYWHERE):
        return True
    # OpenSpec: only open changes. openspec/specs/ is rewritten on archive, not reviewed.
    if parts[0] == "openspec" and parts[1:2] != ("changes",):
        return False
    return parts[0] in WATCHED_ROOTS and (
        path.name.lower() in REVIEW_NAMES or any(name in folders for name in REVIEW_DIRS)
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
    need = (
        f"Its beautyfact mirror {companion} already exists: ask the subagent to update it. "
        if companion.is_file()
        else f"A beautyfact mirror is required at {companion}. "
    )
    message = (
        f"Artifact written: {target}. {need}"
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
