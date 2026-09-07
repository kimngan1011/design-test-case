# Test Cases: LT-107413 — Clear Attendance Notice and Attendance Reason in Salesforce

## Suite: [Renseikai] Salesforce Attendance Clearing

### [Renseikai] Attendance Synchronization – Back Office to Salesforce – Absent to Attend – Cleared values reflected

**Description:** AC 03 — Decision Table and Regression — A teacher changes an absent attendance record to Attend in Back Office; Salesforce reflects Attend with blank absence fields.

**Preconditions:**

- Logged in as HQ Staff to Back Office and as HQ or CM Staff to the Renseikai Salesforce org.
- Published Lesson `RSK-ATT-001` contains Student `Student A`.
- Student A's Student Session has Attendance Status `Absent`, Attendance Reason `Traffic Issue`, and Attendance Notice `No Contact` in Back Office and Salesforce.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | In Back Office, open Collect Attendance for Lesson `RSK-ATT-001` and select Student A. | Student A shows Status `Absent`, Reason `Traffic Issue`, and Notice `No Contact`. | Lesson = RSK-ATT-001; Student = Student A |
| 2 | Change Student A's Attendance Status to `Attend` and save. | Back Office shows Status `Attend`; Attendance Reason and Attendance Notice are blank. | Status: Absent → Attend |
| 3 | In Salesforce, open Student A's Student Session for Lesson `RSK-ATT-001`. | Staff sees Attendance Status `Attend`, Attendance Reason blank, and Attendance Notice blank. | Salesforce Student = Student A |

**Severity:** major
**Priority:** high

---

### [Renseikai] Attendance Synchronization – Back Office to Salesforce – Late to Attend – Cleared values reflected

**Description:** AC 03 — Decision Table and Regression — A teacher changes a late attendance record to Attend in Back Office; Salesforce reflects Attend with blank absence fields.

**Preconditions:**

- Logged in as HQ Staff to Back Office and as HQ or CM Staff to the Renseikai Salesforce org.
- Published Lesson `RSK-ATT-002` contains Student `Student B`.
- Student B's Student Session has Attendance Status `Late`, Attendance Reason `School Event`, and Attendance Notice `On The Day` in Back Office and Salesforce.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | In Back Office, open Collect Attendance for Lesson `RSK-ATT-002` and select Student B. | Student B shows Status `Late`, Reason `School Event`, and Notice `On The Day`. | Lesson = RSK-ATT-002; Student = Student B |
| 2 | Change Student B's Attendance Status to `Attend` and save. | Back Office shows Status `Attend`; Attendance Reason and Attendance Notice are blank. | Status: Late → Attend |
| 3 | In Salesforce, open Student B's Student Session for Lesson `RSK-ATT-002`. | Staff sees Attendance Status `Attend`, Attendance Reason blank, and Attendance Notice blank. | Salesforce Student = Student B |

**Severity:** major
**Priority:** high

---

### [Renseikai] Attendance Synchronization – Back Office to Salesforce – Leave Early to Attend – Cleared values reflected

**Description:** AC 03 — Decision Table and Regression — A teacher changes a leave-early attendance record to Attend in Back Office; Salesforce reflects Attend with blank absence fields.

**Preconditions:**

- Logged in as HQ Staff to Back Office and as HQ or CM Staff to the Renseikai Salesforce org.
- Published Lesson `RSK-ATT-003` contains Student `Student C`.
- Student C's Student Session has Attendance Status `Leave Early`, Attendance Reason `Family Reason`, and Attendance Notice `In Advance` in Back Office and Salesforce.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | In Back Office, open Collect Attendance for Lesson `RSK-ATT-003` and select Student C. | Student C shows Status `Leave Early`, Reason `Family Reason`, and Notice `In Advance`. | Lesson = RSK-ATT-003; Student = Student C |
| 2 | Change Student C's Attendance Status to `Attend` and save. | Back Office shows Status `Attend`; Attendance Reason and Attendance Notice are blank. | Status: Leave Early → Attend |
| 3 | In Salesforce, open Student C's Student Session for Lesson `RSK-ATT-003`. | Staff sees Attendance Status `Attend`, Attendance Reason blank, and Attendance Notice blank. | Salesforce Student = Student C |

**Severity:** major
**Priority:** high

---

### [Renseikai] Attendance Correction – Salesforce Student Session – Absent status cleared – Dependent fields cleared

**Description:** AC 01 — Decision Table — Clearing an absent status clears both dependent absence fields in the Salesforce form.

**Preconditions:**

- Logged in as HQ or CM Staff to the Renseikai Salesforce org.
- Published Lesson `RSK-ATT-004` contains Student `Student D`.
- Student D's Student Session has Attendance Status `Absent`, Attendance Reason `Physical Reasons`, and Attendance Notice `No Contact`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Open Lesson `RSK-ATT-004`, open Student D's Student Session, and select Edit. | The Edit Student Session form shows Status `Absent`, Reason `Physical Reasons`, and Notice `No Contact`. | Lesson = RSK-ATT-004; Student = Student D |
| 2 | Select the x icon for Attendance Status. | Attendance Status, Attendance Reason, and Attendance Notice each show a blank selection. | Status: Absent → blank |

