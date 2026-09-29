# Test Cases: SOQL OFFSET 2,000 — search reaches records beyond the loaded rows

## Suite: Add master participant (Qase 2618)

### Add Master Participant – More than 2,050 matching students – Scroll stops loading and search by name still finds a not-loaded student

_Qase: PX-29124_

**Description:** OFFSET limit — Boundary — The popup pages 50 rows per scroll and cannot load beyond ~2,050 rows; the search bar is applied before paging, so a student past that row is still found by name. Accepted limitation: loading stops around row 2,000; searching by name must still return records that are not loaded.

**Spec sources:**
- [S3] Code – addEventParticipantExt (50 per page, offset = page × 50) → EventParticipantHandler.getTargetParticipants (LIMIT/OFFSET, search in WHERE)
- [S1] Lesson learned 2026-09-29 "Infinite-Scroll / Paged Lists Stop at ~2,000 Rows (SOQL OFFSET Limit)" — design-test-case/knowledge/domain-knowledge/scheduling/lesson-learned/core.md
- [S2] Salesforce SOQL: OFFSET maximum is 2,000 rows (NUMBER_OUTSIDE_VALID_RANGE above it)

**Preconditions:**
- HQ or CM Staff is logged in to Salesforce
- Event Master EM01 has a Target Location (or default filter) that matches more than 2,050 students (default Enrollment Status Enrolled + Temporary)
- Student S_LAST is one of the matching students whose name sorts after row 2,050 in name order (e.g. a name starting with "Z")
- The Add Participant popup of EM01 is open

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff scrolls the student list to the bottom repeatedly until no more rows load | Rows load 50 at a time; loading stops at about 2,050 rows even though more students match; S_LAST is not in the loaded list | expected stop ≈ 2,050 rows |
| 2 | HQ or CM Staff types the name of S_LAST in the search bar | The list shows S_LAST | search = S_LAST name |
| 3 | HQ or CM Staff selects S_LAST and adds it to the Master Participant List | S_LAST is added to the Master Participant List of EM01 |  |

**Severity:** minor
**Priority:** medium

---

## Suite: Add master staff (Qase 2616)

### Add Master Staff – More than 2,050 matching staff – Scroll stops loading and search by name still finds a not-loaded staff

_Qase: PX-29125_

**Description:** OFFSET limit — Boundary — The popup pages 50 staff per scroll and cannot load beyond ~2,050 rows; search by name still finds a staff past that row. Accepted limitation: loading stops around row 2,000; searching by name must still return records that are not loaded.

**Spec sources:**
- [S3] Code – addEventStaffExt (50 per page) → EventStaffHandler.getStaffByFilter (Affiliation aggregate LIMIT/OFFSET, name search applied first)
- [S1] Lesson learned 2026-09-29 "Infinite-Scroll / Paged Lists Stop at ~2,000 Rows (SOQL OFFSET Limit)" — design-test-case/knowledge/domain-knowledge/scheduling/lesson-learned/core.md
- [S2] Salesforce SOQL: OFFSET maximum is 2,000 rows (NUMBER_OUTSIDE_VALID_RANGE above it)

**Preconditions:**
- HQ or CM Staff is logged in to Salesforce
- More than 2,050 available staff match the popup filter (e.g. no location filter, or a location with more than 2,050 affiliated staff) — large-org / generated data required
- Staff T_LAST is one of the matching staff whose position in the list is after row 2,050
- The Add Master Staff popup of Event Master EM01 is open

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff scrolls the staff list to the bottom repeatedly until no more rows load | Loading stops at about 2,050 rows; T_LAST is not in the loaded list | expected stop ≈ 2,050 rows |
| 2 | HQ or CM Staff types the name of T_LAST in the search bar | The list shows T_LAST | search = T_LAST name |
| 3 | HQ or CM Staff selects T_LAST and adds it | T_LAST is added to the Master Staff List of EM01 |  |

**Severity:** minor
**Priority:** low

---

## Suite: Assign to Event (SF) (Qase 2607)

### Assign Staff to Event – Master Staff List larger than 2,100 – Scroll stops loading and search by name still finds a not-loaded staff

_Qase: PX-29126_

**Description:** OFFSET limit — Boundary — The Assign Staff popup pages 100 rows and cannot load beyond ~2,100 rows of the Master Staff List; search by name still finds a staff past that row. Accepted limitation: loading stops around row 2,000; searching by name must still return records that are not loaded.

**Spec sources:**
- [S3] Code – addEventStaffOnAssignEvent (100 per page) → EventStaffHandler.getEventStaffOnAssignEvent → getStaffByFilter
- [S1] Lesson learned 2026-09-29 "Infinite-Scroll / Paged Lists Stop at ~2,000 Rows (SOQL OFFSET Limit)" — design-test-case/knowledge/domain-knowledge/scheduling/lesson-learned/core.md
- [S2] Salesforce SOQL: OFFSET maximum is 2,000 rows (NUMBER_OUTSIDE_VALID_RANGE above it)

