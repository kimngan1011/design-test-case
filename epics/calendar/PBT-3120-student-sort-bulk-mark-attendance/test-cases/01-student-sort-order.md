# Test Cases: PBT-3120 - Student Sort in Bulk Mark Attendance

## Suite: Student Sort Order

### Bulk Mark Attendance - Student List - Multi-key sort with mixed data - Displays Grade then Phonetic then Name then Created at

**Description:** AC 01.1 - Scenario - Validate deterministic ordering using all four sort keys with mixed Japanese and Latin data.

**Preconditions:**
- Logged in as HQ or CM Staff to BO Calendar.
- Open a lesson in Bulk Mark Attendance with at least 6 students.
- Students are prepared with explicit values:
  - S1: Grade=3, Phonetic=アオキ, Name=青木 一郎, CreatedAt=2026-05-01 09:00
  - S2: Grade=2, Phonetic=サトウ, Name=佐藤 花子, CreatedAt=2026-05-01 09:00
  - S3: Grade=3, Phonetic=アオキ, Name=青木 次郎, CreatedAt=2026-05-01 09:30
  - S4: Grade=3, Phonetic=イシダ, Name=石田 太郎, CreatedAt=2026-05-01 09:10
  - S5: Grade=3, Phonetic=アオキ, Name=Abe Ken, CreatedAt=2026-05-01 08:40
  - S6: Grade=2, Phonetic=スズキ, Name=鈴木 一輝, CreatedAt=2026-05-01 08:50

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open the lesson in Bulk Mark Attendance and load the student list | Student list is displayed with all prepared records | dataset_id = PBT3120-SORT-01 |
| 2 | Read the list order from top to bottom | All Grade=2 students appear before Grade=3 students | key1 = Grade asc |
| 3 | In the Grade=2 group, compare students by Phonetic Name | Students are ordered by phonetic reading (サトウ then スズキ, or per approved lexical order) | key2 = Phonetic Name |
| 4 | In the Grade=3 and Phonetic=アオキ group, compare Student Name | Students are ordered by Student Name before Created at | key3 = Student Name |
| 5 | In the exact same Grade+Phonetic+Name group, compare timestamps | Older CreatedAt appears before newer CreatedAt | key4 = CreatedAt asc |

**Severity:** major
**Priority:** high

---

### Bulk Mark Attendance - Student List - Empty phonetic tie-break fallback - Keeps deterministic order without null artifacts

**Description:** AC 01.1 - Decision Table - Ensure null or empty phonetic values are handled consistently in tie-break order.

**Preconditions:**
- Logged in as HQ or CM Staff to BO Calendar.
- Open Bulk Mark Attendance with students in same Grade.
- Test data:
  - S1: Grade=4, Phonetic="", Name=山本 一郎, CreatedAt=2026-05-01 09:00
  - S2: Grade=4, Phonetic=null, Name=山本 二郎, CreatedAt=2026-05-01 09:10
  - S3: Grade=4, Phonetic=ヤマモト, Name=山本 三郎, CreatedAt=2026-05-01 09:20

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open the student list for the prepared lesson | Student list loads successfully with all 3 records | dataset_id = PBT3120-SORT-NULL-01 |
| 2 | Compare ordering among equal-grade rows where phonetic is empty/null/present | Ordering is deterministic and consistent across reloads; no random row jump | phonetic = "" / null / ヤマモト |
| 3 | Reload the page and open the same list again | Order remains the same as before reload | reload = 1 |
| 4 | Observe each row label rendering | No `Null`, empty placeholder token, or broken formatting is displayed in the student row | display_assert = no Null token |

**Severity:** major
**Priority:** high

---

### Bulk Mark Attendance - Student List - Baseline parity with LT-77063 - Produces the same ordered output for equivalent input

**Description:** AC 01.2 - Regression - Confirm this page follows LT-77063 sorting baseline with equivalent fixture data.

**Preconditions:**
- Logged in as HQ or CM Staff.
- Same fixture dataset is available in both baseline flow (LT-77063 reference screen) and Bulk Mark Attendance target screen.
- Fixture includes at least one tie case at each key level.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open baseline screen that implements LT-77063 sort logic and capture visible row order | Baseline order list is recorded | baseline_ref = LT-77063 |
| 2 | Open Bulk Mark Attendance for the same fixture and capture visible row order | Target order list is recorded | target_ref = PBT-3120 |
| 3 | Compare row sequence from both screens | Both screens produce the same relative order for all rows | compare_mode = sequence equality |

**Severity:** minor
**Priority:** medium

---

### Bulk Mark Attendance - Student List - Role consistency in BO access - CPU Teacher and SPU CM see the same ordered sequence

**Description:** AC 01.1 - Decision Table - Validate role-independent ordering for eligible BO roles.

**Preconditions:**
- A lesson is visible to both CPU Teacher and SPU CM accounts.
- Both accounts can access Bulk Mark Attendance for the same lesson.
- Fixture dataset matches the multi-key tie dataset from case PBT3120-SORT-01.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Sign in as CPU Teacher and open Bulk Mark Attendance list | Student list is visible and ordered | role = CPU Teacher |
| 2 | Save the displayed row order as snapshot A | Snapshot A captured | snapshot = A |
| 3 | Sign in as SPU CM and open the same lesson list | Student list is visible and ordered | role = SPU CM |
| 4 | Save the displayed row order as snapshot B and compare with snapshot A | Snapshot B matches snapshot A exactly | compare = A vs B |

**Severity:** minor
**Priority:** medium
