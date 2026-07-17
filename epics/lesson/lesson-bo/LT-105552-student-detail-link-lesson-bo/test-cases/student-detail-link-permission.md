# Test Cases: LT-105552 — Add Link to Student Detail Page from Lesson Detail in BO

## Suite: Student Detail Link — Permission & Access

### Lesson Detail – Student Detail Link – HQ Staff with Full Student Permission – Student Detail Page Opens with Edit Enabled

**Description:** AC 01.2, SC 02, SC 03 — Permission Matrix — An HQ Staff user with full Student object permission (read + edit) on Salesforce can open the BO Student Detail page and sees edit controls enabled.

**Preconditions:**
- Logged in as HQ Staff to Back Office
- The HQ Staff user's Salesforce permission set includes: Student object Read = TRUE, Student object Edit = TRUE
- A published lesson exists with at least 1 student assigned
- The student has an active Lesson Allocation (student + course record) linked to this lesson

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to the Lesson Detail page in Back Office | The Lesson Detail page is displayed with the Student List | — |
| 2 | Click a student name hyperlink in the Student List | The BO Student Detail page for that student opens | — |
| 3 | Observe the student detail page content and action controls | The student's full details are displayed; edit controls (e.g., Edit button or editable fields) are visible and enabled | SF permission: Student Read=TRUE, Edit=TRUE |

**Severity:** major
**Priority:** high

---

### Lesson Detail – Student Detail Link – HQ Staff with Student View-Only Permission – Student Detail Page Opens in Read-Only Mode

**Description:** AC 01.2, SC 02, SC 03 — Permission Matrix — An HQ Staff user with Student object read-only permission on Salesforce can open the BO Student Detail page but cannot edit student data.

**Preconditions:**
- Logged in as HQ Staff to Back Office
- The HQ Staff user's Salesforce permission set includes: Student object Read = TRUE, Student object Edit = FALSE
- A published lesson exists with at least 1 student assigned
- The student has an active Lesson Allocation linked to this lesson

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to the Lesson Detail page in Back Office | The Lesson Detail page is displayed with the Student List | — |
| 2 | Click a student name hyperlink in the Student List | The BO Student Detail page for that student opens | — |
| 3 | Observe the student detail page content and action controls | The student's details are visible; edit controls are absent or disabled — the user cannot modify student data | SF permission: Student Read=TRUE, Edit=FALSE |

**Severity:** major
**Priority:** high

---

### Lesson Detail – Student Detail Link – Teacher CPU with LA-Based Access but No Student Object Permission – Access Denied on Student Detail Page

**Description:** AC 01.2, AC 01.3 — Permission Matrix — A Teacher CPU user can see the student in the lesson Student List (because the student session is backed by a Lesson Allocation the teacher can read), but has no Salesforce Student object read permission. Clicking the link should result in an access denied or error state, not the student's data being exposed.

**Preconditions:**
- Logged in as Teacher (CPU role) to Back Office
- The Teacher is assigned to the lesson (the lesson appears in their BO Lesson list)
- The lesson has at least 1 student assigned — the student is visible in the Student List because the student has an active Lesson Allocation (student + course) for this lesson
- The Teacher CPU user's Salesforce permission set: Lesson Allocation Read = TRUE, Student Session Read = TRUE, **Student object Read = FALSE**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Log in as Teacher (CPU) to Back Office and navigate to the assigned lesson's Lesson Detail page | The Lesson Detail page is displayed; the Student List shows the student's name as a hyperlink (student is visible via Lesson Allocation) | Role = Teacher CPU; Student object permission = FALSE |
| 2 | Click the student name hyperlink in the Student List | The system attempts to open the BO Student Detail page | — |
| 3 | Observe the resulting page | An access denied message or error is shown — the student's personal data is NOT displayed; the teacher cannot view the Student Detail record | Expected: access-denied page or equivalent error state |

**Severity:** critical
**Priority:** high

---

