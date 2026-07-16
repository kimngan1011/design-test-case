# Test Cases: LT-99482 - Add Lesson Calendar button to Trial Lesson page

## Suite: LT-99482 - Scope and Regression

### Trial Lesson Calendar Entry - Surface Scope - Back Office Trial Lesson - Calendar Entry Not Added

**Description:** AC 01.5 - Permission Matrix - Lesson Calendar entry point from Trial Lesson remains SF-only and is not introduced on BO Trial Lesson surface.

**Preconditions:**
- Actor has access to Salesforce and Back Office as HQ or CM Staff.
- Trial Lesson TL-3001 exists and is visible in both systems where applicable.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Trial Lesson TL-3001 detail in Salesforce. | Lesson Calendar button is visible in SF Trial Lesson detail. | sf_trial_lesson = TL-3001 |
| 2 | Open corresponding Trial Lesson detail in Back Office. | Trial Lesson detail opens in BO surface. | bo_trial_lesson = TL-3001 |
| 3 | Inspect BO action area for Trial Lesson calendar entry. | No new Trial Lesson Lesson Calendar entry point is shown in BO. | expected_bo_entry = absent |

**Severity:** major
**Priority:** high

---

### Trial Lesson Calendar Entry - Existing Calendar Access - Direct Calendar Open - Existing Entry Path Unchanged

**Description:** AC 01.5 - Regression - Existing direct access to Lesson Calendar still works after Trial Lesson button addition.

**Preconditions:**
- Actor is logged in to Salesforce as HQ or CM Staff.
- User has menu access to Lesson Calendar.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Lesson Calendar from existing navigation menu (not from Trial Lesson). | Lesson Calendar opens through existing route. | entry_path = main_navigation |
| 2 | Open student filter panel. | Panel behavior is normal and page is usable. | panel_state = default |
| 3 | Return to Trial Lesson and use Lesson Calendar button once. | Trial Lesson entry path also works without affecting existing path behavior. | compare_mode = old_vs_new_entry |

**Severity:** major
**Priority:** high

---

### Trial Lesson Calendar Entry - Missing Student Edge - Trial Lesson Student Unavailable - Deterministic Handling Displayed

**Description:** AC 01.3 edge - Negative - When Trial Lesson student becomes unavailable, navigation behavior is deterministic and does not create wrong student context.

**Preconditions:**
- Actor is logged in to Salesforce as HQ or CM Staff.
- Trial Lesson TL-3002 exists but linked student STU-099 is inactive or inaccessible.
- TL-3002 detail page is open.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Click Lesson Calendar button on Trial Lesson TL-3002 detail. | Lesson Calendar navigation completes without crash. | trial_lesson = TL-3002 |
| 2 | Open student selection/filter panel in calendar. | STU-099 is not incorrectly selected as an active context student. | unavailable_student = STU-099 |
| 3 | Observe system feedback area after load. | System shows deterministic fallback behavior/message per implementation and does not assign a wrong student context implicitly. | expected_behavior = explicit_fallback |

**Severity:** minor
**Priority:** medium
