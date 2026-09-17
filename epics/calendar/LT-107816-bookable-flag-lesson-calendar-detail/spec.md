# LT-107816 - Display Bookable Flag on Lesson Calendar Details Screen

## Sources

- Jira: https://manabie.atlassian.net/browse/LT-107816
- ERP-Salesforce commit: `4094ba67dd` - `[LT-107816] feat: display Bookable Flag on lesson detail in Lesson Calendar (#22180)`
- Jira description Slack link could not be read by the active Slack connector because it points to a different Slack workspace/channel (`manabie.slack.com`, channel `C080P3YK2PJ`).

## Objective

Show the lesson `Bookable Flag` value in the Lesson Calendar lesson detail panel so support/staff users can confirm whether a lesson is bookable without navigating away from the Calendar.

## Implementation Notes

- `splitViewRightManaCalendar.js` now loads `Lesson__c.Bookable_Flag__c` through `getRecord`.
- The loaded value is mapped into `selectedLesson.bookableFlag`.
- `lessonDetailCollapsible.js` also loads and maps `Bookable_Flag__c`.
- `lessonDetail.js` reads `Lesson_Custom_Settings__c.Lesson_Booking__c` and stores it as `isShowBookableFlag`.
- When `isShowBookableFlag` is true:
  - The detail panel shows the `Bookable Flag` row.
  - `record.bookableFlag = true` displays a `utility:check` icon.
  - `record.bookableFlag = false` or null displays `--`.
- When `Lesson_Booking__c` is false, the `Bookable Flag` row is hidden.

## Out of Scope

- Bookable Flag create/edit behavior in Lesson form. Existing Qase suite `2884` covers SF Lesson Detail & Modal for LT-102170.
- Learner App booking visibility and reserve button rules. Existing Nichibei Lesson Booking suites cover those flows.

