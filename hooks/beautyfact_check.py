"""PostToolUse hook (and CLI): normalize and check a `_beautyfact.md` file.

Runs after Write or Edit. When the file ends in `_beautyfact.md` it:
  1. fixes in place what is mechanical: bold text inside « », and the long arrow `──▶` on
     THEN/NOT/AND lines, in diagrams and in text (the short `→ ↓ ↑ ←` are never right);
  2. checks each source link `(file.md#L10)` or `(file.md#L10-L20)`: the file and lines exist,
     and an entry's ID appears in the first linked line. Only `#L10` is generated now (VS Code
     and Cursor do not jump to GitHub's `#L10-L20` range fragment), but both are still accepted;
  3. checks text diagrams (lines over MAX_WIDTH characters, misaligned box edges) and Mermaid
     diagrams (a safe syntax subset, so a block never renders as an error);
  4. confirms the copy of the source that beautyfact_relink.py set aside in SNAPSHOT_DIR
     beside the mirror, so the next relink compares against the version this mirror follows.

Fixes are silent. Problems come back to the agent as additionalContext. It never blocks.
Manual use: python beautyfact_check.py <file_beautyfact.md>
"""

import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote

SUFFIX = "_beautyfact.md"
# Beside each mirror: the copy of its source from the last clean check (read by beautyfact_relink.py).
SNAPSHOT_DIR = ".beautyfact"
MAX_WIDTH = 74
ARROW_LINE = re.compile(r"^(\s*- )(?:──▶ |→ )?(THEN|NOT|AND|Then|And|But)\b")
LINK_MARK = "🔗"
EMOJI = re.compile(r"[\U0001F300-\U0001FAFF☀-➿⭐]")
CASE_LINE = re.compile(r"^- (?:\[.\] )?(?:\*\*)?(?:(?:GIVEN|WHEN|THEN|NOT|AND|Given|When|Then|And)\b|──▶|→)")
QUOTED = re.compile(r"«([^»*]+)»")
LINK = re.compile(r"\[[^\]]*\]\(([^)#\s]+\.md)#L(\d+)(?:-L(\d+))?\)")
ENTRY_ID = re.compile(r"^\s*(?:- (?:\[.\] )?)?(?:\*\*)?([A-Z]{1,3}-?\d+)\b")
MERMAID_TYPES = ("flowchart TD", "flowchart LR", "sequenceDiagram", "stateDiagram-v2")
MERMAID_MAX_LINES = 25
# A node label opened right after its ID without a quote: core[src/core], ask{trusted?}.
UNQUOTED_LABEL = re.compile(r"\b[A-Za-z_][\w-]*(?:\[\[|\[\(|\(\[|\(\(|\{\{|\[|\(|\{)(?![\"\[\(\{])")
UNQUOTED_EDGE = re.compile(r"\|(?!\")[^|]*\|")
END_NODE = re.compile(r"(?:-->|---|-\.->|==>)\s*end\b|^\s*end\s*(?:-->|---|-\.->|==>)|\bend\[")
MESSAGE = re.compile(r"^\s*\S.*?:(.*)$")


ARROWS = str.maketrans("→↓↑←", "▶▼▲◀")


def normalize(lines: list[str]) -> list[str]:
    out, fence, diagram = [], False, False
    for line in lines:
        if line.lstrip().startswith("```"):
            fence = not fence
            diagram = fence and line.strip().strip("`").strip() in ("", "text")
        elif fence:
            if diagram:
                line = line.translate(ARROWS)
        else:
            line = QUOTED.sub(r"«**\1**»", line)
            line = ARROW_LINE.sub(r"\1──▶ \2", line)
            line = line.replace(" → ", " ──▶ ")
        out.append(line)
    return out


def check_links(path: Path, lines: list[str]) -> list[str]:
    problems, fence = [], False
    sources: dict[str, list[str] | None] = {}
    for n, line in enumerate(lines, 1):
        if line.lstrip().startswith("```"):
            fence = not fence
        if fence:
            continue
        entry = ENTRY_ID.match(line)
        for m in LINK.finditer(line):
            name, start, end = unquote(m.group(1)), int(m.group(2)), int(m.group(3) or m.group(2))
            first_time = name not in sources
            if first_time:
                target = path.parent / name
                sources[name] = target.read_text().split("\n") if target.is_file() else None
            src = sources[name]
            if src is None:
                if first_time:
                    problems.append(f"line {n}: linked file {name} does not exist (further links to it not checked)")
            elif start > end or end > len(src):
                problems.append(f"line {n}: {name} L{start}-L{end} is outside the file ({len(src)} lines)")
            elif entry and entry.group(1) not in src[start - 1]:
                problems.append(f"line {n}: {entry.group(1)} not found at {name} L{start} ({src[start - 1][:40]!r})")
    return problems


