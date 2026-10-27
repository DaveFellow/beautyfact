#!/usr/bin/env python3
"""Install the beautyfact skill and its three hooks into a project.

Usage: python3 install.py [target-project-dir]   (default: current directory)

Copies the skill to <target>/.claude/skills/beautyfact/ and the hooks to
<target>/.claude/hooks/, then adds them to <target>/.claude/settings.json.
Safe to run again: existing hook entries are not duplicated, and the old
settings.json is saved as settings.json.bak before it changes.
"""

import json
import shutil
import sys
from pathlib import Path

KIT = Path(__file__).resolve().parent
HOOKS = (
    # (file, PostToolUse matcher, status message)
    ("beautyfact_companion.py", "Write", "Requesting the beautyfact version"),
    ("beautyfact_check.py", "Write|Edit", "Checking the beautyfact file"),
    ("beautyfact_read_guard.py", "Read", "Checking for a beautyfact pair"),
)


def copy_files(claude: Path) -> None:
    skill = claude / "skills" / "beautyfact"
    if skill.exists():
        shutil.rmtree(skill)
    shutil.copytree(KIT / "skills" / "beautyfact", skill)
    (claude / "hooks").mkdir(parents=True, exist_ok=True)
    for name, _, _ in HOOKS:
        shutil.copy2(KIT / "hooks" / name, claude / "hooks" / name)


def register(settings_path: Path) -> list[str]:
    settings = json.loads(settings_path.read_text()) if settings_path.is_file() else {}
    groups = settings.setdefault("hooks", {}).setdefault("PostToolUse", [])
    added = []
    for name, matcher, message in HOOKS:
        command = f'python3 "$CLAUDE_PROJECT_DIR/.claude/hooks/{name}"'
        if any(name in h.get("command", "") for g in groups for h in g.get("hooks", [])):
            continue
        group = next((g for g in groups if g.get("matcher") == matcher), None)
        if group is None:
            group = {"matcher": matcher, "hooks": []}
            groups.append(group)
        group["hooks"].append({"type": "command", "command": command, "statusMessage": message})
        added.append(name)
    if added:
        if settings_path.is_file():
            shutil.copy2(settings_path, settings_path.with_name(settings_path.name + ".bak"))
        settings_path.parent.mkdir(parents=True, exist_ok=True)
        settings_path.write_text(json.dumps(settings, indent=2) + "\n")
    return added


def main() -> None:
    target = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    if not target.is_dir():
        sys.exit(f"Not a directory: {target}")
    claude = target / ".claude"
    copy_files(claude)
    added = register(claude / "settings.json")
    print(f"Installed in {claude}")
    print("Hooks registered: " + (", ".join(added) if added else "already present"))
    print("Watched folders: edit WATCHED_ROOTS / WATCHED_ANYWHERE in .claude/hooks/beautyfact_companion.py")


if __name__ == "__main__":
    main()
