# Test Cases: LT-90306 — Lesson Allocation Soft Delete (Archive)

Source Qase suite reviewed: [PX suite 3075 — "Report History"](https://app.qase.io/project/PX?suite=3075) (5 existing cases, under parent 308). Existing case 1659 confirms the "Report History" tab is shown only when Require Allocation = True. None test an archived Lesson Allocation.

Code trace: the "Report History" tab (`Lesson_Allocation_New_Record_Page1_Ext.flexipage-meta.xml`, a declarative `lst:dynamicRelatedList` on `Student_Sessions__r`) has its own `adminFilters` including `Is_Archived__c|EQUALS|false` — so even in isolation, its related-list rows would be filtered out once the LA's sessions are archived. But a higher-priority gate exists first: the SAME flexipage's containing tabset region (hosting "Student Sessions Related", "Report History", and "Class history" together) has a visibility rule `{!Record.Is_Archived__c} EQUAL false`. For an archived LA, this outer tabset disappears entirely — the "Report History" tab is never reached at all, regardless of its own Require Allocation or Is_Archived__c filters. This is confirmed intentional design (the `Is_Archived__c` field's own metadata description states its purpose is specifically to drive Lightning App Builder component visibility), not an accidental gap.

## Suite: Report History

### Report History – Archived Lesson Allocation – Entire Tabset (Not Just the Tab's Rows) Disappears on Direct Record-Id Access

**Description:** Regression / control case — Decision Table, contrasts with the baseline (case 1659, "Report History Tab – Shown only when Require Allocation = True") — opening an archived Lesson Allocation's detail page directly by record Id hides the "Report History" tab entirely, via the same outer tabset visibility rule already confirmed for "Student Sessions Related" (suite 323/324) — not because its own historical rows are empty, but because the whole containing region is gone before the tab's own filters ever apply. This distinguishes "tab absent" from "tab present but showing zero rows," which matters for how a tester interprets what they see.

**Preconditions:**
- A Lesson Allocation with Require Allocation = True has historical lesson report entries (filled-in Student Sessions with report content) before being archived.
- Student A's Lesson Allocation is subsequently archived (Archived_At__c populated) after its Student Package Order was fully removed.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens Student A's archived Lesson Allocation detail page directly by record Id | The LA Detail page loads; the Archived_At__c field shows a populated timestamp | Page reachable despite archive, by design |
| 2 | HQ or CM Staff looks for the "Report History" tab | The tab is not shown at all — not present with zero rows, but structurally absent from the page, along with "Student Sessions Related" and "Class history" | Outer tabset visibility rule {!Record.Is_Archived__c} EQUAL false hides the whole region before Report History's own Require Allocation / Is_Archived__c filters ever run |
| 3 | A living Student Package Order reappears for Student A's Student Course, so the Lesson Allocation is unarchived on the same record Id, and HQ or CM Staff reopens the LA Detail page | The "Report History" tab reappears, showing the same historical entries as before archiving | Is_Archived__c = FALSE (restored) → tabset region visible again; underlying Student_Sessions__c records unchanged throughout |

**Severity:** minor
**Priority:** medium

---
