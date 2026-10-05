# Test Cases: LT-90306 — Lesson Allocation Soft Delete (Archive)

Source Qase suites reviewed: [PX suite 323 — "Change lesson"](https://app.qase.io/project/PX?suite=323) (5 existing cases) and [PX suite 324 — "Remove lesson"](https://app.qase.io/project/PX?suite=324) (3 existing cases). Both buttons live on the same "Student Sessions Related" tab (`tableStudentSessionLessonAllocation` LWC) on the Lesson Allocation Detail page. None of the 8 existing cases test an archived Lesson Allocation.

Code trace: `Lesson_Allocation_New_Record_Page1_Ext.flexipage-meta.xml`'s main tabset region (hosting "Student Sessions Related", "Report History", and "Class history" together) has a visibility rule `{!Record.Is_Archived__c} EQUAL false` — on a **freshly-loaded** page, the entire tabset (including both "Change Lesson" and "Remove Lesson" buttons) disappears for an archived LA, by design (the field's own description confirms this is its intended purpose: gating Lightning App Builder component visibility). So the normal entry point is correctly protected.

The gap is a **stale-page race condition**: if the page is opened while the LA is still active (tabset renders normally) and the LA gets archived afterward (e.g. in another tab/session) without a page refresh, the buttons remain visible and enabled, and the two actions behave very differently once clicked:
- **"Change Lesson"** → `StudentSessionsHandler.assignLessonToStudentSession` does `SELECT ... FROM Student_Sessions__c WHERE Id = :sessionId AND Is_Deleted__c = FALSE AND Is_Archived__c = FALSE` as a single-row assignment — on an archived LA's session this returns zero rows, throwing an unhandled `System.ListException`, surfaced as a raw Apex error.
- **"Remove Lesson"** → `StudentSessionsRepo.findToBeUnassignedStudentSessions` (ONLY_THIS_LESSON branch) queries `WHERE Id IN :studentSessionIds AND Lesson__c = :lessonId AND Is_Deleted__c = FALSE` — **no `Is_Archived__c` filter at all** — so it succeeds and proceeds to clear `Lesson__c`, set `Is_Deleted__c = true`, etc., on an archived LA's session with no archived check anywhere in that path.

## Suite: Change lesson

### Lesson Allocation Archived – Student Sessions Related Tab (and Change Lesson Button) Disappears on Fresh Page Load

**Description:** Regression / control case — Decision Table — opening an archived Lesson Allocation's detail page directly by record Id hides the entire "Student Sessions Related" tabset region (which hosts the "Change Lesson" button, "Remove Lesson" button, "Report History" tab, and "Class history" tab together) — this is a deliberate visibility rule on `Is_Archived__c`, not an accidental gap, and should be locked in with regression coverage.

**Preconditions:**
- Student A's Lesson Allocation for Math 101 has been archived (Archived_At__c populated) after its Student Package Order was fully removed.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens Student A's archived Lesson Allocation detail page directly by record Id | The LA Detail page loads; the Archived_At__c field shows a populated timestamp | Page reachable despite archive, by design |
| 2 | HQ or CM Staff looks for the "Student Sessions Related", "Report History", and "Class history" tabs | None of the three tabs are shown — the entire tabset region is absent from the page | Flexipage tabset visibility rule: {!Record.Is_Archived__c} EQUAL false |

**Severity:** minor
**Priority:** medium

---

### Change Lesson – Stale Page (LA Archived After Load, Before Click) – Unhandled Apex Error Instead of Friendly Validation

**Description:** Gap case — Decision Table — if a staff member has the LA Detail page open (tabset rendered while the LA was still active) and the LA gets archived in the background before they click "Change Lesson", the button remains visible/enabled on the stale page, and clicking it fails with a raw unhandled Apex exception rather than a friendly validation message.

**Preconditions:**
- HQ or CM Staff has Student A's active Lesson Allocation detail page open, with a Standard-type Student Session assigned to a future lesson, visible in the Student Sessions Related tab.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | In a separate session, the Student Package Order behind this Lesson Allocation is fully removed, so the Lesson Allocation is archived | The Lesson Allocation shows Archived_At__c populated | Archived_At__c = current timestamp |
| 2 | HQ or CM Staff (on the original, stale page, without refreshing) clicks "Change Lesson" on the Student Session, selects a different future lesson, and clicks "Add" | The action fails with a raw/unhandled Apex error, not a clear "this Lesson Allocation is archived" message | assignLessonToStudentSession's SOQL (WHERE Id = :sessionId AND Is_Archived__c = FALSE) returns zero rows, throwing an unhandled System.ListException |
| 3 | HQ or CM Staff refreshes the page | The entire Student Sessions Related tabset is now gone (per the regression case above); the session's Lesson__c link is unchanged from before the failed attempt | No partial update occurred; the failed Apex call never reached any DML |

**Severity:** minor
**Priority:** medium

---

## Suite: Remove lesson

### Remove Lesson – Stale Page (LA Archived After Load, Before Click) – Action Silently Succeeds Despite Archived Lesson Allocation

**Description:** Gap case — Decision Table, more severe than the "Change Lesson" crash above — if a staff member has the LA Detail page open and the LA gets archived in the background before they click "Remove Lesson", the button remains visible/enabled, and — unlike "Change Lesson" — the action silently SUCCEEDS: `StudentSessionsRepo.findToBeUnassignedStudentSessions`'s ONLY_THIS_LESSON query has no `Is_Archived__c` filter at all, so the session is found and unassigned (Lesson__c cleared, Is_Deleted__c set true) with no archived-state check anywhere in that path — a real mutation against an already-archived Lesson Allocation's data.

**Preconditions:**
- HQ or CM Staff has Student A's active Lesson Allocation detail page open, with a Standard-type Student Session assigned to a future lesson, visible in the Student Sessions Related tab.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | In a separate session, the Student Package Order behind this Lesson Allocation is fully removed, so the Lesson Allocation is archived | The Lesson Allocation shows Archived_At__c populated | Archived_At__c = current timestamp |
| 2 | HQ or CM Staff (on the original, stale page, without refreshing) clicks "Remove Lesson" on the Student Session and confirms | The action completes with no error — the session's Lesson__c link is cleared and Is_Deleted__c is set to true, exactly as it would for a non-archived LA | findToBeUnassignedStudentSessions (ONLY_THIS_LESSON) has no Is_Archived__c filter → session found and mutated despite the LA being archived |
| 3 | HQ or CM Staff opens the Student Session record directly by record Id | Lesson__c is blank and Is_Deleted__c = true, permanently recording a data change against an archived Lesson Allocation that staff could no longer normally reach via the UI | Mutation succeeded with no archived-state guard anywhere in this code path |

**Severity:** major
**Priority:** medium

---
