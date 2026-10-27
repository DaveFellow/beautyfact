# Pattern: architecture as stacked boxes that call each other

Excerpt from a real `_beautyfact` file. Copy the shape, not the content.

## 2. 🏗️ Architecture

🔗 Source: [D9 L36–L39](design.md#L36) · [D18 L95–L98](design.md#L95) · [D20 L106–L109](design.md#L106)

```text
 ┌────────────────────────────────────────────────────────────┐
 │ src/extension  (VS Code)         src/webview (page script) │
 │ watch · consent · Install CLI    save/restore scroll only  │
 └──────────────┬─────────────────────────────────────────────┘
                │ calls
                ▼
 ┌────────────────────────────────────────────────────────────┐
 │ src/core  (pure: no vscode, no fs)                         │
 │ validators · state changes · consistency check · render    │
 └──────────────▲─────────────────────────────────────────────┘
                │ calls
 ┌──────────────┴─────────────────────────────────────────────┐
 │ src/cli  (reads files, calls core, writes)                 │
 └──────────────┬─────────────────────────────────────────────┘
                ▼
        .workflow/progress.json · progress.config.json
```

- 📌 The webview sends no messages; the extension ignores any it gets.
- 📌 Adapters live apart in `src/adapters`. Runtime dependencies: none.
