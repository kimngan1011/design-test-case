# Test Cases: LT-90306 — Lesson Allocation Soft Delete (Archive)

Source Qase suite reviewed: [PX suite 548 — "Lesson Report correct"](https://app.qase.io/project/PX?suite=548) (155 existing cases, under OOP FEATURES → Aver, parent 327). Sample reviewed in full (titles + preconditions + steps): #2311, #2313, #2319, #5645–#5665, #5717–#5723, #5764–#5771, #5957, #6009, #6011, #6020 — pattern confirmed across all 155: every precondition gates Add/Edit/Delete/Status-transition and Homework copy purely on `Lesson.Status` (Draft/Canceled/Completed/Published) and on which Lesson Allocation (LA) a record belongs to. None reference `Lesson_Allocation__c.Archived_At__c` or `Student_Sessions__c.Is_Archived__c`.

**Code trace — this is not a "wrong filter" gap, it's an unverifiable one.** `LessonReportRouter.tsx:19-28,41-63` routes the Aver tenant (`LessonDetailSF.tsx:46`, `isAver = domainName === "aver" || "aver-sandbox"`) to `LessonReportDetailEmbeddedSF.tsx:1-58`, which renders only:
```
const url = queryString.stringifyUrl({ url: `${sfUrl}/${sfLang}`, query: { lessonId, userId, allowNavigation } });
return <iframe src={url} ... />;
```
`sfUrl` points at an external Salesforce **Experience Cloud site** (config `lesson.lesson_management.lesson_report.experience_cloud_site_url`). No `Aver_Lesson_Report__c` Apex class, trigger, or digitalExperience metadata exists anywhere in `erp-salesforce`, and no React/TS implementation of Add/Edit/Delete/Status/Homework-copy/PDF-export exists in `school-portal-admin` beyond this iframe wrapper. Whether that external site's logic checks `Archived_At__c`/`Is_Archived__c` **cannot be confirmed or denied by static code review** — it is outside both repos this workspace has access to. (Aver's separate *list/search* layer, `aver-lesson-report-filters.ts:56`, does already carry `MANAERP__Is_Archived__c: { eq: false }`, patched in the same commit as Core's — `5e9fb50ecd7`, "[LT-111546]" — but that is a different suite/surface, not in scope here.)

Every test case below is therefore marked **[UNVERIFIED]**: steps to execute against the live Aver UAT/sandbox org, with the expected result derived from AC-5 ("every read path... excludes archived rows") and the spec's own core risk framing ("the biggest risk is... a child record that still exists while some read path only filters `DeletedAt`/`Is_Deleted` instead of `Is_Archived`"). A FAIL on any of these should be routed back to `[SF][Aver] Check custom aver lesson report`, flagging to the ticket owner that the fix surface is an external Experience Cloud site, not local Apex — the existing 4h estimate was scoped before this was known.

## Suite: Lesson Report correct

### [Aver] Lesson Report – Add – Student's Lesson Allocation Archived – Add Button Unavailable

**Description:** AC-5 (out-of-package, unverifiable by code) — Decision Table — [UNVERIFIED]. Contrasts with existing baseline (#5646 "Can create Lesson Report", #5645 "Can not add Lesson Report" for Canceled Lesson only). Confirms whether the Aver Lesson Report detail page (Experience Cloud iframe) disables the Add button for a student whose Lesson Allocation has archived, even though the Lesson itself is still in an active, non-Canceled status.

**Preconditions:**
- HQ or CM Staff is logged in to the Aver Salesforce org (or Aver sandbox/UAT, per `[SF][Aver] Check custom aver lesson report` scope).
- A Lesson exists with Status = Published. Student A is assigned to the Lesson via Lesson Allocation LA1.
- Student A has not yet had a Lesson Report created for this Lesson.
- The Student Package Order group behind LA1 is fully removed (order voided/cancelled for Student A specifically), so LA1 is archived: `Archived_At__c` is populated. The Lesson itself remains Status = Published (not Canceled) because other students, or the lesson slot itself, are unaffected.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens the Lesson's Report tab (Aver Experience Cloud detail page) for Student A | Per AC-5, the Add button for Student A's report should be unavailable, consistent with how an archived LA is excluded from every other read path in this epic | LA1 Archived_At__c = populated; Lesson Status = Published |
| 2 | HQ or CM Staff inspects whether the Add button is present and enabled | [UNVERIFIED] Record actual behavior: Add button is either correctly disabled/hidden (pass), or still enabled, allowing a report to be created for the archived allocation (fail — route to `[SF][Aver] Check custom aver lesson report`) | Actual result to be captured against live Aver org, since the Experience Cloud site's logic is not inspectable in source |

**Severity:** critical
**Priority:** high

---

### [Aver] Lesson Report – Edit – Student's Lesson Allocation Archived Mid-Lifecycle – Edit Blocked

**Description:** AC-5 (out-of-package, unverifiable by code) — Decision Table — [UNVERIFIED]. Contrasts with existing baseline (#2311 "Can edit Lesson Report with cancel button", #2313 "Can not edit Lesson Report for cancelled lesson" — gates on Lesson status only). Confirms whether an already-created Draft or Submitted Lesson Report for Student A becomes non-editable once Student A's Lesson Allocation archives, independent of the Lesson's own status.

**Preconditions:**
- HQ or CM Staff is logged in to the Aver Salesforce org (or sandbox/UAT).
- A Lesson exists with Status = Published. Student A is assigned via Lesson Allocation LA1. A Lesson Report for Student A exists with Status = Draft.
- The Student Package Order group behind LA1 is fully removed, archiving LA1 (`Archived_At__c` populated), while the Lesson stays Status = Published.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens Student A's existing Draft Lesson Report on the Aver detail page | Per AC-5, Edit should be blocked for a report tied to an archived allocation, matching the existing pattern for Canceled-lesson reports (#2313) | LA1 Archived_At__c = populated; Lesson Report Status = Draft |
| 2 | HQ or CM Staff checks whether the Edit button/form is available | [UNVERIFIED] Record actual behavior: Edit correctly blocked (pass), or still editable (fail — route to `[SF][Aver] Check custom aver lesson report`) | Actual result to be captured against live Aver org |

**Severity:** critical
**Priority:** high

---

### [Aver] Lesson Report – Delete – Student's Lesson Allocation Archived – Delete Button Unavailable

**Description:** AC-5 (out-of-package, unverifiable by code) — Decision Table — [UNVERIFIED]. Contrasts with existing baseline (#5655 "Can Delete Lesson Report", #5656 "Can not Delete Lesson Report" for Published status only). Confirms whether Delete becomes unavailable for a Draft/Submitted report once the student's allocation archives — this is the inverse risk of the Add case: a Delete left enabled on a historical record risks destroying restorable report data that AC-3/AC-4 require to survive an archive→unarchive round trip.

**Preconditions:**
- HQ or CM Staff is logged in to the Aver Salesforce org (or sandbox/UAT).
- A Lesson exists with Status = Published. Student A is assigned via Lesson Allocation LA1. A Lesson Report for Student A exists with Status = Draft.
- LA1 archives (`Archived_At__c` populated) via Student Package Order removal; Lesson stays Status = Published.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens Student A's Draft Lesson Report on the Aver detail page | Per this epic's "archive, never delete" principle, Delete should be unavailable once the allocation is archived — deleting would destroy data that is supposed to remain recoverable, not disabled-but-present | LA1 Archived_At__c = populated |
| 2 | HQ or CM Staff checks whether the Delete button is present and enabled | [UNVERIFIED] Record actual behavior: Delete correctly blocked (pass), or still allowed — which would let staff permanently destroy report data for an allocation that is supposed to be restorable (fail — route to `[SF][Aver] Check custom aver lesson report`, flag as data-loss risk) | Actual result to be captured against live Aver org |

**Severity:** critical
**Priority:** high

---

### [Aver] Lesson Report – Status Transition – Student's Lesson Allocation Archived – Submit/Publish/Revert Blocked

**Description:** AC-5 (out-of-package, unverifiable by code) — State Transition — [UNVERIFIED]. Contrasts with existing baseline (#2319 "Can update Lesson Report status", #5657–#5664 — all gate status-change availability on Lesson status only, never on allocation archive state). Confirms whether Submit, Publish, and Revert-to-Draft/Submitted all become unavailable once the student's allocation archives.

**Preconditions:**
- HQ or CM Staff (or Teacher) is logged in to the Aver Salesforce org (or sandbox/UAT).
- A Lesson exists with Status = Published. Student A is assigned via Lesson Allocation LA1. A Lesson Report for Student A exists with Status = Draft.
- LA1 archives (`Archived_At__c` populated); Lesson stays Status = Published.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Teacher opens Student A's Draft Lesson Report on the Aver detail page and looks for the Submit action | Per AC-5, the status-change action should be unavailable, consistent with #5657's existing pattern for Draft-lesson reports | LA1 Archived_At__c = populated; Lesson Report Status = Draft |
| 2 | Teacher checks whether the Submit button is present and enabled | [UNVERIFIED] Record actual behavior | Actual result to be captured against live Aver org |
| 3 | Repeat for a Submitted-status report of the same student: Teacher looks for the Publish action | Per AC-5, Publish should equally be unavailable | Lesson Report Status = Submitted |
| 4 | Teacher checks whether the Publish button is present and enabled | [UNVERIFIED] Record actual behavior — any status transition left enabled on an archived allocation's report should be routed to `[SF][Aver] Check custom aver lesson report` as a fail | Actual result to be captured against live Aver org |

**Severity:** critical
**Priority:** high

---

### [Aver] Lesson Report – Homework Copy – Source Lesson's Allocation Archived – Homework Not Copied as Current

**Description:** AC-5 (out-of-package, unverifiable by code) — Decision Table — [UNVERIFIED]. Extends the existing isolation pattern already locked in by #5667 "Do not show Homework of different LA" to the archived-LA case: confirms that the Previous-week-Homework section of today's report does not silently surface homework from a previous lesson whose underlying Student Session is now archived, as if it were still a live, current source.

**Preconditions:**
- HQ or CM Staff is logged in to the Aver Salesforce org (or sandbox/UAT).
- Student A has two consecutive weekly Lessons under Lesson Allocation LA1: Lesson L1 (previous week) and Lesson L2 (this week). L1's Lesson Report has a "Next week Homework" entry = "Workbook p.12-15".
- L1's Student Session under LA1 becomes archived (LA1's Student Package Order group removed, `Archived_At__c` populated) before L2's report is created.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens the Report tab for Student A's Lesson L2 and clicks Add to create this week's report | Per AC-5's principle (mirroring #5667's existing isolation test), the Previous Homework section should not silently populate from L1 as if it were an active, current source, since L1's session is now archived | LA1 Archived_At__c = populated at the time L2's report is created |
| 2 | HQ or CM Staff checks the Previous Homework section content | [UNVERIFIED] Record actual behavior: shows "No information" or equivalent empty state (pass, consistent with #5665's existing "no homework" case), or silently copies "Workbook p.12-15" from the archived L1 report as if nothing had changed (fail — route to `[SF][Aver] Check custom aver lesson report`) | Actual result to be captured against live Aver org |

**Severity:** major
**Priority:** high

---

### [Aver] Lesson Report – Historical Access – Allocation Archived After Publish – Report and Homework Remain Viewable and Exportable

**Description:** AC-5 scope note ("archived records remain reachable by direct record Id") — Component — [UNVERIFIED]. Contrasts with the four blocking cases above: confirms the Aver detail page does not over-correct by hard-hiding a report that was already Published before the allocation archived. Historical attendance/report data must stay viewable and exportable, only new edits/status-changes should be blocked.

**Preconditions:**
- HQ or CM Staff is logged in to the Aver Salesforce org (or sandbox/UAT).
- A Lesson Report for Student A exists with Status = Published, created while Lesson Allocation LA1 was active.
- LA1 subsequently archives (`Archived_At__c` populated) via Student Package Order removal.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens Student A's already-Published Lesson Report on the Aver detail page | Per AC-5's scope note, the report content (Report, Previous/Next Homework, PIC confirmation) should remain fully viewable in read-only mode — not hidden or blanked out | LA1 Archived_At__c = populated; Lesson Report Status = Published |
| 2 | HQ or CM Staff clicks the Export button (#5767's existing "Enable Export button when Lesson Report status = Submitted/Published" baseline) | [UNVERIFIED] Record actual behavior: PDF exports normally with full historical content (pass), or export is blocked/errors (fail — over-correction, route to `[SF][Aver] Check custom aver lesson report`) | Actual result to be captured against live Aver org |

**Severity:** major
**Priority:** high

---

### [Aver] Lesson Report – Unarchive Round Trip – Lesson Allocation Restored – Editing Resumes With No Duplicate Report

**Description:** AC-3 (same-Id restore) applied to the Aver detail page — Regression — [UNVERIFIED]. Confirms that once a living Student Package Order reappears and the same Lesson Allocation Id is unarchived, the Aver Lesson Report detail page treats the student as fully active again — resuming Add/Edit/Status actions normally — without creating a second, duplicate report for the same (student, lesson) pair.

**Preconditions:**
- HQ or CM Staff is logged in to the Aver Salesforce org (or sandbox/UAT).
- Student A's Lesson Allocation LA1 was archived (per the Add/Edit/Status cases above), blocking further report actions for Lesson L2.
- A living Student Package Order reappears for Student A's Student Course, and LA1 is unarchived on the same record Id (`Archived_At__c` cleared).

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens the Report tab for Student A's Lesson L2 on the Aver detail page | Add/Edit/Status actions should be available again, matching normal active-allocation behavior | LA1 Archived_At__c = null (restored, same Id) |
| 2 | HQ or CM Staff creates or edits the Lesson Report for L2 and saves | [UNVERIFIED] Record actual behavior: action succeeds normally (pass), or is still blocked as if the allocation were still archived (fail) | Actual result to be captured against live Aver org |
| 3 | HQ or CM Staff checks whether exactly one Lesson Report exists for Student A on Lesson L2 | [UNVERIFIED] Record actual behavior: exactly one report exists (pass), or a second, duplicate report was created alongside any pre-archive report (fail — route to `[SF][Aver] Check custom aver lesson report`) | Expect: 1 report for (Student A, L2) |

**Severity:** minor
**Priority:** medium

---
