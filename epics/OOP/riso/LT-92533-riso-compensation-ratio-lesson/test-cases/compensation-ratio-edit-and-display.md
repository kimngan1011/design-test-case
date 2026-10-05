# Test Cases: LT-92533 — Riso Compensation Ratio

## Suite: Compensation Ratio — Edit & Display

### [Riso] Compensation Ratio – Edit Lesson – Only this lesson – Selected occurrence changes

**Description:** AC 01.3 — State Transition / Regression — Only the selected recurring occurrence changes.

**Preconditions:**

- HQ or CM Staff is logged in to the Riso Salesforce organization.
- A Riso recurring series has three planned occurrences with Compensation Ratio `100%`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff opens Edit Lesson for occurrence 2 and selects `60%`. | The edit scope offers Only this lesson. | selected occurrence = 2; selected ratio = 60% |
| 2 | HQ or CM Staff applies Only this lesson and saves. | Occurrence 2 has Compensation Ratio `60%`. | expected occurrence 2 ratio = 60% |
| 3 | HQ or CM Staff opens occurrences 1 and 3. | Occurrences 1 and 3 retain Compensation Ratio `100%`. | expected ratios = 100%, 100% |

**Severity:** major
**Priority:** high

---

### [Riso] Compensation Ratio – Edit Lesson – This and following – Eligible occurrences change

**Description:** AC 01.3 — State Transition / Regression — The selected and following planned occurrences change while prior occurrences remain unchanged.

**Preconditions:**

- HQ or CM Staff is logged in to the Riso Salesforce organization.
- A Riso recurring series has four planned occurrences with Compensation Ratio `100%`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff opens Edit Lesson for occurrence 2 and selects `60%`. | The edit scope offers This and following lessons. | selected occurrence = 2; selected ratio = 60% |
| 2 | HQ or CM Staff applies This and following lessons and saves. | Occurrences 2 through 4 have Compensation Ratio `60%`. | expected occurrences 2–4 ratio = 60% |
| 3 | HQ or CM Staff opens occurrence 1. | Occurrence 1 retains Compensation Ratio `100%`. | expected occurrence 1 ratio = 100% |

**Severity:** major
**Priority:** high

---

### [Riso] Compensation Ratio – Edit Lesson – This and following – Completed occurrence skipped

**Description:** AC 01.3 — State Transition / Negative — Completed occurrences are not changed by a following-scope edit.

**Preconditions:**

- HQ or CM Staff is logged in to the Riso Salesforce organization.
- A Riso recurring series has a planned occurrence 2, a Completed occurrence 3, and a planned occurrence 4.
- All occurrences have Compensation Ratio `100%`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff changes occurrence 2 to `60%` using This and following lessons. | The following-scope edit is saved. | selected occurrence = 2; completed occurrence = 3 |
| 2 | HQ or CM Staff opens occurrences 2 through 4. | Occurrences 2 and 4 have `60%`; Completed occurrence 3 retains `100%`. | expected ratios = 60%, 100%, 60% |

**Severity:** major
**Priority:** high

---

### [Riso] Compensation Ratio – Edit Lesson – This and following – Cancelled occurrence skipped

**Description:** AC 01.3 — State Transition / Negative — Cancelled occurrences are not changed by a following-scope edit.

**Preconditions:**

- HQ or CM Staff is logged in to the Riso Salesforce organization.
- A Riso recurring series has a planned occurrence 2, a Cancelled occurrence 3, and a planned occurrence 4.
- All occurrences have Compensation Ratio `100%`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff changes occurrence 2 to `60%` using This and following lessons. | The following-scope edit is saved. | selected occurrence = 2; cancelled occurrence = 3 |
| 2 | HQ or CM Staff opens occurrences 2 through 4. | Occurrences 2 and 4 have `60%`; Cancelled occurrence 3 retains `100%`. | expected ratios = 60%, 100%, 60% |

**Severity:** major
**Priority:** high

---

### [Riso] Compensation Ratio – Lesson List bulk edit – Eligible selections – Selected lessons change

**Description:** AC 01.3 — Decision Table / CRUD — Bulk edit updates every eligible selected lesson.

**Preconditions:**

