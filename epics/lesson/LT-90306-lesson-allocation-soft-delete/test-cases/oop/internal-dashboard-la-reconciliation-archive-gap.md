# Test Cases: LT-90306 — Lesson Allocation Soft Delete (Archive)

**No existing Qase suite found for this tool** — it surfaced during a proactive sweep of Nichibei's `outside-packages/` code, prompted by a request to verify whether Core-covered surfaces (Add Student popup, Calendar student list, Lesson Allocation tab list views) are shared or forked for OOP tenants. Those three surfaces turned out to be fully shared with Core (control case below for the newly-confirmed second Add-Student code path); while tracing them, a separate, unrelated `outside-packages/dlrs` tool was flagged and is covered here instead, since it's a genuine new finding.

**`InternalDashboardSearchHandler.cls`** (LWC `intDashLessonAllocationSearch.js`) is an ops/support reconciliation dashboard: staff enter an Order Group Id, Student (Contact) Id, Student Package Order Id, Manabie SPO Id, or Lesson Allocation Id; it resolves to the Student Course(s) and reports whether a Lesson Allocation exists, flagging "needs attention" rows (deleted SPO, still processing, never synced) to spot sync gaps between backend SPOs and Salesforce. This tool is shared `dlrs` infrastructure — not confirmed Nichibei-exclusive, but found via this sweep and included under the OOP folder for now pending confirmation of its actual suite placement in Qase.

**Code-trace confirmation:** both of its `Lesson_Allocation__c` queries — `resolveByLessonAllocationId` (`cls:393-397`) and `getLessonAllocations` (`cls:633-653`, the main lookup behind `buildRows`) — have **no `Archived_At__c` filter at all**, even though that field is actively used for filtering elsewhere in the same file family (`BookingLessonHandlerOutSide.cls:307,570,648,904`), confirming its absence here is a real gap, not a nonexistent field.

## Suite: Internal Dashboard — LA Reconciliation (new suite, not yet in Qase)

### [Cross-Tenant] Internal Dashboard – LA Reconciliation Search – Archived LA Not Distinguished From an Active One

**Description:** AC-5 — Negative — [UNVERIFIED]. The reconciliation dashboard's Lesson Allocation lookup has no archive awareness: an archived LA (a deliberate, correct state introduced by this epic) is indistinguishable from an active one in the tool's output, risking staff misreading a correctly-archived record as a genuine sync anomaly needing manual intervention.

**Preconditions:**
- Ops/support staff has access to the Internal Dashboard LA reconciliation tool.
- Student A's Lesson Allocation for Course A is archived (`Archived_At__c` populated, via its order group being fully removed) — a correct, expected state per this epic's design.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Staff searches the dashboard using Student A's Student (Contact) Id or the archived Lesson Allocation's Id | The tool resolves to Student A's Student Course and reports on the Lesson Allocation it finds | LA Archived_At__c = populated |
| 2 | Staff reviews the row's status/flag | [UNVERIFIED] Record actual behavior: the row is shown as a normal, healthy Lesson Allocation entry with no indication it is archived (fail — staff cannot distinguish "correctly archived" from "actually missing/broken," defeating the tool's diagnostic purpose) | No `Archived_At__c` field surfaced anywhere in `getLessonAllocations`'s query or output columns |

**Severity:** major
**Priority:** high

---

### [Cross-Tenant] Internal Dashboard – LA Reconciliation Search – Archived LA's Underlying Gap Could Be Masked as "Found"

**Description:** AC-5 — Negative — [UNVERIFIED]. Inverse risk of the case above: if a genuinely broken sync (e.g. a backend SPO exists but no Lesson Allocation was ever created) happens to coincide with an unrelated archived LA for the same student/course being returned by the unfiltered query, staff could be misled into believing "a Lesson Allocation was found" (masking the real gap) when the only match is an archived, inactive record that shouldn't count as evidence of a healthy sync.

**Preconditions:**
- Student B has a backend Student Package Order with no corresponding active Lesson Allocation (a genuine sync gap).
- Student B separately has an unrelated, already-archived Lesson Allocation for a different, past enrollment under the same Student Course grouping.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Ops staff searches the dashboard for Student B to diagnose a reported sync issue | Per the tool's purpose, it should clearly flag that no *active* Lesson Allocation exists for the current enrollment, distinct from the unrelated archived one | Backend SPO exists; only archived LA found |
| 2 | Staff reviews the search result | [UNVERIFIED] Record actual behavior: the unfiltered query returns the archived LA as if it were a valid match, potentially causing staff to close the investigation prematurely believing the sync is healthy (fail), or the tool already distinguishes this correctly some other way not yet identified (pass) | Actual result to be captured; `getLessonAllocations` has no `Archived_At__c` filter to exclude this row |

**Severity:** minor
**Priority:** medium

---
