# Test Cases: LT-108387 + LT-101751 — Custom Column Configuration

## Suite: Custom Column Configuration

### Student Session Columns – Column Picker – Enabled tenant – Ten supported fields listed

**Description:** Core configuration — Component and Scroll scenario — A System Administrator can access the enabled tenant picker and see the complete field catalog.

**Preconditions:**

- System Administrator is logged in to the Renseikai Salesforce tenant.
- The Renseikai **Enable Customizable Table Columns** setting is `ON`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | System Administrator opens Lesson Custom Settings. | Lesson Custom Settings opens. | tenant = Renseikai; Enable Customizable Table Columns = ON |
| 2 | System Administrator opens the Student Session column configuration. | The configuration opens with the exact label `Visible Columns`. | picker label = Visible Columns |
| 3 | System Administrator reads the visible field choices and scrolls to the end of the list. | Grade, Risk, Type, Attendance Response, Attendance Status, Attendance Notice, Attendance Reason, Reallocate Flag, Student Name, and Attendance Note are reachable exactly once. | expected catalog = 10 unique fields |

**Severity:** major
**Priority:** high

---

### [Renseikai] Student Session Columns – Japanese locale – Japanese field selection – Saved headers rendered

**Description:** LT-108387 + User request — Component and Readback — A System Administrator customizes the Renseikai Student Session table in Japanese locale and the saved table renders the selected Japanese headers.

**Preconditions:**

- System Administrator is logged in to the Renseikai Salesforce tenant in Japanese locale.
- The Renseikai **Enable Customizable Table Columns** setting is `ON`.
- A published lesson contains Student A with Grade `7`, Attendance Response `Absent (Family event)`, Attendance Status `Absent`, Attendance Reason `Family event`, and Attendance Note `Parent called at 08:15`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | System Administrator opens the Student Session column configuration. | The Renseikai column configuration opens in Japanese locale. | tenant = Renseikai; locale = Japanese; setting = ON |
| 2 | System Administrator selects 生徒名, 学年, 出欠連絡, 出欠状況, 欠席理由, and 備考 and saves the configuration. | The saved selection contains exactly 生徒名, 学年, 出欠連絡, 出欠状況, 欠席理由, and 備考. | selected Japanese fields = 生徒名, 学年, 出欠連絡, 出欠状況, 欠席理由, 備考 |
| 3 | System Administrator opens and refreshes the published lesson in Salesforce Lesson Detail. | The Student Session table headers are exactly 生徒名, 学年, 出欠連絡, 出欠状況, 欠席理由, and 備考. | expected Japanese headers = 生徒名, 学年, 出欠連絡, 出欠状況, 欠席理由, 備考 |
| 4 | System Administrator reads the Student A row. | The Student A row shows `7`, `Absent (Family event)`, `Absent`, `Family event`, and `Parent called at 08:15` under the matching Japanese headers. | Student A values = configured precondition values |

**Severity:** major
**Priority:** high

---

### Student Session Columns – Tenant Setting – Disabled tenant – Configuration unavailable

**Description:** Core configuration — Decision Table and Negative — A tenant with the setting disabled cannot customize Student Session columns.

**Preconditions:**

- System Administrator is logged in to the EEA Salesforce tenant.
- The EEA **Enable Customizable Table Columns** setting is `OFF`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | System Administrator opens Lesson Custom Settings. | Lesson Custom Settings opens for EEA. | tenant = EEA; Enable Customizable Table Columns = OFF |
| 2 | System Administrator searches for Student Session column configuration. | No active control allows the System Administrator to select or reorder Student Session columns. | expected configuration access = unavailable |
| 3 | System Administrator opens a published EEA lesson in Salesforce Lesson Detail. | The EEA table remains usable with its existing saved layout and no configuration action is shown to the System Administrator. | expected table state = existing saved EEA layout |

**Severity:** major
**Priority:** high

---

### Student Session Columns – Configuration Access – Non-System Administrator – Changes blocked

**Description:** Core configuration — Permission Matrix and Negative — A non-System Administrator cannot change a tenant layout.

**Preconditions:**

