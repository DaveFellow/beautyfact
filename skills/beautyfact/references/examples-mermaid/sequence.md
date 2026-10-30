# Pattern: two actors and a shared resource over time

Excerpt from a real `_beautyfact` file. Copy the shape, not the content.

### 🔐 D14 + D15 · two parallel hooks, no lost update 🔗 [L66–L73](design.md#L66)

```mermaid
sequenceDiagram
  participant a as hook A
  participant lock as progress.lock
  participant file as progress.json
  participant b as hook B
  a->>lock: take lock
  b->>lock: take lock
  lock-->>b: lock busy
  a->>file: re-read
  a->>file: write temp, rename
  a->>lock: release
  lock-->>b: lock ok
```

- 📌 Lock waits a few seconds; a lock older than 10 s is stale and replaced.
- 📌 Write goes to a temp file in `.workflow/`, then rename: no half-written file.
