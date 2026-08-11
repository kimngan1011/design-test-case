# Test Cases: LT-92177 — Koyu2 Multiple Days Event

## Suite: [Koyu2] Multiple Days Activity Event

### [Koyu2] Activity Event – Multi-day form – Event Master has no schedule fields

**Description:** AC 01 — Domain correction — Event Master remains a template and does not expose Start Date or End Date scheduling inputs.

**Preconditions:**
- Logged in as HQ or CM Staff to Koyu2 Salesforce org.
- Feature setting MANAERP__Enable_Multiple_Event_Days__c is enabled unless the case says otherwise.
- An Event Master named 'Koyu Outdoor Experience' exists with Event Type = Free, Send To = Parent & Student, Who Can Reserve = Student Only, Open To Booking System = true, Booking Start Date = 2026-09-01, Booking End Date = 2026-12-31.
- Target Location = Tokyo Center; Target Grade = G7; Target Course = Outdoor Program.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Event Master 'Koyu Outdoor Experience'. | Event Master detail page opens. | Event Master = Koyu Outdoor Experience |
| 2 | Click Edit on the Event Master. | Edit Event Master form opens with template, booking, target, reminder, and notification fields. | Surface = Salesforce Event Master |
| 3 | Inspect the Event Master form fields. | No Start Date, End Date, Start Time, End Time, or Duration Days scheduling fields are shown. | Expected scheduling owner = Activity Event |
| 4 | Cancel the edit form. | No Event Master data is changed. |  |

**Severity:** critical
**Priority:** high

---

### [Koyu2] Activity Event – Multi-day create – Three-day event saved as one Activity Event

**Description:** AC 01 — Happy Path — A single Activity Event accepts start datetime on day 1 and end datetime on day 3.

**Preconditions:**
- Logged in as HQ or CM Staff to Koyu2 Salesforce org.
- Feature setting MANAERP__Enable_Multiple_Event_Days__c is enabled unless the case says otherwise.
- An Event Master named 'Koyu Outdoor Experience' exists with Event Type = Free, Send To = Parent & Student, Who Can Reserve = Student Only, Open To Booking System = true, Booking Start Date = 2026-09-01, Booking End Date = 2026-12-31.
- Target Location = Tokyo Center; Target Grade = G7; Target Course = Outdoor Program.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Event Master 'Koyu Outdoor Experience' and click New Activity Event. | New Activity Event form opens. | today = 2026-09-01; timezone = Asia/Tokyo |
| 2 | Verify inherited/default fields from Event Master. | Event Master lookup is preselected and disabled; Activity Event Name and Description are prefilled from Event Master; Send To = Parent & Student; Allow Response = Student only; Reminder Days is inherited when Event Master has Reminders; Event Status defaults to Published if the draft-status setting is enabled. | Event Master = Koyu Outdoor Experience; Who Can Reserve = Student Only |
| 3 | Fill required/general Activity Event fields: Activity Event Name 'Koyu Camp 3D2N', Location 'Tokyo Center', Event Medium 'Offline', Event Capacity 30; leave Classrooms empty unless automation needs a classroom fixture. | Required general fields are valid; selecting Location clears any previously selected Classroom; Event Capacity accepts value greater than 0. | capacity = 30; classroomIds = [] |
| 4 | Confirm conditional fields: Product Offering and Order Location are not shown because Event Type = Free; Allow Submit Proposal = unchecked; Allow Extra Participants = unchecked and Extra Participants remains blank; fill every visible required Additional Field with a valid value. | Free Activity Event has no paid-event required fields; extra-participant validation is not triggered; all dynamic additional fields pass validation. | eventType = Free; allowExtraParticipants = false |
| 5 | Enter Start Date 2026-12-12, Start Time 10:00, End Date 2026-12-14, End Time 17:00. | Duration Days shows '3 days'; Start Date Time is before End Date Time. | start = 2026-12-12 10:00 JST; end = 2026-12-14 17:00 JST |
| 6 | Click Save. | Activity Event is created successfully as one record and success toast is shown. | status = Published |
| 7 | Open the created Activity Event detail page. | Date Range shows 2026/12/12 - 2026/12/14; Start Time shows 10:00; End Time shows 17:00; Event Master, Location, Event Medium, Send To, Allow Response, Capacity, and Status match the values saved from the form. |  |

**Severity:** critical
**Priority:** high

---

### [Koyu2] Activity Event – Multi-day create – Two-day overnight event saved

**Description:** AC 01 — Boundary Value — Minimum true multi-day event across two dates is accepted.

**Preconditions:**
- Logged in as HQ or CM Staff to Koyu2 Salesforce org.
- Feature setting MANAERP__Enable_Multiple_Event_Days__c is enabled unless the case says otherwise.
- An Event Master named 'Koyu Outdoor Experience' exists with Event Type = Free, Send To = Parent & Student, Who Can Reserve = Student Only, Open To Booking System = true, Booking Start Date = 2026-09-01, Booking End Date = 2026-12-31.
- Target Location = Tokyo Center; Target Grade = G7; Target Course = Outdoor Program.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open New Activity Event from the Event Master. | New Activity Event form opens. | timezone = Asia/Tokyo |
| 2 | Enter required non-date fields. | Required fields are valid. | name = Koyu Overnight 2D1N; location = Tokyo Center |
| 3 | Enter Start Date 2026-11-20, Start Time 18:00, End Date 2026-11-21, End Time 09:00. | Duration Days shows '2 days'. | start < end |
| 4 | Save the Activity Event. | One Activity Event record is created with the entered start and end datetime. |  |

**Severity:** major
**Priority:** high

---

### [Koyu2] Activity Event – Multi-day create – Same-date event still saved

**Description:** AC 01 — Regression — Existing one-day Activity Event behavior remains valid when the feature is enabled.

**Preconditions:**
- Logged in as HQ or CM Staff to Koyu2 Salesforce org.
- Feature setting MANAERP__Enable_Multiple_Event_Days__c is enabled unless the case says otherwise.
- An Event Master named 'Koyu Outdoor Experience' exists with Event Type = Free, Send To = Parent & Student, Who Can Reserve = Student Only, Open To Booking System = true, Booking Start Date = 2026-09-01, Booking End Date = 2026-12-31.
- Target Location = Tokyo Center; Target Grade = G7; Target Course = Outdoor Program.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open New Activity Event. | Multi-day layout is displayed. | feature = enabled |
| 2 | Enter Start Date 2026-10-10, Start Time 10:00, End Date 2026-10-10, End Time 12:00. | Duration Days shows '1 day'. | same calendar date |
| 3 | Save the Activity Event. | Activity Event is created successfully. |  |
| 4 | Open Activity Event detail. | Detail shows Date, not Date Range, with Start Time 10:00 and End Time 12:00. |  |

**Severity:** major
**Priority:** high

---

### [Koyu2] Activity Event – Start Date later than End Date – Validation blocks save

**Description:** AC 02 — Negative Testing — End Date cannot be earlier than Start Date.

