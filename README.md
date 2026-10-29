# 💅 beautyfact

> A skill, a subagent, and 3 hooks that mirror any spec `.md` into a
> diagram-first version. The process always runs in the beautyfact
> subagent. Original untouched.

**Legend:** 🎯 purpose · ⚙️ setup · 📌 rule · 🔗 file ref

## 1. 🎯 What it's for

Specs are correct and unreadable. This kit fixes the later.

Every time an artifact `.md` lands in a watched folder, beautyfact writes a sibling `<name>_beautyfact.md`: same content, zero loss, redrawn with ASCII diagrams and icons so a human skims it in seconds.

```text
 specs/foo.md  ──▶  specs/foo_beautyfact.md
 (source, untouched)    (mirror, diagram-first)
```

- 📌 The mirror never replaces the source — a read-time hook enforces that.
- 📌 The parent agent never writes the mirror. It delegates to the
`beautyfact` subagent, which reads `SKILL.md` and redraws the file.

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

The kit does not live under a harness folder. Sources are `agents/beautyfact.md`, `rules/beautyfact-subagent.mdc`, `skills/beautyfact/`, and `hooks/`. Copy each into the directories for the harness you are installing.

**Clone this repo in your project's folder and ask your agent:** «Install this kit and adapt the hooks to my harness.»

That agent uses the map in the next section. Keep the rule text, and switch on whatever frontmatter that harness needs so the rule is always on (Cursor `alwaysApply`, Copilot `applyTo: "**"`, Windsurf `always_on`, Continue `alwaysApply`). The hook scripts speak Claude Code's protocol; register the same three behaviors in the harness's own hook file.

**Claude Code and Cursor, direct:**

```bash
python3 install.py /path/to/your/project
```

That script installs the Claude Code skill, agent, and hooks, and copies the agent and rule for Cursor. Re-run to update — hooks never duplicate; `settings.json` is backed up. Every other harness is installed from the map.

## 4. 📁 What goes where

| Kit file | Role |
|---|---|
| `skills/beautyfact/` | Format rules + examples |
| `agents/beautyfact.md` | The only agent that runs the process |
| `rules/beautyfact-subagent.mdc` | Parent always delegates to that agent |
| `hooks/beautyfact_companion.py` | On write: tells the parent to delegate the mirror |
| `hooks/beautyfact_check.py` | On mirror write/edit: fixes and flags notation |
| `hooks/beautyfact_read_guard.py` | On read: the source stays mandatory |

A root `AGENTS.md` is read by Cursor, Copilot, Codex, Windsurf, Cline, Roo Code, OpenCode, Amp, Goose, Zed, Junie, and Kilo Code. Put the delegation rule there when you want one shared copy. Still add the native file below when that harness does not treat `AGENTS.md` as its only rules file.

| Harness | Rule | Subagent | Skill | Hooks |
|---|---|---|---|---|
| Cursor | `.cursor/rules/*.mdc` | `.cursor/agents/` | `.cursor/skills/` | `.cursor/hooks.json` |
| Claude Code | `.claude/rules/*.md` | `.claude/agents/` | `.claude/skills/` | `.claude/settings.json` |
| GitHub Copilot | `.github/instructions/*.instructions.md` | `.github/agents/*.agent.md` | `.agents/skills/` | `.github/hooks/*.json` |
| Codex | `AGENTS.md` | `.codex/agents/` | `.agents/skills/` | `.codex/hooks.json` |
| Windsurf | `.windsurf/rules/*.md` | — | — | — |
| Cline | `.clinerules/` | — | — | — |
| Roo Code | `.roo/rules/` | — | — | — |
| Continue | `.continue/rules/*.md` | — | — | — |
| Gemini CLI | `GEMINI.md` | — | `.agents/skills/` | — |
| OpenCode | `AGENTS.md` | `.opencode/agents/` | `.opencode/skills/` | — |
| Amp | `AGENTS.md` | — | `.agents/skills/` | — |
| Kilo Code | `.kilo/rules/*.md` | — | — | — |
| Junie | `.junie/AGENTS.md` | — | — | — |
| Kiro | `.kiro/steering/*.md` | — | — | — |
| Amazon Q | `.amazonq/rules/*.md` | — | — | — |
| Goose, Zed | `AGENTS.md` | — | — | — |
| Aider | `CONVENTIONS.md` (load it with `--read` or `read:` in `.aider.conf.yml`) | — | — | — |

Claude Code also reads `CLAUDE.md`. Copilot also reads `.github/copilot-instructions.md`. Cline also reads `.cline/rules/`. Aider has no always-on rules file, so the conventions file has to be loaded on purpose. Where the subagent column is empty, the rule file carries the same delegation text.

## 5. 🔄 How the mirror gets built

```text
 Write .md ──▶ companion hook ──▶ parent delegates to the beautyfact subagent
                                        │
                                        ▼
                  subagent studies SKILL.md examples (parent does not)
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

- 📌 The parent never writes the mirror. Specs, plans, task lists, and test lists in this format go to the same subagent.

- 📌 Nothing is summarized away — every ID/requirement/decision survives.
- 📌 One diagram per structured section, 2–5 bullets adding only what
the diagram can't show.

## 6. 🔧 Settings

- **Watched folders:** `WATCHED_ROOTS` (`openspec`, `.specify`, `specs`) and `WATCHED_ANYWHERE` (`acceptance`) in `beautyfact_companion.py`.
- **Per project only.** The hooks find the project root from their own location, so they do not work from a home-directory config.
- **Check by hand:** `python3 .claude/hooks/beautyfact_check.py path/to/file_beautyfact.md` (or the same script from the harness hooks directory).
- **Needs** Python 3.9 or newer.
