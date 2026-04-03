# Test Cases: LT-92532 — [Riso] Lesson Allocation Detail

> **Scope:** AC 03.1 and AC 03.2 cover changes to the Lesson Allocation Detail view for Riso OOP.
> Class-related UI elements are hidden (red items must hide; blue items hide if low effort).
> AC 03.3 covers the config & control mechanism (Riso-specific feature flag).

---

## Suite: LA Detail – Class-Related Items Hidden

---

### [Riso] Lesson Allocation Detail – Class History Section – Not Displayed

**Description:** AC 03.1 — Decision Table — Verify that the Class History section is hidden from the Lesson Allocation Detail page in the Riso tenant.

**Preconditions:**

- Logged in as HQ or CM user on Riso Salesforce org
- An existing LA is present with start date in the future
- Navigate to the LA detail page (Contact → Course tab → click LA row)

| #   | Action                                          | Expected Result                                            | Test Data |
| --- | ----------------------------------------------- | ---------------------------------------------------------- | --------- |
| 1   | Open the Lesson Allocation Detail page for a LA | LA detail page is displayed                                |           |
| 2   | Inspect the page for a "Class History" section  | No "Class History" section or table is visible on the page |           |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Allocation Detail – Delete/Add Session Buttons – Not Displayed

**Description:** AC 03.1 — Decision Table — Verify that the Delete Session and Add Session action buttons are hidden on the LA Detail page in the Riso tenant.

**Preconditions:**

- Logged in as HQ or CM user on Riso Salesforce org
- An existing LA with at least one session is available
- LA Detail page is open

| #   | Action                                                                      | Expected Result                                               | Test Data |
| --- | --------------------------------------------------------------------------- | ------------------------------------------------------------- | --------- |
| 1   | Open the Lesson Allocation Detail page                                      | LA detail content is displayed                                |           |
| 2   | Inspect for "Delete Session" and "Add Session" buttons or action menu items | Neither "Delete Session" nor "Add Session" control is visible |           |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Allocation Detail – Assign Class Button – Not Displayed

**Description:** AC 03.1 — Decision Table — Verify that the "Assign Class" button is hidden on the LA Detail page in the Riso tenant.

**Preconditions:**

- Logged in as HQ or CM user on Riso Salesforce org
- LA Detail page is open

| #   | Action                                        | Expected Result                                          | Test Data |
| --- | --------------------------------------------- | -------------------------------------------------------- | --------- |
| 1   | Open the Lesson Allocation Detail page        | LA detail content is displayed                           |           |
| 2   | Inspect the page for an "Assign Class" button | No "Assign Class" button is visible anywhere on the page |           |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Allocation Detail – Sync Lesson and Class Button – Not Displayed

**Description:** AC 03.1 — Decision Table — Verify that the "Sync Lesson and Class" button is hidden on the LA Detail page in the Riso tenant.

**Preconditions:**

- Logged in as HQ or CM user on Riso Salesforce org
- LA Detail page is open

| #   | Action                                                | Expected Result                                                   | Test Data |
| --- | ----------------------------------------------------- | ----------------------------------------------------------------- | --------- |
| 1   | Open the Lesson Allocation Detail page                | LA detail content is displayed                                    |           |
| 2   | Inspect the page for a "Sync Lesson and Class" button | No "Sync Lesson and Class" button is visible anywhere on the page |           |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Allocation Detail – Class Field on Header – Not Displayed

**Description:** AC 03.1 — Decision Table (low-effort blue item) — Verify that the "Class" field in the LA Detail header section is hidden for the Riso tenant.

**Preconditions:**

- Logged in as HQ or CM user on Riso Salesforce org
- LA Detail page is open

| #   | Action                                         | Expected Result                                                | Test Data |
| --- | ---------------------------------------------- | -------------------------------------------------------------- | --------- |
| 1   | Open the Lesson Allocation Detail page         | LA detail header area is displayed                             |           |
| 2   | Inspect the header section for a "Class" field | No "Class" field is visible in the header section of LA detail |           |

**Severity:** normal
**Priority:** medium

---

## Suite: LA Detail – Change Location

---

### [Riso] Lesson Allocation Detail – Change Location – Functionality Retained

**Description:** AC 03.2 — CRUD Testing / Regression — Verify that the Change Location functionality in LA Detail still works correctly for Riso tenants.

**Preconditions:**

- Logged in as HQ or CM user on Riso Salesforce org
- An existing LA is available with a defined Location
- The LA does not have a past start date (edit is possible)
- LA Detail page is open

| #   | Action                                             | Expected Result                                                       | Test Data       |
| --- | -------------------------------------------------- | --------------------------------------------------------------------- | --------------- |
| 1   | Open the Lesson Allocation Detail page             | Current Location is displayed in the detail view                      |                 |
| 2   | Click the "Change Location" action or button       | Change Location modal / dialog opens successfully                     |                 |
| 3   | Select a different valid Location from the options | New location is selectable; no error                                  | New Location: B |
| 4   | Confirm the change                                 | Modal closes; LA detail updates to show the new Location              |                 |
| 5   | Verify the updated Location is saved               | Refreshing the page shows the new Location persisted on the LA record |                 |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Allocation Detail – Change Location – Class Fields Not Displayed (if hidden)

**Description:** AC 03.2 — Regression (low-effort blue item) — Verify that class-related fields inside the Change Location modal/popup are hidden or disabled for the Riso tenant.

**Preconditions:**

- Logged in as HQ or CM user on Riso Salesforce org
- LA Detail page is open; Change Location action is available

| #   | Action                                                       | Expected Result                                                                                     | Test Data |
| --- | ------------------------------------------------------------ | --------------------------------------------------------------------------------------------------- | --------- |
| 1   | Click "Change Location" on the LA Detail page                | Change Location modal opens                                                                         |           |
| 2   | Inspect the modal for class-related fields (e.g. Class list) | Class-related fields are hidden or disabled; only location-selection fields are shown               |           |
| 3   | Proceed with location change (non-class fields only)         | Change Location saves successfully using only location-related fields; no class assignment required |           |

**Severity:** normal
**Priority:** medium

---

## Suite: LA Detail – Config & Control

---

### [Riso] Lesson Allocation Detail – Class Items Hidden – Driven by Riso OOP Config

**Description:** AC 03.3 — Decision Table — Verify that all class-related UI items are hidden on LA Detail based on the Riso OOP feature config (not hard-coded per user).

**Preconditions:**

- Riso OOP feature config is enabled for the Riso tenant
- An HQ or CM user is logged in on the Riso Salesforce org
- LA Detail page is open

| #   | Action                                                                        | Expected Result                                                                                                               | Test Data |
| --- | ----------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- | --------- |
| 1   | Open the LA Detail page on the Riso tenant (OOP config enabled)               | Class History, Delete/Add Session, Assign Class, Sync Lesson and Class are all hidden                                         |           |
| 2   | Confirm the same LA Detail on another tenant where the OOP config is disabled | Class History, Delete/Add Session, Assign Class, Sync Lesson and Class are all visible (config does not affect other tenants) |           |

**Severity:** major
**Priority:** high

---
