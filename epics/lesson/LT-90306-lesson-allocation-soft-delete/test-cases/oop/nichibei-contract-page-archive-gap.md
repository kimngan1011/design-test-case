# Test Cases: LT-90306 — Lesson Allocation Soft Delete (Archive)

Source Qase suite reviewed: [PX suite 504 — "Lesson Mobile"](https://app.qase.io/project/PX?suite=504) (9 existing cases, under OOP FEATURES → Nichibei → Point Consumption, parent 372). This is the Learner mobile app's "Contract page," listing a student's Lesson Allocations with purchased slot, end date, remaining points, and product name — almost certainly the screen spec.md's Gap #10 already flags: "Student App's points-consumption screen calls a generic Salesforce proxy (`/lessonAllocation/v2/getPointsConsumption`) whose Apex endpoint was not found... ownership and archive-filter behavior are unverified."

**Business logic (fully specified by the existing 9 cases):** an LA is hidden from the Contract page if it's inactive and outside the configured date range, if its slots are ≤ 0, or if `requiredAllocation = true`; shown otherwise with purchased slot/end date/remaining points/product name; the list updates live after duration/allocation/slots change; visibility is also scoped per-organization on cross-org account switch (Nichibei vs. Renseikai). None of the 9 cases reference `Archived_At__c`/`Is_Archived__c`.

**Code-trace confirmation:** repeated the search from spec's Gap #10 more broadly across all of `erp-salesforce` (every `@RestResource` endpoint repo-wide, grep for `PointsConsumption`/`ContractPage`/`/lessonAllocation/v2/*`) and `school-portal-admin`'s SF proxy map — confirmed this screen's backend is not present in either repo, unrelated to the different, already-archive-aware `BookingLessonHandlerOutSide.cls:638-651` query (that one picks an LA for a new booking; this one lists LAs for display). Cases below are marked [UNVERIFIED] accordingly.

**Scope:** per the same focus agreed for the Point Consumption suites (373/624) — archived LA must not be shown/usable on this screen, and a restored LA must display normally again. The separate, still-open refund-policy question (spec Clarification Question #2) is out of scope here too.

## Suite: Lesson Mobile

### [Nichibei] Contract Page – Archived LA Hidden Even When Every Other Visibility Rule Would Show It

**Description:** AC-5 — Decision Table — [UNVERIFIED]. Contrasts with existing baseline (#16005 "Display LA when slots are greater than 0"). An LA that passes every other documented visibility rule (slots > 0, `requiredAllocation = false`, within the configured date range) must still be hidden from the Contract page if it is archived — archive must override every other condition, not just be one more input alongside them.

**Preconditions:**
- Learner is logged into the Learner app; the Contract page is accessible.
- LA-A: slots = 5, requiredAllocation = false, within the configured date range — passes every existing visibility rule.
- LA-A's `Archived_At__c` is populated (its order group was fully removed).

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Learner navigates to the Contract page | Per AC-5, LA-A should not be displayed, since an archived LA must be excluded from every in-scope read path regardless of its other field values | LA-A Archived_At__c = populated; slots = 5; requiredAllocation = false |
| 2 | Learner checks whether LA-A appears in the list | [UNVERIFIED] Record actual behavior: LA-A correctly hidden (pass), or LA-A still shown because the Contract page's filter doesn't know about `Archived_At__c` (fail — route to the engineering owner once identified for `/lessonAllocation/v2/getPointsConsumption`) | Actual result to be captured against live Nichibei org |

**Severity:** critical
**Priority:** high

---

### [Nichibei] Contract Page – List Updates Live After LA Archives – Previously Visible LA Disappears

**Description:** AC-5 — Regression — [UNVERIFIED]. Extends existing baseline (#16009 "The LA list is updated after updating the duration, required allocation and slots") to include archiving as a trigger for a live list update, consistent with every other field change already confirmed to refresh the list.

**Preconditions:**
- LA-B is currently visible on the Contract page (slots > 0, requiredAllocation = false, within date range).
- Learner has the Contract page open.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | While the Learner has the Contract page open (or reopens it shortly after), HQ or CM Staff archives LA-B by fully removing its order group | LA-B's `Archived_At__c` becomes populated | LA-B Archived_At__c = populated |
| 2 | Learner refreshes or reopens the Contract page | Per AC-5 and the existing live-update pattern, LA-B should no longer appear in the list | [UNVERIFIED] Record actual behavior: LA-B disappears (pass), or LA-B remains visible because archiving isn't one of the recognized update triggers (fail) | Actual result to be captured against live Nichibei org |

**Severity:** major
**Priority:** high

---

### [Nichibei] Contract Page – Unarchive – Restored LA Reappears With Correct Purchased Slot, End Date, Remaining Points, and Product Name

**Description:** AC-3 — Regression — [UNVERIFIED]. Inverse of the hide case above; extends existing baseline (#16008 "Verify contract page displays purchased slot, end date, remaining points, and product name"). Once a living Student Package Order reappears and the LA is unarchived on the same record Id, the Contract page must show it again with the correct field values — restore must work exactly as if the LA had never been archived.

**Preconditions:**
- LA-B was hidden from the Contract page per the archive case above.
- A living Student Package Order reappears for the same `Student_Course_ID__c` group, and LA-B is unarchived on the same record Id (`Archived_At__c` cleared), with purchased slot, end date, remaining points, and product name unchanged from before the archive.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Learner refreshes or reopens the Contract page after LA-B is restored | Per AC-3, LA-B should reappear exactly as a normal, never-archived LA would | LA-B Archived_At__c = null (restored, same Id) |
| 2 | Learner checks the displayed purchased slot, end date, remaining points, and product name for LA-B | [UNVERIFIED] Record actual behavior: all four fields display correctly and match the pre-archive values (pass), or LA-B remains hidden / shows stale or incorrect values (fail — restore is incomplete) | Actual result to be captured against live Nichibei org |

**Severity:** critical
**Priority:** high

---

### [Nichibei] Contract Page – Account Switch – Archived LA Does Not Leak Back In Via a Stale Cached List

**Description:** AC-5 (cross-system) — Regression — [UNVERIFIED]. Extends existing baseline (#29046 "Account Switch – Point Consumption – Nichibei and Renseikai students – Visibility follows organization"), which already confirms org-boundary isolation on account switch. This case adds the archive dimension: switching away from and back to a student must not resurrect an archived LA via a stale client-side cache, even though the org-boundary switch itself works correctly.

**Preconditions:**
- Parent CrossOrg is logged in and linked to Student Nichibei.
- Student Nichibei has LA-C, visible on the Contract page, which then archives (`Archived_At__c` populated) while the parent is viewing a different linked student.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Parent CrossOrg views Student Nichibei's Contract page, confirms LA-C is visible, then switches to a different linked student | LA-C is visible before the switch | LA-C Archived_At__c = null at this point |
| 2 | While viewing the other student, LA-C archives | LA-C's `Archived_At__c` becomes populated | LA-C Archived_At__c = populated |
| 3 | Parent CrossOrg switches back to Student Nichibei and opens the Contract page | [UNVERIFIED] Record actual behavior: LA-C is correctly absent, reflecting its current archived state (pass), or LA-C still appears because the switch restored a stale cached list from step 1 (fail) | Actual result to be captured against live Nichibei org |

**Severity:** minor
**Priority:** medium

---
