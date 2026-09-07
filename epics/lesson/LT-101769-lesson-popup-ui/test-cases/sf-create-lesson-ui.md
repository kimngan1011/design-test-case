# Test Cases: LT-101769 — Improve Lesson popup UI

## Suite: SF Create Lesson UI

### Lesson Popup – SF Create – New Lesson modal – Default state – Designed hierarchy and actions shown

**Description:** AC 01.1 — Component — The New Lesson popup presents the Figma-defined modal hierarchy for staff.

**Preconditions:**
- Logged in as HQ or CM Staff to Salesforce.
- Lesson Management is available and the user can open the New Lesson popup.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Lesson Management and select the New Lesson action. | The New Lesson popup opens over the Lesson screen. | Figma node = 12148:60157 |
| 2 | Review the popup from header to footer. | The modal shows its title, content area, close control, and footer actions in the designed hierarchy. | State = default |
| 3 | Review the visible form layout without changing values. | Controls are grouped and aligned without overlap, clipping, or an unintended page scroll. | Viewport = desktop design |

**Severity:** minor
**Priority:** medium

---

### Lesson Popup – SF Create – Validation feedback – Error state – Designed error treatment shown

**Description:** AC 01.1 — Negative — A configured invalid-form scenario presents the Figma error treatment without losing the popup layout.

**Preconditions:**
- Logged in as HQ or CM Staff to Salesforce.
- A non-persistent invalid-form scenario is available in the QA environment.
- New Lesson popup is open with the scenario’s required UI state.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Trigger the existing invalid-form scenario. | The popup remains open and displays the designed error treatment. | Scenario = existing invalid-form UI state |
| 2 | Review the affected controls and footer. | Error feedback is visible, readable, and does not obscure the form controls or actions. | Figma state = error |

**Severity:** major
**Priority:** high

---

### Lesson Popup – Japanese Localization – SF Create screen – Japanese locale – User-facing copy shown in Japanese

**Description:** AC 06.1 — Component — The SF Create screen presents Japanese user-facing copy when the interface locale is Japanese.

**Preconditions:**
- Logged in as HQ or CM Staff to Salesforce with the interface locale set to Japanese.
- The New Lesson popup is open.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Review the New Lesson popup from header to footer. | The title, labels, field hints, and actions use Japanese text; only approved product names or proper nouns remain unchanged. | Locale = Japanese; Screen = SF Create |
| 2 | Review any visible feedback or helper text. | User-facing feedback and helper text use Japanese and remain readable without truncation or overlap. | State = available UI feedback |

**Severity:** minor
**Priority:** medium

---

### Lesson Popup – SF Create – Success feedback – Completion state – Designed toast shown

**Description:** AC 01.1 — Decision Table — The existing completion state presents the Figma success toast and message.

**Preconditions:**
- Logged in as HQ or CM Staff to Salesforce.
- A non-production lesson fixture can reach the existing completion-feedback UI state.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Use the fixture to reach the existing completion-feedback state. | A success toast appears in the designed position and styling. | Figma state = success |
| 2 | Read the toast message. | The toast states “You have created lesson item successfully!” and includes the designed close control. | Expected message = You have created lesson item successfully! |

**Severity:** major
**Priority:** high

---

### Lesson Popup – SF Create – Lesson flow – New action – Create form opens

**Description:** AC 01.1 — Regression — The Lesson flow opens the designed SF Create form.

**Preconditions:**
- Logged in as HQ or CM Staff to Salesforce.
- Lesson Management list is open.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Select the New Lesson action from the Lesson flow. | The New Lesson popup opens over the Lesson screen. | Entry point = Lesson |
| 2 | Review the opened popup. | The form title, content area, close control, and footer actions match the designed SF Create UI. | Figma node = 12148:60157 |

**Severity:** minor
**Priority:** medium

---

### Lesson Popup – SF Create – Calendar flow – New action – Create form opens

**Description:** AC 01.1 — Regression — The Calendar flow opens the designed SF Create form.

**Preconditions:**
- Logged in as HQ or CM Staff to Salesforce.
- Lesson Calendar is open.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Select the New Lesson action from the Calendar flow. | The New Lesson popup opens over the Calendar screen. | Entry point = Calendar |
| 2 | Review the opened popup. | The form title, content area, close control, and footer actions match the designed SF Create UI. | Figma node = 12148:60157 |

**Severity:** minor
**Priority:** medium

---

### Lesson Popup – SF Create – Duplicate flow – Duplicate action – Create form opens

**Description:** AC 01.1 — Regression — The Duplicate flow opens the designed SF Create form.

**Preconditions:**
- Logged in as HQ or CM Staff to Salesforce.
- An existing lesson with the Duplicate action is available.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Select Duplicate for the existing lesson. | The New Lesson popup opens in the duplicate-flow context. | Entry point = Duplicate; Lesson = existing fixture |
| 2 | Review the opened popup. | The form title, content area, close control, and footer actions match the designed SF Create UI. | Figma node = 12148:60157 |

**Severity:** minor
**Priority:** medium
