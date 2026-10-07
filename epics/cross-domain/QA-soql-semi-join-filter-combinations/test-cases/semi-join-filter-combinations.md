# Test Cases: SOQL / GraphQL semi-join limit — filter combinations

## Suite: Aver lesson report (Qase 2633)

### [Aver] Lesson Report List – Student name search with Teacher filter – Reports matching both conditions listed without error

_Qase: PX-29136_

**Description:** LT-111933 — Decision Table (filter combination) — On the BO Aver Lesson Report list (V2, GraphQL), searching a student name while a Teacher filter is applied must return the reports matching both. Before the fix the query had 3 inq (default + search + Teacher) and failed with "Unable to load data, please try again!".

**Spec sources:**
- [S3] Jira LT-111933 — https://manabie.atlassian.net/browse/LT-111933
- [S4] Code – useRetrieveAverLessonReportSFV2 / aver-lesson-report-filters.ts (CombineAverLessonReportSFFilters adds a default inq)
- [S1] Lesson learned 2026-09-29 "Teacher List Filter Fails Silently … (SOQL 2 Semi-Join Limit)" — design-test-case/knowledge/domain-knowledge/scheduling/lesson-learned/core.md
- [S2] Salesforce: at most 2 semi-join / anti-join sub-queries (IN / NOT IN (SELECT …), GraphQL inq / ninq) per WHERE clause

**Preconditions:**
- Aver tenant; HQ or CM Staff is logged in to Back Office
- Unleash toggle Lesson_BackOffice_LessonSF_AllowViewLessonOtherLocations is ON (V2 list)
- Report R1: student S1 in a lesson taught by teacher T1
- Report R2: student S1 in a lesson taught by teacher T2
- Report R3: student S2 in a lesson taught by teacher T1
- Tester keeps Chrome DevTools > Network open to read the GraphQL response (/services/data/v60.0/graphql)

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens the Aver Lesson Report list | The list is shown |  |
| 2 | HQ or CM Staff types the name of S1 in the search box and presses Enter | R1 and R2 are listed; R3 is not listed | search = S1 |
| 3 | HQ or CM Staff opens Filter, selects Teacher T1 and clicks Apply | Only R1 is listed; no snackbar "Unable to load data, please try again!" is shown | Teacher = T1; search = S1 |
| 4 | Tester opens the latest Lesson_RetrieveLessonReportSF_Aver request in DevTools > Network > Response | Response has no "errors" array and data.uiapi.query.Aver_Lesson_Report__c is not null |  |
| 5 | HQ or CM Staff clears the search box | R1 and R3 are listed (Teacher T1 only) | Teacher = T1 |

**Severity:** major
**Priority:** high

---

## Suite: Lesson List (Qase 250)

### [Aver] Lesson List – Student name search with Teacher Name and Report Status filters – Matching lessons listed without error

_Qase: PX-29137_

**Description:** LT-111934 — Decision Table (filter combination) — On the BO Lesson List of Aver (feature setting lesson.lessonmgmt_sf.experience_cloud_report_site ON), searching a student name with Teacher Name and Report Status applied must return the matching lessons. Before the fix the query had 3 inq (search + Teacher Name + Report Status) and failed with "Unable to load data, please try again!".

**Spec sources:**
- [S3] Jira LT-111934 — https://manabie.atlassian.net/browse/LT-111934
- [S4] Code – useGetLessonListSFV2 / lesson-list-sf-filters.ts (calcSearch, calcTeachers inq; Aver_Lesson_Report__c inq for Report Status)
- [S1] Lesson learned 2026-09-29 "Teacher List Filter Fails Silently … (SOQL 2 Semi-Join Limit)" — design-test-case/knowledge/domain-knowledge/scheduling/lesson-learned/core.md
- [S2] Salesforce: at most 2 semi-join / anti-join sub-queries (IN / NOT IN (SELECT …), GraphQL inq / ninq) per WHERE clause

