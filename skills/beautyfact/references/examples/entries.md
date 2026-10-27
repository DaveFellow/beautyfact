# Pattern: entries with an ID, a title, a link and labeled lines

Excerpt from a real `_beautyfact` file. Copy the shape, not the content.

## 4. 🧱 Foundations

🔗 Source: [design.md L34–L51](design.md#L34)

All rules live in one pure function: it takes config, state, the change, time and source, and returns new state or an error. The CLI only reads and writes files around it.

```text
 inputs ──▶ src/core: pure function ──▶ new state  or  error
 (config, state, change, time, source)
```

- D9 «**Inherited rules**» 🔗 [L36–L39](design.md#L36)
  - 📌 **Decision:** layers, dependency direction, and allowed dependencies follow `architecture.md`. Runtime dependencies: none.
  - ❌ **Rejected:** restating them here.
  - 💡 **Why:** one owner per fact.
- D10 «**Pure core**» 🔗 [L40–L43](design.md#L40)
  - 📌 **Decision:** each state change is a pure function of config, state, the requested change, the time, and the source. It returns the new state or an error. The CLI reads files, calls it, and writes.
  - ❌ **Rejected:** letting the CLI mutate the parsed file in place.
  - 💡 **Why:** `node:test` and mutation testing cover every rule without touching the disk.
- D11 «**Validation by hand**» 🔗 [L44–L47](design.md#L44)
  - 📌 **Decision:** `src/core` holds hand-written validators for the config and the state, with limits: 1 MB per file, 500 units, 200-character names.
  - ❌ **Rejected:** a schema library.
  - 💡 **Why:** no runtime dependencies are allowed, and the shapes are small.
- D21 «**One consistency check**» 🔗 [L48–L51](design.md#L48)
  - 📌 **Decision:** one pure check in `src/core` serves `validate` and the panel warning.
  - ❌ **Rejected:** a second copy of the rules in the panel.
  - 💡 **Why:** the two can never disagree.

- S1 🔒 «**Command probe runs by itself**» 🔗 [L119–L121](design.md#L119)
  - 🛡️ **Addressed by:** D16, D17, D22.
  - 🎯 **Scenarios:** «**Untrusted workspace**», «**No consent yet**», «**Config change needs consent again**», «**Probe hangs**».
- S2 🔒 «**Path escape**» 🔗 [L122–L124](design.md#L122)
  - 🛡️ **Addressed by:** D13, D22, real-path checks on every read and write.
  - 🎯 **Scenarios:** «**Path-like unit id**», «**File probe outside the workspace**».
- S3 🔒 «**Markup in names**» 🔗 [L125–L127](design.md#L125)
  - 🛡️ **Addressed by:** D18, a strict Content-Security-Policy with a nonce, `textContent` only.
  - 🎯 **Scenarios:** «**Markup in a name**», «**Message from the webview**».
- S4 🔒 «**Malformed or huge files**» 🔗 [L128–L130](design.md#L128)
  - 🛡️ **Addressed by:** D11 limits and shape checks.
  - 🎯 **Scenarios:** «**Malformed JSON**», «**Wrong type**», «**Oversized argument**», «**Unit refers to unknown phase**».
- S5 🔒 «**Hostile hook text**» 🔗 [L131–L133](design.md#L131)
  - 🛡️ **Addressed by:** D23.
  - 🎯 **Scenarios:** «**Hostile event text**».
- S6 🔒 «**Fake or lost state**» 🔗 [L134–L136](design.md#L134)
  - 🛡️ **Addressed by:** D14, D15, D21. State is never repaired silently.
  - 🎯 **Scenarios:** «**Write fails midway**», «**Inconsistent state**», «**Cleanup commands**».