def check_diagrams(lines: list[str]) -> list[str]:
    problems, inside, block, lang = [], False, [], ""
    for n, line in enumerate(lines, 1):
        if line.lstrip().startswith("```"):
            if inside:
                problems += mermaid_problems(block) if lang == "mermaid" else box_problems(block)
            else:
                lang = line.strip().strip("`").strip()
            inside, block = not inside, []
        elif inside:
            block.append((n, line))
            if lang != "mermaid" and len(line) > MAX_WIDTH:
                problems.append(f"line {n}: diagram line is {len(line)} characters (max {MAX_WIDTH})")
    return problems


def mermaid_problems(block: list[tuple[int, str]]) -> list[str]:
    """The safe subset of references/diagrams-mermaid.md; anything outside it may render as an error."""
    body = [(n, line) for n, line in block if line.strip() and not line.strip().startswith("%%")]
    if not body:
        return []
    first_n, first = body[0]
    kind = first.strip()
    if kind not in MERMAID_TYPES:
        return [f"line {first_n}: Mermaid type {kind!r} not allowed (use {', '.join(MERMAID_TYPES)})"]
    problems = []
    if len(block) > MERMAID_MAX_LINES:
        problems.append(f"line {first_n}: Mermaid block has {len(block)} lines (max {MERMAID_MAX_LINES}): split it in two")
    depth = 0
    for n, line in body[1:]:
        code = line.strip()
        if code.count('"') % 2:
            problems.append(f"line {n}: odd number of quotes (write #quot; inside a label)")
        if EMOJI.search(code):
            problems.append(f"line {n}: emoji inside a Mermaid diagram")
        if kind.startswith("flowchart"):
            if code.startswith("subgraph"):
                depth += 1
            elif code == "end":
                depth -= 1
            # Drop quoted text first: brackets and pipes inside labels are fine.
            bare = re.sub(r'"[^"]*"', '""', code)
            if UNQUOTED_LABEL.search(bare.removeprefix("subgraph ")):
                problems.append(f"line {n}: node label without double quotes (write id[\"label\"])")
            if UNQUOTED_EDGE.search(bare):
                problems.append(f"line {n}: edge label without double quotes (write -->|\"label\"|)")
            if code != "end" and END_NODE.search(bare):
                problems.append(f"line {n}: `end` used as a node ID (rename it)")
        elif (m := MESSAGE.match(code)) and ";" in m.group(1):
            problems.append(f"line {n}: `;` in message text breaks the diagram (write , or ·)")
    if depth:
        problems.append(f"line {first_n}: subgraph without a matching end")
    return problems


def box_problems(block: list[tuple[int, str]]) -> list[str]:
    problems = []
    for i, (n, line) in enumerate(block):
        for left in (c for c, ch in enumerate(line) if ch == "┌"):
            right = line.find("┐", left)
            if right < 0:
                continue
            for m, below in block[i + 1:]:
                if len(below) <= right or below[right] not in "│┐┘┤┬┴┼":
                    problems.append(f"line {m}: box edge not aligned with the ┐ of line {n} (column {right + 1})")
                    break
                if below[left] == "└":
                    break
    return problems


def check_structure(path: Path, lines: list[str]) -> list[str]:
    """Quality warnings: subsections without a source link, sections without a diagram, invented checkboxes."""
    problems, fence = [], False
    has_links = any(LINK.search(line) for line in lines)
    source = next((path.parent / unquote(m.group(1)) for line in lines if (m := LINK.search(line))), None)
    source_text = source.read_text() if source and source.is_file() else ""
    section, body, diagram, boxes = None, 0, False, []

    def close_section() -> None:
        if section and body >= 6 and not diagram:
            problems.append(f"line {section[0]}: section has no diagram ({section[1][:40]!r})")

    for n, line in enumerate(lines, 1):
        if line.lstrip().startswith("```"):
            fence, diagram = not fence, True
            continue
        if fence:
            continue
        if line.startswith("## "):
            close_section()
            section, body, diagram = (n, line), 0, False
        elif line.startswith("|"):
            diagram = True
        elif line.strip():
            body += 1
        if has_links and re.match(r"#{3,4} ", line) and "🔗" not in line:
            problems.append(f"line {n}: subsection heading has no 🔗 source link")
        if source_text and re.match(r"\s*- \[ \] ", line) and "[ ]" not in source_text:
            boxes.append(n)
    close_section()
    problems += check_emojis(lines)
    if boxes:
        problems.append(f"line {boxes[0]}: {len(boxes)} checkboxes, but the source has none (remove them)")
    return problems


