# Test Cases: LT-98531 — [Riso] Monthly Lesson Assignment Report – Calculations

## Suite: Report Columns – Structure and Sort

### [Riso] Monthly Lesson Assignment Report – Report Columns – All 7 Columns Present Simultaneously

**Description:** AC-08 — Component (Deep) — All seven required columns (Location, Student Name, Course, Student Course Duration Per Month, Purchased Slot, Lesson Allocated, Diff) are present simultaneously in the report.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org
- At least one student-course combination exists with a contract and sessions for the selected month
- today = 2026-06-22; current_AY = 2025-2026; target_month = 2026-06

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to the Monthly Lesson Assignment report page | Report page loads | today = 2026-06-22; current_AY = 2025-2026; target_month = 2026-06 |
| 2 | Select AY 2025-2026 and month June 2026 in the filters, then apply | Report renders at least one data row | target_month = 2026-06; AY = 2025-2026 |
| 3 | Observe the column headers of the report table | The following seven columns are all visible: **Location**, **Student Name**, **Course**, **Student Course Duration Per Month**, **Purchased Slot**, **Lesson Allocated**, **Diff** | Expected columns: Location, Student Name, Course, Student Course Duration Per Month, Purchased Slot, Lesson Allocated, Diff |
| 4 | Observe the data row for the test student-course combination | Each column cell contains a value or an appropriate placeholder (not blank due to a crash) | "" |

**Severity:** major
**Priority:** high

---

### [Riso] Monthly Lesson Assignment Report – Row Sort Order – Location ASC then Student Name ASC then Course ASC then Start Date ASC

**Description:** AC-08 — Scenario — Report rows are ordered by Location ASC, then Student Name ASC, then Course ASC, then Start Date ASC.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org
- Three student-course rows exist for the selected month with different Location and Student Name values (see test data)
- today = 2026-06-22; current_AY = 2025-2026; target_month = 2026-06

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to the Monthly Lesson Assignment report page, select AY 2025-2026 and month June 2026, then apply | Report renders three rows | today = 2026-06-22; Rows: (A) Location=Tokyo, Student=Tanaka, Course=English, Start=2025-04-01; (B) Location=Osaka, Student=Ito, Course=Math, Start=2025-05-01; (C) Location=Tokyo, Student=Sato, Course=English, Start=2025-04-01 |
| 2 | Observe the row order in the report | Rows appear from top to bottom: (1) Osaka–Ito–Math, (2) Tokyo–Sato–English, (3) Tokyo–Tanaka–English | Expected: Osaka < Tokyo (Location ASC); within Tokyo: Sato < Tanaka (Student Name ASC) |

**Severity:** minor
**Priority:** medium

---

### [Riso] Monthly Lesson Assignment Report – Row With Null or Missing Values – Renders Without Error

**Description:** AC-08 — Negative — A student-course row with missing or null optional field values renders without breaking or crashing the report.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org
- A student-course combination exists in the report month where one or more optional fields (e.g., Student Course Duration Per Month) are null or unpopulated
- today = 2026-06-22; current_AY = 2025-2026; target_month = 2026-06

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to the Monthly Lesson Assignment report page and apply filters for AY 2025-2026 and June 2026 | Report loads and renders all rows including the row with missing data | today = 2026-06-22; Student with null Student Course Duration Per Month field |
| 2 | Locate the row for the student with missing field values | The row renders; the cell with missing data shows an empty value or dash — the report does not crash or throw an error | "" |
| 3 | Confirm other rows in the report are unaffected | All other rows display their data correctly | "" |

**Severity:** minor
**Priority:** medium

---

## Suite: Purchased Slot – Contract Type Calculation

### [Riso] Monthly Lesson Assignment Report – Purchased Slot – Monthly Contract Uses Contract.slot

**Description:** AC-09 — Decision Table — For a Monthly contract, the Purchased Slot column displays the value from Contract.slot.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org
- A student has a Monthly contract with Contract.slot = 8 for AY 2025-2026
- today = 2026-06-22; current_AY = 2025-2026; target_month = 2026-06

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to the Monthly Lesson Assignment report page, set filters to AY 2025-2026 and June 2026, then apply | Report loads | today = 2026-06-22; Contract type = Monthly; Contract.slot = 8 |
| 2 | Locate the row for the student with the Monthly contract | The **Purchased Slot** column shows **8** | Expected Purchased Slot = 8 (from Contract.slot) |

**Severity:** major
**Priority:** high

---

### [Riso] Monthly Lesson Assignment Report – Purchased Slot – Weekly Contract Uses Contract.slot

