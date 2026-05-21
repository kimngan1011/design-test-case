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