**Preconditions:**
- Aver tenant; HQ or CM Staff is logged in to Back Office
- Lesson L1: teacher T1, student S1, Aver lesson report status Draft
- Lesson L2: teacher T1, student S1, Aver lesson report status Published
- Lesson L3: teacher T1, student S2, Aver lesson report status Draft
- Tester keeps Chrome DevTools > Network open to read the GraphQL response (/services/data/v60.0/graphql)

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens Lesson Management > Lesson List | The list is shown |  |
| 2 | HQ or CM Staff opens Filter, sets Teacher Name = T1 and Report Status = Draft, clicks Apply | L1 and L3 are listed | Teacher Name = T1; Report Status = Draft |
| 3 | HQ or CM Staff types the name of S1 in Enter Student Name and presses Enter | Only L1 is listed; no snackbar "Unable to load data, please try again!" is shown | search = S1 |
| 4 | Tester opens the latest lesson list GraphQL request in DevTools > Network > Response | Response has no "errors" array and the lesson list data is not null |  |

**Severity:** major
**Priority:** high

---

## Suite: Lesson List (Qase 250)

### Lesson List – Student name search with Teacher Name and Class filters – Matching lessons listed without error

_Qase: PX-29138_

**Description:** LT-111936 — Decision Table (filter combination) — On the BO Lesson List (all tenants), searching a student name with Teacher Name and Class applied must return the matching lessons. Before the fix the query had 3 inq (search + Teacher Name + Class) and failed with "Unable to load data, please try again!". Class can only be selected after Location → Course (see lesson learned "BO Lesson List Filter Chain").

**Spec sources:**
- [S3] Jira LT-111936 — https://manabie.atlassian.net/browse/LT-111936
- [S4] Code – useGetLessonListSFV2 / lesson-list-sf-filters.ts (calcSearch, calcTeachers, calcClasses inq)
- [S1] Lesson learned 2026-09-29 "Teacher List Filter Fails Silently … (SOQL 2 Semi-Join Limit)" — design-test-case/knowledge/domain-knowledge/scheduling/lesson-learned/core.md
- [S2] Salesforce: at most 2 semi-join / anti-join sub-queries (IN / NOT IN (SELECT …), GraphQL inq / ninq) per WHERE clause

**Preconditions:**
- HQ or CM Staff is logged in to Back Office
- Location Loc_A has course C1 with class K1
- Lesson L1 (class K1): teacher T1, student S1
- Lesson L2 (class K1): teacher T1, student S2
- Lesson L3 (class K1): teacher T2, student S1
- Tester keeps Chrome DevTools > Network open to read the GraphQL response (/services/data/v60.0/graphql)

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens Lesson Management > Lesson List | The list is shown |  |
| 2 | HQ or CM Staff opens Filter and selects Location = Loc_A, then Course = C1, then Class = K1, then Teacher Name = T1, and clicks Apply | L1 and L2 are listed | Location → Course → Class order is required (Class is disabled until a Course is selected) |
| 3 | HQ or CM Staff types the name of S1 in Enter Student Name and presses Enter | Only L1 is listed; no snackbar "Unable to load data, please try again!" is shown | search = S1 |
| 4 | Tester opens the latest lesson list GraphQL request in DevTools > Network > Response | Response has no "errors" array and the lesson list data is not null |  |

**Severity:** major
**Priority:** high

---

## Suite: Calendar lesson (Qase 2717)

### Calendar SF Student List – Every filter including Class applied with a student name search – List loads without error

_Qase: PX-29139_

**Description:** Regression (at the 2 semi-join limit) — getListAssignStudent always has 1 semi-join (Enrollment at the calendar location) and adds 1 for Class. Applying every Student List filter together with a search must still load. A new sub-query-based filter would break this.

**Spec sources:**
- [S3] Code – LessonMasterHandler.getListAssignStudent (Enrollment semi-join + Class_Member semi-join)
- [S1] Lesson learned 2026-09-29 "Teacher List Filter Fails Silently … (SOQL 2 Semi-Join Limit)" — design-test-case/knowledge/domain-knowledge/scheduling/lesson-learned/core.md
- [S2] Salesforce: at most 2 semi-join / anti-join sub-queries (IN / NOT IN (SELECT …), GraphQL inq / ninq) per WHERE clause

