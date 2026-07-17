# Test Cases: LT-98531 — [Riso] Monthly Lesson Assignment Report – Multi-Student Filter

## Suite: Multi-Student Filter – Behavior and Row Display

### [Riso] Monthly Lesson Assignment Report – Multi-Student Filter – Multiple Students Selected, All Matching Rows Shown

**Description:** AC-12 — Equivalence Partitioning — When multiple students are selected in the Student or Contact ID filter, all matching rows for each selected student are shown in the report.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org
- Three students exist with contracts and sessions in June 2026: Student A, Student B, Student C
- Each student has at least one contract row expected to appear in the report for AY 2025-2026, June 2026
- today = 2026-06-22; current_AY = 2025-2026; target_month = 2026-06

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to the Monthly Lesson Assignment report page, set AY 2025-2026 and June 2026 | Report page loads with filters applied | today = 2026-06-22; current_AY = 2025-2026; target_month = 2026-06 |
| 2 | In the Student or Contact ID filter, select Student A, Student B, and Student C | All three students are shown as selected in the filter | Student A: STU-001; Student B: STU-002; Student C: STU-003 |
| 3 | Apply the filter (or observe auto-apply) | Report loads rows | "" |
| 4 | Observe all rows in the report | Rows for Student A, Student B, and Student C are all present; no selected student is missing from the results | Expected: at least one row per selected student |
| 5 | Confirm no rows for unselected students appear | Only rows belonging to Student A, B, or C are shown; rows for other students are not present | "" |

**Severity:** minor
**Priority:** medium

---

### [Riso] Monthly Lesson Assignment Report – Multi-Student Filter – Each Student Has One Row Per Student-Course Combination

**Description:** AC-12 — Component — When multiple students are selected, each student appears once per student-course combination in the report (not aggregated across courses, not duplicated).

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org
- Student A has two contracts (two different courses) in AY 2025-2026: Course = English and Course = Math
- Student B has one contract (one course) in AY 2025-2026: Course = English
- today = 2026-06-22; current_AY = 2025-2026; target_month = 2026-06

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to the Monthly Lesson Assignment report page, set AY 2025-2026 and June 2026, select Student A and Student B, then apply | Report loads | today = 2026-06-22; Student A: 2 contracts (English, Math); Student B: 1 contract (English); target_month = 2026-06 |
| 2 | Count the rows for Student A | Student A has exactly **2 rows**: one row for English and one row for Math | Student A rows: (1) Student A – English; (2) Student A – Math |
| 3 | Count the rows for Student B | Student B has exactly **1 row** for English | Student B row: (1) Student B – English |
| 4 | Confirm no duplicate rows exist | Total rows = 3 (2 for Student A + 1 for Student B); no row is duplicated | Expected total: 3 distinct rows |

**Severity:** minor
**Priority:** medium

---
