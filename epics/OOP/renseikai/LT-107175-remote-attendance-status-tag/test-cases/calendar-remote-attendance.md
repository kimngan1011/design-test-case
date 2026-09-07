# Test Cases: LT-107175 — Remote Attendance Status and Tag

## Suite: [Renseikai] Calendar — Remote Attendance

### [Renseikai] Calendar – Group Lesson Card – One Remote learner – Remote dot shown

**Description:** AC 01.1 — Decision Table — The lesson card shows the Remote dot.

**Preconditions:**

- group lesson G-100 has Student A status Remote and Student B status Attend.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff opens group lesson G-100 in Calendar | The lesson card shows the Remote dot | G-100; A=Remote; B=Attend |

**Severity:** major
**Priority:** high

---
### [Renseikai] Calendar – Individual Lesson Card – Learner status Remote – Remote dot shown

**Description:** AC 01.1 — Decision Table — The lesson card shows the Remote dot.

**Preconditions:**

- individual lesson I-100 Student A has status Remote.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff opens individual lesson I-100 in Calendar | The lesson card shows the Remote dot | I-100; A=Remote |

**Severity:** major
**Priority:** high

---
### [Renseikai] Calendar – Lesson Card – Competing indicators – Remote takes highest priority

**Description:** AC 01.1 — Scenario — Remote has higher Calendar precedence than New, Trial, Seasonal, Reallocated, and Absent.

**Preconditions:**

- group lesson G-101 contains learners with Remote, New, Trial, Seasonal, Reallocated, and Absent indicators.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff opens G-101 in Calendar | Only the Remote dot is shown; Remote has higher precedence than New, Trial, Seasonal, Reallocated, and Absent | G-101; indicators=Remote,New,Trial,Seasonal,Reallocated,Absent |

**Severity:** major
**Priority:** high

---
### [Renseikai] Calendar – Lesson Card – Remote absent with New learner – New indicator retained

**Description:** AC 01.2 — Regression — No Remote dot is shown and the New indicator remains.

**Preconditions:**

- group lesson G-102 has no Remote learner and one New learner.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff opens G-102 in Calendar | No Remote dot is shown and the New indicator remains | G-102; indicators=New only |

**Severity:** major
**Priority:** high

---
### [Renseikai] Calendar – Lesson Card – Remote absent with Absent learner – Absent indicator retained

**Description:** AC 01.2 — Regression — No Remote dot is shown and the Absent indicator remains.

**Preconditions:**

- group lesson G-103 has no Remote learner and one Absent learner.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff opens G-103 in Calendar | No Remote dot is shown and the Absent indicator remains | G-103; indicators=Absent only |

**Severity:** major
**Priority:** high

---
### [Renseikai] Calendar – Lesson Detail – Mixed learner roster – Remote tag assigned to Remote learner

**Description:** AC 01.3 — Component — Remote tag appears beside Student A only.

**Preconditions:**

- G-104 has Student A status Remote and Student B status Attend.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff opens Calendar lesson detail for G-104 | Remote tag appears beside Student A only | G-104; A=Remote; B=Attend |

**Severity:** minor
**Priority:** medium

---
### [Renseikai] Calendar – Lesson Detail – Remote changed to Attend – Remote tag removed

**Description:** AC 01.3 — State Transition — Student A has no Remote tag.

**Preconditions:**

- Student A in G-105 is Remote, then is changed to Attend.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff opens Calendar lesson detail after the saved Attend update | Student A has no Remote tag | G-105; A: Remote→Attend |

**Severity:** minor
**Priority:** medium

---
### [Renseikai] Calendar – Legend – English locale – Remote label and Indigo token shown

**Description:** AC 01.4 — Component — Legend shows `Remote` with Vibrant/Indigo/40 dot.

**Preconditions:**

- English locale is available.
- Calendar is available.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff opens Calendar legend in English locale. | Legend shows `Remote` with Vibrant/Indigo/40 dot | locale=EN |

**Severity:** minor
**Priority:** medium

---
### [Renseikai] Calendar – Legend – Japanese locale – Remote label and Indigo token shown

