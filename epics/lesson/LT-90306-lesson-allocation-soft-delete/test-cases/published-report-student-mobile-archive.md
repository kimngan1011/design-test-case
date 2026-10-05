# Test Cases: LT-90306 — Lesson Allocation Soft Delete (Archive)

Source Qase suite reviewed: [PX suite 450 — "View lesson and lesson report"](https://app.qase.io/project/PX?suite=450) (6 existing cases, under parent 320), subsequently confirmed as the home suite for this customer-facing impact area originally raised by the reviewer's question "khi report đã Published luôn" (what happens when the report is already Published). None of the 6 existing cases (which cover feature-flag layout switching, Draft/reverted-report hiding, lesson-info sync, and newly-added-student visibility) test an archived Lesson Allocation.

Code trace: Student Mobile reads a published lesson report via `flutterCommunicate.js` → `LessonMiddlewareHandler.getLessonReportDetail` → `LessonDataHandlerOutSide.getLessonReportDetailFromStudentSession` (`outside-packages/dlrs/main/default/classes/lesson/LessonDataHandlerOutSide.cls:95-171`). This method first gates on `Lesson_Report__c.Lesson_Report_Status__c == 'Published'` (line 115), then queries `Student_Sessions__c` live — **individual lesson branch** (lines 117-132) and **group lesson branch** (lines 154-162) both filter `Is_Deleted__c = FALSE AND Is_Archived__c = FALSE`. There is no snapshot, cache, or frozen copy of Published report data anywhere in the codebase (confirmed by search) — a Published report is read live from `Student_Sessions__c` on every single mobile fetch, exactly like a Draft or Submitted one, and is therefore **equally susceptible to disappearing the moment the student's Lesson Allocation is archived**, even though the parent/student has already seen it published once.

The effect differs by teaching method:
- **Individual lesson**: the entire per-student loop (lines 117-141) never executes once archived, so the mobile response comes back essentially empty — not just the report fields, but `lessonReportStatus` itself disappears, since that field is also only set inside this same loop for individual lessons.
- **Group lesson**: lesson-level fields (`content`, `homework`, `announcement`, `lessonReportStatus`) are set unconditionally from `Lesson_Report__c` (lines 146-150), so they still render — but the archived student's own `homeworkCompletion`, `inLessonQuiz`, `understanding` fields (set only inside the archive-filtered loop, lines 154-166) silently disappear/null out for that one student, while any other non-archived student in the same group report is unaffected. This produces a visibly inconsistent result: the lesson shows report content but the one student's personal fields are gone.

This directly echoes the lesson-learned pattern already on file for this epic (Nichibei 2026-03-04 missing-LA-points incident — families losing visibility into academic records) and should be flagged in spec.md's Conflict & Gap Analysis if not already covered.

## Suite: Student Mobile — Published Lesson Report Visibility (suite TBD)

### Published Lesson Report – Individual Lesson – Student's Lesson Allocation Archived After Publish – Report Disappears Entirely from Student Mobile; Restored – Reappears Fully

**Description:** Gap case — Decision Table — an Individual lesson report already Published and visible to the student/parent on Student Mobile disappears completely from the mobile app once the student's Lesson Allocation is archived, because `getLessonReportDetailFromStudentSession`'s individual-lesson query loop (the sole source of both the report content fields and `lessonReportStatus` for this teaching method) excludes archived sessions with no fallback — the family sees the report vanish with no explanation. It reappears in full once the Lesson Allocation is restored.

**Preconditions:**
- Student A has an Individual lesson with a Published lesson report: Content = "Great improvement in reading", Understanding = "Good", Homework Completion = "Done", In-lesson Quiz = "9/10". Student A (or their parent) has already viewed this report on Student Mobile.
- Student A has an active (non-archived) Lesson Allocation for this course.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Student/Parent opens the lesson on Student Mobile and views the Published report | Report shows Content = "Great improvement in reading", Understanding = "Good", Homework Completion = "Done", In-lesson Quiz = "9/10"; lessonReportStatus = Published | getLessonReportDetailFromStudentSession returns full individual-lesson payload |
| 2 | The Student Package Order behind Student A's Lesson Allocation is fully removed, so the Lesson Allocation is archived | The Lesson Allocation shows Archived_At__c populated | Archived_At__c = current timestamp |
| 3 | Student/Parent reopens the same lesson's report on Student Mobile | The report appears empty — Content, Understanding, Homework Completion, In-lesson Quiz, and even the Published status indicator are all gone, with no error or explanation shown | Student A Is_Archived__c = TRUE (via formula) → the individual-lesson query loop (lines 117-141) returns zero rows, so response stays empty including lessonReportStatus |
| 4 | A living Student Package Order reappears for Student A's Student Course, so the Lesson Allocation is unarchived on the same record Id | The Lesson Allocation shows Archived_At__c blank again | Archived_At__c = null (restored) |
| 5 | Student/Parent reopens the same lesson's report on Student Mobile | The report reappears in full — Content = "Great improvement in reading", Understanding = "Good", Homework Completion = "Done", In-lesson Quiz = "9/10", lessonReportStatus = Published — identical to step 1 | Student A Is_Archived__c = FALSE (restored) → the same Student_Sessions__c record is read again, values unchanged |

**Severity:** critical
**Priority:** high

---

### Published Lesson Report – Group Lesson – One Student's Lesson Allocation Archived After Publish – That Student's Personal Fields Disappear While Lesson Content Still Shows; Other Students Unaffected; Restored – Student's Fields Reappear

**Description:** Gap case — Decision Table, contrasts with the Individual-lesson case above — for a Group lesson, archiving one student's Lesson Allocation after Publish produces a visibly inconsistent result rather than a fully empty one: lesson-level fields (`content`, `homework`, `announcement`, `lessonReportStatus`) are set unconditionally from `Lesson_Report__c` and keep showing, but that one student's personal fields (`homeworkCompletion`, `inLessonQuiz`, `understanding`) silently disappear, while a different, non-archived student in the same group report is completely unaffected.

**Preconditions:**
- A Group lesson has a Published lesson report with Content = "Chapter 5 practice", shared Homework = "Workbook p.20-22". Student A and Student B both have personal fields filled: Student A — Understanding = "Excellent", In-lesson Quiz = "10/10"; Student B — Understanding = "Fair", In-lesson Quiz = "6/10".
- Both students have active (non-archived) Lesson Allocations.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Student A's and Student B's parents each open the lesson's report on Student Mobile | Both see Content = "Chapter 5 practice", Homework = "Workbook p.20-22", lessonReportStatus = Published, plus their own child's Understanding/In-lesson Quiz values | Student A: Understanding = Excellent, Quiz = 10/10; Student B: Understanding = Fair, Quiz = 6/10 |
| 2 | The Student Package Order behind Student A's Lesson Allocation is fully removed, so the Lesson Allocation is archived | The Lesson Allocation shows Archived_At__c populated | Archived_At__c = current timestamp |
| 3 | Student A's parent reopens the report on Student Mobile | Content, Homework, and lessonReportStatus still show normally (these come from Lesson_Report__c directly, not the archived-filtered loop), but Understanding and In-lesson Quiz for Student A are now missing/null — an inconsistent partial result | Student A Is_Archived__c = TRUE → excluded from the per-student loop (lines 154-166), but lesson-level fields (lines 146-150) are unaffected |
| 4 | Student B's parent reopens the same report on Student Mobile at the same time | Student B still sees everything correctly: Content, Homework, lessonReportStatus, and their own Understanding = "Fair", In-lesson Quiz = "6/10" — completely unaffected by Student A's archive | Student B Is_Archived__c = FALSE → unaffected by another student's LA archive |
| 5 | A living Student Package Order reappears for Student A's Student Course, so the Lesson Allocation is unarchived on the same record Id, and Student A's parent reopens the report | Student A's Understanding = "Excellent" and In-lesson Quiz = "10/10" reappear, restoring full consistency with Content and Homework | Student A Is_Archived__c = FALSE (restored) → per-student loop includes Student A again, same values as step 1 |

**Severity:** major
**Priority:** high

---
