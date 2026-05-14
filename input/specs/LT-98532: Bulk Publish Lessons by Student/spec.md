# LT-98532: Bulk Publish Lessons by Student

**ID:** https://manabie.atlassian.net/browse/LT-98532
**Status:** In Development (sub-issues: LT-98543, LT-98554, LT-98560, LT-98561 = Done; LT-98562, LT-98563 = In Development)
**Analysis Date:** 2026-05-12

---

## Summary

Extends the existing SF Calendar Bulk Publish feature so staff can publish lessons for specific students (by applying a student filter on the calendar before triggering Bulk Publish). Adds a new "Apply to selected students" checkbox to the Bulk Publish modal that conditionally locks the location field. After publishing, a push notification is sent to all affected students and their parents (1 per-batch notification, deduplicated). A new Bulk Action Monitoring page (Riso-only, config-gated) tracks job records per student+location pairing with real-time status updates and a 2-week retention window.

---

## Acceptance Criteria

### US 01 — Bulk publish lesson of selected students

#### AC 01.1

Current Bulk Publish feature extended: users can filter by student in Calendar and activate 'Apply to selected students' checkbox in Bulk Publish modal.

#### AC 01.2

When **no student selected** in Calendar filter:

- 'Apply to selected students' checkbox is **DISABLED**
- User can bulk publish at calendar's location (default) or select more locations
- All validations unchanged

#### AC 01.3

When **1+ students selected** in Calendar filter:

- 'Apply to selected students' checkbox is **ENABLED** (but **unchecked by default** when modal opens)
- When checkbox **activated**: location field is **locked** to calendar's current location (disabled, read-only); user **cannot add extra locations** (multi-location selection disabled); scope narrows to selected students' lessons
- When checkbox **NOT activated**: all lessons at selected period published (existing behavior)
- All validations unchanged

> **Confirmed (Q5):** When checkbox is activated, location field shows calendar's location in disabled state. User cannot add extra locations while checkbox is active.
> **Confirmed (Q6):** The student filter **cannot be changed while the Bulk Publish modal is open**. User must close the modal first, then update the filter, then reopen. Checkbox state is always consistent with the filter state at modal open time.

#### AC 01.4

After filling required fields and saving:

- **Success message** shown; user redirected to previous calendar view
- Job runs **asynchronously** — lesson status NOT immediately reflected on calendar
- User must click **Refresh** on calendar to see updated lesson status
- **Publish logic:** Only Draft lessons updated to Published; Published/Completed/Cancelled lessons unaffected

---

### US 02 — Receive notifications when Lesson Schedule published

#### AC 02.1

**Trigger conditions (confirmed):**

- **Full success:** All lessons in the shortlist published → notifications sent to all affected students and parents
- **Partial failure ("Completed with Errors"):** Notifications ARE sent for the students of **successfully published lessons** only. Students with failed lessons are not notified. _(Confirmed Q2)_
- **0 Draft lessons in scope** (all already Published/Completed/Cancelled): **Job skips silently** — no notification fired, no user-facing warning. _(Confirmed Q3)_

**Cross-type deduplication (confirmed Q1):**

- Before sending a bulk notification for a lesson, the system **checks if that lesson was already published** (e.g., via LT-96662 per-lesson "Publish and Notify")
- If a lesson was already published and notified, it is **excluded from the bulk notification batch** — no duplicate notification sent
- Example: Lesson 1 published via LT-96662 → included in LT-98532 bulk period → system skips Lesson 1's notification

**Recipients (deduplicated):**

- **Students:** All students allocated to successfully published lessons — deduplicated across all Lesson Schedules in the action (1 notification per student)
- **Parents:** All parents of the deduplicated student list — 1 notification per parent regardless of how many of their children are affected

**Role gap — Student with no Parent Contact (confirmed Q9):**

- If a student has **no linked Parent Contact** (0 Relationship records), the **student is skipped entirely** — no notification sent to the student or parents

#### AC 02.2