**Description:** AC-09 — Decision Table — For a Weekly contract, the Purchased Slot column displays the value from Contract.slot.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org
- A student has a Weekly contract with Contract.slot = 4 for AY 2025-2026
- today = 2026-06-22; current_AY = 2025-2026; target_month = 2026-06

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to the Monthly Lesson Assignment report page, set filters to AY 2025-2026 and June 2026, then apply | Report loads | today = 2026-06-22; Contract type = Weekly; Contract.slot = 4 |
| 2 | Locate the row for the student with the Weekly contract | The **Purchased Slot** column shows **4** | Expected Purchased Slot = 4 (from Contract.slot) |

**Severity:** major
**Priority:** high

---

### [Riso] Monthly Lesson Assignment Report – Purchased Slot – One Time Contract Uses Contract.total

**Description:** AC-09 — Decision Table — For a One Time contract, the Purchased Slot column displays the value from Contract.total (not Contract.slot).

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org
- A student has a One Time contract with Contract.total = 10 and Contract.slot = 2 for AY 2025-2026
- today = 2026-06-22; current_AY = 2025-2026; target_month = 2026-06

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to the Monthly Lesson Assignment report page, set filters to AY 2025-2026 and June 2026, then apply | Report loads | today = 2026-06-22; Contract type = One Time; Contract.total = 10; Contract.slot = 2 |
| 2 | Locate the row for the student with the One Time contract | The **Purchased Slot** column shows **10** (Contract.total), not 2 (Contract.slot) | Expected Purchased Slot = 10 (from Contract.total); must NOT show 2 |

**Severity:** major
**Priority:** high

---

### [Riso] Monthly Lesson Assignment Report – Purchased Slot – All Three Contract Types Show Correct Values in One Report View

**Description:** AC-09 — Pairwise (Deep) — Monthly, Weekly, and One Time contracts each display the correct Purchased Slot value simultaneously in the same report view.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org
- Three students exist, each with a different contract type for AY 2025-2026: Student A has Monthly (slot=8), Student B has Weekly (slot=4), Student C has One Time (total=10, slot=2)
- today = 2026-06-22; current_AY = 2025-2026; target_month = 2026-06

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to the Monthly Lesson Assignment report page, set AY 2025-2026 and June 2026, select Students A, B, C, then apply | Report loads showing three rows | today = 2026-06-22; Student A: Monthly, slot=8; Student B: Weekly, slot=4; Student C: One Time, total=10, slot=2 |
| 2 | Locate the row for Student A (Monthly contract) | **Purchased Slot** = 8 | Monthly: Contract.slot = 8 |
| 3 | Locate the row for Student B (Weekly contract) | **Purchased Slot** = 4 | Weekly: Contract.slot = 4 |
| 4 | Locate the row for Student C (One Time contract) | **Purchased Slot** = 10 (not 2) | One Time: Contract.total = 10; Contract.slot = 2 |

**Severity:** major
**Priority:** high

---

## Suite: Lesson Allocated – Attendance Calculation

### [Riso] Monthly Lesson Assignment Report – Lesson Allocated – Absent + In Advance Notice – Session Included in Count

**Description:** AC-10 — Decision Table (Critical, Deep) — A session where Attendance = Absent AND Notice = "In Advance" is INCLUDED in the Lesson Allocated count (advance-notice absent is treated as consumed).

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org
- Student A has exactly one session in June 2026 with Attendance = Absent and Notice = "In Advance"
- Student A has no other sessions in June 2026
- Contract for Student A: Monthly, slot = 8
- today = 2026-06-22; current_AY = 2025-2026; target_month = 2026-06

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to the Monthly Lesson Assignment report page, set AY 2025-2026 and June 2026, select Student A, then apply | Report loads showing Student A's row | today = 2026-06-22; Student A session: Attendance = Absent; Notice = In Advance; target_month = 2026-06 |
| 2 | Locate Student A's row in the report | The **Lesson Allocated** column shows **1** (the Absent+InAdvance session is counted) | Expected Lesson Allocated = 1; session is INCLUDED because Notice = In Advance |
| 3 | Observe the **Diff** column for Student A | Diff = 8 − 1 = **7** | Purchased Slot = 8; Lesson Allocated = 1; Diff = 7 |

**Severity:** critical
**Priority:** high

---

### [Riso] Monthly Lesson Assignment Report – Lesson Allocated – Absent + No In Advance Notice – Session Excluded from Count