**Preconditions:**
- Logged in as HQ or CM Staff to Koyu2 Salesforce org.
- Feature setting MANAERP__Enable_Multiple_Event_Days__c is enabled unless the case says otherwise.
- An Event Master named 'Koyu Outdoor Experience' exists with Event Type = Free, Send To = Parent & Student, Who Can Reserve = Student Only, Open To Booking System = true, Booking Start Date = 2026-09-01, Booking End Date = 2026-12-31.
- Target Location = Tokyo Center; Target Grade = G7; Target Course = Outdoor Program.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open New Activity Event and enter required non-date fields. | Form is ready to save except date/time fields. |  |
| 2 | Enter Start Date 2026-12-14, Start Time 10:00, End Date 2026-12-12, End Time 17:00. | Date fields contain an invalid date range. | startDate > endDate |
| 3 | Click Save. | Save is blocked and both date fields show 'End Date cannot be earlier than Start Date'. |  |
| 4 | Search Activity Event list for the entered name. | No Activity Event record is created. |  |

**Severity:** critical
**Priority:** high

---

### [Koyu2] Activity Event – Same datetime – Validation blocks save

**Description:** AC 02 — Boundary Value — Start datetime must be strictly before End datetime.

**Preconditions:**
- Logged in as HQ or CM Staff to Koyu2 Salesforce org.
- Feature setting MANAERP__Enable_Multiple_Event_Days__c is enabled unless the case says otherwise.
- An Event Master named 'Koyu Outdoor Experience' exists with Event Type = Free, Send To = Parent & Student, Who Can Reserve = Student Only, Open To Booking System = true, Booking Start Date = 2026-09-01, Booking End Date = 2026-12-31.
- Target Location = Tokyo Center; Target Grade = G7; Target Course = Outdoor Program.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open New Activity Event and fill required non-date fields. | Form accepts the required values. |  |
| 2 | Enter Start Date 2026-12-12, Start Time 10:00, End Date 2026-12-12, End Time 10:00. | Start datetime equals End datetime. | boundary = equal datetime |
| 3 | Click Save. | Save is blocked and time fields show 'Start time must be before end time'. |  |

**Severity:** critical
**Priority:** high

---

### [Koyu2] Activity Event – Same date with end time before start time – Validation blocks save

**Description:** AC 02 — Negative Testing — One-day Activity Event still rejects an inverted time range.

**Preconditions:**
- Logged in as HQ or CM Staff to Koyu2 Salesforce org.
- Feature setting MANAERP__Enable_Multiple_Event_Days__c is enabled unless the case says otherwise.
- An Event Master named 'Koyu Outdoor Experience' exists with Event Type = Free, Send To = Parent & Student, Who Can Reserve = Student Only, Open To Booking System = true, Booking Start Date = 2026-09-01, Booking End Date = 2026-12-31.
- Target Location = Tokyo Center; Target Grade = G7; Target Course = Outdoor Program.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open New Activity Event. | Form opens. |  |
| 2 | Enter Start Date 2026-12-12, Start Time 17:00, End Date 2026-12-12, End Time 10:00. | Date range is same day but time range is invalid. | same day; startTime > endTime |
| 3 | Click Save. | Save is blocked and time fields show 'Start time must be before end time'. |  |

**Severity:** critical
**Priority:** high

---

### [Koyu2] Activity Event – End Date cleared – Required validation blocks save

**Description:** AC 02 — Required Field — End Date is mandatory in the multi-day layout.

**Preconditions:**
- Logged in as HQ or CM Staff to Koyu2 Salesforce org.
- Feature setting MANAERP__Enable_Multiple_Event_Days__c is enabled unless the case says otherwise.
- An Event Master named 'Koyu Outdoor Experience' exists with Event Type = Free, Send To = Parent & Student, Who Can Reserve = Student Only, Open To Booking System = true, Booking Start Date = 2026-09-01, Booking End Date = 2026-12-31.
- Target Location = Tokyo Center; Target Grade = G7; Target Course = Outdoor Program.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open New Activity Event. | Form opens with Start Date and End Date fields. |  |
| 2 | Enter Start Date 2026-12-12 and leave End Date empty. | End Date is blank. |  |
| 3 | Click Save. | Save is blocked and End Date shows required field validation. |  |

**Severity:** major
**Priority:** high

---

### [Koyu2] Activity Event – End Time cleared – Required validation blocks save

**Description:** AC 02 — Required Field — End Time is mandatory in the multi-day layout.

**Preconditions:**
- Logged in as HQ or CM Staff to Koyu2 Salesforce org.
- Feature setting MANAERP__Enable_Multiple_Event_Days__c is enabled unless the case says otherwise.
- An Event Master named 'Koyu Outdoor Experience' exists with Event Type = Free, Send To = Parent & Student, Who Can Reserve = Student Only, Open To Booking System = true, Booking Start Date = 2026-09-01, Booking End Date = 2026-12-31.
- Target Location = Tokyo Center; Target Grade = G7; Target Course = Outdoor Program.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open New Activity Event. | Form opens. |  |
| 2 | Enter Start Date 2026-12-12, Start Time 10:00, End Date 2026-12-14 and leave End Time empty. | End Time is blank. |  |
| 3 | Click Save. | Save is blocked and End Time shows required field validation. |  |

**Severity:** major
**Priority:** high

---

### [Koyu2] Activity Event – Start Date changed – End Date stays user-selected

**Description:** AC 02 — Regression — When End Date already has a value, changing Start Date must not silently overwrite it.

**Preconditions:**
- Logged in as HQ or CM Staff to Koyu2 Salesforce org.
- Feature setting MANAERP__Enable_Multiple_Event_Days__c is enabled unless the case says otherwise.
- An Event Master named 'Koyu Outdoor Experience' exists with Event Type = Free, Send To = Parent & Student, Who Can Reserve = Student Only, Open To Booking System = true, Booking Start Date = 2026-09-01, Booking End Date = 2026-12-31.
- Target Location = Tokyo Center; Target Grade = G7; Target Course = Outdoor Program.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open New Activity Event. | Form opens. |  |
| 2 | Enter Start Date 2026-12-12 and End Date 2026-12-14. | Duration Days shows '3 days'. | initial date range = 3 days |
| 3 | Change Start Date to 2026-12-13. | End Date remains 2026-12-14 and Duration Days updates to '2 days'. | endDate already populated |
| 4 | Save with valid times 10:00 to 17:00. | Activity Event is saved with Start Date 2026-12-13 and End Date 2026-12-14. |  |

**Severity:** major
**Priority:** high

---

### [Koyu2] Activity Event – Feature disabled – Legacy one-day form remains

**Description:** AC 03 — Feature Flag — When multiple event days is disabled, the legacy Event Date form is used.

