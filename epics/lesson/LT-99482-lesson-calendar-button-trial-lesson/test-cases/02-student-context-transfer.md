# Test Cases: LT-99482 - Add Lesson Calendar button to Trial Lesson page

## Suite: LT-99482 - Student Context Transfer

### Trial Lesson to Calendar - Student Context - Single Student Trial Lesson - Student Pre-Selected on Calendar

**Description:** AC 01.3 - Decision Table - Student from Trial Lesson is auto-selected when calendar opens via Lesson Calendar button.

**Preconditions:**
- Actor is logged in to Salesforce as HQ or CM Staff.
- Trial Lesson TL-2001 has linked student STU-010 (name: Aki Tanaka).
- TL-2001 detail page is open before test.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Click Lesson Calendar button on Trial Lesson TL-2001 detail page. | Lesson Calendar page loads from Trial Lesson context. | trial_lesson = TL-2001 |
| 2 | Open student selection/filter panel on Lesson Calendar. | Student STU-010 is already selected in panel context. | expected_student_id = STU-010 |
| 3 | Inspect selected student chip/row and compare with trial lesson student info. | Selected student matches Aki Tanaka (STU-010). | expected_student_name = Aki Tanaka |

**Severity:** critical
**Priority:** high

---

### Trial Lesson to Calendar - Student Context - Selection Persistence - Calendar Grid and Filter Show Same Student Context

**Description:** AC 01.3 - Data Integrity - Calendar grid context and student filter context remain aligned after Trial Lesson navigation.

**Preconditions:**
- Actor is logged in to Salesforce as HQ or CM Staff.
- Trial Lesson TL-2002 has linked student STU-011 (name: Emi Sato).
- TL-2002 detail page is open.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Click Lesson Calendar on Trial Lesson TL-2002 detail. | Lesson Calendar opens. | trial_lesson = TL-2002 |
| 2 | Capture selected student from filter panel. | Filter panel selected student is STU-011. | panel_student = STU-011 |
| 3 | Validate calendar student-context indicator for active selection. | Calendar context indicator also points to STU-011. | grid_context_student = STU-011 |

**Severity:** critical
**Priority:** high

---

### Trial Lesson to Calendar - Assignment Continuation - Context Kept - User Proceeds Without Manual Student Re-Selection

**Description:** AC 01.4 - Scenario - User can continue assignment flow from transferred student context without manually finding same student again.

**Preconditions:**
- Actor is logged in to Salesforce as HQ or CM Staff.
- Trial Lesson TL-2003 has linked student STU-012 and assignable lesson slot exists in calendar period.
- TL-2003 detail page is open.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Click Lesson Calendar button from Trial Lesson TL-2003 detail. | Lesson Calendar opens with student context initialized. | trial_lesson = TL-2003 |
| 2 | Start assignment flow from calendar for currently selected student. | Assignment flow starts directly for STU-012. | expected_student = STU-012 |
| 3 | Review flow inputs before confirmation step. | No manual student search/re-selection is required for STU-012. | expected_manual_reselect = no |

**Severity:** critical
**Priority:** high
