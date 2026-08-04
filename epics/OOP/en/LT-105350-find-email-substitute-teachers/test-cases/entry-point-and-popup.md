# Test Cases: LT-105350 — [EN] Finding and Emailing Substitute Teacher Candidates

## Suite: Entry Point & Popup

### [EN] Substitute Teacher – Entry Point – "Add Teacher" button on Lesson Detail – No separate substitute menu exists

**Description:** AC 01.2 — Component — "Add Teacher" button is the sole entry point for substitute teacher search; no separate "Find Substitute Teachers" menu item is present on Lesson Detail.

**Preconditions:**
- Logged in as HQ or CM Staff to the EN Salesforce org
- EN organization feature is enabled
- A lesson exists on the Lesson Calendar with at least one vacant teacher slot

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open the Lesson Calendar in Salesforce | Lesson Calendar page is displayed | "" |
| 2 | Click on the target lesson card to open Lesson Detail | Lesson Detail page opens | "" |
| 3 | Locate the Lesson Teacher section on Lesson Detail | The Lesson Teacher section is visible | "" |
| 4 | Observe all buttons and menu options within the Lesson Teacher section | An **Add Teacher** button is visible; no separate "Find Substitute Teachers" button or menu item exists | "" |

**Severity:** minor
**Priority:** medium

---

### [EN] Substitute Teacher – Entry Point – Click "Add Teacher" button – Teacher list popup opens

**Description:** AC 01.2 — Component — Clicking the "Add Teacher" button on Lesson Detail opens the enhanced Teacher list popup.

**Preconditions:**
- Logged in as HQ or CM Staff to the EN Salesforce org
- EN organization feature is enabled
- A lesson is open on Lesson Detail page

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open the target lesson on Lesson Detail | Lesson Detail page is displayed | "" |
| 2 | Click the **Add Teacher** button in the Lesson Teacher section | Add Teacher popup opens; popup is fully loaded | "" |
| 3 | Observe the popup is interactive | Filter controls and teacher list are responsive | "" |

**Severity:** major
**Priority:** high

---

### [EN] Substitute Teacher – Add Teacher Popup – Initial display – All filter components visible

**Description:** AC 01.2, AC 02.1 — Component — On fresh open, the Add Teacher popup displays all required components: Location Selector, Available Teacher Checkbox / "Only teachers free at this time" toggle, Flagged Teacher Checkbox, real-time match count, teacher list with Flagged column, and Send Email button.

**Preconditions:**
- Logged in as HQ or CM Staff to the EN Salesforce org
- EN organization feature is enabled
- A lesson is open on Lesson Detail; Add Teacher popup not yet opened in this session

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open the target lesson on Lesson Detail | Lesson Detail page is displayed | "" |
| 2 | Click the **Add Teacher** button | Add Teacher popup opens | "" |
| 3 | Observe the filter area at the top of the popup | Location Selector, Available Teacher Checkbox / "Only teachers free at this time" toggle, and Flagged Teacher Checkbox are all visible | "" |
| 4 | Observe the teacher results area | A list of teachers is displayed; a column labelled **Flagged** (要注意講師) is visible in the header row | "" |
| 5 | Observe the match count indicator | A count of currently matching teachers is displayed and reflects the current (unfiltered) list | "" |
| 6 | Observe the bottom action bar of the popup | A **Send Email** (メールを送信する) button is visible | "" |

**Severity:** major
**Priority:** high

---
