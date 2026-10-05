# Test Cases: LT-90306 — Lesson Allocation Soft Delete (Archive)

Source Qase suite reviewed: [PX suite 1275 — "BO Reallocate student"](https://app.qase.io/project/PX?suite=1275) (7 existing cases, under "Reallocation" / LT-85058, OOP FEATURES → Nichibei, parent 371). This suite re-tests the same Reallocate flag/unflag and auto-delete rules from the Teacher/BO Collect Attendance entry point, always confirming state via a corresponding SF check (e.g. "Login SF and check Reallocate list and LA detail"). It shares the identical underlying cleanup mechanism already traced and confirmed as a new gap in `nichibei-reallocation-sf-archive-gap.md` (suite 1274) — the code trace is not repeated here. None of the 7 cases reference `Archived_At__c`/`Is_Archived__c`.

**Scope:** since this suite doesn't include its own "Reallocate Lesson" picker (that's SF-only, suite 1274), coverage here is narrower — confirming the orphaned-request behavior is observable (and no worse) from the BO entry point too, and that restore resumes normal behavior from BO as well.

## Suite: BO Reallocate student

### [Nichibei] BO Reallocate – LA Archives With an Open Request – Teacher on BO Still Sees Reallocate Flag Enabled for an Archived Student

**Description:** AC-1 / Gap (Business Rule #10) — Decision Table. Contrasts with existing baseline (#10411 "Update the Reallocate flag with no linked lesson on BO" — confirms the flag and SF list entry disappear together once properly cleared through the legacy hard-delete path). Since the cleanup never fires under archive (per the code trace in suite 1274's file), the Reallocate flag remains visibly enabled on BO's Collect Attendance page for a student whose Lesson Allocation has since archived.

**Preconditions:**
- Teacher has access to Back Office. Student A's Student Session on Lesson A is marked Absent with Reallocate flag enabled (matches an open `Reallocation__c` request).
- The Student Package Order group behind Student A's Lesson Allocation is fully removed, archiving the Lesson Allocation.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Teacher opens Collect Attendance for Lesson A on BO | Per AC-5, an archived student should not appear as an actionable roster entry at all — but confirm whether Student A (and their enabled Reallocate flag) still appears, consistent with the SF-side list also failing to exclude them | LA Archived_At__c = populated |
| 2 | Teacher checks whether the Reallocate flag is still shown as enabled for Student A | [UNVERIFIED] Record actual behavior: flag still shown enabled (consistent with the confirmed SF-side gap — route to the same engineering owner), or Student A is correctly excluded from the roster entirely (pass, would mean BO's own query is independently archive-aware even though SF's list isn't) | Actual result to be captured against live Nichibei org |

**Severity:** major
**Priority:** high

---

### [Nichibei] BO Reallocate – Unarchive – Normal Unflag Behavior Resumes From BO

**Description:** AC-3 — Regression. Confirms that once the Lesson Allocation is restored, Teacher can unflag the Reallocate status from BO exactly as in the pre-archive baseline (#10411), and the change is reflected correctly back on the SF Reallocation list.

**Preconditions:**
- Student A's open Reallocate request survived an LA archive per the case above.
- A living Student Package Order reappears for the same `Student_Course_ID__c` group, and the Lesson Allocation is unarchived on the same record Id.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Teacher opens Collect Attendance for Lesson A on BO after the restore and updates Student A's attendance status to Attend | Per the normal (non-archived) cleanup rule, the Reallocate checkbox auto-unchecks and disables | Archived_At__c = null (restored) |
| 2 | HQ or CM Staff logs into SF and checks the Reallocation list and the Lesson Allocation detail | The request no longer appears in the Reallocation list, and no Reallocate student session remains in the Lesson Allocation detail — matching baseline #10411's behavior exactly, confirming the cleanup mechanism works again post-restore | Reallocation__c record removed/updated per normal behavior |

**Severity:** minor
**Priority:** medium

---
