---
ticket_id: LT-107175
ticket_url: https://manabie.atlassian.net/browse/LT-107175
title: "[Renseikai] Core | Add Remote Attendance status option and tag"
module: scheduling
bucket: OOP/renseikai
status: In Development
internal_uat_date: null
production_release_date: 2026-09-07
last_updated: 2026-08-17
---

# LT-107175: Remote attendance status and tag

## Summary

Renseikai needs students or parents to signal that a student will join a lesson remotely, so the lesson teacher and centre staff can prepare an online session quickly. The feature adds `Remote` as an Attendance Status and `Attended Remotely` as an Attendance Response on `Student_Sessions__c`, then surfaces the status in SF, BO, and Learner App.

The change also introduces the highest-priority Calendar indicator, an App-to-BO status prefill, and a notification to lesson teacher(s) and centre admin. It does not cover Zoom/meeting-link management, attendance reporting, or changes to Informed Absent/Late flows.

---

## Acceptance Criteria

### US 01 — View / edit Remote Attendance Status

- **AC 01.1 — Lesson Card remote dot:** On SF/BO Lesson Calendar, show a Remote dot for a group lesson when at least one student has `Attendance_Status__c = Remote`; for an individual lesson, show it for that student. The stated color is Vibrant/Indigo/40. If multiple status indicators apply, show only the highest priority: `Remote > New > Trial > Seasonal > Reallocated > Absent`.
- **AC 01.2 — No remote response:** When no student has submitted `Attended Remotely`, do not show a Remote dot; existing dot indicators remain unchanged.
- **AC 01.3 — Calendar lesson detail:** In SF/BO Calendar lesson detail, show a Remote tag beside a student whose `Attendance_Status__c = Remote`, using the same priority logic.
- **AC 01.4 — Calendar legend:** Add a Remote legend entry with the assigned dot color.
- **AC 01.5 — SF Lesson Detail:** Display `Attendance_Status__c = Remote` as `Remote` (EN) / `リモート参加` (JP). The editable Attendance Status picklist includes Remote alongside existing values.
- **AC 01.6 — BO Student tab:** Display `Attendance_Status__c = Remote` as `Remote` (EN) / `リモート参加` (JP).
- **AC 01.7 — Learner lesson detail:** Display the new Attendance Status and Attendance Response values. Source wording says “Remote/Attend Remotely”.

### US 02 — View Remote Attendance Response

- **AC 02.1 — SF Lesson Detail:** Display `Attendance_Response__c = Attended Remotely` as `Attended Remotely` (EN) / `リモート参加` (JP).
- **AC 02.2 — BO Student tab:** Display `Attendance_Response__c = Attended Remotely` as `Attended Remotely` (EN) / `リモート参加` (JP).

### US 03 — Collect Attendance

- **AC 03.1 — New choice:** BO Lesson Detail > Collect Attendance includes a new remote-attendance radio choice. The AC uses `Remote` but its update note says `Attended Remotely`.
- **AC 03.2 — Persist:** Selecting Remote and saving persists `Attendance_Status__c = Remote`. In BO, selecting Remote shows the Attendance Reason selector so the user can choose a reason before saving. Attendance Notice behavior is not specified by this update; Attendance Note behavior remains the same as other statuses and can be edited.

### US 04 — Learner / Parent App Submit Attendance

- **AC 04.1 — New option:** App > Submit Attendance offers `Attended Remotely` (EN) / `リモート参加` (JP) alongside existing options.
- **AC 04.2 — Record submission:** A student or parent selection of Attended Remotely sets `Attendance_Response__c` on the corresponding `Student_Sessions__c`; existing remarks formatting remains.
- **AC 04.3 — Notification:** Send the current notification content to lesson teacher(s) and centre admin when Attended Remotely is submitted.

### US 05 — Pre-filled status after App submission

- **AC 05.1 — Auto-sync:** An App submission of Attended Remotely automatically sets Collect Attendance for the same `Student_Sessions__c` record to `Remote`, instead of the default Attend. After this Remote status is produced, Attendance Notice and Attendance Reason are not shown.

### Field and localization mapping

| Field / surface | English | Japanese | Behavior |
|---|---|---|---|
| `Attendance_Status__c` | Remote | リモート参加 | New picklist value; editable where attendance status is editable |
| `Attendance_Response__c` | Attended Remotely | リモート参加 | Displayed as `Option (Remark)` in SF and BO; latest submitted value wins |
| Lesson Card dot / legend | Remote | リモート参加 | Display indicator; stated token is Vibrant/Indigo/40 |
| App Submit Attendance | Attended Remotely | リモート参加 | Selectable response option |

---

## Business Rules (Extracted)

