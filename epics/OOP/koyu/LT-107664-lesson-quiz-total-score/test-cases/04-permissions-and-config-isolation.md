# Test Cases: LT-107664 — Koyu Lesson Quiz and Total Score

## Suite: [Koyu] Permissions and Configuration Isolation

### [Koyu] Lesson Report – Full-access staff – Active score layout – Editing allowed

**Description:** AC 2.1.1 — Permission Matrix — Full-access staff can edit the active score fields.

**Preconditions:**

- A full-access staff member is logged in to the Koyu Salesforce organization.
- The SF Lesson Custom Setting is `ON`.
- Student A's Lesson Report Detail is editable.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | The full-access staff member opens Student A's Lesson Report. | Total Score and Test Result are visible and editable. | staff_role = full_access |
| 2 | The full-access staff member enters Total Score `20.0` and saves the report. | The save completes and Total Score displays `20.0`. | total_score = 20.0 |

**Severity:** major
**Priority:** high

---

### [Koyu] Lesson Report – Centre-level staff – Active score layout – Editing allowed

**Description:** AC 2.1.1 — Permission Matrix — Centre-level-edit staff can edit the active score fields.

**Preconditions:**

- A centre-level-edit staff member is logged in to the Koyu Salesforce organization.
- The SF Lesson Custom Setting is `ON`.
- Student A's Lesson Report Detail is editable.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | The centre-level staff member opens Student A's Lesson Report. | Total Score and Test Result are visible and editable. | staff_role = center_level_edit |
| 2 | The centre-level staff member enters Test Result `18.5` and saves the report. | The save completes and Test Result displays `18.5`. | test_result = 18.5 |

**Severity:** minor
**Priority:** medium

---

### [Koyu] Lesson Report – BO teacher – Active score layout – Editing allowed

**Description:** AC 2.1.1 — Permission Matrix — A BO teacher can edit the active score fields.

**Preconditions:**

- A BO teacher is logged in to the Koyu Back Office.
- The BO internal score setting is `ON`.
- Student A's Lesson Report Detail is editable.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | The BO teacher opens Student A's Lesson Report. | Total Score and Test Result are visible and editable. | staff_role = bo_teacher |
| 2 | The BO teacher enters Total Score `20.0` and saves the report. | The save completes and Total Score displays `20.0`. | total_score = 20.0 |

**Severity:** minor
**Priority:** medium

---

### [Koyu] Learner App – Student – Active score layout – Editing unavailable

**Description:** AC 2.1.2 — Permission Matrix / Negative — A student can read but cannot edit active score fields.

**Preconditions:**

- Student A is logged in to the Koyu Learner App.
- The App internal score setting is `ON`.
- Student A's lesson and Lesson Report are published.
- Student A's Total Score is `20.0`.
- Student A's Test Result is `18.5`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Student A opens the published Lesson Report. | Total Score `20.0` and Test Result `18.5` display read-only. | actor = Student A |
| 2 | Student A selects the score area. | No editable field, Save action, or score modification control is available. | expected_access = read_only |

**Severity:** major
**Priority:** high

---

### [Koyu] Learner App – Parent – Active score layout – Selected child values displayed read-only

**Description:** AC 2.1.2 — Permission Matrix / Component — A parent reads the selected child's active score fields without edit access.

**Preconditions:**

- Parent A is logged in to the Koyu Learner App.
- Parent A selects Student A.
- The App internal score setting is `ON`.
- Student A's lesson and Lesson Report are published.
- Student A's Total Score is `20.0`.
- Student A's Test Result is `18.5`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Parent A opens Student A's published Lesson Report. | Total Score `20.0` and Test Result `18.5` display read-only. | actor = Parent A; selected_student = A |
| 2 | Parent A selects the score area. | No editable field, Save action, or score modification control is available. | expected_access = read_only |

**Severity:** minor
**Priority:** medium

---

### [Koyu] Lesson Report – Koyu configuration – Other organization – New score layout not exposed

**Description:** Scope — Permission Matrix / Regression — The Koyu-specific score layout does not leak to another organization.

**Preconditions:**

- HQ or CM Staff is logged in to a non-Koyu organization.
- The Koyu SF Lesson Custom Setting is `ON` only for Koyu.
- A comparable Lesson Report exists in the non-Koyu organization.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff opens the comparable Lesson Report in the non-Koyu organization. | The Koyu-only Total Score and Test Result layout does not appear. | organization = non-Koyu; koyu_setting = ON |
| 2 | HQ or CM Staff opens the same type of Lesson Report in Koyu. | The Koyu active layout follows Koyu's own configuration without affecting the non-Koyu organization. | organization = Koyu |

**Severity:** major
**Priority:** high
