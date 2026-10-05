# Test Cases: LT-90306 — Lesson Allocation Soft Delete (Archive)

Source Qase suite reviewed: [PX suite 1702 — "Student Risk Flag Info"](https://app.qase.io/project/PX?suite=1702) (13 existing cases). This manual Risk Flag/Remarks feature was confirmed independent of the Lesson Allocation archive mechanism — it writes to a dedicated `Risk_History__c` object keyed off `Contact.Student__c` (`StudentRiskHistoryHandler.cls`/`StudentRiskHistoryRepo.cls`), with no query, trigger, or validation anywhere in that path referencing `Lesson_Allocation__c.Archived_At__c` or `Student_Sessions__c.Is_Archived__c`. None of the 13 existing cases test archive/restore. This case locks in that the Risk Flag value itself survives an archive/restore cycle completely unaffected, since it lives on a separate, parent-independent record.

## Suite: Student Risk Flag Info

### Student with Risk Flag On – Lesson Allocation Archived then Restored – Risk Tag Displays Correctly Again, Unaffected by the Cycle

**Description:** Regression / control case — Decision Table — a student's manually-set Risk Flag (Risk_History__c.Risk_State__c = On) is stored entirely independently of their Lesson Allocation. When the student's Lesson Allocation is archived, the student (and any Risk tag shown alongside their name) disappears from the lesson's Student tab along with their Student Session row — not because the Risk Flag itself was cleared or lost, but because the whole row is hidden by the unrelated `Is_Archived__c` session filter. Once the Lesson Allocation is restored, the student reappears with the Risk tag still correctly showing On, with its Remarks intact, confirming the Risk_History__c record was never touched by the archive/restore cycle.

**Preconditions:**
- Student A has Risk Flag = On (with Remarks = "Multiple absences in March") set via Edit Risk Info. Student A is currently assigned to Lesson L1, showing the Risk tag next to their name on the Student tab.
- Student A has an active Lesson Allocation for the course behind L1.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens Lesson L1's Student tab and confirms Student A is listed with the Risk tag showing On and Remarks = "Multiple absences in March" | Student A's row shows the Risk tag correctly | Risk_History__c.Risk_State__c = On; Remark__c = "Multiple absences in March" |
| 2 | The Student Package Order behind Student A's Lesson Allocation is fully removed, so the Lesson Allocation is archived | The Lesson Allocation shows Archived_At__c populated; Student A's Student Session is hidden from Lesson L1 (and with it, the visible Risk tag on that row) | Archived_At__c = current timestamp; Student A Is_Archived__c = TRUE (via formula) → row hidden, Risk_History__c record itself untouched |
| 3 | HQ or CM Staff opens Student A's Risk Info directly from their Contact/Student record (not via Lesson L1) | Risk Flag still shows On, with Remarks = "Multiple absences in March", completely unchanged | Risk_History__c record unaffected by the Lesson Allocation's archived state |
| 4 | A living Student Package Order reappears for Student A's Student Course, so the Lesson Allocation is unarchived on the same record Id | The Lesson Allocation shows Archived_At__c blank again | Archived_At__c = null (restored) |
| 5 | HQ or CM Staff reopens Lesson L1's Student tab | Student A reappears in the list with the Risk tag correctly showing On and Remarks = "Multiple absences in March", exactly as before archiving | Student A Is_Archived__c = FALSE (restored) → row visible again; Risk tag reflects the same unchanged Risk_History__c record |

**Severity:** minor
**Priority:** medium

---
