# Test Cases: LT-90306 — Lesson Allocation Soft Delete (Archive)

Source Qase suite reviewed: [PX suite 308 — "Lesson Allocation tab"](https://app.qase.io/project/PX?suite=308) (9 existing cases). Case 1655 ("List Views – Each view filters LAs by correct status and Academic Year") already confirms all 8 list views (`All`, `All_2023`, `All_2024`, `Fully_Assigned_2024`, `None_Assigned_2024`, `Over_Assigned_2024`, `Partially_Assigned_2024`, `Recently_Updated`) filter by `Require_Allocation__c = True` and status/Academic Year, but none test an archived Lesson Allocation.

Code trace: every one of the 8 declarative list views on `Lesson_Allocation__c` (`packages/lesson/main/default/objects/Lesson_Allocation__c/listViews/`) already carries two `<filters>` blocks at the metadata level — `Require_Allocation__c equals 1` and `Archived_At__c equals (blank)` — applied identically across all 8. This is already correct, but has zero regression coverage for the archived case specifically. Since this is a standard Salesforce list-view filter (not Apex), there's no code path divergence possible between the 8 views — any difference found during testing would indicate a metadata configuration mistake on one specific view, which is exactly why all 8 are checked explicitly below rather than assumed identical.

One incidental edge case worth testing: archiving an LA (`archiveAllocations`'s `UPDATE` stamping `Archived_At__c`) also updates the record's `LastModifiedDate` to now — which would normally qualify it for the "Recently Updated" list view (filtered on `LastModifiedDate = THIS_WEEK`). The `Archived_At__c` filter still excludes it despite this, since both filters are AND'd together.

## Suite: Lesson Allocation tab

### Lesson Allocation Tab – All 8 List Views – Archived Lesson Allocation Excluded from Every View Simultaneously

**Description:** Regression / control case — Decision Table, contrasts with the baseline (case 1655) — once a Require-Allocation=True Lesson Allocation is archived, it disappears from all 8 declarative list views at once (`All`, `All_2023`, `All_2024`, `Fully_Assigned_2024`, `None_Assigned_2024`, `Over_Assigned_2024`, `Partially_Assigned_2024`, `Recently_Updated`), including "Recently Updated" despite the archive action itself having just modified the record.

**Preconditions:**
- Student A has a Lesson Allocation for Course A, Require Allocation = True, Academic Year = 2024, with some but not all lessons assigned (status = Partially Assigned). It currently appears in the `All`, `All_2024`, and `Partially_Assigned_2024` list views.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff navigates to the Lesson Allocation tab and confirms the LA appears in the `All`, `All_2024`, and `Partially_Assigned_2024` list views | The LA is visible in all three views | Archived_At__c = blank → included |
| 2 | The Student Package Order behind this Lesson Allocation is fully removed, so the Lesson Allocation is archived | The Lesson Allocation shows Archived_At__c populated; LastModifiedDate updates to now | Archived_At__c = current timestamp |
| 3 | HQ or CM Staff checks each of the 8 list views in turn: `All`, `All_2023`, `All_2024`, `Fully_Assigned_2024`, `None_Assigned_2024`, `Over_Assigned_2024`, `Partially_Assigned_2024`, `Recently_Updated` | The Lesson Allocation does not appear in any of the 8 views, including `Recently_Updated` despite its LastModifiedDate having just changed | All 8 list views share the same `Archived_At__c equals (blank)` filter, applied before/alongside each view's own status/date criteria |

**Severity:** minor
**Priority:** medium

---

### Lesson Allocation Tab – Restored Lesson Allocation – Reappears in All and in Its Correct Status-Specific List View

**Description:** Regression / control case — Decision Table, continuing from the case above — once the archived Lesson Allocation is restored, it reappears not just in the generic `All`/`All_2024` views but correctly re-categorized into its actual status-specific view (`Partially_Assigned_2024`), confirming the restore doesn't leave it miscategorized or only partially visible.

**Preconditions:**
- Following directly from the case above: Student A's Lesson Allocation for Course A is archived, Academic Year = 2024, status would be Partially Assigned if visible.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | A living Student Package Order reappears for Student A's Course A Student Course, so the Lesson Allocation is unarchived on the same record Id | The Lesson Allocation shows Archived_At__c blank again | Archived_At__c = null (restored) |
| 2 | HQ or CM Staff navigates to the Lesson Allocation tab and checks the `All` and `All_2024` list views | The Lesson Allocation reappears in both | Archived_At__c = blank (restored) → included |
| 3 | HQ or CM Staff checks the `Partially_Assigned_2024` list view | The Lesson Allocation reappears here too, correctly reflecting its actual Partially Assigned status — not miscategorized into `None_Assigned_2024` or `Fully_Assigned_2024` | Lesson Allocation Status recalculated correctly from Allocated_Sessions__c/Total_Sessions__c, unaffected by the archive/restore cycle |

**Severity:** minor
**Priority:** low

---
