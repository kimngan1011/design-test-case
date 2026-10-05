# Test Cases: LT-90306 — Lesson Allocation Soft Delete (Archive)

Source Qase suite reviewed: [PX suite 3272 — "[Renseikai] Copy lesson report fields values to lesson report details (per student)"](https://app.qase.io/project/PX?suite=3272) (20 existing cases, Jira LT-57816, under parent 292). Despite the tenant-sounding title, this is a **Core mechanism** — every Group lesson's Content/Announcement/Homework edit cascades down to each enrolled student's individual Student Session ("lesson report detail per student"), regardless of tenant. None of the 20 cases test a student whose Lesson Allocation is archived.

Code trace: this cascade is implemented by `LessonReportHandler.updateLessonReportDetailInformation` (`LessonReportHandler.cls:435-472`), invoked from the `Lesson_Report__c` `afterUpdate` trigger (line 514) only when `Teaching_Method_Value__c == 'Group'`. Its query:
```apex
WHERE Lesson_Report__c IN :changedLessonReportIds AND Is_Deleted__c = FALSE AND Is_Archived__c = FALSE
```
already filters `Is_Archived__c = FALSE` — confirmed patched in the same commit (`1eee000f`, "[LT-92895] ... Is_Archived__c checks") as the already-verified `modifyLessonReportDetailsInStudentSession`. This is already correct, but has zero regression coverage for the archived-student case specifically, across any of the 20 existing field/origin/surface combinations in this suite.

## Suite: [Renseikai] Copy lesson report fields values to lesson report details (per student)

### Group Lesson Content/Announcement/Homework Update – One Enrolled Student Archived – Cascade Correctly Skips That Student; Other Students Updated Normally

**Description:** Regression / control case — Decision Table, contrasts with the baseline cases (e.g. 25658/25664, "Content update – Replaced on every student detail" / "Replaced for every student") — when a Group lesson's Content, Announcement, or Homework is updated (from either BO or SF), the cascade to each student's individual lesson report detail correctly skips a student whose Lesson Allocation is archived, while still updating every other enrolled, non-archived student normally. This locks in that the cascade mechanism isn't broken, blocked, or partially corrupted by one archived student mixed into the group.

**Preconditions:**
- A Group lesson report has Aiko Tanaka (active Lesson Allocation) and Haruto Sato (Lesson Allocation archived — Archived_At__c populated) both enrolled. Both currently hold content_v1/announcement_v1/homework_v1 in their individual lesson report details.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff (BO or SF) updates the Group lesson's shared Content field to content_v2 and saves | The Lesson_Report__c-level Content field updates to content_v2 with no error | Lesson_Report__c.Content__c = content_v2 |
| 2 | HQ or CM Staff checks Aiko Tanaka's individual lesson report detail | Content shows content_v2 — the cascade updated this non-archived student normally | Aiko Tanaka Is_Archived__c = FALSE → included in updateLessonReportDetailInformation's WHERE clause |
| 3 | HQ or CM Staff checks Haruto Sato's individual lesson report detail | Haruto Sato is not found in the active Student Sessions list for this lesson at all — the cascade never reached (and never could have reached) his record, since it's excluded by Is_Archived__c = FALSE before the update DML runs | Haruto Sato Is_Archived__c = TRUE (via formula) → excluded from the cascade's WHERE clause |
| 4 | A living Student Package Order reappears for Haruto Sato's Student Course, so the Lesson Allocation is unarchived on the same record Id, and HQ or CM Staff reopens his lesson report detail | Haruto Sato reappears, but his individual lesson report detail still shows the OLD content_v1 — the content_v2 cascade from step 1 never applied to him while he was archived, and restoring the LA does not retroactively re-run that cascade | Haruto Sato Is_Archived__c = FALSE (restored); Content_v1 unchanged, since no DML ever touched his record during the archived window |

**Severity:** major
**Priority:** medium

---

### Published Group Lesson – Cascaded Content Update – Archived Student Does Not See It on Learner App; Restored Student Sees the Pre-Archive Version, Not the Missed Update

**Description:** Gap case — Decision Table, contrasts with the baseline (case 25662/25663, "Stored shared values – Shown to enrolled student on Learner App") — ties the confirmed cascade-skip behavior above to its Learner App consequence: an archived student never receives a Group lesson's cascaded content update, and even after being restored, they see their last-synced (pre-archive) content rather than the update that was pushed out while they were archived, since that update was never written to their record at all.

**Preconditions:**
- A Published Group lesson report has Aiko Tanaka (active Lesson Allocation) and Haruto Sato (will be archived mid-test) both enrolled, both currently able to see content_v1 on Learner App.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Both Aiko Tanaka and Haruto Sato open the lesson report on Learner App | Both see content_v1 | Both Is_Archived__c = FALSE |
| 2 | The Student Package Order behind Haruto Sato's Lesson Allocation is fully removed, so the Lesson Allocation is archived | The Lesson Allocation shows Archived_At__c populated | Archived_At__c = current timestamp |
| 3 | HQ or CM Staff updates the Group lesson's Content to content_v2 and saves | Aiko Tanaka's individual lesson report detail cascades to content_v2; Haruto Sato's does not (per the control case above) | Aiko Tanaka Is_Archived__c = FALSE → cascaded; Haruto Sato excluded |
| 4 | Aiko Tanaka refreshes the lesson report on Learner App | Aiko Tanaka now sees content_v2 | Matches the BO/SF record |
| 5 | A living Student Package Order reappears for Haruto Sato's Student Course, so the Lesson Allocation is unarchived on the same record Id, and Haruto Sato refreshes the lesson report on Learner App | Haruto Sato sees content_v1 — the version from before he was archived, NOT content_v2, since the cascade never reached his record while archived and restoring does not retroactively re-apply it | Haruto Sato's individual lesson report detail still holds content_v1; staff must manually re-apply the update (e.g. a trivial re-save of the Group lesson) to bring him in sync with Aiko Tanaka |

**Severity:** major
**Priority:** medium

---