**Description:** AC 01.4 — Component — Legend shows `リモート参加` with Vibrant/Indigo/40 dot.

**Preconditions:**

- Japanese locale is available.
- Calendar is available.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff opens Calendar legend in Japanese locale. | Legend shows `リモート参加` with Vibrant/Indigo/40 dot | locale=JP |

**Severity:** minor
**Priority:** medium

---
### [Renseikai] Calendar – Status Readback – Salesforce saves Remote – Group card updates

**Description:** AC 01.1 — Cross-system — G-106 group card shows the Remote dot.

**Preconditions:**

- Student A in G-106 has status Attend.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff sets Student A Attendance Status to Remote in Salesforce and saves | G-106 group card shows the Remote dot | G-106; A: Attend→Remote in Salesforce |

**Severity:** major
**Priority:** high

---
### [Renseikai] Calendar – Status Readback – BO Lesson Detail saves Remote – Individual card updates

**Description:** AC 01.1 — Cross-system — I-106 card shows the Remote dot.

**Preconditions:**

- individual lesson I-106 Student A has status Attend.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff saves Remote for Student A from BO Lesson Detail, then opens Calendar | I-106 card shows the Remote dot | I-106; A: Attend→Remote in BO Lesson Detail |

**Severity:** major
**Priority:** high

---
### [Renseikai] Calendar – Status Readback – BO Report saves Remote – Calendar detail updates

**Description:** AC 03.2 — Cross-system — Student A has the Remote tag.

**Preconditions:**

- Student A in G-107 has status Attend and a BO Report is available.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff saves Remote from Collect Attendance in Report, then opens Calendar detail | Student A has the Remote tag | G-107; A: Attend→Remote in BO Report |

**Severity:** major
**Priority:** high

---
### [Renseikai] Calendar – Status Readback – BO Lesson Report Detail saves Remote – Calendar detail updates

**Description:** AC 03.2 — Cross-system — Student A has the Remote tag.

**Preconditions:**

- Student A in G-108 has status Attend and Lesson Report Detail is available.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff saves Remote from Lesson Report Detail, then opens Calendar detail | Student A has the Remote tag | G-108; A: Attend→Remote in Lesson Report Detail |

**Severity:** major
**Priority:** high

---
### [Renseikai] Calendar – Bulk Collect Attendance – Remote selected – Attendance Reason saved

**Description:** AC 03.1 / 03.2 — State Transition — Student A status is Remote, Attendance Reason is selected, and Calendar card shows Remote.

**Preconditions:**

- Calendar bulk attendance for G-109 is editable
- Student A is Attend.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff selects Remote for Student A, chooses `Club Activities` as Attendance Reason, and saves in Calendar Bulk Collect Attendance. | Student A status is Remote; Attendance Reason is `Club Activities`; Calendar card shows Remote. | G-109; Student A: Attend→Remote; Reason=Club Activities |

**Severity:** major
**Priority:** high

---
### [Renseikai] Calendar – App Submission Sync – Attended Remotely submitted – Calendar Remote state shown

**Description:** AC 05.1 — Cross-system — Calendar shows Remote dot and Student A has Remote tag.

**Preconditions:**

- published upcoming lesson G-110 is eligible
- Student A status is Attend.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Student submits `Attended Remotely` in Learner App, then opens G-110 in Calendar | Calendar shows Remote dot and Student A has Remote tag | G-110; A App response=Attended Remotely |

**Severity:** critical
**Priority:** high

---

### [Renseikai] Calendar – Bulk Collect Attendance – Draft lesson – Remote change blocked

**Description:** AC 03.1 — Negative — Calendar Bulk Collect Attendance retains the existing Draft guard for Remote.

**Preconditions:**

- Calendar bulk attendance for draft lesson G-111 is open and Student A has status Attend.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff attempts to select and save `Remote` for Student A from Calendar Bulk Collect Attendance. | Draft guard prevents the attendance change and Student A remains Attend. | G-111; lesson status=Draft; A=Attend; option=Remote |

**Severity:** major
**Priority:** high

---