**Preconditions:**
- Logged in as HQ or CM Staff to a Salesforce org where MANAERP__Enable_Multiple_Event_Days__c is disabled.
- Event Master 'Koyu Outdoor Experience' exists.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open New Activity Event. | Legacy Activity Event form opens. | feature = disabled |
| 2 | Inspect the date/time section. | Only Event Date, Start Time, and End Time are shown; Start Date, End Date, and Duration Days are not shown. |  |
| 3 | Enter Event Date 2026-12-12, Start Time 10:00, End Time 12:00 and save. | One-day Activity Event is created successfully. |  |

**Severity:** major
**Priority:** high

---

### [Koyu2] Activity Event – Edit existing multi-day event – Date range prefilled

**Description:** AC 04 — Edit Flow — Existing Activity Event datetime values populate the edit form correctly.

**Preconditions:**
- Logged in as HQ or CM Staff to Koyu2 Salesforce org.
- Feature setting MANAERP__Enable_Multiple_Event_Days__c is enabled unless the case says otherwise.
- An Event Master named 'Koyu Outdoor Experience' exists with Event Type = Free, Send To = Parent & Student, Who Can Reserve = Student Only, Open To Booking System = true, Booking Start Date = 2026-09-01, Booking End Date = 2026-12-31.
- Target Location = Tokyo Center; Target Grade = G7; Target Course = Outdoor Program.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Activity Event 'Koyu Camp 3D2N'. | Activity Event detail page opens. | start = 2026-12-12 10:00; end = 2026-12-14 17:00 |
| 2 | Click Edit. | Edit Activity Event form opens. |  |
| 3 | Inspect date/time fields. | Start Date = 2026-12-12, Start Time = 10:00, End Date = 2026-12-14, End Time = 17:00, Duration Days = '3 days'. |  |

**Severity:** major
**Priority:** high

---

### [Koyu2] Activity Event – Edit multi-day to longer range – Detail updates

**Description:** AC 04 — State Transition — Increasing End Date updates the saved Activity Event and its detail page.

**Preconditions:**
- Logged in as HQ or CM Staff to Koyu2 Salesforce org.
- Feature setting MANAERP__Enable_Multiple_Event_Days__c is enabled unless the case says otherwise.
- An Event Master named 'Koyu Outdoor Experience' exists with Event Type = Free, Send To = Parent & Student, Who Can Reserve = Student Only, Open To Booking System = true, Booking Start Date = 2026-09-01, Booking End Date = 2026-12-31.
- Target Location = Tokyo Center; Target Grade = G7; Target Course = Outdoor Program.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Edit Activity Event for 'Koyu Camp 3D2N'. | Edit form opens with existing values. | current end = 2026-12-14 17:00 |
| 2 | Change End Date to 2026-12-15 and keep End Time 17:00. | Duration Days updates to '4 days'. | new end = 2026-12-15 17:00 |
| 3 | Click Save. | Activity Event is updated successfully. |  |
| 4 | Open Activity Event detail. | Date Range shows 2026/12/12 - 2026/12/15. |  |

**Severity:** major
**Priority:** high

---

### [Koyu2] Activity Event – Duplicate multi-day event – Date range copied

**Description:** AC 04 — Regression — Duplicate Activity Event copies start and end datetime values before user changes them.

**Preconditions:**
- Logged in as HQ or CM Staff to Koyu2 Salesforce org.
- Feature setting MANAERP__Enable_Multiple_Event_Days__c is enabled unless the case says otherwise.
- An Event Master named 'Koyu Outdoor Experience' exists with Event Type = Free, Send To = Parent & Student, Who Can Reserve = Student Only, Open To Booking System = true, Booking Start Date = 2026-09-01, Booking End Date = 2026-12-31.
- Target Location = Tokyo Center; Target Grade = G7; Target Course = Outdoor Program.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Activity Event 'Koyu Camp 3D2N' and choose Duplicate. | Duplicate Activity Event form opens. |  |
| 2 | Inspect the prefilled date/time fields. | Start Date, Start Time, End Date, and End Time match the source Activity Event. | source = 2026-12-12 10:00 to 2026-12-14 17:00 |
| 3 | Change Activity Event Name to 'Koyu Camp 3D2N Copy' and save. | A separate Activity Event is created with the same date range. |  |

**Severity:** major
**Priority:** high

---

### [Koyu2] Activity Event – Related Activity Events – Sort by Start Date then End Date

**Description:** AC 04 — Ordering — Related Activity Events under Event Master are ordered by Start datetime, End datetime, then Created Date.

**Preconditions:**
- Logged in as HQ or CM Staff to Koyu2 Salesforce org.
- Feature setting MANAERP__Enable_Multiple_Event_Days__c is enabled unless the case says otherwise.
- An Event Master named 'Koyu Outdoor Experience' exists with Event Type = Free, Send To = Parent & Student, Who Can Reserve = Student Only, Open To Booking System = true, Booking Start Date = 2026-09-01, Booking End Date = 2026-12-31.
- Target Location = Tokyo Center; Target Grade = G7; Target Course = Outdoor Program.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Create three Activity Events under the same Event Master with different ranges. | All three Activity Events exist. | A: 2026-12-12 to 2026-12-14; B: 2026-12-01 to 2026-12-02; C: 2026-12-12 to 2026-12-13 |
| 2 | Open Event Master related Activity Events list. | Related list loads. |  |
| 3 | Inspect the order. | Events are ordered B, C, A based on Start Date/Time then End Date/Time. |  |

**Severity:** major
**Priority:** high

---

### [Koyu2] SF Calendar – Weekly view – Multi-day activity spans each day column

**Description:** AC 05 — Calendar Rendering — Weekly calendar renders a multi-day Activity Event across all days in its range.

**Preconditions:**
- Logged in as HQ or CM Staff to Koyu2 Salesforce org.
- Feature setting MANAERP__Enable_Multiple_Event_Days__c is enabled unless the case says otherwise.
- An Event Master named 'Koyu Outdoor Experience' exists with Event Type = Free, Send To = Parent & Student, Who Can Reserve = Student Only, Open To Booking System = true, Booking Start Date = 2026-09-01, Booking End Date = 2026-12-31.
- Target Location = Tokyo Center; Target Grade = G7; Target Course = Outdoor Program.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Salesforce Calendar weekly view for 2026-12-08 to 2026-12-14. | Weekly calendar loads. | range = 2026-12-08..2026-12-14 |
| 2 | Ensure Events filter is selected and Lessons filter remains selected. | Both Lessons and Events are visible. |  |
| 3 | Find Activity Event 'Koyu Camp 3D2N'. | One multi-day event bar spans 2026-12-12, 2026-12-13, and 2026-12-14. | start = 2026-12-12; end = 2026-12-14 |
| 4 | Click the multi-day event bar. | Activity Event detail drawer opens for the same Activity Event ID. |  |

**Severity:** critical
**Priority:** high

---

### [Koyu2] SF Calendar – Daily view – Multi-day banner appears on middle day

**Description:** AC 05 — Calendar Rendering — Daily calendar displays a spanning multi-day Activity Event on a date between start and end.

