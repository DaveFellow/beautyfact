# Pattern: architecture as stacked layers that call each other

Excerpt from a real `_beautyfact` file. Copy the shape, not the content.

## 2. 🏗️ Architecture

🔗 Source: [D9 L36–L39](design.md#L36) · [D18 L95–L98](design.md#L95) · [D20 L106–L109](design.md#L106)

```mermaid
flowchart TD
  subgraph ext["src/extension (VS Code)"]
    watch["watch · consent · Install CLI"]
  end
  subgraph web["src/webview (page script)"]
    scroll["save/restore scroll only"]
  end
  subgraph core["src/core (pure: no vscode, no fs)"]
    rules["validators · state changes ·<br/>consistency check · render"]
  end
  subgraph cli["src/cli"]
    io["reads files, calls core, writes"]
  end
  ext -->|"calls"| core
  cli -->|"calls"| core
  cli --> files[".workflow/progress.json ·<br/>progress.config.json"]
```

- 📌 The webview sends no messages; the extension ignores any it gets.
- 📌 Adapters live apart in `src/adapters`. Runtime dependencies: none.
