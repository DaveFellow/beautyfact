# Harness paths

The kit sources stay in `agents/`, `rules/`, `skills/beautyfact/`, and `hooks/`. Copy them into the directories below for the harness you are installing.

Keep the rule text, and switch on whatever frontmatter that harness needs so the rule is always on (Cursor `alwaysApply`, Copilot `applyTo: "**"`, Windsurf `always_on`, Continue `alwaysApply`). The hook scripts speak Claude Code's protocol; register the same three behaviors in the harness's own hook file.

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

`install.py` installs Claude Code and Cursor only. Every other row is for the installing agent.