**Description:** AC-10 — Decision Table (Critical, Deep) — A session where Attendance = Absent AND Notice is NOT "In Advance" (e.g., "Same Day" or blank) is EXCLUDED from the Lesson Allocated count.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org
- Student B has exactly one session in June 2026 with Attendance = Absent and Notice = "Same Day" (not In Advance)
- Student B has no other sessions in June 2026
- Contract for Student B: Monthly, slot = 8
- today = 2026-06-22; current_AY = 2025-2026; target_month = 2026-06

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to the Monthly Lesson Assignment report page, set AY 2025-2026 and June 2026, select Student B, then apply | Report loads showing Student B's row | today = 2026-06-22; Student B session: Attendance = Absent; Notice = Same Day; target_month = 2026-06 |
| 2 | Locate Student B's row in the report | The **Lesson Allocated** column shows **0** (the Absent+SameDay session is excluded) | Expected Lesson Allocated = 0; session is EXCLUDED because Attendance = Absent AND Notice != In Advance |
| 3 | Observe the **Diff** column for Student B | Diff = 8 − 0 = **8** | Purchased Slot = 8; Lesson Allocated = 0; Diff = 8 |

**Severity:** critical
**Priority:** high

---

### [Riso] Monthly Lesson Assignment Report – Lesson Allocated – Present Attendance – Session Included in Count

**Description:** AC-10 — Decision Table (Critical, Deep) — A session where Attendance = Present is INCLUDED in the Lesson Allocated count regardless of Notice value.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org
- Student C has exactly one session in June 2026 with Attendance = Present
- Student C has no other sessions in June 2026
- Contract for Student C: Monthly, slot = 8
- today = 2026-06-22; current_AY = 2025-2026; target_month = 2026-06

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to the Monthly Lesson Assignment report page, set AY 2025-2026 and June 2026, select Student C, then apply | Report loads showing Student C's row | today = 2026-06-22; Student C session: Attendance = Present; target_month = 2026-06 |
| 2 | Locate Student C's row in the report | The **Lesson Allocated** column shows **1** (the Present session is counted) | Expected Lesson Allocated = 1; Present attendance is always INCLUDED |
| 3 | Observe the **Diff** column for Student C | Diff = 8 − 1 = **7** | Purchased Slot = 8; Lesson Allocated = 1; Diff = 7 |

**Severity:** critical
**Priority:** high

---

### [Riso] Monthly Lesson Assignment Report – Lesson Allocated – All Three Attendance Branches Verified in Same Report Context

**Description:** AC-10 — Decision Table (Critical, Deep) — All three attendance combinations are validated simultaneously in one controlled report view: (1) Absent+InAdvance → INCLUDED, (2) Absent+SameDay → EXCLUDED, (3) Present → INCLUDED.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org
- Three students exist, each with exactly one session in June 2026 covering one attendance branch:
  - Student A: Attendance = Absent, Notice = In Advance (should be included)
  - Student B: Attendance = Absent, Notice = Same Day (should be excluded)
  - Student C: Attendance = Present (should be included)
- All three contracts: Monthly, slot = 8
- today = 2026-06-22; current_AY = 2025-2026; target_month = 2026-06

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to the Monthly Lesson Assignment report page, set AY 2025-2026 and June 2026, select Students A, B, C, then apply | Report loads showing three rows | today = 2026-06-22; Student A: Absent+InAdvance; Student B: Absent+SameDay; Student C: Present; all contracts Monthly slot=8; target_month = 2026-06 |
| 2 | Locate Student A's row (Absent + In Advance) | **Lesson Allocated** = 1; **Diff** = 7 | Student A: Absent + Notice=In Advance → INCLUDED; Purchased Slot=8; Lesson Allocated=1; Diff=7 |
| 3 | Locate Student B's row (Absent + Same Day) | **Lesson Allocated** = 0; **Diff** = 8 | Student B: Absent + Notice=Same Day → EXCLUDED; Purchased Slot=8; Lesson Allocated=0; Diff=8 |
| 4 | Locate Student C's row (Present) | **Lesson Allocated** = 1; **Diff** = 7 | Student C: Present → INCLUDED; Purchased Slot=8; Lesson Allocated=1; Diff=7 |

**Severity:** critical
**Priority:** high

---

### [Riso] Monthly Lesson Assignment Report – Lesson Allocated – Cancelled Lesson Not Excluded from Count

