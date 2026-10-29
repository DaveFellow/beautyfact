"""CLI: shift the source links of a `_beautyfact.md` mirror after its source changed.

Run it before every mirror write, new or update. It sets the current source aside in
`.beautyfact/` beside the mirror, and beautyfact_check.py keeps that copy once the mirror
is written. On the next run, this script compares that copy with the current source, rewrites every link line number in the mirror to the new numbering, and prints
which source lines changed and which mirror sections link to them, so only those sections
need editing. Mechanical work only: it never touches the mirror's prose or diagrams.

Usage: python3 beautyfact_relink.py <file_beautyfact.md>
The first output line is the verdict:
  no snapshot  write the mirror from scratch (no mirror yet, or no saved copy of the source)
  unchanged    the source is the same as when the mirror last passed
  rewrite      too much of the source changed; write the mirror from scratch
  edit         links were shifted; edit only the sections listed
"""

import difflib
import re
import sys
from pathlib import Path

SUFFIX = "_beautyfact.md"
SNAPSHOT_DIR = ".beautyfact"
# Above this share of changed source lines, a fresh mirror is clearer than many edits.
REWRITE_RATIO = 0.5
LINK = re.compile(r"\[([^\]]*)\]\(([^)#\s]+\.md)#L(\d+)(?:-L(\d+))?\)")
TEXT_RANGE = re.compile(r"L(\d+)(?:([–-])L(\d+))?")


def source_of(mirror: Path) -> Path:
    return mirror.with_name(mirror.name[: -len(SUFFIX)] + ".md")


def snapshot_of(mirror: Path) -> Path:
    return mirror.parent / SNAPSHOT_DIR / source_of(mirror).name


def line_map(opcodes, old_len: int, new_len: int):
    """Return f(n, end) mapping an old 1-based line to the new numbering."""

    def mapped(n: int, end: bool) -> int:
        for tag, i1, i2, j1, j2 in opcodes:
            if i1 <= n - 1 < i2:
                if tag == "equal":
                    return j1 + (n - 1 - i1) + 1
                # A replaced or deleted line points at the block that took its place.
                return max(j2, j1 + 1) if end and j2 > j1 else j1 + 1
        return new_len if n > old_len else n

    return lambda n, end=False: max(1, min(mapped(n, end), max(new_len, 1)))


def changed_regions(opcodes) -> list[tuple[int, int, str]]:
    regions = []
    for tag, i1, i2, j1, j2 in opcodes:
        if tag == "equal":
            continue
        if j2 > j1:
            span = f"L{j1 + 1}" if j2 == j1 + 1 else f"L{j1 + 1}–L{j2}"
            regions.append((j1 + 1, j2, f"{span} {'added' if tag == 'insert' else 'changed'}"))
        else:
            regions.append((j1, j1 + 1, f"lines removed between L{j1} and L{j1 + 1}"))
    return regions


def set_aside(source: Path, snapshot: Path) -> None:
    """Keep the source the mirror is about to follow; beautyfact_check.py confirms it once the mirror is written."""
    snapshot.parent.mkdir(exist_ok=True)
    snapshot.with_name(snapshot.name + ".pending").write_text(source.read_text())


def relink(mirror: Path) -> list[str]:
    source, snapshot = source_of(mirror), snapshot_of(mirror)
    if not source.is_file():
        return [f"no source: {source} does not exist"]
    if not mirror.is_file() or not snapshot.is_file():
        set_aside(source, snapshot)
        return ["no snapshot"]
    old, new = snapshot.read_text().split("\n"), source.read_text().split("\n")
    if old == new:
        return ["unchanged"]
    set_aside(source, snapshot)
    opcodes = difflib.SequenceMatcher(None, old, new, autojunk=False).get_opcodes()
    changed = sum(max(i2 - i1, j2 - j1) for tag, i1, i2, j1, j2 in opcodes if tag != "equal")
    if changed / max(len(old), len(new)) > REWRITE_RATIO:
        return ["rewrite", f"{changed} of {len(new)} source lines changed"]

    to_new = line_map(opcodes, len(old), len(new))
    regions = changed_regions(opcodes)
    covered, affected, shifted = set(), [], 0
    lines, fence, heading = mirror.read_text().split("\n"), False, None

    def shift(match: re.Match) -> str:
        nonlocal shifted
        text, target, start, end = match.groups()
        if (mirror.parent / target).resolve() != source.resolve():
            return match.group(0)
        s = to_new(int(start))
        e = to_new(int(end), end=True) if end else None
        m = TEXT_RANGE.search(text)
        if m:
            ts = to_new(int(m.group(1)))
            te = max(ts, to_new(int(m.group(3)), end=True)) if m.group(3) else None
            label = f"L{ts}" if te is None or te == ts else f"L{ts}{m.group(2)}L{te}"
            text = text[: m.start()] + label + text[m.end():]
        href = f"#L{s}" + (f"-L{max(s, e)}" if e else "")
        result = f"[{text}]({target}{href})"
        shifted += result != match.group(0)
        span = (ts, te or ts) if m else (s, e or s)
        for index, (a, b, _) in enumerate(regions):
            if span[0] <= b and a <= span[1]:
                covered.add(index)
                if heading and heading not in affected:
                    affected.append(heading)
        return result

    for number, line in enumerate(lines):
        if line.lstrip().startswith("```"):
            fence = not fence
        if fence:
            continue
        if line.startswith("#"):
            heading = f"{line} (mirror line {number + 1})"
        lines[number] = LINK.sub(shift, line)
    mirror.write_text("\n".join(lines))

    report = ["edit", f"links shifted: {shifted}", "changed source lines:"]
    report += [f"  {label}" for _, _, label in regions]
    report += ["sections to update:"] + [f"  {h}" for h in affected]
    loose = [label for index, (_, _, label) in enumerate(regions) if index not in covered]
    if loose:
        report += ["changes no mirror link covers (find the section they belong to):"]
        report += [f"  {label}" for label in loose]
    return report


def main() -> None:
    if len(sys.argv) != 2 or not sys.argv[1].endswith(SUFFIX):
        sys.exit("Usage: python3 beautyfact_relink.py <file_beautyfact.md>")
    print("\n".join(relink(Path(sys.argv[1]))))


if __name__ == "__main__":
    main()
