---
ticket_id: LT-111303
ticket_url: https://manabie.atlassian.net/browse/LT-111303
title: "[ERPv2] [Lesson Calendar] Blue divider between Student panel and Calendar is draggable/resizable (should be static border only)"
module: scheduling
bucket: calendar
status: New
internal_uat_date: null
production_release_date: null
last_updated: 2026-09-18
---

# LT-111303: Static Student Panel Divider on Lesson Calendar

## Summary

On Salesforce Lesson Calendar, the blue vertical divider between the left Student panel and the main Calendar panel is currently draggable. Dragging the divider resizes both panels. This is incorrect: the divider must be a static visual border only.

The existing collapse/expand control is the small arrow toggle in the white column next to the divider. That toggle remains the only supported way to hide or show the Student panel.

## Acceptance Criteria

### AC 01 - Blue divider is static

- The blue vertical divider between the Student panel and the Calendar panel is not draggable.
- Mouse drag, touch drag, and pointer drag on the divider do not change Student panel width or Calendar panel width.
- The divider does not behave as a resize handle.

### AC 02 - Arrow toggle remains the only collapse/expand control

- Clicking the arrow toggle collapses the Student panel.
- Clicking the arrow toggle again expands the Student panel.
- Collapse/expand does not require dragging the divider.
- The Calendar panel reflows correctly after collapse and expand.

### AC 03 - Existing Calendar behavior is not impacted

- Daily and Weekly Lesson Calendar views remain usable after the divider fix.
- Student search/list, filters, lesson card selection, and the right-side detail drawer continue to work.
- No horizontal overflow, clipped content, or panel overlap appears after collapse/expand or page resize.

## Business Rules

| # | AC | Business Rule | UI Element | Expected Behavior | Platform |
|---|---|---|---|---|---|
| 1 | AC 01 | Divider is a visual border only | Blue vertical divider between Student panel and Calendar | Static, non-draggable, no panel resize | SF |
| 2 | AC 01 | Dragging divider must not mutate layout state | Student panel width, Calendar panel width | Width remains unchanged after attempted drag | SF |
| 3 | AC 02 | Collapse/expand is controlled only by the arrow toggle | White-column arrow toggle | Collapses/expands Student panel | SF |
| 4 | AC 03 | Calendar content must reflow safely | Daily/Weekly calendar grid and lesson cards | No overlap, no clipped grid, selected detail still opens | SF |
| 5 | AC 03 | Student panel interactions remain available when expanded | Student search, Student List accordion, student checkbox | Existing interactions still work | SF |

## Impact Analysis

| Area | Impact | Regression Guardrail |
|---|---|---|
| Lesson Calendar layout shell | Divider behavior changes from draggable/resizable to static border | Measure left panel and calendar panel width before and after pointer drag |
| Student panel collapse state | Existing arrow toggle must remain functional | Verify collapse and expand through the arrow only |
| Calendar grid | Removing resize behavior must not break daily/weekly layout calculation | Check visible grid, date navigation, view switch, and lesson selection |
| Detail drawer | Right-side detail drawer shares horizontal space with Calendar | Open lesson detail before/after attempted divider drag |
| Responsive layout | Static divider must stay aligned after browser resize/zoom | Verify no panel overlap or horizontal scroll at common desktop widths |

## Related Files / Context

- `school-portal-admin/src/squads/calendar/domains/CalendarV2/CalendarSF/IndividualCalendar.tsx` - Salesforce Lesson Calendar surface and Calendar container.
- `school-portal-admin/src/squads/calendar/domains/CalendarV2/CalendarSF/LessonMaster.tsx` - Salesforce Lesson Master calendar layout reference.
- `school-portal-admin/src/squads/calendar/domains/CalendarV2/Calendar/components/ManaCalendar/` - Daily/Weekly calendar grid components.
- Jira attachment `image-20260918-115031.png` shows the affected divider between the Student panel and Calendar panel.

## Assumptions Made

- This is a core Salesforce Lesson Calendar bug because the ticket is not tenant-specific and the affected environment is Staging ERP SF & BO.
- Automation can identify the panels by visible landmarks: `Student`, `Student List`, the blue divider/white toggle column, and `Calendar__container` or the visible Calendar grid.
- A width tolerance of 2 px is acceptable for browser rendering differences when asserting no resize after drag.
