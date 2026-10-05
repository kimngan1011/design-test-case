# Test Cases: LT-90306 — Lesson Allocation Soft Delete (Archive)

Source Qase suite reviewed: [PX suite 1748 — "Lesson Report Detail"](https://app.qase.io/project/PX?suite=1748) (21 existing cases, under parent 292). This suite's content is the same underlying feature set already fully traced and tested under suites 426/3269 (Lesson Report Detail / SRD bulk edit) and 3270 (Report History), combined into one suite here. The same Apex/GraphQL mechanisms and findings apply; this file re-applies them against this suite's own baseline case numbers, since it is a distinct Qase suite ID.

Code trace (already established, see `lesson-report-detail-bulk-edit-archive.md` / `update-lr-archive.md` / `report-history-modal-archive.md` for full detail): `LessonReportHandler.modifyLessonReportDetailsInStudentSession` silently skips archived-session rows with no error; `Lesson_Report__c`-level fields are never touched by archive/restore; the Report History modal's `Is_Archived__c = false` query controls both whether the entry point appears and whether a stale, already-fetched chain stays visible on an unrefreshed page.

## Suite: Lesson Report Detail

### Bulk Edit Individual Report via SF – One Student's Lesson Allocation Archived Mid-Session – That Student's Edit Silently Dropped; Others Saved Normally

**Description:** Gap case — Decision Table, contrasts with the baseline (case 13735, "Bulk Edit Individual Report via SF – Changes Reflected on BO and Mobile") — if a teacher has the Report tab open with multiple students loaded and one student's Lesson Allocation is archived in the background before Save, that student's edit is silently dropped with no error while other students' edits save normally. Same mechanism as already documented for suites 426/3269.

**Preconditions:**
- A Draft lesson report has Student A and Student B both loaded on SF, both with active Lesson Allocations.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Teacher opens the Report tab on SF with both students loaded | Both students' SRD values shown | Both Is_Archived__c = FALSE |
| 2 | The Student Package Order behind Student A's Lesson Allocation is fully removed, so the Lesson Allocation is archived | Archived_At__c populated | Archived_At__c = current timestamp |
| 3 | Teacher (stale page) bulk-edits both students and saves | No error shown; save appears to succeed | modifyLessonReportDetailsInStudentSession excludes Student A's archived session |
| 4 | Teacher refreshes the Report tab | Student B's edit applied; Student A no longer appears, with no indication their edit was dropped | Student A Is_Archived__c = TRUE |

**Severity:** major
**Priority:** medium

---

### Report History – Lesson Allocation Archived – History Chain Inaccessible; Restored – Full Chain Navigable Again

**Description:** Regression / control case — Decision Table, contrasts with the baseline (case 13727, "Report History – Most Recent Entry (Jan 4th) at Top") — once a student's Lesson Allocation is archived, the Report History entry point for that student disappears from the Report tab entirely (no valid Student Session to seed the chain from). Restoring the Lesson Allocation makes the same history chain fully navigable again via Previous/Next.

**Preconditions:**
- Student A is enrolled in Course X with saved lesson reports on Jan 1st–4th. Report History from the Jan 4th lesson currently shows the full chain.
- Student A has an active Lesson Allocation.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Teacher/CM opens Report History for Student A from the Jan 4th lesson | Full Jan 4th → Jan 1st chain shown, navigable | Is_Archived__c = FALSE |
| 2 | The Student Package Order behind Student A's Lesson Allocation is fully removed, so the Lesson Allocation is archived | Archived_At__c populated | Archived_At__c = current timestamp |
| 3 | Teacher/CM reopens the Jan 4th lesson's Report tab | Student A is absent; no Report History entry point for them | Is_Archived__c = TRUE |
| 4 | A living Student Package Order reappears, so the Lesson Allocation is unarchived on the same record Id | Archived_At__c blank again | Archived_At__c = null (restored) |
| 5 | Teacher/CM reopens Report History for Student A from the Jan 4th lesson | Same full Jan 4th → Jan 1st chain shown, same records | Is_Archived__c = FALSE (restored) |

**Severity:** minor
**Priority:** medium

---