### Lesson Detail – Student Detail Link – Teacher CPU with LA Access and Student View Permission – Student Detail Page Opens in Read-Only Mode

**Description:** AC 01.2, AC 01.3, SC 02 — Permission Matrix — A Teacher CPU user who has both Lesson Allocation read access (sees student in lesson list) AND Salesforce Student object read permission can open the student detail page in read-only mode.

**Preconditions:**
- Logged in as Teacher (CPU role) to Back Office
- The Teacher is assigned to the lesson
- The lesson has at least 1 student assigned with an active Lesson Allocation (student + course)
- The Teacher CPU user's Salesforce permission set: Lesson Allocation Read = TRUE, Student Session Read = TRUE, Student object Read = TRUE, Student object Edit = FALSE

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Log in as Teacher (CPU) to Back Office and navigate to the assigned lesson's Lesson Detail page | The Lesson Detail page is displayed; the student's name is shown as a hyperlink | Role = Teacher CPU; Student Read=TRUE, Edit=FALSE |
| 2 | Click the student name hyperlink | The BO Student Detail page for that student opens | — |
| 3 | Observe the student detail page content and action controls | The student's details are visible; edit controls are absent or disabled — the teacher can view but not modify student data | SF permission: Student Edit=FALSE |

**Severity:** major
**Priority:** high

---

### Lesson Detail – Student Detail Link – LBAC: Student Record at Different Location – Access Restricted When Opening Student Detail

**Description:** AC 01.2 — Permission Matrix (LBAC) — A Teacher SPU user can see a student in the lesson Student List because the student attends the lesson at the teacher's location. However, if the student's primary record is scoped to a different location (LBAC), the teacher may not have access to the full student detail page. This test confirms the LBAC restriction is applied when navigating to student detail.

**Preconditions:**
- Logged in as Teacher (SPU role) to Back Office — the teacher is scoped to Location A
- A lesson at Location A has student B assigned — student B's Lesson Allocation is for Location A (student attends lesson at teacher's location)
- Student B's primary student record in Salesforce is scoped to Location B (a different location the teacher does not manage)
- The Teacher SPU's LBAC restricts access to records at Location B

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Log in as Teacher (SPU, Location A) to Back Office and open the lesson at Location A | The Lesson Detail page is displayed; student B's name is visible in the Student List as a hyperlink (student is visible because lesson LA is at Location A) | Teacher location = Location A; Student's lesson location = Location A; Student's primary record location = Location B |
| 2 | Click student B's name hyperlink | The system attempts to open the BO Student Detail page for student B | — |
| 3 | Observe the resulting page | Access is restricted — either an access-denied page is shown, or the student detail opens with limited data (only the fields the teacher's LBAC at Location A allows to see) — student's records at Location B are NOT exposed | Expected: access denied or data-restricted view based on LBAC |

**Severity:** major
**Priority:** high

---

### Lesson Detail – Student Detail Link – Teacher SPU with Student View Permission – Student Detail Page Opens for Students in Scoped Location

**Description:** AC 01.3, SC 01, SC 02 — Permission Matrix — A Teacher SPU user with Student object read permission can open the BO Student Detail page for any student in the Student List within their location scope.

**Preconditions:**
- Logged in as Teacher (SPU role) to Back Office — the teacher is scoped to Location A
- The Teacher SPU's Salesforce permission set: Student object Read = TRUE, Student object Edit = FALSE
- A published lesson at Location A exists with at least 1 student assigned — the student's primary record is also at Location A (within the teacher's LBAC scope)

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Log in as Teacher (SPU, Location A) to Back Office and navigate to a lesson at Location A | The Lesson Detail page is displayed with the Student List | Role = Teacher SPU; Lesson location = Location A |
| 2 | Click a student name hyperlink in the Student List | The BO Student Detail page for that student opens | — |
| 3 | Observe the student detail page | The student's details are visible and consistent with the teacher's permission level (read-only); the page is not restricted | SF permission: Student Read=TRUE; student location = Location A (within scope) |

**Severity:** major
**Priority:** high
