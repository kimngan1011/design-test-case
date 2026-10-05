# Test Cases: LT-90306 — Lesson Allocation Soft Delete (Archive)

Source Qase suite reviewed: [PX suite 1293 — "Lesson Allocation Detail"](https://app.qase.io/project/PX?suite=1293) (15 existing cases). None test the LA Detail page's behavior when the Lesson Allocation itself is archived.

Code trace: `tableStudentCourseSubscription.js` (the LWC backing this page) sets `isDisableAssignClass = true` only when `MANAERP__Type__c.includes("Trial")` — there is no equivalent check for `Archived_At__c`. Since an archived Lesson Allocation remains reachable by record Id (per the Confluence spec's own "Still reachable" note), staff can open an archived LA's detail page and use "Assign Class" exactly as if it were active.

## Suite: Lesson Allocation Detail

### LA Detail – Archived Lesson Allocation – Assign Class Button Not Disabled – New Class Member Created but Immediately Hidden

**Description:** Feature Impact (LA authorization & Add Student) — Decision Table — the "Assign Class" button on the LA Detail page is not disabled for an archived Lesson Allocation (unlike the existing Trial-LA guard), so staff can complete an assignment that produces a Class Member hidden the instant it's created, with no warning that the LA is archived.

**Preconditions:**
- Student A's Lesson Allocation for Math 101 has been archived (Archived_At__c populated) after its Student Package Order was fully removed.
- Class A exists for Math 101 at Location Tokyo HQ. Student A currently has no class assigned.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens Student A's archived Lesson Allocation detail page directly by record Id | The LA Detail page loads; the Archived_At__c field shows a populated timestamp | Page reachable despite archive, by design |
| 2 | HQ or CM Staff clicks "Assign Class" on this archived LA | The Assign Class dialog opens normally — the button is not disabled or hidden, unlike the existing Trial-LA guard (suite 290, case 6024) | isDisableAssignClass is only set for Type__c = Trial, never for Archived_At__c populated |
| 3 | HQ or CM Staff selects Class A, sets Effective Date = today, and saves | The dialog closes with no error; a new Class Member record is created for Student A on Class A | New Class_Member__c created, tied to the archived LA |
| 4 | HQ or CM Staff refreshes the LA Detail page's Class Assignment section | Class A does NOT appear as an active class, even though it was just "successfully" assigned — the new Class Member's Is_Archived__c formula already reads TRUE from the parent LA | Student A's Class Member Is_Archived__c = TRUE immediately, reflecting the current archived LA state rather than the moment of creation |

**Severity:** major
**Priority:** medium

---

### LA Detail – Scheduled Class on Archived Lesson Allocation – Effective Date Reached – Class Member Does Not Activate; Not Synced to BO

**Description:** Feature Impact (Class Assignment / Master Queue) — Decision Table — contrasts with the non-archived baseline (case 25398, "Scheduled Class to Active - Sync to BO"): a Scheduled (future-dated) Class Member retained under an archived Lesson Allocation does not become active when its effective date arrives, because `Is_Archived__c` is a pure formula on the parent LA's `Archived_At__c` and is completely independent of the effective-date comparison — the archived state overrides date-based activation everywhere, including the BO sync.

**Preconditions:**
- Student A has a Lesson Allocation for Math 101 with a Scheduled Class A membership, Effective_Start_Date_Time__c = 2026-05-21 (not yet active; today = 2026-05-20).
- Before the effective date arrives, Student A's Lesson Allocation is archived (Archived_At__c populated) after its Student Package Order was fully removed.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens Student A's LA Detail page on 2026-05-20 (before the effective date) | Class A is shown as scheduled/future, not yet active | Class A Effective_Start_Date_Time__c = 2026-05-21 (future); LA Archived_At__c populated |
| 2 | Today advances to 2026-05-21, the Class A effective date | — | today = 2026-05-21 |
| 3 | HQ or CM Staff refreshes the LA Detail page's Class Assignment section | Class A does NOT become active — it remains excluded, since Is_Archived__c still reads TRUE from the archived parent LA regardless of the effective date passing | Student A Class Member Is_Archived__c = TRUE (LA still archived) → not treated as active despite the date being reached |
| 4 | HQ or CM Staff logs in to BO and navigates to Student A's Student Detail → Courses tab | Class A does NOT appear as Student A's active class on BO | Class A not synced to BO; archived state suppresses the activation |

**Severity:** major
**Priority:** high

---

### LA Detail – Scheduled Class on Restored Lesson Allocation – Effective Date Reached – Class Member Activates Normally; Synced to BO

**Description:** Feature Impact (Class Assignment / Master Queue), control case — Decision Table — once the Lesson Allocation is restored before the Scheduled Class Member's effective date arrives, the class activates and syncs to BO exactly like the never-archived baseline (case 25398), confirming the archive → restore cycle has no lingering effect on date-based activation.

**Preconditions:**
- Student A has an archived Lesson Allocation for Math 101 with a retained Scheduled Class A membership, Effective_Start_Date_Time__c = 2026-05-21 — currently excluded everywhere (today = 2026-05-20, before the effective date).
- A living Student Package Order reappears for Student A's Math 101 Student Course, so the Lesson Allocation is unarchived on the same record Id, before the effective date arrives.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens Student A's LA Detail page on 2026-05-20, after the restore | Class A is shown as scheduled/future, consistent with a normal (never-archived) scheduled class | Student A Class Member Is_Archived__c = FALSE (restored); Effective_Start_Date_Time__c = 2026-05-21 still future |
| 2 | Today advances to 2026-05-21, the Class A effective date | — | today = 2026-05-21 |
| 3 | HQ or CM Staff refreshes the LA Detail page's Class Assignment section | Class A is now shown as the active class, exactly like the non-archived baseline (case 25398) | Class A Effective_Start_Date_Time__c <= today, Is_Archived__c = FALSE → active |
| 4 | HQ or CM Staff logs in to BO and navigates to Student A's Student Detail → Courses tab | Class A appears as Student A's active class on BO, with start date = 2026-05-21 | Class A correctly synced to BO, consistent with case 25398 |

**Severity:** major
**Priority:** high

---

### LA Detail – "Lesson Allocated" Count Unaffected by Archive or Restore – Same Value Displayed Throughout

**Description:** Regression / control case — Decision Table — `Lesson_Allocation__c.Lesson_Allocated__c` ("x/y" display) is a formula built from two roll-up summaries, `Allocated_Sessions__c` (`Assigned_Lesson__c = True AND Is_Deleted__c = False`) and `Total_Sessions__c` (no filter) — neither roll-up has an `Is_Archived__c` filter condition. Since every direct `Student_Sessions__c` child of a given Lesson Allocation shares that LA's own archived state (the formula is `NOT(ISBLANK(Lesson_Allocation__r.Archived_At__c))` of that same parent), archiving an LA cannot partially affect its own roll-up — the "x/y" count is computed identically before archiving, while archived, and after restore. This is a different counting definition than `LessonAllocationHandler.getAssignedSessionCountByLessonAllocationId` (used for order-cancellation eligibility, which does filter `Is_Archived__c = FALSE`), but since both definitions are scoped to one LA's own children, they can't diverge due to archive state either. This case locks in that staff navigating directly to an archived LA's detail page (already confirmed reachable, case above) sees the exact same "Lesson Allocated" value as before the LA was archived — not reset, not recalculated to 0/y.

**Preconditions:**
- Student A's Lesson Allocation for Math 101 shows "Lesson Allocated" = "5/10" (5 of 10 total sessions assigned to lessons).

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens Student A's LA Detail page and records the "Lesson Allocated" value | "Lesson Allocated" shows "5/10" | Allocated_Sessions__c = 5, Total_Sessions__c = 10 |
| 2 | The Student Package Order behind Student A's Lesson Allocation is fully removed, so the Lesson Allocation is archived | The Lesson Allocation shows Archived_At__c populated | Archived_At__c = current timestamp |
| 3 | HQ or CM Staff opens the same archived LA Detail page directly by record Id | "Lesson Allocated" still shows "5/10", unchanged — the roll-up has no Is_Archived__c filter, and even if it did, all 10 sessions share the same now-archived state as their parent LA, so the ratio cannot shift | Allocated_Sessions__c and Total_Sessions__c unchanged; both roll-ups are scoped to this LA's own children only |
| 4 | A living Student Package Order reappears for Student A's Math 101 Student Course, so the Lesson Allocation is unarchived on the same record Id, and HQ or CM Staff reopens the LA Detail page | "Lesson Allocated" still shows "5/10", unchanged | Archived_At__c = null (restored); Allocated_Sessions__c and Total_Sessions__c unchanged throughout the entire archive/restore cycle |

**Severity:** minor
**Priority:** low

---
