# Test Cases: LT-92533 — Riso Compensation Ratio

## Suite: Compensation Ratio — Create & Configuration

### [Riso] Compensation Ratio – New Lesson form – Riso tenant – PRD field and values available

**Description:** AC 01.1 — Component / Equivalence Partitioning — Riso staff can use the confirmed label and three picklist values.

**Preconditions:**

- HQ or CM Staff is logged in to the Riso Salesforce organization.
- A valid New Lesson form is available.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff opens the New Lesson form. | The form displays a field labeled `Compensation Ratio`. | tenant = Riso |
| 2 | HQ or CM Staff opens the Compensation Ratio picklist. | The picklist contains `100%`, `60%`, and `発生しない` and does not contain `NA`. | allowed values = 100%, 60%, 発生しない |

**Severity:** major
**Priority:** high

---

### [Riso] Compensation Ratio – New Lesson form – 発生しない selection – Selected value persists

**Description:** AC 01.1, AC 01.2 — Equivalence Partitioning / CRUD — The Riso-specific allowed value `発生しない` can be selected during lesson creation and is persisted.

**Preconditions:**

- HQ or CM Staff is logged in to the Riso Salesforce organization.
- A valid New Lesson form is available.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff selects `発生しない` in Compensation Ratio. | The field shows `発生しない`. | selected ratio = 発生しない |
| 2 | HQ or CM Staff completes required lesson data and saves. | The new lesson is saved with Compensation Ratio `発生しない`. | expected ratio = 発生しない |

**Severity:** major
**Priority:** high

---

### [Riso] Compensation Ratio – Lesson List SF New Lesson – Default and values available

**Description:** AC 01.1, AC 01.2 — Entry-point regression — The Lesson List SF New Lesson route opens a PRD-compliant Compensation Ratio field.

**Preconditions:**

- HQ or CM Staff is logged in to the Riso Salesforce organization.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff selects New from Lesson List in Salesforce. | The New Lesson form displays `Compensation Ratio` with default value `100%`. | tenant = Riso |
| 2 | HQ or CM Staff opens the Compensation Ratio picklist. | The picklist contains `100%`, `60%`, and `発生しない`; `NA` is absent. | allowed values = 100%, 60%, 発生しない |
| 3 | HQ or CM Staff selects `60%`, completes required lesson data, and saves. | The new lesson is saved with Compensation Ratio `60%`. | selected ratio = 60% |

**Severity:** major
**Priority:** high

---

### [Riso] Compensation Ratio – Lesson Schedule Detail Add Lesson – Default and values available

**Description:** AC 01.1, AC 01.2 — Entry-point regression — Adding a lesson from Lesson Schedule Detail opens a PRD-compliant Compensation Ratio field.

**Preconditions:**

- HQ or CM Staff is logged in to the Riso Salesforce organization.
- A Riso Lesson Schedule Detail record can accept an added lesson.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff selects Add Lesson from Lesson Schedule Detail. | The upsert form displays `Compensation Ratio` with default value `100%`. | tenant = Riso |
| 2 | HQ or CM Staff opens the Compensation Ratio picklist. | The picklist contains `100%`, `60%`, and `発生しない`; `NA` is absent. | allowed values = 100%, 60%, 発生しない |
| 3 | HQ or CM Staff selects `60%`, completes required lesson data, and saves. | The added lesson is saved with Compensation Ratio `60%`. | selected ratio = 60% |

**Severity:** major
**Priority:** high

---

### [Riso] Compensation Ratio – Lesson Schedule Detail Extend Recurrence – Values available

**Description:** AC 01.1 — Entry-point regression — Extend Recurrence exposes the PRD-defined Compensation Ratio control without asserting an unspecified inherited default.

**Preconditions:**

- HQ or CM Staff is logged in to the Riso Salesforce organization.
- A Riso Lesson Schedule Detail record can be extended as a recurring schedule.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff selects Extend Recurrence from Lesson Schedule Detail. | The extension upsert form displays a field labeled `Compensation Ratio`. | tenant = Riso |
| 2 | HQ or CM Staff opens the Compensation Ratio picklist. | The picklist contains `100%`, `60%`, and `発生しない`; `NA` is absent. | allowed values = 100%, 60%, 発生しない |
| 3 | HQ or CM Staff selects `60%`, completes the extension data, and saves. | The newly created extended lesson has Compensation Ratio `60%`. | selected ratio = 60% |

**Severity:** major
**Priority:** high

---

### [Riso] Compensation Ratio – Lesson SF Duplicate Lesson – Values available

**Description:** AC 01.1 — Entry-point regression — Duplicating a lesson exposes the PRD-defined Compensation Ratio control; no copied/default value is asserted because the PRD does not specify duplicate initialization.

**Preconditions:**