- HQ or CM Staff is logged in to the Renseikai Salesforce tenant without the System Administrator role.
- The Renseikai **Enable Customizable Table Columns** setting is `ON`.
- The saved Renseikai layout is Student Name, Grade, Attendance Status.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff opens Lesson Custom Settings. | The staff user cannot access the Student Session column configuration as an editable control. | tenant = Renseikai; role = non-System Administrator; setting = ON |
| 2 | HQ or CM Staff opens the published lesson in Salesforce Lesson Detail. | The table shows the saved Renseikai layout without any column-edit control. | saved headers = Student Name, Grade, Attendance Status |
| 3 | HQ or CM Staff refreshes Salesforce Lesson Detail. | The saved Renseikai layout remains unchanged. | expected configuration write = none |

**Severity:** major
**Priority:** high

---

### Student Session Columns – Field Selection – Saved subset – Headers persist after refresh

**Description:** Core configuration — State Transition and Readback — A System Administrator saves a selected subset and the target tenant table retains exactly that subset.

**Preconditions:**

- System Administrator is logged in to the Renseikai Salesforce tenant.
- The Renseikai **Enable Customizable Table Columns** setting is `ON`.
- A published lesson contains Student A with Grade `7` and Attendance Status `Absent`.
- A different HQ or CM Staff user can access the Renseikai Salesforce tenant without the System Administrator role.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | System Administrator opens the Student Session column configuration. | The column configuration opens for Renseikai. | tenant = Renseikai; setting = ON; selected fields = none before selection |
| 2 | System Administrator selects Student Name, Grade, and Attendance Status and saves the configuration. | The saved selection contains exactly Student Name, Grade, and Attendance Status. | selected fields = Student Name, Grade, Attendance Status |
| 3 | System Administrator opens the published lesson in Salesforce Lesson Detail. | The Student Session table shows exactly Student Name, Grade, and Attendance Status. | expected headers = Student Name, Grade, Attendance Status |
| 4 | System Administrator refreshes Salesforce Lesson Detail. | The same three headers remain and Student A still shows `7` and `Absent`. | expected persisted headers = Student Name, Grade, Attendance Status |
| 5 | A different HQ or CM Staff user opens and refreshes the same published lesson in Salesforce Lesson Detail. | The Student Session table shows exactly Student Name, Grade, and Attendance Status. | role = non-System Administrator; expected headers = Student Name, Grade, Attendance Status |

**Severity:** major
**Priority:** high

---

### Student Session Columns – Field Order – Non-default sequence – Header order persists

**Description:** Core configuration — Scenario — A saved non-default order is rendered in the same relative order after refresh.

**Preconditions:**

- System Administrator is logged in to the Renseikai Salesforce tenant.
- The Renseikai **Enable Customizable Table Columns** setting is `ON`.
- Student Name, Grade, and Attendance Status are selected for the Renseikai tenant.
- A different HQ or CM Staff user can access the Renseikai Salesforce tenant without the System Administrator role.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | System Administrator opens the Student Session column configuration. | The three selected fields are available for reordering. | tenant = Renseikai; setting = ON; selected fields = Student Name, Grade, Attendance Status |
| 2 | System Administrator saves the order Attendance Status, Student Name, Grade. | The saved order is Attendance Status first, Student Name second, and Grade third. | saved order = Attendance Status → Student Name → Grade |
| 3 | System Administrator opens and refreshes the published lesson in Salesforce Lesson Detail. | The first three Student Session table headers are Attendance Status, Student Name, and Grade in that exact order. | expected header order = Attendance Status → Student Name → Grade |
| 4 | A different HQ or CM Staff user opens and refreshes the same published lesson in Salesforce Lesson Detail. | The first three Student Session table headers are Attendance Status, Student Name, and Grade in that exact order. | role = non-System Administrator; expected header order = Attendance Status → Student Name → Grade |

**Severity:** major
**Priority:** high

---

### Student Session Columns – Field Exclusion – Selected field removed – Header absent after save

**Description:** Core configuration — State Transition and Negative — Removing a selected field removes only that field from the saved tenant layout.

**Preconditions:**

