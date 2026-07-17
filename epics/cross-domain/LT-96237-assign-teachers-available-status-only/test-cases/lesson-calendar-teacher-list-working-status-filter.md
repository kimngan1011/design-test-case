# Test Cases: LT-96237 — Assign Teachers with "Available" Status Only

## Suite: Lesson Calendar – Teacher's List – Working Status Filter

### Lesson Calendar – Teacher's List – Working Status Filter – Filter field is displayed

**Description:** BR-06 — Component — Working Status filter field is present in the Teacher's List section of the Lesson Calendar.

**Preconditions:**
- Logged in as HQ or CM Staff to the Back Office
- Lesson Calendar view is accessible

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to the Lesson Calendar | Lesson Calendar is displayed | "" |
| 2 | Open the Teacher's List panel | Teacher's List panel is visible | "" |
| 3 | Observe the filter area in the panel | Working Status filter field is displayed | "" |

**Severity:** major
**Priority:** high

---

### Lesson Calendar – Teacher's List – Working Status Filter – Default selection is "Available" on calendar open

**Description:** BR-06 — EP — The Working Status filter defaults to "Available" when the Lesson Calendar Teacher's List first loads.

**Preconditions:**
- Logged in as HQ or CM Staff to the Back Office
- Lesson Calendar view is accessible

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to the Lesson Calendar | Lesson Calendar is displayed | "" |
| 2 | Open the Teacher's List panel | Teacher's List panel is visible | "" |
| 3 | Observe the current value of the Working Status filter | Working Status filter shows "Available" as the selected default | "" |

**Severity:** major
**Priority:** high

---

### Lesson Calendar – Teacher's List – Working Status Filter – Select "On Leave" – Only On Leave teachers are listed

**Description:** BR-06 — Decision Table — Changing the filter to "On Leave" updates the teacher list to show only On Leave teachers.

**Preconditions:**
- Logged in as HQ or CM Staff to the Back Office
- Lesson Calendar view is accessible
- Teacher A has working status "Available"
- Teacher B has working status "On Leave"

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to Lesson Calendar and open the Teacher's List panel | Teacher's List shows Available teachers by default | "" |
| 2 | Change Working Status filter to "On Leave" | Filter updates to "On Leave" | "Filter = On Leave" |
| 3 | Observe the teacher list | Teacher B (On Leave) is shown; Teacher A (Available) is not shown | "Teacher A = Available, Teacher B = On Leave" |

**Severity:** minor
**Priority:** medium

---
