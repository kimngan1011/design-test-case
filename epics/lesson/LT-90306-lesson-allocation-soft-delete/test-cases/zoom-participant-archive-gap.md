# Test Cases: LT-90306 — Lesson Allocation Soft Delete (Archive)

Source Qase suite reviewed: [PX suite 251 — "Lesson Detail"](https://app.qase.io/project/PX?suite=251) (6 existing cases). All 6 cases cover lesson-edit CRUD and recurrence scope ("Only this lesson" vs "This and the following") for the manually-edited `Live_Streaming_Link__c` field — none test the separately-sourced Zoom Owner/Link info drawn from `Zoom_Participant__c` records, which is what this gap, found while reviewing suite 250 ("Lesson List")'s recent archive-filter fix and confirmed by an exhaustive repo-wide sweep of every GraphQL/TS file in `school-portal-admin` referencing `Student_Sessions__c`, `Zoom_Participant__c`, `Lesson_Report_Detail__c`-equivalent objects, `Lesson_Allocation__c`, and `Class_Members__r`, is about. This is the **only** such gap found in the entire frontend repo — every other query touching these objects was already correctly patched.

Code trace: commit `5e9fb50e` ("[LT-111546] feature: filter archived lesson allocation records out of SF queries") retrofitted `MANAERP__Is_Archived__c: { eq: false }` onto every `MANAERP__Zoom_Participant__c` → `MANAERP__Student_Session__r` GraphQL query it touched (`lesson-zoom-participants-service/lesson-zoom-participants.graphql` and `squads/calendar/service/sf/lesson-zoom-participants.graphql`), plus 4 other files (student session, lesson report, Aver lesson report queries) and a raw-SOQL zoom-owner lookup. The sibling query `src/squads/lesson/service/sf/lesson-service/lesson.query.graphql`'s `GetLessonSFDetailByID` (lines 179-203) — which ALSO selects `MANAERP__Zoom_Participant__c` records, specifically to populate the main Lesson Detail page's Zoom Owner/Link — was **not** patched: no `Is_Archived__c` filter at all on its Zoom Participant sub-query.

This is more than a cosmetic inconsistency: the query is `orderBy: { CreatedDate: { order: DESC } }`, and its consumer, `src/squads/lesson/domains/LessonManagement/modules/lesson-sf-detail/hooks/useGetLessonSFDetail.ts` (lines 74-184), picks the FIRST element of that ordered list (`pick1stElement(...)`) to populate `lessonData.zoomLink` / `lessonData.zoomOwner`. Since archived-student Zoom Participant rows are never excluded, a student's (now-archived) participation record — if it happens to be the most recently created one — can win this "most recent" pick and surface a stale or wrong Zoom link/owner on the live Lesson Detail page, actively overriding what should be shown.

## Suite: Lesson Detail

### Lesson Detail Page – Zoom Owner/Link – Most-Recent Zoom Participant Record Belongs to an Archived Student – Stale Zoom Info Wins the Pick

**Description:** Gap case — Decision Table — `GetLessonSFDetailByID`'s Zoom Participant sub-query has no `Is_Archived__c` filter, unlike the Calendar page and the dedicated zoom-participants-service query (both patched by commit `5e9fb50e`). Because `useGetLessonSFDetail.ts` orders this list by `CreatedDate DESC` and picks only the first element to populate the Lesson Detail page's Zoom Owner/Link, an archived student's Zoom Participant row — if it is the most recently created one for this lesson — silently wins the pick over a more relevant, still-valid participant record.

**Preconditions:**
- Lesson L1 has two Zoom Participant records: an earlier one for the Teacher (Zoom Owner), and a later one for Student A (joined via Zoom after the teacher). Student A has an active Lesson Allocation. The Lesson Detail page currently shows Student A's Zoom Participant record as the most recent (since no filter yet distinguishes them).

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens Lesson L1's Lesson Detail page and the Calendar view for the same lesson, confirming both currently show the same Zoom Owner/Link info sourced from Student A's (most recent) Zoom Participant record | Both pages show identical Zoom Owner/Link info | Student A Is_Archived__c = FALSE; Student A's Zoom Participant row is the most recently created |
| 2 | The Student Package Order behind Student A's Lesson Allocation is fully removed, so the Lesson Allocation is archived | The Lesson Allocation shows Archived_At__c populated | Archived_At__c = current timestamp |
| 3 | HQ or CM Staff reopens the Calendar view for Lesson L1 | The Calendar view's Zoom Participant list now correctly excludes Student A's row — correctly excluded, consistent with the LT-111546 fix | Calendar's lesson-zoom-participants.graphql filters Is_Archived__c = false |
| 4 | HQ or CM Staff reopens Lesson L1's Lesson Detail page (same lesson, same Zoom session) | The Zoom Owner/Link shown is STILL sourced from Student A's archived Zoom Participant record — inconsistent with the Calendar page in step 3, and potentially stale/wrong, since GetLessonSFDetailByID's Zoom Participant sub-query was never patched with the same filter and still picks the most-recently-created row regardless of archive state | useGetLessonSFDetail.ts's pick1stElement(...) on a DESC-ordered, unfiltered Zoom Participant list still selects Student A's record |

**Severity:** minor
**Priority:** low

---
