# Test Cases: PBT-3507 — [Nichibei] Additional Requirements for Lesson Booking System

## Suite: Lesson Report Display

### [Nichibei] Lesson Report – Detail Section – Learner App – Detail section not shown

**Description:** #18 — Smoke — In the Nichibei learner app, the lesson report detail part (quiz / exercises section) is hidden because Nichibei does not use it.

**Preconditions:**
- Logged in as a student to the Nichibei learner app
- A lesson exists with a lesson report that includes a detail section (e.g. quiz or exercises)

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open the Nichibei learner app | App home screen displayed | — |
| 2 | Navigate to a lesson that has a lesson report | Lesson report screen opens | lesson has report with a detail section (e.g. quiz) |
| 3 | View the full lesson report | The detail section (quiz / exercises area) is NOT displayed; only the summary part is shown | detail_section_type = quiz |

**Severity:** major
**Priority:** high

---

### [Nichibei] Lesson Report – Report Label – Learner App – [公開] prefix not shown

**Description:** #19 — Smoke — The "[公開]" prefix is removed from the lesson report label in the Nichibei learner app; the label shows only the report name without the publication status tag.

**Preconditions:**
- Logged in as a student to the Nichibei learner app
- A lesson with a published lesson report exists

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open the learner app and navigate to a lesson that has a lesson report | Lesson report screen shown | — |
| 2 | Read the lesson report label or heading | Label does NOT include the "[公開]" prefix | expected_label does not start with "[公開]"; e.g. shows "授業レポート" not "[公開] 授業レポート" |

**Severity:** minor
**Priority:** medium

---
