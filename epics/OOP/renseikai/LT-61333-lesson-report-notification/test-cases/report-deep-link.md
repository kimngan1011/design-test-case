# Test Cases: LT-61333 — Lesson Report Notification

## Suite: Report Deep-link and Student Context

### [Renseikai] Lesson Report Notification – View Report Detail – Student notification – Intended report opened
**Description:** REQ-04 — Regression — The Student CTA opens the notification's report rather than Lesson Detail.
**Preconditions:**
- Report R-401 for Math K is eligible and its notification is present for logged-in Student A.
- Student A can view R-401 in the Learner App.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Student A opens the notification for R-401. | Student A sees View Report Detail. | CTA=View Report Detail |
| 2 | Student A selects View Report Detail. | Learner App opens the lesson-report section for R-401. | report=R-401; lesson=Math K |
| 3 | Student A reads the destination header. | Destination identifies Math K's report and not a generic Lesson Detail page. | expected=Math K report |
**Severity:** major
**Priority:** high

### [Renseikai] Lesson Report Notification – Parent Context – Student B active – Student A report opened
**Description:** REQ-04 — State Transition — Parent context changes to the notified child before report navigation.
**Preconditions:**
- Parent P is logged in to the Parent App with Student B currently active.
- Parent P is the Default Parent for Student A and Student B.
- Report R-402 for Student A is eligible and its notification is present.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Parent P opens the notification for Student A's R-402. | Parent App changes the active student from Student B to Student A. | from=Student B; to=Student A |
| 2 | Parent P selects View Report Detail. | Parent App opens R-402 in Student A's report section. | report=R-402 |
| 3 | Parent P reads the active student and report identity. | Active student is Student A and the displayed report belongs to Student A. | expected_student=Student A |
**Severity:** critical
**Priority:** high

### [Renseikai] Lesson Report Notification – Report fields – Multiple Students in One Lesson – Student and Parent values are isolated
**Description:** REQ-04 — Data Integrity — Learner and Parent Apps render the notified Student's exact report values when Student A and Student B attend the same lesson.
**Preconditions:**
- Student A and Student B both have a Published report for Math L, and a notification exists for each Student and for their Default Parent P.
- Math L report for Student A has Homework Completion=90%, Total Score=88, Test Result=Pass, Understanding=Excellent.
- Math L report for Student B has Homework Completion=60%, Total Score=65, Test Result=Needs Improvement, Understanding=Developing.
- Parent P is the Default Parent of Student A and Student B, with Student B currently active.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Student A opens Student A's Math L notification and selects View Report Detail. | Learner App identifies Student A and displays Homework Completion=90%, Total Score=88, Test Result=Pass, and Understanding=Excellent. | report=R-404-A; lesson=Math L |
| 2 | Student B opens Student B's Math L notification and selects View Report Detail. | Learner App identifies Student B and displays Homework Completion=60%, Total Score=65, Test Result=Needs Improvement, and Understanding=Developing. Student A's values are not displayed. | report=R-404-B; lesson=Math L |
| 3 | Parent P, while Student B is active, opens Student A's Math L notification and selects View Report Detail. | Parent App switches active student to Student A before render and displays exactly Student A's four values. | from=Student B; to=Student A; report=R-404-A |
| 4 | Parent P opens Student B's Math L notification and selects View Report Detail. | Parent App switches active student to Student B before render and displays exactly Student B's four values. Student A's values are not displayed. | from=Student A; to=Student B; report=R-404-B |
**Severity:** critical
**Priority:** high

### [Renseikai] Lesson Report Notification – Report fields – Multiple Students in Multiple Lessons – Student and Parent values map to each report
**Description:** REQ-02 and REQ-04 — Data Integrity — Each report notification opens the correct Student/lesson record with its own report-field values.
**Preconditions:**
- Student A and Student B each have Published reports for Math M and Science N; notifications exist for each Student and Default Parent P.
- R-405-A-Math: Student A, Math M, Homework Completion=95%, Total Score=92, Test Result=Pass, Understanding=Excellent.
- R-405-A-Science: Student A, Science N, Homework Completion=80%, Total Score=84, Test Result=Pass, Understanding=Good.
- R-405-B-Math: Student B, Math M, Homework Completion=70%, Total Score=72, Test Result=Pass, Understanding=Good.
- R-405-B-Science: Student B, Science N, Homework Completion=50%, Total Score=58, Test Result=Needs Improvement, Understanding=Developing.
- Parent P is the Default Parent of both Students and starts with Student B active.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Each Student opens both of their report notifications and selects View Report Detail. | Student A sees Math M: Homework Completion=95%, Total Score=92, Test Result=Pass, Understanding=Excellent; and Science N: 80%, 84, Pass, Good. Student B sees Math M: 70%, 72, Pass, Good; and Science N: 50%, 58, Needs Improvement, Developing. Each destination matches the notification's report and lesson. | reports=R-405-A-Math;R-405-A-Science;R-405-B-Math;R-405-B-Science |
| 2 | Parent P opens Student A's Math M notification and selects View Report Detail. | Parent App switches to Student A and displays Homework Completion=95%, Total Score=92, Test Result=Pass, Understanding=Excellent for Math M. | from=Student B; to=Student A; report=R-405-A-Math |
| 3 | Parent P opens Student A's Science N notification and selects View Report Detail. | Parent App remains/switches to Student A and displays Homework Completion=80%, Total Score=84, Test Result=Pass, Understanding=Good for Science N; the Math M values are not reused. | report=R-405-A-Science |
| 4 | Parent P opens Student B's Math M and Science N notifications and selects View Report Detail for each. | Parent App switches to Student B and displays Math M: Homework Completion=70%, Total Score=72, Test Result=Pass, Understanding=Good; and Science N: 50%, 58, Needs Improvement, Developing. No report is associated with the wrong Student or lesson. | to=Student B; reports=R-405-B-Math;R-405-B-Science |
**Severity:** critical
**Priority:** high

### [Renseikai] Lesson Report Notification – Parent Context – Stale Student B state – Student A report not exposed under Student B
**Description:** REQ-04 — Permission Matrix Negative — The app does not render Student A data in Student B context.
**Preconditions:**
- Parent P is logged in with Student B active.
- Parent P has a notification for Student A's R-403.
- Student A and Student B have different report lesson names.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Parent P opens the notification for Student A's R-403. | Parent App resolves Student A as the active student before content loads. | target=Student A |
| 2 | Parent P selects View Report Detail. | Parent App does not show Student A's report while Student B remains active. | prohibited_context=Student B |
| 3 | Parent P reads the displayed report. | Displayed report is Student A's R-403, or access is denied without exposing either student's incorrect report. | report=R-403 |
**Severity:** critical
**Priority:** high
