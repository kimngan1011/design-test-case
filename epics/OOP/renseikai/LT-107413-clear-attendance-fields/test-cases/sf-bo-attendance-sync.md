# Test Cases: LT-107413 — Clear Attendance Notice and Attendance Reason in Salesforce

## Suite: [Renseikai] Salesforce-to-Back Office Attendance Synchronization

### [Renseikai] Attendance Synchronization – Salesforce to Back Office – Absent to Attend saved – Cleared values reflected

**Description:** AC 04 — Decision Table and Regression — A saved SF correction from Absent to Attend appears in BO with both absence fields blank.

**Preconditions:**

- Logged in as HQ or CM Staff to the Renseikai Salesforce org and as HQ Staff to Back Office.
- Published Lesson `RSK-SYNC-001` contains Student `Student O`.
- Student O's Student Session has Attendance Status `Absent`, Attendance Reason `Traffic Issue`, and Attendance Notice `No Contact` in Salesforce.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | In Salesforce, open Student O's Student Session for Lesson `RSK-SYNC-001` and select Edit. | The form shows Status `Absent`, Reason `Traffic Issue`, and Notice `No Contact`. | Lesson = RSK-SYNC-001; Student = Student O |
| 2 | Change Attendance Status to `Attend` and select Save. | Salesforce saves the Student Session with Status `Attend`, blank Reason, and blank Notice. | Status: Absent → Attend |
| 3 | In Back Office, open Collect Attendance for the same lesson and student. | Student O displays Attendance Status `Attend`, Attendance Reason blank, and Attendance Notice blank. | BO Lesson = RSK-SYNC-001; Student = Student O |
| 4 | In Learner App, open Lesson `RSK-SYNC-001` for Student O. | Student O's lesson displays Attendance Status `Attend`. | Learner App Student = Student O |

**Severity:** critical
**Priority:** high

---

### [Renseikai] Attendance Synchronization – Salesforce to Back Office – Late to Attend saved – Cleared values reflected

**Description:** AC 04 — Decision Table and Regression — A saved SF correction from Late to Attend appears in BO with both absence fields blank.

**Preconditions:**

- Logged in as HQ or CM Staff to the Renseikai Salesforce org and as HQ Staff to Back Office.
- Published Lesson `RSK-SYNC-002` contains Student `Student P`.
- Student P's Student Session has Attendance Status `Late`, Attendance Reason `School Event`, and Attendance Notice `On The Day` in Salesforce.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | In Salesforce, open Student P's Student Session for Lesson `RSK-SYNC-002` and select Edit. | The form shows Status `Late`, Reason `School Event`, and Notice `On The Day`. | Lesson = RSK-SYNC-002; Student = Student P |
| 2 | Change Attendance Status to `Attend` and select Save. | Salesforce saves the Student Session with Status `Attend`, blank Reason, and blank Notice. | Status: Late → Attend |
| 3 | In Back Office, open Collect Attendance for the same lesson and student. | Student P displays Attendance Status `Attend`, Attendance Reason blank, and Attendance Notice blank. | BO Lesson = RSK-SYNC-002; Student = Student P |
| 4 | In Learner App, open Lesson `RSK-SYNC-002` for Student P. | Student P's lesson displays Attendance Status `Attend`. | Learner App Student = Student P |

**Severity:** critical
**Priority:** high

---

### [Renseikai] Attendance Synchronization – Salesforce to Back Office – Leave Early to Attend saved – Cleared values reflected

**Description:** AC 04 — Decision Table and Regression — A saved SF correction from Leave Early to Attend appears in BO with both absence fields blank.

**Preconditions:**

- Logged in as HQ or CM Staff to the Renseikai Salesforce org and as HQ Staff to Back Office.
- Published Lesson `RSK-SYNC-003` contains Student `Student Q`.
- Student Q's Student Session has Attendance Status `Leave Early`, Attendance Reason `Family Reason`, and Attendance Notice `In Advance` in Salesforce.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | In Salesforce, open Student Q's Student Session for Lesson `RSK-SYNC-003` and select Edit. | The form shows Status `Leave Early`, Reason `Family Reason`, and Notice `In Advance`. | Lesson = RSK-SYNC-003; Student = Student Q |
| 2 | Change Attendance Status to `Attend` and select Save. | Salesforce saves the Student Session with Status `Attend`, blank Reason, and blank Notice. | Status: Leave Early → Attend |
| 3 | In Back Office, open Collect Attendance for the same lesson and student. | Student Q displays Attendance Status `Attend`, Attendance Reason blank, and Attendance Notice blank. | BO Lesson = RSK-SYNC-003; Student = Student Q |
| 4 | In Learner App, open Lesson `RSK-SYNC-003` for Student Q. | Student Q's lesson displays Attendance Status `Attend`. | Learner App Student = Student Q |

**Severity:** critical
**Priority:** high

---

### [Renseikai] Attendance Synchronization – Salesforce to Back Office – Absent status cleared and saved – Blank values reflected

**Description:** AC 04 — Decision Table and Regression — A saved SF-cleared Absent status appears in BO with all three attendance values blank.

**Preconditions:**

