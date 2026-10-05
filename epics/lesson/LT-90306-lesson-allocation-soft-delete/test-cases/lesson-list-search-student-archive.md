# Test Cases: LT-90306 — Lesson Allocation Soft Delete (Archive)

Source Qase suite reviewed: [PX suite 250 — "Lesson List"](https://app.qase.io/project/PX?suite=250) (13 existing cases). Case 1889 ("Search by Student Name – Matching Student Name Entered – Lessons with That Student Returned") and the recent fix cases 29137/29138 (LT-111934/LT-111936, combined-filter semi-join bug) all exercise student-name search, but none test an archived Lesson Allocation.

Code trace: the "Search by Student Name" filter (`calcSearch` in `school-portal-admin/src/squads/lesson/domains/LessonManagement/hooks/useGetLessonListSFV2/lesson-list-sf-filters.ts`) already filters `MANAERP__Student_Sessions__c.MANAERP__Is_Archived__c: { eq: false }` on its semi-join — confirmed added by commit `5e9fb50e` ("[LT-111546] feature: filter archived lesson allocation records out of SF queries"), which retrofitted this same filter across 9 GraphQL query files and 3 filter-builder files in the BO frontend (student session, lesson report, Aver lesson report, zoom participants, calendar sessions). This query executes live against Salesforce's native GraphQL API (no replica/sync layer), so there is no staleness concern. **This is already correct, but has zero regression coverage** for the archived-search-exclusion behavior specifically — the case below locks it in.

## Suite: Lesson List

### Lesson List – Search by Student Name – Student's Only Session in Lesson Archived – Lesson Excluded from Search Results; Restored – Reappears

**Description:** Regression / control case — Decision Table, contrasts with the baseline (case 1889, "Search by Student Name – Matching Student Name Entered – Lessons with That Student Returned") — once Student A's Lesson Allocation is archived, a Lesson List search for Student A's name no longer returns the lesson they were assigned to (since the matching Student_Sessions__c row is excluded by the search's `Is_Archived__c = false` semi-join filter), and the lesson reappears in search results once the Lesson Allocation is restored.

**Preconditions:**
- Lesson L1 exists with Student A assigned (Student A is the only student in L1). Searching "Student A" on the Lesson List currently returns L1.
- Student A has an active Lesson Allocation for the course behind L1.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens Lesson Management > Lesson List and searches "Student A" | L1 appears in the search results | Student A Is_Archived__c = FALSE → matched |
| 2 | The Student Package Order behind Student A's Lesson Allocation is fully removed, so the Lesson Allocation is archived | The Lesson Allocation shows Archived_At__c populated | Archived_At__c = current timestamp |
| 3 | HQ or CM Staff repeats the search for "Student A" on the Lesson List | L1 no longer appears in the search results | Student A's Student Session Is_Archived__c = TRUE (via formula) → excluded from calcSearch's semi-join |
| 4 | A living Student Package Order reappears for Student A's Student Course, so the Lesson Allocation is unarchived on the same record Id | The Lesson Allocation shows Archived_At__c blank again | Archived_At__c = null (restored) |
| 5 | HQ or CM Staff repeats the search for "Student A" on the Lesson List | L1 reappears in the search results | Student A Is_Archived__c = FALSE (restored) → matched again |

**Severity:** minor
**Priority:** medium

---
