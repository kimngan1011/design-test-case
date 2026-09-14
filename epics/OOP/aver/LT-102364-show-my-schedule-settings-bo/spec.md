---
ticket_id: LT-102364
ticket_url: https://manabie.atlassian.net/browse/LT-102364
title: [Core][Aver] Show my schedule settings in BO
module: scheduling
bucket: OOP/aver
status: In Development
priority: Medium
fix_version: v2026.09.07
last_updated: 2026-08-25
---

# LT-102364: [Core][Aver] Show my schedule settings in BO

## Summary

This epic adds tenant/config control for the default "Show my schedule" behavior in Back Office scheduling surfaces.
Release notes describe the impacted behavior as the BO Lesson Calendar and Lesson List filter that previously defaulted to showing only lessons/events assigned to the logged-in teacher. The new config allows the default teacher filter to be removed, while the existing default remains ON unless the tenant requests the change.

## Sources Read

- Jira: `LT-102364` - `[Core][Aver] Show my schedule settings in BO`
- Jira: `PBT-3130` - `Show my schedule settings in BO`
- Confluence release notes: `[External]preprod 2026.06.29`, row for `LT-102364`
- `school-portal-admin/src/squads/calendar/stores/CalendarStore.ts`
- `school-portal-admin/src/squads/calendar/providers/CalendarFilterProvider.tsx`
- `school-portal-admin/src/squads/calendar/component-v2/FilterLessonOnCalendar/FilterTeacherSection/ShowMySchedule.tsx`
- `school-portal-admin/src/squads/calendar/domains/Calendar/components/Filters/FilterLessonOnCalendar/ShowMySchedule.tsx`
- `school-portal-admin/src/squads/lesson/domains/LessonManagement/components/Forms/FormFilterAdvancedLessonSF/FormFilterAdvancedLessonSF.tsx`
- `school-portal-admin/src/squads/lesson/domains/LessonManagement/hooks/useLimitTeacherAccessEnabled.ts`
- `knowledge/domain-knowledge/scheduling/calendar/access-by-user-type.md`

## Acceptance Criteria

### US 01 - Configure default BO Calendar teacher filtering

- AC 01.1: BO Calendar shows the `Show my schedule` filter only when BO calls the Salesforce lesson flow.
- AC 01.2: With the default behavior unchanged, `Show my schedule` is checked by default and the current user's teacher id is applied to the active teacher filter.
- AC 01.3: When `lesson.remove_default_teacher_filter.is_enabled` is enabled and `lesson.limit_teacher_access_other_lessons.is_enabled` is not active for the user, `Show my schedule` is unchecked by default and the current user's teacher id is not auto-applied.
- AC 01.4: When teacher access is limited, `Show my schedule` remains checked by default even if remove-default-teacher-filter is enabled.
- AC 01.5: Manual checking/unchecking of `Show my schedule` updates only the active teacher filter and keeps other filters intact.

### US 02 - Configure default BO Lesson List teacher filtering

- AC 02.1: Lesson List default filters include the current teacher when remove-default-teacher-filter is disabled.
- AC 02.2: Lesson List default filters do not include the current teacher when remove-default-teacher-filter is enabled and limit-teacher-access is not active.
- AC 02.3: For teacher/part-time-teacher users under limited teacher access, Lesson List keeps the current teacher as a mandatory filter on initialization, reset, and filter-chip deletion.
- AC 02.4: Once the user explicitly applies filters, saved dirty filters are respected and not overwritten by the defaulting plugin.

## Business Rules

| # | AC | Business Rule | Source |
|---|---|---|---|
| 1 | AC 01.1 | `Show my schedule` is rendered only when `isCallSFFromBO` is true. | `ShowMySchedule.tsx` |
| 2 | AC 01.2 | Calendar V2 default checked state is true when `lesson.lessonmgmt_sf.is_enabled` is true and remove-default-teacher-filter is false. | `CalendarStore.ts` |
| 3 | AC 01.3 | Calendar V2 default checked state becomes false when SF lesson flow is enabled, remove-default-teacher-filter is true, and limit-teacher-access is false. | `CalendarStore.ts` |
| 4 | AC 01.4 | Limit teacher access overrides remove-default-teacher-filter and keeps the default checked state true. | `CalendarStore.ts` |
| 5 | AC 01.5 | Checking `Show my schedule` appends the current user's id to active teacher ids; unchecking removes or stops auto-appending it. | `CalendarStore.ts`, `CalendarFilterProvider.tsx` |
| 6 | AC 02.1 | Lesson List non-dirty saved/default filters set `teachers = [{ id: userId, name: userName }]` when remove-default-teacher-filter is false. | `FormFilterAdvancedLessonSF.tsx` |
| 7 | AC 02.2 | Lesson List non-dirty saved/default filters set `teachers = []` when remove-default-teacher-filter is true and limit-teacher-access is false. | `FormFilterAdvancedLessonSF.tsx` |
| 8 | AC 02.3 | Limit teacher access applies only when the user is teacher or part-time teacher and forces the current teacher on reset/delete. | `useLimitTeacherAccessEnabled.ts`, `FormFilterAdvancedLessonSF.tsx` |
| 9 | AC 02.4 | `onFilterSubmit` marks filters dirty so later initialization does not overwrite user-selected filters. | `FormFilterAdvancedLessonSF.tsx` |

