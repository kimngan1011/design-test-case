---
ticket_id: LT-98529
ticket_url: https://manabie.atlassian.net/browse/LT-98529
title: "[Riso] Core | Lesson Note and Timeslot (App)"
module: scheduling/lesson-management
bucket: OOP/riso
status: Ready for QA
priority: High
linked_pbt: PBT-1927
qa_ticket: LT-106142
target_uat: 2026-06-30
last_updated: 2026-08-26
---

# LT-98529: [Riso] Core | Lesson Note and Timeslot (App)

## Summary

This epic adds a direct Lesson-level announcement field and Timeslot display to learner-facing App schedule surfaces. Staff can create/edit `Lesson Note` from SF or BO. Students and parents can see a note-available tag on App Calendar lesson cards and the full note on App Lesson Detail. Timeslot is displayed on App lesson cards and detail only when Timeslot display is enabled and the lesson has a Timeslot.

The PRD says this is a CORE build for all partners without partner-specific config for Lesson Note. Visibility is value-driven: blank Lesson Note hides the App note block/tag so existing partners keep current UI when they do not use the field.

## Sources Read

- Jira `LT-98529` - `[Riso] Core | Lesson Note and Timeslot (App)`
- Jira `PBT-1927` - original epic and approach notes
- Jira `LT-106142` - QA task for testcase/testing
- Confluence PRD `Riso | Core | Lesson Note and Timeslot (App)` page `2422767817`
- `erp-salesforce/packages/lesson/main/default/objects/Lesson__c/fields/Lesson_Note__c.field-meta.xml`
- `erp-salesforce/packages/lesson/main/default/objects/Lesson__c/fields/Timeslot__c.field-meta.xml`
- `erp-salesforce/packages/lesson/main/default/objects/Lesson__c/fields/Lesson_Timeslot__c.field-meta.xml`
- `erp-salesforce/packages/lesson/main/default/objects/Lesson__c/fields/Show_Timeslot_In_Lesson__c.field-meta.xml`
- `erp-salesforce/packages/lesson/main/default/lwc/formLesson/formLesson.html`
- `erp-salesforce/packages/lesson/main/default/lwc/formLessonOnLessonSchedule/formLessonOnLessonSchedule.html`
- `erp-salesforce/packages/lesson/main/default/lwc/lessonDetail/lessonDetail.html`
- `erp-salesforce/packages/lesson/main/default/classes/LessonUpdateProcessor.cls`
- `school-portal-admin/src/squads/lesson/domains/LessonManagement/components/Forms/FormLessonUpsert/FormLessonUpsertControlledSF.tsx`
- `school-portal-admin/src/squads/lesson/pages/LessonManagement/components/DetailSections/DetailSectionLessonGeneralInfo/DetailSectionLessonGeneralInfoSF.tsx`
- Existing related specs: `LT-98530` Lesson History App and `LT-92536` Daily Timetable Print

## Acceptance Criteria

### US01 - Create/Edit Lesson Note in SF and BO

| ID | Feature | Acceptance Criteria |
|---|---|---|
| US01.1 | Field Display | `Lesson Note` is displayed on SF and BO lesson detail/edit screens as a Long Text Area, max 32,768 characters, optional. |
| US01.2 | Edit Permissions | Field follows existing Lesson object permissions. |
| US01.3 | Save Behavior | Saved note is immediately reflected in App; blank note hides App note UI. |
| US01.4 | Lesson Calendar Display | Lesson Note is shown in Lesson Calendar information. |

### US02 - View Lesson Note in App

| ID | Feature | Acceptance Criteria |
|---|---|---|
| US02.1 | Calendar Card Tag | App Calendar lesson card shows `Lesson Note Available` / `教室からのお知らせあり` when Lesson Note is entered; tag is hidden when Lesson Note is blank. |
| US02.2 | Lesson Detail Note | App Lesson Detail shows a dedicated section at the top with note icon + `Lesson Note` / `教室からのお知らせ`; content is plain text, read-only, and preserves line breaks; entire section is hidden when blank. |

### US03 - Timeslot Display in App

| ID | Feature | Acceptance Criteria |
|---|---|---|
| US03.1 | Calendar Card Timeslot | When Timeslot display is enabled in partner config and the lesson has Timeslot, card time displays `[Start Time] - [End Time] ([Timeslot Name])`; hide Timeslot name when blank. |
| US03.2 | Lesson Detail Timeslot | App Lesson Detail Basic Info shows `Timeslot` / `時限` under Time; hide the row when Timeslot is not set, or apply the same no-blank visual rule as card. |

## Business Rules

