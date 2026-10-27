# Pattern: risk ──▶ mitigation rows

Excerpt from a real `_beautyfact` file. Copy the shape, not the content.

## 10. ⚠️ Risks / Trade-offs

🔗 Source: [design.md L138–L144](design.md#L138)

```text
 Agent sync never runs command probes  ──▶ skipped and named
 Page replace loses scroll position    ──▶ script restores it (D18)
 Stale lock blocks writes              ──▶ expires after 10 s (D14)
 Hook event names differ per harness   ──▶ confirm before the adapter
 Copied CLI goes out of date           ──▶ version file, offer reinstall
```

- ⚠️ Command probes never run from an agent's `sync`: they are skipped and named, and «**Workflow: Run sync**» runs them after consent.
- ⚠️ Hook event names and payload fields differ per harness: confirm them before writing the adapter, as the spec says.
- ⚠️ The copied CLI goes out of date after an extension update: `.workflow/bin/` holds a version file, and the extension offers to reinstall.