def check_emojis(lines: list[str]) -> list[str]:
    """Every top-level bullet carries a type emoji before its first 🔗 (WHEN/THEN lines are exempt).

    🔗 marks a link, not a type, so it never counts. A bullet with no link may carry the
    emoji anywhere (a quote marked 💬, for example).
    """
    fence, bare = False, []
    for n, line in enumerate(lines, 1):
        if line.lstrip().startswith("```"):
            fence = not fence
        elif not fence and line.startswith("- ") and not CASE_LINE.match(line):
            if not EMOJI.search(line.split(LINK_MARK, 1)[0]):
                bare.append(n)
    if bare:
        shown = ", ".join(str(n) for n in bare[:8])
        return [f"{len(bare)} top-level bullets have no type emoji before their 🔗 link (lines {shown}): "
                f"add one for their type (📌 rule, 🧭 decision, 🎯 result…); an ID may come first, as in `- RF-04 📌 …`"]
    return []


NUMBER_WORDS = {w: i for i, w in enumerate(
    "zero one two three four five six seven eight nine ten eleven twelve".split())}
COUNT_PHRASE = re.compile(r"\b(\d+|" + "|".join(NUMBER_WORDS) + r")\s+(areas|groups|columns|phases|steps)\b", re.I)


def check_counts(lines: list[str]) -> list[str]:
    """A paragraph that says "N areas" and is followed by a diagram: the diagram must have N rows."""
    problems = []
    for n, line in enumerate(lines):
        m = COUNT_PHRASE.search(line)
        if not m or n + 1 >= len(lines):
            continue
        nxt = next((k for k in range(n + 1, min(n + 4, len(lines))) if lines[k].startswith(("```", "|"))), None)
        if nxt is None:
            continue
        rows = []
        if lines[nxt].startswith("|"):
            # A table: every row after the header and its | --- | separator.
            for body in lines[nxt + 2 :]:
                if not body.startswith("|"):
                    break
                rows.append(body)
        for body in [] if rows else lines[nxt + 1 :]:
            if body.startswith("```"):
                break
            if re.match(r"^ \S", body):
                rows.append(body)
        start = line.rfind(". ", 0, m.start()) + 1
        stop = line.find(". ", m.end())
        sentence = line[start : stop if stop >= 0 else len(line)]
        if len(re.findall(r"\b(\d+|" + "|".join(NUMBER_WORDS) + r")\b", sentence, re.I)) > 1:
            continue  # "five groups ... plus six threats": several numbers, rows cannot be matched
        word = m.group(1).lower()
        said = int(word) if word.isdigit() else NUMBER_WORDS[word]
        if rows and said != len(rows):
            problems.append(f"line {n + 1}: text says {m.group(0)!r} but the diagram below has {len(rows)} rows")
    return problems


def check_list_breaks(lines: list[str]) -> list[str]:
    """A diagram between an entry line and its sub-bullets cuts the list in two."""
    problems, n = [], 0
    while n < len(lines):
        if lines[n].startswith("```"):
            before = next((lines[k] for k in range(n - 1, -1, -1) if lines[k].strip()), "")
            end = next((k for k in range(n + 1, len(lines)) if lines[k].startswith("```")), len(lines) - 1)
            after = next((lines[k] for k in range(end + 1, len(lines)) if lines[k].strip()), "")
            if re.match(r"- ", before) and re.match(r"\s+- ", after):
                problems.append(f"line {n + 1}: diagram sits between an entry and its sub-bullets; move it before the entry")
            n = end
        n += 1
    return problems


def process(path: Path, fix: bool = True) -> list[str]:
    original = path.read_text().split("\n")
    fixed = normalize(original)
    if fix and fixed != original:
        path.write_text("\n".join(fixed))
    return check_links(path, fixed) + check_diagrams(fixed) + check_structure(path, fixed) + check_counts(fixed) + check_list_breaks(fixed)


def save_snapshot(path: Path) -> None:
    """The mirror was written: confirm the source copy beautyfact_relink.py set aside for it.

    Without a pending copy nothing changes, so a hand check of a stale mirror cannot
    make it look current.
    """
    if not path.name.endswith(SUFFIX):
        return
    snapshot = path.parent / SNAPSHOT_DIR / (path.name[: -len(SUFFIX)] + ".md")
    pending = snapshot.with_name(snapshot.name + ".pending")
    if pending.is_file():
        pending.replace(snapshot)


def main() -> None:
    args = [a for a in sys.argv[1:] if a != "--no-fix"]
    if args:
        problems = process(Path(args[0]), fix="--no-fix" not in sys.argv)
        save_snapshot(Path(args[0]))
        print("\n".join(problems) or "ok")
        return
    payload = json.load(sys.stdin)
    target = Path((payload.get("tool_input") or {}).get("file_path") or "")
    if not target.name.endswith(SUFFIX) or not target.is_file():
        return
    problems = process(target)
    save_snapshot(target)
    if problems:
        message = f"beautyfact_check found problems in {target.name}; fix them:\n" + "\n".join(problems[:20])
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": message}}))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
