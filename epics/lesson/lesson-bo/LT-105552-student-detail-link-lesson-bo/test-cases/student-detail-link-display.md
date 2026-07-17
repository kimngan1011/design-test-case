# Test Cases: LT-105552 — Add Link to Student Detail Page from Lesson Detail in BO

## Suite: Student Detail Link — Display & Navigation

### Lesson Detail – Student List – Published Lesson – All Student Names Rendered as Hyperlinks

**Description:** AC 01.1 — Equivalence Partitioning — On a published lesson, every student name in the Student List section of the BO Lesson Detail page is displayed as a clickable hyperlink.

**Preconditions:**
- Logged in as HQ Staff to Back Office
- A published lesson exists with at least 2 students assigned (via active Lesson Allocation with Require Allocation = True)
- The HQ Staff user has Lesson view permission in BO

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to the Lesson List in Back Office and open the published lesson | The Lesson Detail page is displayed | Lesson status = Published |
| 2 | Scroll to the Student List section on the Lesson Detail page | The Student List section is visible with all assigned student names | At least 2 students assigned |
| 3 | Observe the appearance of each student name in the list | Each student name is rendered as a clickable hyperlink (visually distinct — underlined or styled as a link) | — |

**Severity:** major
**Priority:** high

---

### Lesson Detail – Student List – Draft Lesson – Student Names Rendered as Hyperlinks

**Description:** AC 01.1 — Decision Table (lesson status) — Student names in the Student List are rendered as hyperlinks on a Draft lesson, confirming the link is not restricted to Published status.

**Preconditions:**
- Logged in as HQ Staff to Back Office
- A Draft lesson exists with at least 1 student assigned
- The HQ Staff user has Lesson view permission in BO

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to the Lesson Detail page of a Draft lesson in Back Office | The Lesson Detail page is displayed | Lesson status = Draft |
| 2 | Scroll to the Student List section | The Student List section is visible with assigned student names | 1 student assigned |
| 3 | Observe the student name in the list | The student name is rendered as a clickable hyperlink | — |

**Severity:** minor
**Priority:** medium

---

### Lesson Detail – Student List – Completed Lesson – Student Names Rendered as Hyperlinks

**Description:** AC 01.1 — Decision Table (lesson status) — Student names in the Student List remain hyperlinks on a Completed lesson.

**Preconditions:**
- Logged in as HQ Staff to Back Office
- A Completed lesson exists with at least 1 student assigned
- The HQ Staff user has Lesson view permission in BO

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to the Lesson Detail page of a Completed lesson in Back Office | The Lesson Detail page is displayed | Lesson status = Completed |
| 2 | Scroll to the Student List section | The Student List section is visible with assigned student names | 1 student assigned |
| 3 | Observe the student name in the list | The student name is rendered as a clickable hyperlink | — |

**Severity:** minor
**Priority:** medium

---

### Lesson Detail – Student List – Cancelled Lesson – Student Names Rendered as Hyperlinks

**Description:** AC 01.1 — Decision Table (lesson status) — Student names in the Student List remain hyperlinks on a Cancelled lesson.

**Preconditions:**
- Logged in as HQ Staff to Back Office
- A Cancelled lesson exists with at least 1 student assigned (student was assigned before cancellation)
- The HQ Staff user has Lesson view permission in BO

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to the Lesson Detail page of a Cancelled lesson in Back Office | The Lesson Detail page is displayed | Lesson status = Cancelled |
| 2 | Scroll to the Student List section | The Student List section is visible with student names from before cancellation | 1 student assigned |
| 3 | Observe the student name in the list | The student name is rendered as a clickable hyperlink | — |

**Severity:** minor
**Priority:** medium

---

### Lesson Detail – Student List – Click Student Name – BO Student Detail Page Opens for Correct Student

**Description:** AC 01.1, SC 01 — Scenario — Clicking a student name hyperlink on the Lesson Detail page opens the BO Student Detail page for that specific student.

**Preconditions:**
- Logged in as HQ Staff to Back Office
- The HQ Staff user has Student view permission on Salesforce (full object read access)
- A published lesson exists with student A assigned (e.g., student A = "Nguyen Van A")
- The lesson's Student List is visible

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to the Lesson Detail page and scroll to the Student List section | Student A's name is visible as a hyperlink | Student A = "Nguyen Van A" |
| 2 | Click on student A's name hyperlink | The BO Student Detail page opens | — |
| 3 | Observe the student detail page header/title | The page shows student A's name and details | Page title or header = "Nguyen Van A" (or equivalent student identifier) |

**Severity:** critical
**Priority:** high

---

### Lesson Detail – Student List – Multiple Students – Each Name Links to Respective Student Detail Page

**Description:** AC 01.1 — Scenario — When multiple students are in the Student List, each student name links to that specific student's BO Student Detail page (not the same page for all).

**Preconditions:**
- Logged in as HQ Staff to Back Office
- The HQ Staff user has Student view permission on Salesforce
- A published lesson exists with student A and student B assigned (different students with different SF records)
- The lesson's Student List shows both students

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to the Lesson Detail page and scroll to the Student List | Student A and student B names are both visible as hyperlinks | Student A and Student B are different students |
| 2 | Click student A's name hyperlink | BO Student Detail page for student A opens | — |
| 3 | Navigate back to the Lesson Detail page | The Student List is displayed again with both student names | — |
| 4 | Click student B's name hyperlink | BO Student Detail page for student B opens | — |
| 5 | Compare the two student detail pages | The two pages show different students — student A's page does not display student B's information | Page for student A shows A's details; page for student B shows B's details |

**Severity:** major
**Priority:** high