- **Title:** "Lesson Schedule has been Published"
- **Body Line 1:** "Lesson schedules for the following period have been published"
- **Body Line 2:** Published period in format `Month Day, Year ~ Month Day, Year` (e.g., "March 1, 2025 ~ July 20, 2025")
- **Deep-link:** Calendar page in app at the **month** of the published start date, with the start date selected

---

### US 03 — Bulk Action Monitoring

#### AC 03.1

- **Config-gated:** "Bulk Action Monitoring config" (On = Riso, Off = other partners)
- **Permission-gated:** "Bulk Action Monitoring permission" for HQ or CM only
- **Record granularity:** Bulk Complete → 1 record per location; Bulk Publish → 1 record per student+location pairing
- **Default sort:** Created Time descending
- **Batch grouping:** All records from one user action share a Batch ID and are grouped together

#### AC 03.2

**Fields per record:** Job ID / Batch ID, ID, Action (Bulk Complete / Bulk Publish), Job Status, Location, Student (Bulk Publish only), Lesson Start Date, Lesson End Date, Total Lessons, Processed Count, Success, Failed, Created By, Created Time, Completed Time, Run Time.

#### AC 03.3

**Job statuses:** Pending → Processing → Completed / Completed with Errors / Failed

- **Processed Count** = Success Count + Failed Count
- Status auto-updates based on job outcome

#### AC 03.4

- If some lessons fail: **Failed Count** increments
- If all processed but some failed: Job Status = **Completed with Errors**
- If job terminates due to system error: Job Status = **Failed**

#### AC 03.5

**Data retention:** All job records auto-purged after 2 weeks.

#### AC 03.6