| # | AC | Business Rule | Field | Field Behavior | Platform |
|---:|---|---|---|---|---|
| 1 | AC 01.1 | Add Remote as a selectable Attendance Status value. | `Attendance_Status__c` | Editable picklist | SF / BO |
| 2 | AC 01.1 | Group card shows Remote if at least one session is Remote. | Attendance Status | Computed display trigger | SF / BO Calendar |
| 3 | AC 01.1 | Individual card shows Remote for that student's Remote session. | Attendance Status | Computed display trigger | SF / BO Calendar |
| 4 | AC 01.1 | Display only highest indicator: Remote > New > Trial > Seasonal > Reallocated > Absent. | Status indicator | Computed priority | SF / BO Calendar |
| 5 | AC 01.2 | No Remote dot if no relevant remote predicate is true; preserve other dots. | Remote dot | Computed / absent | SF / BO Calendar |
| 6 | AC 01.3 | Show Remote tag in Calendar lesson detail. | Attendance Status | Computed display | SF / BO Calendar |
| 7 | AC 01.4 | Add Remote legend entry using assigned color. | Calendar legend | Display-only | SF / BO Calendar |
| 8 | AC 01.5 | Show localized Remote and offer it in SF status picker. | `Attendance_Status__c` | Editable + localized | SF |
| 9 | AC 01.6 | Show localized Remote in BO Student tab. | `Attendance_Status__c` | Localized display | BO |
| 10 | AC 01.7 | App displays the values defined in the PRD: Status = Remote and Response = Attended Remotely. | Both attendance fields | Localized display | Learner / Parent App |
| 11 | AC 02.1 | Show localized Attended Remotely response in SF in `Option (Remark)` format. | `Attendance_Response__c` | Localized display | SF |
| 12 | AC 02.2 | Show localized Attended Remotely response in BO in `Option (Remark)` format. | `Attendance_Response__c` | Localized display | BO |
| 13 | AC 03.1 | Collect Attendance displays one new status choice labelled Remote. | Attendance Status | Editable radio option | BO |
| 14 | AC 03.2 | Saving Remote persists status; note editing behaves as existing statuses. | Status / Note | Persisted / editable | BO |
| 15 | AC 04.1 | Eligible App users can select Attended Remotely without changing the existing audience or eligibility configuration. | Attendance Response | Selectable | Learner / Parent App |
| 16 | AC 04.2 | Submission writes Attended Remotely in `Option (Remark)` format; the newest submitted value wins. | Attendance Response | App-written / persistent | App → shared data |
| 17 | AC 04.3 | Submission uses the existing PX suite 3276 attendance-notification flow: Notification Center and SF Chatter, lesson-teacher delivery, and centre-admin routing by lesson location/access scope. | Notification | System-triggered | App / notification service |
| 18 | AC 05.1 | App response automatically sets same session status to Remote; later valid updates use the newest value. | Attendance Status | System-written / auto-sync | App → BO Collect Attendance |
| 19 | AC 03.2 | When a user directly selects Remote in BO, Attendance Reason is shown and can be selected before saving. This supersedes the earlier BO hidden-field decision; no Attendance Notice behavior or stored-value-clearing behavior is inferred. | Attendance Reason | displayed and selectable when BO status is Remote | BO Collect Attendance |

---

## Conflict & Gap Analysis

### Conflicts with Existing System

| # | Tag | Source | AC | Description |
|---:|---|---|---|---|
| 1 | [EXTENDED] | Confirmed product decision | AC 01.1 / AC 01.2 | Calendar displays Remote whenever `Attendance_Status__c = Remote`, including a manual staff update; `Attendance_Response__c = Attended Remotely` is a separate response field. |
| 2 | [EXTENDED] | Confirmed product decision | AC 02.1 / AC 02.2 / AC 04.1 | `Attendance_Response__c` is displayed in `Option (Remark)` format in SF and BO. |
| 3 | [EXTENDED] | Confirmed product decision | AC 03.1 | BO Collect Attendance label is `Remote` and persists the Attendance Status value. |
| 4 | [EXTENDED] | `LT-107413-clear-attendance-fields/spec.md` | AC 01.5–01.7 | Remote joins the existing persisted SF → BO → Learner App Attendance Status read-back path. |
| 5 | [EXTENDED] | `calendar/student-teacher-reallocation-list.md` | AC 01.3 | Calendar detail already renders Student Session data; Remote tag is display-only and must not trigger assignment cascades. |
| 6 | [EXTENDED] | `PBT-3120-student-sort-bulk-mark-attendance/spec.md` | AC 01.1 | Remote extends the existing Renseikai Calendar indicator system without changing sort/localization behavior. |
| 7 | [EXTENDED] | `LT-96152-collect-attendance-entry-points-bo/spec.md` | AC 03.1 / AC 03.2 | Remote must work through every existing BO Collect Attendance entry point; existing Draft disabled behavior remains a regression guard. |
| 8 | [EXTENDED] | `LT-106349-submit-attendance-button-control.md` | AC 04.1 / AC 04.2 | Attended Remotely follows the existing Student/Parent audience configuration and lesson eligibility without change. |
| 9 | [EXTENDED] | Qase PX suite 3276 | AC 04.3 | Remote submission reuses the existing attendance-notification routing via Notification Center and SF Chatter. |