- HQ or CM Staff is logged in to the Riso Salesforce organization.
- A Riso lesson with Compensation Ratio `100%` exists.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff selects Duplicate Lesson for the source lesson in Salesforce. | The duplicate upsert form displays a field labeled `Compensation Ratio`. | source ratio = 100% |
| 2 | HQ or CM Staff opens the Compensation Ratio picklist. | The picklist contains `100%`, `60%`, and `発生しない`; `NA` is absent. | allowed values = 100%, 60%, 発生しない |
| 3 | HQ or CM Staff selects `60%`, completes required lesson data, and saves. | The duplicated lesson is saved with Compensation Ratio `60%`. | selected ratio = 60% |

**Severity:** major
**Priority:** high

---

### [Riso] Compensation Ratio – Calendar SF New Lesson – Default and values available

**Description:** AC 01.1, AC 01.2 — Entry-point regression — Creating a lesson from Calendar SF opens a PRD-compliant Compensation Ratio field.

**Preconditions:**

- HQ or CM Staff is logged in to the Riso Salesforce organization.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff selects New Lesson from Calendar in Salesforce. | The New Lesson form displays `Compensation Ratio` with default value `100%`. | tenant = Riso |
| 2 | HQ or CM Staff opens the Compensation Ratio picklist. | The picklist contains `100%`, `60%`, and `発生しない`; `NA` is absent. | allowed values = 100%, 60%, 発生しない |
| 3 | HQ or CM Staff selects `60%`, completes required lesson data, and saves. | The calendar-created lesson is saved with Compensation Ratio `60%`. | selected ratio = 60% |

**Severity:** major
**Priority:** high

---

### [Riso] Compensation Ratio – Calendar SF Drag and drop New Lesson – Default and values available

**Description:** AC 01.1, AC 01.2 — Entry-point regression — Creating a lesson by Calendar drag and drop opens a PRD-compliant Compensation Ratio field.

**Preconditions:**

- HQ or CM Staff is logged in to the Riso Salesforce organization.
- An empty Calendar SF time slot is available.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff drags an empty Calendar SF time slot to create a lesson. | The New Lesson form uses the dragged datetime and displays `Compensation Ratio` with default value `100%`. | target datetime = 2026-09-15 10:00 JST |
| 2 | HQ or CM Staff opens the Compensation Ratio picklist. | The picklist contains `100%`, `60%`, and `発生しない`; `NA` is absent. | allowed values = 100%, 60%, 発生しない |
| 3 | HQ or CM Staff selects `60%`, completes required lesson data, and saves. | The drag-and-drop-created lesson is saved with Compensation Ratio `60%`. | selected ratio = 60% |

**Severity:** major
**Priority:** high

---

### [Riso] Compensation Ratio – Available Teacher Calendar New Lesson – Default and values available

**Description:** AC 01.1, AC 01.2 — Entry-point regression — Creating a lesson from Available Teacher Calendar opens a PRD-compliant Compensation Ratio field.

**Preconditions:**

- HQ or CM Staff is logged in to the Riso Salesforce organization.
- An available teacher time slot is visible in Available Teacher Calendar.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff creates a lesson from Available Teacher Calendar. | The New Lesson form displays `Compensation Ratio` with default value `100%`. | tenant = Riso |
| 2 | HQ or CM Staff opens the Compensation Ratio picklist. | The picklist contains `100%`, `60%`, and `発生しない`; `NA` is absent. | allowed values = 100%, 60%, 発生しない |
| 3 | HQ or CM Staff selects `60%`, completes required lesson data, and saves. | The lesson is saved with Compensation Ratio `60%`. | selected ratio = 60% |

**Severity:** major
**Priority:** high

---

### [Riso] Compensation Ratio – Calendar SF Duplicate Lesson – Values available

**Description:** AC 01.1 — Entry-point regression — Duplicating from Calendar SF exposes the PRD-defined Compensation Ratio control; no copied/default value is asserted because the PRD does not specify duplicate initialization.

**Preconditions:**

- HQ or CM Staff is logged in to the Riso Salesforce organization.
- A Riso lesson with Compensation Ratio `100%` exists on Calendar SF.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff selects Duplicate Lesson from the Calendar SF lesson. | The duplicate upsert form displays a field labeled `Compensation Ratio`. | source ratio = 100% |
| 2 | HQ or CM Staff opens the Compensation Ratio picklist. | The picklist contains `100%`, `60%`, and `発生しない`; `NA` is absent. | allowed values = 100%, 60%, 発生しない |
| 3 | HQ or CM Staff selects `60%`, completes required lesson data, and saves. | The duplicated calendar lesson is saved with Compensation Ratio `60%`. | selected ratio = 60% |

**Severity:** major
**Priority:** high

---

### [Riso] Compensation Ratio – Edit Lesson form – Riso tenant – PRD field and values available

**Description:** AC 01.1 — Component / Equivalence Partitioning — The edit surface matches the PRD label and allowed values.

**Preconditions:**

- HQ or CM Staff is logged in to the Riso Salesforce organization.
- A Riso lesson with Compensation Ratio `100%` exists.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff opens Edit Lesson for the Riso lesson. | The edit form displays a field labeled `Compensation Ratio`. | lesson ratio = 100% |
| 2 | HQ or CM Staff opens the Compensation Ratio picklist. | The picklist contains `100%`, `60%`, and `発生しない` and does not contain `NA`. | allowed values = 100%, 60%, 発生しない |

