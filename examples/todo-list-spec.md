# To-Do List App — Spec

## 1. Summary

A mobile and web to-do list app that lets a single user create, organize,
and complete tasks, and keeps working offline. The app syncs automatically
once the connection returns, so nothing is lost between devices.

Success metrics:
- 95% of tasks created offline sync within 5 seconds of reconnecting.
- Fewer than 1% of sync operations produce a duplicate or lost task.
- A new user can create their first task in under 10 seconds.

## 2. Scope

In scope:
- Create, edit, complete, and delete tasks.
- Group tasks into lists (e.g. "Work", "Personal").
- Due dates and simple reminders.
- Offline use with background sync.

Out of scope:
- Sharing lists or tasks with other users.
- Sub-tasks or checklists inside a task.
- Calendar integrations.

Platforms: iOS, Android, and a responsive web app. Backend in Node.js,
client apps in React Native (mobile) and React (web).

## 3. Main flow

The central path: the user opens the app, adds a task to a list, and
marks it done when finished.

1. User opens the app and lands on the "Inbox" list.
2. User taps "Add task", types a title, and optionally sets a due date
   and a list.
3. Task appears at the top of the list, marked as pending.
4. User taps the checkbox to mark the task as done; it moves to a
   collapsed "Completed" section.

Secondary flows:
- User creates a new list from the sidebar and assigns a color to it.
- User edits a task's title, due date, or list from the task's detail view.

## 4. Functional requirements

Tasks:
- RF-01 (M): User can create a task with a title (required) and an
  optional due date and list.
- RF-02 (M): User can edit any task field after creation.
- RF-03 (M): User can mark a task as done or undone.
- RF-04 (M): User can delete a task; deletion is reversible for 10
  seconds via an "Undo" toast.

Lists:
- RF-05 (M): User can create, rename, and delete a list.
- RF-06 (S): User can assign a color to a list.
- RF-07 (M): The default "Inbox" list cannot be deleted.

Offline and sync:
- RF-08 (M): All task and list operations work offline and are queued.
- RF-09 (M): Queued operations sync automatically when the connection
  returns, without user action.
- RF-10 (S): A reminder notification fires at the task's due date/time
  if the device has notifications enabled.

## 5. Non-functional requirements

- Performance: the task list renders in under 300ms for up to 1,000
  tasks.
- Offline: the app is fully usable with no network connection; no
  operation blocks on the network.
- Sync: queued operations sync within 5 seconds of regaining
  connectivity, applied in the order they were created.
- Security: all sync traffic uses HTTPS; tasks are scoped to the
  authenticated user only.
- Accessibility: all interactive elements have a minimum 44x44pt touch
  target and support screen readers.
- Compatibility: iOS 15+, Android 10+, and the two latest versions of
  Chrome, Safari, and Firefox for web.

## 6. Data model

Entities:
- `Task`: id, title, done (bool), due_date (optional), list_id, created_at,
  updated_at, deleted_at (optional, for soft delete).
- `List`: id, name, color, is_default (bool), created_at.

Relations: a `List` has many `Task`s; a `Task` belongs to exactly one
`List`. Deleting a `List` moves its tasks to "Inbox" rather than deleting
them.

Task lifecycle: `pending` → `done` (toggleable both ways) → `deleted`
(soft, kept 30 days before hard delete) → purged.

Integrity rules:
- A task's `list_id` must reference an existing list; if its list is
  deleted, `list_id` is rewritten to the Inbox list's id, never left
  dangling.
- `done` transitions do not change `due_date`.

## 7. Contracts / API

The client and server exchange a sync payload: the client sends all
locally queued operations since the last successful sync, and the
server returns the authoritative state of anything that changed
elsewhere.

- `POST /sync` — body: `{ since: timestamp, ops: [...] }`. Returns
  `{ server_time, applied: [...], conflicts: [...] }`.
- `GET /tasks` — returns the full task list for the authenticated user
  (used for first login or a full resync after 30+ days offline).
- `PATCH /tasks/:id` — single-task edit, used for the detail view when
  online.

Error format: `{ error: { code, message } }`. Sync conflicts (the same
task edited on two devices before either synced) are resolved
last-write-wins by `updated_at`, and the losing edit is returned in
`conflicts` so the client can show it was overwritten.

## 8. Screens and UX

Screens: Inbox (default), List view, Task detail, Lists sidebar.

Navigation: sidebar → List view → tap a task → Task detail. A floating
"+" button is present on every list screen to add a task.

Key screen — List view:
- Header with the list name and color.
- Scrollable task rows: checkbox, title, due date badge if set.
- Completed tasks collapse into a "Completed (N)" section at the
  bottom, expandable.
- Swipe left on a row reveals "Delete"; swipe right reveals "Edit".

Gestures: swipe to delete/edit, pull to refresh (forces a sync attempt),
long-press to multi-select tasks for bulk delete or move.

Design rules: pending tasks use the list's color as an accent; completed
tasks are shown at 50% opacity with a strikethrough title.

## 9. Edge cases

Most complex case: a task is edited offline on two different devices
before either syncs, producing a conflict.

1. Device A edits the task's due date while offline.
2. Device B edits the task's title while offline (different field, same
   task).
3. Device A reconnects first and syncs; server now holds A's edit.
4. Device B reconnects and syncs; server applies B's edit on top
   (different field, no real conflict) but keeps A's due date, since
   last-write-wins is applied per full record, not per field, so the
   second writer's `updated_at` wins for the whole record and the
   server returns the previous state in `conflicts` for the client to
   diff and warn the user if any field changed unexpectedly.

Other edge cases:
- Deleting a task offline, then editing it on another device before
  sync: the delete wins (soft-deleted tasks are not resurrected by a
  stale edit).
- A due date reminder fires for a task that was completed moments
  earlier on another device but not yet synced locally: the
  notification still fires, since the device has no way to know yet.
- Deleting the list a pending offline task belongs to: on sync, the
  task is reassigned to Inbox rather than failing.

## 10. Acceptance criteria

- [ ] CA-01 (RF-01) — Create a task with only a title
  - WHEN the user adds a task with just a title and no due date or list
  - THEN it appears in Inbox, pending, within 1 second
- [ ] CA-02 (RF-04) — Delete with undo
  - WHEN the user deletes a task
  - THEN it disappears immediately and an "Undo" toast appears for 10
    seconds
  - NOT the task is removed from the server before the undo window
    closes
- [ ] CA-03 (RF-08, RF-09) — Create offline, then sync
  - WHEN the user creates 3 tasks offline and then regains the network
  - THEN all 3 sync to the server within 5 seconds
  - NOT any task is duplicated or lost
- [ ] CA-04 (RF-07) — Inbox cannot be deleted
  - WHEN the user tries to delete the "Inbox" list
  - THEN the delete option is disabled and no action is taken

## 11. Open questions

- Should reminder notifications be configurable per task (e.g. "30 min
  before"), or always fire exactly at the due time?
- Is there a limit on how many lists a single user can create?