- HQ or CM Staff is logged in to the Riso Salesforce organization.
- Two planned Riso lessons have Compensation Ratio `100%`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff selects both planned lessons in Lesson List. | Both selected lessons are available for bulk edit. | selected lessons = 2 planned lessons |
| 2 | HQ or CM Staff bulk edits Compensation Ratio to `60%` and saves. | Both selected lessons have Compensation Ratio `60%`. | selected ratio = 60% |

**Severity:** major
**Priority:** high

---

### [Riso] Compensation Ratio – Lesson List bulk edit – Completed selection – Completed lesson skipped

**Description:** AC 01.3 — Decision Table / Negative — Bulk edit skips a selected Completed lesson.

**Preconditions:**

- HQ or CM Staff is logged in to the Riso Salesforce organization.
- One planned Riso lesson has Compensation Ratio `100%`.
- One Completed Riso lesson has Compensation Ratio `100%`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff selects the planned and Completed lessons in Lesson List. | Both lessons are selected for the bulk-edit attempt. | selected statuses = Planned, Completed |
| 2 | HQ or CM Staff bulk edits Compensation Ratio to `60%` and saves. | The planned lesson has `60%` and the Completed lesson retains `100%`. | expected ratios = 60%, 100% |

**Severity:** major
**Priority:** high

---

### [Riso] Compensation Ratio – Lesson List bulk edit – Cancelled selection – Cancelled lesson skipped

**Description:** AC 01.3 — Decision Table / Negative — Bulk edit skips a selected Cancelled lesson.

**Preconditions:**

- HQ or CM Staff is logged in to the Riso Salesforce organization.
- One planned Riso lesson has Compensation Ratio `100%`.
- One Cancelled Riso lesson has Compensation Ratio `100%`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff selects the planned and Cancelled lessons in Lesson List. | Both lessons are selected for the bulk-edit attempt. | selected statuses = Planned, Cancelled |
| 2 | HQ or CM Staff bulk edits Compensation Ratio to `60%` and saves. | The planned lesson has `60%` and the Cancelled lesson retains `100%`. | expected ratios = 60%, 100% |

**Severity:** major
**Priority:** high

---

### [Riso] Compensation Ratio – Lesson List bulk edit – Recurring selection – Following occurrence unchanged

**Description:** AC 01.3 — State Transition / Regression — Bulk edit does not propagate through a recurring series.

**Preconditions:**

- HQ or CM Staff is logged in to the Riso Salesforce organization.
- A Riso recurring series has three planned occurrences with Compensation Ratio `100%`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff selects occurrence 2 in Lesson List. | Occurrence 2 is selected for bulk edit. | selected occurrence = 2 |
| 2 | HQ or CM Staff bulk edits Compensation Ratio to `60%` and saves. | Occurrence 2 has Compensation Ratio `60%`. | selected ratio = 60% |
| 3 | HQ or CM Staff opens occurrence 3. | The unselected following occurrence retains Compensation Ratio `100%`. | expected occurrence 3 ratio = 100% |

**Severity:** major
**Priority:** high

---

### [Riso] Compensation Ratio – Lesson List – Populated lesson – Label and value displayed

**Description:** AC 01.4 — Component — Lesson List displays the PRD label and a persisted value.

**Preconditions:**

- HQ or CM Staff is logged in to the Riso Salesforce organization.
- A Riso lesson with Compensation Ratio `60%` exists in Lesson List.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff opens Lesson List and locates the Riso lesson. | The list has a column labeled `Compensation Ratio`. | lesson ratio = 60% |
| 2 | HQ or CM Staff reads the Riso lesson row. | The Compensation Ratio cell shows `60%`. | expected ratio = 60% |

**Severity:** minor
**Priority:** medium

---

### [Riso] Compensation Ratio – Edit Lesson form – 発生しない selection – Updated value persists

**Description:** AC 01.1, AC 01.3 — Equivalence Partitioning / CRUD — The Riso-specific allowed value `発生しない` can replace an existing lesson value.

**Preconditions:**

- HQ or CM Staff is logged in to the Riso Salesforce organization.
- An editable Riso lesson with Compensation Ratio `100%` exists.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff opens Edit Lesson and selects `発生しない` in Compensation Ratio. | The field shows `発生しない`. | persisted ratio = 100%; selected ratio = 発生しない |
| 2 | HQ or CM Staff saves the lesson and reopens Edit Lesson. | Compensation Ratio shows `発生しない`. | expected ratio = 発生しない |

