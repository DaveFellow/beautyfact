# Diagram rules: Mermaid

Loaded from `SKILL.md` when its diagram style is Mermaid. Examples: `references/examples-mermaid/`.

Three tools, picked by the shape of the content. Never align anything by hand: Mermaid lays out graphs, and Markdown lays out tables.

| Content | Use |
| --- | --- |
| General idea, components | `flowchart LR`, one node per component |
| Layers, who calls whom | `flowchart TD` with one `subgraph` per layer and labeled edges ("calls") |
| Entities and relations | `flowchart LR` with edges labeled `"1"`, `"many"` |
| Steps with decisions | `flowchart TD` with `{"question?"}` nodes and `"yes"` / `"no"` edges |
| Lifecycle of an object | `stateDiagram-v2` |
| States changing step by step | Table: one row per step, one column per state, `[>]` current, `[x]` done, `[ ]` pending |
| Client ◀──▶ server, concurrent actors | `sequenceDiagram` with 2–4 participants |
| Inside / outside, goals / non-goals | Table with two columns |
| Effort, proportion, counts | Table with a `▓` bar column and the item IDs |
| Items ──▶ what covers them, risk ──▶ mitigation | Table with two columns |
| Merging inputs into a pipeline | `flowchart TD`: inputs on top, joined into one chain |
| Files and folders | `text` tree (`├──`, `└──`) with the purpose of each entry: no alignment needed |
| Phases and gates | `flowchart LR` with `{"gate"}` nodes |
| Screens | `flowchart LR` navigation map, plus a `text` box mockup (the one place boxes stay) |

## Mermaid syntax (the checker enforces the starred rules)

Mermaid fails hard: one syntax error and the reader sees an error instead of the diagram. Keep to this subset.

- Code block with language `mermaid`. First line: `flowchart TD`, `flowchart LR`, `sequenceDiagram`, or `stateDiagram-v2`. ★ No other type.
- ★ Every node label in double quotes: `core["src/core (pure)"]`, `trust{"trusted?"}`, `start(["Run sync"])`. A label never contains `"`; write `#quot;` instead.
- ★ Every edge label in double quotes: `trust -->|"no"| skip`.
- Node IDs: short lowercase words or letters and digits (`cli`, `s1`). ★ Never `end`. Not `graph`, `subgraph`, `style`, `class`, or `click` either.
- One space on each side of an arrow: `a --> b`, `a -.-> b`.
- Line breaks inside a label: `<br/>`.
- ★ `sequenceDiagram` and `stateDiagram-v2`: no `;` in message or transition text (write `,` or `·`). Name actors once: `participant a as hook A`. Replies use `-->>`.
- ★ No emojis inside a diagram. « » and `──▶` belong to prose, not to Mermaid: use its own arrows.
- No `style`, `classDef`, `%%{init}` or colors: themes differ per editor and dark mode.
- ~15 nodes or messages at most. ★ A block over 25 lines is too big: split it in two.
- `flowchart LR` for chains of up to ~5 nodes, `TD` for anything longer or with decisions.

## Tables

- A plain Markdown table: header row, `| --- |` separator, one row per item. No code block.
- No alignment by hand: cells are not padded.
- IDs, `▓` bars and `[x]` marks go in their own column.
- Notation inside cells is the same as in bullets: «**names**», backticks, 💬 for UI text.

## Text blocks that stay

- UI box mockups (`┌ ┐ └ ┘`), folder trees, and the WHEN/THEN format blocks stay in `text` code blocks with the ASCII rules: at most 74 characters wide, box edges in the same column.