**Preconditions:**
- Logged in as HQ or CM Staff to Koyu2 Salesforce org.
- Feature setting MANAERP__Enable_Multiple_Event_Days__c is enabled unless the case says otherwise.
- An Event Master named 'Koyu Outdoor Experience' exists with Event Type = Free, Send To = Parent & Student, Who Can Reserve = Student Only, Open To Booking System = true, Booking Start Date = 2026-09-01, Booking End Date = 2026-12-31.
- Target Location = Tokyo Center; Target Grade = G7; Target Course = Outdoor Program.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Salesforce Calendar daily view for 2026-12-13. | Daily view loads. | middle date = 2026-12-13 |
| 2 | Ensure Events filter is selected. | Event data is visible. |  |
| 3 | Inspect the multi-day event banner area. | 'Koyu Camp 3D2N' appears even though it does not start on 2026-12-13. | event spans 2026-12-12 to 2026-12-14 |
| 4 | Click the banner. | Detail drawer opens and shows Date Range 2026/12/12 - 2026/12/14. |  |

**Severity:** critical
**Priority:** high

---

### [Koyu2] SF Calendar – Range time filter – Multi-day event remains visible

**Description:** AC 05 — Regression — Range Time filter does not hide multi-day Activity Events.

**Preconditions:**
- Logged in as HQ or CM Staff to Koyu2 Salesforce org.
- Feature setting MANAERP__Enable_Multiple_Event_Days__c is enabled unless the case says otherwise.
- An Event Master named 'Koyu Outdoor Experience' exists with Event Type = Free, Send To = Parent & Student, Who Can Reserve = Student Only, Open To Booking System = true, Booking Start Date = 2026-09-01, Booking End Date = 2026-12-31.
- Target Location = Tokyo Center; Target Grade = G7; Target Course = Outdoor Program.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open SF Calendar weekly view containing 'Koyu Camp 3D2N'. | Multi-day event is visible. | event start = 10:00; end = 17:00 two days later |
| 2 | Set Range Time filter to 13:00 - 15:00. | Calendar refreshes with the selected range. | rangeTime = 13:00..15:00 |
| 3 | Inspect the multi-day event band. | 'Koyu Camp 3D2N' remains visible because multi-day events bypass Range Time filtering. |  |

**Severity:** major
**Priority:** high

---

### [Koyu2] SF Calendar – Teacher filter – Assigned staff sees multi-day event

**Description:** AC 05 — Decision Table — Multi-day Activity Event respects assigned staff filtering.

**Preconditions:**
- Logged in as HQ or CM Staff to Koyu2 Salesforce org.
- Feature setting MANAERP__Enable_Multiple_Event_Days__c is enabled unless the case says otherwise.
- An Event Master named 'Koyu Outdoor Experience' exists with Event Type = Free, Send To = Parent & Student, Who Can Reserve = Student Only, Open To Booking System = true, Booking Start Date = 2026-09-01, Booking End Date = 2026-12-31.
- Target Location = Tokyo Center; Target Grade = G7; Target Course = Outdoor Program.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Assign staff Teacher A to 'Koyu Camp 3D2N'. | Teacher A appears in Event Staff list. | staff = Teacher A |
| 2 | Open SF Calendar weekly view and filter Teacher = Teacher A. | Calendar applies teacher filter. |  |
| 3 | Inspect event results. | 'Koyu Camp 3D2N' is visible across its date range. |  |
| 4 | Change Teacher filter to Teacher B who is not assigned. | 'Koyu Camp 3D2N' is hidden. | staff = Teacher B |

**Severity:** major
**Priority:** high

---

### [Koyu2] SF Calendar – Event filter off – Multi-day event hidden

**Description:** AC 05 — Decision Table — Calendar type filter still controls multi-day Activity Events.

**Preconditions:**
- Logged in as HQ or CM Staff to Koyu2 Salesforce org.
- Feature setting MANAERP__Enable_Multiple_Event_Days__c is enabled unless the case says otherwise.
- An Event Master named 'Koyu Outdoor Experience' exists with Event Type = Free, Send To = Parent & Student, Who Can Reserve = Student Only, Open To Booking System = true, Booking Start Date = 2026-09-01, Booking End Date = 2026-12-31.
- Target Location = Tokyo Center; Target Grade = G7; Target Course = Outdoor Program.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open SF Calendar weekly view containing lessons and 'Koyu Camp 3D2N'. | Lessons and events are visible. |  |
| 2 | Clear the Events checkbox while keeping Lessons selected. | Calendar refreshes. | types = Lessons only |
| 3 | Inspect the week. | 'Koyu Camp 3D2N' is hidden and lessons remain visible. |  |
| 4 | Select Events again. | 'Koyu Camp 3D2N' becomes visible again. | types = Lessons + Events |

**Severity:** major
**Priority:** high

---

### [Koyu2] SF Calendar – Draft event setting off – Draft multi-day event hidden

**Description:** AC 05 — Status Rule — Draft Activity Events are hidden when draft-event visibility is disabled.

**Preconditions:**
- Logged in as HQ or CM Staff to Koyu2 Salesforce org.
- Multiple event days is enabled.
- Draft event visibility setting is disabled.
- Activity Event 'Koyu Draft Camp' exists with Status = Draft and date range 2026-12-12 10:00 to 2026-12-14 17:00.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open SF Calendar weekly view for 2026-12-08 to 2026-12-14. | Calendar loads. | draft visibility = disabled |
| 2 | Inspect event results. | 'Koyu Draft Camp' is not shown. | status = Draft |
| 3 | Open Event Master related Activity Events list. | 'Koyu Draft Camp' still exists in Salesforce. |  |

**Severity:** major
**Priority:** high

---

### [Koyu2] SF Calendar – Draft event setting on – Draft multi-day event visible

**Description:** AC 05 — Status Rule — Draft Activity Events are shown when draft-event visibility is enabled.

**Preconditions:**
- Logged in as HQ or CM Staff to Koyu2 Salesforce org.
- Multiple event days is enabled.
- Draft event visibility setting is enabled.
- Activity Event 'Koyu Draft Camp' exists with Status = Draft and date range 2026-12-12 10:00 to 2026-12-14 17:00.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open SF Calendar weekly view for 2026-12-08 to 2026-12-14. | Calendar loads. | draft visibility = enabled |
| 2 | Inspect event results. | 'Koyu Draft Camp' is visible as a multi-day event. | status = Draft |
| 3 | Open its detail drawer. | Detail drawer shows Status = Draft and Date Range 2026/12/12 - 2026/12/14. |  |

**Severity:** major
**Priority:** high

---

### [Koyu2] BO Calendar – Weekly view – Multi-day feature flag enabled

**Description:** AC 06 — Back Office Rendering — BO Calendar displays multi-day Activity Events when BO feature config is enabled.

**Preconditions:**
- Logged in as HQ Staff to Back Office.
- FeatureSettingConfig calendar.multiple_event_day.is_enabled is enabled.
- Activity Event 'Koyu Camp 3D2N' exists and is visible to the user location.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Back Office Calendar weekly view for 2026-12-08 to 2026-12-14. | Weekly calendar loads. | BO config = enabled |
| 2 | Select Event filter. | Event data loads. |  |
| 3 | Inspect the weekly event band. | 'Koyu Camp 3D2N' spans 2026-12-12, 2026-12-13, and 2026-12-14. |  |
| 4 | Open the event detail drawer. | General Info shows Date Range 2026/12/12 – 2026/12/14. |  |

