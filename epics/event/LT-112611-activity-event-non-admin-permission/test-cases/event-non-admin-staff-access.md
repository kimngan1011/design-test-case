# Test Cases: LT-112611 — Event screens for non-admin staff after new event fields

## Suite: Activity Event – Non-admin Staff Access

### Activity Event – Edit Dialog – Center Staff PSG User – Existing values prefilled

**Description:** Incident MANACS-2648 — Permission matrix — A non-admin Center Staff user sees the saved Activity Event values when opening the Edit dialog.

**Preconditions:**
- Reservation Deadline setting is turned off in the org.
- Staff user QA Center Staff PSG is assigned only the ManabieERP_Center_Staff_PSG permission set group.
- QA Center Staff PSG is a Centre Staff at location 目黒教室.
- Event Master EM-112611-01 (Event Type Free, Send To Parent & Student) exists.
- Activity Event AE-112611-01 under EM-112611-01 exists with location 目黒教室, date 2026-10-20, 10:00–11:00, capacity 30, Event Medium Offline.
- QA Center Staff PSG is logged in to Salesforce.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | QA Center Staff PSG opens Activity Event AE-112611-01 | The Activity Event detail page shows AE-112611-01 | activity_event = AE-112611-01 |
| 2 | QA Center Staff PSG clicks **Edit** | The Edit dialog opens without an error message | |
| 3 | QA Center Staff PSG reviews the fields in the Edit dialog | Event Name, Event Master, Location, Date, Start Time, End Time, Event Capacity, and Event Medium show the saved values | event_name = AE-112611-01; event_master = EM-112611-01; location = 目黒教室; date = 2026-10-20; time = 10:00–11:00; capacity = 30; medium = Offline |
| 4 | QA Center Staff PSG changes Event Capacity to 35 and clicks **Save** | A success message is shown and the detail page shows Event Capacity 35 | capacity = 35 |

**Severity:** critical
**Priority:** high

---

### Activity Event – Duplicate Dialog – Center Staff PSG User – Existing values prefilled

**Description:** Incident MANACS-2648 — Permission matrix — A non-admin Center Staff user can duplicate an Activity Event with its saved values copied.

**Preconditions:**
- Reservation Deadline setting is turned off in the org.
- Staff user QA Center Staff PSG is assigned only the ManabieERP_Center_Staff_PSG permission set group.
- QA Center Staff PSG is a Centre Staff at location 目黒教室.
- Event Master EM-112611-01 (Event Type Free, Send To Parent & Student) exists.
- Activity Event AE-112611-01 under EM-112611-01 exists with location 目黒教室, date 2026-10-20, 10:00–11:00, capacity 30, Event Medium Offline.
- QA Center Staff PSG is logged in to Salesforce.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | QA Center Staff PSG opens Activity Event AE-112611-01 | The Activity Event detail page shows AE-112611-01 | activity_event = AE-112611-01 |
| 2 | QA Center Staff PSG clicks **Duplicate** | The Duplicate dialog opens without an error message | |
| 3 | QA Center Staff PSG reviews the fields in the Duplicate dialog | Event Master, Location, Date, Start Time, End Time, Event Capacity, and Event Medium show the values copied from AE-112611-01 | event_master = EM-112611-01; location = 目黒教室; date = 2026-10-20; time = 10:00–11:00; capacity = 30; medium = Offline |
| 4 | QA Center Staff PSG enters Event Name AE-112611-01-COPY and clicks **Save** | A success message is shown and a new Activity Event AE-112611-01-COPY appears under EM-112611-01 | event_name = AE-112611-01-COPY |

**Severity:** critical
**Priority:** high

---

### Activity Event – Edit Dialog – Center Staff PSG User – Reservation Deadline enabled – Reservation Deadline prefilled

**Description:** LT-101742 — Permission matrix — With the Reservation Deadline setting on, a non-admin Center Staff user sees the saved Reservation Deadline in the Edit dialog.

