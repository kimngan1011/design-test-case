# Test Cases: LT-107834 / LT-107836 — 7-Day Teacher Schedule View and Teacher List filter

## Suite: Calendar lesson (Qase 2717)

### 7-Day Teacher Schedule View - Single teacher filter and select - View stays active (baseline)

_Qase: PX-25845_

**Description:** Baseline regression for LT-107836 and LT-107834 — Scenario — The 7-Day View can only be opened after exactly one teacher is selected; selecting a teacher via the Teacher List search then clicking the 7-Day View icon shows that teacher's weekly schedule.

**Spec sources:**
- [S1] Jira LT-107836 – Filter teacher list multiple times causes teacher count to drop to 0 and view reverts to Daily View — https://manabie.atlassian.net/browse/LT-107836
- [S2] Jira LT-107834 – Clearing search input causes selected teacher count to drop to 0 and view reverts to Daily View — https://manabie.atlassian.net/browse/LT-107834
- [S4] Code – SPA CreateLessonModeBanner (7-Day View icon enabled only with exactly 1 selected teacher; view exits when the count is not 1; SF calendar only) and Apex LessonMasterHandler.getAssignTeacher (Location, Subject and Working time filters each add an "Id IN (SELECT …)" semi-join; SOQL allows at most 2 per WHERE)

**Preconditions:**
- Enable_Teacher_Week_View__c = true
- HQ or CM Staff is on the Lesson Calendar in Salesforce (7-Day Teacher Schedule View exists only on the SF calendar, not on Back Office)
- 7-Day Teacher Schedule View is available
- No teacher or student is selected

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens the Teacher List on the Lesson Calendar | Teacher List is shown with 0 selected teachers; the 7-Day View icon is disabled (tooltip "Select a teacher to view their weekly schedule" / 講師別週次ビューを表示するには講師を選択してください) | count = 0 |
| 2 | HQ or CM Staff types a teacher name in the Teacher List search field | Matching teachers are listed in the results |  |
| 3 | HQ or CM Staff selects one teacher from the results | Teacher count = 1; the 7-Day View icon becomes enabled (tooltip "Show teacher's 7-day view" / 講師の週間ビューを表示) | count = 1 |
| 4 | HQ or CM Staff clicks the 7-Day View icon | 7-Day Teacher Schedule View is active and displays the selected teacher's weekly schedule |  |

**Severity:** major
**Priority:** medium

---

### 7-Day Teacher Schedule View - Clear search input after selecting a teacher - Teacher stays selected and view remains active

_Qase: PX-25846_

**Description:** Bug ref: LT-107834 — Scenario — After selecting a teacher via search while the Teacher List has Subject + Location + Working time filters applied, clearing the search input must NOT deselect the teacher or exit 7-Day View. Root cause: with these 3 filters the teacher list API returns an error (3 semi-join sub-queries), the list is emptied and the count drops to 0.

**Spec sources:**
- [S2] Jira LT-107834 – Clearing search input causes selected teacher count to drop to 0 and view reverts to Daily View — https://manabie.atlassian.net/browse/LT-107834
- [S5] Root cause confirmed by dev (Long, 2026-09-29): with Subject + Location + Working time applied, the teacher list API returns an error, no new teacher list is loaded and the selected teacher count drops to 0
- [S4] Code – SPA CreateLessonModeBanner (7-Day View icon enabled only with exactly 1 selected teacher; view exits when the count is not 1; SF calendar only) and Apex LessonMasterHandler.getAssignTeacher (Location, Subject and Working time filters each add an "Id IN (SELECT …)" semi-join; SOQL allows at most 2 per WHERE)