**Description:** AC-10 — Negative — A Cancelled lesson has no attendance record and is NOT excluded from the Lesson Allocated count. The SF report does not filter by lesson status; only the attendance exclusion rule applies. Because Cancelled lessons have no Attendance value, they do not meet the exclusion condition (`Attendance = Absent AND Notice ≠ In Advance`) and are therefore counted.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org
- Student D has exactly two sessions in June 2026:
  - Session 1: lesson status = Published/Completed, Attendance = Present → counted by attendance rule
  - Session 2: lesson status = Cancelled, Attendance = (no record / null) → not excluded because null attendance does not satisfy the exclusion condition
- Contract for Student D: Monthly, slot = 8
- today = 2026-06-22; current_AY = 2025-2026; target_month = 2026-06

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to the Monthly Lesson Assignment report page, set AY 2025-2026 and June 2026, select Student D, then apply | Report loads showing Student D's row | today = 2026-06-22; Student D: Session 1 (Published, Attendance=Present); Session 2 (Cancelled, no attendance record); Contract Monthly slot=8; target_month = 2026-06 |
| 2 | Locate Student D's row in the report and observe the Lesson Allocated column | **Lesson Allocated = 2** (both sessions are counted; the Cancelled session is NOT excluded because the system does not filter by lesson status, and null attendance does not satisfy the exclusion condition) | Expected Lesson Allocated = 2; Session 1: Present → INCLUDED; Session 2: Cancelled with no attendance → INCLUDED (exclusion rule `Attendance=Absent AND Notice≠InAdvance` does not apply to null attendance) |
| 3 | Observe the **Diff** column for Student D | Diff = 8 − 2 = **6** | Purchased Slot = 8; Lesson Allocated = 2; Diff = 6 |

**Severity:** major
**Priority:** high

---

## Suite: Diff Formula

### [Riso] Monthly Lesson Assignment Report – Diff – Positive Value When Purchased Slot Greater Than Lesson Allocated

**Description:** AC-11 — Boundary Value Analysis — Diff displays as a positive number when Purchased Slot > Lesson Allocated.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org
- A student has a Monthly contract with slot = 8; the student attended 5 sessions in the target month (all Present)
- today = 2026-06-22; current_AY = 2025-2026; target_month = 2026-06

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to the Monthly Lesson Assignment report page, set AY 2025-2026 and June 2026, select the student, then apply | Report loads showing the student's row | today = 2026-06-22; Purchased Slot = 8; Lesson Allocated = 5; target_month = 2026-06 |
| 2 | Locate the student's row and observe the **Diff** column | **Diff** = **3** (positive value; displayed without a minus sign) | Purchased Slot = 8; Lesson Allocated = 5; Diff = 8 − 5 = 3 |

**Severity:** minor
**Priority:** medium

---

### [Riso] Monthly Lesson Assignment Report – Diff – Zero Value When Purchased Slot Equals Lesson Allocated

**Description:** AC-11 — Boundary Value Analysis — Diff displays as zero when Purchased Slot = Lesson Allocated.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org
- A student has a Monthly contract with slot = 6; the student attended exactly 6 sessions in the target month (all Present)
- today = 2026-06-22; current_AY = 2025-2026; target_month = 2026-06

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to the Monthly Lesson Assignment report page, set AY 2025-2026 and June 2026, select the student, then apply | Report loads showing the student's row | today = 2026-06-22; Purchased Slot = 6; Lesson Allocated = 6; target_month = 2026-06 |
| 2 | Locate the student's row and observe the **Diff** column | **Diff** = **0** (zero displayed, not blank) | Purchased Slot = 6; Lesson Allocated = 6; Diff = 6 − 6 = 0 |

**Severity:** minor
**Priority:** medium

---

### [Riso] Monthly Lesson Assignment Report – Diff – Negative Value When Purchased Slot Less Than Lesson Allocated

**Description:** AC-11 — Boundary Value Analysis — Diff displays as a negative number (with minus sign) when Purchased Slot < Lesson Allocated; no absolute value substitution occurs.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org
- A student has a Monthly contract with slot = 4; the student has 6 sessions counted in the target month (e.g., some sessions attended on extra days)
- today = 2026-06-22; current_AY = 2025-2026; target_month = 2026-06

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to the Monthly Lesson Assignment report page, set AY 2025-2026 and June 2026, select the student, then apply | Report loads showing the student's row | today = 2026-06-22; Purchased Slot = 4; Lesson Allocated = 6; target_month = 2026-06 |
| 2 | Locate the student's row and observe the **Diff** column | **Diff** = **−2** (negative value with minus sign; NOT blank and NOT 2) | Purchased Slot = 4; Lesson Allocated = 6; Diff = 4 − 6 = −2 |

**Severity:** minor
**Priority:** medium

---
