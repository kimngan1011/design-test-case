# Test Cases: LT-98532 — Bulk Publish Lessons by Student

## Suite: [Riso] Bulk Publish by Student – Async Job

---

### [Riso] Bulk Publish – Submit – Success Message Displayed and User Redirected to Calendar

**Description:** AC 01.4 — Equivalence Partitioning — After completing the Bulk Publish modal and clicking Save, a success message is shown and the user is redirected to the previous calendar view.

**Preconditions:**

- User is logged into SF as a Riso HQ Admin
- SF Calendar is open; at least 1 Draft lesson exists in the selected period
- Bulk Publish modal is filled in with all required fields
- "Apply to selected students" checkbox may be activated or not (behavior is the same)

| #   | Action                                                 | Expected Result                                                                                                   | Test Data                                        |
| --- | ------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------- | ------------------------------------------------ |
| 1   | Complete all required fields in the Bulk Publish modal | All fields are filled; form is valid                                                                              | Period: May 1–31, 2026; Location: "Hanoi Branch" |
| 2   | Click **Save**                                         | Modal closes; a success message appears                                                                           | ""                                               |
| 3   | Read the success message text                          | Message reads: **"Bulk publish lesson request has been submitted successfully. Changes will be applied shortly"** | ""                                               |
| 4   | Observe the page after the message dismisses           | User is back on the **Calendar page** at the same period and location as before opening the modal                 | ""                                               |

**Severity:** minor
**Priority:** medium

---

### [Riso] Bulk Publish – After Submit – Lesson Status Not Immediately Updated on Calendar

**Description:** AC 01.4 — State Transition Testing — Immediately after submitting the Bulk Publish request, the Calendar still shows Draft status for the lessons because the job runs asynchronously.

**Preconditions:**

- User is logged into SF as a Riso HQ Admin
- The period contains at least 2 Draft lessons (Lesson X and Lesson Y)
- Bulk Publish modal submitted and success message has appeared
- User is back on the Calendar view

| #   | Action                                                                  | Expected Result                                           | Test Data        |
| --- | ----------------------------------------------------------------------- | --------------------------------------------------------- | ---------------- |
| 1   | After the success message, observe Lesson X on the Calendar immediately | Lesson X still shows status **"Draft"** — not yet updated | Lesson X (Draft) |
| 2   | Observe Lesson Y on the Calendar immediately                            | Lesson Y still shows status **"Draft"** — not yet updated | Lesson Y (Draft) |
| 3   | Wait a few seconds without clicking Refresh                             | Lesson statuses do **not** automatically update on screen | ""               |

**Severity:** major
**Priority:** high

---

### [Riso] Bulk Publish – Click Refresh – Calendar Shows Updated Published Status

**Description:** AC 01.4 — State Transition Testing — After clicking the Refresh button on the Calendar, the lesson statuses update to "Published" reflecting the completed async job.

**Preconditions:**

- User is logged into SF as a Riso HQ Admin
- Bulk Publish request has been submitted; the async job has had sufficient time to complete (at least a few seconds)
- User is on the Calendar page; lessons still show "Draft" (no Refresh yet)

| #   | Action                                                              | Expected Result                        | Test Data |
| --- | ------------------------------------------------------------------- | -------------------------------------- | --------- |
| 1   | Observe the Calendar before Refresh — note Lesson X showing "Draft" | Lesson X shows **"Draft"**             | Lesson X  |
| 2   | Click the **Refresh** button on the Calendar                        | Calendar reloads data from the server  | ""        |
| 3   | Observe Lesson X after Refresh                                      | Lesson X status is now **"Published"** | ""        |
| 4   | Observe Lesson Y after Refresh                                      | Lesson Y status is now **"Published"** | ""        |

**Severity:** major
**Priority:** high

---

### [Riso] Bulk Publish – Student-Scoped Publish – Only Draft Lessons of Selected Students Are Published

**Description:** AC 01.4 — State Transition Testing — When the "Apply to selected students" checkbox is activated, only the Draft lessons belonging to the students in the Calendar filter are published; lessons of students outside the filter remain Draft.

**Preconditions:**

- User is logged into SF as a Riso HQ Admin
- SF Calendar period contains:
  - Lesson A (Draft) assigned to Student A (in the student filter)
  - Lesson B (Draft) assigned to Student B (NOT in the student filter)
- Student A is selected in the Calendar student filter
- Bulk Publish modal: "Apply to selected students" checkbox **activated**, all required fields complete

