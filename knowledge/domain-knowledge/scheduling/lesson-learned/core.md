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