**Preconditions:**
- Reservation Deadline setting is turned on in the org.
- Staff user QA Center Staff PSG is assigned only the ManabieERP_Center_Staff_PSG permission set group.
- QA Center Staff PSG is a Centre Staff at location 目黒教室.
- Event Master EM-112611-02 (Event Type Free, Send To Parent & Student) exists with Reservation Deadline (hours) 24.
- Activity Event AE-112611-02 under EM-112611-02 exists with location 目黒教室, date 2026-10-20, 10:00–11:00, and Reservation Deadline 2026-10-19 10:00.
- QA Center Staff PSG is logged in to Salesforce.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | QA Center Staff PSG opens Activity Event AE-112611-02 | The Activity Event detail page shows AE-112611-02 | today = 2026-10-06; activity_event = AE-112611-02; reservation_deadline_hours = 24 |
| 2 | QA Center Staff PSG clicks **Edit** | The Edit dialog opens without an error message | |
| 3 | QA Center Staff PSG reviews the Reservation Deadline field | Reservation Deadline shows 2026-10-19 10:00 and the other fields show the saved values | reservation_deadline = 2026-10-19 10:00; date = 2026-10-20; time = 10:00–11:00 |

**Severity:** critical
**Priority:** high

---

### Activity Event – New from Activity Events List – Center Staff PSG User – Event Master lookup returns results

**Description:** LT-101742 — Permission matrix — A non-admin Center Staff user can find an Event Master in the Event Master lookup when creating an Activity Event from the list.

**Preconditions:**
- Reservation Deadline setting is turned off in the org.
- Staff user QA Center Staff PSG is assigned only the ManabieERP_Center_Staff_PSG permission set group.
- QA Center Staff PSG is a Centre Staff at location 目黒教室.
- Event Master EM-112611-01 (Event Type Free, Send To Parent & Student) exists.
- QA Center Staff PSG is logged in to Salesforce.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | QA Center Staff PSG opens the Activity Events list and clicks **New** | The Create Activity Event dialog opens without an error message | |
| 2 | QA Center Staff PSG types EM-112611 in the Event Master field | EM-112611-01 appears in the search results | search = EM-112611 |
| 3 | QA Center Staff PSG selects EM-112611-01, fills the required fields, and clicks **Save** | A success message is shown and the new Activity Event appears under EM-112611-01 | event_name = AE-112611-03; location = 目黒教室; date = 2026-10-21; time = 10:00–11:00; medium = Offline; send_to = Parent & Student |

**Severity:** major
**Priority:** high

---

### Activity Event – Create from Event Master Detail – Center Staff PSG User – Activity Event saved

**Description:** LT-101742 — Permission matrix — A non-admin Center Staff user can create an Activity Event from the Event Master detail page.

**Preconditions:**
- Reservation Deadline setting is turned off in the org.
- Staff user QA Center Staff PSG is assigned only the ManabieERP_Center_Staff_PSG permission set group.
- QA Center Staff PSG is a Centre Staff at location 目黒教室.
- Event Master EM-112611-01 (Event Type Free, Send To Parent & Student) exists.
- QA Center Staff PSG is logged in to Salesforce.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | QA Center Staff PSG opens Event Master EM-112611-01 and clicks **Create Activity Event** | The Create Activity Event dialog opens with Event Master EM-112611-01 filled in | event_master = EM-112611-01 |
| 2 | QA Center Staff PSG fills the required fields and clicks **Save** | A success message is shown | event_name = AE-112611-04; location = 目黒教室; date = 2026-10-22; time = 10:00–11:00; medium = Offline; send_to = Parent & Student |
| 3 | QA Center Staff PSG opens the Activity Events list of EM-112611-01 | AE-112611-04 is listed with location 目黒教室 and date 2026-10-22 10:00–11:00 | |

**Severity:** major
**Priority:** high

---

### Event Master – Open Booking System – Center Staff PSG User – Booking dialog opens

**Description:** LT-101742 — Permission matrix — A non-admin Center Staff user can open the booking system dialog from an Event Master.

**Preconditions:**
- Reservation Deadline setting is turned off in the org.
- Staff user QA Center Staff PSG is assigned only the ManabieERP_Center_Staff_PSG permission set group.
- QA Center Staff PSG is a Centre Staff at location 目黒教室.
- Event Master EM-112611-01 (Event Type Free, Send To Parent & Student) exists.
- Activity Event AE-112611-01 under EM-112611-01 exists with location 目黒教室, date 2026-10-20, 10:00–11:00.
- QA Center Staff PSG is logged in to Salesforce.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | QA Center Staff PSG opens Event Master EM-112611-01 | The Event Master detail page shows EM-112611-01 | event_master = EM-112611-01 |
| 2 | QA Center Staff PSG clicks **Open Booking System** | The booking dialog opens without an error message and lists Activity Event AE-112611-01 | activity_event = AE-112611-01 |

**Severity:** major
**Priority:** high

---
