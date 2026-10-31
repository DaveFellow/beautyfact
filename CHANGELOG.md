# Changelog

## Unreleased (`v0.21`)

### Added

- Mermaid diagram style, the new default. Graphs (flows, layers, sequences, lifecycles, pipelines) are Mermaid blocks; columns, rows, bars, and step tables are Markdown tables. Nothing is aligned by hand, so mirrors cost fewer tokens. UI mockups and folder trees stay as text.
- `install.py` asks the diagram style after the mode (`--mermaid` / `--ascii` up front; without a terminal it stays Mermaid), writes the choice into the installed `SKILL.md`, and points VS Code and Cursor users to a Mermaid preview extension. `HARNESS.md` gives other harnesses the same question.
- Both styles draw tabular content (goals / non-goals, risk ──▶ mitigation, `▓` counts, step tables, case ──▶ response) as Markdown tables instead of hand-aligned text columns. ASCII diagrams are kept for flows, layers, sequences, trees, and mockups.
- `references/diagrams-mermaid.md` (rules and a safe syntax subset) and `references/examples-mermaid/` (every pattern redrawn). The ASCII rules moved to `references/diagrams-ascii.md`.
- The checker lints Mermaid blocks: allowed types, quoted node and edge labels, no `end` node, no `;` in messages, no emojis, balanced subgraphs, at most 25 lines. Width and box checks apply to `text` blocks only. Tables count as a section's diagram and in the row-count check.


Changes on branch `v0.2` compared with branch `v0.1` (`b80d758`, 2026-10-27).

`v0.2` is `7c84986` (2026-10-29). Five commits, 12 files, 552 insertions, 96 deletions.

## Added

- The beautyfact process runs only in the `beautyfact` subagent (`agents/beautyfact.md`). It reads the skill and the source itself, writes the requested artifact or `<name>_beautyfact.md` mirror, runs the relink and check scripts, and reports the path it wrote. The parent passes paths, not the file body.
- An always-on rule (`rules/beautyfact-subagent.mdc`) tells every other agent to delegate that work once, in the foreground, and not to read the examples or write the mirror. A mirror is only for a document the user reviews, or one the user names.
- `HARNESS.md` lists where the rule, subagent, skill, and hooks go for Cursor, Claude Code, GitHub Copilot, Codex, and other harnesses. `install.py` covers Claude Code and Cursor. Every other row is for the installing agent.
- `hooks/beautyfact_relink.py`, run by the subagent and not registered as a hook. Before a mirror is written it records the source, shifts existing source links to the new line numbers, and prints a verdict: `rewrite`, `unchanged`, or `edit` (with the sections to update).
- Source copies in `.beautyfact/` beside each mirror, so the next update compares against the version that mirror follows. The installer adds `.beautyfact/` to `.gitignore`.
- Install modes. `--auto` mirrors each review document when it is written. `--manual` mirrors only when the user calls `/beautyfact`. Without a terminal, one of the two flags is required.

## Changed

- Mirrors are limited to documents a person reviews. Inside `openspec/changes/` and Spec Kit trees that is `proposal`, `design`, `tasks`, `spec`, `plan`, `research`, `data-model`, `quickstart`, `constitution`, plus `contracts/` and `checklists/`, and any Markdown file in an `acceptance/` folder. Archives, templates, `openspec/specs/`, agent instructions, and READMEs are skipped.
- The companion hook no longer asks the parent to write the mirror. It tells the parent to delegate to the beautyfact subagent. If the mirror already exists, the ask is to update it. Manual installs omit this hook and drop it on a later `--manual` run.
- `install.py` copies the skill, the three hooks, `beautyfact_relink.py`, the subagent (`.cursor/agents/` and `.claude/agents/`), and the rule (`.cursor/rules/`, and `.claude/rules/` without Cursor frontmatter). Hooks are registered in Claude Code `settings.json`. Re-runs do not duplicate hooks, and the previous settings file is backed up. It ends with a reminder to set the subagent model (`model: inherit` in the kit).
- The checker requires a type emoji on every top-level bullet before the first link. A link mark does not count as a type. After a clean check it confirms the source snapshot `beautyfact_relink.py` set aside, so a hand check of a stale mirror cannot make it look current.
- The skill tells the subagent to run relink before every mirror, to keep the section-to-pattern list as a private plan, and to place each entry’s type emoji beside its ID and before the link. Wrapping quoted names in bold stays with the checker. The subagent’s report is one line: the path written, or the error that stopped the write.
- The read guard still requires the source. It now says only the beautyfact subagent updating a mirror needs to read the mirror.
- Example entries and UI mockups show the type emoji before the source link.

## Commits

| Commit | Date | Summary |
|---|---|---|
| `f60db7f` | 2026-10-28 | Run the beautyfact process in its own subagent |
| `c69018f` | 2026-10-28 | Add the beautyfact subagent and the delegation rule |
| `32dfc64` | 2026-10-28 | Add `agents/` and `rules/` |
| `ea7ea57` | 2026-10-28 | Add `HARNESS.md` and point install docs at it |
| `7c84986` | 2026-10-29 | Automatic or manual install, relink, and review-only mirrors |
