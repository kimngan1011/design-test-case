# Test Cases: LT-90306 — Lesson Allocation Soft Delete (Archive)

Source Qase suite reviewed: [PX suite 1295 — "Bulk Assign Class"](https://app.qase.io/project/PX?suite=1295) (21 existing cases). The existing suite covers active Lesson Allocations only. These cases cover archive filtering, restore, and the time-of-check/time-of-use boundary created by the soft-delete refactor.

## Suite: Bulk Assign Class

### Bulk Assign Class – Archived Lesson Allocation – Allocation Table – Student Cannot Be Selected

**Description:** AC-5 — Negative — An archived Lesson Allocation is absent from the source table, so it cannot be selected for bulk class assignment.

**Preconditions:**
- HQ or CM Staff is logged in to Salesforce.
- Today is 2026-05-20 in the organisation time zone.
- Student A has a Math 101 Lesson Allocation from 2026-05-01 through 2026-12-31.
- Student A's Math 101 Lesson Allocation was archived after every related Student Package Order was removed.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens Student A's Course tab and opens the Require Lesson Allocation table | The table is displayed | today = 2026-05-20; allocation_status = archived |
| 2 | HQ or CM Staff searches for Student A's Math 101 allocation and attempts to select it for Bulk Assign Class | The allocation is absent and cannot be selected; the Bulk Assign Class flow cannot be started for it | archived_allocation = Math 101 |

**Severity:** critical
**Priority:** high

---

### Bulk Assign Class – Allocation Archived Before Submit – Existing Modal Selection – No Membership Created

**Description:** AC-5 — State Transition — A bulk assignment opened while an allocation was active must not create a Class Member if the allocation is archived before submission.

**Preconditions:**
- HQ or CM Staff is logged in to Salesforce.
- Today is 2026-05-20 in the organisation time zone.
- Student A has an active Math 101 Lesson Allocation from 2026-05-01 through 2026-12-31.
- Student A has no Class Member for Math 101.
- Class A has Academic Level Grade 2 and belongs to Math 101 at Location Tokyo HQ.
- A Group lesson for Class A exists on 2026-05-21.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff selects Student A's active Math 101 allocation, opens Bulk Assign Class, selects Class A, and enters 2026-05-20 as the effective date without submitting | The confirmation step is ready for submission | today = 2026-05-20; class = Class A; effective_date = 2026-05-20 |
| 2 | A second authorised staff session removes every Student Package Order for Student A's Math 101 allocation and waits for allocation processing to finish | Student A's selected Lesson Allocation becomes archived before the first staff member submits | allocation_status = archived |
| 3 | HQ or CM Staff confirms Bulk Assign Class in the original modal | The assignment is not completed; no new Class Member is created for Student A | selected_allocation = archived before submission |
| 4 | HQ or CM Staff opens the Class A lesson on 2026-05-21 after class processing finishes | Student A is absent from the Student Sessions list | lesson_date = 2026-05-21; expected_student_sessions_for_student_a = 0 |

**Severity:** critical
**Priority:** high

---

### Bulk Assign Class – Restored Lesson Allocation – Existing Same-Level Class Member – Duplicate Membership Skipped

**Description:** AC-2 / AC-3 / AC-5 — Decision Table — After restore, Bulk Assign Class recognises the original active Class Member and does not create a duplicate for the same academic level.

**Preconditions:**
- HQ or CM Staff is logged in to Salesforce.
- Today is 2026-05-20 in the organisation time zone.
- Student A has an archived Math 101 Lesson Allocation and its original archived Class A membership from 2026-05-01 through 2026-12-31.
- Class A has Academic Level Grade 2 and belongs to Math 101 at Location Tokyo HQ.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff restores one living Student Package Order for Student A's Math 101 allocation and waits for allocation processing to finish | The original allocation and Class A membership are restored; no additional Class A membership is created | today = 2026-05-20; restored_order_start = 2026-05-01; restored_order_end = 2026-12-31 |
| 2 | HQ or CM Staff selects the restored Math 101 allocation, chooses Class A with Academic Level Grade 2, sets effective date to 2026-05-20, and confirms Bulk Assign Class | The assignment completes without creating another Class A membership | class = Class A; academic_level = Grade 2; effective_date = 2026-05-20 |
| 3 | HQ or CM Staff opens Student A's Class history | Exactly one active Class A membership exists from 2026-05-01 through 2026-12-31 | expected_class_a_membership_count = 1 |

**Severity:** critical
**Priority:** high

---

### Bulk Assign Class – Restored Lesson Allocation – Existing Class Member – New Class Assigned

**Description:** AC-2 / AC-3 / AC-5 — State Transition — A restored Lesson Allocation with an existing Class Member can still use Bulk Assign Class to change to a new class.

**Preconditions:**
- HQ or CM Staff is logged in to Salesforce.
- Today is 2026-05-20 in the organisation time zone.
- Student A has an archived Math 101 Lesson Allocation and its original archived Class A membership from 2026-05-01 through 2026-12-31.
- Class A has Academic Level Grade 2 and Class B has Academic Level Grade 3; both belong to Math 101 at Location Tokyo HQ.
- A Group lesson for Class B exists on 2026-05-21.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff restores one living Student Package Order for Student A's Math 101 allocation and waits for allocation processing to finish | The original allocation and Class A membership are restored on their existing records | today = 2026-05-20; restored_order_start = 2026-05-01; restored_order_end = 2026-12-31 |
| 2 | HQ or CM Staff selects the restored Math 101 allocation, chooses Class B with Academic Level Grade 3, sets effective date to 2026-05-20, accepts the level-mismatch confirmation, and confirms Bulk Assign Class | Class A ends on 2026-05-20 and a Class B membership starts on 2026-05-20 | previous_class = Class A; new_class = Class B; effective_date = 2026-05-20 |
| 3 | HQ or CM Staff opens the Class B lesson on 2026-05-21 after class processing finishes | Student A appears once in the Student Sessions list | lesson_date = 2026-05-21; expected_student_sessions_for_student_a = 1 |

**Severity:** critical
**Priority:** high

---

### Bulk Assign Class – Restored Lesson Allocation – No Matching Class Member – New Membership Created

**Description:** AC-2 / AC-3 / AC-5 — CRUD — A restored Lesson Allocation remains eligible for a new Bulk Assign Class action when it has no matching Class Member.

**Preconditions:**
- HQ or CM Staff is logged in to Salesforce.
- Today is 2026-05-20 in the organisation time zone.
- Student A has an archived Math 101 Lesson Allocation from 2026-05-01 through 2026-12-31.
- Student A has no Class Member for Math 101.
- Class A has Academic Level Grade 2 and belongs to Math 101 at Location Tokyo HQ.
- A Group lesson for Class A exists on 2026-05-21.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff restores one living Student Package Order for Student A's Math 101 allocation and waits for allocation processing to finish | Student A's original Lesson Allocation is restored and is selectable for Bulk Assign Class | today = 2026-05-20; restored_order_start = 2026-05-01; restored_order_end = 2026-12-31 |
| 2 | HQ or CM Staff selects the restored Math 101 allocation, chooses Class A with Academic Level Grade 2, sets effective date to 2026-05-20, and confirms Bulk Assign Class | One new Class A membership is created for Student A with start date 2026-05-20 | class = Class A; academic_level = Grade 2; effective_date = 2026-05-20 |
| 3 | HQ or CM Staff opens the Class A lesson on 2026-05-21 after class processing finishes | Student A appears once in the Student Sessions list | lesson_date = 2026-05-21; expected_student_sessions_for_student_a = 1 |

**Severity:** critical
**Priority:** high

---

### Bulk Assign Class – Restored Lesson Allocation – JST and UTC Effective-Date Boundary – Membership Starts on Selected JST Date

**Description:** AC-3 / AC-5 — Boundary Value Analysis — Bulk Assign Class after restore preserves the user-selected JST effective date when its UTC representation falls on the previous calendar day.

**Preconditions:**
- HQ or CM Staff is logged in to Salesforce with timezone Asia/Tokyo.
- Student A has an archived Math 101 Lesson Allocation from 2026-05-01 through 2026-12-31.
- Student A has no Class Member for Math 101.
- Class A has Academic Level Grade 2 and belongs to Math 101 at Location Tokyo HQ.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff restores one living Student Package Order for Student A's Math 101 allocation and waits for allocation processing to finish | Student A's original Lesson Allocation is restored and is selectable for Bulk Assign Class | restored_at = 2026-05-20 00:30 JST (= 2026-05-19 15:30 UTC) |
| 2 | HQ or CM Staff selects the restored allocation, chooses Class A, enters 2026-05-20 as the effective date, and confirms Bulk Assign Class | A Class A membership is created with effective start date 2026-05-20 in JST | effective_date = 2026-05-20 JST; stored_start = 2026-05-19 15:00 UTC |
| 3 | HQ or CM Staff opens Student A's Class history in JST | Class A displays start date 2026-05-20, not 2026-05-19 | display_timezone = JST; expected_display_start = 2026-05-20 |

**Severity:** major
**Priority:** high