**Severity:** major
**Priority:** high

---

### [Riso] Compensation Ratio – Lesson SF Edit Lesson – Values available and update persists

**Description:** AC 01.1, AC 01.3 — Entry-point regression — Editing from Lesson SF exposes the PRD-defined field and persists an allowed change.

**Preconditions:**

- HQ or CM Staff is logged in to the Riso Salesforce organization.
- An editable Riso lesson with Compensation Ratio `100%` exists.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff selects Edit Lesson for the Riso lesson in Salesforce. | The Edit Lesson form displays `Compensation Ratio` with the persisted value `100%`. | persisted ratio = 100% |
| 2 | HQ or CM Staff opens the Compensation Ratio picklist. | The picklist contains `100%`, `60%`, and `発生しない`; `NA` is absent. | allowed values = 100%, 60%, 発生しない |
| 3 | HQ or CM Staff selects `60%` and saves the lesson. | Reopening the lesson shows Compensation Ratio `60%`. | selected ratio = 60% |

**Severity:** major
**Priority:** high

---

### [Riso] Compensation Ratio – Back Office Edit Lesson – Field hidden – Other edits retain value

**Description:** BO clarification — Negative / Regression — Compensation Ratio is not exposed in Back Office, and updating another lesson field preserves the saved ratio.

**Preconditions:**

- HQ or CM Staff is logged in to Riso Back Office.
- An editable Riso lesson with Compensation Ratio `100%` exists.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff opens Edit Lesson for the Riso lesson in Back Office. | The form does not display a `Compensation Ratio` field. | persisted ratio = 100% |
| 2 | HQ or CM Staff changes and saves each editable lesson field other than Compensation Ratio. | Each save succeeds without a Compensation Ratio control being shown. | edited fields = every editable Back Office lesson field except Compensation Ratio |
| 3 | HQ or CM Staff opens the lesson in Salesforce after each save. | Compensation Ratio retains the persisted value `100%` after every edit. | expected ratio = 100% |

**Severity:** major
**Priority:** high

---

### [Riso] Compensation Ratio – Calendar SF Drag and drop Edit Lesson – Values available and update persists

**Description:** AC 01.1, AC 01.3 — Entry-point regression — Editing by Calendar drag and drop retains a PRD-compliant Compensation Ratio field.

**Preconditions:**

- HQ or CM Staff is logged in to the Riso Salesforce organization.
- An editable Riso lesson with Compensation Ratio `100%` exists on Calendar SF.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff drags the Riso lesson to a different Calendar SF time slot and opens the resulting edit form. | The form displays `Compensation Ratio` with persisted value `100%`. | persisted ratio = 100% |
| 2 | HQ or CM Staff opens the Compensation Ratio picklist. | The picklist contains `100%`, `60%`, and `発生しない`; `NA` is absent. | allowed values = 100%, 60%, 発生しない |
| 3 | HQ or CM Staff selects `60%` and saves the lesson. | Reopening the moved lesson shows Compensation Ratio `60%`. | selected ratio = 60% |

**Severity:** major
**Priority:** high

---

### [Riso] Compensation Ratio – Calendar SF Edit Lesson – Values available and update persists

**Description:** AC 01.1, AC 01.3 — Entry-point regression — Editing from Calendar SF exposes the PRD-defined field and persists an allowed change.

**Preconditions:**

- HQ or CM Staff is logged in to the Riso Salesforce organization.
- An editable Riso lesson with Compensation Ratio `100%` exists on Calendar SF.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff selects Edit Lesson from the Calendar SF lesson. | The Edit Lesson form displays `Compensation Ratio` with persisted value `100%`. | persisted ratio = 100% |
| 2 | HQ or CM Staff opens the Compensation Ratio picklist. | The picklist contains `100%`, `60%`, and `発生しない`; `NA` is absent. | allowed values = 100%, 60%, 発生しない |
| 3 | HQ or CM Staff selects `60%` and saves the lesson. | Reopening the lesson shows Compensation Ratio `60%`. | selected ratio = 60% |

**Severity:** major
**Priority:** high

---

### [Riso] Compensation Ratio – Back Office Calendar Edit Lesson – Field hidden – Other edits retain value

