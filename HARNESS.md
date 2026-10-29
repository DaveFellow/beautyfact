# Harness paths

Given only the repo URL, clone it to a temporary folder outside the project, install from there, and delete the clone when done. Do not leave the kit inside the project.

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

Before installing, ask the user: automatic (each document to review gets a mirror when it is written) or manual (only when they call the beautyfact skill). For manual, do not register `beautyfact_companion.py`; register the other two hooks either way. With `install.py`, pass `--auto` or `--manual` with the answer.

Also copy `hooks/beautyfact_relink.py` beside the hooks. The subagent runs it; it is not registered as a hook. Add `.beautyfact/` to the project's `.gitignore`: the checker keeps a copy of each source there so the next mirror update can shift its links.

## Model

The subagent ships with `model: inherit`. Keep it in the kit, and when installing:

1. Suggest a model for the harness. Claude Code: `inherit`, or `sonnet` for speed. Cursor and others: the model the user trusts most for long structured writing. With a reasoning model (Grok, GPT), a lower reasoning effort for the subagent, if the harness has that setting. Haiku and other small models only after checking their mirrors by hand, because the checker does not catch missing content.
2. Remind the user to set the model in the installed agent file, and to check one mirror by hand after any change of model.
