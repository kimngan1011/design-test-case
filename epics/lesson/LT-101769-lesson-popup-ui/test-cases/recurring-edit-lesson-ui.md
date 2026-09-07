# Test Cases: LT-101769 — Improve Lesson popup UI

## Suite: Recurring Edit Lesson UI

### Lesson Popup – Recurring Edit – Recurring Settings section – Default state – Hierarchy and labels shown

**Description:** AC 05.1 — Component — The Edit Lesson recurring section follows the Figma hierarchy and confirmed wording.

**Preconditions:**
- Logged in as HQ or CM Staff to Salesforce.
- The Edit Lesson popup is open for an existing lesson.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to the recurring settings area of the Edit Lesson popup. | The Recurring Settings section is visible in the designed hierarchy. | Figma section = 12463:54991 |
| 2 | Review the labels and controls. | Labels are readable, aligned, and do not overlap nearby popup controls. | Viewport = desktop design |

**Severity:** minor
**Priority:** medium

---

### Lesson Popup – Japanese Localization – Recurring Edit screen – Japanese locale – User-facing copy shown in Japanese

**Description:** AC 06.1 — Component — The Edit Lesson recurring settings present Japanese user-facing copy when the interface locale is Japanese.

**Preconditions:**
- Logged in as HQ or CM Staff to Salesforce with the interface locale set to Japanese.
- The Edit Lesson popup is open and the Recurring Settings section is visible.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Review the Recurring Settings labels and choices. | The section title, One Time, Weekly Recurring, and related actions use Japanese text; only approved product names or proper nouns remain unchanged. | Locale = Japanese; Screen = Recurring Edit |
| 2 | Review the selected and unselected option appearance. | Japanese labels remain readable and aligned for both selected and unselected choices. | State = either recurring option selected |

**Severity:** minor
**Priority:** medium

---

### Lesson Popup – Recurring Edit – Saving option – One Time state – Selected appearance shown

**Description:** AC 05.1 — Decision Table — The One Time recurring-setting choice uses the designed selected presentation.

**Preconditions:**
- Logged in as HQ or CM Staff to Salesforce.
- The Edit Lesson popup is open with the One Time setting selected.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Review the Recurring Settings choices. | One Time and Weekly Recurring are visible. | Confirmed labels = One Time; Weekly Recurring |
| 2 | Review the One Time choice. | One Time is visually selected and Weekly Recurring is visibly unselected. | State = One Time |

**Severity:** minor
**Priority:** medium

---

### Lesson Popup – Recurring Edit – Saving option – Weekly Recurring state – Selected appearance shown

**Description:** AC 05.1 — Decision Table — The Weekly Recurring choice uses the designed selected presentation.

**Preconditions:**
- Logged in as HQ or CM Staff to Salesforce.
- The Edit Lesson popup is open with the Weekly Recurring setting selected.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Review the Recurring Settings choices. | One Time and Weekly Recurring are visible. | Confirmed labels = One Time; Weekly Recurring |
| 2 | Review the Weekly Recurring choice. | Weekly Recurring is visually selected and One Time is visibly unselected. | State = Weekly Recurring |

**Severity:** minor
**Priority:** medium
