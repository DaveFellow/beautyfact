# Diagram rules: ASCII

Loaded from `SKILL.md` when its diagram style is ASCII. Examples: `references/examples/`.

Two tools, picked by the shape of the content: hand-drawn text diagrams for anything that is a drawing (flows, layers, sequences, trees, mockups), and plain Markdown tables for anything that is only columns. Never draw a table by hand.

## Text diagrams

- Always inside a code block with language `text` (monospace).
- **No emojis inside diagrams with aligned columns** (their width varies). Emojis go in headings and bullets.
- Align by counting characters: define columns by index and pad with spaces; verify that the verticals `│`, arrows `▼ ▲ ▶ ◀` and corners `┌ ┐ └ ┘` land in the same column.
- Allowed characters: `─ │ ┌ ┐ └ ┘ ├ ┤ ┬ ┴ ┼ ▶ ◀ ▲ ▼ ◆ ▓`.
- At most 74 characters wide (the hook checks it) and ~15 lines per diagram. If it does not fit, split it in two.
- Pick a text diagram or a table by the shape of the content:

| Content | Use |
| --- | --- |
| General idea, components | Tree mind map |
| Layers, who calls whom | Stacked boxes joined by `▼ ▲` and a short label ("calls") |
| Entities and relations | Tree with `<` for «many» |
| Steps with decisions | Flowchart with `?` and yes/no branches, drawn vertically |
| Lifecycle of an object | One line of states joined by `──▶` and `◀──▶` |
| States changing step by step | Table: one row per step, one column per state, `[>]` current, `[x]` done, `[ ]` pending |
| Client ◀──▶ server, concurrent actors | Sequence with 2–4 verticals; `┼` where an arrow crosses a vertical |
| Inside / outside, goals / non-goals | Table with two columns |
| Effort, proportion, counts | Table with a `▓` bar column and the item IDs |
| Items ──▶ what covers them, risk ──▶ mitigation | Table with two columns |
| Merging inputs into a pipeline | Branches joined with `┐ ├ ┘`, then a vertical `▼` chain |
| Files and folders | Tree with the purpose of each entry |
| Phases and gates | Line with `──▶` and `◆` for gates |
| Screens | Navigation map and box mockup |

## Tables

- A plain Markdown table: header row, `| --- |` separator, one row per item. No code block.
- No alignment by hand: cells are not padded.
- IDs, `▓` bars and `[x]` marks go in their own column.
- Notation inside cells is the same as in bullets: «**names**», backticks, 💬 for UI text.
