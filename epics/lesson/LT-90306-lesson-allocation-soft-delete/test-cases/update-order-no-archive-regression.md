# Test Cases: LT-90306 — Lesson Allocation Soft Delete (Archive)

Source Qase suite reviewed: [PX suite 2574 — "Update Order"](https://app.qase.io/project/PX?suite=2574) (14 existing cases, US05). None explicitly test that partial updates (slot increase/decrease, duration extend/reduce) leave `Archived_At__c` untouched. This file adds regression-lock cases confirming the archive refactor did not change this flow's behavior.

Code trace: `LessonAllocationSyncService.collectAllocationsToUpdate` → `DefaultAllocationDurationRecalculator.recalculateFromOrders` only rewrites `Start_Date_Time__c`, `End_Date_Time__c`, `Order_Remark_Value__c`, `Total_Session_Count__c`, `Purchased_Slot_Number__c` — it never touches `Archived_At__c`. `shouldArchiveAllocationOfStudentCourse` only fires when **every** order for the student-course is removed (`DeletedAt__c != null` or both Start/End dates null on all orders) — a decrease that leaves the order alive with valid dates never satisfies this, no matter how small the resulting slot count or duration becomes. This confirms the archive mechanism introduced by this epic has zero effect on the existing Update Order (slot/duration) behavior already covered by cases 1666–9929/18832–18834 — this file locks that boundary in explicitly.

## Suite: Update Order

### Update Order – Slot Decreased to Minimum (1) – Lesson Allocation Not Archived; Existing Behavior Unchanged

**Description:** Regression / boundary case — Decision Table, contrasts with the baseline (case 1667, "Decrease Slot – Purchased Slot Updated") — decreasing a Frequency/Slot-Based order's slot count all the way down to the minimum valid value (1) never archives the Lesson Allocation, since the order itself still exists with valid Start/End dates. Only Purchased_Slot_Number__c and Total_Session_Count__c are recalculated; Archived_At__c remains untouched throughout.

**Preconditions:**
- Student A has a Frequency order for Course A with Require Allocation = True, currently at 3 slots/week. Student A is auto-assigned to a group lesson by class.
- `Enable_Lesson_Allocation_Archive__c` = TRUE.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens the order group detail, clicks "Update", decreases slot/week from 3 to the minimum value of 1, fills in an effective date, saves draft, and submits | The order is submitted successfully | New slot/week = 1 |
| 2 | HQ or CM Staff opens Student A's Lesson Allocation | Purchased_Slot_Number__c and Total_Session_Count__c are recalculated for 1 slot/week; Archived_At__c remains blank; LA duration unchanged | Archived_At__c = null throughout; no archive-related fields touched |
| 3 | HQ or CM Staff navigates to Student A's Course tab / Lesson Allocation list | The Lesson Allocation still appears in the active list, exactly as before the update | Is_Archived__c = FALSE (via formula) → unaffected by the slot decrease |

**Severity:** minor
**Priority:** medium

---

### Update Order – Duration Reduced to a Single Day – Lesson Allocation Not Archived; Existing Behavior Unchanged

**Description:** Regression / boundary case — Decision Table, contrasts with the baseline (case 9925, "Reduce Start and End Date – Duration Updated") — reducing a Slot-Based order's duration down to the narrowest valid window (start date = end date, a single day) never archives the Lesson Allocation, as long as the order itself is not removed (both dates remain populated, non-null). Only Start_Date_Time__c/End_Date_Time__c are recalculated; Archived_At__c remains untouched.

**Preconditions:**
- Student A has a Slot-Based order for Course A with Require Allocation = True, currently spanning 2026-08-01 to 2026-12-31.
- `Enable_Lesson_Allocation_Archive__c` = TRUE.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens the order group detail, clicks "Update", reduces both start and end date to the same single day (2026-09-15), saves draft, and submits | The order is submitted successfully | new_start = new_end = 2026-09-15 |
| 2 | HQ or CM Staff opens Student A's Lesson Allocation | LA Start_Date_Time__c and End_Date_Time__c both update to 2026-09-15; Archived_At__c remains blank | Archived_At__c = null throughout; a narrow but non-null duration is not treated as "removed" |
| 3 | HQ or CM Staff navigates to Student A's Course tab / Lesson Allocation list | The Lesson Allocation still appears in the active list | Is_Archived__c = FALSE (via formula) → unaffected by the extreme duration reduction |

**Severity:** minor
**Priority:** medium

---
