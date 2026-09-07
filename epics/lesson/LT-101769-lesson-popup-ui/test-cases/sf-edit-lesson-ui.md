# Test Cases: LT-101769 — Improve Lesson popup UI

## Suite: SF Edit Lesson UI

### Lesson Popup – SF Edit – Edit affordance – Hover state – Edit entry point shown

**Description:** AC 02.1 — Regression — Staff can discover the Figma edit affordance for an existing lesson.

**Preconditions:**
- Logged in as HQ or CM Staff to Salesforce.
- An existing editable lesson is available in Lesson Management.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open the existing lesson and hover the designed edit area. | The Edit affordance is visible and follows the Figma hover presentation. | Figma frame = 12151:77367 |
| 2 | Select the Edit affordance. | The Edit Lesson popup opens over the existing Lesson page. | Lesson = editable fixture |

**Severity:** minor
**Priority:** medium

---

### Lesson Popup – SF Edit – Edit Lesson modal – Default state – Designed hierarchy and actions shown

**Description:** AC 02.1 — Component — The SF Edit Lesson popup preserves the designed header, content, close control, and footer actions.

**Preconditions:**
- Logged in as HQ or CM Staff to Salesforce.
- The Edit Lesson popup is open for an existing editable lesson.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Review the Edit Lesson popup from header to footer. | The title is “Edit Lesson” and the close control, content area, and footer actions are present in the designed hierarchy. | Figma frame = 12151:77788 |
| 2 | Review the populated form layout. | Existing values and controls are aligned without overlap, clipping, or an unintended page scroll. | State = default |

**Severity:** minor
**Priority:** medium

---

### Lesson Popup – SF Edit – Validation feedback – Error state – Designed warning shown

**Description:** AC 02.1 — Negative — The existing SF edit error state displays the Figma warning treatment.

**Preconditions:**
- Logged in as HQ or CM Staff to Salesforce.
- An existing edit fixture can trigger the designed warning state without changing production data.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Trigger the existing edit warning state. | The Edit Lesson popup remains visible with the designed warning feedback. | Figma frame = 12152:79733 |
| 2 | Read the warning copy. | The warning states “We hit a snag” and “There are more lessons than all classrooms for the selected date and timeslot.” | Expected copy = Figma warning |

**Severity:** major
**Priority:** high

---

### Lesson Popup – Japanese Localization – SF Edit screen – Japanese locale – User-facing copy shown in Japanese

**Description:** AC 06.1 — Component — The SF Edit screen presents Japanese user-facing copy when the interface locale is Japanese.

**Preconditions:**
- Logged in as HQ or CM Staff to Salesforce with the interface locale set to Japanese.
- The Edit Lesson popup is open for an existing lesson.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Review the Edit Lesson popup from header to footer. | The title, populated-field labels, actions, and close control context use Japanese text; only approved product names or proper nouns remain unchanged. | Locale = Japanese; Screen = SF Edit |
| 2 | Review any visible feedback or helper text. | User-facing feedback and helper text use Japanese and remain readable without truncation or overlap. | State = available UI feedback |

**Severity:** minor
**Priority:** medium

---

### Lesson Popup – SF Edit – Success feedback – Completion state – Designed toast and copy shown

**Description:** AC 02.1 — Decision Table — The existing SF edit completion state presents the Figma success toast.

**Preconditions:**
- Logged in as HQ or CM Staff to Salesforce.
- A non-production edit fixture can reach the existing completion-feedback UI state.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Use the fixture to reach the existing completion-feedback state. | A success toast appears in the designed position and styling. | Figma frame = 12151:71201 |
| 2 | Read the toast description. | The toast description is “You have edited lesson successfully.” and its close control is visible. | Expected message = You have edited lesson successfully. |

**Severity:** major
**Priority:** high

---

### Lesson Popup – SF Edit – Lesson flow – Edit action – Edit form opens

**Description:** AC 02.1 — Regression — The Lesson flow opens the designed SF Edit form.

**Preconditions:**
- Logged in as HQ or CM Staff to Salesforce.
- An editable lesson is open from the Lesson flow.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Select Edit from the Lesson flow. | The Edit Lesson popup opens over the Lesson screen. | Entry point = Lesson; Lesson = editable fixture |
| 2 | Review the opened popup. | The Edit Lesson title, content area, close control, and footer actions match the designed SF Edit UI. | Figma node = 12151:70357 |

**Severity:** minor
**Priority:** medium

---

### Lesson Popup – SF Edit – Calendar flow – Edit action – Edit form opens

**Description:** AC 02.1 — Regression — The Calendar flow opens the designed SF Edit form.

**Preconditions:**
- Logged in as HQ or CM Staff to Salesforce.
- An editable lesson is visible on the Lesson Calendar.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Select Edit for the lesson from the Calendar flow. | The Edit Lesson popup opens over the Calendar screen. | Entry point = Calendar; Lesson = editable fixture |
| 2 | Review the opened popup. | The Edit Lesson title, content area, close control, and footer actions match the designed SF Edit UI. | Figma node = 12151:70357 |

**Severity:** minor
**Priority:** medium
