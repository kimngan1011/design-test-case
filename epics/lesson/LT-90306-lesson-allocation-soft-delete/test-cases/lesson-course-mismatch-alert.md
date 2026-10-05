# Test Cases: LT-90306 — Lesson Allocation Soft Delete (Archive)

Source Qase suite reviewed: [PX suite 1647 — "Show Confirmation Alert when Lesson and LA course are different"](https://app.qase.io/project/PX?suite=1647) (10 existing cases). None test a student whose Lesson Allocation is archived.

Code trace: the course-mismatch alert (`alertLessonOutCourseDuration`'s sibling check, computed via `tableStudentSession.js`'s `isSomeStudentCourseMismatch` getter) is driven entirely by `StudentSessionsHandler.getStudentSessionsByLessonId`, whose base query filters `Is_Deleted__c = FALSE AND Is_Archived__c = FALSE`. The `isMismatchLessonCourse` flag is computed per row from that same filtered dataset, comparing `Lesson__r.Lesson_Schedule__r.Location_Course__r.Course_Master__c` against `Lesson_Allocation__r.Course_Offering__r.Course_Master__c` — the exact Lesson Allocation referenced in that comparison is the same one whose `Archived_At__c` drives `Is_Archived__c` on the row. So once a Lesson Allocation is archived, the Student Session row (and any mismatch flag it carried) disappears from the table entirely — it is never shown as a stale "match" or a stale "mismatch". The "Add Student" picker (`LessonAllocationHandler.getLessonAllocationListByLessonInfo`) independently excludes archived LAs (`Archived_At__c = NULL`) from being offered in the first place, so a student can't even be newly assigned using an already-archived LA. **This is already correct, but has zero regression coverage** — no Apex test (`StudentSessionsHandlerTest`) exercises `isMismatchLessonCourse` together with an archived LA.

## Suite: Show Confirmation Alert when Lesson and LA course are different

### Lesson Course Alert – Mismatched Student's Lesson Allocation Archived – Student and Alert Both Removed from the Lesson; Restored – Student and Mismatch Alert Reappear

**Description:** Regression / control case — Decision Table, contrasts with the baseline (case 12723, "First Student Assigned to One-Time Group Lesson – Lesson course ≠ LA course – Confirmation alert shown"): once the mismatched student's Lesson Allocation is archived, the student's Student Session row — and with it the course-mismatch alert it was the sole cause of — disappears from the lesson entirely, rather than leaving a stale alert visible for a student who is no longer actually assigned. The alert correctly reappears, together with the student, once the Lesson Allocation is restored.

**Preconditions:**
- Lesson L1 is type = Group, course = Course X. Student S1 has an active Lesson Allocation with course = Course Y (mismatch). S1 has already been added to L1, and the course-mismatch confirmation alert is currently shown.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff confirms the course-mismatch alert is visible in Lesson L1 | Alert visible: S1's LA course (Course Y) ≠ Lesson course (Course X) | S1 Is_Archived__c = FALSE; isMismatchLessonCourse = TRUE |
| 2 | The Student Package Order behind S1's Course Y Lesson Allocation is fully removed, so the Lesson Allocation is archived | The Lesson Allocation shows Archived_At__c populated | Archived_At__c = current timestamp |
| 3 | HQ or CM Staff reopens Lesson L1's Student Sessions section | S1 no longer appears in the student list at all, and the course-mismatch alert is no longer shown — not because the mismatch was resolved, but because the whole row is hidden | S1 Is_Archived__c = TRUE (via formula) → row excluded from getStudentSessionsByLessonId, so isMismatchLessonCourse is never evaluated for it |
| 4 | A living Student Package Order reappears for S1's Course Y Student Course, so the Lesson Allocation is unarchived on the same record Id | The Lesson Allocation shows Archived_At__c blank again | Archived_At__c = null (restored) |
| 5 | HQ or CM Staff reopens Lesson L1's Student Sessions section | S1 reappears in the list, and the course-mismatch alert is shown again, since the underlying mismatch (Course Y vs Course X) was never actually resolved | S1 Is_Archived__c = FALSE (restored) → row visible again; isMismatchLessonCourse recomputed as TRUE |

**Severity:** minor
**Priority:** medium

---