| # | AC | Business Rule | Field/Config | Platform |
|---|---|---|---|---|
| BR-01 | US01.1 | Lesson Note is stored directly on Lesson, not Lesson Report. | `Lesson__c.Lesson_Note__c` | SF/BO/App |
| BR-02 | US01.1 | Lesson Note is Long Text Area length 32,768 and optional. | `Lesson_Note__c` | SF/BO |
| BR-03 | US01.1 | SF Lesson page field is controlled by `Show_Lesson_Note__c` formula/custom setting. | `Lesson_Custom_Settings__c.Show_Lesson_Note__c` | SF |
| BR-04 | US01.1 | BO Lesson form uses `lesson.lesson_note.is_enabled` to render the field. | feature setting | BO |
| BR-05 | US01.2 | Read/write follows existing Lesson object and field permissions. | permission sets | SF/BO |
| BR-06 | US01.3 | Saved note is sent in lesson upsert/update payload as `lessonNote`. | `UpsertLessonParams.lessonNote` | SF/BO backend |
| BR-07 | US01.3 | Blank note hides App tag and App detail section. | value-driven display | App |
| BR-08 | US01.4 | Calendar lesson information includes Lesson Note when configured and value exists. | `Lesson_Note__c` | SF Calendar |
| BR-09 | US02.1 | App Calendar card tag label is `Lesson Note Available` in EN and `教室からのお知らせあり` in JP. | i18n | App |
| BR-10 | US02.2 | App detail section label is `Lesson Note` in EN and `教室からのお知らせ` in JP. | i18n | App |
| BR-11 | US02.2 | Lesson Note content is plain text, not rich text; line breaks are reflected. | `Lesson_Note__c` | App |
| BR-12 | US03.1 | App card Timeslot appears only when partner Timeslot display is enabled and lesson has Timeslot. | `Show_Timeslot_In_Lesson__c`, `Timeslot__c` | App |
| BR-13 | US03.1 | App card Timeslot format is `09:00 - 10:00 (TimeSlot S)`. | start/end + timeslot name | App |
| BR-14 | US03.2 | App detail Basic Info shows `Timeslot` / `時限` under Time when available. | timeslot name | App |
| BR-15 | US03.2 | Timeslot row/name is hidden or visually blank-safe when `Timeslot__c` is empty. | `Timeslot__c` | App |

## Conflict & Gap Analysis

| # | Tag | Source | Description |
|---|---|---|---|
| 1 | [CONFIG GAP] | PRD section 6 vs code | PRD says Lesson Note is CORE without partner-specific config, but code has SF custom setting `Show_Lesson_Note__c` and BO feature setting `lesson.lesson_note.is_enabled`; tests must verify both enabled and disabled paths. |
| 2 | [FORMAT RISK] | `Lesson_Timeslot__c` formula vs PRD | Salesforce formula displays `Name (HH:mm ~ HH:mm)`, while App card PRD expects `Start - End (Timeslot Name)`. App tests must assert PRD format, not SF formula format. |
| 3 | [BLANK RISK] | PRD hide rules | Requirement says hide when blank. It does not define whitespace-only note handling; testcase treats whitespace-only as blank expectation to catch awkward empty tags. |
| 4 | [DATA SYNC RISK] | `LessonUpdateProcessor.cls` | Existing update path only writes `Lesson_Note__c` when `params.lessonNote != null`; clearing note must send an explicit empty string/null-safe value. |
| 5 | [CROSS-FEATURE RISK] | LT-98530 Lesson History | Timeslot is already displayed in Lesson History. LT-98529 App Calendar/Detail changes must not regress Lesson History row display. |
| 6 | [SCOPE GAP] | PRD | PRD says Parent or Student but does not explicitly restate multi-child parent scoping; tests reuse existing selected-child/access rules. |

## Clarification Questions

1. Should whitespace-only Lesson Note be treated as blank and hide the App tag/detail section?
2. When `Show_Lesson_Note__c` / `lesson.lesson_note.is_enabled` is disabled but an old note value exists, should App still display the note, or is the App also gated by config?
3. Should Timeslot display depend on active Timeslot Master status after the lesson already references it, or only on lesson `Timeslot__c` value and partner config?
4. For recurring lesson creation/edit, should Lesson Note be copied to all created/updated occurrences or only the selected lesson based on the saving method?

## Related Specs

- `epics/OOP/riso/LT-98530-contract-monthly-lesson-history-app/spec.md` - App Lesson History already displays lesson time + Timeslot name.
- `epics/calendar/LT-92536-daily-timetable-print/spec.md` - Timeslot display/config behavior for SF Daily Timetable Print.
- `epics/OOP/riso/LT-94698-subject-in-lesson-detail/test-cases/` - Nearby Riso Lesson Detail display/import style.

## QASE Coverage Target

- Suggested target suite: create a new suite `[Riso] Lesson Note & Timeslot (App)` under the Riso/App area.
- CSV currently uses suite `3253` (`[Riso] Lesson History — Display & Navigation`) as the closest existing App display suite so it remains importable without inventing an unknown Qase id.

> Posted status: not posted
