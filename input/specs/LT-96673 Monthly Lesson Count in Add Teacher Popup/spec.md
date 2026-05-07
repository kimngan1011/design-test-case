# LT-96673: Monthly Lesson Count in Add Teacher Popup & Calendar Teacher Details

**ID:** https://manabie.atlassian.net/browse/LT-96673
**Status:** Ready for Development
**Partner:** Riso (OOP)
**Issue Type:** Epic
**Analysis Date:** 2026-04-16

---

## Summary

This feature adds a "Monthly Lesson Count" (今月の授業数) column to two surfaces on SF for Riso OOP:

1. **Add Teacher popup** on SF Lesson Detail — shows each teacher's lesson count for the same month as the selected lesson.
2. **Teacher Details panel** on SF Lesson Calendar — shows each selected teacher's lesson count for **today's month** (always current month, regardless of calendar view month).

The goal is to help Centre Managers and HQ staff make informed teacher assignment decisions by showing how many lessons the teacher is already scheduled for that month.

---

## Acceptance Criteria

### US 01 — Monthly Lesson Count View

> As a CM or HQ, I want to see monthly lesson count when opening Add Teacher pop up and teacher details on calendar so that I will know how many lessons teacher has been assigned to, to take further assignment.

| ID      | Feature                                                            | Acceptance Criteria                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| ------- | ------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| AC 01.1 | **Object Manager**                                                 | Create new field under `Lesson Teacher` object. Logic update to populate this field based on the selected lesson when assigning a teacher.                                                                                                                                                                                                                                                                                                                                                                                                                     |
| AC 01.2 | **Monthly Lesson Teacher count in Add Teacher popup**              | **Pre-conditions:** Lessons created successfully; Teachers assigned to lessons across months. **Trigger:** User opens SF Lesson Detail → opens Add Teacher dialog. **Feature:** Based on the selected lesson's month: get all lessons with status Draft/Published/Completed; for each teacher, if assigned to any lesson during that month, calculate and show the count in column "Monthly Lesson Count" (JP: 今月の授業数). Count populates when popup opens (not real-time). When user applies a filter and the teacher list reloads, the count may update. |
| AC 01.3 | **Monthly Lesson Teacher count in Teacher Details on SF Calendar** | **Pre-conditions:** Same as AC 01.2. **Trigger:** User opens SF Lesson Calendar → selects one or more teachers on the left side. **Feature:** Teacher info displayed on the right panel. Shows count of lessons in **current month (today's month)** that teacher is assigned to. Label: "Monthly Lesson Count". Value: number of lessons of teacher. **Even if user changes calendar view to other months, teacher details only show count for current month.**                                                                                               |

---

## Business Rules (Extracted)

| #   | AC                | Business Rule                                                                                                                                                                                                                         | Field                                  | Field Behavior                | Platform |
| --- | ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------- | ----------------------------- | -------- |
| 1   | AC 01.1           | New custom field 'Monthly Lesson Count' created on Lesson Teacher object                                                                                                                                                              | Monthly Lesson Count (LT object field) | auto-calculated               | SF       |
| 2   | AC 01.2           | New column 'Monthly Lesson Count' appears in Add Teacher popup                                                                                                                                                                        | Monthly Lesson Count column            | read-only, display            | SF       |
| 3   | AC 01.2           | Count = lessons (status: Draft/Published/Completed) teacher is assigned to during selected lesson's month                                                                                                                             | Count calculation                      | auto-calculated at popup open | SF       |
| 4   | AC 01.2           | Cancelled lessons are EXCLUDED from the count                                                                                                                                                                                         | Lesson status filter                   | excluded                      | SF       |
| 5   | AC 01.2           | Count populates when popup opens; **not updated in real-time**; applying filters does NOT refresh the count                                                                                                                           | Count update behavior                  | fixed at open time            | SF       |
| 6   | AC 01.2           | Teacher with **zero** lessons in the month shows **0** (not blank)                                                                                                                                                                    | Zero-lesson display                    | 0                             | SF       |
| 7   | AC 01.2           | Count includes lessons from **ALL locations** teacher is assigned to — not limited to the current lesson's location                                                                                                                   | Location scope                         | all locations                 | SF       |
| 8   | AC 01.2           | No role restriction — all SF users who can open the Add Teacher popup see the Monthly Lesson Count column                                                                                                                             | Access control                         | all roles                     | SF       |
| 9   | AC 01.2           | Monthly Lesson Count column is **NOT sortable** — sorting follows existing teacher list logic only                                                                                                                                    | Sortability                            | non-sortable                  | SF       |
| 10  | AC 01.2           | Add Teacher popup count uses SELECTED LESSON's month as reference — not today's month                                                                                                                                                 | Reference period                       | selected lesson's month       | SF       |
| 11  | AC 01.3           | Monthly Lesson Count shown in Teacher Details panel on SF Lesson Calendar (existing UI component)                                                                                                                                     | Monthly Lesson Count (Calendar panel)  | read-only, display            | SF       |
| 12  | AC 01.3           | Calendar Teacher Details count **always uses TODAY's month** regardless of which month the user is viewing                                                                                                                            | Reference period                       | today's month                 | SF       |
| 13  | AC 01.3           | Count shown on Calendar is static per session — no real-time refresh; counts bất kể (regardless of) calendar view navigation                                                                                                          | Count update behavior                  | fixed to today's month        | SF       |
| 14  | AC 01.2 + AC 01.3 | **Month boundary uses lesson datetime in UI/local timezone** — lesson datetime stored in DB as UTC may differ by 1 day from UI display; month calculation must use the local-timezone date displayed in the UI, NOT the raw UTC value | Timezone handling                      | local timezone date           | SF       |

---

## Conflict & Gap Analysis

### Conflicts with Existing System

| #   | Tag | Source | AC  | Description                                             |
| --- | --- | ------ | --- | ------------------------------------------------------- |
| —   | —   | —      | —   | No direct conflicts with existing business rules found. |

### Missing in Requirements

| #   | Tag                | Source                                   | Description                                                                                                                                                                                                                                                                                                                                                                                                            |
| --- | ------------------ | ---------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | [EXTENDED]         | Confluence AC 01.2                       | Monthly Lesson Count column is a net-new display column in the existing Add Teacher popup. No conflicts with existing columns (Location, Working Type, Subject, Working Hours).                                                                                                                                                                                                                                        |
| 2   | [REGRESSION RISK]  | AC 01.2 + AC 01.3 — confirmed by PO note | **Timezone boundary risk:** Lesson datetime is stored in DB as UTC but displayed on UI in local time (JST/org timezone). A lesson on Jan 31 at 11:30pm JST = Feb 1 00:30 UTC. If the system calculates month using DB/UTC value, this lesson would be counted in February instead of January. The count must use UI-local timezone date. This affects month-boundary lessons and is a high-risk data accuracy concern. |
| 3   | [MISSING BEHAVIOR] | AC 01.2                                  | AC does not specify whether "selected lesson's month" uses the lesson's **start date** or **end date** when a lesson spans midnight across month boundaries (edge case).                                                                                                                                                                                                                                               |

### Lesson-Learned Risks

| #   | Incident                         | Date       | AC      | Risk                                                                                                                                                                                           | Guardrail                                                                    |
| --- | -------------------------------- | ---------- | ------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| 1   | Aso — Duplicate Student Sessions | 2026-04-13 | AC 01.2 | If multiple staff simultaneously assign the same teacher to lessons in the same month, the count shown at popup-open may not reflect the latest activity (acknowledged by AC as non-real-time) | Verify count accuracy after concurrent teacher assignments in the same month |

### E2E Scenario Impact

| Scenario                                                                 | Title                        | Impact                                                   | Action                                                                                    |
| ------------------------------------------------------------------------ | ---------------------------- | -------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| All E2E scenarios referencing "Lesson Teacher > Assign in lesson detail" | Teacher Assignment Core Flow | MINOR — display column added; assignment logic unchanged | UPDATE — add a step to verify Monthly Lesson Count column is visible in Add Teacher popup |

### Assumptions Made

- Feature is Riso OOP-only
- Month boundary uses local/UI timezone (confirmed by PO: lesson datetime stored in DB as UTC may differ from UI display date)
- "Selected lesson's month" in AC 01.2 uses the lesson's start date in local time
- Calendar Teacher Details is an existing SF Calendar UI component (not a new one), always showing today's month count regardless of navigation

---

## Clarification Questions

> ✅ All questions answered by PO on 2026-04-16 (via chat). No Jira post required.

| #                       | Question                                                                     | Answer                                                                              |
| ----------------------- | ---------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| Q1 [ROLE GAP]           | Role restriction for Monthly Lesson Count column?                            | **No restriction** — all SF users who can open the Add Teacher popup see the column |
| Q2 [MISSING BEHAVIOR]   | Teacher with 0 lessons in the month — show 0 or blank?                       | **Show 0**                                                                          |
| Q3 [MISSING BEHAVIOR]   | Count includes lessons from all locations or only current lesson's location? | **All locations**                                                                   |
| Q4 [UNDOCUMENTED IN AC] | Is the Calendar teacher panel new or existing? Which views?                  | **Existing UI** — always shows monthly count regardless of calendar view            |
| Q5 [MISSING BEHAVIOR]   | Calendar Teacher Details — UI indication that count is today's month?        | **No additional label** — count is always today's month by design                   |
| Q6 [MISSING BEHAVIOR]   | Filter in Add Teacher popup — does it refresh the count?                     | **Filter does NOT affect the count**                                                |
| Q7 [MISSING BEHAVIOR]   | Is Monthly Lesson Count column sortable?                                     | **Not sortable** — sorting follows existing teacher list logic only                 |

**Additional finding from PO (critical):**

> Month boundary calculation uses **lesson datetime** — lesson date/time stored in DB as UTC may differ from UI-displayed date (local timezone). This can cause lessons near month boundaries to be counted in the wrong month if the system uses the UTC value instead of the local-time value.

---

## Related Specs

- `input/specs/LT-96662 Renseikai Receive notifications when a new lesson is published/spec.md` — Renseikai OOP SF feature for reference (different partner, similar epicstructure)

## Related Test Cases

- `output/test-cases/lesson-management/lesson-teacher/teacher-assignment-lesson-detail.md` — TC-1214 (Add Teacher popup view), TC-1219 (Filter teacher) may need extension to cover Monthly Lesson Count column
- `output/test-cases/lesson-management/lesson-teacher/clashing-alert.md` — not directly impacted; different concern

## QASE Coverage Gaps

**AC 01.2 — Add Teacher popup:**

- Count column displayed when popup opens (happy path — teacher has lessons in selected month)
- Teacher with **0 lessons** in selected month shows **0** (not blank)
- Count includes lessons from **multiple locations** (cross-location accuracy)
- **Cancelled** lessons are excluded from count; Draft/Published/Completed are included
- Count does **NOT refresh** when filter is applied (location, working type, subject, working hours)
- Count does **NOT refresh** in real-time when a new lesson is assigned during same session
- Monthly Lesson Count column is **not sortable**
- All SF user roles (CM, HQ, Centre Staff) can see the column
- Selected lesson in **January** → popup shows January count; lessons from other months not counted
- **[TIMEZONE RISK]** Teacher has a lesson on the last day of month at late evening local time (JST) → count must include/exclude correctly based on UI-local date, not UTC-stored date
- **[TIMEZONE RISK]** Teacher has a lesson on the first day of month at early morning local time → count uses local date; verify lesson is counted in correct month

**AC 01.3 — Calendar Teacher Details panel:**

- Monthly Lesson Count shown in Teacher Details panel when teacher selected
- Count uses **today's month** (not the calendar view month)
- User navigates to **next month** in calendar → count still shows today's month count
- User navigates to **previous month** in calendar → count still shows today's month count
- Teacher with **0 lessons** in today's month shows **0**
- Count includes lessons from **all locations** of teacher
- **Cancelled** lessons not counted; Draft/Published/Completed counted
- **[TIMEZONE RISK]** Lesson on first/last day of current month at boundary hours — count correct per local timezone