**Preconditions:**
- HQ or CM Staff is logged in to Salesforce
- Event Master EM01 has more than 2,100 staff in its Master Staff List — generated data required
- Staff T_LAST is in the Master Staff List and its position in the popup list is after row 2,100
- Activity Event AE01 under EM01 is open and its Assign Staff popup is open

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff scrolls the staff list to the bottom repeatedly until no more rows load | Loading stops at about 2,100 rows; T_LAST is not in the loaded list | expected stop ≈ 2,100 rows |
| 2 | HQ or CM Staff types the name of T_LAST in the search bar | The list shows T_LAST | search = T_LAST name |
| 3 | HQ or CM Staff selects T_LAST and confirms the assignment | T_LAST is added to the Event Staff list of AE01 |  |

**Severity:** minor
**Priority:** low

---

## Suite: Assign to Event (SF) (Qase 2607)

### Assign to Event – More than 2,100 students in the list – Scroll stops loading and search by name still finds a not-loaded student

_Qase: PX-29127_

**Description:** OFFSET limit — Boundary — The Assign to Event student popup pages 100 rows; the code caps at offset 2,000 but one page late, so the request at offset 2,100 fails silently. Search by name still finds a student past that row. Accepted limitation: loading stops around row 2,000; searching by name must still return records that are not loaded.

**Spec sources:**
- [S3] Code – addEventParticipantOnAssignEvent (100 per page, hasNextPage = offset <= 2000) → EventParticipantHandler.getEventParticipantFilters
- [S1] Lesson learned 2026-09-29 "Infinite-Scroll / Paged Lists Stop at ~2,000 Rows (SOQL OFFSET Limit)" — design-test-case/knowledge/domain-knowledge/scheduling/lesson-learned/core.md
- [S2] Salesforce SOQL: OFFSET maximum is 2,000 rows (NUMBER_OUTSIDE_VALID_RANGE above it)

**Preconditions:**
- HQ or CM Staff is logged in to Salesforce
- Event Master EM01 has a target segment and/or Master Participant List giving more than 2,100 students in the Assign to Event popup
- Student S_LAST is in that list and its position is after row 2,100 (name order)
- Activity Event AE01 under EM01 is open and its Assign to Event (student) popup is open

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff scrolls the student list to the bottom repeatedly until no more rows load | Loading stops at about 2,100 rows; S_LAST is not in the loaded list; further scrolling loads nothing (no error message) | expected stop ≈ 2,100 rows |
| 2 | HQ or CM Staff types the name of S_LAST in the search bar | The list shows S_LAST | search = S_LAST name |
| 3 | HQ or CM Staff selects S_LAST and assigns it to AE01 | S_LAST is added as Event Participant of AE01 |  |

**Severity:** minor
**Priority:** medium

---

## Suite: Aver lesson report (Qase 2633)

### [Aver] Lesson Report List (V1) – More than 2,025 reports – Pages after row 2,025 fail and search by student name still finds a report there

_Qase: PX-29128_

**Description:** OFFSET limit — Boundary — With the Unleash toggle Lesson_BackOffice_LessonSF_AllowViewLessonOtherLocations OFF (V1 list), the list pages 25 rows with SOQL OFFSET and an uncapped total count; pages starting after row 2,025 show "Unable to load data". Search by student name still returns reports there. Accepted limitation: loading stops around row 2,000; searching by name must still return records that are not loaded.

**Spec sources:**
- [S3] Code – school-portal-admin useRetrieveAverLessonReportList (V1: LIMIT 25 OFFSET page × 25, COUNT() not capped)
- [S1] Lesson learned 2026-09-29 "Infinite-Scroll / Paged Lists Stop at ~2,000 Rows (SOQL OFFSET Limit)" — design-test-case/knowledge/domain-knowledge/scheduling/lesson-learned/core.md
- [S2] Salesforce SOQL: OFFSET maximum is 2,000 rows (NUMBER_OUTSIDE_VALID_RANGE above it)

**Preconditions:**
- Aver tenant; HQ or CM Staff is logged in to Back Office
- Unleash toggle Lesson_BackOffice_LessonSF_AllowViewLessonOtherLocations is OFF for the environment (V1 list)
- More than 2,025 Aver Lesson Reports match the default list filter
- Report R_LAST belongs to student S_LAST and its row in the default order (lesson start ascending) is after row 2,025

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens the Aver Lesson Report list in Back Office | The list shows 25 rows per page and a total count above 2,025 |  |
| 2 | HQ or CM Staff goes to page 81, then to page 82 (or the last page) | Page 81 (rows 2,001–2,025) loads; page 82 and later show "Unable to load data" and no rows | page size = 25; page 82 offset = 2,025 |
| 3 | HQ or CM Staff types the name of S_LAST in the search box | The list shows R_LAST | search = S_LAST name |

**Severity:** minor
**Priority:** medium

---
