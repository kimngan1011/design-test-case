# Test Cases: LT-107175 — Remote Attendance Status and Tag

## Suite: [Renseikai] Learner App — Remote Submission & Sync

### [Renseikai] Learner App – Submit Attendance – Eligible Student – Attended Remotely option available

**Description:** AC 04.1 — Permission Matrix — The exact option `Attended Remotely` is available.

**Preconditions:**

- published upcoming lesson APP-201 is enabled for Student audience.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Student opens Submit Attendance for APP-201 | The exact option `Attended Remotely` is available | APP-201; audience=Student; published=yes; upcoming=yes |

**Severity:** major
**Priority:** high

---

### [Renseikai] Learner App – Submit Attendance – Two students on one device – Each response belongs to the selected student

**Description:** AC 04.2 — State isolation — Switching between two students on one device saves each response to that student's own session in the same lesson.

**Preconditions:**

- Upcoming published lesson APP-212 is eligible for Student attendance submission.
- Student A and Student B are enrolled in APP-212.
- Both attendance responses are blank.
- The same device can switch between Student A and Student B accounts.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Student A signs in on the shared device, selects `Attended Remotely` for APP-212, and submits. | APP-212 saves `Attended Remotely` for Student A. | Student A; response=Attended Remotely |
| 2 | Student B signs in on the same device, selects `Attend` for APP-212, and submits. | APP-212 saves `Attend` for Student B. | Student B; response=Attend |
| 3 | HQ or CM Staff opens the Student Session records for both students in SF and BO. | Student A has Attendance Response `Attended Remotely` and Status `Remote`; Student B has Attendance Response and Status `Attend`. | same lesson=APP-212; students=Student A,Student B |

**Severity:** critical
**Priority:** high

---

### [Renseikai] Learner App – Submit Attendance – Parent switches between two students – Each response belongs to the selected student

**Description:** AC 04.2 — State isolation — A parent's selected learner controls which Student Session receives the submitted attendance response.

**Preconditions:**

- Upcoming published lesson APP-213 is eligible for Parent attendance submission.
- Parent P1 is linked to Student A and Student B, and both students are enrolled in APP-213.
- Both attendance responses are blank.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Parent P1 selects Student A, selects `Attended Remotely` for APP-213, and submits. | APP-213 saves `Attended Remotely` for Student A. | selected student=Student A; response=Attended Remotely |
| 2 | Parent P1 switches to Student B, selects `Attend` for APP-213, and submits. | APP-213 saves `Attend` for Student B. | selected student=Student B; response=Attend |
| 3 | HQ or CM Staff opens the Student Session records for both students in SF and BO. | Student A has Attendance Response `Attended Remotely` and Status `Remote`; Student B has Attendance Response and Status `Attend`. | same lesson=APP-213; parent=P1 |

**Severity:** critical
**Priority:** high

---
### [Renseikai] Learner App – Submit Attendance – Eligible Parent – Attended Remotely option available

**Description:** AC 04.1 — Permission Matrix — The exact option `Attended Remotely` is available.

**Preconditions:**

- published upcoming lesson APP-202 is enabled for Parent audience.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Parent of Student A opens Submit Attendance for APP-202 | The exact option `Attended Remotely` is available | APP-202; audience=Parent; published=yes; upcoming=yes |

**Severity:** major
**Priority:** high

---
### [Renseikai] Learner App – Submit Attendance – Student audience disabled – Option unavailable

**Description:** AC 04.1 — Negative — Attended Remotely is not available to the Student user.

**Preconditions:**

- published upcoming lesson APP-203 has Student audience disabled.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Student opens Submit Attendance for APP-203 | Attended Remotely is not available to the Student user | APP-203; audience=Student disabled; published=yes |

**Severity:** major
**Priority:** high

---
### [Renseikai] Learner App – Submit Attendance – Unpublished lesson – Option unavailable

**Description:** AC 04.1 — Negative — Submit Attendance and Attended Remotely are unavailable.

**Preconditions:**

- lesson APP-204 is upcoming but unpublished.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Student opens APP-204 in Learner App | Submit Attendance and Attended Remotely are unavailable | APP-204; published=no; upcoming=yes |

