# Test Cases: LT-94694 - Booking Link to Event List page

## Suite: Booking Link Pre-login Navigation

### [Koyu Booking Link] - Entry Routing - External Link Opened - Activity Event List Shown First

**Description:** AC 01.1 - State Transition Testing - Follow Jira and Figma flow where booking link lands on Activity Event List before any auth.

**Preconditions:**
- Logged-in state: none (fresh app/browser session).
- Actor is Student or Parent user using Koyu booking link.
- Booking link points to Event Master EM-1001 with at least 1 published Activity Event.
- Reference design: Figma node 7593-44460 (https://www.figma.com/design/qmHa3rUESxPnfenYsKXbtv/-Eng--Event-Management?node-id=7593-44460&t=HtBSqAJUwV05Az5f-4).

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open booking link URL in a new incognito/private session. | Screen lands on Activity Event List, not Login/Sign up. | booking_link = EM-1001; session = logged_out |
| 2 | Read first visible header/title and event card area. | Activity Event List is visible with at least one event card ready for selection. | expected_first_screen = Activity Event List; min_cards >= 1 |
| 3 | Observe UI state before touching Reserve. | No blocking Login/Register screen appears before Reserve action. | auth_gate_timing = reserve_only |

**Severity:** critical
**Priority:** high

---

### [Koyu Booking Link] - Event Browsing - List Item Opened - Event Detail Visible Without Login

**Description:** AC 01.2 - Display Completeness - User can browse Event List and open Event Detail pre-login as defined in proposed booking-link flow.

**Preconditions:**
- Continue from logged-out booking-link session.
- Event List contains Event A and Event B under EM-1001.
- Reference design: Figma node 7593-44460 (https://www.figma.com/design/qmHa3rUESxPnfenYsKXbtv/-Eng--Event-Management?node-id=7593-44460&t=HtBSqAJUwV05Az5f-4).

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Tap Event A card from Activity Event List. | Event A detail opens directly with no auth redirect. | selected_event = Event A |
| 2 | Validate detail content for booking decision. | Event title, date/time, location, and Reserve button are visible and readable. | required_fields = title,date_time,location,reserve_button |
| 3 | Return to list and open Event B. | Event B detail also opens without forced login. | selected_event = Event B |

**Severity:** major
**Priority:** high

---

### [Koyu Booking Link] - Pre-login Display - Event List Cards - Mandatory Fields Rendered

**Description:** AC 01.2 - Component Testing - Pre-login list cards keep required fields and support detail navigation for discovery flow.

**Preconditions:**
- Logged-out booking-link session is active.
- Activity Event List has at least 3 events with distinct schedule values.
- Reference design: Figma node 7593-44460 (https://www.figma.com/design/qmHa3rUESxPnfenYsKXbtv/-Eng--Event-Management?node-id=7593-44460&t=HtBSqAJUwV05Az5f-4).

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open booking link and wait until list render completes. | At least 3 event cards are rendered. | min_cards = 3 |
| 2 | Inspect each sampled card on list view. | Each card shows event name and date/time with no missing core text. | mandatory_card_fields = name,date_time; sample_size = 3 |
| 3 | Tap each sampled card to detail and navigate back. | Card-to-detail navigation works and still does not trigger login before Reserve tap. | navigation_mode = card_tap; auth_gate = reserve_only |

**Severity:** major
**Priority:** medium