**Severity:** critical
**Priority:** high

---

### [Koyu2] BO Calendar – Feature flag disabled – Legacy display does not show multi-day band

**Description:** AC 06 — Feature Flag — BO Calendar keeps legacy behavior when its multiple-event-day config is disabled.

**Preconditions:**
- Logged in as HQ Staff to Back Office.
- FeatureSettingConfig calendar.multiple_event_day.is_enabled is disabled.
- Activity Event 'Koyu Camp 3D2N' exists.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Back Office Calendar weekly view for the event week. | Calendar loads with legacy event rendering. | BO config = disabled |
| 2 | Inspect 2026-12-13 middle day. | No multi-day band is rendered for the middle day. | middle date = 2026-12-13 |
| 3 | Open the event from its start date if visible. | Event detail can still open from the legacy event entry. |  |

**Severity:** major
**Priority:** high

---

### [Koyu2] BO Calendar – Daily view – Middle-day multi-day event visible

**Description:** AC 06 — Back Office Rendering — Daily view shows a multi-day Activity Event on each spanned day.

**Preconditions:**
- Logged in as HQ Staff to Back Office.
- FeatureSettingConfig calendar.multiple_event_day.is_enabled is enabled.
- Activity Event 'Koyu Camp 3D2N' exists.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open BO Calendar daily view for 2026-12-13. | Daily view loads. | middle date = 2026-12-13 |
| 2 | Inspect the event banner area. | 'Koyu Camp 3D2N' is shown. |  |
| 3 | Click the event. | Detail drawer opens and shows the original Activity Event. |  |

**Severity:** major
**Priority:** high

---

### [Koyu2] Activity Event Detail – Salesforce – Multi-day label is Date Range

**Description:** AC 07 — Detail Display — Salesforce Activity Event detail uses Date Range for multi-day Activity Events.

**Preconditions:**
- Logged in as HQ or CM Staff to Koyu2 Salesforce org.
- Feature setting MANAERP__Enable_Multiple_Event_Days__c is enabled unless the case says otherwise.
- An Event Master named 'Koyu Outdoor Experience' exists with Event Type = Free, Send To = Parent & Student, Who Can Reserve = Student Only, Open To Booking System = true, Booking Start Date = 2026-09-01, Booking End Date = 2026-12-31.
- Target Location = Tokyo Center; Target Grade = G7; Target Course = Outdoor Program.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Salesforce Activity Event detail for 'Koyu Camp 3D2N'. | Detail page opens. |  |
| 2 | Inspect General Info. | Label is Date Range and value is 2026/12/12 - 2026/12/14. |  |
| 3 | Inspect Start Time and End Time. | Start Time = 10:00 and End Time = 17:00. |  |

**Severity:** major
**Priority:** high

---

### [Koyu2] Activity Event Detail – Back Office – Multi-day label is Date Range

**Description:** AC 07 — Detail Display — Back Office detail drawer uses Date Range for multi-day Activity Events.

**Preconditions:**
- Logged in as HQ Staff to Back Office.
- BO multiple-event-day config is enabled.
- Activity Event 'Koyu Camp 3D2N' exists.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open BO Calendar and click 'Koyu Camp 3D2N'. | Event detail drawer opens. |  |
| 2 | Inspect General Info date field. | Label is Date Range and value is 2026/12/12 – 2026/12/14. |  |
| 3 | Inspect Start Time and End Time. | Start Time = 10:00 and End Time = 17:00. |  |

**Severity:** major
**Priority:** high

---

### [Koyu2] Activity Event Detail – One-day event – Label remains Event Date

**Description:** AC 07 — Regression — One-day Activity Events do not use Date Range label.

**Preconditions:**
- Logged in as HQ or CM Staff to Koyu2 Salesforce org.
- Feature setting MANAERP__Enable_Multiple_Event_Days__c is enabled unless the case says otherwise.
- An Event Master named 'Koyu Outdoor Experience' exists with Event Type = Free, Send To = Parent & Student, Who Can Reserve = Student Only, Open To Booking System = true, Booking Start Date = 2026-09-01, Booking End Date = 2026-12-31.
- Target Location = Tokyo Center; Target Grade = G7; Target Course = Outdoor Program.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open detail for one-day Activity Event 'Koyu One Day Workshop'. | Detail opens. | start = 2026-10-10 10:00; end = 2026-10-10 12:00 |
| 2 | Inspect General Info date field. | Label is Event Date and value is 2026/10/10. |  |
| 3 | Inspect time fields. | Start Time = 10:00 and End Time = 12:00. |  |

**Severity:** major
**Priority:** high

---

### [Koyu2] Learner App Calendar – Student sees event dot on every spanned day

**Description:** AC 08 — Mobile Calendar — Assigned student sees the multi-day Activity Event across each date in the event range.

**Preconditions:**
- Activity Event 'Koyu Camp 3D2N' is Published and assigned to Student A.
- Student A matches target segment and can log in to Learner App.
- Event Send To = Parent & Student.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Log in to Learner App as Student A. | Student home screen opens. | student = Student A |
| 2 | Open Calendar for December 2026. | Calendar month view opens. |  |
| 3 | Inspect dates 2026-12-12, 2026-12-13, and 2026-12-14. | Each date shows an event indicator for the same Activity Event. | event range = 2026-12-12..2026-12-14 |
| 4 | Tap 2026-12-13. | 'Koyu Camp 3D2N' appears in the selected date event list. | middle date |

**Severity:** critical
**Priority:** high

---

### [Koyu2] Learner App Event Detail – Multi-day range displayed

**Description:** AC 08 — Mobile Detail — Event detail shows full start and end datetime for a multi-day Activity Event.

**Preconditions:**
- Student A is assigned to Activity Event 'Koyu Camp 3D2N'.
- Student A is logged in to Learner App.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Calendar and tap 'Koyu Camp 3D2N'. | Event detail screen opens. |  |
| 2 | Inspect the schedule section. | Start is 2026/12/12 10:00 and End is 2026/12/14 17:00. |  |
| 3 | Return to Calendar and tap 2026-12-14. | The same Activity Event can be opened from the end date. |  |

**Severity:** major
**Priority:** high

---

### [Koyu2] Learner App Response – Accept multi-day event once

**Description:** AC 08 — State Transition — Student or parent response applies to the single Activity Event, not one response per day.

**Preconditions:**
- Activity Event 'Koyu Camp 3D2N' is assigned to Student A.
- Allow Response = Parent & Student.
- Student A has not responded.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Log in to Learner App as Student A and open 'Koyu Camp 3D2N'. | Event detail shows Accept and Decline actions. |  |
| 2 | Tap Accept. | Response is submitted successfully. | response = Accept |
| 3 | Open Salesforce Activity Event participant list. | Student A has one Event Participant record with Response = Accept. | expected records = 1 |
| 4 | Open 2026-12-13 in Learner App Calendar. | The same accepted event is shown; no duplicate response is requested for the middle day. |  |

