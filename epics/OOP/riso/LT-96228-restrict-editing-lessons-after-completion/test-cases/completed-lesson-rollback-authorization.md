# Test Cases: LT-96228 — Restrict Editing Lessons After Completion

## Suite: [Riso] Completed Lesson Rollback Authorization

### [Riso] Completed Lesson Rollback – Lesson Details – Permission Granted – Status Changes to Published

**Description:** AC01.1, AC02.1 — Permission Matrix / State Transition — A staff member with the epic custom permission can correct a completed lesson from Complete to Published in Salesforce Lesson Details.

**Preconditions:**

- A Riso lesson exists with Status = `Complete`.
- A staff member is logged in to Salesforce.
- The staff member has the custom permission defined for LT-96228.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | The staff member opens the completed lesson in Salesforce Lesson Details. | The Lesson Status shows `Complete`. | `lesson_status = Complete` |
| 2 | The staff member changes Lesson Status to `Published` and saves the lesson. | The lesson saves with Lesson Status = `Published`. | `target_status = Published` |

**Severity:** critical  
**Priority:** high

---

### [Riso] Completed Lesson Rollback – Lesson Details – Permission Granted – Lesson Details Become Editable

**Description:** AC02.1 — State Transition / Regression — An authorized correction restores Lesson Details editability.

**Preconditions:**

- A Riso lesson exists with Status = `Complete`.
- A staff member is logged in to Salesforce.
- The staff member has the custom permission defined for LT-96228.
- The lesson Name is `Algebra Correction Lesson`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | The staff member opens the completed lesson in Salesforce Lesson Details. | The Lesson Status shows `Complete`. | `lesson_status = Complete` |
| 2 | The staff member changes Lesson Status to `Published` and saves the lesson. | The Lesson Status shows `Published`. | `target_status = Published` |
| 3 | The staff member changes the lesson Name to `Algebra Corrected Lesson` and saves the lesson. | The lesson Name saves as `Algebra Corrected Lesson`, confirming Lesson Details are editable after the authorized rollback. | `lesson_name = Algebra Corrected Lesson` |

**Severity:** major  
**Priority:** high

---

### [Riso] Completed Lesson Rollback – Lesson Details – Permission Absent – English Denial Message Shown

**Description:** AC01.1 — Permission Matrix / Component — A staff member without the custom permission receives the exact English denial message.

**Preconditions:**

- A Riso lesson exists with Status = `Complete`.
- A staff member is logged in to Salesforce with English selected.
- The staff member does not have the custom permission defined for LT-96228.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | The staff member opens the completed lesson in Salesforce Lesson Details. | The Lesson Status shows `Complete`. | `locale = English` |
| 2 | The staff member changes Lesson Status to `Published` and saves the lesson. | The message `You are not allowed to change the status of a completed lesson.` is shown exactly. | `target_status = Published` |

**Severity:** major  
**Priority:** high

---

### [Riso] Completed Lesson Rollback – Lesson Details – Permission Absent – Japanese Denial Message Shown

**Description:** AC01.1 — Equivalence Partitioning / Component — A staff member without the custom permission receives the supplied Japanese denial message.

**Preconditions:**

- A Riso lesson exists with Status = `Complete`.
- A staff member is logged in to Salesforce with Japanese selected.
- The staff member does not have the custom permission defined for LT-96228.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | The staff member opens the completed lesson in Salesforce Lesson Details. | The Lesson Status shows `Complete`. | `locale = Japanese` |
| 2 | The staff member changes Lesson Status to `Published` and saves the lesson. | The message `完了済の授業のステータスを変更するには権限が必要です。` is shown exactly. | `target_status = Published` |

**Severity:** major  
**Priority:** high

---

### [Riso] Completed Lesson Rollback – Lesson List Bulk Change – Permission Granted – Completed Lesson Publishes

**Description:** AC02.1 — Permission Matrix / State Transition — An authorized staff member can correct a selected completed lesson from the Salesforce Lesson List bulk action.

**Preconditions:**

- A Riso lesson exists with Status = `Complete`.
- A staff member is logged in to Salesforce.
- The staff member has the custom permission defined for LT-96228.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | The staff member opens the Salesforce Lesson List and selects the completed lesson. | The selected lesson shows Status = `Complete`. | `selected_lesson_status = Complete` |
| 2 | The staff member chooses Bulk Change Lesson Status and selects `Published`. | The bulk action accepts `Published` as the target status. | `target_status = Published` |
| 3 | The staff member submits the bulk change. | The selected lesson shows Status = `Published`. | `custom_permission = assigned` |

**Severity:** critical  
**Priority:** high

---

### [Riso] Completed Lesson Rollback – Lesson List Bulk Change – Permission Absent – Completed Lesson Remains Complete

**Description:** AC01.1 — Permission Matrix / Negative — A Salesforce Lesson List bulk action cannot bypass the custom-permission restriction.

**Preconditions:**

- A Riso lesson exists with Status = `Complete`.
- A staff member is logged in to Salesforce.
- The staff member does not have the custom permission defined for LT-96228.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | The staff member opens the Salesforce Lesson List and selects the completed lesson. | The selected lesson shows Status = `Complete`. | `selected_lesson_status = Complete` |
| 2 | The staff member chooses Bulk Change Lesson Status and selects `Published`. | The bulk action rejects the change with the applicable localized denial message. | `target_status = Published` |
| 3 | The staff member refreshes the Lesson List. | The selected lesson still shows Status = `Complete`. | `custom_permission = absent` |

**Severity:** critical  
**Priority:** high

---

### [Riso] Completed Lesson Rollback – Lesson List Bulk Change – Permission Absent – Teacher Email Is Not Sent

**Description:** AC01.1 — Decision Table / Regression — A blocked bulk correction does not trigger the Riso teacher-email path.

**Preconditions:**

- A Riso lesson exists with Status = `Complete`.
- An available Lesson Teacher with a reachable email address is assigned to the lesson.
- A staff member is logged in to Salesforce.
- The staff member does not have the custom permission defined for LT-96228.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | The staff member selects the completed lesson in the Salesforce Lesson List. | The selected lesson shows Status = `Complete`. | `selected_lesson_status = Complete` |
| 2 | The staff member submits Bulk Change Lesson Status with target status `Published`. | The change is denied and the lesson remains `Complete`. | `target_status = Published` |
| 3 | The staff member opens the assigned teacher's email inbox. | No new Riso lesson-publish email exists for the blocked change. | `expected_emails = 0` |

**Severity:** critical  
**Priority:** high

---

### [Riso] Completed Lesson Rollback – Repeated Requests – Permission Absent – Completed Lesson Remains Complete

**Description:** AC01.1 — Negative / Data Integrity — Repeating a denied correction does not create a partial status change or bypass authorization.

**Preconditions:**

- A Riso lesson exists with Status = `Complete`.
- A staff member is logged in to Salesforce.
- The staff member does not have the custom permission defined for LT-96228.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | The staff member opens the completed lesson in Salesforce Lesson Details. | The Lesson Status shows `Complete`. | `lesson_status = Complete` |
| 2 | The staff member submits the `Published` status change twice without reloading the page. | Both requests are denied and no request changes the status. | `request_count = 2` |
| 3 | The staff member reloads Salesforce Lesson Details. | The Lesson Status still shows `Complete`. | `custom_permission = absent` |

**Severity:** critical  
**Priority:** high

---