**Severity:** major
**Priority:** high

---

### [Renseikai] Attendance Correction – Salesforce Student Session – Late status cleared – Dependent fields cleared

**Description:** AC 01 — Decision Table — Clearing a late status clears both dependent absence fields in the Salesforce form.

**Preconditions:**

- Logged in as HQ or CM Staff to the Renseikai Salesforce org.
- Published Lesson `RSK-ATT-005` contains Student `Student E`.
- Student E's Student Session has Attendance Status `Late`, Attendance Reason `Traffic Issue`, and Attendance Notice `On The Day`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Open Lesson `RSK-ATT-005`, open Student E's Student Session, and select Edit. | The Edit Student Session form shows Status `Late`, Reason `Traffic Issue`, and Notice `On The Day`. | Lesson = RSK-ATT-005; Student = Student E |
| 2 | Select the x icon for Attendance Status. | Attendance Status, Attendance Reason, and Attendance Notice each show a blank selection. | Status: Late → blank |

**Severity:** major
**Priority:** high

---

### [Renseikai] Attendance Correction – Salesforce Student Session – Leave Early status cleared – Dependent fields cleared

**Description:** AC 01 — Decision Table — Clearing a leave-early status clears both dependent absence fields in the Salesforce form.

**Preconditions:**

- Logged in as HQ or CM Staff to the Renseikai Salesforce org.
- Published Lesson `RSK-ATT-006` contains Student `Student F`.
- Student F's Student Session has Attendance Status `Leave Early`, Attendance Reason `Family Reason`, and Attendance Notice `In Advance`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Open Lesson `RSK-ATT-006`, open Student F's Student Session, and select Edit. | The Edit Student Session form shows Status `Leave Early`, Reason `Family Reason`, and Notice `In Advance`. | Lesson = RSK-ATT-006; Student = Student F |
| 2 | Select the x icon for Attendance Status. | Attendance Status, Attendance Reason, and Attendance Notice each show a blank selection. | Status: Leave Early → blank |

**Severity:** major
**Priority:** high

---

### [Renseikai] Attendance Correction – Salesforce Student Session – Absent to Late – Existing absence fields retained

**Description:** AC 01 — Negative Testing — A status change that does not become Attend or blank does not invoke the new clear behavior.

**Preconditions:**

- Logged in as HQ or CM Staff to the Renseikai Salesforce org.
- Published Lesson `RSK-ATT-007` contains Student `Student G`.
- Student G's Student Session has Attendance Status `Absent`, Attendance Reason `Traffic Issue`, and Attendance Notice `No Contact`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Open Lesson `RSK-ATT-007`, open Student G's Student Session, and select Edit. | The Edit Student Session form shows Status `Absent`, Reason `Traffic Issue`, and Notice `No Contact`. | Lesson = RSK-ATT-007; Student = Student G |
| 2 | Change Attendance Status to `Late`. | Attendance Status shows `Late`; Attendance Reason remains `Traffic Issue` and Attendance Notice remains `No Contact`. | Status: Absent → Late |

**Severity:** major
**Priority:** high

---

### [Renseikai] Attendance Correction – Salesforce Student Session – Selected attendance controls – Each x icon clears its field

**Description:** AC 02 — Component — All three selected attendance controls provide and apply their clear affordance.

**Preconditions:**

- Logged in as HQ or CM Staff to the Renseikai Salesforce org.
- Published Lesson `RSK-ATT-008` contains Student `Student H`.
- Student H's Student Session has Attendance Status `Absent`, Attendance Reason `Traffic Issue`, and Attendance Notice `No Contact`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Open Lesson `RSK-ATT-008`, open Student H's Student Session, and select Edit. | Status `Absent`, Reason `Traffic Issue`, and Notice `No Contact` are displayed; each selected control shows an x icon. | Lesson = RSK-ATT-008; Student = Student H |
| 2 | Select the x icon for Attendance Reason. | Attendance Reason is blank; Attendance Status remains `Absent` and Attendance Notice remains `No Contact`. | Clear field = Attendance Reason |
| 3 | Select `Traffic Issue` for Attendance Reason, then select the x icon for Attendance Notice. | Attendance Notice is blank; Attendance Status remains `Absent` and Attendance Reason remains `Traffic Issue`. | Reason = Traffic Issue; Clear field = Attendance Notice |
| 4 | Select `No Contact` for Attendance Notice, then select the x icon for Attendance Status. | Attendance Status, Attendance Reason, and Attendance Notice each show a blank selection. | Notice = No Contact; Clear field = Attendance Status |

**Severity:** minor
**Priority:** medium
