# Test Cases: LT-90306 — Lesson Allocation Soft Delete (Archive)

**No code found in either repo.** Source Qase case reviewed: [PX case #22551 — "[EEA] OOP | Custom Student Session Table in Lesson Detail"](https://app.qase.io/project/PX?suite=1424) (LT-101751, OOP FEATURES → EEA, parent 311). This is exactly spec.md's already-ticketed gap: "EEA's custom `Student_Sessions__c` table lives outside the package; package filters don't reach it. Ticket: `[SF][EEA] Check custom Student Session table` — 1d." Columns: Student Name, Grade, Type, Attendance Response, Attendance Status, Attendance Reason, Reallocate Flag.

**Code-trace result: not found in either repo.** Exhaustive search for "EEA" (case-insensitive) and for the specific column combination ("Attendance Reason" + "Reallocate") across `erp-salesforce` (`outside-packages/`, `outside-packages-ext/`) and `school-portal-admin` found nothing EEA-specific — every hit was a false-positive substring match. The named fields exist only as standard package fields consumed by standard Core LWCs. This is the same category as Aver's Lesson Report and Nichibei's priority-chain class: it exists live on EEA's org but is not checked into either repo this workspace has access to.

**Grounding used instead of code:** the single existing case's own field list, plus the AC-5/AC-3 principles already proven throughout this epic for every other custom/outside-package table.

## Suite: EEA

### [EEA] Custom Student Session Table – Archived Session Excluded From Lesson Detail

**Description:** AC-5 — Decision Table — [UNVERIFIED]. Contrasts with existing baseline (#22551, which only documents the required fields, no archive dimension). Mirrors the AC-5 exclusion principle already proven for every other Student Session list/table in this epic (Core and OOP alike): a student whose Lesson Allocation has archived should not appear in this custom table.

**Preconditions:**
- HQ or CM Staff is on the EEA Salesforce org, viewing a Lesson's detail page with the custom Student Session table.
- Student A (active Lesson Allocation) and Student B (active Lesson Allocation) both currently appear in the table, with their Attendance Response, Attendance Status, Attendance Reason, and Reallocate Flag populated.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff confirms both Student A and Student B appear in the custom table | Both rows visible with all 7 required fields | Both sessions Is_Archived__c = FALSE |
| 2 | The Student Package Order group behind Student A's Lesson Allocation is fully removed, so the Lesson Allocation is archived | Student A's Student Session becomes Is_Archived__c = TRUE via formula | Archived_At__c = current timestamp |
| 3 | HQ or CM Staff reopens the Lesson's detail page | [UNVERIFIED] Record actual behavior: Student A no longer appears in the custom table, Student B unaffected (pass), or Student A still appears as if active (fail — route to the engineering owner of `[SF][EEA] Check custom Student Session table`) | Actual result to be captured against the live EEA org |

**Severity:** major
**Priority:** high

---

### [EEA] Custom Student Session Table – Restore – Row Reappears With Correct Field Values

**Description:** AC-3 — Regression — [UNVERIFIED]. Confirms that once a living Student Package Order reappears and the Lesson Allocation is unarchived on the same record Id, the custom table shows the student's row again with all fields intact — matching the restore-correctness principle already proven across this entire epic.

**Preconditions:**
- Student A's row was hidden from the custom table per the case above.
- A living Student Package Order reappears for Student A's Student Course, and the Lesson Allocation is unarchived on the same record Id, with Attendance Response/Status/Reason and Reallocate Flag unchanged from before the archive.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff confirms the Lesson Allocation is restored (`Archived_At__c` cleared, same Id) | — | Archived_At__c = null (restored) |
| 2 | HQ or CM Staff reopens the Lesson's detail page | [UNVERIFIED] Record actual behavior: Student A's row reappears with all fields matching the pre-archive values (pass), or the row remains missing / shows stale data (fail) | Actual result to be captured against the live EEA org |

**Severity:** minor
**Priority:** medium

---