- Logged in as HQ or CM Staff to the Renseikai Salesforce org and as HQ Staff to Back Office.
- Published Lesson `RSK-SYNC-004` contains Student `Student R`.
- Student R's Student Session has Attendance Status `Absent`, Attendance Reason `Physical Reasons`, and Attendance Notice `No Contact` in Salesforce.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | In Salesforce, open Student R's Student Session for Lesson `RSK-SYNC-004` and select Edit. | The form shows Status `Absent`, Reason `Physical Reasons`, and Notice `No Contact`. | Lesson = RSK-SYNC-004; Student = Student R |
| 2 | Select the x icon for Attendance Status and select Save. | Salesforce saves the Student Session with blank Status, blank Reason, and blank Notice. | Status: Absent → blank |
| 3 | In Back Office, open Collect Attendance for the same lesson and student. | Student R displays blank Attendance Status, blank Attendance Reason, and blank Attendance Notice. | BO Lesson = RSK-SYNC-004; Student = Student R |
| 4 | In Learner App, open Lesson `RSK-SYNC-004` for Student R. | Student R's lesson displays a blank Attendance Status. | Learner App Student = Student R |

**Severity:** critical
**Priority:** high

---

### [Renseikai] Attendance Synchronization – Salesforce to Back Office – Late status cleared and saved – Blank values reflected

**Description:** AC 04 — Decision Table and Regression — A saved SF-cleared Late status appears in BO with all three attendance values blank.

**Preconditions:**

- Logged in as HQ or CM Staff to the Renseikai Salesforce org and as HQ Staff to Back Office.
- Published Lesson `RSK-SYNC-005` contains Student `Student S`.
- Student S's Student Session has Attendance Status `Late`, Attendance Reason `Traffic Issue`, and Attendance Notice `On The Day` in Salesforce.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | In Salesforce, open Student S's Student Session for Lesson `RSK-SYNC-005` and select Edit. | The form shows Status `Late`, Reason `Traffic Issue`, and Notice `On The Day`. | Lesson = RSK-SYNC-005; Student = Student S |
| 2 | Select the x icon for Attendance Status and select Save. | Salesforce saves the Student Session with blank Status, blank Reason, and blank Notice. | Status: Late → blank |
| 3 | In Back Office, open Collect Attendance for the same lesson and student. | Student S displays blank Attendance Status, blank Attendance Reason, and blank Attendance Notice. | BO Lesson = RSK-SYNC-005; Student = Student S |
| 4 | In Learner App, open Lesson `RSK-SYNC-005` for Student S. | Student S's lesson displays a blank Attendance Status. | Learner App Student = Student S |

**Severity:** critical
**Priority:** high

---

### [Renseikai] Attendance Synchronization – Salesforce to Back Office – Leave Early status cleared and saved – Blank values reflected

**Description:** AC 04 — Decision Table and Regression — A saved SF-cleared Leave Early status appears in BO with all three attendance values blank.

**Preconditions:**

- Logged in as HQ or CM Staff to the Renseikai Salesforce org and as HQ Staff to Back Office.
- Published Lesson `RSK-SYNC-006` contains Student `Student T`.
- Student T's Student Session has Attendance Status `Leave Early`, Attendance Reason `Family Reason`, and Attendance Notice `In Advance` in Salesforce.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | In Salesforce, open Student T's Student Session for Lesson `RSK-SYNC-006` and select Edit. | The form shows Status `Leave Early`, Reason `Family Reason`, and Notice `In Advance`. | Lesson = RSK-SYNC-006; Student = Student T |
| 2 | Select the x icon for Attendance Status and select Save. | Salesforce saves the Student Session with blank Status, blank Reason, and blank Notice. | Status: Leave Early → blank |
| 3 | In Back Office, open Collect Attendance for the same lesson and student. | Student T displays blank Attendance Status, blank Attendance Reason, and blank Attendance Notice. | BO Lesson = RSK-SYNC-006; Student = Student T |
| 4 | In Learner App, open Lesson `RSK-SYNC-006` for Student T. | Student T's lesson displays a blank Attendance Status. | Learner App Student = Student T |

**Severity:** critical
**Priority:** high

---

### [Renseikai] Attendance Synchronization – Salesforce edit cancelled – Back Office values retained

**Description:** AC 04 — Negative Testing — Cancelling an SF correction does not create a partial BO update.

**Preconditions:**

- Logged in as HQ or CM Staff to the Renseikai Salesforce org and as HQ Staff to Back Office.
- Published Lesson `RSK-SYNC-007` contains Student `Student U`.
- Student U's Student Session has Attendance Status `Absent`, Attendance Reason `Traffic Issue`, and Attendance Notice `No Contact` in Salesforce and Back Office.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | In Salesforce, open Student U's Student Session for Lesson `RSK-SYNC-007` and select Edit. | The form shows Status `Absent`, Reason `Traffic Issue`, and Notice `No Contact`. | Lesson = RSK-SYNC-007; Student = Student U |
| 2 | Change Attendance Status to `Attend` and select Cancel. | Salesforce closes the form without saving the correction. | Status: Absent → Attend; Action = Cancel |
| 3 | In Back Office, open Collect Attendance for the same lesson and student. | Student U continues to display Status `Absent`, Reason `Traffic Issue`, and Notice `No Contact`. | BO Lesson = RSK-SYNC-007; Student = Student U |
| 4 | In Learner App, open Lesson `RSK-SYNC-007` for Student U. | Student U's lesson continues to display Attendance Status `Absent`. | Learner App Student = Student U |

**Severity:** major
**Priority:** high