**Description:** BO clarification — Negative / Regression — Compensation Ratio is not exposed in Back Office Calendar, and updating another lesson field preserves the saved ratio.

**Preconditions:**

- HQ or CM Staff is logged in to Riso Back Office.
- An editable Riso lesson with Compensation Ratio `100%` exists in Back Office Calendar.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff opens Edit Lesson for the Riso lesson from Back Office Calendar. | The form does not display a `Compensation Ratio` field. | persisted ratio = 100% |
| 2 | HQ or CM Staff changes and saves each editable lesson field other than Compensation Ratio. | Each save succeeds without a Compensation Ratio control being shown. | edited fields = every editable Back Office Calendar lesson field except Compensation Ratio |
| 3 | HQ or CM Staff opens the lesson in Salesforce after each save. | Compensation Ratio retains the persisted value `100%` after every edit. | expected ratio = 100% |

**Severity:** major
**Priority:** high

---

### [Riso] Compensation Ratio – Lesson List – Historical lesson – Blank value displayed

**Description:** AC 01.4 — Component / Negative — A pre-release lesson displays a blank value.

**Preconditions:**

- HQ or CM Staff is logged in to the Riso Salesforce organization.
- A Riso lesson created before the feature release exists in Lesson List.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff opens Lesson List and locates the historical lesson. | The list has a column labeled `Compensation Ratio`. | lesson type = historical |
| 2 | HQ or CM Staff reads the historical lesson row. | The Compensation Ratio cell is blank. | expected ratio = blank |

**Severity:** minor
**Priority:** medium

---

### [Riso] Compensation Ratio – Lesson Detail – Populated lesson – Label and value displayed

**Description:** AC 01.4 — Component — Lesson Detail displays the PRD label and a persisted value.

**Preconditions:**

- HQ or CM Staff is logged in to the Riso Salesforce organization.
- A Riso lesson with Compensation Ratio `60%` exists.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff opens Lesson Detail for the Riso lesson. | Lesson Detail displays a field labeled `Compensation Ratio`. | lesson ratio = 60% |
| 2 | HQ or CM Staff reads the Compensation Ratio field. | The field shows `60%`. | expected ratio = 60% |

**Severity:** minor
**Priority:** medium

---

### [Riso] Compensation Ratio – Lesson Detail – Historical lesson – Blank value displayed

**Description:** AC 01.4 — Component / Negative — Lesson Detail presents a blank field for a pre-release lesson.

**Preconditions:**

- HQ or CM Staff is logged in to the Riso Salesforce organization.
- A Riso lesson created before the feature release exists.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff opens Lesson Detail for the historical lesson. | Lesson Detail displays a field labeled `Compensation Ratio`. | lesson type = historical |
| 2 | HQ or CM Staff reads the Compensation Ratio field. | The field is blank. | expected ratio = blank |

**Severity:** minor
**Priority:** medium

---

### [Riso] Compensation Ratio – Calendar detail drawer – Populated lesson – Label and value displayed

**Description:** AC 01.4 — Component — Calendar detail drawer displays the PRD label and a persisted value.

**Preconditions:**

- HQ or CM Staff is logged in to the Riso Salesforce organization.
- A Riso lesson with Compensation Ratio `60%` exists on Lesson Calendar.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff opens the lesson's detail drawer from Lesson Calendar. | The drawer displays a field labeled `Compensation Ratio`. | lesson ratio = 60% |
| 2 | HQ or CM Staff reads the Compensation Ratio field. | The field shows `60%`. | expected ratio = 60% |

**Severity:** minor
**Priority:** medium

---

### [Riso] Compensation Ratio – Calendar detail drawer – Historical lesson – Blank value displayed

**Description:** AC 01.4 — Component / Negative — Calendar detail drawer presents a blank field for a pre-release lesson.

**Preconditions:**

- HQ or CM Staff is logged in to the Riso Salesforce organization.
- A Riso lesson created before the feature release exists on Lesson Calendar.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff opens the historical lesson's detail drawer from Lesson Calendar. | The drawer displays a field labeled `Compensation Ratio`. | lesson type = historical |
| 2 | HQ or CM Staff reads the Compensation Ratio field. | The field is blank. | expected ratio = blank |

**Severity:** minor
**Priority:** medium
