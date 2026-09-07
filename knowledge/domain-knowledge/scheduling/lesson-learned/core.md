# Lesson Learned — Core Domain Issues

---

## [2026-04-13] Aso — Duplicate Student Sessions from Manual Assign + Auto Assign

**Slack thread:** https://manabie.slack.com/archives/C037409QQ4S/p1775610509175129

### Issue
Students were assigned to the same lesson multiple times, resulting in duplicate student session records.

**Root cause:**
A staff member performed **2 actions that both created student sessions for the same group of students**:
1. Used **"Add Student Sessions by Bulk"** (manual assignment)
2. Then **Imported Class Members** → system automatically auto-assigned student sessions

Both flows created student session records independently, generating **1,655 duplicate records** on 2026-04-07.

**Data:**
- Manually created by staff: 4,561 student sessions
- Auto-assigned by system: 35,522 student sessions
- Duplicates: **1,655**

### Resolution
- Deleted the **manually assigned** student sessions, kept the **auto-assigned** ones
- Total deleted: **1,809 records** (1,655 on 2026-04-07 + 154 on the day of resolution)

### Lessons Learned / Design Notes
- When **2 flows can both create student sessions** (bulk manual + auto-assign from class import), implement a **deduplication or duplicate-prevention** mechanism at the business logic layer.
- Check for existence before inserting a student session: if a session already exists for the same `(student, lesson)` pair, skip creation.
- Consider a **UI warning** when staff manually assigns a student who already has a session from auto-assign.

---

## [2026-06-18] Aso — Duplicate Students on Lesson Copy Due to Missing `Unique_Key__c` Backfill

**Slack thread:** https://manabie.slack.com/archives/C037409QQ4S/p1781748589810049

### Issue

After copying lessons in Aso Prod, students were found assigned twice to the same lesson. The bug was introduced by the June 15 release of the auto-assign-by-class-member flow.

**Root cause:**
1. The auto-assign flow uses `Unique_Key__c` (a composite key of Lesson ID + Student ID) to detect and skip duplicate enrollments.
2. Old student session records created before `Unique_Key__c` was introduced did not have this field populated.
3. When the auto-assign flow processed these legacy records, it could not detect the existing enrollment and inserted duplicate student sessions.

### Resolution

- Removed the duplicate student session records created on or after the June 15 release (Aso Prod data fix).
- Ran a backfill migration to populate `Unique_Key__c` on all legacy student session records across all partners (tracked in LT-104284).
- Reverted lesson surveys (lesson inquiries) that were inadvertently deleted when the duplicate enrollments were cleaned up.

### Lessons Learned / Design Notes

- When introducing a new deduplication key field, **backfill it for all existing records in the same release** — never assume old data has the field populated.
- The auto-assign flow should use a raw `(lesson_id, student_id)` existence check as a **fallback deduplication guard** for records where the composite key is missing, rather than relying solely on `Unique_Key__c`.
- Before running any data-cleanup script, **audit cascading dependencies** (e.g., lesson surveys, submissions) linked to the records being deleted to avoid unintended data loss.
- When a fix removes records across partners, ensure the migration scope covers **all partners**, not just the one that reported the issue.

---

## [2026-08-18] Renseikai — Published Lesson Missing Student Sessions Due to Salesforce 10,000-Record Bulk Write Limit

**Slack thread:** https://manabie.slack.com/archives/C02B6RYSD7A/p1787034274581849

### Issue

A bulk lesson-generation import (~1,300 lesson schedules across ~1,200 classes) created the lessons successfully, but the follow-up step that queues students for auto-assignment silently failed for one batch, leaving Published Lessons with zero Student Sessions despite having active Class Members. This blocked attendance tracking.

**Root cause:**
1. Lesson generation ran in batches; one batch processed 1,000 schedules and, at its last step, looked up every student enrolled across the corresponding ~1,200 classes (~9,000 students) to queue auto-assign rows.
2. That single operation attempted to write ~9,000 auto-assign queue rows plus 1,000 schedule rows = 10,001 records in one call, exceeding Salesforce's hard limit of 10,000 records per single write operation.
3. The write was rejected, but lesson creation (an earlier, already-committed step) was unaffected — so lessons existed with no student sessions, and the failure was not surfaced as an error to the importer.

