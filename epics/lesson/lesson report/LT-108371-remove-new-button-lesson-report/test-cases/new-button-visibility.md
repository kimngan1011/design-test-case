# Test Cases: LT-108371 — Remove "New" button from Lesson Report in LA detail page

## Suite: Lesson Report New Button Visibility

### Lesson Allocation Detail – Lesson Report Tab – STAG Core Partner – New button not displayed

**Description:** AC 01 — Component / Decision Table — The removed control is absent for the Core Partner on STAG.

**Preconditions:**

- HQ or CM Staff is logged in to the STAG Core Partner Salesforce org.
- A Lesson Allocation named `LA-CORE-STAG-001` exists.
- The Lesson Allocation has an accessible Lesson Report tab.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff opens `LA-CORE-STAG-001` from Contact → Course. | The Lesson Allocation Detail page for `LA-CORE-STAG-001` is displayed. | `environment=STAG; partner_type=Core Partner; LA=LA-CORE-STAG-001` |
| 2 | HQ or CM Staff selects the Lesson Report tab. | The Lesson Report tab loads and contains no visible control labelled `New`. | `tab=Lesson Report; expected_button_label=New; expected_visibility=absent` |

**Severity:** minor
**Priority:** medium

---

### [Renseikai] Lesson Allocation Detail – Lesson Report Tab – PREPROD Core Partner – New button not displayed

**Description:** AC 01 — Component / Decision Table — The removed control is absent for Renseikai on PREPROD.

**Preconditions:**

- HQ or CM Staff is logged in to the PREPROD Renseikai Salesforce org.
- A Lesson Allocation named `LA-REN-PRE-001` exists.
- The Lesson Allocation has an accessible Lesson Report tab.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff opens `LA-REN-PRE-001` from Contact → Course. | The Lesson Allocation Detail page for `LA-REN-PRE-001` is displayed. | `environment=PREPROD; partner=Renseikai; LA=LA-REN-PRE-001` |
| 2 | HQ or CM Staff selects the Lesson Report tab. | The Lesson Report tab loads and contains no visible control labelled `New`. | `tab=Lesson Report; expected_button_label=New; expected_visibility=absent` |

**Severity:** minor
**Priority:** medium

---

### [Nichibei] Lesson Allocation Detail – Lesson Report Tab – PREPROD Custom Partner – New button not displayed

**Description:** AC 01 — Component / Decision Table — The removed control is absent for Nichibei on PREPROD.

**Preconditions:**

- HQ or CM Staff is logged in to the PREPROD Nichibei Salesforce org.
- A Lesson Allocation named `LA-NIC-PRE-001` exists.
- The Lesson Allocation has an accessible Lesson Report tab.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff opens `LA-NIC-PRE-001` from Contact → Course. | The Lesson Allocation Detail page for `LA-NIC-PRE-001` is displayed. | `environment=PREPROD; partner=Nichibei; LA=LA-NIC-PRE-001` |
| 2 | HQ or CM Staff selects the Lesson Report tab. | The Lesson Report tab loads and contains no visible control labelled `New`. | `tab=Lesson Report; expected_button_label=New; expected_visibility=absent` |

**Severity:** minor
**Priority:** medium

---

### [EEA] Lesson Allocation Detail – Lesson Report Tab – PREPROD Custom Partner – New button not displayed

**Description:** AC 01 — Component / Decision Table — The removed control is absent for EEA on PREPROD.

**Preconditions:**

- HQ or CM Staff is logged in to the PREPROD EEA Salesforce org.
- A Lesson Allocation named `LA-EEA-PRE-001` exists.
- The Lesson Allocation has an accessible Lesson Report tab.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff opens `LA-EEA-PRE-001` from Contact → Course. | The Lesson Allocation Detail page for `LA-EEA-PRE-001` is displayed. | `environment=PREPROD; partner=EEA; LA=LA-EEA-PRE-001` |
| 2 | HQ or CM Staff selects the Lesson Report tab. | The Lesson Report tab loads and contains no visible control labelled `New`. | `tab=Lesson Report; expected_button_label=New; expected_visibility=absent` |

**Severity:** minor
**Priority:** medium

---

### [Aver] Lesson Allocation Detail – Lesson Report Tab – PREPROD Custom Partner – New button not displayed

**Description:** AC 01 — Component / Decision Table — The removed control is absent for Aver on PREPROD.

**Preconditions:**

