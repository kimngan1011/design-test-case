# Test Cases: LT-96662 — Publish and Notify Student

## Suite: Publish and Notify Student – Button Visibility

### Publish and Notify Button – Draft Lesson – "Publish and notify student" button visible

**Description:** AC 01.1 — Decision Table — The "Publish and notify student" button is visible on the SF Lesson Detail page when lesson status is Draft.

**Preconditions:**

- User is logged into SF with the **"Publish Lesson With Notification"** custom permission (member of the Renseikai OOP Permission Set)
- A lesson exists with status = **Draft** and has an assigned student

| #   | Action                                                    | Expected Result                                      | Test Data                             |
| --- | --------------------------------------------------------- | ---------------------------------------------------- | ------------------------------------- |
| 1   | Navigate to the SF Lesson Detail page of the Draft lesson | Lesson Detail page opens; status label shows "Draft" | Draft lesson ID with assigned student |
| 2   | Observe the action buttons area at the top of the page    | "Publish and notify student" button is visible       | ""                                    |

**Severity:** major
**Priority:** high

---

### Publish and Notify Button – Published Lesson – "Publish and notify student" button visible

**Description:** AC 01.1 — Decision Table — The "Publish and notify student" button is visible on the SF Lesson Detail page when lesson status is Published.

**Preconditions:**

- User is logged into SF with the **"Publish Lesson With Notification"** custom permission (member of the Renseikai OOP Permission Set)
- A lesson exists with status = **Published** and has an assigned student

| #   | Action                                                        | Expected Result                                          | Test Data                                 |
| --- | ------------------------------------------------------------- | -------------------------------------------------------- | ----------------------------------------- |
| 1   | Navigate to the SF Lesson Detail page of the Published lesson | Lesson Detail page opens; status label shows "Published" | Published lesson ID with assigned student |
| 2   | Observe the action buttons area                               | "Publish and notify student" button is visible           | ""                                        |

**Severity:** major
**Priority:** high

---

### Publish and Notify Button – Completed Lesson – "Publish and notify student" button not visible

**Description:** AC 01.1 — Decision Table + Negative Testing — The "Publish and notify student" button is hidden when lesson status is Completed.

**Preconditions:**

- User is logged into SF with the **"Publish Lesson With Notification"** custom permission (member of the Renseikai OOP Permission Set)
- A lesson exists with status = **Completed**

| #   | Action                                                        | Expected Result                                                    | Test Data           |
| --- | ------------------------------------------------------------- | ------------------------------------------------------------------ | ------------------- |
| 1   | Navigate to the SF Lesson Detail page of the Completed lesson | Lesson Detail page opens; status label shows "Completed"           | Completed lesson ID |
| 2   | Observe the action buttons area                               | "Publish and notify student" button is **not present** on the page | ""                  |

**Severity:** major
**Priority:** high

---

### Publish and Notify Button – Cancelled Lesson – "Publish and notify student" button not visible

**Description:** AC 01.1 — Decision Table + Negative Testing — The "Publish and notify student" button is hidden when lesson status is Cancelled.

**Preconditions:**

- User is logged into SF with the **"Publish Lesson With Notification"** custom permission (member of the Renseikai OOP Permission Set)
- A lesson exists with status = **Cancelled**

| #   | Action                                                        | Expected Result                                                    | Test Data           |
| --- | ------------------------------------------------------------- | ------------------------------------------------------------------ | ------------------- |
| 1   | Navigate to the SF Lesson Detail page of the Cancelled lesson | Lesson Detail page opens; status label shows "Cancelled"           | Cancelled lesson ID |
| 2   | Observe the action buttons area                               | "Publish and notify student" button is **not present** on the page | ""                  |

**Severity:** major
**Priority:** high

---

### Publish and Notify Button – User Without Custom Permission – Button not visible regardless of lesson status

**Description:** PRD — Decision Table — When the logged-in SF user does **not** have the custom permission "Publish Lesson With Notification", the button does not appear on any lesson regardless of status.

**Preconditions:**

- User is logged into SF **without** the "Publish Lesson With Notification" custom permission (not a member of the Renseikai OOP Permission Set)
- A lesson exists with status = **Draft** and an assigned student

| #   | Action                                                      | Expected Result                                        | Test Data                            |
| --- | ----------------------------------------------------------- | ------------------------------------------------------ | ------------------------------------ |
| 1   | Navigate to the SF Lesson Detail page of the Draft lesson   | Lesson Detail page opens; status = "Draft"             | Draft lesson ID                      |
| 2   | Observe the action buttons area                             | "Publish and notify student" button is **not present** | ""                                   |
| 3   | Navigate to the SF Lesson Detail page of a Published lesson | Lesson Detail page opens; status = "Published"         | Published lesson ID in Renseikai org |
| 4   | Observe the action buttons area                             | "Publish and notify student" button is **not present** | ""                                   |

**Severity:** major
**Priority:** high

---

### Publish and Notify Button – Partner Without OOP Permission Set – Button not visible on SF Lesson Detail page

**Description:** PRD — Permission Matrix — The "Publish and notify student" button is not visible for SF users who do not have the custom permission "Publish Lesson With Notification" (e.g. users from a partner org whose OOP PS does not include this permission).

> ⚠️ **Note:** Requires access to a non-Renseikai partner sandbox where the OOP PS does not include the "Publish Lesson With Notification" custom permission.

**Preconditions:**

- Logged into SF under a **partner org without the "Publish Lesson With Notification" custom permission** (e.g. non-Renseikai partner, or Renseikai user not assigned the OOP PS)
- A lesson exists with status = Draft

| #   | Action                                                  | Expected Result                                        | Test Data       |
| --- | ------------------------------------------------------- | ------------------------------------------------------ | --------------- |
| 1   | Navigate to the SF Lesson Detail page of a Draft lesson | Lesson Detail page opens; status = "Draft"             | Draft lesson ID |
| 2   | Observe the action buttons area                         | "Publish and notify student" button is **not present** | ""              |

**Severity:** major
**Priority:** high

---
