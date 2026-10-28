---
ticket_id: LT-108382
ticket_url: https://manabie.atlassian.net/browse/LT-108382
title: EEA | Core | Student's Lesson Report or Lesson Classroom info in Lesson object
module: scheduling
bucket: lesson
status: in QA
internal_uat_date: 2026-10-19
production_release_date: 2026-11-02
last_updated: 2026-10-12
---

# LT-108382: Student Lesson Report with Classroom

## Summary

This core Salesforce feature provides a student-scoped lesson report that Centre Staff can open from the Student detail page. The report shows the student's lessons for the current academic year, including the newly requested Lesson Classroom value, so staff can discuss past and upcoming lessons; teachers also use the report to confirm and update attendance.

The supplied Salesforce evidence shows the intended entry point and a report containing student, lesson, attendance, and Student Session data. Qase suite `3713` exists for this ticket and currently contains no cases.

---

## Acceptance Criteria

### US 01 — Open a student's lesson report

- **AC 01.1:** As a Centre Staff user, I can open the Student Lesson Report from the Student detail page.

### US 02 — View a student's current-academic-year lessons

- **AC 02.1:** The report shows the student's lessons in the current academic year, including past and future lessons.
- **AC 02.2:** The report contains these columns: Student Name (生徒名), Lesson Date (授業日), Location (拠点), Start Time, End Time, Lesson Name (授業名), Lesson Teacher (講師名), Lesson Classroom (教室), Attendance Status (出欠状況), Absent Reason (欠席理由), and Student Session.
- **AC 02.3:** Lesson Classroom is added as a new report column. The report obtains the value from the classroom related to the Lesson object.
- **AC 02.4:** Student Session is a link to its detail page.

### US 03 — Use the report for attendance

- **AC 03.1:** As a teacher, I can use the report to confirm and update students' attendance.

### Evidence used

- Jira ticket description and linked child item `LT-108383`.
- Supplied Salesforce screenshots: the Student detail page entry point and the resulting report layout.
- Qase project `PX`, suite `3713`: existing suite, zero test cases.

---

## Business Rules (Extracted)

| # | AC | Business Rule | Field | Field Behavior | Platform |
|---:|---|---|---|---|---|
| BR-01 | AC 01.1 | Centre Staff can open the Student Lesson Report from the Student detail page. | Student Lesson Report link | role-gated navigation | Salesforce |
| BR-02 | AC 02.1 | The report scope is lessons belonging to the selected student in the current academic year, including past and future lessons. | Academic Year / Student | filtered | Salesforce |
| BR-03 | AC 02.2 | The report displays the specified student, lesson, attendance, and Student Session columns. | Report columns | display-only | Salesforce |
| BR-04 | AC 02.3 | Lesson Classroom is displayed as a newly added report column using the classroom related to the Lesson. | Lesson Classroom | derived / display-only | Salesforce |
| BR-05 | AC 02.4 | Student Session is a navigable link to its detail page. | Student Session | link | Salesforce |
| BR-06 | AC 03.1 | A teacher can confirm and update attendance from the report workflow. | Attendance Status / Absent Reason | editable behavior not specified | Salesforce |
| BR-07 | AC 01.1 | Partners may decide whether to add the report link themselves; the ticket frames the feature as core. | Student Lesson Report link | configuration scope not specified | Salesforce |

---

## Conflict & Gap Analysis

### Conflicts with Existing System

No documented contradiction was identified in the scoped review. A deep impact analysis was intentionally skipped at the user's direction.

### Missing in Requirements

