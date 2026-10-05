# Test Cases: LT-90306 — Lesson Allocation Soft Delete (Archive)

**No existing Qase suite or code reference found.** "Point Management" is Nichibei's screen for Lesson Allocations where `Require_Allocation__c = False` (point-based/consumable allocations) — the direct counterpart to Core's "Lesson Allocation tab," whose 8 declarative list views are exhaustively `Require_Allocation__c = True` only (see `lesson-allocation-tab-list-views-archive.md` and the control-case verification in `nichibei-add-student-calendar-la-tab-control.md`).

**Code-trace result: not found anywhere in either repo.** Exhaustive search (grep for "point management"/"Point_Management"/"ポイント管理" across `erp-salesforce` packages/outside-packages and `school-portal-admin`; search for any tab/LWC/Visualforce/FlexiPage named with "point"; relaxed search for any `Require_Allocation__c = False` listing query or list view under any name) found nothing. This is an org-specific Nichibei customization not checked into either repo — the same category as Aver's Experience Cloud Lesson Report page and Nichibei's external `StudentSessionHandlerOutSide` priority-chain class, both already confirmed unverifiable-by-code elsewhere in this effort.

**Grounding used instead of code:** the fields/business shape of `Require_Allocation__c = False` LAs are already well-established from the Point Consumption suites already covered (373/624/504) — Purchase Point, Priority flag, Duration, General-course flag, remaining points. Test cases below apply the same AC-5/AC-3 principle already proven for the Required-Allocation counterpart, explicitly marked [UNVERIFIED] since no code or existing Qase case confirms actual behavior here.

## Suite: [Nichibei] Point Management (no known Qase suite — new area)

### [Nichibei] Point Management – Archived LA (Require Allocation = False) Excluded From the List

**Description:** AC-5 — Decision Table — [UNVERIFIED]. Mirrors the already-confirmed-safe Required-Allocation counterpart (`lesson-allocation-tab-list-views-archive.md`): once a Require_Allocation = False Lesson Allocation archives, it should no longer appear in Point Management, consistent with every other LA-listing surface in this epic.

**Preconditions:**
- HQ or CM Staff has access to the Nichibei Point Management screen.
- Student A has a Lesson Allocation with Require Allocation = False, Priority = True, Purchase Point = 10, currently visible in Point Management.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens Point Management and confirms Student A's Lesson Allocation is listed, showing Purchase Point = 10 and Priority = True | The LA is visible with its correct fields | Archived_At__c = blank → included |
| 2 | The Student Package Order group behind this Lesson Allocation is fully removed, so the Lesson Allocation is archived | The Lesson Allocation shows Archived_At__c populated | Archived_At__c = current timestamp |
| 3 | HQ or CM Staff reopens Point Management | [UNVERIFIED] Record actual behavior: the LA is no longer listed (pass, consistent with AC-5 and every other LA-listing surface already confirmed in this epic), or the LA remains visible as if still active (fail — a genuinely new gap, since this screen has no code or prior test coverage to have ever caught it) | Actual result to be captured against the live Nichibei org |

**Severity:** major
**Priority:** high

---

### [Nichibei] Point Management – Restore – LA Reappears With Correct Point/Priority/Duration Fields

**Description:** AC-3 — Regression — [UNVERIFIED]. Once a living Student Package Order reappears and the Lesson Allocation is unarchived on the same record Id, Point Management should show it again with its fields intact, matching the same restore-correctness principle already verified for the Required-Allocation tab, Contract Page, and Point Consumption priority chain elsewhere in this epic.

**Preconditions:**
- Student A's Lesson Allocation (Require Allocation = False, Priority = True, Purchase Point = 10) was hidden from Point Management per the case above.
- A living Student Package Order reappears for the same `Student_Course_ID__c` group, and the Lesson Allocation is unarchived on the same record Id, with its fields unchanged from before the archive.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff confirms the Lesson Allocation is restored (`Archived_At__c` cleared, same Id) | — | Archived_At__c = null (restored) |
| 2 | HQ or CM Staff reopens Point Management | [UNVERIFIED] Record actual behavior: the LA reappears with Purchase Point = 10, Priority = True, and its original duration unchanged (pass), or it remains missing / shows stale or incorrect values (fail — restore is incomplete on this screen) | Actual result to be captured against the live Nichibei org |

**Severity:** minor
**Priority:** medium

---