**Preconditions:**
- Enable_Teacher_Week_View__c = true
- HQ or CM Staff is on the Lesson Calendar in Salesforce (7-Day Teacher Schedule View exists only on the SF calendar, not on Back Office)
- 7-Day Teacher Schedule View is active with 1 teacher selected (count = 1)
- The Teacher List filter has Subject, Location and Working time applied together (the 3 fields that reproduce LT-107834)
- The Restrict Teacher Match All Subjects setting is OFF for the org (when ON, the Subject filter does not use a sub-query and the bug does not reproduce). How to check: Setup > Quick Find "Custom Settings" > Lesson Custom Settings > Manage > Default Organization Level Value: "Restrict Teacher Match All Subjects" must be unticked (no org default record also means OFF; Profile / User rows are ignored). Alternative: Developer Console > Query Editor: SELECT SetupOwner.Name, MANAERP__Restrict_Teacher_Match_All_Subjects__c FROM MANAERP__Lesson_Custom_Settings__c -> the row of the organization must be false or absent
- The Lesson_Staff_Working_Hour feature flag is ON (otherwise the Working time filter does not exist). How to check: the Teacher List filter shows the working time fields (start time, end time, day of week); or Setup > Quick Find "Custom Metadata Types" > FeatureFlag > Manage Records > Lesson_Staff_Working_Hour: IsEnabled is ticked

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Confirm 7-Day Teacher Schedule View is active with 1 teacher selected (count = 1) | Teacher count = 1, weekly schedule is displayed |  |
| 2 | Type a teacher name in the search field and select a different teacher from the results | Teacher count = 1, view re-renders with the newly selected teacher's weekly schedule |  |
| 3 | Clear the search input field (delete all typed text) | Teacher count remains = 1, 7-Day Teacher Schedule View stays active with the currently selected teacher's schedule still displayed |  |

**Severity:** major
**Priority:** high

---

### 7-Day Teacher Schedule View - Filter and switch teachers multiple times - Teacher count stays 1 and view stays active

_Qase: PX-25847_

**Description:** Bug ref: LT-107836. Filtering and selecting different teachers 3-5 times must not cause teacher count to drop to 0 or revert the calendar back to Standard Daily View.

**Spec sources:**
- [S1] Jira LT-107836 – Filter teacher list multiple times causes teacher count to drop to 0 and view reverts to Daily View — https://manabie.atlassian.net/browse/LT-107836
- [S3] erp-salesforce commit 9deddb4 [LT-107836] (listTeacherCalendar ignores an empty selection event while re-syncing) — https://github.com/manabie-com/erp-salesforce/commit/9deddb423111c58a7134bd8ea47b81d0d4a70d90

**Preconditions:**
- Enable_Teacher_Week_View__c = true
- HQ or CM Staff is on the Lesson Calendar in Salesforce (7-Day Teacher Schedule View exists only on the SF calendar, not on Back Office)
- 7-Day Teacher Schedule View is active with 1 teacher selected (count = 1)
- Multiple teachers are available to filter and select

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Confirm 7-Day Teacher Schedule View is active with 1 teacher selected (count = 1) | Teacher count = 1, weekly schedule is displayed |  |
| 2 | Use the filter to search for another teacher and select them | Teacher count = 1, view re-renders with the new teacher's schedule |  |
| 3 | Repeat: filter for a different teacher name and select them (repeat 3-5 times total) | After each selection: teacher count = 1, 7-Day View remains active with the newly selected teacher's weekly schedule |  |
| 4 | After completing 3-5 teacher switches, observe the view state and teacher count | Teacher count = 1, 7-Day Teacher Schedule View is still active — calendar has NOT reverted to Standard Daily View |  |

**Severity:** major
**Priority:** high

---

### 7-Day Teacher Schedule View - Filter for different fields multiple times then select - View does not revert to Daily View

_Qase: PX-25848_

**Description:** Extended scenario for LT-107836. Filters using different search keywords (not just teacher name) multiple times before selecting, verifying no view regression.

**Spec sources:**
- [S1] Jira LT-107836 – Filter teacher list multiple times causes teacher count to drop to 0 and view reverts to Daily View — https://manabie.atlassian.net/browse/LT-107836
- [S3] erp-salesforce commit 9deddb4 [LT-107836] (listTeacherCalendar ignores an empty selection event while re-syncing) — https://github.com/manabie-com/erp-salesforce/commit/9deddb423111c58a7134bd8ea47b81d0d4a70d90

**Preconditions:**
- Enable_Teacher_Week_View__c = true
- HQ or CM Staff is on the Lesson Calendar in Salesforce (7-Day Teacher Schedule View exists only on the SF calendar, not on Back Office)
- 7-Day Teacher Schedule View is active with 1 teacher selected (count = 1)

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | In 7-Day Teacher Schedule View, confirm teacher count = 1 | 7-Day View active, teacher count = 1 |  |
| 2 | Filter teacher list with search term A, then clear it, then filter with search term B, then clear it (repeat with different keywords) | Teacher list updates on each filter; no change to selected teacher count or view mode |  |
| 3 | Filter with a new term and select a teacher from the results | Teacher count = 1, 7-Day Teacher Schedule View re-renders the selected teacher's schedule — view has NOT reverted to Standard Daily View |  |

