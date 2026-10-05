# Test Cases: LT-90306 — Lesson Allocation Soft Delete (Archive)

Source Qase suite reviewed: [PX suite 1088 — "Student's lesson allocation Dashboard per month"](https://app.qase.io/project/PX?suite=1088) (7 existing cases). Existing cases (9202 "View Monthly Allocation Report", 9221 "View Overall Allocation Report across AY") describe the row-selection filter as "Get all Student's Lesson Allocation which Require Allocation flag = ON" — no case mentions archived state at all.

Code trace: this dashboard is **not Apex-driven** — it is two native Salesforce declarative Reports (`Monthly_Allocation_Report.report-meta.xml` and `Overall_Allocated_Report.report-meta.xml`, report type `Student_Allocation_Report__c`), opened via a thin `@AuraEnabled` lookup (`LessonAllocationHandler.getStudentAllocationReportId`, which only resolves the Report's Id — no filtering logic of its own). Both reports' `<filter>` blocks test only `Lesson_Allocation__r.Require_Allocation__c equals 1` plus the student/month filters — **neither filter block references `Archived_At__c` or `Is_Archived__c` anywhere.** The aggregated metrics themselves (`Has_Lesson_Number__c`, `Has_Attendance__c`, `Is_Reallocated_Session__c`, `Is_Assigned_Session__c`, `Is_Conducted_Session__c`, `Is_Not_Reallocated_Session__c` — all formula fields on `Student_Sessions__c`) also never incorporate `Is_Archived__c` or `Is_Deleted__c`. **This is a confirmed, genuine gap**: unlike every other list/table/related-list already covered in this epic (all of which filter `Archived_At__c`/`Is_Archived__c` consistently), this dashboard was never updated to exclude archived Lesson Allocations — an archived LA's row and all its figures (Lesson Assigned, Lesson Conducted, Remaining Lessons, Execution Ratio, Reallocated Lessons, Total Purchased Slots) continue to display exactly as if the LA were still active.

## Suite: Student's lesson allocation Dashboard per month

### Monthly Allocation Report – Archived Lesson Allocation – Row and All Figures Still Displayed Unchanged

**Description:** Gap case — Decision Table, contrasts with the baseline (case 9202, "View Monthly Allocation Report") — once a Lesson Allocation is archived, it continues to appear as a full row in the Monthly Allocation Report for the selected month, with Lesson Assigned/Lesson Conducted/Remaining Lessons/Execution Ratio/Reallocated Lessons all computed exactly as before archiving, because the report's declarative filter never tests `Archived_At__c`/`Is_Archived__c`.

**Preconditions:**
- Student A has a Lesson Allocation for Course A, Require Allocation = True, with 5 lessons assigned and 3 conducted (with attendance recorded) in the current month — the Monthly Report currently shows this LA's row with Lesson Assigned = 5, Lesson Conducted = 3, Remaining Lessons = 2, Execution Ratio = 60.0%.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens Student A's Contact record, selects "Monthly" from the report menu for the current month, and confirms the Course A row's figures | Course A row shows Lesson Assigned = 5, Lesson Conducted = 3, Remaining Lessons = 2, Execution Ratio = 60.0% | Baseline snapshot before archive |
| 2 | The Student Package Order behind this Lesson Allocation is fully removed, so the Lesson Allocation is archived | The Lesson Allocation shows Archived_At__c populated | Archived_At__c = current timestamp |
| 3 | HQ or CM Staff reopens the Monthly Allocation Report for the same student and month | Course A's row still appears, with the exact same figures as before archiving — the report does not reflect that the underlying package/order was removed | Monthly_Allocation_Report's filter only tests Require_Allocation__c = 1; no Archived_At__c/Is_Archived__c criteria anywhere in the report metadata or its underlying formula fields |

**Severity:** major
**Priority:** medium

---

### Overall Allocation Report – Archived Lesson Allocation – Row and All Totals Still Displayed Unchanged

**Description:** Gap case — Decision Table, contrasts with the baseline (case 9221, "View Overall Allocation Report across AY") — the same gap as the Monthly Report applies to the Overall Report's aggregated-across-duration figures (Total Assigned/Conducted/Reallocated Lessons, Total Purchased Slots): none of them are affected by archiving the Lesson Allocation.

**Preconditions:**
- Student A has a Lesson Allocation for Course A, Require Allocation = True, with Total Assigned Lessons = 20, Total Conducted Lessons = 12, Total Purchased Slots = 24 shown on the Overall Report.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens Student A's Contact record, selects "Overall" from the report menu, and confirms the Course A row's figures | Course A row shows Total Assigned Lessons = 20, Total Conducted Lessons = 12, Total Purchased Slots = 24 | Baseline snapshot before archive |
| 2 | The Student Package Order behind this Lesson Allocation is fully removed, so the Lesson Allocation is archived | The Lesson Allocation shows Archived_At__c populated | Archived_At__c = current timestamp |
| 3 | HQ or CM Staff reopens the Overall Allocation Report for the same student | Course A's row still appears with the exact same totals as before archiving, with no visual indication the Lesson Allocation is no longer active | Overall_Allocated_Report's filter only tests Require_Allocation__c = 1 and End_Date_Time__c >= TODAY; no Archived_At__c/Is_Archived__c criteria anywhere |

**Severity:** major
**Priority:** medium

---
