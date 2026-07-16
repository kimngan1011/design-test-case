# Test Cases: LT-94694 - Booking Link to Event List page

## Suite: Reserve Auth Trigger and Continuation

### [Koyu Booking Link] - Auth Trigger - Reserve Tapped While Logged Out - Login/Register Displayed

**Description:** AC 01.3 - Permission Matrix - Auth gate is triggered at Reserve action boundary only, consistent with LT-94696 direct navigation intent.

**Preconditions:**
- User is logged out.
- Booking link EM-1001 is valid and Event A is reservable.
- Related implementation: LT-94696 Handle Direct Navigation without login redirect.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open booking link and enter Event A detail page. | Event detail opens in pre-login mode. | event = Event A |
| 2 | Interact with non-reserve detail content (scroll/read). | No login/register redirect appears during non-reserve interactions. | interaction_scope = non_reserve_only |
| 3 | Tap Reserve button. | Login/Register gate appears and keeps Event A context for continuation. | auth_trigger = reserve_button_tap; expected_context = Event A |

**Severity:** critical
**Priority:** high

---

### [Koyu Booking Link] - Login Continuation - Logged Out Reserve Flow - Booking Continues After Login

**Description:** AC 01.4 - State Transition Testing - After Login from Reserve, flow returns to same event and reaches booking verified screen.

**Preconditions:**
- Start from Event A detail in logged-out booking-link flow.
- Valid account User S1 exists and can sign in.
- Related implementation: LT-94695 review current event page flow.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Tap Reserve on Event A detail. | Login or Register choices are shown as auth gate. | event = Event A; trigger = reserve_button |
| 2 | Choose Login and sign in with User S1. | Authentication succeeds and flow returns to Event A booking context. | auth_path = login; user = S1 |
| 3 | Proceed with booking after return. | Booking verified screen is reached for Event A. | expected_post_auth = booking_verified; expected_context = Event A |

**Severity:** critical
**Priority:** high

---

### [Koyu Booking Link] - Register Continuation - New User Reserve Flow - Booking Continues After Registration

**Description:** AC 01.4 - Scenario Testing - Register path preserves selected event context and continues booking flow (including register-info UI).

**Preconditions:**
- Start from Event B detail in logged-out booking-link flow.
- New profile P1 is eligible for registration.
- Related implementation: LT-99387 improve login flow UI.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Tap Reserve on Event B detail. | Auth screen with Register path is shown. | event = Event B; trigger = reserve_button |
| 2 | Choose Register and complete required register information for P1. | Registration succeeds and user becomes authenticated. | auth_path = register; profile = P1_new |
| 3 | Continue booking immediately after register completion. | Flow resumes with Event B context and proceeds to booking verified or next booking step. | expected_context = Event B; expected_post_auth = booking_verified_or_next |

**Severity:** major
**Priority:** high
