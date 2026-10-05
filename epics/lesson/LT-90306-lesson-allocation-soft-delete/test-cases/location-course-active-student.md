# Test Cases: LT-90306 — Lesson Allocation Soft Delete (Archive)

Source Qase suite reviewed: [PX suite 1291 — "Location Course -> Active Student"](https://app.qase.io/project/PX?suite=1291) (8 existing cases). Code trace confirms both `LessonAllocationHandler.getActiveLessonAllocationByLocationCourseId` (Active tab) and `getInactiveLessonAllocationByLocationCourseId` (Inactive tab) filter `Archived_At__c = NULL` — an archived Lesson Allocation is excluded from both tabs entirely, not surfaced anywhere on this page. This is already correct, but had zero regression coverage before this epic — the case below locks it in.

## Suite: Location Course -> Active Student

### Location Course Student List – Lesson Allocation Archived – Student Excluded from Both Active and Inactive Tabs; Restored Student Reappears in Active Tab

**Description:** Regression / control case — Decision Table — a student whose Lesson Allocation has been archived is excluded from both the Active and Inactive tabs of the Location Course student list (not just moved from one tab to the other), and reappears correctly in the Active tab once the Lesson Allocation is restored.

**Preconditions:**
- A Location Course exists with Student A and Student B enrolled, both with active Lesson Allocations (End_Date_Time__c in the future).
- Student A's Lesson Allocation is subsequently archived (Archived_At__c populated) after its Student Package Order was fully removed.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens the Location Course detail and views the Active Student tab | Student B appears in the list | Student B Archived_At__c = blank → included |
| 2 | HQ or CM Staff looks for Student A in the Active Student tab | Student A does not appear | Student A Archived_At__c populated → excluded |
| 3 | HQ or CM Staff switches to the Inactive Student tab | Student A does not appear here either — an archived Lesson Allocation is excluded from both tabs, not reclassified as Inactive | Archived state excluded from both End-Date-based tabs |
| 4 | A living Student Package Order reappears for Student A's Student Course, so the Lesson Allocation is unarchived on the same record Id | Student A's Lesson Allocation shows Archived_At__c blank again | Archived_At__c = null (restored) |
| 5 | HQ or CM Staff reopens the Active Student tab | Student A reappears in the list | Student A Archived_At__c = blank (restored) → included again |

**Severity:** major
**Priority:** high

---

### Location Course – Class Assigned to Student – Lesson Allocation Archived – Student Hidden from Lesson; Restored – Student Shown Again

**Description:** Feature Impact (Class Assignment / Master Queue) — Decision Table — a student assigned to a Class via the Location Course "Active Student" flow (case 10541 baseline) disappears from that Class's lesson Student Sessions once their Lesson Allocation is archived, and reappears on the same record once the Lesson Allocation is restored.

**Preconditions:**
- Student A has an active Lesson Allocation for Math 101 at Location Tokyo HQ.
- HQ or CM Staff has assigned Class A to Student A via the Location Course Active Student page (effective date = today), and a lesson for Class A exists today — Student A currently appears in that lesson's Student Sessions.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens the Class A lesson's Student Sessions section | Student A is listed as an active student | Student A Is_Archived__c = FALSE → shown |
| 2 | The Student Package Order behind Student A's Math 101 Lesson Allocation is fully removed, so the Lesson Allocation is archived | The Lesson Allocation shows Archived_At__c populated; Student A's Class Member (created via the Location Course flow) flips to archived via the same formula | Archived_At__c = current timestamp |
| 3 | HQ or CM Staff reopens the Class A lesson's Student Sessions section | Student A no longer appears in the list | Student A Is_Archived__c = TRUE (via formula) → hidden |
| 4 | A living Student Package Order reappears for Student A's Math 101 Student Course, so the Lesson Allocation is unarchived on the same record Id | The Lesson Allocation shows Archived_At__c blank again | Archived_At__c = null (restored) |
| 5 | HQ or CM Staff reopens the Class A lesson's Student Sessions section | Student A reappears in the list — the same original Student Session and Class Member, not newly created | Student A Is_Archived__c = FALSE (restored) → shown again |

**Severity:** major
**Priority:** high

---

### Location Course – Class Auto-Assign/Auto-Remove – Lesson Allocation Archived – Future Sessions Hidden, Not Deleted (Unlike Cancel Future Class); Restored – All Future Sessions Reappear

**Description:** Feature Impact (Class Assignment / Master Queue) — Decision Table — contrasts the existing "Cancel Future Class" auto-remove behavior (case 10545/10546, which hard-deletes future Student Sessions via `ClassMemberMasterQueueExecutor.removeSessionsByClass`) with archiving the Lesson Allocation: `LessonAllocationSyncService.executeSyncPlan` never calls that cleanup, so future sessions across every lesson instance are only hidden by the `Is_Archived__c` formula, never deleted — and all of them reappear, same records, once the Lesson Allocation is restored.

**Preconditions:**
- Student A has an active Lesson Allocation for Math 101 at Location Tokyo HQ, with Class A assigned (effective date = today, no end date).
- Class A has 3 future lesson instances: 2026-05-21, 2026-05-28, 2026-06-04. Student A currently appears in all 3 as an auto-assigned student (per case 10543's baseline).

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens all 3 future Class A lesson instances and checks Student Sessions | Student A appears in all 3 | Student A Is_Archived__c = FALSE → shown in all 3 |
| 2 | The Student Package Order behind Student A's Math 101 Lesson Allocation is fully removed, so the Lesson Allocation is archived | The Lesson Allocation shows Archived_At__c populated | Archived_At__c = current timestamp |
| 3 | HQ or CM Staff reopens all 3 future Class A lesson instances | Student A no longer appears in any of the 3 — but unlike "Cancel Future Class" (case 10545/10546), no Student Session record is deleted; only the Is_Archived__c formula flips | Student A Is_Archived__c = TRUE (via formula) → hidden in all 3, records preserved |
| 4 | HQ or CM Staff opens Student A's 3 Student Session records directly by their record Ids | All 3 records still exist, unmodified aside from the formula-derived Is_Archived__c | Records preserved for history/restore, no hard delete occurred |
| 5 | A living Student Package Order reappears for Student A's Math 101 Student Course, so the Lesson Allocation is unarchived on the same record Id | The Lesson Allocation shows Archived_At__c blank again | Archived_At__c = null (restored) |
| 6 | HQ or CM Staff reopens all 3 future Class A lesson instances | Student A reappears in all 3 — the same original Student Session records from step 4, not newly created ones | Student A Is_Archived__c = FALSE (restored) → shown again in all 3, same record Ids as before archiving |

**Severity:** major
**Priority:** high

---
