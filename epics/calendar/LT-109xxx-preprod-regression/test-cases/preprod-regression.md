# Test Cases: LT-109754 / LT-109576 / LT-109520 Preprod Regression

## LT-109754 - Timeslot classroom-axis DnD keeps only target classroom in Edit Lesson popup

**Description:** Regression for LT-109754. In Riso extUAT Timeslot view > Daily view > Classroom axis, dragging a lesson from one classroom to another must prefill only the target classroom in the Edit Lesson popup and must not create duplicate classroom assignment after saving.

**Preconditions:**
- Environment: Riso extUAT.
- Enable Calendar Drag And Drop = ON.
- Timeslot view is enabled.
- Lesson L1 exists in Timeslot view Daily > Classroom axis.
- L1 is assigned to exactly one original classroom `Classroom A`.
- Target classroom `Classroom B` exists in the same date/timeslot and is selectable.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Lesson Calendar > Timeslot view > Daily view > Classroom axis. | Calendar loads and L1 is displayed under `Classroom A`. | date = L1 date; view = Timeslot Daily; axis = Classroom |
| 2 | Drag L1 from `Classroom A` to `Classroom B`. | Edit Lesson popup opens. | source classroom = Classroom A; target classroom = Classroom B |
| 3 | Inspect the Classrooms field before clicking Save. | Classrooms field contains only `Classroom B`; `Classroom A` is not pre-populated. | expected chips = [Classroom B] |
| 4 | Click Save without manually changing the Classrooms field. | Save succeeds. |  |
| 5 | Refresh Calendar and reopen L1 detail. | L1 is assigned only to `Classroom B`; no duplicate classroom assignment remains on the lesson. | expected final classrooms = [Classroom B] |

**Severity:** critical
**Priority:** high

---

## LT-109576 - Learner App shows Lesson Note Available tag and Lesson Note detail

**Description:** Regression for LT-109576. When a Lesson has Lesson Note from the School populated, the Learner App must show the note-available tag on the Lesson Card and the note content on Lesson Detail.

**Preconditions:**
- Environment: UAT sandbox `riso-kyoiku--extuat`.
- Student `26000002` can log in to Learner App.
- Lesson L1 is assigned to Student `26000002`.
- L1 has `Lesson Note from the School` / `Lesson_Note__c` populated.
- L1 is visible on the student's App Calendar.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open the Lesson record in SF and confirm Lesson Note from the School is populated. | Lesson Note value exists on the Lesson record. | field = Lesson_Note__c |
| 2 | Log in to Learner App as Student `26000002`. | Student logs in successfully. | student = 26000002 |
| 3 | Navigate to Calendar and locate L1 Lesson Card. | L1 card is visible. | lesson = L1 |
| 4 | Inspect the bottom area of the Lesson Card. | `Lesson Note Available` tag is displayed; in JP locale, `教室からのお知らせあり` is displayed. | expected tag |
| 5 | Open L1 Lesson Detail. | Lesson Detail opens. |  |
| 6 | Inspect the top Lesson Note section. | `Lesson Note` / `教室からのお知らせ` section is displayed with the exact note content from the Lesson record. | expected note content |

**Severity:** critical
**Priority:** high

---

## LT-109520 - BO Calendar Lesson popup follows new UI layout

**Description:** Regression for LT-109520. BO Calendar Lesson popup must match the new Lesson UI layout from LT-101769, including Cancellation Reason and Recurring Settings sections.

**Preconditions:**
- Logged in to BO as HQ/CM user with Lesson Calendar access.
- New Lesson UI layout feature from LT-101769 is enabled.
- BO Calendar is accessible.
- At least one editable lesson exists for edit-popup validation.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open BO Calendar. | Calendar loads successfully. | surface = BO Calendar |
| 2 | Click Add Lesson or open an editable Lesson from Calendar. | Lesson popup opens using the new UI layout. | action = add/edit |
| 3 | Compare the popup structure with LT-101769 Figma layout. | Fields are arranged according to the new layout; spacing/section grouping does not fall back to the old layout. | Figma node = 12148-60157 |
| 4 | Inspect the Cancellation Reason section where applicable. | Cancellation Reason section is present/placed according to the new layout when the lesson status/action requires it. | section = Cancellation Reason |
| 5 | Inspect Recurring Settings for a recurring lesson/create recurring flow. | Recurring Settings section is present/placed according to the new layout. | section = Recurring Settings |
| 6 | Save/cancel the popup. | Existing add/edit flow still works and no layout-only change blocks the action. | regression = existing flow |

**Severity:** major
**Priority:** high
