# Test Cases: LT-94694 - Booking Link to Event List page

## Suite: Existing Flow Regression

### [Koyu Booking Link] - In-app Booking Path - Logged-in User - Existing Flow Preserved

**Description:** AC 01.5 - Regression Analysis - Existing app flow remains Login > Calendar > Booking system > Master Event > Activity Event List > Detail > Reserve.

**Preconditions:**
- User S2 is already logged in.
- Event A under EM-1001 is available for booking in app flow.
- No booking-link URL is used in this case.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | From app home, open Calendar then Booking system. | Existing in-app route opens without unexpected auth gate. | entry_path = login>calendar>booking_system |
| 2 | Open Master Event EM-1001 then Event A detail. | Event A detail is displayed in logged-in flow. | master_event = EM-1001; event = Event A |
| 3 | Tap Reserve on Event A detail. | Booking continues directly with no Login/Register detour. | user_state = logged_in; expected_auth_redirect = none |

**Severity:** critical
**Priority:** high

---

### [Koyu Booking Link] - Direct Event Navigation - Existing User Journey - No Unexpected Login-first Regression

**Description:** AC 01.5 - Regression Analysis - Direct navigation to Event Detail stays stable for logged-in users and does not regress to login-first behavior.

**Preconditions:**
- User S2 is logged in.
- Direct Event A detail path/URL is available.
- Related implementation: LT-94696 direct navigation handling.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open direct Event A detail path while still logged in. | Event A detail opens successfully. | direct_path = event_detail_a; user_state = logged_in |
| 2 | Tap Reserve button on detail page. | Booking proceeds and does not bounce to Login/Register. | expected_auth_redirect = none |
| 3 | Compare outcome with pre-LT-94694 baseline path. | Behavior is equivalent to baseline for logged-in direct navigation. | baseline = pre_LT-94694 |

**Severity:** major
**Priority:** medium
