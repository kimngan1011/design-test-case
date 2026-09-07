# Test Cases: LT-101769 — Improve Lesson popup UI

## Suite: Recurring New Lesson UI

### Lesson Popup – Recurring New – Recurring control – Off state – Recurring controls hidden

**Description:** AC 04.1 — Decision Table — The New Lesson popup does not show recurring configuration when recurring is off.

**Preconditions:**
- Logged in as HQ or CM Staff to Salesforce.
- The New Lesson popup is open.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Set the recurring control to off. | The popup remains in the Figma recurring-off presentation. | Figma frame = 12275:145487 |
| 2 | Review the area below the recurring control. | Recurrence Frequency, Ends, and related recurring controls are not displayed. | State = recurring off |

**Severity:** major
**Priority:** high

---

### Lesson Popup – Japanese Localization – Recurring New screen – Japanese locale – User-facing copy shown in Japanese

**Description:** AC 06.1 — Component — The New Lesson recurring settings present Japanese user-facing copy when the interface locale is Japanese.

**Preconditions:**
- Logged in as HQ or CM Staff to Salesforce with the interface locale set to Japanese.
- The New Lesson popup is open with recurring enabled.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Review the Recurrence Frequency and Ends controls. | Frequency choices, end-option labels, checkboxes, and actions use Japanese text; only approved product names or proper nouns remain unchanged. | Locale = Japanese; Screen = Recurring New |
| 2 | Change the visible recurring selection state without saving. | Any newly displayed user-facing labels remain Japanese, readable, and aligned in the popup. | State = visible recurrence selection |

**Severity:** minor
**Priority:** medium

---

### Lesson Popup – Recurring New – Recurring control – On state – Weekly presented as default

**Description:** AC 04.1 — Decision Table — Enabling recurring reveals the Figma settings with Weekly visibly selected by default.

**Preconditions:**
- Logged in as HQ or CM Staff to Salesforce.
- The New Lesson popup is open with recurring set to off.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Enable the recurring control. | The Recurrence Frequency settings become visible in the designed layout. | Figma frame = 12275:146080 |
| 2 | Review the selected frequency. | Weekly is visibly selected as the default frequency. | Default presentation = Weekly |

**Severity:** major
**Priority:** high

---

### Lesson Popup – Recurring New – Frequency selector – Expanded state – Daily, Weekly, Custom, and Course Schedule options shown

**Description:** AC 04.1 — Component — The recurring frequency UI exposes each Figma-defined choice.

**Preconditions:**
- Logged in as HQ or CM Staff to Salesforce.
- The New Lesson popup is open with recurring enabled.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open the recurrence frequency selector. | The selector opens without obscuring the surrounding popup controls. | State = recurring on |
| 2 | Review the choices. | Daily, Weekly, Custom, and Course Schedule are visible and readable as separate choices. | Expected options = Daily; Weekly; Custom; Course Schedule |

**Severity:** major
**Priority:** high

---

### Lesson Popup – Recurring New – Custom frequency – Custom state – Day and end-option controls shown

**Description:** AC 04.1 — Decision Table — Selecting Custom displays the Figma-dependent day and Ends controls.

**Preconditions:**
- Logged in as HQ or CM Staff to Salesforce.
- The New Lesson popup is open with recurring enabled.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Select Custom from the recurrence frequency selector. | The popup changes to the Figma Custom recurring presentation. | Figma frame = 12275:146753 |
| 2 | Review the dependent recurring controls. | Day-selection and Ends controls are visible, aligned, and distinct from the frequency selector. | State = Custom |
| 3 | Open the Ends control. | The On (End Date) and After (Number of Lessons) choices are visible. | Expected options = On; After |

**Severity:** major
**Priority:** high

---

### Lesson Popup – Recurring New – Course Schedule – Course Schedule state – Skip Closed Date control absent

**Description:** AC 04.1 — Negative — Course Schedule follows the Figma presentation without a Skip Closed Date UI control.

**Preconditions:**
- Logged in as HQ or CM Staff to Salesforce.
- The New Lesson popup is open with recurring enabled.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Select Course Schedule from the recurrence frequency selector. | The popup shows the Course Schedule presentation. | Figma frame = 12451:53196 |
| 2 | Review the recurring controls. | The Skip Closed Date checkbox is absent; the remaining Course Schedule controls retain the designed spacing and alignment. | State = Course Schedule |

**Severity:** major
**Priority:** high
