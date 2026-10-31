# Pattern: decisions with yes / no branches

Excerpt from a real `_beautyfact` file. Copy the shape, not the content.

## 6. 🔎 Probes and sync

🔗 Source: [design.md L75–L91](design.md#L75)

```mermaid
flowchart TD
  start(["Workflow: Run sync<br/>(explicit command, never on panel load)"]) --> trust{"workspace trusted?"}
  trust -->|"no"| skip["skip, name the probe"]
  trust -->|"yes"| consent{"consent for this command hash?"}
  consent -->|"no"| ask["ask, run nothing"]
  consent -->|"yes"| run["run: cwd = workspace, 30 s limit"]
  run --> stdin["results on stdin"] --> sync["progress sync"] --> file["progress.json"]
```

- 📌 Consent lives in VS Code workspace state; an edited command has a new hash and asks again.
- 📌 A plain CLI `sync` runs file probes only and names the skipped commands.
