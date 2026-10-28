# Test Cases: LT-108382 — Student Lesson Report with Classroom

## Suite: Report Entry and Access

### Student Lesson Report – Student Detail – Authorized Centre Staff – Opens the selected student's report

**Description:** AC 01.1 — Permission Matrix — An authorized Centre Staff member opens the report from the selected Student detail page.

**Preconditions:**

- Centre Staff A is logged in to Salesforce and has permission to view Student A at Tokyo Center.
- Student A has one current-academic-year lesson at Tokyo Center.
- The Student A detail page contains the Student Lesson Report entry point.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Centre Staff A opens the Student A detail page. | The Student A detail page identifies Student A and shows the Student Lesson Report entry point. | Student = Student A; Location = Tokyo Center |
| 2 | Centre Staff A selects the Student Lesson Report entry point. | Salesforce opens a report scoped to Student A. | Report context = Student A |
| 3 | Centre Staff A reads the report row. | The row belongs to Student A and includes the prepared current-academic-year lesson. | Lesson = Lesson Tokyo 01 |

**Severity:** major
**Priority:** high

---

### Student Lesson Report – Student Detail – Restricted-location staff – Does not expose another center's report

**Description:** AC 01.1 — Permission Matrix / Negative — A staff member without access to Student A's location cannot read Student A's report data.

**Preconditions:**

- Centre Staff B is logged in to Salesforce with access to Osaka Center only.
- Student A belongs to Tokyo Center.
- Student A has one current-academic-year lesson at Tokyo Center.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Centre Staff B attempts to open the Student A detail page. | Salesforce denies access or does not expose Student A's record. | Staff location = Osaka Center; Student location = Tokyo Center |
| 2 | Centre Staff B attempts to open the Student Lesson Report from any available Student A route. | Salesforce does not display Student A's lesson or attendance data. | Student = Student A |

**Severity:** major
**Priority:** high

---

### Student Lesson Report – Student Detail – User without report permission – Keeps the report unavailable

**Description:** AC 01.1 — Permission Matrix / Negative — A user lacking report permission cannot open the Student Lesson Report.

**Preconditions:**

- User C is logged in to Salesforce without the permission that grants Student Lesson Report access.
- Student A is visible to User C through a permitted non-report route.
- Student A has one current-academic-year lesson.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | User C opens the Student A detail page. | The Student A detail page opens without exposing report data. | Student = Student A |
| 2 | User C inspects the Student Lesson Report entry point. | The entry point is unavailable, disabled, or opening it is denied without displaying Student A's report rows. | User permission = Report access absent |

**Severity:** major
**Priority:** high
