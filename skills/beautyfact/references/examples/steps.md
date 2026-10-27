# Pattern: steps over states: a table that changes row by row

Excerpt from a real `_beautyfact` file. Copy the shape, not the content.

## 5. ✍️ State and writes

🔗 Source: [design.md L53–L73](design.md#L53)

### 🔄 D12 · how a phase move marks «**done**» 🔗 [L55–L61](design.md#L55)

```text
                  Plan   Red    Green  Audit
 1 start          [>]    [ ]    [ ]    [ ]
 2 Plan ▶ Green   [x]    [x]    [>]    [ ]    Red skipped: done
 3 Green ▶ Audit  [x]    [x]    [x]    [>]    Green left: done
 4 Audit ▶ Green  [x]    [x]    [>]    [ ]    Green +1 visit
 [>] current   [x] done   [ ] not done
```

- 📌 Step 2: «**Red**» is skipped, so it is done with 0 visits.
- 📌 Step 4: backward, so no done mark changes and «**Audit**» keeps its visit.
