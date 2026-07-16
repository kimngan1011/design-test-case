# Test Cases: LT-104241 - Feedback Cancel Booked Event (App)

## Suite: LT-104241 Feedback Updates

### [Koyu Feedback] Cancel Reservation - Other Reason - Detail Mandatory Before Submit

**Description:** LT-103839 / AC 03.3, AC 05.2 - Decision Table + Negative - When reason is Other, detail is required and submit remains disabled until detail is entered.

**Preconditions:**
- Logged in as Student/Parent on Learner App with booked eligible event.
- Cancel Type allows cancellation and Cancel Reservation button is visible.
- Related ticket: LT-103839.

| # | Action | Expected Result | Test Data |
| --- | --- | --- | --- |
| 1 | Open event detail and tap Cancel Reservation. | Cancellation modal opens with reason selector. | entry = event_detail |
| 2 | Select reason = Other and keep detail empty. | Confirm/Submit button stays disabled and cannot submit. | reason = Other; detail = empty |
| 3 | Enter valid detail text then tap Confirm/Submit. | Submit becomes enabled and cancellation request/cancel now proceeds. | detail = Personal schedule change |

**Severity:** critical
**Priority:** high

---

### [Koyu Feedback] Cancel Reservation Button - Eligible Case - Visible and Enabled

**Description:** LT-104248 / AC 02.1 - Decision Table - Eligible participant sees enabled Cancel Reservation button.

**Preconditions:**
- Logged in as Student/Parent with booked event in future.
- Cancel Type is Cancel or Cancellation Request and deadline not expired.
- Related ticket: LT-104248.

| # | Action | Expected Result | Test Data |
| --- | --- | --- | --- |
| 1 | Open booked event detail from learner app. | Event detail screen loads. | event_state = future_and_eligible |
| 2 | Observe action area on event detail. | Cancel Reservation button is visible and enabled. | expected_button_state = visible_enabled |
| 3 | Tap Cancel Reservation once. | Cancellation modal is displayed. | action = tap_cancel_reservation |

**Severity:** major
**Priority:** high

---

### [Koyu Feedback] Cancellation Deadline Section - Deadline Empty or 0 - Section Hidden and Action Available

**Description:** LT-104249 + LT-104251 / AC 02.1 - Boundary - Deadline empty/0 hides deadline section while cancel action remains available when otherwise eligible.

**Preconditions:**
- Booked participant has eligible cancellation and event in future.
- Cancellation Deadline Hours is null or 0.
- Related tickets: LT-104249, LT-104251.

| # | Action | Expected Result | Test Data |
| --- | --- | --- | --- |
| 1 | Open booked event detail in learner app. | Event detail loads. | deadline_hours = 0_or_null |
| 2 | Check cancellation deadline information section. | Cancellation Deadline section is not displayed. | expected_deadline_section = hidden |
| 3 | Check Cancel Reservation button state. | Button remains visible and enabled when other eligibility conditions pass. | expected_button_state = visible_enabled |

**Severity:** major
**Priority:** high

---

### [Koyu Feedback] Cancellation Reason Detail - Length Constraint - 255 Accepted and 256 Rejected

**Description:** LT-104250 / AC 05.2 - BVA - Detail field accepts 255 chars and blocks submission at 256 with inline validation.

**Preconditions:**
- Cancellation modal is open and reason = Other.
- Related ticket: LT-104250.

| # | Action | Expected Result | Test Data |
| --- | --- | --- | --- |
| 1 | Input exactly 255 characters in detail field. | No validation error; submit can proceed. | detail_length = 255 |
| 2 | Replace input with 256 characters. | Inline error is shown and submit is disabled. | detail_length = 256 |
| 3 | Reduce back to 255 and re-check state. | Error clears and submit becomes enabled again. | detail_length = 255_recovered |

**Severity:** major
**Priority:** high

---

### [Koyu Feedback] Event Participant List - Response Value Displayed for Canceled and Cancel Requested

**Description:** LT-104252 / AC 08.1 - CRUD - Event Participant list shows updated Response statuses and requested context.

**Preconditions:**
- Staff account can access Salesforce Event Participant list.
- Dataset includes participants with Attend/Canceled/Cancel Requested.
- Related ticket: LT-104252.

| # | Action | Expected Result | Test Data |
| --- | --- | --- | --- |
| 1 | Open Activity Event participant list in Salesforce. | Participant list is displayed. | surface = SF_event_participant_list |
| 2 | Locate rows with cancellation outcomes. | Response column displays Canceled and Cancel Requested correctly. | expected_values = Canceled,Cancel Requested |
| 3 | Open one row detail and return to list. | Displayed response value remains consistent between detail and list. | consistency_check = list_vs_detail |

