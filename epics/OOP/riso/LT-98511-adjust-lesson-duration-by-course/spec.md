---
ticket_id: LT-98511
ticket_url: https://manabie.atlassian.net/browse/LT-98511
title: "[Riso] Core | Adjust lesson duration (mins) by Course"
module: scheduling
bucket: oop-riso
status: Ready for QA
target_release: v2026.10.05
last_updated: 2026-09-18
prd_url: https://manabie.atlassian.net/wiki/spaces/PRDM/pages/2423914539/WIP+Riso+OOP+Adjust+Lesson+Duration+by+Course
---

# LT-98511: Adjust Lesson Duration by Course

## Summary

Riso mostly uses 80-minute lessons, but some younger-student courses require shorter lessons such as 50 minutes. This feature adds an optional duration value to Location Course so lesson creation can automatically set lesson duration based on the selected course.

The Salesforce field is `Location_Course__c.Location_Duration__c` with label `Location Duration`, inline help `Minutes`, precision 4, scale 0, and `required=false`. The field is displayed on the Location Course record page only when `Location_Course__c.Is_Show_Location_Duration__c` is true. That formula reads `$Setup.Lesson_Custom_Settings__c.config_Lesson_Location_Lesson_Duration__c`.

## Acceptance Criteria

### AC-01 - Configure Lesson Duration on Location Course

- Location Course has an optional Lesson Duration / Location Duration field.
- Default value remains blank.
- Saved duration value can be retrieved when the Location Course is selected during lesson creation.
- Field visibility follows `config_Lesson_Location_Lesson_Duration`.

### AC-02 - Populate Duration in real time

- During lesson creation, Duration updates when Timeslot and/or Location Course changes.
- If selected Location Course has `Location_Duration__c`, that value overrides the timeslot-derived duration.
- If selected Location Course has blank duration and Timeslot is selected, Duration uses the timeslot duration.
- If neither source provides duration, the form follows the existing default/manual behavior.

### AC-03 - Manual override remains possible

- Duration remains editable.
- Start Time remains editable.
- End Time remains editable.
- Manual values remain as entered until the user changes Timeslot or Location Course.

### AC-04 - Recalculate after source field changes

- Manual Duration does not block recalculation.
- Changing Timeslot recalculates Duration from the latest selected values.
- Changing Location Course recalculates Duration from the latest selected values.

## Business Rules

| # | AC | Business Rule | Field / Source | Expected Behavior |
|---|---|---|---|---|
| 1 | AC-01 | Location Course duration is optional | `Location_Course__c.Location_Duration__c` | Blank by default; no required validation |
| 2 | AC-01 | Config controls field visibility | `config_Lesson_Location_Lesson_Duration__c` via `Is_Show_Location_Duration__c` | Riso ON shows field; non-Riso/OFF hides feature |
| 3 | AC-02 | Course duration has highest priority | Location Course duration = 50, timeslot = 80 | Lesson Duration = 50 |
| 4 | AC-02 | Timeslot fallback | Location Course duration blank, timeslot = 80 | Lesson Duration = 80 |
| 5 | AC-02 | No source fallback | Location Course duration blank and no timeslot | Existing default/manual behavior, no forced course duration |
| 6 | AC-03 | Manual override is allowed | Duration, Start Time, End Time | Editable and retained until source changes |
| 7 | AC-04 | Timeslot/source changes recalculate | Timeslot changed after manual edit | Duration and derived time are recalculated |
| 8 | AC-04 | Course/source changes recalculate | Location Course changed after manual edit | Duration and derived time are recalculated |

## Impact Analysis

| Area | Impact | Regression Guardrail |
|---|---|---|
| Location Course UI | New optional Location Duration field is visible only when config ON | Verify visibility, blank default, save, and reload |
| Lesson Course lookup | Course option carries `MANAERP__Location_Duration__c` to the lesson form | Select course with duration and assert form Duration |
| Lesson time calculation | Course duration overrides timeslot duration | Use 80-minute timeslot + 50-minute course |
| Manual edits | Staff can still edit Duration/Start/End Time | Verify manual value remains before source change |
| Source recalculation | Timeslot or Location Course changes overwrite old manual values | Verify both change directions |
| Partner scope | Non-Riso/OFF config should preserve current behavior | Verify field hidden and timeslot logic unaffected |

## Related Files / Evidence

- PRD: `Riso | OOP | Adjust Lesson Duration by Course`
- `erp-salesforce/packages/master/main/default/objects/Location_Course__c/fields/Location_Duration__c.field-meta.xml`
- `erp-salesforce/packages/master/main/default/objects/Location_Course__c/fields/Is_Show_Location_Duration__c.field-meta.xml`
- `erp-salesforce/packages/master-ext/main/default/flexipages/Location_Course_Record_Page_Ext.flexipage-meta.xml`
- `erp-salesforce/packages/lesson/main/default/lwc/lookupCourseOnLesson/lookupCourseOnLesson.js`
- `erp-salesforce/packages/lesson/main/default/lwc/formLesson/formLesson.js`

## Assumptions

- The business-facing PRD calls the field "Lesson Duration"; the Salesforce API/metadata name is `Location_Duration__c` and UI label is `Location Duration`.
- Duration is in minutes and accepts positive integer values due to field scale 0 and existing lesson duration validation.
- Test data should use a clear boundary such as Timeslot 09:00-10:20 = 80 minutes and Location Course Duration = 50 minutes.
