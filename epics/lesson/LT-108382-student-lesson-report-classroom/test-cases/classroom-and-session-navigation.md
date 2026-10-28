# Test Cases: LT-108382 — Student Lesson Report with Classroom

## Suite: Classroom and Student Session Navigation

### Student Lesson Report – Lesson Classroom – Two lessons with distinct classrooms – Maps each row to its source classroom

**Description:** AC 02.3 — CRUD/readback / Regression — Each lesson row displays the Classroom related to that exact Lesson.

**Preconditions:**

- Centre Staff A is logged in to Salesforce with access to Student A.
- Student A has Lesson Tokyo 01 in the current academic year with Classroom Room A.
- Student A has Lesson Tokyo 02 in the current academic year with Classroom Room B.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Centre Staff A opens Student A's Student Lesson Report. | The report opens with rows for Lesson Tokyo 01 and Lesson Tokyo 02. | Student = Student A |
| 2 | Centre Staff A reads the Lesson Classroom value for Lesson Tokyo 01. | Lesson Tokyo 01 displays Room A in Lesson Classroom. | Lesson Tokyo 01 → Room A |
| 3 | Centre Staff A reads the Lesson Classroom value for Lesson Tokyo 02. | Lesson Tokyo 02 displays Room B in Lesson Classroom. | Lesson Tokyo 02 → Room B |

**Severity:** major
**Priority:** high

---

### Student Lesson Report – Student Session – Report row link – Opens the matching Student Session detail

**Description:** AC 02.4 — Scenario / Regression — The Student Session link opens the exact Student Session represented by its report row.

**Preconditions:**

- Centre Staff A is logged in to Salesforce with access to Student A.
- Student A has Lesson Tokyo 01 in the current academic year.
- Student Session SS-A01 links Student A to Lesson Tokyo 01.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Centre Staff A opens Student A's Student Lesson Report. | The report shows the Lesson Tokyo 01 row with Student Session SS-A01. | Student Session = SS-A01 |
| 2 | Centre Staff A selects the Student Session value in the Lesson Tokyo 01 row. | Salesforce opens the detail page for Student Session SS-A01. | Source row = Lesson Tokyo 01 |
| 3 | Centre Staff A reads the Student and Lesson values on the destination page. | The destination identifies Student A and Lesson Tokyo 01, matching the source report row. | Student = Student A; Lesson = Lesson Tokyo 01 |

**Severity:** minor
**Priority:** medium

---

### Student Lesson Report – Student Session – Restricted detail – Does not reveal an inaccessible session

**Description:** AC 02.4 — Permission Matrix / Negative — A restricted staff user cannot use a Student Session link to reveal unavailable session data.

**Preconditions:**

- Centre Staff B is logged in to Salesforce with Osaka Center access only.
- Student Session SS-A01 belongs to Student A at Tokyo Center.
- A report route containing the SS-A01 link is available to Centre Staff B only through a stale bookmark or direct navigation attempt.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Centre Staff B attempts to open Student Session SS-A01 through the report link or direct route. | Salesforce denies access or does not display the SS-A01 detail. | Staff location = Osaka Center; Session location = Tokyo Center |
| 2 | Centre Staff B reads the resulting page state. | The page does not reveal Student A's lesson, attendance, or Student Session values. | Student Session = SS-A01 |

**Severity:** major
**Priority:** high