| #   | Action                                                           | Expected Result                                                    | Test Data |
| --- | ---------------------------------------------------------------- | ------------------------------------------------------------------ | --------- |
| 1   | Submit the Bulk Publish modal with checkbox activated            | Success message appears; user redirected to Calendar               | ""        |
| 2   | Click **Refresh** on the Calendar                                | Calendar reloads                                                   | ""        |
| 3   | Observe Lesson A (Student A's Draft lesson)                      | Lesson A status is now **"Published"**                             | Lesson A  |
| 4   | Observe Lesson B (Student B's Draft lesson — outside the filter) | Lesson B status is still **"Draft"** — not affected by the publish | Lesson B  |

**Severity:** critical
**Priority:** high

---

### [Riso] Bulk Publish – Student-Scoped Publish – Published, Completed, and Cancelled Lessons Not Changed

**Description:** AC 01.4 — State Transition Testing + Negative Testing — When the Bulk Publish job runs, lessons that are already Published, Completed, or Cancelled remain in their existing status and are not altered.

**Preconditions:**

- User is logged into SF as a Riso HQ Admin
- SF Calendar period contains, all assigned to Student A (in the filter):
  - Lesson A (Draft)
  - Lesson B (Published)
  - Lesson C (Completed)
  - Lesson D (Cancelled)
- Bulk Publish modal submitted with "Apply to selected students" activated

| #   | Action                                                                      | Expected Result                                     | Test Data |
| --- | --------------------------------------------------------------------------- | --------------------------------------------------- | --------- |
| 1   | Submit the Bulk Publish modal and click **Refresh** after the job completes | Calendar shows updated data                         | ""        |
| 2   | Observe Lesson A (Draft)                                                    | Lesson A is now **"Published"**                     | Lesson A  |
| 3   | Observe Lesson B (Published)                                                | Lesson B remains **"Published"** — status unchanged | Lesson B  |
| 4   | Observe Lesson C (Completed)                                                | Lesson C remains **"Completed"** — status unchanged | Lesson C  |
| 5   | Observe Lesson D (Cancelled)                                                | Lesson D remains **"Cancelled"** — status unchanged | Lesson D  |

**Severity:** critical
**Priority:** high

---

### [Riso] Bulk Publish – Period-Scoped Publish – Draft Lessons Outside the Selected Period Are Not Published

**Description:** AC 01.4 — Boundary Value Analysis — When the Bulk Publish job runs for a selected period, only Draft lessons whose dates fall within that period are published. Draft lessons of the same student that fall outside the period boundary remain unchanged.

**Preconditions:**

- User is logged into SF as a Riso HQ Admin
- Student A is selected in the Calendar student filter
- Bulk Publish period is set to **May 1, 2026 ~ May 31, 2026**
- The following Draft lessons exist for Student A:
  - Lesson A on **May 15, 2026** (within the period)
  - Lesson B on **June 5, 2026** (outside the period — after the end date)
  - Lesson C on **April 28, 2026** (outside the period — before the start date)
- "Apply to selected students" checkbox activated; all required fields complete

| #   | Action                                                   | Expected Result                                                                              | Test Data                 |
| --- | -------------------------------------------------------- | -------------------------------------------------------------------------------------------- | ------------------------- |
| 1   | Submit the Bulk Publish modal with period May 1–31, 2026 | Success message appears; user redirected to Calendar                                         | Period: May 1–31, 2026    |
| 2   | Click **Refresh** on the Calendar                        | Calendar reloads                                                                             | ""                        |
| 3   | Navigate to May 2026 and observe Lesson A (May 15)       | Lesson A status is now **"Published"**                                                       | Lesson A — May 15, 2026   |
| 4   | Navigate to June 2026 and observe Lesson B (June 5)      | Lesson B status is still **"Draft"** — not affected because it is outside the publish period | Lesson B — June 5, 2026   |
| 5   | Navigate to April 2026 and observe Lesson C (April 28)   | Lesson C status is still **"Draft"** — not affected because it is outside the publish period | Lesson C — April 28, 2026 |

**Severity:** critical
**Priority:** high

---

### [Riso] Bulk Publish – Location-Scoped Publish – Only Lessons at the Calendar's Selected Location Are Published; Lessons of the Same Students at Other Locations Remain Draft

**Description:** AC 01.3 + AC 01.4 — Decision Table + Boundary Value Analysis — When the "Apply to selected students" checkbox is activated, the Location field is locked to the calendar's current location. Only Draft lessons of the selected students **at that locked location** are published. Draft lessons of the same students at any other location are not affected.

**Preconditions:**

- User is logged into SF as a Riso HQ Admin
- SF Calendar is set to location **"Hanoi Branch"** and period May 1–31, 2026
- Two students are selected in the Calendar student filter: Student A and Student B
- Draft lessons within the period:
  - Lesson A1 (Student A, **Hanoi Branch** — the locked location)
  - Lesson A2 (Student A, **Osaka Branch** — a different location)
  - Lesson B1 (Student B, **Hanoi Branch** — the locked location)
  - Lesson B2 (Student B, **Tokyo Branch** — a different location)
- "Apply to selected students" checkbox activated; Location field shows **"Hanoi Branch"** (locked, read-only)

| #   | Action                                                                        | Expected Result                                                                             | Test Data                       |
| --- | ----------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- | ------------------------------- |
| 1   | Confirm the Location field in the modal shows "Hanoi Branch" and is read-only | Location field displays "Hanoi Branch"; field is disabled and cannot be changed             | Calendar location: Hanoi Branch |
| 2   | Submit the Bulk Publish modal                                                 | Success message appears; user redirected to Calendar                                        | ""                              |
| 3   | Click **Refresh** on the Calendar                                             | Calendar reloads                                                                            | ""                              |
| 4   | Observe Lesson A1 (Student A, Hanoi Branch)                                   | Lesson A1 status is now **"Published"**                                                     | Lesson A1                       |
| 5   | Observe Lesson B1 (Student B, Hanoi Branch)                                   | Lesson B1 status is now **"Published"**                                                     | Lesson B1                       |
| 6   | Navigate to the Osaka Branch calendar view and observe Lesson A2              | Lesson A2 status is still **"Draft"** — not published because it is at a different location | Lesson A2                       |
| 7   | Navigate to the Tokyo Branch calendar view and observe Lesson B2              | Lesson B2 status is still **"Draft"** — not published because it is at a different location | Lesson B2                       |

**Severity:** critical
**Priority:** high

---
