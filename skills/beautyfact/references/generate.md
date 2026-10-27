# Generating spec, plan, tasks and test list

Loaded from `SKILL.md` only when one of these artifacts is requested from scratch. The principles, ASCII rules and WHEN/THEN format live in `SKILL.md`.

## Traceability

Use stable IDs and link them across artifacts:

```text
 RF-xx  ──▶  T-xx  ──▶  TC-xx
 requirement  task     test case
```

- Requirements: `RF-01…` (functional), `RNF-01…` (non-functional).
- Tasks: `T-01…`, with the RF/RNF they cover.
- Tests: `TC-01…`, with the RF/RNF or criterion they verify.
- Every must-have RF has at least one task and one test. Point out the gaps.

## 1. Spec

What is built and why. No implementation decisions (those go in the plan).

Sections, in this order (omit those that do not apply):

1. **Summary** — 2 sentences + a «the idea in one view» diagram + success metrics (3 bullets).
2. **Scope** — two-column IN / OUT diagram + platforms and languages.
3. **Main flow** — flowchart of the central path + 2 secondary flows in one line each.
4. **Functional requirements** — bullets grouped by module with emoji, `RF-xx` and priority (M must, S should).
5. **Non-functional requirements** — bullets with measurable figures (performance, offline, security, accessibility, compatibility).
6. **Data model** — mind map, relations, lifecycle of the main entity, integrity rules.
7. **Contracts / API** — client ◀──▶ server sequence + endpoints as bullets + error format.
8. **Screens and UX** — navigation map + mockup of the key screen + gestures and design rules.
9. **Edge cases** — decision diagram of the most complex case + bullets with emoji.
10. **Acceptance criteria** — `- [ ]` checklist in WHEN/THEN format (see «WHEN/THEN format»), linked to RF.
11. **Open questions** — bullets; what is unresolved is not invented.

## 2. Plan / design

How it is built. Starts from an existing spec and cites it by ID.

Sections:

1. **Context and goal** — 2–3 lines; link the spec.
2. **Architecture** — component diagram and who calls whom (client/server, modules, stores).
3. **Decisions** — one line each: *decision ──▶ why ──▶ rejected alternative*. Mark those still to validate.
4. **Data and contracts** — only what changes or is critical; refer to the spec for the rest.
5. **Technical flows** — sequence or states of the delicate parts (sync, auth, queues).
6. **Phases and gates** — phase line with `◆` and the criterion of each gate.
7. **Risks** — `risk ──▶ mitigation`, at most 5.
8. **Out of the plan** — what is postponed.

Do not invent technology without marking it as a proposal. Do not fix dates if the user gave none: use relative weeks and mark them as an estimate.

## 3. Tasks

Executable work derived from the plan, ordered by dependency.

Format of each task (checklist):

```text
- [ ] T-03 · Verb + concrete object   [M]  ◀ T-01, T-02
      covers: RF-02, RF-03
      done when: one-sentence verifiable criterion
```

Rules:

- Title starts with a verb and fits on one line.
- Size S (≤ half a day), M (≤ 2 days) or L (more; split it if you can).
- «Done when» is always measurable; if it cannot be measured, the task is badly defined.
- Group by milestone with `### 🧱 Name`.
- If there are more than 6 tasks, include a dependency diagram:

```text
 T-01 ──▶ T-02 ──▶ T-04 ──▶ T-06
   └────▶ T-03 ──────┘
```

- Close with 🚧 **Blockers and assumptions** (at most 3 bullets).

## 4. Test list

Verifiable cases, linked to requirements.

Format (table; the user may add rows):

| ID | Case | Should | Should not |
| --- | --- | --- | --- |
| TC-01 | Create task with a valid title (RF-02) | Appears in the Inbox and persists after closing the app | — |
| TC-02 | Create task with an empty title (RF-02) | Show a field error | Create the task |

Rules:

- **Case:** a concrete situation, in one line (given/when compressed).
- **Should:** observable, measurable result (with a figure if the spec gives one).
- **Should not:** only when a relevant unwanted effect exists (duplicates, data loss, permission leak, inconsistent state). If it does not apply, leave `—`; if no row needs it, remove the column.
- Group by area with `### 🔀 Name` (main flow, edge cases, security, performance, accessibility).
- Always cover: happy path, validations, offline / external error, concurrency or conflict, permissions, and the NFRs with figures.
- Each row ends with the RF/RNF it verifies, for example `(RF-02)`.
- Optionally close with a proportion diagram (unit / integration / E2E) with `▓` bars if it helps decide where to invest.

## Workflow

1. Identify which artifact is requested. If there is no spec and a plan, tasks, or tests are requested, first summarize the assumptions in 3 bullets and continue; do not block.
2. If the artifacts are requested together, respect the order spec ──▶ plan ──▶ tasks ──▶ tests and keep the IDs consistent.
3. Write, draw, and complement section by section with the format above.
4. Review before delivering:
   - Does each structured section have its diagram, and is it aligned?
   - Does each important RF have a task and a test?
   - Is the ~200-line limit respected?
   - Is anything invented without being marked as a proposal or estimate?
5. Deliver and mention in one sentence the traceability gaps or the most important open questions.

## Common adjustments

- «Shorter» ──▶ remove complements, keep diagrams and M requirements.
- «More detailed» ──▶ add subsections and complements, but stay under ~200 lines; if needed, split into two artifacts.
- «Only one section» ──▶ apply the same pattern (diagram + complements) to that section and offer to link it to the rest.
