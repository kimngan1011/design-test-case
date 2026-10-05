# Test Cases: LT-90306 — Lesson Allocation Soft Delete (Archive)

Source Qase suite reviewed: [PX suite 1649 — "Assign/Unassign a student"](https://app.qase.io/project/PX?suite=1649), child of suite 267 "Assign/Unassign a student by Add student popup" (20 existing cases). Cases 8509-8520 establish the baseline: assigning a student to one instance of a recurring lesson (Daily/Weekly/Custom, End Date or Lesson Count) propagates the assignment to every instance in the chain. None of those cases combine this propagation with a student whose Lesson Allocation was archived and then restored.

## Suite: Assign/Unassign a student

### Assign Student – This and Following Lessons – Lesson Allocation Restored – Student Appears and Assignable Across All Following Instances

**Description:** Feature Impact (LA authorization & Add Student / Class Assignment) — Decision Table — after a previously archived Lesson Allocation is restored (unarchived, same record Id), the student becomes selectable in the Add Student picker again and, once assigned with "This and following lessons" scope, is correctly propagated to every remaining instance of the recurring chain — not just the first one.

**Preconditions:**
- HQ or CM Staff is logged in to Salesforce.
- A weekly recurring lesson chain for Class A exists at Location Tokyo HQ with 5 instances: 2026-05-04, 05-11, 05-18, 05-25, 06-01.
- Student A's Lesson Allocation was previously archived, then unarchived (same record Id) after a living Student Package Order reappeared for the same Student Course, so Student A's Lesson Allocation now shows Archived_At__c blank.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens the first lesson instance (2026-05-04) and clicks Add Student | The Add Student picker opens and shows Student A, since their Lesson Allocation is no longer archived | Student A Archived_At__c = blank (restored) → shown |
| 2 | HQ or CM Staff selects Student A, chooses "This and following lessons" scope, and saves | Student A is assigned to the first instance and the assignment propagates to the following instances in the chain | scope = This and following lessons |
| 3 | HQ or CM Staff opens each of the remaining 4 lesson instances (2026-05-11, 05-18, 05-25, 06-01) | Student A appears in the Student Sessions section of every instance | Student A present in all 5 lesson instances |
| 4 | HQ or CM Staff opens Student A's Lesson Allocation record | Lesson Allocated count reflects all 5 newly assigned sessions; Lesson Allocation Status and Report History are updated consistently with the full propagated assignment | Student A LA detail fields reflect all 5 sessions |

**Severity:** major
**Priority:** high

---