**Severity:** critical
**Priority:** high

---

### [Koyu2] Booking System – Event list – Multi-day activity shown under matching Event Master

**Description:** AC 09 — Booking Flow — Booking System shows Event Master and available multi-day Activity Event.

**Preconditions:**
- Event Master is open to booking with Booking Start Date 2026-09-01 and Booking End Date 2026-12-31.
- Activity Event 'Koyu Camp 3D2N' is Published, future-dated, capacity 30, and has remaining seats.
- Student A matches target segment.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Log in to Learner App as Student A and open Booking System. | Booking System opens. | today = 2026-09-10 |
| 2 | Search or filter for Event Master 'Koyu Outdoor Experience'. | Event Master is visible. | target segment matches Student A |
| 3 | Open the Event Master activity list. | 'Koyu Camp 3D2N' is listed with start 2026/12/12 10:00 and end 2026/12/14 17:00. |  |

**Severity:** critical
**Priority:** high

---

### [Koyu2] Booking System – Reserve – One participant record created

**Description:** AC 09 — Booking Flow — Reserving a multi-day Activity Event creates one participant record for the single Activity Event.

**Preconditions:**
- Student A matches target segment.
- Activity Event 'Koyu Camp 3D2N' is open for booking and has remaining capacity.
- Student A has no existing Event Participant for this Activity Event.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Booking System as Student A. | Available events are shown. |  |
| 2 | Open 'Koyu Camp 3D2N' and click Reserve. | Reservation confirmation is shown. | activityEventId = Koyu Camp 3D2N |
| 3 | Confirm reservation. | Reservation succeeds. |  |
| 4 | Open Salesforce Activity Event participant list. | Exactly one Event Participant exists for Student A under 'Koyu Camp 3D2N'. | expected records = 1 |

**Severity:** critical
**Priority:** high

---

### [Koyu2] Booking System – Search by middle date – Multi-day activity remains discoverable

**Description:** AC 09 — Search/Filter — Activity Event is discoverable when the user searches a date inside the multi-day range.

**Preconditions:**
- Activity Event 'Koyu Camp 3D2N' exists with date range 2026-12-12 10:00 to 2026-12-14 17:00.
- Student A can access Booking System.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Booking System as Student A. | Booking System opens. |  |
| 2 | Filter date to 2026-12-13. | Filter is applied. | selected date = middle day |
| 3 | Inspect event results. | 'Koyu Camp 3D2N' is shown because 2026-12-13 is within its date range. |  |

**Severity:** major
**Priority:** high

---

### [Koyu2] Booking System – Capacity – Multi-day reservation consumes one seat

**Description:** AC 09 — Capacity Rule — Reserving a multi-day Activity Event decreases remaining capacity by one, not by number of days.

**Preconditions:**
- Activity Event 'Koyu Camp 3D2N' has Event Capacity = 30 and Participant Count = 5.
- Student A has not reserved it.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Booking System and view 'Koyu Camp 3D2N'. | Remaining capacity shows 25. | capacity = 30; participantCount = 5 |
| 2 | Reserve the event as Student A. | Reservation succeeds. |  |
| 3 | Refresh the Activity Event or Booking System list. | Participant Count becomes 6 and remaining capacity becomes 24. | one reservation = one seat |

**Severity:** major
**Priority:** high

---

### [Koyu2] Booking System – Cancellation deadline – Uses Activity Event start datetime

**Description:** AC 09 — Deadline Rule — Cancellation deadline is calculated from Activity Event Start DateTime, not Event Master booking dates or End DateTime.

**Preconditions:**
- Event Master Cancellation Type allows cancellation with deadline.
- Cancellation Deadline Hours = 24.
- Activity Event 'Koyu Camp 3D2N' starts 2026-12-12 10:00 and ends 2026-12-14 17:00.
- Student A has reserved it.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Set system date/time to 2026-12-11 09:59 JST or use test data with equivalent clock. | Current time is before cancellation deadline. | deadline = 2026-12-11 10:00 JST |
| 2 | Open reservation detail in Learner App. | Cancel action is available. | now < deadline |
| 3 | Set system date/time to 2026-12-11 10:01 JST or use equivalent test clock. | Current time is after cancellation deadline. | now > deadline |
| 4 | Open reservation detail again. | Cancel action is blocked or unavailable according to existing Koyu cancellation rule. | deadline source = Activity Event Start DateTime |

**Severity:** critical
**Priority:** high

---

### [Koyu2] Auto Create Application – Multi-day reservation – Application linked once

**Description:** AC 10 — Koyu Integration — Auto-create application runs once for a multi-day event reservation.

**Preconditions:**
- Event Master has Is Create Application at the Booking = true.
- Student A reserves Activity Event 'Koyu Camp 3D2N'.
- Koyu auto-create application feature is enabled.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Reserve 'Koyu Camp 3D2N' as Student A. | Reservation succeeds. |  |
| 2 | Open Student A applications. | One Application record is created for the event reservation. | expected applications = 1 |
| 3 | Inspect Application linkage. | Application is linked to the same Activity Event ID and Event Participant ID. |  |
| 4 | Inspect applications for each event date. | No separate applications are created for 2026-12-13 or 2026-12-14. | multi-day is single Activity Event |

**Severity:** critical
**Priority:** high

---

### [Koyu2] Get Event API – Full date range – Multi-day activity returned

**Description:** AC 11 — API Contract — Get Event API returns multi-day Activity Event when Start and End datetime are fully inside request range.

**Preconditions:**
- API client can call /event_masters/v1.
- Event Master is open for booking and target_location includes tokyo-center.
- Activity Event 'Koyu Camp 3D2N' is Published and starts 2026-12-12T01:00:00Z, ends 2026-12-14T08:00:00Z.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Call Get Event API with start_date=2026-12-01T00:00:00Z, end_date=2026-12-31T23:59:59Z, target_location=tokyo-center. | API returns HTTP 200. | request range contains full activity range |
| 2 | Inspect response events array. | Event Master 'Koyu Outdoor Experience' is returned. |  |
| 3 | Inspect activities array for that Event Master. | 'Koyu Camp 3D2N' is returned with startDatetime and endDatetime matching the Activity Event. |  |

**Severity:** critical
**Priority:** high

---

### [Koyu2] Get Event API – Partial overlap at request start – Activity excluded

**Description:** AC 11 — Boundary Rule — Current API requires Activity Event Start DateTime to be on or after request start_date.

**Preconditions:**
- Activity Event 'Koyu Camp 3D2N' starts 2026-12-12T01:00:00Z and ends 2026-12-14T08:00:00Z.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Call Get Event API with start_date=2026-12-13T00:00:00Z, end_date=2026-12-31T23:59:59Z, target_location=tokyo-center. | API returns HTTP 200. | request overlaps middle/end only |
| 2 | Inspect activities array. | 'Koyu Camp 3D2N' is not returned because its Start DateTime is before request start_date. | query rule = Start_Date_Time__c >= start_date |

