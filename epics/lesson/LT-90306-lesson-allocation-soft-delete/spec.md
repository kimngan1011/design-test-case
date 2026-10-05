---
ticket_id: LT-90306
ticket_url: https://manabie.atlassian.net/browse/LT-90306
title: "[Scheduling] Refactoring LA soft deletion flow"
module: scheduling
bucket: lesson
status: Ready for QA
internal_uat_date: null
production_release_date: null
last_updated: 2026-10-05
---

# LT-90306: Lesson Allocation Soft Delete (Archive) Refactor

## Summary

`Lesson_Allocation__c` (LA) is no longer hard-deleted when its `Student_Package_Order__c` (SPO) records are removed. It is **archived**: `Archived_At__c` is stamped with the current time instead of the record being deleted. `Student_Sessions__c` and Salesforce `Class_Member__c` require no child write in the archive transaction — their `Is_Archived__c` is a formula reading the parent `Lesson_Allocation__r.Archived_At__c`, so they flip state the instant the parent archives/unarchives. The Backend then handles its native class-member projection using the `sf_class_member` soft-delete signal and the guard documented below. When a living SPO reappears for the same `Student_Course_ID__c` group, the **same** LA record (same Id) is rebuilt and unarchived — existing `Student_Sessions__c` and attendance history survive instead of being recreated. The whole mechanism is gated by `Lesson_Custom_Settings__c.Enable_Lesson_Allocation_Archive__c` (`FALSE` = legacy hard-delete, preserved byte-for-byte for rollback safety).

The archive lifecycle originates in the Salesforce managed package, whose in-package read paths filter archived records out. Backend (Go) has a defined class-member projection contract (AC-2a/AC-3a); its remaining LA/session read-path gaps are tracked below. Other surfaces — Back Office, OOP partner customizations (Nichibei, EEA, Aver, Riso), partner REST API consumers, and org-owned Salesforce reports/dashboards/page layouts — were audited separately and several still have no committed fix.

