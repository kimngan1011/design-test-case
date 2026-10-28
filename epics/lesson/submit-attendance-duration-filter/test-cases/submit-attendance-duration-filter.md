# Test Cases: Submit Attendance — Duration Filter

## Suite: Submit Attendance Page and View Notification Center

### Submit Attendance – Duration Filter – Lessons within inclusive dates – Only eligible lessons listed

**Description:** AC Duration-01 — Equivalence Partitioning — The lesson list contains every lesson whose JST lesson date falls inside the selected inclusive Duration and excludes lessons outside it.

**Preconditions:**
- A Parent or Student is logged in to the Learner App for Student A.
- Student A can submit attendance for lessons L1 through L6.
- L1 starts on 2026-10-08 09:00 JST.
- L2 starts on 2026-10-09 06:00 JST.
- L3 starts on 2026-10-09 09:00 JST.
- L4 starts on 2026-10-12 09:00 JST.
- L5 starts on 2026-10-16 18:00 JST.
- L6 starts on 2026-10-17 09:00 JST.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Parent or Student opens Submit Attendance and sets the Duration Start Date to 2026/10/09 and End Date to 2026/10/16. | The Lessons tab shows 4 lessons. | start_date = 2026-10-09 JST; end_date = 2026-10-16 JST; L1 = 2026-10-08; L2 = 2026-10-09; L3 = 2026-10-09; L4 = 2026-10-12; L5 = 2026-10-16; L6 = 2026-10-17 |
| 2 | Parent or Student reviews every lesson displayed on the Lessons tab. | L2, L3, L4, and L5 are displayed with their configured lesson dates and times. L1 and L6 are not displayed. | eligible_dates = 2026-10-09 through 2026-10-16 inclusive |

**Severity:** major
**Priority:** high

---

### Submit Attendance – Duration Filter – Lessons tab count – Count matches selectable lessons

**Description:** AC Duration-02 — Decision Table — The count beside the Lessons tab equals the number of lessons available for selection after applying Duration.

**Preconditions:**
- A Parent or Student is logged in to the Learner App for Student A.
- Student A has five attendance-eligible lessons within the selected Duration: L1 on 2026-10-09 06:00 JST, L2 on 2026-10-09 09:00 JST, L3 on 2026-10-12 09:00 JST, L4 on 2026-10-14 09:00 JST, and L5 on 2026-10-16 18:00 JST.
- Student A has no other attendance-eligible lesson from 2026-10-09 through 2026-10-16 JST.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Parent or Student opens Submit Attendance and sets the Duration Start Date to 2026/10/09 and End Date to 2026/10/16. | The Lessons tab label shows `Lessons (5)`. | start_date = 2026-10-09 JST; end_date = 2026-10-16 JST; eligible_lesson_count = 5 |
| 2 | Parent or Student selects All Lessons and reviews the selected lesson cards. | Exactly five lesson cards are selected: L1, L2, L3, L4, and L5. | selected_lesson_count = 5 |

**Severity:** major
**Priority:** high

---

### Submit Attendance – Duration Filter – All filtered lessons selected – Submit summary preserves count and date range

**Description:** AC Duration-03 — Scenario — The selected-lesson total and Duration shown before Next are identical to the summary on the Submit Attendance screen.

**Preconditions:**
- A Parent or Student is logged in to the Learner App for Student A.
- Student A has five attendance-eligible lessons within 2026-10-09 through 2026-10-16 JST.
- Student A has no other attendance-eligible lesson within that Duration.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Parent or Student opens Submit Attendance and sets the Duration Start Date to 2026/10/09 and End Date to 2026/10/16. | The Lessons tab label shows `Lessons (5)`. | start_date = 2026-10-09 JST; end_date = 2026-10-16 JST; eligible_lesson_count = 5 |
| 2 | Parent or Student selects All Lessons. | Five lessons are selected and the selected set contains all lessons returned by the Duration filter. | selected_lesson_count = 5 |
| 3 | Parent or Student taps Next. | The Submit Attendance screen shows `Lessons Selected: 5` and `2026/10/09 - 2026/10/16`. | filter_count = 5; filter_range = 2026/10/09 - 2026/10/16; summary_count = 5; summary_range = 2026/10/09 - 2026/10/16 |

**Severity:** major
**Priority:** high

---

### Submit Attendance – Duration Filter – JST-to-UTC date boundary – Filter and summary retain the JST date and count

**Description:** AC Duration-04 — Boundary — Lessons at the JST-to-UTC calendar boundary are filtered by their JST date, and the Submit Attendance summary matches the filter.

**Preconditions:**
- A Parent or Student is logged in to the Learner App for Student A using the Japan time zone.
- Student A can submit attendance for L1 and L2.
- L1 starts at 2026-10-09 00:30 JST and is stored as 2026-10-08 15:30 UTC.
- L2 starts at 2026-10-09 23:30 JST and is stored as 2026-10-09 14:30 UTC.
- Student A has no other attendance-eligible lesson on 2026-10-09 JST.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Parent or Student opens Submit Attendance and sets both Duration dates to 2026/10/09. | The Lessons tab label shows `Lessons (2)` and displays L1 and L2. | start_date = end_date = 2026-10-09 JST; L1 = 2026-10-09 00:30 JST (= 2026-10-08 15:30 UTC); L2 = 2026-10-09 23:30 JST (= 2026-10-09 14:30 UTC) |
| 2 | Parent or Student selects All Lessons and taps Next. | The Submit Attendance screen shows `Lessons Selected: 2` and `2026/10/09`; neither lesson is shifted to 2026/10/08 or 2026/10/10. | filter_count = 2; filter_range = 2026/10/09; summary_count = 2; summary_range = 2026/10/09 |

**Severity:** major
**Priority:** high