- HQ or CM Staff is logged in to the PREPROD Aver Salesforce org.
- A Lesson Allocation named `LA-AVG-PRE-001` exists.
- The Lesson Allocation has an accessible Lesson Report tab.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff opens `LA-AVG-PRE-001` from Contact → Course. | The Lesson Allocation Detail page for `LA-AVG-PRE-001` is displayed. | `environment=PREPROD; partner=Aver; LA=LA-AVG-PRE-001` |
| 2 | HQ or CM Staff selects the Lesson Report tab. | The Lesson Report tab loads and contains no visible control labelled `New`. | `tab=Lesson Report; expected_button_label=New; expected_visibility=absent` |

**Severity:** minor
**Priority:** medium

---

### [Riso] Lesson Allocation Detail – Lesson Report Tab – PREPROD Custom Partner – New button not displayed

**Description:** AC 01 — Component / Decision Table — The removed control is absent for Riso on PREPROD.

**Preconditions:**

- HQ or CM Staff is logged in to the PREPROD Riso Salesforce org.
- A Lesson Allocation named `LA-RIS-PRE-001` exists.
- The Lesson Allocation has an accessible Lesson Report tab.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff opens `LA-RIS-PRE-001` from Contact → Course. | The Lesson Allocation Detail page for `LA-RIS-PRE-001` is displayed. | `environment=PREPROD; partner=Riso; LA=LA-RIS-PRE-001` |
| 2 | HQ or CM Staff selects the Lesson Report tab. | The Lesson Report tab loads and contains no visible control labelled `New`. | `tab=Lesson Report; expected_button_label=New; expected_visibility=absent` |

**Severity:** minor
**Priority:** medium

---

### Lesson Allocation Detail – Lesson Report Tab – Full Access permission set – New button not displayed

**Description:** AC 01 — Component / Permission Matrix — The removed control is absent for a user with the `full_access` permission set.

**Preconditions:**

- A staff user assigned the `full_access` permission set is logged in to the Salesforce test org selected for execution.
- A Lesson Allocation named `LA-ROLE-FULL-001` exists.
- The Lesson Allocation has an accessible Lesson Report tab.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Full Access Staff opens `LA-ROLE-FULL-001` from Contact → Course. | The Lesson Allocation Detail page for `LA-ROLE-FULL-001` is displayed. | `access_profile=full_access; LA=LA-ROLE-FULL-001` |
| 2 | Full Access Staff selects the Lesson Report tab. | The Lesson Report tab loads and contains no visible control labelled `New`. | `tab=Lesson Report; expected_button_label=New; expected_visibility=absent` |

**Severity:** minor
**Priority:** medium

---

### Lesson Allocation Detail – Lesson Report Tab – Center Level Edit permission set – New button not displayed

**Description:** AC 01 — Component / Permission Matrix — The removed control is absent for a user with the `center_level_edit` permission set.

**Preconditions:**

- A staff user assigned the `center_level_edit` permission set is logged in to the Salesforce test org selected for execution.
- A Lesson Allocation named `LA-ROLE-CLE-001` exists.
- The Lesson Allocation has an accessible Lesson Report tab.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Center Level Edit Staff opens `LA-ROLE-CLE-001` from Contact → Course. | The Lesson Allocation Detail page for `LA-ROLE-CLE-001` is displayed. | `access_profile=center_level_edit; LA=LA-ROLE-CLE-001` |
| 2 | Center Level Edit Staff selects the Lesson Report tab. | The Lesson Report tab loads and contains no visible control labelled `New`. | `tab=Lesson Report; expected_button_label=New; expected_visibility=absent` |

**Severity:** minor
**Priority:** medium

---

### Lesson Allocation Detail – Lesson Report Tab – Admin – New button not displayed

**Description:** AC 01 — Component / Permission Matrix — The removed control is absent for an Admin user.

**Preconditions:**

- An Admin user is logged in to the Salesforce test org selected for execution.
- A Lesson Allocation named `LA-ROLE-ADMIN-001` exists.
- The Lesson Allocation has an accessible Lesson Report tab.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Admin opens `LA-ROLE-ADMIN-001` from Contact → Course. | The Lesson Allocation Detail page for `LA-ROLE-ADMIN-001` is displayed. | `access_profile=Admin; LA=LA-ROLE-ADMIN-001` |
| 2 | Admin selects the Lesson Report tab. | The Lesson Report tab loads and contains no visible control labelled `New`. | `tab=Lesson Report; expected_button_label=New; expected_visibility=absent` |

**Severity:** minor
**Priority:** medium