**Severity:** major
**Priority:** high

---

### [Koyu2] Get Event API – Partial overlap at request end – Activity excluded

**Description:** AC 11 — Boundary Rule — Current API requires Activity Event End DateTime to be on or before request end_date.

**Preconditions:**
- Activity Event 'Koyu Camp 3D2N' starts 2026-12-12T01:00:00Z and ends 2026-12-14T08:00:00Z.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Call Get Event API with start_date=2026-12-01T00:00:00Z, end_date=2026-12-13T23:59:59Z, target_location=tokyo-center. | API returns HTTP 200. | request overlaps start/middle only |
| 2 | Inspect activities array. | 'Koyu Camp 3D2N' is not returned because its End DateTime is after request end_date. | query rule = End_Date_Time__c <= end_date |

**Severity:** major
**Priority:** high

---

### [Koyu2] Get Event API – Invalid range – Error returned

**Description:** AC 11 — Negative Testing — API rejects request when start_date is not before end_date.

**Preconditions:**
- API client can call /event_masters/v1.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Call Get Event API with start_date=2026-12-14T00:00:00Z and end_date=2026-12-12T00:00:00Z. | API returns HTTP 400. | start_date >= end_date |
| 2 | Inspect error message. | Response says 'start_date must be before end_date'. |  |

**Severity:** major
**Priority:** high

---

### [Koyu2] Activity Event API – Assigned student date range – Multi-day event returned

**Description:** AC 12 — Mobile API — Assigned participant API returns multi-day Activity Event when it fits from_date/to_date.

**Preconditions:**
- Student A is assigned to Activity Event 'Koyu Camp 3D2N'.
- API client can call /activity_events.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Call Activity Events API with user_id=Student A, login_user_id=Student A, from_date=2026-12-01 00:00:00, to_date=2026-12-31 23:59:59. | API returns HTTP 200. | full month range |
| 2 | Inspect returned events. | 'Koyu Camp 3D2N' appears with start_date_time and end_date_time values. |  |
| 3 | Inspect participant fields. | Response and attendance status are returned for the same Event Participant record. |  |

**Severity:** major
**Priority:** high

---

### [Koyu2] Attendance – Multi-day activity – One attendance list for the event

**Description:** AC 13 — Attendance Flow — Collect attendance works against the single Activity Event participant list.

**Preconditions:**
- Activity Event 'Koyu Camp 3D2N' has participants Student A and Student B.
- Event Status = Published or Completed according to existing attendance rule.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Activity Event detail for 'Koyu Camp 3D2N'. | Detail page opens with participants list. | participants = Student A, Student B |
| 2 | Click Collect Attendance. | Attendance modal opens with Student A and Student B once each. | expected duplicate count = 0 |
| 3 | Mark Student A = Attend and Student B = Absent, then save. | Attendance is saved successfully. |  |
| 4 | Reopen participant list. | Student A and Student B show their saved attendance statuses for the Activity Event. | single event-level attendance |

**Severity:** critical
**Priority:** high

---

### [Koyu2] Participant CSV – Multi-day activity – Export contains full date range

**Description:** AC 13 — Export Regression — Participant export remains tied to the Activity Event and includes enough date context for multi-day events.

**Preconditions:**
- Activity Event 'Koyu Camp 3D2N' has at least one participant.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Activity Event detail for 'Koyu Camp 3D2N'. | Detail page opens. |  |
| 2 | Click Download Participant List. | Participant CSV is downloaded. |  |
| 3 | Open the CSV. | CSV contains participants once and identifies the Activity Event with its start/end datetime or date range according to current export format. | expected duplicate participant rows = 0 |

**Severity:** major
**Priority:** high

---

### [Koyu2] Calendar – Multi-day event crossing week boundary – Weekly band clamps to visible week

**Description:** AC 05 — Boundary Value — Weekly calendar displays the visible part of a multi-day Activity Event that starts before the current week.

**Preconditions:**
- Logged in as HQ or CM Staff to Koyu2 Salesforce org.
- Feature setting MANAERP__Enable_Multiple_Event_Days__c is enabled unless the case says otherwise.
- An Event Master named 'Koyu Outdoor Experience' exists with Event Type = Free, Send To = Parent & Student, Who Can Reserve = Student Only, Open To Booking System = true, Booking Start Date = 2026-09-01, Booking End Date = 2026-12-31.
- Target Location = Tokyo Center; Target Grade = G7; Target Course = Outdoor Program.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Create Activity Event 'Koyu Cross Week Camp' from 2026-12-06 10:00 to 2026-12-09 17:00. | Activity Event is created. | week view = 2026-12-08..2026-12-14 |
| 2 | Open SF Calendar weekly view for 2026-12-08 to 2026-12-14. | Weekly calendar loads. |  |
| 3 | Inspect multi-day band. | 'Koyu Cross Week Camp' appears from 2026-12-08 through 2026-12-09 only within the visible week. | visible clamp = Tue-Wed |

**Severity:** major
**Priority:** high

---

### [Koyu2] Calendar – Overlapping multi-day events – Bars stack without overlap

**Description:** AC 05 — Layout Regression — Overlapping multi-day Activity Events are stacked in separate rows.

**Preconditions:**
- Logged in as HQ or CM Staff to Koyu2 Salesforce org.
- Feature setting MANAERP__Enable_Multiple_Event_Days__c is enabled unless the case says otherwise.
- An Event Master named 'Koyu Outdoor Experience' exists with Event Type = Free, Send To = Parent & Student, Who Can Reserve = Student Only, Open To Booking System = true, Booking Start Date = 2026-09-01, Booking End Date = 2026-12-31.
- Target Location = Tokyo Center; Target Grade = G7; Target Course = Outdoor Program.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Create Activity Event A from 2026-12-12 10:00 to 2026-12-14 17:00. | Event A exists. |  |
| 2 | Create Activity Event B from 2026-12-13 09:00 to 2026-12-15 12:00. | Event B exists. |  |
| 3 | Open weekly calendar for 2026-12-08 to 2026-12-14. | Weekly calendar loads. |  |
| 4 | Inspect 2026-12-13. | Event A and Event B are both visible and stacked; text remains readable and clickable. | overlap date = 2026-12-13 |

**Severity:** major
**Priority:** high

---

### [Koyu2] Calendar – Multi-day event with lessons – Lessons remain visible

**Description:** AC 05 — Cross-domain Regression — Multi-day Activity Events do not hide normal lesson cards in the same week.

