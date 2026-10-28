# Test Cases: LT-90306 — Lesson Allocation Soft Delete (Archive)

Source Qase suite reviewed: [PX suite 308 — "Lesson Allocation tab"](https://app.qase.io/project/PX?suite=308) (9 existing cases). Case 1655 ("List Views – Each view filters LAs by correct status and Academic Year") confirms the normal `Require Allocation`, status, and Academic Year filtering across 8 list views (`All`, `All_2023`, `All_2024`, `Fully_Assigned_2024`, `None_Assigned_2024`, `Over_Assigned_2024`, `Partially_Assigned_2024`, `Recently_Updated`), but it does not cover an archived Lesson Allocation.

**Known runtime behavior (updated 2026-10-19):** a soft-deleted Lesson Allocation cannot be hidden in the Lesson Allocation list views. It remains visible in every view whose normal status and Academic Year filters it matches. This is a visibility limitation only: it must not make the archived LA selectable in operational flows such as Add Student. The previous expected result that the record disappeared has been retired in local documentation and Qase cases #29303/#29226.

An archived LA's update also refreshes its Last Modified Date, so it remains eligible for `Recently_Updated` when the view's usual date window matches. That is part of the visible-current-behavior check below.

## Suite: Lesson Allocation tab

### Lesson Allocation Tab – Matching List Views – Archived Lesson Allocation Remains Visible

**Description:** Known behavior — Decision Table. A soft-deleted Lesson Allocation remains visible in every list view whose usual filters it matches. This documents the current List View limitation without treating the archived LA as active or selectable.

**Preconditions:**
- Student A has a Lesson Allocation for Course A, Require Allocation = True, Academic Year = 2024, with some but not all lessons assigned (status = Partially Assigned). It currently appears in the `All`, `All_2024`, and `Partially_Assigned_2024` list views.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff navigates to the Lesson Allocation tab and confirms the LA appears in the `All`, `All_2024`, and `Partially_Assigned_2024` list views | The LA is visible in all three views | Archive timestamp blank; included |
| 2 | HQ or CM Staff fully removes the Student Package Order behind this Lesson Allocation so the Lesson Allocation is archived | The Lesson Allocation shows its archive timestamp populated and Last Modified Date updated to now | Archive timestamp = current timestamp |
| 3 | HQ or CM Staff checks all 8 list views: `All`, `All_2023`, `All_2024`, `Fully_Assigned_2024`, `None_Assigned_2024`, `Over_Assigned_2024`, `Partially_Assigned_2024`, and `Recently_Updated` | The archived Lesson Allocation remains visible in the four matching views (`All`, `All_2024`, `Partially_Assigned_2024`, and `Recently_Updated`). It is absent from the other four only because it does not satisfy their ordinary Academic Year or status filters. | Archive timestamp populated; matching filters: Require Allocation = True, Academic Year = 2024, Status = Partially Assigned, Last Modified Date = this week |

**Severity:** minor
**Priority:** medium

---

### Lesson Allocation Tab – Restored Lesson Allocation – Remains Visible with Its Status Classification Unchanged

**Description:** Known behavior regression — Decision Table. Because an archived Lesson Allocation remains visible in matching list views, restore clears the archive state without changing its list visibility or its status classification.

**Preconditions:**
- Student A's Lesson Allocation for Course A is archived, Academic Year = 2024, and Status = Partially Assigned. It remains visible in the matching list views.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff restores a living Student Package Order for Student A's Course A Student Course | The same Lesson Allocation is unarchived and its archive timestamp is cleared | Same Lesson Allocation record Id; archive timestamp = blank |
| 2 | HQ or CM Staff navigates to the Lesson Allocation tab and checks the `All` and `All_2024` list views | The Lesson Allocation remains visible in both; restore does not cause it to disappear or duplicate. | Archive timestamp cleared; same Lesson Allocation record |
| 3 | HQ or CM Staff checks the `Partially_Assigned_2024` list view | The Lesson Allocation remains visible and retains the Partially Assigned classification; it is not moved to `None_Assigned_2024` or `Fully_Assigned_2024`. | Lesson Allocation Status is Partially Assigned before and after restore |

**Severity:** minor
**Priority:** low

---
