# Lesson Learned — OOP / Partner-Specific Issues

---

## [2026-03-04] Nichibei — Student Sessions Missing LA → Points Not Deducted

**Slack thread:** https://manabie.slack.com/archives/C080P3YK2PJ/p1772620580604049

### Issue
Lessons were assigned to students without a linked LA ID → consumed points not deducted.

**Root cause:**
Nichibei's SPO sync flow was missing improvements that had already been applied to the Core SPO sync. This gap caused LAs to be incorrectly deleted on Slot Update / Duration Update actions, resulting in:
- Lessons with student sessions but **no linked LA** → points not consumed
- In some cases, **LA-assigned lesson itself deleted**

**Data:**
- **145 lessons, 27 students** affected
  - 5 students: points transferred successfully
  - 5 students: insufficient points
  - 16 students: LA deletion was correct (Cancel/Void/Change Course)
  - 1 student: undetermined cause

### Resolution
- Queried lessons with null LA via `Student_Course_Id` → manually restored consumed points
- Added cron job to detect deleted LAs and notify team proactively
- Created Nichibei-specific SPO sync flow to replace Core flow for Slot/Duration Update cases

**Remaining gap:** Cancel Full Order / Void Order / Change Course still have no dedicated handler — LA deletion in these cases is intended but can cause data errors if not handled.

### Lessons Learned / Design Notes
- OOP partners should have their **own sync flow** when business rules differ from Core — shared Core sync risks unintended LA deletion for OOP.
- Any future improvement to the **Core SPO sync must also be applied to the Nichibei sync flow** — treat them as coupled.
- Before deleting an LA via system logic, check if any lessons are still linked → cascade cleanup or block deletion.
- Add monitoring for any flow that deletes financial records (LA, SPO, points).
- Always confirm **full data scope before starting recovery** — mid-recovery findings increase pressure on PS and client.

---
