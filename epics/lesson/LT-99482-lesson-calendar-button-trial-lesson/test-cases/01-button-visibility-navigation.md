# Test Cases: LT-99482 - Add Lesson Calendar button to Trial Lesson page

## Suite: LT-99482 - Button Visibility and Navigation

### Trial Lesson Detail - Lesson Calendar Entry - SF Trial Lesson Detail - Eligible Record - Button Displayed

**Description:** AC 01.1 - Component - Lesson Calendar button is visible on Trial Lesson detail for SF user flow.

**Preconditions:**
- Actor is logged in to Salesforce as HQ or CM Staff.
- Trial Lesson TL-1001 exists with status Open and linked student STU-001.
- User can open Trial Lesson detail page.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Trial Lesson TL-1001 detail page in Salesforce. | Trial Lesson detail page loads. | trial_lesson = TL-1001 |
| 2 | Observe the action/navigation area on the detail page. | Lesson Calendar button is visible and enabled. | expected_button = Lesson Calendar |
| 3 | Hover or focus on Lesson Calendar button. | Button remains interactive with no disabled state. | expected_state = enabled |

**Severity:** major
**Priority:** high

---

### Trial Lesson Detail - Lesson Calendar Entry - Button Interaction - User Selects Button - Calendar Page Opened

**Description:** AC 01.2 - State Transition - Clicking Lesson Calendar from Trial Lesson detail opens Lesson Calendar destination.

**Preconditions:**
- Actor is logged in to Salesforce as HQ or CM Staff.
- Trial Lesson TL-1001 detail page is open.
- Lesson Calendar feature is accessible in current org.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Click Lesson Calendar button from Trial Lesson TL-1001 detail page. | Navigation is triggered from Trial Lesson detail context. | source_page = trial_lesson_detail |
| 2 | Wait for destination page load completion. | Lesson Calendar page is displayed. | destination_page = lesson_calendar |
| 3 | Read page header and route indicator. | Header and route indicate Lesson Calendar, not Trial Lesson detail. | expected_header = Lesson Calendar |

**Severity:** major
**Priority:** high

---

### Trial Lesson Detail - Lesson Calendar Entry - Repeated Access - Button Clicked Twice - Navigation Remains Stable

**Description:** AC 01.2 - Regression - Repeated use of Lesson Calendar button does not break navigation behavior.

**Preconditions:**
- Actor is logged in to Salesforce as HQ or CM Staff.
- Trial Lesson TL-1002 exists and detail page is accessible.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Trial Lesson TL-1002 detail page and click Lesson Calendar. | Lesson Calendar opens from Trial Lesson context. | trial_lesson = TL-1002 |
| 2 | Navigate back to TL-1002 detail page using browser/app back. | Trial Lesson detail page is shown again. | navigation = back |
| 3 | Click Lesson Calendar again. | Lesson Calendar opens again without route error or blank state. | attempt = second_click |

**Severity:** minor
**Priority:** medium