**Filters:** Action (default all), Job Status (default all), Created Date (this week default), Location (user's assigned locations). SF standard filtering capabilities only.

---

## Business Rules (Extracted)

| #   | AC      | Business Rule                                                                                                  | Field                               | Field Behavior                   | Platform |
| --- | ------- | -------------------------------------------------------------------------------------------------------------- | ----------------------------------- | -------------------------------- | -------- |
| 1   | AC 01.2 | Checkbox DISABLED when 0 students selected in Calendar filter                                                  | Apply to selected students checkbox | disabled                         | [SF]     |
| 2   | AC 01.2 | Location field editable; user can add multiple locations when checkbox disabled                                | Location field                      | editable (multi-select)          | [SF]     |
| 3   | AC 01.3 | Checkbox ENABLED when 1+ students selected in Calendar filter                                                  | Apply to selected students checkbox | enabled (not checked by default) | [SF]     |
| 4   | AC 01.3 | Location field LOCKED to calendar location when checkbox activated                                             | Location field                      | locked / read-only               | [SF]     |
| 5   | AC 01.3 | Existing publish-all-in-period behavior retained when checkbox NOT activated                                   | Bulk Publish modal behavior         | existing behavior                | [SF]     |
| 5a  | AC 01.3 | Checkbox is UNCHECKED by default when Bulk Publish modal opens (even with students in filter)                  | Apply to selected students checkbox | unchecked by default             | [SF]     |
| 5b  | AC 01.3 | User cannot modify the Calendar student filter while Bulk Publish modal is open; must close modal first        | Calendar student filter             | blocked while modal open         | [SF]     |
| 5c  | AC 01.3 | When checkbox activated: user cannot add extra locations (multi-location disabled)                             | Location field — extra locations    | disabled                         | [SF]     |
| 6   | AC 01.4 | Success message shown after submission                                                                         | Success message                     | informational                    | [SF]     |
| 7   | AC 01.4 | User redirected to previous calendar view after submission                                                     | Post-submit navigation              | auto-redirect                    | [SF]     |
| 8   | AC 01.4 | Job runs asynchronously — calendar not updated until Refresh clicked                                           | Lesson status on Calendar           | async / manual refresh           | [SF]     |
| 9   | AC 01.4 | User must click Refresh to see updated lesson statuses                                                         | Calendar Refresh button             | manual refresh required          | [SF]     |
| 10  | AC 01.4 | Only Draft → Published; Published/Completed/Cancelled lessons unaffected                                       | Lesson status transition            | Draft → Published only           | [SF]     |
| 11  | AC 02.1 | Notification sent after job completes for successfully published lessons                                       | Notification trigger                | post-completion                  | [Mobile] |
| 11a | AC 02.1 | Partial failure (Completed with Errors): notifications sent for successfully published students only           | Notification trigger — partial      | fires for successes only         | [Mobile] |
| 11b | AC 02.1 | 0 Draft lessons in scope: job skips silently, no notification fired                                            | Notification trigger — empty batch  | silent skip                      | [Mobile] |
| 11c | AC 02.1 | Cross-type dedup: if lesson was already published+notified via LT-96662, it is excluded from bulk notification | Notification deduplication          | cross-type dedup                 | [Mobile] |
| 12  | AC 02.1 | Notification recipients = all students allocated to published lessons (deduplicated across all LS)             | Notification recipient – Student    | unique list                      | [Mobile] |
| 13  | AC 02.1 | Parents of deduplicated students also receive 1 notification per parent                                        | Notification recipient – Parent     | deduplicated per parent          | [Mobile] |
| 13a | AC 02.1 | Student with no linked Parent Contact → student skipped entirely (no notification sent)                        | Notification recipient – no parent  | student skipped                  | [Mobile] |
| 14  | AC 02.2 | Title: "Lesson Schedule has been Published"                                                                    | Notification title                  | fixed text                       | [Mobile] |
| 15  | AC 02.2 | Body Line 1: "Lesson schedules for the following period have been published"                                   | Notification body Line 1            | fixed text                       | [Mobile] |
| 16  | AC 02.2 | Body Line 2: Published period in format "Month Day, Year ~ Month Day, Year"                                    | Notification body Line 2            | dynamic text                     | [Mobile] |
| 17  | AC 02.2 | Deep-link: Calendar at month of start date, start date selected                                                | Notification deep-link              | navigates to Calendar            | [Mobile] |
| 18  | AC 03.1 | Bulk Action Monitoring gated by config (On = Riso, Off = others)                                               | Config flag                         | feature-flag                     | [SF]     |
| 19  | AC 03.1 | Permission: "Bulk Action Monitoring permission" for HQ or CM only                                              | Permission                          | permission-guarded               | [SF]     |
| 20  | AC 03.1 | Bulk Publish: 1 record per student+location pairing                                                            | Job record granularity              | auto-created                     | [SF]     |
| 21  | AC 03.1 | Records from same batch grouped together (Batch ID)                                                            | Batch grouping                      | grouped by Batch ID              | [SF]     |
| 22  | AC 03.3 | Processed Count = Success Count + Failed Count                                                                 | Processed Count                     | auto-calculated                  | [SF]     |
| 23  | AC 03.4 | Job Status = "Completed with Errors" when Failed > 0 AND all lessons processed                                 | Job Status                          | auto-set                         | [SF]     |
| 24  | AC 03.4 | Job Status = "Failed" when system error terminates job before completion                                       | Job Status                          | auto-set                         | [SF]     |
| 25  | AC 03.5 | All job records purged after 2 weeks                                                                           | Job records retention               | auto-purged                      | [SF]     |

---

## Conflict & Gap Analysis

### Conflicts with Existing System

_No direct conflicts detected. The new feature extends (not replaces) existing Bulk Publish behavior. LT-96662 "Publish and Notify" boundary is explicitly maintained (bulk publish does not trigger that notification)._

### Missing in Requirements

| #   | Tag                                | Source                                      | Description                                                                                                                                                                                          |
| --- | ---------------------------------- | ------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | [MISSING BEHAVIOR → ✅ RESOLVED]   | temp/business_rules.json                    | AC 01.3: Extra locations + checkbox activation → **spec already defines this**: location field disabled, user cannot add extra locations when checkbox activated.                                    |
| 2   | [MISSING BEHAVIOR → ✅ RESOLVED]   | temp/business_rules.json                    | AC 01.3: Checkbox unchecked by default at modal open. User must close modal to update filter (filter locked while modal open).                                                                       |
| 3   | [MISSING BEHAVIOR → ✅ RESOLVED]   | temp/business_rules.json + AC 03.4          | AC 02.1 (Completed with Errors): **Notifications sent for successfully published students only.**                                                                                                    |
| 4   | [MISSING BEHAVIOR → ✅ RESOLVED]   | temp/business_rules.json                    | AC 02.1 (0 Draft lessons): **Job skips silently — no notification, no user-facing warning.**                                                                                                         |
| 5   | [MISSING BEHAVIOR]                 | temp/business_rules.json                    | AC 03.1: Sort order within a batch group not defined. Multiple student+location records in same batch — sub-sort by what field? _(Not confirmed — test based on Created Time, flag if inconsistent)_ |
| 6   | [MISSING BEHAVIOR]                 | temp/business_rules.json                    | AC 03.6: Location filter behavior for HQ Admin (system-wide access) — follows SF standard filtering. _(Not confirmed — follow system behavior)_                                                      |
| 7   | [UNDOCUMENTED IN AC → ✅ IGNORED]  | Figma node 6904-12827                       | AC 02.2: "Start date selected" on monthly calendar — treated as implementation detail, not tested explicitly.                                                                                        |
| 8   | [UNDOCUMENTED IN AC → ✅ RESOLVED] | raw_requirement.json figma_discrepancies    | AC 01.1: SF modal Figma not available — refer to Confluence spec page for UI definition.                                                                                                             |
| 9   | [ROLE GAP → ✅ RESOLVED]           | temp/domain_context.json data_relationships | AC 02.1: Student with no linked Parent Contact → **student skipped entirely** (no notification sent).                                                                                                |

### Regression Risks

| #   | Tag                              | Source                                | AC      | Description                                                                                                                                                                 |
| --- | -------------------------------- | ------------------------------------- | ------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | [REGRESSION RISK → ✅ NO ACTION] | output/test-cases/PX-2026-04-13.json  | AC 01.1 | 6 existing Qase Bulk Publish TCs (4624-4626, 4751-4753) do not account for new checkbox — **confirmed: no update needed** (Q4). New TCs will cover new behavior separately. |
| 2   | [REGRESSION RISK]                | lesson-status.md (TC-1469 to TC-1476) | AC 01.4 | Async job model may break test assertions that assume immediate calendar update. New TCs must include Refresh step; existing TCs may need guard note.                       |

### Lesson-Learned Risks

| #   | Incident                                     | Date       | AC      | Risk                                                                                                                   | Guardrail                                                                                                                                                |
| --- | -------------------------------------------- | ---------- | ------- | ---------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Aso — Duplicate Student Sessions (Dual-Path) | 2026-04-13 | AC 02.1 | LT-96662 per-lesson notification + LT-98532 bulk notification could both fire for the same student in the same period. | ✅ **RESOLVED (Q1):** System checks if lesson was already published+notified → excluded from bulk batch. Cross-type deduplication confirmed implemented. |

### E2E Scenario Impact

| Scenario  | Title                                                       | Impact               | Action                      |
| --------- | ----------------------------------------------------------- | -------------------- | --------------------------- |
| E2E-37    | [Renseikai] Publish Lesson and Notify Students              | Test isolation note  | NOTE (no structural change) |
| E2E-NEW-1 | [Riso] Bulk Publish lessons for Selected Students           | New flow             | CREATE                      |
| E2E-NEW-2 | [Riso] Mobile notification after Bulk Publish               | New flow             | CREATE                      |
| E2E-NEW-3 | [Riso] Bulk Action Monitoring — view and filter job records | New feature entirely | CREATE                      |

### Assumptions Made

- "Apply to selected students" checkbox is only available in SF (not BO — BO has no Bulk Publish Calendar access).
- "All validations unchanged" in AC 01.2 and 01.3 means existing date-range and location validations remain without modification.
- The Bulk Publish notification (LT-98532) and the Publish and Notify notification (LT-96662) are fully independent notification types with separate triggers; they do not share a common deduplication mechanism.
- "Shortlist" in AC 02.1 refers to the set of Draft lessons identified for publishing in the batch — already-Published/Completed/Cancelled lessons are excluded from the shortlist (consistent with BR #10).
- Bulk Action Monitoring is SF-only (not on BO or Mobile) based on the SF config/permission language in AC 03.1.

---

## Clarification Questions

> All 9 questions were answered directly in session. **No Jira post required.**

---

1. **[LESSON-LEARNED RISK → ✅ ANSWERED]** Based on the 2026-04-13 Aso incident (dual-path operations creating duplicate records), AC 02.1 introduces a new bulk notification path alongside the existing LT-96662 per-lesson 'Publish and Notify' path. The LT-96662 spec excludes bulk publish from triggering its notification — but the reverse is not guarded. If a lesson is individually published+notified via LT-96662 and the same period is then covered by a bulk publish, that student may receive both notifications. Has cross-type deduplication (between LT-96662 individual and LT-98532 bulk) been considered? Is dual notification acceptable, or is cross-type deduplication required?
   **Answer:** System checks if a lesson was already published. If Lesson 1 was published via LT-96662, it will NOT receive a bulk notification even if it falls within the LT-98532 batch period (already published + already notified).
   _Evidence: `input/domain-knowledge/scheduling/lesson-learned/core.md` — 2026-04-13 Aso dual-path pattern; `input/specs/LT-96662 Renseikai.../spec.md` — Out of Scope: one-directional exclusion only_

2. **[MISSING BEHAVIOR → ✅ ANSWERED]** AC 02.1 states notification fires "after all lessons in the shortlist published successfully." When the job completes as "Completed with Errors" (AC 03.4: some lessons fail, others succeed), should the notification: (a) fire for the students of successfully published lessons, (b) not fire at all, or (c) some other behavior? Not addressing this leaves students silently unnotified after a partial success.
   **Answer:** Notifications ARE sent for successfully published students. Students with failed lessons are not notified.
   _Evidence: `temp/business_rules.json` — Rule #11 trigger condition vs. Rule #23 "Completed with Errors" status_

3. **[MISSING BEHAVIOR → ✅ ANSWERED]** If all lessons in the selected period/student scope are already Published/Completed/Cancelled at execution time, the batch has 0 Draft lessons to publish. Should the notification fire (for 0 lessons)? Should the job skip silently, or show a user-facing warning?
   **Answer:** Job skips silently — no notification, no user-facing warning.
   _Evidence: `temp/business_rules.json` — Rule #10: only Draft → Published; AC 02.1 — no empty-shortlist coverage_

4. **[REGRESSION RISK → ✅ ANSWERED]** 6 existing Qase Bulk Publish test cases (4624, 4625, 4626, 4751, 4752, 4753) cover the existing modal. Can we confirm: (a) the new 'Apply to selected students' checkbox appears in ALL Bulk Publish modal variants (weekly view, daily view, teacher view), and (b) its state is determined solely by the Calendar student filter regardless of Calendar view mode? This is needed to correctly update all 6 existing test cases.
   **Answer:** Confirmed correct — checkbox appears in all modal variants (weekly, daily, teacher view), driven solely by the Calendar student filter. No need to update existing test cases.
   _Evidence: `output/test-cases/PX-2026-04-13.json` — 6 Qase cases without checkbox; AC 01.1 — does not specify which Calendar views include the checkbox_

5. **[MISSING BEHAVIOR → ✅ ANSWERED]** AC 01.3: If a user has already added multiple extra locations to the Bulk Publish form, then activates the 'Apply to selected students' checkbox (which locks location to calendar default) — what happens to the extra locations already entered? (a) auto-cleared and location reverts, (b) checkbox activation blocked until extra locations removed, (c) other?
   **Answer:** Already defined in spec — user cannot select multiple locations when checkbox is activated. Location field shows calendar's location in disabled state.
   _Evidence: `temp/business_rules.json` — Rule #2: multi-location allowed when checkbox disabled; Rule #4: location locked when checkbox activated — no transition defined_

6. **[MISSING BEHAVIOR → ✅ ANSWERED]** AC 01.3: Two sub-states are undefined: (a) when the Bulk Publish modal opens with students in the filter, is the checkbox unchecked by default? (b) if checkbox is activated and user then removes all students from the Calendar filter without closing the modal — does the checkbox auto-disable+uncheck, or stay activated?
   **Answer:** User must close the modal first before updating the student filter. Checkbox cannot be changed independently of the filter outside of closing+reopening the modal.
   _Evidence: `temp/business_rules.json` — Rules #1, #3, #4 cover static states but not default check-state or dynamic mid-session filter changes_

7. **[UNDOCUMENTED IN AC → ✅ IGNORED]** AC 02.2 states the deep-link opens "Calendar page at the month of the published start date, with the start date selected." Figma (node 6904-12827) shows a monthly calendar with a date appearing highlighted. What exactly does "start date selected" mean in the monthly calendar UX — is the date highlighted in the grid, does it trigger navigation to the weekly view at that date, or is it a Figma prototype artifact?
   **Answer:** Ignore — treat as implementation detail. Not tested explicitly.
   _Evidence: `temp/raw_requirement.json` — figma_discrepancies: "meaning of 'default selected' on monthly calendar view not formally defined in AC"_

8. **[UNDOCUMENTED IN AC → ✅ ANSWERED]** No Figma designs are available for the SF Bulk Publish modal with the new 'Apply to selected students' checkbox. Can design assets be provided — specifically: the checkbox's position in the modal, its label text, and the visual distinction between disabled/enabled states?
   **Answer:** Check UI in the Confluence spec page (https://manabie.atlassian.net/wiki/spaces/PRDM/pages/2127724545).
   _Evidence: `temp/raw_requirement.json` — figma_discrepancies: "No Figma provided for SF side. SF UI changes are undocumented in designs."_

9. **[ROLE GAP → ✅ ANSWERED]** AC 02.1 defines notification recipients as students and "their parents." Domain knowledge confirms Student → (1:N) ParentContact — meaning 0 parents is a valid state. When a student has no linked Parent Contact in SF: (a) student is still notified, parents gracefully skipped, (b) student is skipped entirely, or (c) system error?
   **Answer:** Confirmed with PM — student skipped entirely (no notification to student or parents).
   _Evidence: `temp/domain_context.json` — data_relationships: "Student → (1:N) ParentContact via Relationship"; Rule #13: no clause for 0-parent case_

---

## Related Specs

- `input/specs/LT-96662 Renseikai Receive notifications when a new lesson is published/spec.md` — Per-lesson "Publish and Notify" feature; explicitly out of scope for bulk publish but relevant for dual-notification risk analysis

## Related Test Cases

- `output/test-cases/PX-2026-04-13.json` (Qase 4624-4626, 4751-4753) — Existing Bulk Publish TCs needing new checkbox assertions (**high impact**)
- `output/test-cases/lesson-management/lesson/lesson-status/lesson-status.md` (TC-1469 to TC-1476) — Bulk status change from Lesson List; may need async assertion guard
- `output/test-cases/lesson-management/lesson/publish-notify-student/send-notification.md` — Individual notification TCs (LT-96662 scope); check test isolation from bulk notification
- `output/test-cases/lesson-management/lesson/publish-notify-student/notification-recipients.md` — Recipient logic TCs; similar patterns apply to bulk notification recipients

## QASE Coverage Gaps

- AC 01.1-01.3 — No existing test case covers "Apply to selected students" checkbox in Bulk Publish modal (neither enabled/disabled state nor activated behavior)
- AC 01.4 — Async job behavior + manual Refresh requirement: no existing TC
- AC 02.1-02.2 — Bulk publish notification (title, body, deep-link, deduplication): no existing TC
- AC 03.1-03.6 — Entire Bulk Action Monitoring feature: no existing TC