**Severity:** minor
**Priority:** medium

---

### Calendar Teacher List – Subject, Location and Working time filters applied together – Matching teachers listed without error

_Qase: PX-29120_

**Description:** LT-107834 root cause — Decision Table — Applying Subject + Location + Working time together in the Teacher List filter must return the teachers matching all three instead of an error / empty list. Independent of the calendar view. Before the fix the API fails because the query has 3 semi-join sub-queries (SOQL allows at most 2). The error is silent: the UI shows no message, only an empty Teacher List (it looks like "no teacher matches"), so the API response must be checked in DevTools. Only 7-Day View makes it visible (it exits).

**Spec sources:**
- [S2] Jira LT-107834 – Clearing search input causes selected teacher count to drop to 0 and view reverts to Daily View — https://manabie.atlassian.net/browse/LT-107834
- [S5] Root cause confirmed by dev (Long, 2026-09-29): with Subject + Location + Working time applied, the teacher list API returns an error, no new teacher list is loaded and the selected teacher count drops to 0
- [S4] Code – SPA CreateLessonModeBanner (7-Day View icon enabled only with exactly 1 selected teacher; view exits when the count is not 1; SF calendar only) and Apex LessonMasterHandler.getAssignTeacher (Location, Subject and Working time filters each add an "Id IN (SELECT …)" semi-join; SOQL allows at most 2 per WHERE)

**Preconditions:**
- HQ or CM Staff is on the Lesson Calendar in Salesforce (7-Day Teacher Schedule View exists only on the SF calendar, not on Back Office)
- The Restrict Teacher Match All Subjects setting is OFF for the org (when ON, the Subject filter does not use a sub-query and the bug does not reproduce). How to check: Setup > Quick Find "Custom Settings" > Lesson Custom Settings > Manage > Default Organization Level Value: "Restrict Teacher Match All Subjects" must be unticked (no org default record also means OFF; Profile / User rows are ignored). Alternative: Developer Console > Query Editor: SELECT SetupOwner.Name, MANAERP__Restrict_Teacher_Match_All_Subjects__c FROM MANAERP__Lesson_Custom_Settings__c -> the row of the organization must be false or absent
- The Lesson_Staff_Working_Hour feature flag is ON (otherwise the Working time filter does not exist). How to check: the Teacher List filter shows the working time fields (start time, end time, day of week); or Setup > Quick Find "Custom Metadata Types" > FeatureFlag > Manage Records > Lesson_Staff_Working_Hour: IsEnabled is ticked
- Teacher T1: eligible subject Sub_A, affiliated with Loc_A, working hour Monday 10:00–18:00 (not an off day)
- Teacher T2: eligible subject Sub_A, affiliated with Loc_A, no working hour on Monday
- Teacher T3: eligible subject Sub_B only, affiliated with Loc_A, working hour Monday 10:00–18:00
- No teacher is selected
- Tester has Chrome DevTools open on the Network tab, filtered by "getAssignTeacher" (request header x-sfdc-lds-endpoints: ApexActionController.execute:LessonMasterHandler.getAssignTeacher)

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens the Teacher List and opens its filter | The filter shows Location, Subject and Working time fields |  |
| 2 | HQ or CM Staff sets Location = Loc_A and Subject = Sub_A and applies the filter | Teacher List shows T1 and T2; T3 is not shown | Location = Loc_A; Subject = Sub_A (2 filters) |
| 3 | HQ or CM Staff also sets Working time = Monday 12:00–13:00 and applies the filter | Teacher List shows T1 only; T2 and T3 are not shown. An empty list is a FAIL (the API error is silent in the UI) | Location = Loc_A; Subject = Sub_A; Working time = Monday 12:00–13:00 (3 filters) |
| 4 | Tester opens the latest getAssignTeacher request in DevTools > Network and reads its Response and Payload | Response: actions[0].state = "SUCCESS" and returnValue contains T1 (not state "ERROR" with a query error). Payload params contain locationIds, subjects and startWorkingTime / endWorkingTime (all 3 filters sent) | Request: POST /aura?...aura.ApexAction.execute=1; method = LessonMasterHandler.getAssignTeacher |
| 5 | HQ or CM Staff selects T1 | Teacher count = 1 and T1 stays selected | count = 1 |

**Severity:** critical
**Priority:** high

---