**Primary sources for this spec:**
- Confluence: [Draft Lesson Allocation Soft Delete](https://manabie.atlassian.net/wiki/spaces/TECH/pages/2883354639/Draft+Lesson+Allocation+Soft+Delete) (page still in Draft status, version 39, impact audit dated 2026-09-25).
- Jira description links to a Google Doc (`docs.google.com/document/d/15Er0YmteZR4MU3MNd1A7zGli77O0bPD-uBK6u7OIH7A`) not accessible from this environment (no Drive connector authorized) — treat as a secondary source to reconcile once available.
- Direct code verification in `erp-salesforce` (`LessonAllocationSyncService.cls`, `StudentPackageOrderHandler.cls`, `LessonFeatureToggles.cls`) and `school-portal-admin`.
- A prior Codex analysis session (local, `~/.codex/sessions/.../01a0f5b4-...jsonl`) that additionally traced the `backend` (Go) repo, surfacing gaps not present in the Confluence audit.
- Backend class-member handling clarification supplied by Engineering (2026-10-05): `sf_class_member` soft delete, guarded native `class_member` deletion, and unarchive recreation by `(student, course, academic year)`.

---

## Acceptance Criteria

| ID | Requirement |
|---|---|
| AC-1 | When every `Student_Package_Order__c` sharing a `Student_Course_ID__c` is removed (hard-deleted, or `DeletedAt__c` set, or both `Start_Date_Time__c`/`End_Date_Time__c` null) **and** the LA is still alive, the LA is archived: `Archived_At__c` = current timestamp. One order still alive in the group → nothing happens. Out-of-scope package types (`PACKAGE_TYPE_MONTHLY`) are skipped. Archive is idempotent (re-archiving keeps the original timestamp). |
| AC-2 | The Salesforce archive transaction performs exactly one DML: update `Lesson_Allocation__c.Archived_At__c`. `Student_Sessions__c` and Salesforce `Class_Member__c` are not child-written in that transaction; their `Is_Archived__c` formula (`NOT(ISBLANK(Lesson_Allocation__r.Archived_At__c))`) reflects the parent state instantly, both directions. Backend projection handling is specified separately in AC-2a/AC-3a. |
| AC-2a | When `sf_class_member` is soft-deleted, Backend deletes the corresponding native `class_member` **only if** the student has no other `sf_class_member` with the same `(student, course, academic year)` key. If another matching SF class member exists, the native `class_member` is retained. |
| AC-3 | When at least one SPO in the group becomes alive again and resolves to an existing `Course_Offering__c` + student `Contact`, the **same** LA Id is rebuilt from the representative order (earliest living order with both dates) and `Archived_At__c` is cleared. `Start/End_Date_Time__c`, `Purchased_Slot_Number__c`, `Week_Range__c` are recomputed from all living orders; a removed order can't pull the start earlier or push the end later. A LA hard-deleted by the legacy flow and still in the Recycle Bin is undeleted and refreshed in the same run, same Id. |
| AC-3a | On SF unarchive, Backend clears `sf_class_member.deleted_at` and sets `updated_at = now()`. If the prior native `class_member` was deleted, Backend inserts a new native `class_member`; the existence/deletion decision uses the same `(student, course, academic year)` key. It must not create a duplicate active native membership. |
| AC-4 | After unarchive, exactly one `Student_Sessions__c` per (student, `Lesson__c`) is enforced: sessions restored by unarchive are walked by `CreatedDate ASC`; if another active allocation already holds the same (student, lesson) key, the restored session is **detached** (`Lesson__c = null`, `Assigned_Lesson__c = false`, `Lesson_Report__c = null`) — never deleted — so it can be reassigned manually. Failures are logged to `Sync_History__c`. |
| AC-5 | Every read path inside the managed package excludes archived records: `Lesson_Allocation__c` → `Archived_At__c = NULL`; `Student_Sessions__c` / `Class_Member__c` → `Is_Archived__c = FALSE`. Scope: Lesson calendar + attendance list, reallocation list, student group, teacher timesheet, grade book, student app lesson booking, internal sync monitor. Archived records remain reachable by direct record Id and by report filter `Archived_At__c != NULL`. |
| AC-6 | The add-student popup on `Lesson__c` is **deliberately unfiltered** — it must keep showing a student who already has a `Student_Sessions__c` (even archived) as already assigned, to avoid re-adding and violating `Student_Sessions__c.Unique_Key__c`. |
| AC-7 | `Lesson_Custom_Settings__c.Enable_Lesson_Allocation_Archive__c = FALSE` must reproduce the legacy hard-delete flow exactly (parity), with no behavior change, as the rollback path. |
| AC-8 | Archive must succeed even when the LA's data would otherwise fail validation (archive is a pure timestamp write and must not be blocked by business validation rules). |

### Scope exclusions

- **Riso manual LA** (create/edit via the popup on the Student Course Subscription tab) does not go through SPO/Core order sync and is therefore **not** archived by this lifecycle — its own manual **Delete** button still hard-deletes and is explicitly out of scope for this epic (tracked as an open gap below, not a regression of this change).
- Riso Contract API (`LT-98533`) and Riso Lesson API (`LT-110368`) already carry their own archived/deleted exclusion guards in their own specs, independent of this epic — only a shared-query regression check is in scope here, not new aggregation logic.
- Native backend allocation objects unrelated to Salesforce sync (e.g. `lesson_student_subscriptions` in Postgres, if used as an independent domain) are out of scope unless confirmed to require the same semantics.

---

## Feature Impact Analysis

Feature-level impact pass across the workspace's existing test design, split into Core (shared SF → BO → Mobile flow) and OOP (partner-gated behavior), run after the archive/unarchive/dedup baseline above was confirmed. Risk is framed the same way throughout: **the biggest risk is not LA archive failing — it's a child record that still exists while some read path only filters `DeletedAt`/`Is_Deleted` instead of `Is_Archived`**, so the system keeps showing a student/class member/session as active in BO, Mobile, attendance, booking, or point consumption even though the LA has been archived.

### Core

| Feature impact | Severity | What must hold |
|---|---:|---|
| Order/SPO lifecycle: Cancel, Void, Change Course, Add Course, Withdrawal, LOA, Resume, reprocess | Critical | Archive the whole LA group by `Student_Course_ID__c`; unarchive must restore the exact same record; no duplicate LA/Class Member/Student Session created. Feature flag OFF must still hard-delete exactly as before. |
| LA authorization & Add Student | Critical | Archived LA must not appear in Add Student, Calendar, BO/SF lesson detail, or CSV/import candidate lists. `Lesson Allocated` count, Status, and Report History must not count it as active. |
| Student Session lifecycle | Critical | Sessions under an archived LA must not be shown, attended, reallocated, or removed via active-session flows, or appear in BO/Mobile — but attendance/report history must remain so it can be restored. Existing auto-delete test expectations need updating. |
| Class Assignment / Master Queue | Critical | On `sf_class_member` soft delete, Backend deletes native `class_member` only when no other SF class member shares `(student, course, academic year)`; otherwise it retains the native membership. On SF unarchive it clears `sf_class_member.deleted_at`, updates `updated_at`, and recreates native `class_member` only when the prior native record was deleted. Test both paths and ensure no duplicate active membership. Directly affects the triggers covered in `LT-107255-order-group-class-assignment`. |
| Attendance, Lesson Report, Report Detail | High | Must block attendance/report edits on archived sessions. `Lesson_Report_Detail__c` does not auto-archive with its parent LA, so an explicit filter/read-policy is required — otherwise a report can still be exposed via API after the student has been archived. |
| SF / School Portal / BO / Mobile read paths | Critical | Every lesson list, student list, calendar, lesson detail, report, and media query must exclude `Is_Archived` — a cross-system (SF → BO → Mobile) concern, not a Salesforce-only change. |
| Reallocation, Zoom participant, Lesson Schedule Student | High | The old hard-delete cleaned these child records via a `BEFORE_DELETE` trigger; archive (an `UPDATE`) never runs that trigger. A decision is needed: keep them for restorability but exclude from operational flows, or run a dedicated cleanup — otherwise orphaned reallocation requests / Zoom participants / schedule-students accumulate. |
| Native backend Class Member sync | Critical | Backend implements archive propagation through `sf_class_member.deleted_at`, with a membership guard keyed by `(student, course, academic year)` rather than a new `is_archived` field. A guarded delete prevents an unrelated active SF membership from removing the native record; unarchive refreshes the SF projection and recreates the native record only when needed. |

Domain-knowledge / epic files needing the most updates for this re-baseline: `knowledge/domain-knowledge/scheduling/lesson-management/lesson-allocation.md`, `student-session.md`, `class-assignment.md`, and `epics/lesson/LT-107410-auto-delete-student-sessions/spec.md` (currently expects "deleted"; needs to distinguish "removed normally" from "hidden because the parent LA was archived").

### OOP / Partner-Specific

| Partner feature | Severity | Impact |
|---|---:|---|
| Nichibei Point Consumption | Critical | LA is the financial authorization record. An archived LA must not be selected in the priority chain or have points consumed from it. Must decide whether archived-period sessions get refunded, and must not double-consume on unarchive. A past incident already produced sessions with no LA and incorrect point totals (see Lesson-Learned Risks). |
| Nichibei Lesson Booking | Critical | Booking-candidate selection must only consider non-archived LA. A student must not be able to book using an archived LA; old bookings/sessions must disappear from the Booking List / Collect Attendance. Unarchive must not silently recreate a booking or resend a notification. |
| Nichibei Reallocation | High | Reallocation requests (source/target session) must ignore archived LA/sessions; must not complete a request against an already-archived record or double-count points after restore. |
| Riso Manual LA / CSV import | High | Riso LA is created manually, independent of Order/SPO, and currently has its own hard-delete for future LA. The Core SPO archive behavior must not be silently applied to this flow (see Scope exclusions). If Riso is ever brought into scope, it needs its own archive design preserving the "synchronous unlink from lesson" rule. |
| Riso Contract API, LA aggregation, reports | High | APIs/reports must filter archived LA, otherwise Total Session Count, monthly reports, or contract history could still count archived allocations. Already partly guarded by `LT-98533`/`LT-110368` — treat as a regression check, not new logic. |
| Renseikai attendance / remote attendance / custom Student Session table | Medium–High | These screens read Student Session directly. Archived sessions must not appear in the Calendar tag, Collect Attendance, app attendance response, or notifications — and attendance history must not be lost on unarchive. |
| Withus direct class assignment | Medium | Has its own custom Class Member flow; needs confirmation that every query/class-assignment job excludes `Is_Archived`, especially memberships with a past effective date. |

Direct OOP sources: `knowledge/domain-knowledge/scheduling/partner-rules/nichibei-lesson-allocation.md`, `nichibei-lesson-booking.md`, `riso-lesson-allocation.md`, and `knowledge/domain-knowledge/scheduling/lesson-learned/oop.md`.

---

## Business Rules (Extracted)

| # | AC | Business Rule | Field | Field Behavior | Platform |
|---:|---|---|---|---|---|
| 1 | AC-1 | Archive only when **every** SPO in the `Student_Course_ID__c` group is removed. | `Lesson_Allocation__c.Archived_At__c` | set to now() | SF |
| 2 | AC-1 | `PACKAGE_TYPE_MONTHLY` is excluded from archive/unarchive eligibility entirely. | `Package_Type__c` | skip | SF |
| 3 | AC-2 | Salesforce child objects are not written during the LA archive transaction; their archived state is formula-derived. | `Student_Sessions__c.Is_Archived__c`, `Class_Member__c.Is_Archived__c` | read-only formula | SF |
| 3a | AC-2a | Soft-deleting `sf_class_member` deletes native `class_member` only when no other SF member remains for the same student, course, and academic year. | `sf_class_member.deleted_at`, native `class_member` | guarded delete / retain | Backend (Go) |
| 4 | AC-3 | Unarchive reuses the existing LA Id; no new record is created. | `Lesson_Allocation__c.Id` | unchanged | SF |
| 4a | AC-3a | Unarchive clears the SF class-member soft-delete marker and refreshes it; native membership is recreated only if its prior record was deleted. | `sf_class_member.deleted_at`, `sf_class_member.updated_at`, native `class_member` | `NULL`, `now()`, conditional insert | Backend (Go) |
| 5 | AC-3 | A removed order can't extend the rebuilt LA's duration beyond what living orders support. | `Start_Date_Time__c` / `End_Date_Time__c` | recomputed from living orders only | SF |
| 6 | AC-4 | Duplicate (student, lesson) pair after unarchive → newer-created session is detached, not deleted. | `Student_Sessions__c.Lesson__c` | set to null | SF |
| 7 | AC-5 | All in-package read surfaces exclude archived rows by default. | `Archived_At__c` / `Is_Archived__c` | `= NULL` / `= FALSE` filter | SF |
| 8 | AC-6 | Add-student popup intentionally does not apply the archive filter. | — | unfiltered by design | SF |
| 9 | AC-7 | Feature flag off reproduces legacy hard-delete exactly. | `Enable_Lesson_Allocation_Archive__c` | `FALSE` → legacy path | SF |
| 10 | Gap | `Lesson_Report_Detail__c`, `Lesson_Schedule_Student__c`, `Enrollment__c`, `Zoom_Participant__c`, `Reallocation__c` carry no archived state and are not touched by archive — only the old `BEFORE_DELETE` cascade cleaned these, and that cascade does not run on archive (an `UPDATE`). | — | unchanged, no archive signal | SF |
| 11 | AC-2a | Backend does not introduce an `is_archived` field for native `class_member`; it consumes `sf_class_member.deleted_at` and uses the `(student, course, academic year)` guard before deleting the native record. | `sf_class_member.deleted_at`, native `class_member` | delete only when no sibling SF membership exists | Backend (Go) / Postgres |
| 12 | AC-3a | Backend unarchive clears `sf_class_member.deleted_at`, stamps `updated_at`, and conditionally recreates the native membership by the same key. | `sf_class_member.deleted_at`, `sf_class_member.updated_at`, native `class_member` | restore SF projection; conditional insert | Backend (Go) / Postgres |

---

## Conflict & Gap Analysis

### Conflicts with Existing System

| # | Tag | Source | AC | Description |
|---:|---|---|---|---|
| 1 | [CONFLICT — NEEDS UPDATE] | `knowledge/e2e-scenario/e2e-scenarios.md` E2E-09 step 6/9, E2E-10 steps 1/3/5 | AC-1, AC-3 | These scenarios currently read "Old LA deleted" / "LA deleted" / "LA re-created" for Change Course, Void, Cancel LOA, Void Add Course. With the flag ON, the correct language is "LA archived" (same Id, recoverable) and "LA unarchived" (same Id, not a new record) — existing wording and any test case asserting record absence vs record presence-with-`Archived_At__c` will diverge. |
| 2 | [CONFLICT — SCOPE] | Confluence Impact table, "Riso" row vs Codex re-analysis (2026-10-01 06:20) | Scope exclusions | The Confluence audit lists "Riso" as an open impact row for the *manual LA Delete button still hard-deleting*. A separate, more specific finding (Riso Contract/Lesson API aggregation) was initially flagged then **retracted** after confirming Riso manual LA doesn't go through SPO sync. Both statements are kept in this spec as distinct: the manual-delete-button gap stands; the aggregation-API gap does not. |

### Regression Risks and Extensions

| # | Tag | Source | AC | Description |
|---:|---|---|---|---|
| 1 | [REGRESSION RISK] | Lesson-learned `core.md` — [2026-08-19] Renseikai manual-session auto-removal incident | AC-4 | The existing class-assignment re-scan already has a known history of sweeping up manually-assigned sessions it shouldn't touch (916 records incorrectly removed). The new unarchive de-duplication logic (AC-4) is a **second, independent** path that detaches sessions based on `(Lesson__c, Student__c)` key collision — it must be verified against manually-assigned sessions specifically, since the same class of bug (auto-logic silently touching manual assignments) has already occurred once in this domain. |
| 2 | [REGRESSION RISK] | Codex backend trace, 2026-10-01 04:45 | AC-5 (backend equivalent) | Backend API `GetStudentsByLessonID` reads `Student_Sessions__c` without filtering `Is_Archived__c`/`Is_Deleted__c` — used by Student App's Calendar feature to list lesson members. Archived-LA students can still appear as lesson members on mobile. |
| 3 | [REGRESSION RISK — HIGH] | Codex backend trace, 2026-10-01 04:45 | AC-5 (backend equivalent) | Backend API `RetrieveLessonReportMedias` reads session-by-lesson-and-student without an archive filter **and** selects `records[0]` with no `ORDER BY`. If both an active and an archived session exist for the same (lesson, student), the wrong session's report/media can be returned non-deterministically. |
| 4 | [REGRESSION RISK] | Confluence §2.1 org-reports audit, 2026-09-25 | AC-5 (out-of-package) | 77 Salesforce report types / 1,320 reports (810 run in the last 90 days) / 24 dashboards across 14 production orgs do not filter `Archived_At__c`/`Is_Archived__c` — all keep counting archived LA/session/class-member rows. Not fixable by this epic's code; needs a separate report-remediation pass. |
| 5 | [EXTENDED] | Confluence §3.1–3.4 | AC-1–AC-4 | Core archive/unarchive/dedup behavior is net-new relative to existing "LA deleted on cancel" coverage in E2E-09/E2E-10 and needs dedicated new test cases, not just wording edits (see Missing in Requirements). |

### Missing in Requirements

| # | Tag | Source | Description |
|---:|---|---|---|
| 1 | [BEHAVIOR CLARIFIED — TEST REQUIRED] | Engineering clarification, 2026-10-05 | Backend deliberately does **not** add `is_archived` to native `class_member`. It consumes `sf_class_member.deleted_at`: delete native `class_member` only when there is no other `sf_class_member` with the same `(student, course, academic year)`; retain it otherwise. This supersedes the earlier claim that archive must never map to deletion. |
| 2 | [BEHAVIOR CLARIFIED — TEST REQUIRED] | Engineering clarification, 2026-10-05 | On SF unarchive, Backend sets `sf_class_member.deleted_at = NULL` and `updated_at = now()`. It inserts native `class_member` only when the previous native record was deleted for the same `(student, course, academic year)` key; duplicate active memberships are not allowed. |
| 3 | [MISSING BEHAVIOR — OPEN, TICKETED] | Confluence Impact table | Backend still needs to decide which *other* reads must exclude archived LA. Ticket: `[BE] Check archived lesson allocation scope` — 1d. This includes the two concrete API findings (`GetStudentsByLessonID`, `RetrieveLessonReportMedias`), but not the class-member propagation contract above. |
| 4 | [MISSING BEHAVIOR — OPEN, TICKETED] | Confluence Impact table | Nichibei: LA now survives void/cancel instead of being deleted, but consumed points vs billing reconciliation for the archived period is undefined. Ticket: `[SF][Nichibei] Implement LA soft delete with consume point` — 3d. |
| 5 | [MISSING BEHAVIOR — OPEN, TICKETED] | Confluence Impact table | EEA's custom `Student_Sessions__c` table lives outside the package; package filters don't reach it. Ticket: `[SF][EEA] Check custom Student Session table` — 1d. |
| 6 | [MISSING BEHAVIOR — OPEN, TICKETED] | Confluence Impact table | Aver's custom lesson report lives outside the package; same gap. Ticket: `[SF][Aver] Check custom aver lesson report` — 4h. |
| 7 | [MISSING BEHAVIOR — OPEN, NO TICKET] | Confluence Impact table | Riso manual LA's own **Delete** button (Student Course Subscription tab popup) still hard-deletes `Student_Sessions__c` + attendance. No ticket filed yet. |
| 8 | [MISSING BEHAVIOR — OPEN, CANNOT FIX SERVER-SIDE] | Confluence §2.2 Postman audit | Partner REST API consumers (WithUs Juku, Kyoiku, Riso UAT, and others) query `Lesson_Allocation__c`/`Student_Sessions__c`/`Class_Member__c` with partner-owned queries that don't filter archived rows. We can only update sample Postman requests and notify partners — cannot force a fix. Ticket: `[SF] Check Partner REST API / Postman collection` — 4h. |
| 9 | [MISSING BEHAVIOR — OPEN, TICKETED] | Confluence Impact table | 1 org page layout + 15 Lightning record pages (5 on LA/Session, 10 on related objects) still surface archived rows via related lists; `Archived_At__c` isn't on any layout. Ticket: `[SF] Check Custom page layouts and related lists` — 4h. |
| 10 | [MISSING BEHAVIOR — UNVERIFIED] | Codex backend trace, 2026-10-01 04:45 | Student App's points-consumption screen calls a generic Salesforce proxy (`/lessonAllocation/v2/getPointsConsumption`) whose Apex endpoint was not found in the current `erp-salesforce` source — ownership and archive-filter behavior for this endpoint are unverified. |
| 11 | [MISSING BEHAVIOR — NOT TRACKED ANYWHERE] | Direct repo check (no purge batch found for `Archived_At__c` in `erp-salesforce`) | There is no retention/purge job for archived `Lesson_Allocation__c` records. Previously hard-delete freed storage; now archived records accumulate indefinitely, a Salesforce storage-limit risk with no owner or ticket. |
| 12 | [MISSING BEHAVIOR — DRAFT INCOMPLETE] | Confluence §4 "Need to confirm" | The spec's own "Need to confirm" section lists two open items ("Duplicated students", "UI lesson allocation detail") with only screenshots attached and no written description — the source document itself is not fully resolved. |
| 13 | [MISSING BEHAVIOR — NO DEFENSE IN DEPTH, UNTICKETED] | Direct repo check, 2026-10-01: `StudentSessionsHandler.cls:119-154` (`addStudentSessionToSingleLessonV2`) and `:1844` (`upsertStudentSession`) | The only protection against assigning a student to a lesson using an archived Lesson Allocation is at the UI picker layer (`LessonAllocationHandler.cls:92`, `WHERE Archived_At__c = NULL`) — the student simply doesn't appear in the Add Student search results. The actual `Student_Sessions__c` insert methods behind that picker perform **no re-check** of `Archived_At__c` on the `Lesson_Allocation__c` they're given. If an archived `lessonAllocationId` reaches either method through any other entry point (a different LWC modal, a future API, an automation script, Platform Import, or a picker bug), the record is created silently with no error. Not reliably exercisable through the standard manual-QA UI path today — flagged as an architecture gap for dev/unit-test coverage rather than a Qase manual test case. |
| 14 | [MISSING BEHAVIOR — DATA INTEGRITY, UNTICKETED] | Direct repo check, 2026-10-01: `LessonAllocationSyncService.cls:1408-1431` (`SoqlLessonAllocationReader.findAllocationsByStudentCourseIdIncludingRemoved`) + `Lesson_Allocation__c.Student_Course_ID__c` field metadata (`unique = false`, `externalId = false`) | `MasterDataSnapshot.allocationsByStudentCourseId` is a strict one-to-one `Map<String, Lesson_Allocation__c>` keyed by `Student_Course_ID__c`, which has **no uniqueness constraint** at the schema level. If two `Lesson_Allocation__c` records ever share the same `Student_Course_ID__c` (data quality issue, migration artifact, or a re-enrollment reusing an old Id), the builder query's tie-break (`ORDER BY Student_Course_ID__c, Archived_At__c ASC NULLS FIRST, IsDeleted, CreatedDate DESC`, first-row-wins) deterministically favors a non-archived record over an archived one — so an active allocation is **not** at risk of being wrongly archived by this ambiguity. However, the losing duplicate (whichever record doesn't win the tie-break) becomes permanently invisible to the entire archive/unarchive/create sync engine: it is never archived, never unarchived, and never updated by `LessonAllocationSyncService` again, while other read paths that don't share this dedup logic may still display it — a latent, silent data-integrity risk with no detection mechanism. Not easily reproducible through normal UI flows (requires an actual duplicate `Student_Course_ID__c` to already exist); best suited to a data-script or unit-level test rather than manual QA. |

