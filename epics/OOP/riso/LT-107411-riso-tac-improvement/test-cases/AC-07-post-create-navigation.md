# Test Cases: LT-107411 — Riso | Core | TAC improvement (July)

## Suite: AC-07 — Post-Create Navigation

### AC 07.1 – Post-Create Navigation – Successful lesson creation redirects to Lesson Schedule detail

**Description:** AC 07 — CRUD + Regression (High Risk) — Successful lesson creation triggers redirect to the Lesson Schedule detail page (not back to Lesson Calendar).

**Preconditions:**
- User role: HQ/CM Staff
- Location: Create Lesson form (from Riso TAC or Lesson Schedule)
- Form fields populated: Course="Course A", Subject="Mathematics", Teacher="Tanaka Yuki", Date="2026-07-01", Time="09:00-10:00", Location="Room A"
- Student: "Yamada Taro"
- Form ready for submission

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Verify form is complete with all required fields | Form populated with valid data | form_state = "complete" |
| 2 | Submit Create Lesson form by clicking Save/Create button | Form submitted to backend | submit_action = "click_save" |
| 3 | Verify API response indicates success (HTTP 200 or similar) | Server returns success code | api_response = "201_created" |
| 4 | Verify page navigates to Lesson Schedule detail page | URL changes from /create-lesson to /lesson-schedule/{lesson_id} | expected_url = "/lesson-schedule/[lesson_id]" |
| 5 | Verify Lesson Schedule detail page displays created lesson data | Page shows: Course, Subject, Teacher, Date, Time, Location, Student | lesson_detail_visible = true |
| 6 | Verify lesson_id in URL matches created lesson | URL parameter matches database record | lesson_id_match = true |

**Severity:** major
**Priority:** high

---

### AC 07.2 – Post-Create Navigation – Cancel button does not redirect (preserves calendar/form state)

**Description:** AC 07 — CRUD + Negative (State Transition) — Cancel action on Create Lesson form does not trigger post-create redirect; user remains on form or returns to previous page without navigation surprise.

**Preconditions:**
- User role: HQ/CM Staff
- Location: Create Lesson form (opened from Riso TAC or Lesson Schedule)
- Form partially populated with data
- Cancel button visible on form

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to Create Lesson form from Riso TAC | Form opens; previous page is Riso TAC | previous_page = "riso_tac" |
| 2 | Populate some form fields (partial fill) | Form has data entered | form_state = "partial" |
| 3 | Click Cancel button | Cancel action triggered | cancel_action = "click_cancel" |
| 4 | Verify no lesson record created in database | Query lesson table; no new record added | lesson_created = false |
| 5 | Verify page navigation returns to Riso TAC (or previous page) | URL changes back to Riso TAC or form closes without redirect to detail | navigation = "back_to_previous_page" |
| 6 | Verify no unexpected redirect to Lesson Schedule detail | User does NOT see Lesson Schedule detail page | redirect_to_detail = false |

**Severity:** minor
**Priority:** medium

---

### AC 07.3 – Post-Create Navigation – Form validation error does not trigger redirect

**Description:** AC 07 — CRUD + Negative (State Transition & Boundary) — When form submission fails due to validation error (e.g., missing required Course), page does NOT redirect; error message displayed and form remains.

**Preconditions:**
- User role: HQ/CM Staff
- Location: Create Lesson form
- Course field: null/empty (required field missing)
- Other fields: populated with valid data
- Submit button visible

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to Create Lesson form | Form opens with empty Course field | form_state = "missing_course" |
| 2 | Populate all other required fields (Subject, Teacher, Date, Time, Location) | Form filled except Course | course_value = null |
| 3 | Attempt to submit form by clicking Save button | Form submission attempted | submit_action = "click_save" |
| 4 | Verify validation error returned (form not submitted to backend) | Validation error message displayed (e.g., "Course is required") | error_message_visible = true |
| 5 | Verify page does NOT navigate away | User remains on Create Lesson form page; URL unchanged | page_change = false |
| 6 | Verify form fields retain entered data | Previously filled fields still contain data (no loss) | data_retention = true |

**Severity:** minor
**Priority:** medium

---

## Test Data Dictionary

- `form_state`: State of Create Lesson form (complete, partial, missing_course, submitted)
- `submit_action`: Action to submit form (click_save, click_create, keyboard_enter)
- `api_response`: HTTP response from backend (201_created, 200_ok, 400_bad_request, 500_error)
- `expected_url`: Expected URL after successful creation (/lesson-schedule/[lesson_id])
- `lesson_detail_visible`: Boolean; Lesson Schedule detail page loaded and displaying data
- `lesson_id_match`: Boolean; URL lesson_id matches database record ID
- `previous_page`: Page user came from before opening Create Lesson form (riso_tac, lesson_schedule, etc.)
- `cancel_action`: Action to cancel form (click_cancel, click_close, esc_key)
- `lesson_created`: Boolean; lesson record exists in database after cancel
- `navigation`: Navigation result after cancel (back_to_previous_page, close_form, no_change)
- `redirect_to_detail`: Boolean; page navigated to Lesson Schedule detail
- `course_value`: Value in Course field (null, empty, valid course ID)
- `error_message_visible`: Boolean; validation error message displayed
- `page_change`: Boolean; page URL or location changed
- `data_retention`: Boolean; form fields retained entered data after error