**Severity:** major
**Priority:** high

---

### [Riso] Compensation Ratio – Tenant isolation – Non-Riso organization – Field unavailable

**Description:** AC 01.1 — Permission Matrix / Negative — The Riso-only field is unavailable outside the Riso organization.

**Preconditions:**

- HQ or CM Staff is logged in to a non-Riso Salesforce organization.
- A valid New Lesson form is available.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff opens the New Lesson form. | No field labeled `Compensation Ratio` is available on the form. | tenant = non-Riso |
| 2 | HQ or CM Staff saves a lesson with all required standard lesson data. | The saved non-Riso lesson has no Compensation Ratio field value. | tenant = non-Riso |

**Severity:** major
**Priority:** high

---

### [Riso] Compensation Ratio – New Lesson form – Unchanged default – 100% persists

**Description:** AC 01.2 — Equivalence Partitioning / CRUD — The PRD default is persisted when the user does not alter it.

**Preconditions:**

- HQ or CM Staff is logged in to the Riso Salesforce organization.
- A valid New Lesson form is available.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff opens the New Lesson form. | Compensation Ratio shows `100%` before any change. | default ratio = 100% |
| 2 | HQ or CM Staff completes required lesson data and saves without changing Compensation Ratio. | The lesson is saved with Compensation Ratio `100%`. | selected ratio = 100% |
| 3 | HQ or CM Staff opens Lesson Detail for the saved lesson. | Lesson Detail displays `Compensation Ratio` with value `100%`. | expected displayed ratio = 100% |

**Severity:** major
**Priority:** high

---

### [Riso] Compensation Ratio – New Lesson form – 60% selection – Selected value persists

**Description:** AC 01.2 — Equivalence Partitioning / CRUD — A valid non-default value can be saved.

**Preconditions:**

- HQ or CM Staff is logged in to the Riso Salesforce organization.
- A valid New Lesson form is available.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff selects `60%` in Compensation Ratio. | The field shows `60%`. | selected ratio = 60% |
| 2 | HQ or CM Staff completes required lesson data and saves. | The lesson is saved with Compensation Ratio `60%`. | selected ratio = 60% |

**Severity:** major
**Priority:** high

---

### [Riso] Compensation Ratio – New Lesson form – Cleared optional value – Blank persists

**Description:** AC 01.2 — Equivalence Partitioning / CRUD — The optional field can be cleared and saved blank.

**Preconditions:**

- HQ or CM Staff is logged in to the Riso Salesforce organization.
- A valid New Lesson form is available.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff clears the Compensation Ratio default value. | Compensation Ratio is blank and the form remains savable. | selected ratio = blank |
| 2 | HQ or CM Staff completes required lesson data and saves. | The lesson is saved with a blank Compensation Ratio. | selected ratio = blank |

**Severity:** major
**Priority:** high

---

### [Riso] Compensation Ratio – Recurring creation – Default first occurrence – 100% inherited

**Description:** AC 01.2 — State Transition / Regression — A recurring series inherits the first lesson's default value.

**Preconditions:**

- HQ or CM Staff is logged in to the Riso Salesforce organization.
- A New Lesson form can create three weekly recurring occurrences.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff creates a three-occurrence recurring lesson without changing Compensation Ratio. | The recurring series is saved. | occurrences = 3; first ratio = 100% |
| 2 | HQ or CM Staff opens each created occurrence. | Each occurrence has Compensation Ratio `100%`. | expected ratios = 100%, 100%, 100% |

**Severity:** major
**Priority:** high

---

### [Riso] Compensation Ratio – Recurring creation – 60% first occurrence – 60% inherited

**Description:** AC 01.2 — State Transition / Regression — A recurring series inherits a selected non-default value.

**Preconditions:**

- HQ or CM Staff is logged in to the Riso Salesforce organization.
- A New Lesson form can create three weekly recurring occurrences.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff selects `60%` and creates a three-occurrence recurring lesson. | The recurring series is saved. | occurrences = 3; first ratio = 60% |
| 2 | HQ or CM Staff opens each created occurrence. | Each occurrence has Compensation Ratio `60%`. | expected ratios = 60%, 60%, 60% |

**Severity:** major
**Priority:** high

---

### [Riso] Compensation Ratio – Recurring creation – Blank first occurrence – Blank inherited

**Description:** AC 01.2 — State Transition / Regression — A recurring series preserves the optional blank value from the first lesson.

**Preconditions:**

- HQ or CM Staff is logged in to the Riso Salesforce organization.
- A New Lesson form can create three weekly recurring occurrences.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff clears Compensation Ratio and creates a three-occurrence recurring lesson. | The recurring series is saved. | occurrences = 3; first ratio = blank |
| 2 | HQ or CM Staff opens each created occurrence. | Each occurrence has a blank Compensation Ratio. | expected ratios = blank, blank, blank |

**Severity:** major
**Priority:** high