**Severity:** major
**Priority:** high

---

### [Koyu Feedback] Open to Booking - Before Booking Start Date - Availability Message Displayed

**Description:** LT-104253 / AC 01.5 - Boundary - When current date is before Booking Start Date, reserve action is unavailable and message is shown.

**Preconditions:**
- Master Event has Open to Booking enabled with Booking Start Date in the future.
- Related ticket: LT-104253.

| # | Action | Expected Result | Test Data |
| --- | --- | --- | --- |
| 1 | Open booking link or event detail before booking start date. | Event detail loads with booking context. | today = 2026-07-06; booking_start_date = 2026-07-10 |
| 2 | Observe reserve action availability. | Reserve action is disabled or not actionable before start date. | expected_reserve_state = unavailable |
| 3 | Read guidance message on screen. | Message indicates event is available for booking from booking start date. | expected_message = available_from_booking_start_date |

**Severity:** critical
**Priority:** high

---

### [Koyu Feedback] Cancellation Deadline Update - Event Started - Warning Message and Scoped Recompute

**Description:** LT-104254 / AC 01.3 - State Transition - Updating cancellation deadline for started event shows warning and only applies to unstarted activities on confirm.

**Preconditions:**
- Staff can edit Event Master with mix of started and unstarted activities.
- Related ticket: LT-104254.

| # | Action | Expected Result | Test Data |
| --- | --- | --- | --- |
| 1 | Change Cancellation Deadline on Event Master where at least one activity already started. | Warning message is displayed before apply. | activity_mix = started_and_unstarted |
| 2 | Choose Confirm on warning dialog. | New deadline applies only to unstarted activities. | dialog_action = confirm |
| 3 | Re-open started activity details. | Started activity keeps prior effective deadline; no retroactive change. | expected_scope = unstarted_only |

**Severity:** major
**Priority:** high

---

### [Koyu Feedback] Re-booking After Cancellation - Capacity Available - Rebook Allowed with New Record

**Description:** LT-104255 / AC 10.1 - State Transition + Data Integrity - User can rebook after cancel when capacity is available and historical cancel record is retained.

**Preconditions:**
- User previously canceled event and was removed from participant list.
- Event currently has available capacity.
- Related ticket: LT-104255.

| # | Action | Expected Result | Test Data |
| --- | --- | --- | --- |
| 1 | Open same event after prior cancellation. | Event can be opened for re-book evaluation. | capacity_remaining >= 1 |
| 2 | Tap Reserve/Book again and complete booking. | Booking succeeds and user is added back as active participant. | action = rebook |
| 3 | Check participant records in staff view. | Old canceled record remains for audit; new active record exists with blank cancellation fields. | expected_records = historical_canceled + new_active |

**Severity:** critical
**Priority:** high

---

### [Koyu Feedback] SF Cancellation Notification - Language Independent Content

**Description:** LT-104256 / AC 07.1 - Cross-system - Notification payload remains correct regardless of Salesforce user language.

**Preconditions:**
- Response Notification setting enables cancel notification.
- Two staff users exist with different SF language settings.
- Related ticket: LT-104256.

| # | Action | Expected Result | Test Data |
| --- | --- | --- | --- |
| 1 | Trigger cancellation from mobile app (cancel now or cancel request). | Cancellation action is processed. | trigger_source = mobile |
| 2 | Open SF bell notifications with language A user. | Notification appears with correct event/student/cancel-type info. | sf_language = JA_or_EN_A |
| 3 | Open SF bell notifications with language B user. | Notification still appears with correct semantic content and no missing placeholders. | sf_language = EN_or_JA_B |

**Severity:** major
**Priority:** medium

---

### [Koyu Feedback] Cancel Action Labels - UI Translation Matches Latest PRD

**Description:** LT-104257 / Localization - UI labels for cancel actions match latest PRD text for active locale.

**Preconditions:**
- Learner app build includes LT-104257 changes.
- PRD localization baseline is available from epic documents.
- Related ticket: LT-104257.

| # | Action | Expected Result | Test Data |
| --- | --- | --- | --- |
| 1 | Open cancellation modal in locale A. | Primary/secondary cancel-related button labels match PRD for locale A. | locale = A |
| 2 | Switch to locale B and reopen same modal. | Button labels match PRD for locale B with no fallback text. | locale = B |
| 3 | Compare both against PRD localization entries. | No label mismatch is found for cancel-related controls. | comparison = app_vs_prd |

**Severity:** minor
**Priority:** medium
