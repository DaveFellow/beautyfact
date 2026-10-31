# Pattern: folder tree and a short chain of steps

Excerpt from a real `_beautyfact` file. Copy the shape, not the content.

## 8. 📦 Distribution and adapters

🔗 Source: [design.md L104–L113](design.md#L104)

```text
 .workflow/bin/
 ├── progress.js
 ├── core files
 └── version file
```

```mermaid
flowchart LR
  ext["extension"] -->|"Workflow: Install CLI"| bin[".workflow/bin/"]
  agent["agent"] -->|"node .workflow/bin/progress.js"| bin
```

The extension copies the CLI into `.workflow/bin/` so agents have a stable path. Claude Code hooks are written only after you confirm, and each runs one fixed line, never text from an event.

```mermaid
flowchart LR
  triggers["config triggers"] --> show["skill shows hook entries"]
  show --> confirm{"user confirms?"}
  confirm -->|"yes"| settings[".claude/settings.json<br/>edited only now"]
  settings --> line["each hook runs ONE fixed CLI line<br/>with --source claude-code"]
```
