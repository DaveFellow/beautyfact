# Pattern: goals / non-goals or in / out as a two-column table

Excerpt from a real `_beautyfact` file. Copy the shape, not the content.

## 1. 🎯 Context and goals

🔗 Source: [Context L13–L18](design.md#L13) · [Goals / Non-Goals L20–L30](design.md#L20)

| Goals | Non-goals |
| --- | --- |
| Rules in `src/core`, no VS Code or disk | No second store or network |
| Parallel CLI calls lose no update | No bundler |
| No config command without consent | No task breakdown (`tasks.md`) |

- 📌 Every business rule lives in `src/core`, testable without VS Code or the disk.
- 📌 Two parallel CLI calls never lose an update. A command from a config file never runs without trust and consent.
- 📌 No second state store, database, or network use. The CLI and core ship as plain compiled files (no bundler).
- 📌 No task breakdown: that is `tasks.md`.
- 📌 Motivation and scope: [proposal.md](proposal.md). Behavior: the seven specs in `specs/`.
- 📌 Inherited and already approved: stack, layers, allowed dependencies, security baseline in `.claude/rules/architecture.md` and `.claude/rules/security.md`.
- 📌 Product and UI rules in `.claude/rules/product.md` and `.claude/rules/ui.md` also apply.
- 📌 There is no existing code. The project starts empty.
