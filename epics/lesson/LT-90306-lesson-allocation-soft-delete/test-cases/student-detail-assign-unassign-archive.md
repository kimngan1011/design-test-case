# Test Cases: LT-90306 — Lesson Allocation Soft Delete (Archive)

Source Qase suites reviewed: [PX suite 325 — "Student Detail"](https://app.qase.io/project/PX?suite=325) (11 cases) and its child [PX suite 2077 — "Assign/Unassign a student"](https://app.qase.io/project/PX?suite=2077) (16 cases). This is the Lesson Detail → Student tab's Add Student / Remove Student feature, gated by config flags `lesson.lessonmgmt_v2.assign_student_to_lesson` and `lesson.remove_student_from_lesson.is_enabled`. Despite the "v2" naming, this is a React BO frontend (`TabStudentSF`/`TabStudentSFV2` in `school-portal-admin`) that calls the **exact same erp-salesforce Apex backend** as the older Salesforce-native LWC already covered elsewhere in this epic (suite 219/1293) — not a separate data layer. None of the 27 existing cases across both suites test an archived Lesson Allocation.

Code trace:
- **Add Student popup** (`DialogAddStandardStudentSF.tsx` → `useRetrieveLessonAllocationSF.ts` → REST `/lessonAllocations/retrieve/v1` → `LessonAllocationRestAPITransport.cls` → `LessonAllocationHandler.getLessonAllocationListByLessonInfoClient`) shares the exact same SOQL builder (`buildGetLessonAllocationListByLessonInfoStmt`, `LessonAllocationHandler.cls:91-92`, `WHERE Archived_At__c = NULL AND (...)`) already confirmed correct for the LA Detail / Lesson Schedule "Add Student" flow — already correct, zero regression coverage for this specific suite.
- **Remove Student button** (`useRemoveStudentSessionsOfOutLessonSF.ts` → REST `/studentSessions/v1/unassignStudentSessionInLesson` → `StudentSessionRestAPI.UnassignStudentSessionInLesson` → `StudentSessionsHandler.unassignStudentSessionInLesson` → `StudentSessionsRepo.findToBeUnassignedStudentSessions`) is the **exact same Apex method** already found to have no `Is_Archived__c` filter in its lookup query (`WHERE Id IN :studentSessionIds AND Lesson__c = :lessonId AND Is_Deleted__c = FALSE`) when reviewing the "Remove Lesson" button on LA Detail (suite 324) — this is a shared backend gap reachable from a second, independent UI entry point.
- **Course mismatch confirmation alert** (TabStudentSFV2 only, flag `lesson.student_course_mismatch.is_enabled`) sources its data from `Lesson_GetLessonStudentsByLessonId` GraphQL query, which filters `Student_Sessions__c.Is_Archived__c = false` and `Lesson_Allocation__c.Archived_At__c = null` consistently with the old LWC's equivalent — already correct, zero regression coverage.

## Suite: Assign/Unassign a student

### Add Student Popup – Student's Only Lesson Allocation Archived – Excluded from Search Results

**Description:** Regression / control case — Decision Table, contrasts with the baseline (case 1915, "Add Student Popup – Search and Filter by Name, Course, Grade – Correct Students Displayed") — a student whose only Lesson Allocation for the lesson's course is archived does not appear in the Add Student popup's search results at all, consistent with the shared `Archived_At__c = NULL` picker filter already confirmed for the LA Detail / Lesson Schedule flow.

**Preconditions:**
- Student A's Lesson Allocation for Course A has been archived (Archived_At__c populated) after its Student Package Order was fully removed. A lesson for Course A exists with no students assigned yet.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens the Course A lesson's Student tab, clicks "Add Students", and searches for Student A by name | Student A does not appear in the search results | Archived LA excluded by getLessonAllocationListByLessonInfoClient's Archived_At__c = NULL filter |
| 2 | A living Student Package Order reappears for Student A's Course A Student Course, so the Lesson Allocation is unarchived on the same record Id | The Lesson Allocation shows Archived_At__c blank again | Archived_At__c = null (restored) |
| 3 | HQ or CM Staff repeats the search for Student A in the Add Student popup | Student A now appears in the search results and can be added normally | Archived_At__c = blank (restored) → included again |

**Severity:** minor
**Priority:** medium

---

### Remove Student Button – Stale Page (LA Archived After Load, Before Click) – Action Silently Succeeds Despite Archived Lesson Allocation

**Description:** Gap case — Decision Table, contrasts with the baseline (case 9138, "Student List – Remove Student Button – Visible and Student Removed on Confirm") — if a staff member has the Lesson Detail → Student tab open with Student A already assigned, and Student A's Lesson Allocation gets archived in the background before "Remove Student" is clicked, the action still succeeds with no error, because `StudentSessionsRepo.findToBeUnassignedStudentSessions` has no `Is_Archived__c` filter — the same shared backend gap already documented for the "Remove Lesson" button on LA Detail (suite 324), reachable here through a second, independent UI entry point.

**Preconditions:**
- HQ or CM Staff has the Course A lesson's Student tab open, with Student A assigned and visible in the student list.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | In a separate session, the Student Package Order behind Student A's Lesson Allocation is fully removed, so the Lesson Allocation is archived | The Lesson Allocation shows Archived_At__c populated | Archived_At__c = current timestamp |
| 2 | HQ or CM Staff (on the original, stale page, without refreshing) clicks "Remove Student" for Student A and confirms | The action completes with no error — Student A's session is unassigned (Lesson__c cleared) exactly as it would for a non-archived LA | findToBeUnassignedStudentSessions's ONLY_THIS_LESSON query has no Is_Archived__c filter → session found and mutated despite the LA being archived |
| 3 | HQ or CM Staff refreshes the Student tab | Student A no longer appears in the student list (removed), and reopening the Add Student popup confirms Student A's archived LA is also excluded from re-adding | Mutation succeeded with no archived-state guard anywhere in this shared code path |

**Severity:** major
**Priority:** medium

---

### Course Mismatch Alert (TabStudentSFV2) – Mismatched Student's Lesson Allocation Archived – Student and Alert Both Removed; Restored – Both Reappear

**Description:** Regression / control case — Decision Table, contrasts with the baseline (case 12756, "Assign First Student – Group One-Time Lesson – LA Course Differs from Lesson Course – Confirmation Alert Shown") — once the mismatched student's Lesson Allocation is archived, the student disappears from the lesson's student list entirely (and with it, the course-mismatch alert it was the sole cause of), since `Lesson_GetLessonStudentsByLessonId`'s GraphQL query filters `Is_Archived__c = false` — the same pattern already locked in for the older LWC's equivalent alert (suite 1647).

**Preconditions:**
- Group lesson L1 has Course = C1. Student S1 has an active Lesson Allocation with Course = C2 (mismatch) and has already been added to L1 — the course-mismatch confirmation alert is currently shown on the TabStudentSFV2 Student tab.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff confirms the course-mismatch alert is visible on L1's Student tab | Alert visible: S1's LA course (C2) ≠ Lesson course (C1) | S1 Is_Archived__c = FALSE; isCourseMismatch = TRUE |
| 2 | The Student Package Order behind S1's Course C2 Lesson Allocation is fully removed, so the Lesson Allocation is archived | The Lesson Allocation shows Archived_At__c populated | Archived_At__c = current timestamp |
| 3 | HQ or CM Staff reopens L1's Student tab | S1 no longer appears in the student list at all, and the course-mismatch alert is no longer shown | S1 excluded from Lesson_GetLessonStudentsByLessonId's Is_Archived__c = false filter |
| 4 | A living Student Package Order reappears for S1's Course C2 Student Course, so the Lesson Allocation is unarchived on the same record Id | The Lesson Allocation shows Archived_At__c blank again | Archived_At__c = null (restored) |
| 5 | HQ or CM Staff reopens L1's Student tab | S1 reappears, and the course-mismatch alert is shown again, since the underlying mismatch was never resolved | S1 Is_Archived__c = FALSE (restored) → visible again; isCourseMismatch recomputed as TRUE |

**Severity:** minor
**Priority:** medium

---
