# Pattern: acceptance criteria or scenarios (WHEN / THEN)

Excerpt from a real `_beautyfact` file. Copy the shape, not the content.

## 6. 🎯 Draft Acceptance Criteria

🔗 Source: [Draft Acceptance Criteria L60–L77](proposal.md#L60)

Sixteen criteria in four groups (grouping, not in the source): CLI writes, phase moves, panel display, sync and safety.

| Group | Criteria |
| --- | --- |
| CLI writes (grouping) | Add a unit · Reject unknown phase |
| Phase moves (grouping) | Advance · Skipped phases done · Backward jump |
| Panel display (grouping) | Gate lock · Lock clears · Done unit |
| Sync, safety (grouping) | Probe sync · Untrusted workspace |

### 🔄 Phase moves, step by step 🔗 [L63–L67](proposal.md#L63)

| Step | Plan | Red | Green | Audit | Note |
| --- | --- | --- | --- | --- | --- |
| 1 start | [>] | [ ] | [ ] | [ ] | |
| 2 Plan ▶ Green | [x] | [x] | [>] | [ ] | Red skipped: done |
| 4 Audit ▶ Green | [x] | [x] | [>] | [ ] | Green visit 2: shows 2 |

### 🎯 Criteria 🔗 [L62–L77](proposal.md#L62)

- 🎯 **Add a unit** 🔗 [L62](proposal.md#L62)
  - WHEN `progress add-unit` runs with «**Login screen**»
  - ──▶ THEN `progress.json` lists it as «**pending**»
- 🎯 **Reject unknown phase** 🔗 [L64](proposal.md#L64)
  - WHEN `set-phase` names a phase missing from the config
  - ──▶ THEN the CLI exits with a clear error and writes nothing
- 🎯 **Repeat is a no-op** 🔗 [L68](proposal.md#L68)
  - WHEN the same `set-phase` call runs twice in a row
  - ──▶ THEN the second call changes nothing, adds no history entry, and adds no visit
