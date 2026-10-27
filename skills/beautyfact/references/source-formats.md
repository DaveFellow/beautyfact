# Source formats

Loaded from `SKILL.md` only when converting an artifact. The core rules are in `SKILL.md`.

## Source formats

How to apply the core rules to a specific spec-driven toolkit. Use the headings and IDs found in the source; the names below are the usual template ones and may vary by version.

### OpenSpec

Layout: `openspec/changes/<change>/` with `proposal.md`, `design.md`, `tasks.md`, and `specs/<capability>/spec.md`.

| Source | Diagrams to use |
| --- | --- |
| `proposal.md`: Why, What Changes, Capabilities, Impact | Problem ──▶ fix flow, change tree, capability tree (two-line entries), impact tree |
| `proposal.md`: Out of Scope, Draft Acceptance Criteria, Decisions | Two columns «out / instead in v1», state strip or mockup per criterion group, decision map, small diagram per decision |
| `design.md`: Context, Goals / Non-Goals, Architecture | Two columns goals / non-goals, stacked layers |
| `design.md`: Decisions, Security, Risks | Decision map with `▓` bars, flows (sequence, probe flow, pipeline), threat bars, risk rows |
| `specs/*/spec.md`: Purpose, `## ADDED / MODIFIED / REMOVED Requirements` | Purpose diagram, then per requirement the `SHALL` sentence as a quote and a small diagram where it helps |
| `#### Scenario:` WHEN / THEN | One entry per scenario with a link beside the title (WHEN and THEN as sub-bullets, verbatim; every line after the WHEN starts with `──▶`: `- WHEN …` then `- ──▶ THEN …`, `- ──▶ NOT …`) |
| `tasks.md` | Dependency diagram; keep task numbering and checkboxes |

Project conventions to keep when present (see `.claude/rules/writing.md`):

- The «What to check» opener, «Summary» checkbox groups, «Out of Scope», «Modified Capabilities», «Open Questions» and the «Deferrable» reasons.
- Entry shapes: `D3 🧭`, `S1 🔒`, `C2 ✏️`, `Q1 ❓`, test entries (📥 Input, 🎯 Expected output), acceptance steps (👉 Do, 👀 You should see).
- `### Requirement:` and `#### Scenario:` titles stay recognizable.

### Spec Kit

Layout: `.specify/memory/constitution.md`, and per feature `specs/<NNN-feature>/` with `spec.md`, `plan.md`, `research.md`, `data-model.md`, `contracts/`, `quickstart.md`, `tasks.md`.

Every Spec Kit artifact gets the same treatment as the examples in `references/examples/`, with no exceptions: a diagram per structured section, a 1–3 line summary before a diagram-only section, nothing omitted (including `[NEEDS CLARIFICATION]` markers and every `FR-` / `SC-` / `T` ID), a `🔗 Source` link per section, and a link beside each story, scenario, requirement, and task title.

| Source | Diagrams to use |
| --- | --- |
| `constitution.md`: principles | One entry per principle with its rule; a gate list that `plan.md` checks against |
| `spec.md`: user stories with priority (P1, P2…) | Story flow per story, Given / When / Then kept verbatim, one entry each with a link |
| `spec.md`: `FR-001` requirements, key entities, `SC-001` success criteria | Requirement groups with IDs, entity relation tree, success bars; keep every `[NEEDS CLARIFICATION]` marker as an open question |
| `plan.md`: technical context, constitution check, project structure | Two-column key / value, pass / fail gate rows, folder tree |
| `research.md` | Decision entries: decision ──▶ rationale ──▶ alternatives considered |
| `data-model.md` | Entity relation tree, state strip for lifecycles, validation rules as bullets |
| `contracts/` | One sequence per endpoint or event, error cases as bullets |
| `quickstart.md` | Numbered step flow with the expected result per step |
| `tasks.md`: `T001`, `[P]`, `[US1]`, phases | Phase groups (setup, foundational, per story, polish), dependency diagram with parallel lanes for `[P]` tasks, checkpoints |
