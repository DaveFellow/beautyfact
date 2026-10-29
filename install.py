#!/usr/bin/env python3
"""Install the beautyfact skill, subagent, and three hooks into a project.

Usage: python3 install.py [--auto | --manual] [target-project-dir]
       (default target: current directory)

Asks whether mirrors are made automatically (the companion hook asks for one
each time a document to review is written) or only when you call the skill
yourself (/beautyfact <file>). --auto / --manual answer it up front; without a
terminal one of them is required.

This script covers Claude Code and Cursor only. Other harnesses are
listed in HARNESS.md.

Copies the skill to <target>/.claude/skills/beautyfact/ and the hooks to
<target>/.claude/hooks/, then adds them to <target>/.claude/settings.json.
Adds .beautyfact/ (source copies kept for mirror updates) to <target>/.gitignore
and ends with a reminder to choose the subagent's model.
Also copies agents/beautyfact.md to <target>/.cursor/agents/ and
<target>/.claude/agents/, and rules/beautyfact-subagent.mdc to
<target>/.cursor/rules/ and (without its frontmatter) to
<target>/.claude/rules/beautyfact-subagent.md. Safe to run again: existing hook entries are not
duplicated, and the old settings.json is saved as settings.json.bak before
it changes.
"""

import json
import shutil
import sys
from pathlib import Path

KIT = Path(__file__).resolve().parent
COMPANION = "beautyfact_companion.py"
HOOKS = (
    # (file, PostToolUse matcher, status message)
    (COMPANION, "Write", "Delegating the beautyfact version"),
    ("beautyfact_check.py", "Write|Edit", "Checking the beautyfact file"),
    ("beautyfact_read_guard.py", "Read", "Checking for a beautyfact pair"),
)
# Run by the subagent, not registered as a hook.
TOOLS = ("beautyfact_relink.py",)
# Copies of each source kept beside its mirror by beautyfact_check.py.
IGNORE = ".beautyfact/"
MODELS = """\
Model: the subagent ships with `model: inherit` (it uses the parent's model).
Set `model:` in .claude/agents/beautyfact.md and .cursor/agents/beautyfact.md
to choose another. Suggested:
  Claude Code  inherit, or sonnet for speed (haiku only after checking its
               mirrors by hand: the checker does not catch missing content)
  Cursor       inherit, or the model you trust most for long structured
               writing; with a reasoning model (Grok, GPT), pick a lower
               reasoning effort if Cursor offers one and compare the result
Check a mirror by hand after any change of model."""


def copy_files(target: Path, claude: Path) -> None:
    skill = claude / "skills" / "beautyfact"
    if skill.exists():
        shutil.rmtree(skill)
    shutil.copytree(KIT / "skills" / "beautyfact", skill)
    (claude / "hooks").mkdir(parents=True, exist_ok=True)
    for name in [h[0] for h in HOOKS] + list(TOOLS):
        shutil.copy2(KIT / "hooks" / name, claude / "hooks" / name)
    agent = KIT / "agents" / "beautyfact.md"
    rule = KIT / "rules" / "beautyfact-subagent.mdc"
    for dest in (target / ".cursor" / "agents", claude / "agents"):
        dest.mkdir(parents=True, exist_ok=True)
        shutil.copy2(agent, dest / "beautyfact.md")
    rules = target / ".cursor" / "rules"
    rules.mkdir(parents=True, exist_ok=True)
    shutil.copy2(rule, rules / "beautyfact-subagent.mdc")
    # Claude Code loads a rule with no `paths:` frontmatter in every session; the
    # Cursor frontmatter (description, alwaysApply) means nothing there, so drop it.
    body = rule.read_text().split("---", 2)[2].lstrip("\n")
    (claude / "rules").mkdir(parents=True, exist_ok=True)
    (claude / "rules" / "beautyfact-subagent.md").write_text(body)


def ask_auto(args: list[str]) -> bool:
    if "--auto" in args or "--manual" in args:
        return "--auto" in args
    if not sys.stdin.isatty():
        sys.exit("Pass --auto (mirror each document to review as it is written) or --manual (only when you call /beautyfact).")
    print("Make beautyfact mirrors automatically?")
    print("  a) automatic: each spec, plan, task list... you should review gets a mirror when it is written")
    print("  m) manual: only when you call the skill yourself (/beautyfact <file>)")
    while True:
        answer = input("[a/m]: ").strip().lower()
        if answer in ("a", "m"):
            return answer == "a"


def register(settings_path: Path, auto: bool) -> tuple[list[str], list[str]]:
    settings = json.loads(settings_path.read_text()) if settings_path.is_file() else {}
    groups = settings.setdefault("hooks", {}).setdefault("PostToolUse", [])
    added, removed = [], []
    if not auto:
        # Manual mode: drop the companion hook left by an earlier automatic install.
        for g in groups:
            kept = [h for h in g.get("hooks", []) if COMPANION not in h.get("command", "")]
            if len(kept) != len(g.get("hooks", [])):
                g["hooks"] = kept
                removed = [COMPANION]
        groups[:] = [g for g in groups if g.get("hooks")]
    for name, matcher, message in HOOKS:
        if name == COMPANION and not auto:
            continue
        command = f'python3 "$CLAUDE_PROJECT_DIR/.claude/hooks/{name}"'
        if any(name in h.get("command", "") for g in groups for h in g.get("hooks", [])):
            continue
        group = next((g for g in groups if g.get("matcher") == matcher), None)
        if group is None:
            group = {"matcher": matcher, "hooks": []}
            groups.append(group)
        group["hooks"].append({"type": "command", "command": command, "statusMessage": message})
        added.append(name)
    if added or removed:
        if settings_path.is_file():
            shutil.copy2(settings_path, settings_path.with_name(settings_path.name + ".bak"))
        settings_path.parent.mkdir(parents=True, exist_ok=True)
        settings_path.write_text(json.dumps(settings, indent=2) + "\n")
    return added, removed


def ignore_snapshots(target: Path) -> bool:
    gitignore = target / ".gitignore"
    text = gitignore.read_text() if gitignore.is_file() else ""
    if IGNORE in text.split("\n"):
        return False
    gitignore.write_text(text + ("\n" if text and not text.endswith("\n") else "") + IGNORE + "\n")
    return True


def main() -> None:
    args = sys.argv[1:]
    paths = [a for a in args if not a.startswith("--")]
    target = Path(paths[0] if paths else ".").resolve()
    if not target.is_dir():
        sys.exit(f"Not a directory: {target}")
    auto = ask_auto(args)
    claude = target / ".claude"
    copy_files(target, claude)
    added, removed = register(claude / "settings.json", auto)
    print(f"Installed in {claude}")
    print(f"Subagent: {target / '.cursor' / 'agents' / 'beautyfact.md'}")
    print("Hooks registered: " + (", ".join(added) if added else "already present"))
    if removed:
        print("Hooks removed: " + ", ".join(removed))
    if auto:
        print("Mode: automatic. Which documents get a mirror: REVIEW_NAMES and the folder")
        print("constants in .claude/hooks/beautyfact_companion.py")
    else:
        print("Mode: manual. Ask for a mirror with /beautyfact <file> (re-run with --auto to switch)")
    if ignore_snapshots(target):
        print(f"Added {IGNORE} to {target / '.gitignore'}")
    print()
    print(MODELS)


if __name__ == "__main__":
    main()
