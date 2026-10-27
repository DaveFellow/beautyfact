"""PostToolUse hook: the source is mandatory, the beautyfact mirror never replaces it.

Runs after Read. A `_beautyfact.md` file repeats its source file's content in a
different, usually longer format (diagrams added, nothing cut) meant for human
reading, so it has no advantage for an agent. This is a safety net for when an agent
reads the mirror without reading the source: through additionalContext, it tells the
agent it still has to read the source before relying on this content. Reading the
source first needs no such correction — then the mirror is simply redundant. It never
blocks: any problem (unexpected input) is ignored silently.
"""

import json
import sys
from pathlib import Path

SUFFIX = "_beautyfact"


def main() -> None:
    payload = json.load(sys.stdin)
    target = (payload.get("tool_input") or {}).get("file_path") or ""
    if not target:
        return
    path = Path(target)
    if path.suffix.lower() != ".md":
        return

    if path.stem.endswith(SUFFIX):
        source = path.with_name(path.stem[: -len(SUFFIX)] + path.suffix)
        if not source.is_file():
            return
        message = (
            f"{path.name} is the beautyfact (human-readable) mirror of {source.name}, made for human "
            f"reading and with no advantage for you. It does not replace {source.name}: you still "
            f"have to read {source.name}, the actual source, before relying on this content."
        )
    else:
        companion = path.with_name(path.stem + SUFFIX + path.suffix)
        if not companion.is_file():
            return
        message = (
            f"{path.name} has a beautyfact mirror at {companion.name}, kept for human reading only "
            f"(it has no advantage for you). You already have the content from {path.name}; you do "
            f"not need to also read {companion.name}."
        )
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": message}}))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