- System Administrator is logged in to the Renseikai Salesforce tenant.
- The Renseikai **Enable Customizable Table Columns** setting is `ON`.
- The saved Renseikai layout contains Student Name, Grade, Attendance Status, and Attendance Notice.
- A different HQ or CM Staff user can access the Renseikai Salesforce tenant without the System Administrator role.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | System Administrator opens the Student Session column configuration. | Attendance Notice appears as a currently selected field. | tenant = Renseikai; setting = ON; selected fields include Attendance Notice |
| 2 | System Administrator removes Attendance Notice from the selected fields and saves the configuration. | The saved selection no longer includes Attendance Notice. | removed field = Attendance Notice |
| 3 | System Administrator opens and refreshes the published lesson in Salesforce Lesson Detail. | Attendance Notice is absent while Student Name, Grade, and Attendance Status remain visible. | expected headers = Student Name, Grade, Attendance Status; excluded header = Attendance Notice |
| 4 | A different HQ or CM Staff user opens and refreshes the same published lesson in Salesforce Lesson Detail. | Attendance Notice is absent while Student Name, Grade, and Attendance Status remain visible. | role = non-System Administrator; expected headers = Student Name, Grade, Attendance Status; excluded header = Attendance Notice |

**Severity:** major
**Priority:** high

---

### Student Session Columns – Tenant Isolation – Renseikai saved layout – EEA layout unchanged

**Description:** Core configuration — Decision Table and Regression — Saving a Renseikai layout does not overwrite the EEA layout.

**Preconditions:**

- System Administrator can access the Renseikai and EEA Salesforce tenants.
- The Renseikai and EEA **Enable Customizable Table Columns** settings are `ON`.
- The saved EEA layout is Student Name, Grade, Type, Attendance Status, Attendance Reason, and Reallocate Flag.
- A different HQ or CM Staff user can access the Renseikai Salesforce tenant without the System Administrator role.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | System Administrator saves the Renseikai layout as Student Name, Grade, Attendance Status. | The Renseikai saved layout contains exactly three fields. | tenant A = Renseikai; saved headers = Student Name, Grade, Attendance Status |
| 2 | A different HQ or CM Staff user opens and refreshes a published Renseikai lesson in Salesforce Lesson Detail. | The Renseikai table shows Student Name, Grade, and Attendance Status. | role = non-System Administrator; expected Renseikai headers = Student Name, Grade, Attendance Status |
| 3 | System Administrator switches to EEA and opens a published EEA lesson in Salesforce Lesson Detail. | The EEA table still shows Student Name, Grade, Type, Attendance Status, Attendance Reason, and Reallocate Flag. | tenant B = EEA; expected EEA headers = Student Name, Grade, Type, Attendance Status, Attendance Reason, Reallocate Flag |

**Severity:** major
**Priority:** high

---

### Student Session Columns – Configuration Save – Existing session values – No attendance data changed

**Description:** Core configuration — Data Integrity and Regression — Saving a column layout never changes Student Session attendance data.

**Preconditions:**

- System Administrator is logged in to the Renseikai Salesforce tenant.
- The Renseikai **Enable Customizable Table Columns** setting is `ON`.
- A published lesson contains Student A with Attendance Response `Absent (Family event)`, Attendance Status `Absent`, Attendance Reason `Family event`, and Attendance Note `Parent called at 08:15`.
- A different HQ or CM Staff user can access the Renseikai Salesforce tenant without the System Administrator role.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | System Administrator records Student A's four attendance values from the separate Edit function. | The recorded values are `Absent (Family event)`, `Absent`, `Family event`, and `Parent called at 08:15`. | tenant = Renseikai; setting = ON; Student A attendance values = precondition values |
| 2 | System Administrator saves a new table layout containing Student Name, Attendance Response, Attendance Status, Attendance Reason, and Attendance Note. | The table layout is saved for Renseikai. | selected fields = Student Name, Attendance Response, Attendance Status, Attendance Reason, Attendance Note |
| 3 | System Administrator refreshes Salesforce Lesson Detail and opens the separate Edit function for Student A. | The four attendance values remain exactly `Absent (Family event)`, `Absent`, `Family event`, and `Parent called at 08:15`. | expected Student A attendance values = precondition values |
| 4 | A different HQ or CM Staff user opens and refreshes the same published lesson in Salesforce Lesson Detail. | The Student Session table shows exactly Student Name, Attendance Response, Attendance Status, Attendance Reason, and Attendance Note. | role = non-System Administrator; expected headers = Student Name, Attendance Response, Attendance Status, Attendance Reason, Attendance Note |

**Severity:** major
**Priority:** high
