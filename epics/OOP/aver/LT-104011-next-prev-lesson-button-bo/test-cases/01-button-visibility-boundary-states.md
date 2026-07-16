# Test Cases: LT-104011 - Add Next and Prev lesson button in BO

## Suite: [Aver] BO Lesson Detail Navigation - Button Visibility and Boundary States

### [Aver] Lesson Detail Navigation - Action Area - Middle recurring lesson - Previous Lesson and Next Lesson enabled

**Description:** AC 01.1 / AC 01.3 - Decision Table - Middle lesson in a recurring chain shows both lesson-navigation buttons as active controls on BO Lesson Detail.

**Preconditions:**
- Logged in to Back Office as HQ or CM Staff with access to Aver lesson detail.
- Recurring lesson chain RC-1001 exists with three lessons: LES-1001 (first), LES-1002 (middle), LES-1003 (last).
- LES-1002 detail page is open in BO Lesson Detail view mode.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open BO Lesson Detail for LES-1002 in the recurring chain. | Lesson Detail page for LES-1002 loads without redirecting to another surface. | recurring_chain = RC-1001; lesson = LES-1002 |
| 2 | Observe the top action area of Lesson Detail. | `Previous Lesson` and `Next Lesson` buttons are both visible in the action area. | expected_buttons = Previous Lesson, Next Lesson |
| 3 | Hover or focus on both lesson-navigation buttons. | Both buttons remain enabled and interactive. | expected_state = enabled |

**Severity:** major
**Priority:** high

---

### [Aver] Lesson Detail Navigation - Boundary State - First recurring lesson - Previous Lesson disabled

**Description:** AC 01.4 - Boundary Value Analysis - First lesson in the recurring chain disables backward navigation while preserving forward navigation.

**Preconditions:**
- Logged in to Back Office as HQ or CM Staff with access to Aver lesson detail.
- Recurring lesson chain RC-1001 exists with LES-1001 as the first lesson and LES-1002 as the next lesson.
- LES-1001 detail page is open in BO Lesson Detail view mode.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open BO Lesson Detail for the first lesson LES-1001. | Lesson Detail page for LES-1001 loads. | recurring_chain = RC-1001; lesson = LES-1001 |
| 2 | Observe the lesson-navigation buttons in the action area. | `Previous Lesson` is visible but disabled, and `Next Lesson` is visible and enabled. | previous_state = disabled; next_state = enabled |
| 3 | Attempt to click `Previous Lesson`. | No navigation occurs and the current lesson remains LES-1001. | blocked_action = Previous Lesson |

**Severity:** major
**Priority:** high

---

### [Aver] Lesson Detail Navigation - Boundary State - Last recurring lesson - Next Lesson disabled

**Description:** AC 01.4 - Boundary Value Analysis - Last lesson in the recurring chain disables forward navigation while preserving backward navigation.

**Preconditions:**
- Logged in to Back Office as HQ or CM Staff with access to Aver lesson detail.
- Recurring lesson chain RC-1001 exists with LES-1002 before LES-1003, and LES-1003 is the last lesson.
- LES-1003 detail page is open in BO Lesson Detail view mode.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open BO Lesson Detail for the last lesson LES-1003. | Lesson Detail page for LES-1003 loads. | recurring_chain = RC-1001; lesson = LES-1003 |
| 2 | Observe the lesson-navigation buttons in the action area. | `Next Lesson` is visible but disabled, and `Previous Lesson` is visible and enabled. | previous_state = enabled; next_state = disabled |
| 3 | Attempt to click `Next Lesson`. | No navigation occurs and the current lesson remains LES-1003. | blocked_action = Next Lesson |

**Severity:** major
**Priority:** high

---

### [Aver] Lesson Detail Navigation - Action Area Composition - Existing detail actions present - Lesson navigation pair coexists without replacement

**Description:** AC 01.1 - Component - Lesson navigation buttons appear alongside the existing BO Lesson Detail action set, matching the legacy report-navigation pattern.

**Preconditions:**
- Logged in to Back Office as HQ or CM Staff with access to Aver lesson detail.
- Recurring lesson LES-1002 is open in BO Lesson Detail view mode.
- Existing lesson-detail actions for LES-1002 are available in the action area.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open BO Lesson Detail for LES-1002. | Lesson Detail page opens with its normal action area. | lesson = LES-1002 |
| 2 | Inspect the action area where lesson-detail actions are shown. | Existing lesson-detail actions remain visible. | existing_actions = lesson_detail_default_actions |
| 3 | Observe the lesson-navigation pair in the same action area. | `Previous Lesson` and `Next Lesson` are added without hiding or replacing existing actions. | navigation_pair = visible_with_existing_actions |

**Severity:** major
**Priority:** high

---

### [Aver] Lesson Detail Navigation - View Surface Scope - Lesson detail view mode - Navigation pair shown on intended surface only

**Description:** AC 01.1 - Regression - The lesson-navigation pair is rendered on the intended BO Lesson Detail view surface, following the legacy `view mode only` expectation from LT-84885.

**Preconditions:**
- Logged in to Back Office as HQ or CM Staff with access to Aver lesson detail.
- Recurring lesson LES-1002 exists and its BO Lesson Detail page supports view-mode content and nested report access.
- LES-1002 detail page is open in BO Lesson Detail view mode.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open BO Lesson Detail for LES-1002 and remain on the main Lesson Detail view surface. | The main Lesson Detail view is displayed. | lesson = LES-1002; surface = lesson_detail_view |
| 2 | Observe the action area on the main view surface. | `Previous Lesson` and `Next Lesson` are visible on the intended Lesson Detail view surface. | expected_surface = lesson_detail_view |
| 3 | Move to a nested lesson-related surface such as the report view for the same lesson. | No duplicate lesson-navigation pair appears outside the intended lesson-detail view surface unless explicitly designed there. | nested_surface = lesson_report_view |

**Severity:** major
**Priority:** high