**Severity:** major
**Priority:** high

---
### [Renseikai] Learner App – Submit Attendance – Past lesson – Option unavailable

**Description:** AC 04.1 — Negative — Attended Remotely is unavailable under the unchanged past-lesson rule.

**Preconditions:**

- lesson APP-205 ended at 2026-09-10 08:00 JST (= 2026-09-09 23:00 UTC).

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Student opens APP-205 in Learner App | Attended Remotely is unavailable under the unchanged past-lesson rule | lesson_end=2026-09-10 08:00 JST (=2026-09-09 23:00 UTC) |

**Severity:** major
**Priority:** high

---
### [Renseikai] Learner App – Submit Attendance – JST to UTC date boundary – Eligibility preserved

**Description:** AC 04.1 — Boundary — Attended Remotely availability follows the existing eligible state despite different JST and UTC calendar dates.

**Preconditions:**

- published lesson APP-206 starts 2026-09-10 00:30 JST and is stored as 2026-09-09 15:30 UTC
- it is eligible in baseline configuration.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Student opens Submit Attendance for APP-206 using the Japan locale | The App interprets the stored UTC start as 2026-09-10 00:30 JST and shows Attended Remotely under the existing eligible state | lesson_start=2026-09-10 00:30 JST (=2026-09-09 15:30 UTC); audience=Student |

**Severity:** major
**Priority:** high

---
### [Renseikai] Learner App – Submission – Attended Remotely selected – Response persists in SF and BO

**Description:** AC 04.2 — Cross-system — Both surfaces show `Attended Remotely` as Option (Remark) for Student A.

**Preconditions:**

- APP-207 is eligible
- Student A response is blank and status is Attend.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Student selects Attended Remotely and submits, then opens SF and BO session details | Both surfaces show `Attended Remotely` as Option (Remark) for Student A | APP-207; response: blank→Attended Remotely |

**Severity:** critical
**Priority:** high

---
### [Renseikai] Learner App – Submission – Latest valid response – Final value retained

**Description:** AC 04.2 — Concurrency — SF and BO show Attend as the final response.

**Preconditions:**

- APP-208 is eligible
- current response is Attend.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Student submits Attended Remotely, then submit Attend as the later valid response | SF and BO show Attend as the final response | APP-208; ordered submissions=Attended Remotely then Attend |

**Severity:** critical
**Priority:** high

---
### [Renseikai] Learner App – Submission – Competing valid updates – Later submission wins

**Description:** AC 04.2 — Concurrency — SF and BO show Attended Remotely as the final response.

**Preconditions:**

- Student and Parent accounts for Student A can submit on APP-209.
- current response is blank.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Student submits Attend, then Parent submits Attended Remotely later | SF and BO show Attended Remotely as the final response | APP-209; ordered writers=Student Attend then Parent Attended Remotely |

**Severity:** critical
**Priority:** high

---
### [Renseikai] Learner App – Submission – Failed confirmation – No partial Remote state

**Description:** AC 04.2 / AC 05.1 — Negative — SF and BO retain Attend; no incomplete Remote or hidden-field state is shown.

**Preconditions:**

- APP-210 is eligible
- simulated submission failure is available
- current response is Attend.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Student submits Attended Remotely and receives the failure outcome | SF and BO retain Attend; no incomplete Remote status is shown; the initially visible Attendance Notice and Attendance Reason controls remain visible | APP-210; simulated failure; prior response=Attend |

**Severity:** critical
**Priority:** high

---
### [Renseikai] Learner App – Remote Sync – Remote status – Notice and Reason not shown

**Description:** AC 05.1 — State Transition — Status is Remote; Attendance Notice and Attendance Reason are not shown; no clearing of stored values is asserted.

**Preconditions:**

- APP-211 is eligible
- Student A status is Attend and dependent controls are visible in BO.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Student submits Attended Remotely, then opens BO Collect Attendance | Status is Remote; Attendance Notice and Attendance Reason are not shown; no clearing of stored values is asserted | APP-211; response=Attended Remotely; status=Remote |

**Severity:** major
**Priority:** high

---