### Missing in Requirements

| # | Tag | Source | Description |
|---:|---|---|---|
| 1 | [EXTENDED] | Confirmed product decision | All impacted ACs | All users can view and update Remote status; no additional Renseikai permission/config gate is required. |
| 2 | [EXTENDED] | Confirmed product decision | AC 01.7 | Use the values and labels defined in the PRD; do not introduce a separate App-specific label contract. |
| 3 | [EXTENDED] | Updated PdM confirmation | AC 03.2 | When a user directly selects Attendance Status = Remote in BO, Attendance Reason is shown for selection. This supersedes the earlier BO hidden-field decision. Attendance Notice behavior and stored-value clearing are not specified. |
| 4 | [EXTENDED] | Confirmed product decision | AC 04.2 / AC 05.1 | For response/status updates, the newest valid submitted value wins. |

### Lesson-Learned Risks

| # | Incident | Date | AC | Risk | Guardrail |
|---:|---|---|---|---|---|
| — | No entity-and-operation match | — | — | All core/OOP incident entries concern assignment, duplication, or Lesson Allocation/points, not attendance updates on existing Student Sessions. | No historical-risk question generated; retain normal sync and idempotency coverage. |

### E2E Scenario Impact

| Scenario | Title | Impact | Action |
|---|---|---|---|
| E2E-01 | Lesson Lifecycle — Create, Teach, Report, View | Add App Remote response and same-session BO/calendar/mobile read-back. | UPDATE |
| E2E-17 | Renseikai — Attendance & Error Configuration | Add Remote collection, card/tag/legend priority, and unchanged Draft guard. | UPDATE |
| E2E-26 | Create Lesson — Recurrence Verification & End-to-End Lifecycle | Make its App attendance step cover Attended Remotely and Remote propagation. | UPDATE |
| E2E-35 | Automated Reports — Bulk Assign, Report Lifecycle & Mobile Attendance | Add exact option label and App-to-BO Remote sync coverage. | UPDATE |

### Assumptions Made

- This is Renseikai OOP scope because the Jira title and labels are Renseikai-specific; no separate feature-flag/config is required.
- `Remote` is the Attendance Status value; `Attended Remotely` is the Attendance Response value. A manual Remote status update also drives Calendar display.
- PdM updated the direct-BO behavior: selecting Remote in BO shows Attendance Reason for selection. This supersedes the earlier BO hidden-field decision. The update does not explicitly change the separate App auto-sync behavior, which remains covered independently.
- Existing Student Session assignment, Lesson Allocation, Lesson Report Detail, and Zoom-link behavior are not changed.
- The US 01 display requirements define the implementation behavior; Figma was retrieved via MCP, but rate limiting prevented deeper state extraction.

---

## Clarification Questions

> No open clarification questions. PdM updated the BO Remote rule via the user: show Attendance Reason for selection. This was not posted to Jira.

## Related Specs

- `epics/OOP/renseikai/LT-107413-clear-attendance-fields/spec.md` — attendance-field persistence and SF → BO / Learner App synchronization.
- `epics/lesson/LT-96152-collect-attendance-entry-points-bo/spec.md` — existing BO collect-attendance entry points and Draft guard.
- `epics/OOP/renseikai/LT-96662-publish-notify-student/spec.md` — Renseikai notification reliability and recipient safeguards.
- `epics/calendar/PBT-3120-student-sort-bulk-mark-attendance/spec.md` — Renseikai BO Calendar attendance context.

## Related Test Cases

- `epics/OOP/renseikai/LT-106349-enable-attendance-response-parent-app-only/test-cases/LT-106349-submit-attendance-button-control.md` — audience configuration and existing App attendance options.
- `epics/lesson/LT-96152-collect-attendance-entry-points-bo/test-cases/LT-96152-collect-attendance-entry-points.md` — BO entry-point and Draft-state assertions.
- `epics/OOP/renseikai/LT-107413-clear-attendance-fields/test-cases/sf-bo-attendance-sync.md` — existing attendance sync regression surface.
- Qase PX suite 3276 — existing attendance-notification routing and delivery assertions.

## QASE Coverage Gaps

- AC 01.1–01.4 — Remote dot/tag/legend, priority and no-Remote cases across group and individual lessons.
- AC 01.5–02.2 — exact EN/JP values and SF/BO persistence/read-back for both status and response.
- AC 03.1–03.2 — Remote selection and persistence across all BO entry points, Draft guard, dependent fields, and attendance note.
- AC 04.1–05.1 — add Remote variants to the unchanged audience-config matrix; assert latest-value-wins propagation to BO.
- AC 04.3 — reuse and extend Qase PX suite 3276 for Remote-specific notification routing, including teacher and centre-admin location/access boundaries.
