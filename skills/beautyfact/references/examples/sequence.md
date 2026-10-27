# Pattern: two actors and a shared resource over time

Excerpt from a real `_beautyfact` file. Copy the shape, not the content.

### 🔐 D14 + D15 · two parallel hooks, no lost update 🔗 [L66–L73](design.md#L66)

```text
 hook A       progress.lock   progress.json      hook B
    │               │               │               │
    │── take lock ─▶│               │               │
    │               │◀── lock busy ─┼───────────────│
    │── re-read ────┼──────────────▶│               │
    │── write temp ─┼── rename ────▶│               │
    │── release ───▶│               │               │
    │               │◀── lock ok ───┼───────────────│
```

- 📌 Lock waits a few seconds; a lock older than 10 s is stale and replaced.
- 📌 Write goes to a temp file in `.workflow/`, then rename: no half-written file.
