# 💅 beautyfact

> A skill, a subagent, and 3 hooks that mirror each spec `.md` you review
> into a diagram-first version. The process always runs in the beautyfact
> subagent. Original untouched.
>
> ***DISCLAIMER:** This kit was mostly tested using Sonnet 5.5 in Claude Code and optimized for Anthropic models, it works pretty well there so use it for this task. While it works in other agents, Grok 4.7 High in Cursor looked to be inneficient running it, but maybe my test setup was way too biased and as this is a personal tool I didn't care too much about it so you can do your tests and report your findings.*

**Legend:** 📌 rule · ⚠️ edge case · 🔗 source line

## 1. 🎯 What it's for

Specs are correct and unreadable. This kit fixes the latter.

Every time a document you should review lands (an OpenSpec change, a Spec Kit feature artifact, an acceptance checklist), beautyfact writes a sibling `<name>_beautyfact.md`: same content, zero loss, redrawn with ASCII diagrams and icons so a human skims it in seconds.

```text
 specs/foo.md          ──▶  specs/foo_beautyfact.md
 (source, untouched)        (mirror, diagram-first)
```

- 📌 The mirror never replaces the source — a read-time hook enforces that.
- 📌 The parent agent never writes the mirror. It delegates to the `beautyfact` subagent, which reads `SKILL.md` and redraws the file.

## 2. 👀 Example

The same two requirements, before and after. Nothing is added or cut: the relation requirement ──▶ behavior is drawn, so it reads at a glance.

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

- RF-01 📌 🔗 [L11](foo.md#L11): User can create a task offline.
- RF-02 📌 🔗 [L12](foo.md#L12): Offline tasks sync when connection
  returns.
```

## 3. ⚙️ Install

Two ways in. Both ask you «**automatic**» or «**manual**» first.

```text
                     ┌─ any harness ───────▶ A. give your agent the URL
 install beautyfact ─┤
                     └─ Claude Code/Cursor ▶ B. run install.py yourself

 automatic ──▶ each document to review gets its mirror when written
 manual    ──▶ only when you call /beautyfact path/to/file.md
```

### 🤖 A. Give your agent the URL

Paste this to your agent, in your project:

```text
Install https://github.com/DaveFellow/beautyfact in this project
and adapt the hooks to my harness.
```

- 📌 The agent clones the kit outside your project, follows `HARNESS.md` for your harness's paths, and deletes the clone when done.
- 📌 On Claude Code or Cursor it runs `install.py` with `--auto` or `--manual`, after asking you which.
- 📌 It copies `skills/beautyfact/`, `agents/beautyfact.md`, `rules/beautyfact-subagent.mdc`, and `hooks/beautyfact_*.py`, then registers the hooks.

### 💻 B. Run the script (Claude Code and Cursor)

```bash
git clone https://github.com/DaveFellow/beautyfact /tmp/beautyfact
python3 /tmp/beautyfact/install.py /path/to/your/project  # asks a/m
```

- 📌 `--auto` or `--manual` answers the question up front.
- 📌 Re-run to update or to switch mode: hooks never duplicate, and `settings.json` is backed up first.
- ⚠️ Other harnesses: use option A. The script only knows the Claude Code and Cursor paths.

## 4. 📁 What goes where

```text
 beautyfact kit
 ├─ skills/beautyfact/             format rules + examples
 ├─ agents/beautyfact.md           the only agent that runs the process
 ├─ rules/beautyfact-subagent.mdc  parent always delegates to that agent
 └─ hooks/
    ├─ beautyfact_companion.py     on Write of a doc to review: asks
    │                              for the mirror (automatic mode only)
    ├─ beautyfact_check.py         on mirror write/edit: fixes and
    │                              flags notation
    ├─ beautyfact_read_guard.py    on Read: source stays mandatory
    └─ beautyfact_relink.py        run by the subagent: shifts mirror
                                   links after the source changes
```

- 📌 Claude Code: each folder goes under `.claude/` (`skills/`, `agents/`, `rules/`, `hooks/`). The rule lands as `.claude/rules/beautyfact-subagent.md`, without its Cursor frontmatter.
- 📌 Cursor: the agent goes to `.cursor/agents/` and the rule to `.cursor/rules/`.
- 📌 Any other harness: paths are in `HARNESS.md`.
- ⚠️ `beautyfact_relink.py` sits beside the hooks but is not registered as one.

## 5. 🔄 How the mirror gets built

```text
 Write review doc ──▶ companion hook ──▶ parent delegates to the subagent
 (manual: /beautyfact file.md ────────▶ parent delegates to the subagent)
                                        │
                                        ▼
        subagent runs relink, studies SKILL.md examples (parent does not)
                                        │
                                        ▼
            section ──▶ source link + diagram + bullets (no repeats)
                                        │
                                        ▼
        _beautyfact.md written ──▶ check hook fixes/flags notation
                                        │
                                        ▼
            read_guard: mirror read ──▶ still must read source
```

- 📌 Specs, plans, task lists, and test lists written in this format go to the same subagent.
- 📌 Nothing is summarized away: every ID, requirement, and decision survives.
- 📌 One diagram per structured section, then 2–5 bullets adding only what the diagram can't show.

## 6. 🔧 Settings

### 📄 Which documents get a mirror

Only the ones you review. Everything else needs a `/beautyfact` call.

```text
 gets a mirror                       never
 ─────────────                       ─────
 openspec/changes/<change>/          openspec/changes/archive/
   proposal, design, tasks,          openspec/specs/
   specs/*/spec                      openspec/AGENTS.md, project.md
 specs/<feature>/                    .specify/templates/
   spec, plan, research, tasks,      READMEs, notes, any other .md
   data-model, quickstart,
   contracts/, checklists/
 .specify/memory/constitution.md
 any .md in an acceptance/ folder
```

- 📌 The lists live in `beautyfact_companion.py`: `WATCHED_ROOTS`, `REVIEW_NAMES`, `REVIEW_DIRS`, `WATCHED_ANYWHERE`, and `SKIP_DIRS`.
- ⚠️ `openspec/specs/` is rewritten when a change is archived, so nobody reviews it there.

### ⚙️ Other settings

- ⚠️ **Per project only.** The hooks find the project root from their own location, so they do not work from `~/.claude`.
- 📌 **Check by hand:** `python3 .claude/hooks/beautyfact_check.py path/to/file_beautyfact.md`.
- 📌 **Updates are edits.** Each mirror write keeps a copy of its source in `.beautyfact/` (the installer adds it to `.gitignore`). On the next change, `beautyfact_relink.py` shifts the links and the subagent edits only the changed sections.
- 📌 **Model:** the subagent uses `model: inherit`. Set another in the installed agent file; `HARNESS.md` has suggestions.
- ⚠️ **Needs** Python 3.9 or newer.
