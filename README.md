# 💅 beautyfact

> A Claude Code skill + 3 hooks that mirror any spec `.md` into a
> diagram-first version. Original untouched. Built for Claude, usable
> by any agent that can read a skill file and hook on writes.

**Legend:** 🎯 purpose · ⚙️ setup · 📌 rule · 🔗 file ref

## 1. 🎯 What it's for

Specs are correct and unreadable. This kit fixes the later.

Every time an artifact `.md` lands in a watched folder, beautyfact writes a sibling `<name>_beautyfact.md`: same content, zero loss, redrawn with ASCII diagrams and icons so a human skims it in seconds.

```text
 specs/foo.md  ──▶  specs/foo_beautyfact.md
 (source, untouched)    (mirror, diagram-first)
```

- 📌 The mirror never replaces the source — a read-time hook enforces that.
- 📌 Claude Code-shaped install, but the logic is just "read `SKILL.md`,
redraw the file" — any agent can wire its own trigger.

## 2. 👀 Example

```text
                              specs/foo.md (source)
## 3. Requirements
- RF-01: User can create a task offline.
- RF-02: Offline tasks sync when connection returns.
```

```text
                      specs/foo_beautyfact.md (mirror)
## 3. 📋 Requirements
🔗 Source: [foo.md L10–L13](foo.md#L10)

 RF-01  Create task offline   ──▶ allowed
 RF-02  Offline sync          ──▶ on reconnect

- 📌 RF-01 🔗 [L11](foo.md#L11)
- 📌 RF-02 🔗 [L12](foo.md#L12)
```

Same two requirements, nothing added or cut — just drawn so the relation
(requirement ──▶ behavior) is visible at a glance instead of read twice.

## 3. ⚙️ Install

**Clone this repo in your project's folder and ask your agent:** «Install this kit and adapt the hooks to my harness.»

**Claude Code, direct:**

```bash
python3 install.py /path/to/your/project
```

Re-run to update — hooks never duplicate; `settings.json` is backed up.

## 4. 📁 What goes where

| Kit file | Installed to | Role |
|---|---|---|
| `skills/beautyfact/` | `.claude/skills/beautyfact/` | Format rules + examples |
| `beautyfact_companion.py` | `.claude/hooks/` | On `Write`: asks for the mirror |
| `beautyfact_check.py` | `.claude/hooks/` | On mirror write/edit: fixes & flags notation |
| `beautyfact_read_guard.py` | `.claude/hooks/` | On `Read`: source stays mandatory |

## 5. 🔄 How the mirror gets built

```text
 Write .md ──▶ companion hook ──▶ agent studies SKILL.md examples
                                        │
                                        ▼
            section ──▶ 🔗 source link + diagram + bullets (no repeats)
                                        │
                                        ▼
        _beautyfact.md written ──▶ check hook fixes/flags notation
                                        │
                                        ▼
            read_guard: mirror read ──▶ still must read source
```

- 📌 Nothing is summarized away — every ID/requirement/decision survives.
- 📌 One diagram per structured section, 2–5 bullets adding only what
the diagram can't show.

## 6. 🔧 Settings

- **Watched folders:** `WATCHED_ROOTS` (`openspec`, `.specify`, `specs`) and `WATCHED_ANYWHERE` (`acceptance`) in `beautyfact_companion.py`.
- **Per project only.** The hooks find the project root from their own location, so they do not work from `~/.claude`.
- **Check by hand:** `python3 .claude/hooks/beautyfact_check.py path/to/file_beautyfact.md`.
- **Needs** Python 3.9 or newer.
