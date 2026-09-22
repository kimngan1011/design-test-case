# Test Cases: LT-107411 — Filter Accordion

## Suite: [Riso] TAC — Filter Accordion

### [Riso] TAC – Filter Accordion – Collapsed state – Location filter hidden
**Description:** AC 04 — State Transition — Location is hidden with the other filters.
**Preconditions:**
- HQ or CM Staff is logged in to the Riso Salesforce org.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff collapses the filter accordion. | The Location filter is hidden with the other filters. | accordion = collapsed |
**Severity:** minor
**Priority:** medium

### [Riso] TAC – Filter Accordion – Expanded state – Location filter restored
**Description:** AC 04 — State Transition — Location is available after expansion.
**Preconditions:**
- HQ or CM Staff is logged in to the Riso Salesforce org.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff expands the filter accordion. | The Location filter is visible and available. | accordion = expanded |
**Severity:** minor
**Priority:** medium

### [Riso] TAC – Filter Accordion – Selected Location – Filtering retained
**Description:** AC 04 — Regression — Accordion state change preserves the selected Location filter.
**Preconditions:**
- HQ or CM Staff is logged in to the Riso Salesforce org.
- Location `Tokyo` has calendar lessons.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff selects Location `Tokyo`. | The calendar shows lessons in `Tokyo`. | location = Tokyo |
| 2 | HQ or CM Staff collapses and expands the filter accordion. | `Tokyo` remains selected and the same location-filtered lessons remain shown. | location = Tokyo |
**Severity:** major
**Priority:** high