## Flag Matrix

| BO mode | `lesson.lessonmgmt_sf.is_enabled` | `lesson.remove_default_teacher_filter.is_enabled` | `lesson.limit_teacher_access_other_lessons.is_enabled` | User type | Expected default |
|---|---:|---:|---:|---|---|
| BO calling SF | ON | OFF | OFF | Staff/teacher | Show my schedule ON; current teacher applied |
| BO calling SF | ON | ON | OFF | Staff/teacher | Show my schedule OFF; current teacher not auto-applied |
| BO calling SF | ON | ON | ON | Teacher/part-time teacher | Show my schedule ON; current teacher mandatory |
| BO calling SF | ON | ON | ON | Non-teacher staff | Show my schedule OFF on Lesson List; Calendar follows global config |
| Pure SF app | Any | Any | Any | Any | Show my schedule control hidden or irrelevant |
| BO legacy non-SF lesson flow | OFF | Any | Any | Any | Show my schedule control hidden or false |

## Conflict & Gap Analysis

| # | Tag | Source | Description |
|---|---|---|---|
| 1 | [REGRESSION RISK] | `CalendarFilterProvider.tsx` | The legacy Calendar provider still defaults `showMySchedule` to true for BO-calling-SF and does not read `lesson.remove_default_teacher_filter.is_enabled`; if legacy Calendar is still reachable, this epic can fail there. |
| 2 | [REGRESSION RISK] | Release notes vs code | Release notes mention "lessons/events assigned to the user"; Calendar teacher filtering can affect both lesson and activity event display because activity events also have teacher ids. |
| 3 | [PERMISSION RISK] | `useLimitTeacherAccessEnabled.ts` | Limit-teacher-access behavior depends on both feature flag and logged-in role being teacher or part-time teacher, not only the feature flag. |
| 4 | [PERSISTENCE RISK] | `FormFilterAdvancedLessonSF.tsx` | Lesson List only applies default teacher mutation when saved filter is not dirty; existing user-saved filters must not be silently changed. |
| 5 | [SCOPE GAP] | Jira description empty | Jira does not define exact tenant rollout, UI copy change, or whether legacy Calendar must be updated in addition to Calendar V2. |

## Clarification Questions

1. Should the legacy Calendar provider also honor `lesson.remove_default_teacher_filter.is_enabled`, or is LT-102364 scoped only to Calendar V2?
2. For non-teacher staff when `lesson.limit_teacher_access_other_lessons.is_enabled` is ON, should Calendar default ON globally or only teacher/part-time-teacher should be forced?
3. Should "Show my schedule" affect activity events exactly the same way as lessons when the activity event has teacher ids?

## Related Existing Knowledge

- `knowledge/domain-knowledge/scheduling/calendar/access-by-user-type.md` - Aver CPU teachers see assigned lessons; SPU users see lessons by affiliated locations.
- `knowledge/domain-knowledge/scheduling/scheduling-feature-permission-matrix.csv` - Scheduling permission and feature matrix by tenant/role.

## QASE Coverage Target

- Suite target used for CSV: `Calendar lesson` (`suite_id=2717`, `suite_parent_id=2628`) for Calendar-facing cases.
- Lesson List cases are included in the same import CSV with tags `Lesson List` and can be moved to a dedicated Lesson Management suite during Qase upload if desired.

## QASE Posting

- Suite: `Calendar lesson` - https://app.qase.io/project/PX?suite=2717
- Created cases: `PX-27175` through `PX-27188`
- Test run: https://app.qase.io/run/PX/dashboard/3458
- Imported case count: 14

> Posted status: posted on 2026-08-26
