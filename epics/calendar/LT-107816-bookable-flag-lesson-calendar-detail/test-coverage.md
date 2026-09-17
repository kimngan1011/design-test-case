# Test Coverage: LT-107816 - Display Bookable Flag on Lesson Calendar Details Screen

## New Test Suite Recommendation

- Qase parent suite: `PX > ... > Calendar lesson` (`suite_id=2717`)
- New child suite suggestion: `Bookable Flag on Lesson Calendar Detail (LT-107816)`

## Coverage Matrix

| Area | Coverage |
|---|---|
| Calendar detail visibility | Opening a lesson from Lesson Calendar shows `Bookable Flag` when Lesson Booking setting is enabled. |
| True value display | `Bookable_Flag__c = TRUE` renders the check icon in the Calendar detail panel. |
| False/null value display | `Bookable_Flag__c = FALSE` or null renders `--`, not a check icon. |
| Feature setting guard | `Lesson_Booking__c = FALSE` hides the Bookable Flag row even if lesson data is true. |
| Refresh after update | Changing Bookable Flag through edit flow refreshes Calendar detail value after save. |
| Collapsible detail variant | `lessonDetailCollapsible` uses the same field mapping and value display as the main Calendar right panel. |

## Existing Qase Testcases

No direct testcase for `LT-107816` or Bookable Flag on **Lesson Calendar detail screen** was found.

Related existing Qase cases:

- `PX-21815` - Lesson Detail page - Flag field visible in Detail section
- `PX-21816` - Lesson Detail page - Staff with edit permission turns flag ON saves
- `PX-21817` - Lesson Detail page - Staff turns flag OFF existing sessions unaffected
- `PX-21819` - Lesson New modal - Flag visible defaults OFF
- `PX-21820` - Lesson New modal - Create lesson with flag ON
- `PX-21821` - Lesson Edit modal - Flag reflects current value and can be toggled
- `PX-20863` - Lesson Lists - Bookable Flag OFF lesson hidden
- `PX-20933` - Bookable Flag change history tracked in Salesforce

Impact assessment:

- `PX-21815` to `PX-21821` are adjacent but do not cover the Lesson Calendar right panel/collapsible detail implementation from LT-107816.
- `PX-20863` and other Lesson Lists cases validate Learner App visibility, not Salesforce Calendar detail display.

