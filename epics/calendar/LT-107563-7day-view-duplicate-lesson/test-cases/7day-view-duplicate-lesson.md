# Test Cases: LT-107563 — Duplicate lesson not available in the SF Calendar 7-Day View

## Suite: Calendar lesson (Qase 2717)

### Calendar 7-Day View – Teacher selected – Lesson card opened – Duplicate action not available

**Description:** LT-107563 — Decision Table (baseline) — In the 7-Day (teacher week) View, opening a lesson card must not offer Duplicate.

**Spec sources:**
- [S1] Jira LT-107563 – [ERPv2 SF] [Preprod] User can duplicate lesson in calendar in 7-days view — https://manabie.atlassian.net/browse/LT-107563
- [S2] Code – school-portal-admin CalendarSF CreateLessonModeBanner (7-Day View toggle enabled only when exactly 1 teacher is selected; view exits when the teacher count changes) — src/squads/calendar/domains/CalendarV2/CalendarSF/components/CreateLessonModeBanner/
- [S3] Qase PX-25841 / PX-25842 / PX-25843 – same rule without a specific calendar view

**Preconditions:**
- HQ or CM Staff with LBAC access to Loc_A and Loc_B is logged in to Salesforce and opens the Lesson Calendar at Loc_A
- 7-Day View (teacher week view) is enabled for the org
- Teacher T1 has a Published lesson L_A at Loc_A and a Published lesson L_B at Loc_B in the current week

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens the Teacher List, selects only Teacher T1 and clicks the 7-Day View icon (tooltip "Show teacher's 7-day view" / 講師の週間ビューを表示) | The calendar switches to 7-Day View: 7 day rows for Teacher T1 with the lessons of the current week | Teacher List: T1 only |
| 2 | HQ or CM Staff clicks lesson card L_A | The lesson detail panel of L_A opens; the Duplicate action is not shown | Card = L_A (Loc_A) |

**Severity:** major
**Priority:** high

---

### Calendar 7-Day View – Location switched while the view is open (LBAC multi-location) – Duplicate action still not available

**Description:** LT-107563 — State transition (bug scenario) — After selecting a teacher and opening the 7-Day View, switching to another location and opening a lesson card must still not offer Duplicate. Before the fix, Duplicate became available here.

**Spec sources:**
- [S1] Jira LT-107563 – [ERPv2 SF] [Preprod] User can duplicate lesson in calendar in 7-days view — https://manabie.atlassian.net/browse/LT-107563
- [S2] Code – school-portal-admin CalendarSF CreateLessonModeBanner (7-Day View toggle enabled only when exactly 1 teacher is selected; view exits when the teacher count changes) — src/squads/calendar/domains/CalendarV2/CalendarSF/components/CreateLessonModeBanner/
- [S3] Qase PX-25841 / PX-25842 / PX-25843 – same rule without a specific calendar view

**Preconditions:**
- HQ or CM Staff with LBAC access to Loc_A and Loc_B is logged in to Salesforce and opens the Lesson Calendar at Loc_A
- 7-Day View (teacher week view) is enabled for the org
- Teacher T1 has a Published lesson L_A at Loc_A and a Published lesson L_B at Loc_B in the current week

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens the Teacher List, selects only Teacher T1 and clicks the 7-Day View icon (tooltip "Show teacher's 7-day view" / 講師の週間ビューを表示) | The calendar switches to 7-Day View: 7 day rows for Teacher T1 with the lessons of the current week | Teacher List: T1 only |
| 2 | HQ or CM Staff clicks lesson card L_A | The lesson detail panel of L_A opens; the Duplicate action is not shown | Card = L_A (Loc_A) |
| 3 | HQ or CM Staff closes the lesson detail and changes the calendar location to Loc_B | The calendar shows Loc_B; Teacher T1 stays selected (changing location does not unselect the teacher) and 7-Day View stays active | Location: Loc_A → Loc_B |
| 4 | HQ or CM Staff clicks lesson card L_B | The lesson detail panel of L_B opens; the Duplicate action is not shown | Card = L_B (Loc_B) |

**Severity:** major
**Priority:** high

---

### Calendar 7-Day View – View exited by clicking the 7-Day View icon again – Duplicate action available again

**Description:** LT-107563 — Regression — The fix must be limited to the 7-Day View: after leaving it and clearing the teacher selection, a lesson card on the normal Weekly view offers Duplicate again.

**Spec sources:**
- [S1] Jira LT-107563 – [ERPv2 SF] [Preprod] User can duplicate lesson in calendar in 7-days view — https://manabie.atlassian.net/browse/LT-107563
- [S2] Code – school-portal-admin CalendarSF CreateLessonModeBanner (7-Day View toggle enabled only when exactly 1 teacher is selected; view exits when the teacher count changes) — src/squads/calendar/domains/CalendarV2/CalendarSF/components/CreateLessonModeBanner/
- [S3] Qase PX-25841 / PX-25842 / PX-25843 – same rule without a specific calendar view

**Preconditions:**
- HQ or CM Staff with LBAC access to Loc_A and Loc_B is logged in to Salesforce and opens the Lesson Calendar at Loc_A
- 7-Day View (teacher week view) is enabled for the org
- Teacher T1 has a Published lesson L_A at Loc_A and a Published lesson L_B at Loc_B in the current week

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens the Teacher List, selects only Teacher T1 and clicks the 7-Day View icon (tooltip "Show teacher's 7-day view" / 講師の週間ビューを表示) | The calendar switches to 7-Day View: 7 day rows for Teacher T1 with the lessons of the current week | Teacher List: T1 only |
| 2 | HQ or CM Staff clicks the 7-Day View icon again and clears the teacher selection | The calendar returns to the previous Weekly view with no teacher or student selected |  |
| 3 | HQ or CM Staff clicks lesson card L_A | The lesson detail panel of L_A opens; the Duplicate action is shown | Card = L_A (Loc_A) |

**Severity:** minor
**Priority:** medium

---
