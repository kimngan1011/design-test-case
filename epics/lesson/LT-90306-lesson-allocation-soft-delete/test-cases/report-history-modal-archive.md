# Test Cases: LT-90306 — Lesson Allocation Soft Delete (Archive)

Source Qase suite reviewed: [PX suite 3270 — "Report History"](https://app.qase.io/project/PX?suite=3270) (5 existing cases, under "Lesson Report under Lesson" parent 427). Case 21860 ("Student in Multiple Courses – Navigation Scoped per Lesson Allocation") confirms the Report History modal's Previous/Next navigation chain is scoped strictly per Lesson Allocation (student + course) — it never crosses between a student's different course allocations. None of the 5 cases test an archived Lesson Allocation.

Code trace — **correction from an earlier assumption in this epic**: the live BO modal does NOT actually call the Apex REST endpoint backed by `LessonReportDetailRepo.getLessonReportHistoryByStudentSessionId` (confirmed via repo-wide search — that endpoint has zero call sites in the current `school-portal-admin` frontend; it is dead code, despite filtering `Is_Archived__c` correctly itself). The live modal instead uses a separate, Apex-bypassing Salesforce GraphQL (UI API) query, `Lesson_GetStudentSessionReportHistoryByLessonAllocationId` (`school-portal-admin/src/squads/lesson/service/sf/student-session-service/student-session.query.graphql:1-83`), which independently filters:
```graphql
where: { and: [
  { MANAERP__Lesson_Allocation__c: { eq: $lesson_allocation_id } }
  { MANAERP__Lesson__c: { ne: null } }
  { MANAERP__Is_Archived__c: { eq: false } }
] }
```
Behaviorally this reaches the same conclusion (archived LA → excluded), just via a different, previously-uncited code path — this file's test cases have been updated to cite the correct query.

A second, important mechanical finding: the full report-history array is fetched **exactly once**, at the moment the "Report History" **button** itself renders (`ButtonReportHistorySF.tsx` calls `useGetReportHistoriesSF({ lessonAllocationId })` before the dialog even opens) — not when the modal is opened, and not on every Previous/Next click. Once fetched, "Previous Report"/"Next Report" are pure client-side array indexing (`useIterateArray.ts`, plain `useState`) with **zero further server calls**. This means: (1) there is no scenario where the button is visible but a Previous/Next click independently fails mid-session, since no per-click query exists to fail — but (2) there IS a distinct staleness risk: if the Report tab page was loaded (and the button's query ran) while the Lesson Allocation was still active, then archived in the background, the button and its already-fetched (now-stale) history array remain fully usable for the rest of that page session, since nothing ever re-checks the archive state after the initial fetch.

## Known mechanism, confirmed from the above: no "button shows, Next/Previous breaks mid-click" scenario exists

Each Previous/Next click only moves a local array index — it never re-queries Salesforce. So archiving a Lesson Allocation while the modal is *already open and navigating* cannot break that in-progress session. The only reachable archive-related risk is the **stale pre-fetch** scenario captured in the second test case below.

## Suite: Report History

### Report History – Lesson Allocation Archived – History Chain Inaccessible from the Lesson's Report Tab; Restored – Full Chain Navigable Again

**Description:** Regression / control case — Decision Table, contrasts with the baseline (case 3225, "Most Recent Entry Displayed at Top") — once a student's Lesson Allocation is archived, the "Report History" button/modal for that student on any of that allocation's lessons has no valid Student Session to seed from, since `Lesson_GetStudentSessionReportHistoryByLessonAllocationId`'s query filters `Is_Archived__c = FALSE`. The student (and the Report History entry point itself) is simply absent from the Report tab. Restoring the Lesson Allocation makes the full history chain navigable again, from the same underlying records.

**Preconditions:**
- Student A is enrolled in Course X with lessons on Jan 1st, Jan 2nd, Jan 3rd, Jan 4th, all with saved lesson reports. Opening Report History from the Jan 4th lesson currently shows the full Jan 4th → Jan 3rd → Jan 2nd → Jan 1st chain.
- Student A has an active Lesson Allocation for Course X.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Teacher/CM opens the Jan 4th lesson's Report tab and clicks "Report History" for Student A | The modal opens showing the full Jan 4th → Jan 1st chain, navigable via Previous/Next | Student A Is_Archived__c = FALSE throughout the chain |
| 2 | The Student Package Order behind Student A's Course X Lesson Allocation is fully removed, so the Lesson Allocation is archived | The Lesson Allocation shows Archived_At__c populated | Archived_At__c = current timestamp |
| 3 | Teacher/CM reopens the Jan 4th lesson's Report tab | Student A no longer appears on the Report tab at all — there is no "Report History" entry point to click for this student on this lesson | Student A's Student Sessions Is_Archived__c = TRUE (via formula) → excluded from the Report tab's own student list, same mechanism as suite 426 |
| 4 | A living Student Package Order reappears for Student A's Course X Student Course, so the Lesson Allocation is unarchived on the same record Id | The Lesson Allocation shows Archived_At__c blank again | Archived_At__c = null (restored) |
| 5 | Teacher/CM reopens the Jan 4th lesson's Report tab and clicks "Report History" for Student A | The modal opens showing the exact same Jan 4th → Jan 1st chain as before archiving — same records, not regenerated | Is_Archived__c = FALSE (restored) → Lesson_GetStudentSessionReportHistoryByLessonAllocationId's query succeeds again |

**Severity:** minor
**Priority:** medium

---

### Report History – Lesson Allocation Archived After Page Load (Before Button Click) – Button Still Shows Stale, Pre-Archive History Data

**Description:** Gap case — Decision Table — since the full report-history array is fetched once when the "Report History" button itself renders (not on dialog open, not per Previous/Next click), a teacher who already has the Report tab open when the Lesson Allocation gets archived in the background will still see the button and its already-fetched history data exactly as it was before archiving — the UI never re-checks the archive state after the initial fetch, for the remainder of that page session. This is a different failure mode than "button shows but navigation breaks mid-click" (which cannot happen, since Previous/Next never re-queries) — it's a pure staleness issue: the whole modal is usable, but is silently showing data for a student whose Lesson Allocation is no longer actually active.

**Preconditions:**
- Teacher has the Jan 4th lesson's Report tab open for Student A, with the "Report History" button already rendered (its one-time data fetch has already completed, showing the Jan 4th → Jan 1st chain).

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Teacher confirms the "Report History" button is visible for Student A on the already-loaded Report tab | Button visible, underlying data already fetched into the page | useGetReportHistoriesSF already resolved for lessonAllocationId |
| 2 | In a separate session, the Student Package Order behind Student A's Course X Lesson Allocation is fully removed, so the Lesson Allocation is archived | The Lesson Allocation shows Archived_At__c populated | Archived_At__c = current timestamp |
| 3 | Teacher (on the original, stale page, without refreshing) clicks "Report History" for Student A | The modal still opens and shows the full Jan 4th → Jan 1st chain, with no indication that the Lesson Allocation is now archived | Dialog renders from the already-fetched, now-stale `reportHistories` array; no re-fetch occurs on dialog open |
| 4 | Teacher clicks "Previous Report" repeatedly through the whole chain | Navigation works normally end-to-end — all entries display, since this is pure client-side indexing with no server calls | useIterateArray's setCurrentIndex never re-validates archive state |
| 5 | Teacher refreshes the Report tab (fresh page load) | Student A no longer appears on the Report tab at all, and the "Report History" button is gone — the staleness only persisted for the already-open page, not across a refresh | A fresh useGetReportHistoriesSF call now correctly excludes the archived Student Session |

**Severity:** minor
**Priority:** low

---

### Report History – Lesson Allocation Restored on a Fresh Page Load – Full Previous/Next Chain Navigable Again with Correct Content at Every Step

**Description:** Regression / control case — Decision Table, deeper than the restore step covered in the first case above — after restoring an archived Lesson Allocation and loading the Report tab fresh (not reusing a stale pre-archive page), the "Report History" button reappears and the full Previous/Next chain is navigable end-to-end, with each individual entry's Lesson Name, Course, and report content displaying correctly — matching the same level of step-by-step verification as the original baseline cases (3225/3226/3227), not just confirming the modal opens.

**Preconditions:**
- Student A's Lesson Allocation for Course X was archived, hiding the Report History entry point for lessons on Jan 1st, Jan 2nd, Jan 3rd, and Jan 4th (all with previously-saved lesson reports).

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | A living Student Package Order reappears for Student A's Course X Student Course, so the Lesson Allocation is unarchived on the same record Id | The Lesson Allocation shows Archived_At__c blank again | Archived_At__c = null (restored) |
| 2 | Teacher/CM loads the Jan 4th lesson's Report tab fresh (new page load, not a reused stale tab) and confirms the "Report History" button is visible for Student A | The button is visible again | Student A Is_Archived__c = FALSE (restored) → Lesson_GetStudentSessionReportHistoryByLessonAllocationId's query includes this student's sessions again |
| 3 | Teacher/CM clicks "Report History" | The modal opens showing the Jan 4th entry as current, with correct Lesson Name and Course = "Course X"; "Next Report" is deactivated (Jan 4th is the most recent) | Jan 4th report content matches what was saved before the archive/restore cycle |
| 4 | Teacher/CM clicks "Previous Report" three times in succession | Each click correctly steps to Jan 3rd, then Jan 2nd, then Jan 1st, with each entry's Lesson Name/Course/report content displaying accurately; "Previous Report" deactivates at Jan 1st (the oldest) | Full chain content unchanged from before archiving — same underlying Student_Sessions__c/Lesson_Report__c records, never recreated |
| 5 | Teacher/CM clicks "Next Report" three times in succession, back to Jan 4th | Each click correctly steps forward through Jan 2nd, Jan 3rd, to Jan 4th, with "Next Report" deactivating again at Jan 4th | Round-trip navigation fully functional post-restore, identical to the pre-archive baseline behavior (cases 3225–3227) |

**Severity:** minor
**Priority:** medium

---
