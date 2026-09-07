# Test Cases: LT-101769 — Improve Lesson popup UI

## Suite: BO Edit Lesson UI

### Lesson Popup – BO Edit – Calendar entry point – Hover state – Edit dialog opens

**Description:** AC 03.1 — Regression — The BO Calendar exposes the Figma edit entry point for an editable lesson.

**Preconditions:**
- Logged in as HQ Staff to Back Office.
- An editable lesson is visible on the BO Calendar.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Hover the editable lesson on the Calendar. | The Edit affordance is visible in the designed hover state. | Figma frame = 12152:131902 |
| 2 | Select Edit. | The Edit Lesson dialog opens over the BO Calendar. | Entry point = Calendar |

**Severity:** minor
**Priority:** medium

---

### Lesson Popup – BO Edit – Lesson Detail entry point – Edit action – Edit dialog opens

**Description:** AC 03.1 — Regression — The Lesson Detail page exposes the designed edit action.

**Preconditions:**
- Logged in as HQ Staff to Back Office.
- An editable lesson is open on the Lesson Detail page.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Locate the Edit action on Lesson Detail. | The action is visible and consistent with the Figma entry point. | Entry point = Lesson Detail |
| 2 | Select Edit. | The Edit Lesson dialog opens over the Lesson Detail page. | Figma frame = 12287:150600 |

**Severity:** minor
**Priority:** medium

---

### Lesson Popup – BO Edit – Edit Lesson dialog – Default state – Designed section hierarchy shown

**Description:** AC 03.1 — Component — The BO dialog groups all designed information sections for scanning.

**Preconditions:**
- Logged in as HQ Staff to Back Office.
- The Edit Lesson dialog is open for an existing editable lesson.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Review the dialog title and content sections. | The dialog title is “Edit Lesson”; Basic information, Schedule, Location Course, and Recurring Settings are visible in the designed order. | Figma node = 12287:150381 |
| 2 | Review dialog actions. | The dialog actions are visible, aligned, and remain accessible without overlapping the content. | Viewport = desktop design |

**Severity:** major
**Priority:** high

---

### Lesson Popup – Japanese Localization – BO Edit screen – Japanese locale – User-facing copy shown in Japanese

**Description:** AC 06.1 — Component — The BO Edit dialog presents Japanese user-facing copy when the interface locale is Japanese.

**Preconditions:**
- Logged in as HQ Staff to Back Office with the interface locale set to Japanese.
- The Edit Lesson dialog is open.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Review the dialog title, Basic information, Schedule, Location Course, and Recurring Settings. | Each section title, field label, action, and radio-button label uses Japanese text; only approved product names or proper nouns remain unchanged. | Locale = Japanese; Screen = BO Edit |
| 2 | Review any visible feedback or helper text. | User-facing feedback and helper text use Japanese and remain readable without truncation or overlap. | State = available UI feedback |

**Severity:** minor
**Priority:** medium

---

### Lesson Popup – BO Edit – Field states – Existing lesson displayed – Editable and disabled appearances distinguished

**Description:** AC 03.1 — Component — The dialog visually distinguishes editable, disabled, and read-only controls as designed.

**Preconditions:**
- Logged in as HQ Staff to Back Office.
- The Edit Lesson dialog is open for a fixture containing populated and non-editable values.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Review populated controls across Basic information, Schedule, and Location Course. | Editable controls use the enabled presentation; fixed controls use the disabled or read-only presentation. | Fixture = populated editable lesson |
| 2 | Compare the controls with the section layout. | Field states are visually distinct and labels remain legible. | Figma node = 12287:150381 |

**Severity:** major
**Priority:** high

---

### Lesson Popup – BO Edit – Recurring Settings – Default state – One Time and Weekly Recurring choices shown

**Description:** AC 03.1 — Component — The BO saving option presents the confirmed recurring choices with the designed selection treatment.

**Preconditions:**
- Logged in as HQ Staff to Back Office.
- The Edit Lesson dialog is open.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to the Recurring Settings section. | The section is visible after the lesson information and divider. | Figma node = 12287:150429 |
| 2 | Review the available choices. | “One Time” and “Weekly Recurring” are displayed with the designed radio-button appearance. | Confirmed labels = One Time; Weekly Recurring |

**Severity:** major
**Priority:** high

---

### Lesson Popup – BO Edit – Feedback presentation – Error and success states – Corresponding visual treatment shown

**Description:** AC 03.1 — Decision Table — Existing BO edit feedback states use their corresponding Figma visual treatment.

**Preconditions:**
- Logged in as HQ Staff to Back Office.
- Non-production fixtures can independently reach the existing BO error and completion-feedback UI states.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Reach the existing BO error-feedback state. | The error alert is visible, readable, and does not cover the dialog actions. | Figma frame = 12287:151389 |
| 2 | Reach the existing BO completion-feedback state. | The success alert is visible in the designed success styling. | Figma frame = 12287:149703 |

**Severity:** major
**Priority:** high
