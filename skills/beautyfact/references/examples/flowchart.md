# Pattern: decisions with yes / no branches

Excerpt from a real `_beautyfact` file. Copy the shape, not the content.

## 6. 🔎 Probes and sync

🔗 Source: [design.md L75–L91](design.md#L75)

```text
 Workflow: Run sync   (explicit command, never on panel load)
          │
          ▼
 workspace trusted? ── no ──▶ skip, name the probe
          │ yes
          ▼
 consent for this command hash? ── no ──▶ ask, run nothing
          │ yes
          ▼
 run: cwd = workspace, 30 s limit
          │
          ▼
 results on stdin ──▶ progress sync ──▶ progress.json
```

- 📌 Consent lives in VS Code workspace state; an edited command has a new hash and asks again.
- 📌 A plain CLI `sync` runs file probes only and names the skipped commands.