**Preconditions:**
- Logged in as HQ or CM Staff to Koyu2 Salesforce org.
- Feature setting MANAERP__Enable_Multiple_Event_Days__c is enabled unless the case says otherwise.
- An Event Master named 'Koyu Outdoor Experience' exists with Event Type = Free, Send To = Parent & Student, Who Can Reserve = Student Only, Open To Booking System = true, Booking Start Date = 2026-09-01, Booking End Date = 2026-12-31.
- Target Location = Tokyo Center; Target Grade = G7; Target Course = Outdoor Program.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Create or confirm a lesson on 2026-12-13 13:00 to 14:00 in Tokyo Center. | Lesson exists. | lesson date overlaps multi-day event |
| 2 | Open weekly calendar for 2026-12-08 to 2026-12-14 with Lessons and Events selected. | Calendar loads both object types. |  |
| 3 | Inspect 2026-12-13. | 'Koyu Camp 3D2N' and the lesson are both visible; selecting either opens the correct detail drawer. |  |

**Severity:** major
**Priority:** high

---

### [Koyu2] Activity Event – Paid multi-day event – Product Offering remains required

**Description:** AC 14 — Paid Event Regression — Multi-day scheduling does not bypass paid-event required fields.

**Preconditions:**
- Paid Event feature is enabled.
- Event Master 'Koyu Paid Camp' exists with Event Type = Paid.
- Multiple event days is enabled.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open New Activity Event from Event Master 'Koyu Paid Camp'. | New Activity Event form opens. | event type = Paid |
| 2 | Enter valid date range 2026-12-12 10:00 to 2026-12-14 17:00 and leave Product Offering empty. | Date/time values are valid but Product Offering is blank. |  |
| 3 | Click Save. | Save is blocked by Product Offering required validation. |  |
| 4 | Select a Product Offering and save again. | Paid multi-day Activity Event is created successfully. |  |

**Severity:** major
**Priority:** high

---

### [Koyu2] Activity Event – Extra participants – Multi-day event keeps participant setting validation

**Description:** AC 14 — Regression — Multi-day scheduling does not bypass extra participant constraints.

**Preconditions:**
- Logged in as HQ or CM Staff to Koyu2 Salesforce org.
- Feature setting MANAERP__Enable_Multiple_Event_Days__c is enabled unless the case says otherwise.
- An Event Master named 'Koyu Outdoor Experience' exists with Event Type = Free, Send To = Parent & Student, Who Can Reserve = Student Only, Open To Booking System = true, Booking Start Date = 2026-09-01, Booking End Date = 2026-12-31.
- Target Location = Tokyo Center; Target Grade = G7; Target Course = Outdoor Program.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open New Activity Event. | Form opens. |  |
| 2 | Enter valid multi-day date range and enable Allow Extra Participants. | Extra participant field is enabled. | start = 2026-12-12 10:00; end = 2026-12-14 17:00 |
| 3 | Enter invalid extra participant value according to existing Koyu rule. | Field displays validation error. | example invalid value = -1 or above configured maximum |
| 4 | Correct the value and save. | Activity Event is saved only after participant settings are valid. |  |

**Severity:** major
**Priority:** high

---

### [Koyu2] SF Bulk Import – Activity Event multi-day row imports successfully

**Description:** AC 15 — Import Happy Path — Bulk import creates one Activity Event record with Start Date Time and End Date Time spanning multiple days.

**Preconditions:**
- Logged in as HQ or CM Staff to Koyu2 Salesforce org.
- Multiple event days is enabled.
- Event Master 'Koyu Outdoor Experience' exists.
- A valid Activity Event import CSV is prepared with Start Date Time = 2026-12-12 10:00 and End Date Time = 2026-12-14 17:00.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open the Salesforce bulk import flow for Activity Event. | Import page opens. | object = Activity Event |
| 2 | Upload the prepared CSV file. | File is accepted and preview shows the multi-day row without validation errors. | start = 2026-12-12 10:00; end = 2026-12-14 17:00 |
| 3 | Execute the import. | Import completes successfully. |  |
| 4 | Open the imported Activity Event detail page. | One Activity Event exists under the Event Master and Date Range shows 2026/12/12 - 2026/12/14 with Start Time 10:00 and End Time 17:00. |  |

**Severity:** critical
**Priority:** high

---

### [Koyu2] SF Bulk Import – Single-day Activity Event row still imports after multi-day change

**Description:** AC 15 — Import Regression — Existing one-day Activity Event import remains valid when Start Date Time and End Date Time are on the same calendar date.

**Preconditions:**
- Logged in as HQ or CM Staff to Koyu2 Salesforce org.
- Multiple event days is enabled.
- Event Master 'Koyu Outdoor Experience' exists.
- A valid Activity Event import CSV is prepared with Start Date Time = 2026-10-10 10:00 and End Date Time = 2026-10-10 12:00.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open the Salesforce bulk import flow for Activity Event. | Import page opens. |  |
| 2 | Upload the single-day Activity Event CSV. | File is accepted and row preview is valid. | start date = end date |
| 3 | Execute the import. | Import completes successfully. |  |
| 4 | Open the imported Activity Event detail page. | Detail shows Date 2026/10/10, Start Time 10:00, End Time 12:00; no duplicate per-day records are created. |  |

**Severity:** major
**Priority:** high

---

### [Koyu2] SF Bulk Import – Invalid multi-day row with End Date before Start Date is rejected

**Description:** AC 15 — Import Negative — Bulk import enforces Activity Event date range validation and rejects rows where End Date Time is before Start Date Time.

**Preconditions:**
- Logged in as HQ or CM Staff to Koyu2 Salesforce org.
- Multiple event days is enabled.
- Event Master 'Koyu Outdoor Experience' exists.
- An Activity Event import CSV is prepared with Start Date Time = 2026-12-14 10:00 and End Date Time = 2026-12-12 17:00.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open the Salesforce bulk import flow for Activity Event. | Import page opens. |  |
| 2 | Upload the invalid CSV file. | Import preview or validation result marks the row invalid. | start > end |
| 3 | Execute import if the UI allows continuing. | Invalid row is rejected and no Activity Event is created for that row. |  |
| 4 | Search Activity Events by the row name. | No record exists for the rejected row. |  |

**Severity:** critical
**Priority:** high

---

### [Koyu2] SF Bulk Import – Mixed valid and invalid rows only create valid Activity Events

**Description:** AC 15 — Import Data Integrity — A mixed import file creates valid multi-day rows and rejects invalid rows without corrupting Event Master or Activity Event data.

**Preconditions:**
- Logged in as HQ or CM Staff to Koyu2 Salesforce org.
- Multiple event days is enabled.
- Event Master 'Koyu Outdoor Experience' exists.
- A mixed Activity Event import CSV is prepared with two valid rows and one invalid row where End Date Time is before Start Date Time.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open the Salesforce bulk import flow for Activity Event. | Import page opens. |  |
| 2 | Upload the mixed CSV file. | Valid rows are accepted; invalid row is flagged with date range validation. | row A valid multi-day; row B invalid; row C valid one-day |
| 3 | Execute the import. | Only valid rows are imported; invalid row is skipped or rejected with an error result. |  |
| 4 | Open Event Master related Activity Events list. | Exactly the valid imported Activity Events are listed; the invalid row name is absent. | expected created rows = A and C only |

**Severity:** critical
**Priority:** high

---