**Preconditions:**
- HQ or CM Staff is logged in to Salesforce and opens the Lesson Calendar at Loc_A
- Student S1 has an active lesson allocation at Loc_A in course C1, class K1, grade G1
- Tester keeps Chrome DevTools > Network open to read the Apex response (request /aura?…ApexAction.execute, check actions[0].state)

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens the Student List and its filter | The filter shows all Student List fields |  |
| 2 | HQ or CM Staff sets every available filter so that S1 still matches (Location, Course C1, Class K1, Grade G1, school, type, status fields) and applies | The list loads and shows S1 | Class = K1 + all other filters |
| 3 | HQ or CM Staff types the name of S1 in the search box | The list shows S1 only | search = S1 |
| 4 | Tester reads the latest LessonMasterHandler.getListAssignStudent response in DevTools | actions[0].state = "SUCCESS" (no ERROR) |  |

**Severity:** minor
**Priority:** medium

---

## Suite: Change lesson (Qase 2271)

### Change Lesson popup – Every filter including Class applied with a lesson name search – Lesson list loads without error

_Qase: PX-29140_

**Description:** Regression (at the 2 semi-join limit) — getReallocateLessonList always has 1 anti-join (lessons the student already has) and adds 1 for Class. Applying every filter together with a lesson name search must still load. The Reallocate popup uses the same API.

**Spec sources:**
- [S3] Code – LessonHandler.getReallocateLessonList (NOT IN Student_Sessions + Lesson_Schedule_Class semi-join)
- [S1] Lesson learned 2026-09-29 "Teacher List Filter Fails Silently … (SOQL 2 Semi-Join Limit)" — design-test-case/knowledge/domain-knowledge/scheduling/lesson-learned/core.md
- [S2] Salesforce: at most 2 semi-join / anti-join sub-queries (IN / NOT IN (SELECT …), GraphQL inq / ninq) per WHERE clause

**Preconditions:**
- HQ or CM Staff is logged in to Salesforce
- Future lesson L_TARGET at Loc_A: course C1, class K1, lesson name "LT-REG-TARGET"
- Student S1 has a student session in another lesson at Loc_A; its lesson detail is open on the SF calendar
- Tester keeps Chrome DevTools > Network open to read the Apex response (request /aura?…ApexAction.execute, check actions[0].state)

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens the Change Lesson popup for S1 | The candidate lesson list is shown |  |
| 2 | HQ or CM Staff opens the popup filter, sets every available filter so that L_TARGET still matches (Location, Course C1, Class K1, date range, capacity, teaching method) and applies | The list loads and shows L_TARGET | Class = K1 + all other filters |
| 3 | HQ or CM Staff types "LT-REG-TARGET" in Search lessons and presses Enter | The list shows L_TARGET only |  |
| 4 | Tester reads the latest LessonHandler.getReallocateLessonList response in DevTools | actions[0].state = "SUCCESS" |  |

**Severity:** minor
**Priority:** medium

---

## Suite: View the Add Student Popup (Qase 1648)

### Add Student Popup – Every filter including Class applied with a student name search – List loads without error

_Qase: PX-29141_

**Description:** Regression (at the 2 semi-join limit) — getLessonAllocationListByLessonInfo always has 1 semi-join (Enrollment at the lesson location) and adds 1 for Class. Applying every filter together with a student name search must still load.

**Spec sources:**
- [S3] Code – LessonAllocationHandler.buildGetLessonAllocationListByLessonInfoStmt (Enrollment + Class_Member semi-joins)
- [S1] Lesson learned 2026-09-29 "Teacher List Filter Fails Silently … (SOQL 2 Semi-Join Limit)" — design-test-case/knowledge/domain-knowledge/scheduling/lesson-learned/core.md
- [S2] Salesforce: at most 2 semi-join / anti-join sub-queries (IN / NOT IN (SELECT …), GraphQL inq / ninq) per WHERE clause