**Data:**

- ~1,300 lesson schedules / ~1,200 classes in the source import
- 1,000 schedules processed in the failing batch
- ~9,000 students queued for auto-assign in that batch
- 10,001 total records attempted vs. Salesforce's 10,000-record-per-operation limit

### Resolution

- Reproduced the failure on preprod to confirm root cause.
- Re-ran auto-assign for all class members that were missed — a data fix only, no re-import needed.
- Follow-up work planned to improve the performance/batching of the auto-assign queueing step.

### Lessons Learned / Design Notes

- Any batch operation that writes to Salesforce must chunk its payload to stay under the 10,000-record-per-operation limit — size the chunk dynamically off the number of students to queue, not just the number of schedules/lessons, since the queue step scales with class enrollment.
- A step that depends on an earlier step's success (auto-assign depending on lesson creation) should fail loudly and be retryable/idempotent rather than leaving lessons in a partially-processed state with no student sessions and no visible error.
- Add monitoring/alerting for "lesson exists but has zero Student Sessions despite active Class Members" as a detectable data-integrity signal, so partial failures like this surface before a partner reports missing attendance tracking.

---

## [2026-08-19] Renseikai — Manually-Assigned Student Sessions Auto-Removed by Class-Assignment Re-Scan Logic

**Slack thread:** https://manabie.slack.com/archives/C02B6RYSD7A/p1787111883369399

### Issue

83 Student Sessions across 12 school-specific lessons were unexpectedly deleted between 18–19 Aug 2026, blocking attendance management. The lessons themselves remained active; only the student assignments were removed.

**Root cause:**
1. When a Lesson Allocation (LA) class member's duration is updated — or a class is added/removed on an overlapping lesson — the system triggers a re-auto-assign that re-scans not just which lessons to *assign*, but also which existing student sessions should be *removed*, treating them as "invalid" if they no longer match current class-assignment rules.
2. The re-scan does not distinguish sessions that were manually assigned by staff from ones the system auto-assigned, so manual assignments get swept up in the same cleanup.
3. Two distinct deletion patterns occurred from the same re-scan run:
   - Manually-assigned sessions in a lesson group **without a class** that falls within the class member's duration → incorrectly treated as invalid and removed (this is the actual bug).
   - Manually-assigned sessions in a lesson group **with a class**, where the lesson's class doesn't match the class member's duration → removed as well, but this is **correct** per the existing auto-assign design (confirmed with the partner, not reverted).

**Data:**

- 83 Student Sessions deleted across 12 lessons total (35 on 19 Aug, 48 on 23 Aug) as originally reported
- 916 records deleted from lesson groups without a class (Type 1 — the bug)
- 3,333 records deleted from lesson groups with a mismatched class (Type 2 — correct/intended behavior)

### Resolution

- Reverted the 916 Type-1 records (manually assigned sessions in class-less lesson groups).
- Did not revert the 3,333 Type-2 records — confirmed by the requester as expected auto-assign behavior.
- Filed bug ticket [LT-109020](https://manabie.atlassian.net/browse/LT-109020) — "[SF] Auto-remove assigned student from the group lesson without class when triggering class assignment flow" — for the Type-1 bug.
- An existing improvement ticket, [LT-107584](https://manabie.atlassian.net/browse/LT-107584), already planned for the Sep release, will exclude intentional manual assignments from the system's re-scan/removal logic more broadly.

### Lessons Learned / Design Notes

- The auto-assign re-scan/cleanup logic must distinguish manually-assigned student sessions from auto-assigned ones before removing "invalid" lessons — a manual assignment reflects explicit staff intent and shouldn't be silently deleted by a background re-scan.
- Any update to a class member's duration, or adding/removing a class on an overlapping lesson, can silently trigger this re-scan and delete existing student sessions — this side effect is not obvious from the triggering action and should be called out (and ideally require confirmation) wherever such updates are made.
- Even where auto-removal is by-design (class-mismatch case), deletions are user-visible and partner-impacting — communicate the behavior to partners proactively rather than only after an incident is raised.

---
