# Test Cases: LT-90306 — Lesson Allocation Soft Delete (Archive)

Source Qase suite reviewed: [PX suite 1090 — "Lesson Point Consumption tracking"](https://app.qase.io/project/PX?suite=1090) (6 existing cases, under "SF Report" → "OTHERS", not tenant-specific). Shows per student: all Lesson Allocations, Course Name, Total Purchased Points, Remaining Points, and per-row Lesson Date + Consumed Points. None of the 6 cases reference `Archived_At__c`/`Is_Archived__c`.

**Code-trace confirmation.** Not custom code — a declarative SF Report Type, `Student_Allocation_Report__c` (`packages/lesson/main/default/reportTypes/Student_Allocation_Report.reportType-meta.xml`), with matching reports `Overall_Allocated_Report` and `Monthly_Allocation_Report`. Neither filters or exposes `Archived_At__c`/`Is_Archived__c` as a column. This is a **concrete instance of spec.md's already-documented Regression Risk #4**: "77 Salesforce report types / 1,320 reports... do not filter `Archived_At__c`/`Is_Archived__c`... Not fixable by this epic's code; needs a separate report-remediation pass."

**Nuance specific to this report — not simply "archived rows should be excluded."** Unlike a headcount/active-enrollment report, a consumption-tracking report arguably *should* keep showing an archived LA's historical point consumption, per AC-5's "archived records remain reachable via report filter" scope note — hiding it would lose legitimate financial history. The actual, narrower risk: **archived and active LA rows are visually indistinguishable** in the report output, so staff could misread an archived LA's "Remaining Points" as still usable, when the underlying enrollment is no longer active.

**This is a verification artifact, not a pass/fail code test** — adding an Archived/Status column to the declarative report type is report-metadata work outside this epic's code scope (same mitigation class as the Partner API gap in `withus-juku-partner-api-archive-gap.md`).

## Suite: Lesson Point Consumption tracking

### Lesson Point Consumption Report – Archived LA's Historical Consumption Still Shown, No Distinguishing Indicator

**Description:** AC-5 (confirmed instance of existing Regression Risk #4) — Negative. Contrasts with existing baseline (#9300 "View Lesson Point Consumption Report", #9301 "View sorting report list" — neither accounts for an archived LA mixed into the same student's row group). Confirms current behavior (archived LA's consumption history still appears, which is arguably correct) while documenting the concrete gap (no way to tell it apart from an active LA in the same report).

**Preconditions:**
- Student A has two Lesson Allocations for Course A: LA-1 (active, Total Purchased Points = 20, Remaining = 15, with lesson consumption rows) and LA-2 (archived, `Archived_At__c` populated, Total Purchased Points = 10, Remaining = 4, with its own historical lesson consumption rows from before the archive).

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff generates the Lesson Point Consumption report, grouped by Student A | Per AC-5's scope note, LA-2's historical consumption rows should remain visible — archiving must not erase financial/consumption history | LA-2 Archived_At__c = populated; historical rows preserved |
| 2 | HQ or CM Staff reviews LA-1's and LA-2's rows side by side in the report | Both LA-1 (active) and LA-2 (archived) appear with their respective Total Purchased Points and Remaining Points, with no column, flag, or visual indicator distinguishing LA-2 as archived | Confirmed: report type has no Archived_At__c/Is_Archived__c column |
| 3 | HQ or CM Staff (hypothetically) relies on this report alone to judge whether Student A still has 4 usable points under LA-2 | Risk: a staff member could misread LA-2's "Remaining Points = 4" as still consumable, when the underlying enrollment is archived/inactive — this is the concrete, actionable gap, recommended fix: add an Archived/Status column to the `Student_Allocation_Report__c` report type as part of the broader report-remediation pass already tracked in spec | No server-side/report fix within this epic's scope — documentation only |

**Severity:** minor
**Priority:** medium

---