### Lesson-Learned Risks

| # | Incident | Date | AC | Risk | Guardrail |
|---:|---|---|---|---|---|
| 1 | Renseikai — Manually-Assigned Student Sessions Auto-Removed by Class-Assignment Re-Scan Logic ([LT-109020](https://manabie.atlassian.net/browse/LT-109020)) | 2026-08-19 | AC-4 | Auto-logic that removes/detaches sessions based on scan rules has already incorrectly swept up manually-assigned sessions once in this domain (916 records). The new de-duplication-after-unarchive logic is a structurally similar auto-detach path. | Explicitly test de-duplication against a manually-assigned session colliding with a restored one; assert the manual session is never silently detached unless it is genuinely the newer-created duplicate per the `CreatedDate ASC` rule. |
| 2 | Nichibei — Student Sessions Missing LA → Points Not Deducted | 2026-03-04 | Gap #4 (Missing in Requirements) | A prior incident already showed that LA/SPO sync gaps directly cause financial errors (145 lessons / 27 students affected, consumed points not deducted or LA itself gone). The design note from that incident — "before deleting/changing an LA via system logic, check if any lessons are still linked" and "any Core SPO sync improvement must also reach the Nichibei flow" — applies directly to this archive refactor, since Nichibei's point-consumption handling for archived LA is still an open, undefined gap. | Do not sign off QA for Nichibei until the consumed-points behavior for an archived LA (and for an unarchived one) is explicitly specified and tested; treat this as a release blocker for the Nichibei rollout of the flag, not just a documentation gap. |

### E2E Scenario Impact

| Scenario | Title | Impact | Action |
|---|---|---|---|
| E2E-09 | Lesson Allocation — New Order, Change Course & Void | Steps 6 and 9 currently say "Old LA deleted" / "Old LA re-created" for Change Course and its Void. With the flag ON, update to "Old LA archived" (same Id) / "Old LA unarchived (same Id, not re-created)", and add an assertion that `Student_Sessions__c`/attendance under the old LA survive the archive→unarchive round trip. | UPDATE |
| E2E-10 | Lesson Allocation — LOA, Add Course & Lesson Assignment | Steps 1, 3, 5 say "LA deleted" for Cancel LOA, Cancel Resume LOA, Void Add Course. Same wording update as above; add a de-duplication assertion when the same (student, lesson) pair could be held by two allocations across the archive/unarchive cycle. | UPDATE |
| E2E-10 extension | Native class-member projection | For archive, assert native `class_member` is deleted only with no other matching `sf_class_member` `(student, course, academic year)`; assert it is retained when a sibling exists. For unarchive, assert `deleted_at` clears, `updated_at` changes, and a native member is recreated only after prior deletion. | ADD |
| E2E-11 / E2E-12 | Point Consumption (Nichibei) — Priority Chain & Edge Cases / Publish, Reporting & Reallocation | Add a branch covering point consumption when the underlying LA is archived (not deleted) — current scenarios predate this refactor and assume LA absence rather than LA archive. | UPDATE (blocked on Gap #4 above being specified first) |

### Assumptions Made

- The Confluence page (version 39, 2026-09-25 audit) plus direct code verification in `erp-salesforce` is treated as ground truth for the **implemented** (flag-on) managed-package behavior, since the Jira ticket's own description only links to an inaccessible Google Doc.
- Findings attributed to the prior Codex session (backend repo trace) are included as flagged risks/gaps for QA and dev follow-up; they were spot-checked (repo and referenced files exist) but not re-verified line-by-line in this pass — treat line numbers in that trace as approximate until re-confirmed.
- Engineering's 2026-10-05 clarification is the ground truth for the Backend class-member contract and supersedes the earlier backend-trace conclusion that archive should use a separate `is_archived` state and never delete native `class_member`.
- Bucket is `lesson` (Core) because the archive/unarchive/dedup mechanism and the majority of testable AC live in Core Salesforce; OOP partner impacts are tracked here as regression risks and gaps rather than split into separate OOP epics, since the root cause and fix surface are shared.
- "Riso" appears twice in source material with two different, non-overlapping meanings (manual LA delete button vs. Contract/Lesson API aggregation) — both are preserved as distinct items in this spec rather than merged or dropped.
- No Figma design is linked to this ticket; this is a backend/data-layer refactor with no new UI.

---

## Clarification Questions

1. **[OPEN]** Which Backend reads must exclude archived LA, and on what timeline? (`[BE] Check archived lesson allocation scope`) — does this include `GetStudentsByLessonID` and `RetrieveLessonReportMedias` specifically?
2. **[OPEN]** For Nichibei: should consumed points for sessions under an archived LA be refunded, held, or left as-is? Should unarchive re-consume or leave the original consumption untouched?
3. **[OPEN]** Is a retention/purge policy planned for permanently archived `Lesson_Allocation__c` records, given there is currently no batch job for this and records now accumulate indefinitely?
4. **[OPEN]** Will the Riso manual LA Delete button be brought in line with the archive behavior, or is hard-delete an intentional, permanent design decision for manually-created LA?
5. **[OPEN]** What are the two unresolved items in Confluence §4 ("Duplicated students", "UI lesson allocation detail")? The source page currently has screenshots only, no written description.
6. **[OPEN]** Should `addStudentSessionToSingleLessonV2` and `upsertStudentSession` (`StudentSessionsHandler.cls`) add a defense-in-depth check that rejects an archived `Lesson_Allocation__c`, instead of relying solely on the Add Student picker to keep archived LAs out of reach? Worth a unit/Apex test even though it isn't reachable through the current manual UI.
7. **[OPEN]** Should `Student_Course_ID__c` on `Lesson_Allocation__c` have a uniqueness constraint (or an upstream dedup check) added, given `MasterDataSnapshot.allocationsByStudentCourseId` silently drops any duplicate beyond the first per the `Archived_At__c ASC NULLS FIRST, CreatedDate DESC` tie-break? Worth a data-integrity/unit test even though it isn't reproducible through normal manual QA.

---

## Related Specs

- `epics/lesson/LT-107255-order-group-class-assignment/spec.md` — class-session origin preservation and automatic reconciliation; directly relevant to AC-4 de-duplication behavior.
- `epics/lesson/LT-107410-auto-delete-student-sessions/spec.md` — sibling Core session-lifecycle refactor; shares the same "deleted vs hidden-but-recoverable" distinction this spec introduces for LA itself.
- `epics/OOP/riso/LT-98533-riso-contract-api/spec.md` — already specifies its own archived/deleted exclusion guard (AC-GET-4), independent of this epic.
- `epics/OOP/riso/LT-110368-lesson-api-oop-fields/spec.md` — already requires `Is_Deleted=false` and `Is_Archived=false` on returned Student Sessions.
- `knowledge/domain-knowledge/scheduling/lesson-management/lesson-allocation.md` — needs re-baselining from "LA deleted" to "LA archived" semantics.
- `knowledge/domain-knowledge/scheduling/lesson-management/student-session.md` — needs the same re-baselining for session visibility vs deletion.
- `knowledge/domain-knowledge/scheduling/partner-rules/nichibei-lesson-allocation.md` and `nichibei-lesson-booking.md` — consumed-points and booking-candidate rules need the archived-LA branch added once Gap #4 is resolved.
- `knowledge/domain-knowledge/scheduling/lesson-learned/core.md` (2026-08-19 entry) and `oop.md` (2026-03-04 entry) — directly informed the Lesson-Learned Risks above.

## Related Test Cases

- No existing Qase suite currently exercises archive/unarchive/de-duplication specifically — this is net-new coverage.
- Existing Qase coverage for LA tab, Cancel, Void, LOA, Change Course (referenced in E2E-09/E2E-10 feature lists) asserts "LA deleted/re-created" and will need review against the new archived/unarchived wording during `/define-test-coverage`.

## QASE Coverage Gaps

- AC-1 — Archive triggers: all-orders-removed vs one-order-alive, hard-delete vs Master Queue cancel path, out-of-scope package type skip, idempotency.
- AC-2 — Child formula propagation with zero DML on `Student_Sessions__c`/`Class_Member__c`; confirm `LastModifiedDate` of children is unaffected.
- AC-2a / AC-3a — Backend class-member projection: delete native `class_member` only when no other `sf_class_member` has the same `(student, course, academic year)`; retain it when a sibling exists; on unarchive clear `deleted_at`, update `updated_at`, and insert a native member only after prior deletion. Assert no duplicate active native membership.
- AC-3 — Unarchive rebuild correctness (same Id, recomputed duration/slot count from living orders only), including undelete-from-Recycle-Bin edge case.
- AC-4 — De-duplication after unarchive: manual-vs-auto session collision (see Lesson-Learned Risk #1), detach-not-delete verification, `Sync_History__c` failure logging.
- AC-5 — Read-path exclusion across every listed surface (calendar, attendance, reallocation, student group, teacher timesheet, grade book, student app, sync monitor).
- AC-6 — Add-student popup regression check confirming it intentionally still shows archived-session students as assigned.
- AC-7 — Full legacy-parity regression suite with the feature flag OFF.
- Gap-driven coverage (new, pending implementation): `GetStudentsByLessonID` / `RetrieveLessonReportMedias` archive filters once fixed; Nichibei consumed-points behavior once specified; Riso manual-delete-button regression if brought into scope.
