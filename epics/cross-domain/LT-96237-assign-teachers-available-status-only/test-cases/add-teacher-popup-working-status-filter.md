# Test Cases: LT-96237 — Assign Teachers with "Available" Status Only

## Suite: Add Teacher Popup – Working Status Filter

### Add Teacher Popup – Working Status Filter – Filter field is displayed

**Description:** BR-01 — Component — Working Status multiselect filter field is present in the Add Teacher popup.

**Preconditions:**
- Logged in as HQ or CM Staff to the Back Office
- A lesson exists with a status that allows teacher addition

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open the lesson detail page | Lesson detail page is displayed | "" |
| 2 | Click the **Add Teacher** button | Add Teacher popup opens | "" |
| 3 | Observe the filter area in the popup | Working Status filter field is visible | "" |

**Severity:** major
**Priority:** high

---

### Add Teacher Popup – Working Status Filter – Default selection is "Available" on popup open

**Description:** BR-02 — EP — The Working Status filter defaults to "Available" when the Add Teacher popup first opens.

**Preconditions:**
- Logged in as HQ or CM Staff to the Back Office
- A lesson exists
- The Add Teacher popup has not been opened in the current session (fresh open)

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open the lesson detail page | Lesson detail page is displayed | "" |
| 2 | Click the **Add Teacher** button | Add Teacher popup opens | "" |
| 3 | Observe the current value of the Working Status filter | Working Status filter shows "Available" as the selected default | "" |

**Severity:** major
**Priority:** high

---

### Add Teacher Popup – Working Status Filter – All four options (None, Available, On Leave, Resigned) are listed

**Description:** BR-03 — EP — The Working Status filter dropdown contains exactly four selectable options.

**Preconditions:**
- Logged in as HQ or CM Staff to the Back Office
- A lesson exists

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open the lesson detail page | Lesson detail page is displayed | "" |
| 2 | Click the **Add Teacher** button | Add Teacher popup opens | "" |
| 3 | Click to expand the Working Status filter dropdown | Dropdown opens showing a list of options | "" |
| 4 | Read all available options in the dropdown | Dropdown shows exactly: None, Available, On Leave, Resigned | "Options: None, Available, On Leave, Resigned" |

**Severity:** major
**Priority:** high

---

### Add Teacher Popup – Working Status Filter – Select "Available" – Only teachers with Available status are listed

**Description:** BR-04 — Decision Table — Selecting "Available" filters the teacher list to show only teachers whose working status is Available.

**Preconditions:**
- Logged in as HQ or CM Staff to the Back Office
- A lesson exists
- Teacher A has working status "Available"
- Teacher B has working status "On Leave"
- Teacher C has working status "Resigned"

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open the lesson detail page and click **Add Teacher** | Add Teacher popup opens | "" |
| 2 | Set Working Status filter to "Available" | Filter is set to "Available" | "Filter = Available" |
| 3 | Observe the teacher list | Teacher A is shown; Teacher B and Teacher C are not shown | "Teacher A = Available, Teacher B = On Leave, Teacher C = Resigned" |

**Severity:** major
**Priority:** high

---

### Add Teacher Popup – Working Status Filter – Select "Available" and "On Leave" – Teachers from both statuses are listed

**Description:** BR-04 — Decision Table — Selecting multiple statuses in the multiselect filter shows teachers from all selected status groups.

**Preconditions:**
- Logged in as HQ or CM Staff to the Back Office
- A lesson exists
- Teacher A has working status "Available"
- Teacher B has working status "On Leave"
- Teacher C has working status "Resigned"

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open the lesson detail page and click **Add Teacher** | Add Teacher popup opens | "" |
| 2 | Select both "Available" and "On Leave" in the Working Status filter (multiselect) | Both "Available" and "On Leave" are selected | "Filter = Available + On Leave" |
| 3 | Observe the teacher list | Teacher A (Available) and Teacher B (On Leave) are both shown; Teacher C (Resigned) is not shown | "Teacher A = Available, Teacher B = On Leave, Teacher C = Resigned" |

**Severity:** minor
**Priority:** medium

---

### Add Teacher Popup – "Only teachers free at this time" – Label is updated from "Only available teachers"

**Description:** BR-05 — Component — The toggle/checkbox label reads "Only teachers free at this time" and the old label "Only available teachers" does not appear.

**Preconditions:**
- Logged in as HQ or CM Staff to the Back Office
- A lesson exists

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open the lesson detail page and click **Add Teacher** | Add Teacher popup opens | "" |
| 2 | Locate the free-time filter toggle/checkbox label | Label reads "Only teachers free at this time" | "" |
| 3 | Confirm the old label is absent | The text "Only available teachers" does not appear anywhere in the popup | "" |

**Severity:** major
**Priority:** high

---
