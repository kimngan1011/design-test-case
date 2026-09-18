# Test Coverage: LT-101718 / PBT-3075 - Add Subject Code in Subject Master

## Coverage Strategy

| Area | Business Rules | Logic Type | Technique | Risk | Depth | Cases |
|---|---|---|---|---|---|---:|
| Subject Master field metadata and layout | BR-01, BR-02 | Metadata/UI | Component, BVA | High | Standard | 4 |
| Subject Master CRUD | BR-01, BR-02, BR-03 | Data persistence | Equivalence, Negative | High | Deep | 4 |
| Permissions and list views | BR-01 | Access/display | Role matrix | Medium | Standard | 2 |
| Teacher Available Calendar display | BR-05, BR-06 | Integration display | Scenario, Regression | Critical | Deep | 4 |
| Regression guards | BR-07 | Compatibility | Regression | High | Standard | 2 |

Estimated total: 16 cases.

## High-Risk Notes

- The Jira epic says Subject Code should be viewable in Teacher Available Calendar and relevant forms. PRD evidence narrows the clear display requirement to Teacher Available Calendar selected student lesson display, especially US02.2.
- Existing subjects can have blank Subject Code because data migration is out of scope. QA must test blank behavior instead of assuming all lessons can display a code.
- `Subject_Code__c` is optional and Text(30); boundary and over-limit values should be checked on the Salesforce form.
- Current Apex test coverage does not assert `subjectCode` returned by `AvailableTeacherHandler.getStudentLessonsForMonth`, so repo regression gap exists.
- Current Qase ATC suites cover student search and create lesson but not the selected student's existing lesson chip text format.

## Suggested Suite Structure

```
Qase PX > Manabie Scheduling > CORE FEATURES > Event Master > update testcase > Calendar lesson
  Add Subject Code in Subject Master (LT-101718 / PBT-3075)
    - Subject Master CRUD and layout
    - Teacher Available Calendar display
    - Regression
```

## Existing Coverage Reused / Impacted

| Existing area | Existing coverage | New coverage needed |
|---|---|---|
| Available Teacher Calendar student search | Qase `PX-23042`, `PX-23045` in suite `3013` | Keep as regression; add selected student's lesson chip display with Subject Code. |
| Available Teacher Calendar create lesson | Qase `PX-23046`, `PX-23048` in suite `3014` | Confirm Subject Code display does not break prefill or manual override. |
| Course Master CRUD | Qase Course Master cases such as `PX-22608` to `PX-22618` and older `PX-5855`, `PX-5878` | Use as pattern only; Course Code behavior should remain unchanged. |
| Subject Master direct CRUD | No strong Qase match found except unrelated API case `PX-5861` mentioning Subject Master. | Create new Subject Master cases. |
| Apex `AvailableTeacherHandlerTest` | Covers empty/null, session returned, and hasTeacher true. | Add assertion for `subjectCode` and blank fallback. |

## Test Data Matrix

| Fixture | Purpose |
|---|---|
| Subject `国語` with Subject Code `JP01` | Verify Subject Master create/detail/list and ATC chip code. |
| Subject `中国語` with Subject Code `中国` | Verify multibyte code display in limited space. |
| Subject `Math Long` with 30-character code | Verify boundary length. |
| Subject with blank Subject Code | Verify optional field and no-migration fallback. |
| Student `田中花子` with published lessons in two timeslots | Verify selected student lesson chips in ATC. |
| One lesson with assigned teacher whose LastName is `佐藤` | Verify `SubjectCode (佐藤)` format. |
| One lesson without assigned teacher | Verify Subject Code only, no empty parentheses. |
| Available teachers with existing availability data | Verify availability counts/teacher filters are unchanged. |
