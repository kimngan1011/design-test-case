---
ticket_id: LT-107411
ticket_url: https://manabie.atlassian.net/browse/LT-107411
title: Riso | Core | TAC improvement (July)
module: scheduling
bucket: OOP/riso
status: In Development
internal_uat_date: null
production_release_date: null
last_updated: 2026-09-22
---

# LT-107411: Riso | Core | TAC improvement (July)

## Summary

This Riso Salesforce Teacher Availability Calendar (TAC) improvement removes misleading subject suggestions, expands teacher search, updates calendar labels and filter layout, makes Course mandatory in the creation sidebar, consolidates duplicate lessons, and changes the post-create destination to Lesson Schedule detail. The PBT attachment screenshots are the visual source for the duplicate indicator/alert, label arrangement, and fixed Course layout.

---

## Acceptance Criteria

| AC | Requirement |
|---|---|
| AC 01 | Subject filter opens with no partial suggestion list; users enter text before selecting a subject. Subject search and selection continue to work. |
| AC 02 | Teacher filter searches Teacher Name, Phonetic Name, and External User ID. The placeholders are `Search Teacher Name, External User ID` and `講師名、外部IDで検索`. |
| AC 03 | Student lesson label shows `Subject Name (Teacher Name)` instead of `Lesson Name (Teacher Name)`. |
| AC 04 | Location is part of the collapsible filter accordion and its filtering behavior persists across expand/collapse. |
| AC 05 | Course is required and fixed in the left sidebar; only Available Teachers/Timeslot content scrolls. Japanese date is shown without a slash, for example `7月1日`. |
| AC 06 | Duplicate lessons for one student in one timeslot use the consolidated Calendar representation and sidebar alert shown in the PBT attachment. A single lesson remains normal. |
| AC 07 | Successful creation opens the created Lesson Schedule detail instead of Lesson Calendar. Cancel and error behavior remain unchanged. |

## Business Rules (Extracted)

| # | AC | Business Rule | Field | Field Behavior | Platform |
|---:|---|---|---|---|---|
| 1 | AC 01 | Empty Subject search shows no suggestions. | Subject filter | conditional | SF |
| 2 | AC 01 | Entered matching text permits Subject selection. | Subject filter | searchable | SF |
| 3 | AC 02 | Teacher search finds Teacher Name, Phonetic Name, and External User ID. | Teacher filter | searchable | SF |
| 4 | AC 02 | Placeholder text follows EN/JP locale exactly. | Teacher filter placeholder | computed | SF |
| 5 | AC 03 | A populated student lesson chip shows Subject Name and Teacher Name together. | Student lesson label | computed | SF |
| 6 | AC 04 | Location is hidden and restored with the filter accordion. | Location filter | conditional | SF |
| 7 | AC 05 | Lesson creation without Course is blocked. | Course | required | SF |
| 8 | AC 05 | Course stays fixed while the Available Teachers/Timeslot section scrolls. | Left sidebar | locked | SF |
| 9 | AC 05 | Japanese date format contains no slash. | Date display | computed | SF |
| 10 | AC 06 | Two lessons in one student-timeslot use the PBT's duplicate chip and alert pattern. | Calendar / sidebar | conditional | SF |
| 11 | AC 06 | One lesson in a student-timeslot uses normal rendering. | Calendar / sidebar | conditional | SF |
| 12 | AC 07 | Success opens the created Lesson Schedule detail; cancel/error do not redirect to Calendar. | Post-create navigation | computed | SF |

## Visual Source Mapping

| Area | Evidence | Required visual behavior |
|---|---|---|
| Student label | PBT-3607 `image-20260726-174001.png` | Calendar chip places the Subject before the Teacher name, for example `中国 (山田)`. |
| Course and scrolling | PBT-3607 `image-20260726-174911.png` | `Course *` stays above the red-marked scrollable Available Teachers/Timeslot area. |
| Duplicate lessons | PBT-3607 `image-20260726-175058.png` | Calendar shows `B限 ⚠ 2授業`; sidebar shows the warning `授業が重複しています(2件)` and a lesson detail entry. |
| Subject filter | PBT-3607 description and `image-20260726-173532.png` | Do not show a partial option list before a search term. |

## Conflict & Gap Analysis

| # | Tag | Source | AC | Description |
|---:|---|---|---|---|
| 1 | [REGRESSION RISK] | `epics/OOP/riso/LT-94698-subject-in-lesson-detail/test-coverage.md` | AC 01 | Existing Riso Calendar Subject filtering must retain search, selection, clear, and result filtering. |
| 2 | [REGRESSION RISK] | `epics/OOP/riso/LT-98529-lesson-note-timeslot-app/test-coverage.md` | AC 05 | Fixed Course must not conceal or corrupt scrollable Timeslot content. |
| 3 | [REGRESSION RISK] | `knowledge/e2e-scenario/e2e-scenarios.md`, E2E-01 | AC 07 | The create flow now lands on Schedule detail; Calendar verification remains a separate lifecycle step. |
| 4 | [MISSING BEHAVIOR] | Riso Subject is optional | AC 03 | The source does not define the fallback label when a lesson has no Subject. Coverage is limited to a populated Subject. |
| 5 | [MISSING BEHAVIOR] | PBT duplicate screenshot | AC 06 | The PBT defines the two-lesson visual state; behavior for three or more duplicate lessons is not specified. |

## Assumptions Made

- The PBT instruction “No options to be shown (so that user always enter some text)” selects the no-suggestions option for AC 01.
- PBT attachment screenshots are accepted as the visual requirement where the linked Figma file is unavailable through workspace tools.
- The Student label requirement is tested only for a lesson with a populated Subject; the Subject-blank fallback remains an uncovered clarification item.

## Related Specs

- `epics/OOP/riso/LT-94698-subject-in-lesson-detail/test-coverage.md` — Riso Subject and Calendar filter regression.
- `epics/OOP/riso/LT-98529-lesson-note-timeslot-app/test-coverage.md` — Timeslot display and blank-safe regression.
- `epics/lesson/LT-107960-duplicate-lesson-duration-validation/spec.md` — existing duplicate-lesson creation path.
