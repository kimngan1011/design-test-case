---
name: update-domain-knowledge
description: >
  **WORKFLOW SKILL** — Update the domain knowledge file with confirmed new business rules from an analyzed requirement.
  USE FOR: Phase 6a of analyze-requirement agent — runs after user approves questions posted to Jira.
  INPUT: temp/impact_findings.json + temp/business_rules.json (already on disk).
  OUTPUT: Updated file(s) under knowledge/domain-knowledge/<domain>/ (after user approval). The domain folder is split per sub-domain — see overview.md § File index for the correct target file.
  DO NOT USE FOR: documenting production incidents (use save-slack-issue for that).
---

# Skill: Update Domain Knowledge

You are adding confirmed new business rules to the domain knowledge file so future analyses of related tickets will have accurate context. This is a write operation — never auto-update without user approval.

---

## Input

Read from disk (do not rely on chat context):

- `temp/impact_findings.json` — to identify rules tagged `[EXTENDED]` or `[REPLACED]`
- `temp/business_rules.json` — full content of new business rules

---

## Workflow

### Step 1 — Identify update candidates

From `temp/impact_findings.json`, filter rules that should be added to domain knowledge:

| Finding tag                            | Action                                                   |
| -------------------------------------- | -------------------------------------------------------- |
| `[EXTENDED]`                           | Add as new sub-rule to existing section                  |
| `[REPLACED]`                           | Mark old rule as superseded + add new rule               |
| `[CONFLICT]` with confirmed resolution | Add the winning rule, mark the losing rule as superseded |
| `[CONFLICT]` unresolved                | Skip — do not add until resolved                         |
| `[MISSING BEHAVIOR]` confirmed by PM   | Add as new rule                                          |

> Rules tagged `[MISSING BEHAVIOR]` that were NOT clarified → do not add (still ambiguous).

### Step 2 — Locate the correct file + section

Domain knowledge is split per sub-domain. First read `knowledge/domain-knowledge/<domain>/overview.md` § File index to discover the right file.

For each rule, locate the target file by topic. For the `scheduling` domain:

| Topic of the new rule                                                                                                   | Target file                                     |
| ----------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------- |
| Lesson entity (CRUD, recurrence, status, code, end-date, closed dates, Zoom, lesson report)                             | `lesson-management/lesson.md`                   |
| Lesson Allocation authorization (Require Allocation, duration, order lifecycle)                                         | `lesson-management/lesson-allocation.md`        |
| Student Session entity (assignment methods, recurring scope, filter, name display)                                      | `lesson-management/student-session.md`          |
| Class-based auto-assign/auto-remove OR multi-class lesson configuration                                                 | `lesson-management/class-assignment.md`         |
| Lesson Teacher entity (clashing, cross-location access, Monthly Lesson Count)                                           | `lesson-management/lesson-teacher.md`           |
| **Mobile (Learner App) viewing or any push notification to student/parent** (incl. per-lesson publish notify)           | `lesson-management/lesson-mobile.md`            |
| Event Master, Activity Event, Booking, Events on Calendar                                                               | `event/<entity>.md`                             |
| SF Calendar features (drag&drop, multi-class display, **bulk publish**, clashing, view, filter)                         | `calendar/calendar-sf.md`                       |
| BO Calendar features (incl. Renseikai bulk attendance)                                                                  | `calendar/calendar-bo.md`                       |
| Calendar lesson-detail contextual lists (Student / Teacher / Reallocation)                                              | `calendar/student-teacher-reallocation-list.md` |
| Calendar access rules (CPU/SPU vs affiliation)                                                                          | `calendar/access-by-user-type.md`               |
| Partner-specific behaviors NOT fitting above (Nichibei booking, Nichibei point LA, Riso manual LA, Koyu event features) | `partner-rules/<tenant>-<feature>.md`           |

Then inside the target file:

- Match the most specific section (e.g., "Lesson Statuses", "CRUD Operations", "Notification Recipients").
- If no section matches: propose a new sub-section under the closest parent.
- If no existing file fits at all: propose creating a new file under the correct sub-folder, citing why.

### Step 3 — Draft proposed changes

For each update candidate, draft the proposed addition:

**For `[EXTENDED]` rules:**

```markdown
#### [EXISTING SUBSECTION NAME]

... existing content ...

- **[NEW RULE]**: [Rule description]. Added from LT-XXXXX ([date]).
```

**For `[REPLACED]` rules:**

```markdown
- ~~**[OLD RULE]**: [Old description].~~ _(Superseded by LT-XXXXX — see below)_
- **[NEW RULE]**: [New rule description]. Replaces previous rule as of LT-XXXXX ([date]).
```

### Step 4 — Present diff to user

Before writing any changes, present the full proposed diff:

```
=== DOMAIN KNOWLEDGE UPDATE PREVIEW ===

File: knowledge/domain-knowledge/scheduling/lesson-management/lesson-mobile.md

Section: Publish & Notify Student (Renseikai)
PROPOSED ADDITIONS:
+ ### New deep-link variant — open lesson chat
+ - When the notification is tapped from a Draft lesson context, the app deep-links to
+   the Lesson Chat tab instead of the Lesson Detail tab. Added from LT-XXXXX (2026-04-14).

File: knowledge/domain-knowledge/scheduling/lesson-management/lesson.md

Section: Lesson Statuses
PROPOSED ADDITIONS:
+ - **Publish & Notify path**: When "Publish & Notify" button is clicked on a Draft lesson,
+   lesson status changes to Published immediately (status change happens BEFORE the
+   confirmation modal). See lesson-mobile.md for the notification flow.
+   Added from LT-XXXXX (2026-04-14).

Apply these changes? (Y/N)
```

### Step 5 — Apply approved changes

Only write to the file after user explicitly confirms Y.

If user says N → log "Domain knowledge update declined by user" and proceed to next phase.

If user modifies the proposed text → incorporate their edits before writing.

---

## Safety Rules

- **NEVER auto-update** — always present diff and wait for explicit Y
- **Only add confirmed rules** — no speculative rules, no "probably" behaviors
- **Never remove existing rules** — only mark as superseded (strikethrough + note)
- **Always include source reference** — every addition must cite the ticket ID and date
- **Maintain existing document style** — match heading levels, list format, table format of surrounding content

---

## Quality Checks

- [ ] Read temp/impact_findings.json and temp/business_rules.json from disk
- [ ] Only `[EXTENDED]`, `[REPLACED]`, and confirmed `[MISSING BEHAVIOR]` rules are update candidates
- [ ] Correct section identified by reading the full domain knowledge file
- [ ] Full diff presented to user before any write
- [ ] Waited for explicit Y before writing
- [ ] Every addition cites ticket ID and date
- [ ] Existing rules not deleted — only marked as superseded if `[REPLACED]`
- [ ] Document style preserved (headings, lists, tables)