| # | Tag | Source | Description |
|---:|---|---|---|
| 1 | [MISSING BEHAVIOR] | AC 02.1 | The ticket does not define the academic-year boundary or the behavior when a student has no current-AY lessons. |
| 2 | [MISSING BEHAVIOR] | AC 02.3 | The ticket does not define the display behavior when a Lesson has no Classroom or the related Classroom is unavailable. |
| 3 | [ROLE GAP] | AC 03.1 | The ticket says teachers can update attendance but does not identify the report control, editable fields, permission model, or save feedback. |
| 4 | [MISSING BEHAVIOR] | AC 02.1–02.4 | The ticket does not specify sort order, pagination, report refresh behavior, or access handling for a student/lesson outside the viewer's scope. |
| 5 | [MISSING BEHAVIOR] | AC 01.1 / BR-07 | The ownership and configuration rule for the Student detail-page report link is ambiguous: core-provisioned versus partner-managed. |

### Lesson-Learned Risks

Not assessed: deep lesson-learned analysis was skipped at the user's direction.

### E2E Scenario Impact

| Scenario | Title | Impact | Action |
|---|---|---|---|
| E2E-01 | Lesson Lifecycle — Create, Teach, Report, View | The report must reflect lesson, student session, attendance, teacher, and classroom data created through the core lifecycle. | COVER IN NEW TESTS |

### Assumptions Made

- “Current AY” refers to the academic year applied by the Salesforce report, but its exact filter definition is not stated.
- Lesson Classroom is a display value; the ticket does not request editing the Classroom from the report.
- Attendance updates use an existing Salesforce attendance mechanism; the exact control and persistence flow require confirmation.
- The supplied screenshots are evidence of the intended surfaces, not an independent requirement source.

---

## Clarification Questions

1. **[MISSING BEHAVIOR]** What field and boundary determine “current AY”, and what should the report show when the selected student has no lessons in that AY?
   _Evidence: `LT-108382`, AC 02.1 specifies current AY but not its filter behavior._
2. **[MISSING BEHAVIOR]** When a Lesson has no linked Classroom, what exact value should the new Lesson Classroom column display?
   _Evidence: `LT-108382`, AC 02.3 requests the column but defines no empty-state behavior._
3. **[ROLE GAP]** Which attendance fields and controls are editable from this report, which teacher roles may save them, and what must confirm a successful save?
   _Evidence: `LT-108382`, AC 03.1 gives the outcome but not the interaction or permission contract._
4. **[MISSING BEHAVIOR]** What is the required default sorting/order of rows, and are pagination or report refresh expectations defined?
   _Evidence: `LT-108382`, AC 02.1–02.4 list data but not list behavior._
5. **[MISSING BEHAVIOR]** Is the Student detail-page report link provisioned by the core feature for every partner, or is it partner-admin configurable?
   _Evidence: `LT-108382` says each PS may decide/add the link while also calling the feature core._

> Not posted to Jira. Posting questions is an external action and requires separate approval.

---

## Related Specs

- `epics/lesson/LT-108378-attendance-remark-lesson-report/spec.md` — related attendance data display and update workflow across Salesforce and Back Office.
- `epics/OOP/aver/LT-105354-aver-lesson-report-improvements/spec.md` — related Lesson Report and Student Session data relationships; tenant-specific behavior only.
- `epics/OOP/aver/LT-111026-aver-lesson-report-duplicate-race-condition/spec.md` — related Lesson Report and Student Session integrity constraints; tenant-specific behavior only.
- `knowledge/domain-knowledge/scheduling/lesson-management/lesson.md` — Lesson, Lesson Report, and Salesforce-to-BO/Mobile relationship rules.
- `knowledge/domain-knowledge/scheduling/lesson-management/student-session.md` — Student Session, attendance, and Lesson relationship rules.

## Related Test Cases

- No existing test case was found in Qase suite `3713`; new coverage is required.
- Existing tenant-specific Lesson Report tests must not be treated as core acceptance coverage without adaptation.

## QASE Coverage Gaps

- AC 01.1 — No target-suite coverage for opening the report from Student detail.
- AC 02.1–02.4 — No target-suite coverage for current-AY filtering, required columns, Lesson Classroom derivation, or Student Session navigation.
- AC 03.1 — No target-suite coverage for teacher attendance confirmation and update behavior.