**Preconditions:**
- HQ or CM Staff is logged in to Salesforce
- Lesson L1 at Loc_A; student S1 (not in L1) has an active lesson allocation at Loc_A in course C1, class K1, grade G1
- The Lesson Detail of L1 is open
- Tester keeps Chrome DevTools > Network open to read the Apex response (request /aura?…ApexAction.execute, check actions[0].state)

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff clicks "Add Students" in the Student Sessions section | The Add Student popup is shown |  |
| 2 | HQ or CM Staff sets every available filter so that S1 still matches (Location, Course C1, Class K1, Grade G1, school, type, classification) and applies | The list loads and shows S1 | Class = K1 + all other filters |
| 3 | HQ or CM Staff types the name of S1 in Enter student name | The list shows S1 only | search = S1 |
| 4 | Tester reads the latest LessonAllocationHandler.getLessonAllocationListByLessonInfo response in DevTools | actions[0].state = "SUCCESS" |  |

**Severity:** minor
**Priority:** medium

---

## Suite: Calendar lesson (Qase 2717)

### Available Teacher Calendar – Subject, Tag, Name and Gender filters applied together – Qualified teachers listed without error

_Qase: PX-29142_

**Description:** Regression (at the 2 semi-join limit) — AvailableTeacherHandler.resolveQualifiedTeacherIds always has 1 semi-join (Affiliation at the location) and adds 1 for Subject. Applying every teacher filter together must still load.

**Spec sources:**
- [S3] Code – AvailableTeacherHandler.resolveQualifiedTeacherIds (Affiliation + Eligible_Subject semi-joins)
- [S1] Lesson learned 2026-09-29 "Teacher List Filter Fails Silently … (SOQL 2 Semi-Join Limit)" — design-test-case/knowledge/domain-knowledge/scheduling/lesson-learned/core.md
- [S2] Salesforce: at most 2 semi-join / anti-join sub-queries (IN / NOT IN (SELECT …), GraphQL inq / ninq) per WHERE clause

**Preconditions:**
- HQ or CM Staff is logged in to Salesforce and opens the Available Teacher Calendar at Loc_A
- Teacher T1: affiliated with Loc_A, eligible for subject SUB1, tag TAG1, gender set, working status Available
- Tester keeps Chrome DevTools > Network open to read the Apex response (request /aura?…ApexAction.execute, check actions[0].state)

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff selects a date / slot and sets Subject = SUB1, Tag = TAG1, teacher name = T1 and Gender = the gender of T1 | The qualified teacher list loads and shows T1 | all teacher filters |
| 2 | Tester reads the latest AvailableTeacherHandler.getTeachersForDateSlot (or getMonthlyAvailability) response in DevTools | actions[0].state = "SUCCESS" |  |

**Severity:** minor
**Priority:** medium

---

## Suite: Aver lesson report (Qase 2633)

### [Aver] Lesson Report List (V1) – Every filter including Teacher applied with a student name search – Reports listed without error

_Qase: PX-29143_

**Description:** Regression (at the 2 semi-join limit) — With the Unleash toggle Lesson_BackOffice_LessonSF_AllowViewLessonOtherLocations OFF (V1 list), the SOQL always has 1 semi-join (Lesson__c IN (SELECT Id FROM Lesson__c)) and adds 1 for Teacher; the student search is not a semi-join in V1. Applying every filter with a search must still load.

**Spec sources:**
- [S3] Code – useRetrieveAverLessonReportList (V1 SOQL)
- [S1] Lesson learned 2026-09-29 "Teacher List Filter Fails Silently … (SOQL 2 Semi-Join Limit)" — design-test-case/knowledge/domain-knowledge/scheduling/lesson-learned/core.md
- [S2] Salesforce: at most 2 semi-join / anti-join sub-queries (IN / NOT IN (SELECT …), GraphQL inq / ninq) per WHERE clause

**Preconditions:**
- Aver tenant; HQ or CM Staff is logged in to Back Office
- Unleash toggle Lesson_BackOffice_LessonSF_AllowViewLessonOtherLocations is OFF for the environment
- Report R1: student S1, teacher T1, location Loc_A, course C1, lesson status Published, report status Draft

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens the Aver Lesson Report list and sets every filter so that R1 still matches (lesson status, report status, location, course, Teacher T1, date range) and applies | The list loads and shows R1 | all filters |
| 2 | HQ or CM Staff types the name of S1 in the search box | The list shows R1; no snackbar "Unable to load data, please try again!" is shown | search = S1 |

**Severity:** minor
**Priority:** medium

---
