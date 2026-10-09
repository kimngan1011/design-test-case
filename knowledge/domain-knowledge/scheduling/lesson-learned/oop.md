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

## [2025-09-22] Aver — Lesson Report PDF Shows Homework Weeks in Wrong Order (Sep → Oct)

**Jira:** [LT-86378](https://manabie.atlassian.net/browse/LT-86378) (Closed)
**Slack thread:** https://manabie.slack.com/archives/C037409QQ4S/p1758525884519909

### Issue

In the exported Aver Lesson Report PDF (Report for Teacher / Report for Student), when the homework date range covered 2 consecutive weeks, the later week (e.g. 10/01–10/07) was displayed **before** the earlier week (e.g. 9/24–9/30). The date rows are in the 前回からの宿題 (Previous Week Homework) and 次回までの宿題 (Next Week Homework) tables, column 月日/曜日, one row per day from the day after the lesson to the next lesson date.

**Root cause:**
Not recorded on the ticket. *(Suspected, not confirmed by dev)* The date rows were ordered by their `M/DD` display text rather than by date: `"10/01"` sorts before `"9/24"` as text. This fits the ticket title ("Oct–Dec"): the bug only shows when a 1-digit month (Sep) and a 2-digit month (Oct–Dec) are in the same range. The verification PDFs attached to the ticket (lessons 2025-09-22, 2025-10-05) show the correct order.

### Resolution

- Fixed by dev (assignee: Pham Van Loi); ticket Closed.
- No Qase case covered it until 2026-10-09: the existing export cases (PX-2428/2429/2430, PX-5769/5770/5771) check layout, colors and ratios, but not date order.
- Added Qase **PX-29646** in suite Incident Prevention (2183), linked to LT-86378: Teacher + Student PDF, month boundary (9/30 → 10/01) in both homework tables, and year boundary (12/31 → 1/01).

### Lessons Learned / Design Notes

- **Any list of dates displayed in a report must be sorted by the date value, never by the formatted string.** Formats like `M/DD` (no leading zero, no year) break text sorting at month changes (Sep → Oct) and at the year change (12/31 → 1/01).
- **Test data for date-range features should cross a month boundary and a year boundary**, not stay inside one month. A range inside September (or inside Oct–Dec) does not reproduce this bug.
- Check the order across **page breaks** too — the date rows of one table can span several PDF pages.
- When a production bug is fixed, add a regression case to Qase at the same time; this one stayed uncovered for over a year.

---
