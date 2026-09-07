# Test Cases: LT-107175 — Remote Attendance Status and Tag

## Suite: [Renseikai] Collect Attendance — Remote

### [Renseikai] Collect Attendance – Lesson Detail – Editable lesson – Remote option available

**Description:** AC 03.1 — Component — The exact option `Remote` is available for Student A.

**Preconditions:**

- Lesson Detail for CA-101 is editable and Student A is Attend.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff opens Collect Attendance from Lesson Detail | The exact option `Remote` is available for Student A | CA-101; entry=Lesson Detail |

**Severity:** major
**Priority:** high

---
### [Renseikai] Collect Attendance – Report – Editable report – Remote option available

**Description:** AC 03.1 — Component — The exact option `Remote` is available for Student A.

**Preconditions:**

- Report for CA-102 is editable and Student A is Attend.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff opens Collect Attendance from Report | The exact option `Remote` is available for Student A | CA-102; entry=Report |

**Severity:** major
**Priority:** high

---
### [Renseikai] Collect Attendance – Lesson Report Detail – Editable report – Remote option available

**Description:** AC 03.1 — Component — The exact option `Remote` is available for Student A.

**Preconditions:**

- Lesson Report Detail for CA-103 is editable and Student A is Attend.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff opens Collect Attendance from Lesson Report Detail | The exact option `Remote` is available for Student A | CA-103; entry=Lesson Report Detail |

**Severity:** major
**Priority:** high

---
### [Renseikai] Collect Attendance – Lesson Detail – Draft lesson – Remote change blocked

**Description:** AC 03.1 — Negative — Draft guard prevents the attendance change.

**Preconditions:**

- Lesson Detail for draft lesson CA-104 is open.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff attempts to select and save Remote | Draft guard prevents the attendance change | CA-104; lesson status=Draft; option=Remote |

**Severity:** major
**Priority:** high

---
### [Renseikai] Collect Attendance – Report – Draft report – Remote change blocked

**Description:** AC 03.1 — Negative — Draft guard prevents the attendance change.

**Preconditions:**

- Report for draft lesson CA-105 is open.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff attempts to select and save Remote | Draft guard prevents the attendance change | CA-105; lesson status=Draft; option=Remote |

**Severity:** major
**Priority:** high

---
### [Renseikai] Collect Attendance – Lesson Report Detail – Draft report – Remote change blocked

**Description:** AC 03.1 — Negative — Draft guard prevents the attendance change.

**Preconditions:**

- Lesson Report Detail for draft lesson CA-106 is open.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff attempts to select and save Remote | Draft guard prevents the attendance change | CA-106; lesson status=Draft; option=Remote |

**Severity:** major
**Priority:** high

---
### [Renseikai] Collect Attendance – Lesson Detail – Remote saved – BO and Salesforce readback match

**Description:** AC 03.2 — State Transition — Attendance Reason can be selected with Remote and both values persist on reread.

**Preconditions:**

- editable lesson CA-107 Student A status is Attend.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff selects Remote and `Club Activities` as Attendance Reason from Lesson Detail, then saves and reopens BO and Salesforce session details. | BO and Salesforce show Attendance Status `Remote` and Attendance Reason `Club Activities`. | CA-107; Student A: Attend→Remote; Reason=Club Activities |

**Severity:** major
**Priority:** high

---
### [Renseikai] Collect Attendance – Report – Remote saved – BO and Salesforce readback match

**Description:** AC 03.2 — State Transition — Attendance Reason can be selected with Remote and both values persist on reread.

**Preconditions:**

- editable report CA-108 Student A status is Attend.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff selects Remote and `Club Activities` as Attendance Reason from Report, then saves and reopens BO and Salesforce session details. | BO and Salesforce show Attendance Status `Remote` and Attendance Reason `Club Activities`. | CA-108; Student A: Attend→Remote; Reason=Club Activities |

**Severity:** major
**Priority:** high

---
### [Renseikai] Collect Attendance – Lesson Report Detail – Remote saved – BO and Salesforce readback match

**Description:** AC 03.2 — State Transition — Attendance Reason can be selected with Remote and both values persist on reread.

**Preconditions:**

- editable report detail CA-109 Student A status is Attend.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff selects Remote and `Club Activities` as Attendance Reason from Lesson Report Detail, then saves and reopens BO and Salesforce session details. | BO and Salesforce show Attendance Status `Remote` and Attendance Reason `Club Activities`. | CA-109; Student A: Attend→Remote; Reason=Club Activities |

**Severity:** major
**Priority:** high

---
### [Renseikai] Collect Attendance – Remote state – Attendance Reason – Selector shown and saved

**Description:** AC 03.2 — State Transition — Attendance Reason is shown after Remote is selected and can be saved.

**Preconditions:**

- editable lesson CA-110 Student A is Attend.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff selects Remote for Student A in Collect Attendance. | Attendance Reason selector is shown. | CA-110; Student A: Attend→Remote |
| 2 | Select `Club Activities` as Attendance Reason, save, and reopen the form. | Student A shows Remote and Attendance Reason `Club Activities`. | Reason=Club Activities |

**Severity:** major
**Priority:** high

---
