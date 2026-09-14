# Test Cases: LT-103775 - SF Calendar Draft Activity Events

## Suite: PX > Manabie Scheduling > CORE FEATURES > Event Master > update testcase > Calendar lesson (suite 2717)

### [Core] SF Calendar - Draft Activity Event - Weekly view shows draft card when feature is enabled

**Description:** AC 01 - Decision Table - Draft Activity Event is visible on SF Lesson Calendar only when Draft Activity Event feature is enabled.

**Preconditions:**
- Logged in as HQ or CM Staff to Salesforce org.
- `MANAERP__Enable_Draft_Status_On_Activity_Event__c = true`.
- Event Master `Core Draft Calendar Event` exists.
- Activity Event `Draft Workshop A` exists with Event Status = Draft, Location = Tokyo Center, Event Medium = Offline, Capacity = 20, Start Date Time = 2026-09-14 10:00 JST, End Date Time = 2026-09-14 11:00 JST.
- Calendar location filter is Tokyo Center.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open SF Lesson Calendar in Weekly view. | Calendar loads for Tokyo Center. | today = 2026-08-12; calendar_week = 2026-09-14 to 2026-09-20; flag = on |
| 2 | Confirm Event type filter is selected. | Activity Events are included in calendar results. | type_filter = Lesson + Event |
| 3 | Keep default Status filter values. | Draft card is not shown because default status filter excludes Draft. | default statuses = Published, Completed |
| 4 | Add Draft to the Status filter. | `Draft Workshop A` appears in the 2026-09-14 10:00 slot. | status_filter = Draft, Published, Completed |

**Severity:** critical
**Priority:** high

---

### [Core] SF Calendar - Draft Activity Event - Feature disabled hides draft card

**Description:** AC 08 - Decision Table - Draft Activity Event is filtered out when the feature flag is disabled.

**Preconditions:**
- Logged in as HQ or CM Staff to Salesforce org where `MANAERP__Enable_Draft_Status_On_Activity_Event__c = false`.
- Draft Activity Event `Draft Workshop A` and Published Activity Event `Published Workshop A` exist on 2026-09-14 in Tokyo Center.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open SF Lesson Calendar in Weekly view for Tokyo Center. | Calendar loads. | today = 2026-08-12; flag = off |
| 2 | Select Draft in the Status filter. | `Draft Workshop A` is not displayed. | status_filter = Draft |
| 3 | Select Published in the Status filter. | `Published Workshop A` is displayed. | status_filter = Published |

**Severity:** critical
**Priority:** high

---

### [Core] SF Calendar - Draft Activity Event - Non-SF calendar hides draft card

**Description:** AC 08 - Regression - Draft Activity Event remains hidden outside the SF Calendar runtime.

**Preconditions:**
- Logged in as HQ Staff to Back Office.
- Draft Activity Event `Draft Workshop A` exists in Tokyo Center on 2026-09-14.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Back Office Calendar for Tokyo Center. | Calendar loads. | today = 2026-08-12; runtime = non-SF |
| 2 | Navigate to 2026-09-14. | Published calendar items display as usual. | event_date = 2026-09-14 |
| 3 | Search visible calendar cards for `Draft Workshop A`. | Draft Activity Event is not displayed. | expected_visibility = hidden |

**Severity:** critical
**Priority:** high

---

### [Core] SF Calendar - Draft Activity Event - Card uses draft event green outline

**Description:** AC 02 - Component - Single-day Draft Event card uses Draft styling copied from Draft Lesson but with event green color.

**Preconditions:**
- Logged in as HQ or CM Staff to Salesforce org.
- Draft Activity Event `Draft Workshop A` is visible in SF Calendar Weekly view.
- Published Activity Event `Published Workshop A` is visible in the same week.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open SF Lesson Calendar Weekly view and select Draft and Published statuses. | Both draft and published event cards are visible. | flag = on; statuses = Draft, Published |
| 2 | Inspect `Draft Workshop A` card. | Card has white background, green border, normal text, and participant/capacity chip. | draft_style = white + green border |
| 3 | Inspect `Published Workshop A` card. | Card uses filled green event styling. | published_style = green filled |
| 4 | Compare card text. | Both cards show time range, event name, and capacity without text overlap. | draft_start = 10:00; capacity = 20 |

**Severity:** major
**Priority:** high

---

### [Core] SF Calendar - Draft Activity Event - Daily view shows draft card in correct time slot

**Description:** AC 01 - Regression - Draft Event is shown in Daily view at its scheduled time.

**Preconditions:**
- Logged in as HQ or CM Staff to Salesforce org.
- Draft Activity Event `Draft Workshop A` exists from 2026-09-14 10:00 to 11:00 JST.
- Feature flag is enabled.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open SF Lesson Calendar in Daily view for 2026-09-14. | Daily view loads. | today = 2026-08-12; calendar_date = 2026-09-14 |
| 2 | Select Draft in Status filter and Event in type filter. | Draft Event cards are eligible to display. | status_filter = Draft; type_filter includes Event |
| 3 | Inspect the 10:00 to 11:00 area. | `Draft Workshop A` appears in the correct time slot with draft event styling. | start = 10:00; end = 11:00 |

**Severity:** major
**Priority:** high

---

### [Core] SF Calendar - Draft Activity Event - Multi-day draft event shows in weekly band

**Description:** AC 01 - Regression - Multi-day Draft Event is shown as a weekly band when multi-day events are enabled.

**Preconditions:**
- Logged in as HQ or CM Staff to Salesforce org.
- `MANAERP__Enable_Draft_Status_On_Activity_Event__c = true`.
- `MANAERP__Enable_Multiple_Event_Days__c = true`.
- Draft Activity Event `Draft Camp 2D1N` exists from 2026-09-16 10:00 to 2026-09-17 17:00 JST.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open SF Lesson Calendar Weekly view for 2026-09-14 to 2026-09-20. | Weekly view loads. | today = 2026-08-12; week = 2026-09-14 |
| 2 | Select Draft in the Status filter. | Draft status is active. | status_filter = Draft |
| 3 | Inspect the multi-day event band area. | `Draft Camp 2D1N` appears as a spanning bar across 2026-09-16 and 2026-09-17. | start = 2026-09-16 10:00; end = 2026-09-17 17:00 |
| 4 | Inspect the bar styling. | Bar has white background, green border, name, date range, time range, and capacity chip. | status = Draft |

**Severity:** major
**Priority:** high

---

### [Core] SF Calendar - Draft Activity Event - Click opens Activity Event detail drawer

**Description:** AC 03 - Scenario - Clicking a Draft Event opens the Activity Event detail drawer on the right side.

**Preconditions:**
- Logged in as HQ or CM Staff to Salesforce org.
- Draft Activity Event `Draft Workshop A` is visible in SF Calendar.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open SF Lesson Calendar Weekly view with Draft status selected. | `Draft Workshop A` is visible. | event_id = AE-DRAFT-A |
| 2 | Click `Draft Workshop A`. | Right-side drawer opens. | objectType = ACTIVITY |
| 3 | Inspect drawer header and General Info tab. | Drawer shows Activity Event detail, not Lesson detail. | drawerLessonDetail = AE-DRAFT-A |
| 4 | Click the same event card again. | Drawer closes and calendar width returns to full view. | toggle_same_card = true |

**Severity:** major
**Priority:** high

---

### [Core] SF Calendar - Draft Activity Event - Detail drawer shows event fields

**Description:** AC 03 - Display Completeness - Activity Event detail drawer contains required general information for a Draft Event.

**Preconditions:**
- Logged in as HQ or CM Staff to Salesforce org.
- Draft Activity Event `Draft Workshop A` is visible and has Event Master, Location, Date/Time, Capacity, Event Medium, Classroom, Staff, and Participants.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Click `Draft Workshop A` in SF Calendar. | Activity Event drawer opens. | event = Draft Workshop A |
| 2 | Open General Info tab. | Event Master, Location, Event Date, Start Time, End Time, Event Capacity, Event Medium, Classroom, Staff, and Participants are shown. | start = 2026-09-14 10:00; end = 11:00 |
| 3 | Click Event Master link. | Salesforce opens the related Event Master record in a new tab/window. | Event Master = Core Draft Calendar Event |
| 4 | Return to the drawer. | Drawer remains on Activity Event detail. | objectType = ACTIVITY |

**Severity:** major
**Priority:** high

---

### [Core] SF Calendar - Status filter - Draft shows draft lessons and draft events

**Description:** AC 04 - Decision Table - The Draft status filter applies to both Lessons and Activity Events.

**Preconditions:**
- Logged in as HQ or CM Staff to Salesforce org.
- Draft Lesson `Draft Lesson A` and Draft Activity Event `Draft Workshop A` exist on 2026-09-14 in Tokyo Center.
- Published Lesson `Published Lesson A` and Published Activity Event `Published Workshop A` exist in the same week.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open SF Lesson Calendar Weekly view. | Calendar loads. | today = 2026-08-12; flag = on |
| 2 | Set Status filter to Draft only. | Only Draft status is active. | status_filter = Draft |
| 3 | Inspect visible cards. | `Draft Lesson A` and `Draft Workshop A` are visible; `Published Lesson A` and `Published Workshop A` are hidden. | expected_visible = draft lesson + draft event |

**Severity:** critical
**Priority:** high

---

### [Core] SF Calendar - Status filter - Published hides draft event

**Description:** AC 04 - Decision Table - Published status filter excludes Draft Events.

**Preconditions:**
- Logged in as HQ or CM Staff to Salesforce org.
- Draft and Published Lessons and Activity Events exist in the same week.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open SF Lesson Calendar Weekly view. | Calendar loads. | today = 2026-08-12 |
| 2 | Set Status filter to Published only. | Published status is active. | status_filter = Published |
| 3 | Inspect visible cards. | Published Lesson and Published Event are visible; Draft Lesson and Draft Event are hidden. | expected_hidden = Draft Workshop A |

**Severity:** major
**Priority:** high

---

### [Core] SF Calendar - Status filter - Draft plus Published shows both statuses

**Description:** AC 04 - Pairwise - Multiple selected statuses include both matching Lessons and matching Activity Events.

**Preconditions:**
- Logged in as HQ or CM Staff to Salesforce org.
- Draft and Published Lessons and Activity Events exist in Tokyo Center.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open SF Lesson Calendar Weekly view. | Calendar loads. | today = 2026-08-12 |
| 2 | Select Draft and Published in Status filter. | Two statuses are active. | status_filter = Draft, Published |
| 3 | Inspect visible cards. | Draft Lesson, Draft Event, Published Lesson, and Published Event are visible; Completed and Cancelled items are hidden. | expected_visible_statuses = Draft, Published |

**Severity:** major
**Priority:** high

---

### [Core] SF Calendar - Default Status filter - Draft event hidden until Draft selected

**Description:** AC 04 - Regression - Default calendar status filter remains Published and Completed only.

**Preconditions:**
- Logged in as HQ or CM Staff to Salesforce org.
- Draft Activity Event `Draft Workshop A`, Published Activity Event `Published Workshop A`, and Completed Lesson `Completed Lesson A` exist in the selected week.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open SF Lesson Calendar after clearing saved filters. | Calendar opens with default filter state. | default statuses = Published, Completed |
| 2 | Inspect visible cards. | `Published Workshop A` and `Completed Lesson A` are visible; `Draft Workshop A` is hidden. | status_filter = default |
| 3 | Add Draft to the Status filter. | `Draft Workshop A` appears. | status_filter = Draft, Published, Completed |

**Severity:** major
**Priority:** high

---

### [Core] SF Calendar - Event type filter - Events off hides draft event

**Description:** AC 04 - Conditional - Event type filter still controls Draft Event visibility.

**Preconditions:**
- Logged in as HQ or CM Staff to Salesforce org.
- Draft Lesson `Draft Lesson A` and Draft Activity Event `Draft Workshop A` exist on 2026-09-14.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open SF Lesson Calendar Weekly view and select Draft status. | Draft Lesson and Draft Event are visible. | status_filter = Draft; type_filter = Lesson + Event |
| 2 | Turn off Event type filter and keep Lesson selected. | Activity Events are excluded. | type_filter = Lesson only |
| 3 | Inspect visible cards. | `Draft Lesson A` remains visible; `Draft Workshop A` is hidden. | expected_visible = lesson only |

**Severity:** major
**Priority:** high

---

### [Core] SF Calendar - Event type filter - Lessons off still shows draft event

**Description:** AC 04 - Conditional - Draft Event remains visible when Event type is selected and Lesson type is not selected.

**Preconditions:**
- Logged in as HQ or CM Staff to Salesforce org.
- Draft Lesson `Draft Lesson A` and Draft Activity Event `Draft Workshop A` exist on 2026-09-14.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open SF Lesson Calendar Weekly view and select Draft status. | Draft Lesson and Draft Event are visible. | status_filter = Draft |
| 2 | Turn off Lesson type filter and keep Event selected. | Lessons are excluded. | type_filter = Event only |
| 3 | Inspect visible cards. | `Draft Workshop A` remains visible; `Draft Lesson A` is hidden. | expected_visible = event only |

**Severity:** major
**Priority:** high

---

### [Core] SF Calendar - Teacher filter - Assigned staff sees matching draft event

**Description:** AC 04 - Pairwise - Teacher filter applies to Draft Activity Events through assigned Event Staff.

**Preconditions:**
- Logged in as HQ or CM Staff to Salesforce org.
- Draft Activity Event `Draft Workshop Staff A` exists with Event Staff = Teacher A.
- Draft Activity Event `Draft Workshop Staff B` exists with Event Staff = Teacher B.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open SF Lesson Calendar Weekly view and select Draft status. | Both draft events are visible. | status_filter = Draft |
| 2 | Apply Teacher filter = Teacher A. | Teacher filter is active. | teacher = Teacher A |
| 3 | Inspect visible event cards. | `Draft Workshop Staff A` is visible; `Draft Workshop Staff B` is hidden. | event_staff = Teacher A |

**Severity:** major
**Priority:** high

---

### [Core] SF Calendar - Capacity filter - Draft event respects capacity status

**Description:** AC 04 - Pairwise - Capacity filter applies to Draft Activity Events.

**Preconditions:**
- Logged in as HQ or CM Staff to Salesforce org.
- Draft Activity Event `Draft Under Capacity` exists with Capacity = 5 and 2 participants.
- Draft Activity Event `Draft Meet Capacity` exists with Capacity = 2 and 2 participants.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open SF Lesson Calendar Weekly view and select Draft status. | Both Draft Events are visible. | status_filter = Draft |
| 2 | Apply Capacity filter = Under Capacity. | Under Capacity filter is active. | under = 2/5 |
| 3 | Inspect visible event cards. | `Draft Under Capacity` is visible; `Draft Meet Capacity` is hidden. | meet = 2/2 |

**Severity:** minor
**Priority:** medium

---

### [Core] SF Calendar - Range time filter - Single-day draft event outside range hidden

**Description:** AC 04 - Boundary Value - Range time filter applies to single-day Draft Events.

**Preconditions:**
- Logged in as HQ or CM Staff to Salesforce org.
- Draft Activity Event `Draft Morning Event` exists from 2026-09-14 10:00 to 11:00 JST.
- Draft Activity Event `Draft Evening Event` exists from 2026-09-14 19:00 to 20:00 JST.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open SF Lesson Calendar Daily view for 2026-09-14 and select Draft status. | Both Draft Events are eligible by status. | today = 2026-08-12; date = 2026-09-14 |
| 2 | Set visible time range to 09:00 to 18:00. | Range filter is applied. | range_start = 09:00; range_end = 18:00 |
| 3 | Inspect visible event cards. | `Draft Morning Event` is visible; `Draft Evening Event` is hidden. | morning_start = 10:00; evening_start = 19:00 |

**Severity:** minor
**Priority:** medium

---

### [Core] SF Calendar - Drag Draft Event - Edit Event UI opens with dropped time

**Description:** AC 05/06 - State Transition - Dragging a single-day Draft Event opens Edit Event UI with Date and Time from the drop tile.

**Preconditions:**
- Logged in as HQ or CM Staff to Salesforce org.
- Calendar DnD feature is enabled.
- Draft Activity Event `Draft Workshop A` exists from 2026-09-14 10:00 to 11:00 JST in Tokyo Center.
- Draft Activity Event feature flag is enabled.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open SF Lesson Calendar Weekly view and select Draft status. | `Draft Workshop A` is visible and draggable. | today = 2026-08-12; original = 2026-09-14 10:00-11:00 |
| 2 | Drag `Draft Workshop A` to 2026-09-15 13:00 tile. | Edit Activity Event UI opens. | drop_tile = 2026-09-15 13:00 |
| 3 | Inspect the date/time fields before saving. | Date = 2026-09-15, Start Time = 13:00, End Time = 14:00; Status remains Draft. | original_duration = 60 minutes |

**Severity:** critical
**Priority:** high

---

### [Core] SF Calendar - Drag Draft Event - Save moves card to drop area

**Description:** AC 07 - State Transition - Saving the Edit Event UI after drag/drop updates the Activity Event location on calendar.

**Preconditions:**
- Logged in as HQ or CM Staff to Salesforce org.
- Edit Activity Event UI is open after dragging `Draft Workshop A` to 2026-09-15 13:00.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Confirm Edit Activity Event fields. | Date = 2026-09-15, Start Time = 13:00, End Time = 14:00, Status = Draft. | dropped_start = 2026-09-15 13:00 |
| 2 | Click Save. | Edit form closes and success toast is shown. | action = save |
| 3 | Inspect 2026-09-15 13:00 tile. | `Draft Workshop A` appears in the drop area with Draft styling. | expected_new_tile = 2026-09-15 13:00 |
| 4 | Inspect original 2026-09-14 10:00 tile. | `Draft Workshop A` no longer appears in original tile. | expected_original_tile = empty |

**Severity:** critical
**Priority:** high

---

### [Core] SF Calendar - Drag Draft Event - Cancel edit keeps original schedule

**Description:** AC 06 - Negative - Closing Edit Event UI after drag/drop does not persist the dropped time.

**Preconditions:**
- Logged in as HQ or CM Staff to Salesforce org.
- Draft Activity Event `Draft Workshop B` exists from 2026-09-14 15:00 to 16:00 JST.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Drag `Draft Workshop B` to 2026-09-15 09:00 tile. | Edit Activity Event UI opens with dropped time. | original = 2026-09-14 15:00; dropped = 2026-09-15 09:00 |
| 2 | Click Cancel or close the Edit Event UI. | Edit UI closes without success toast. | action = cancel |
| 3 | Refresh calendar. | `Draft Workshop B` remains at 2026-09-14 15:00 and is not shown at 2026-09-15 09:00. | expected_persisted = original |

**Severity:** major
**Priority:** high

---

### [Core] SF Calendar - Drag Published Event - Edit Event UI opens with dropped time

**Description:** AC 05/06 - Regression - Published single-day Activity Events remain draggable.

**Preconditions:**
- Logged in as HQ or CM Staff to Salesforce org.
- Published Activity Event `Published Workshop A` exists from 2026-09-14 11:00 to 12:00 JST.
- Calendar DnD feature is enabled.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open SF Lesson Calendar Weekly view and select Published status. | `Published Workshop A` is visible and draggable. | status = Published |
| 2 | Drag `Published Workshop A` to 2026-09-15 14:00 tile. | Edit Activity Event UI opens. | drop_tile = 2026-09-15 14:00 |
| 3 | Inspect date/time fields. | Date = 2026-09-15, Start Time = 14:00, End Time = 15:00; Status remains Published. | original_duration = 60 minutes |

**Severity:** critical
**Priority:** high

---

### [Core] SF Calendar - Drag Completed Event - Dragging is not allowed

**Description:** AC 05 - Negative - Completed Activity Events are not draggable.

**Preconditions:**
- Logged in as HQ or CM Staff to Salesforce org.
- Completed Activity Event `Completed Workshop A` exists from 2026-09-14 12:00 to 13:00 JST.
- Calendar DnD feature is enabled.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open SF Lesson Calendar Weekly view and select Completed status. | `Completed Workshop A` is visible. | status = Completed |
| 2 | Try to drag `Completed Workshop A` to another tile. | Card cannot be dragged and Edit Event UI does not open. | allowed_statuses = Draft, Published |
| 3 | Inspect the original tile. | `Completed Workshop A` remains in the original tile. | original = 2026-09-14 12:00 |

**Severity:** major
**Priority:** high

---

### [Core] SF Calendar - Drag Cancelled Event - Dragging is not allowed

**Description:** AC 05 - Negative - Cancelled Activity Events are not draggable.

**Preconditions:**
- Logged in as HQ or CM Staff to Salesforce org.
- Cancelled Activity Event `Cancelled Workshop A` exists from 2026-09-14 13:00 to 14:00 JST.
- Calendar DnD feature is enabled.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open SF Lesson Calendar Weekly view and select Cancelled status. | `Cancelled Workshop A` is visible. | status = Cancelled |
| 2 | Try to drag `Cancelled Workshop A` to another tile. | Card cannot be dragged and Edit Event UI does not open. | allowed_statuses = Draft, Published |
| 3 | Inspect original tile. | `Cancelled Workshop A` remains in the original tile. | original = 2026-09-14 13:00 |

**Severity:** major
**Priority:** high

---

### [Core] SF Calendar - Drag Multi-day Draft Event - Dragging is not allowed

**Description:** AC 05 - Negative - Multi-day Activity Events are not draggable even when status is Draft.

**Preconditions:**
- Logged in as HQ or CM Staff to Salesforce org.
- Multi-day Draft Activity Event `Draft Camp 2D1N` exists and is visible in weekly band.
- Calendar DnD feature is enabled.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open SF Lesson Calendar Weekly view and select Draft status. | `Draft Camp 2D1N` is visible as a multi-day band. | isMultipleDay = true |
| 2 | Try to drag `Draft Camp 2D1N` to another day. | Multi-day bar cannot be dragged and Edit Event UI does not open. | drag_allowed = false |
| 3 | Inspect the original week. | `Draft Camp 2D1N` remains on 2026-09-16 to 2026-09-17. | expected_range = unchanged |

**Severity:** major
**Priority:** high

---

### [Core] SF Calendar - Drag Draft Event in timeslot mode - Uses timeslot master start and end

**Description:** AC 06 - Boundary Value - Timeslot drop uses the target timeslot master start/end values.

**Preconditions:**
- Logged in as HQ or CM Staff to Salesforce org.
- Timeslot mode is enabled.
- Timeslot `Slot PM` exists with Start Time = 13:30 and End Time = 15:00.
- Draft Activity Event `Draft Workshop Timeslot` exists from 2026-09-14 10:00 to 11:00 JST.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open SF Lesson Calendar Weekly Timeslot view and select Draft status. | `Draft Workshop Timeslot` is visible and draggable. | timeslot_mode = on |
| 2 | Drag the event to 2026-09-16 `Slot PM`. | Edit Activity Event UI opens. | drop_slot = Slot PM |
| 3 | Inspect date/time fields. | Date = 2026-09-16, Start Time = 13:30, End Time = 15:00. | slot_start = 13:30; slot_end = 15:00 |

**Severity:** critical
**Priority:** high

---

### [Core] SF Calendar - Drag Draft Event in classroom view - Classroom changes to target classroom

**Description:** AC 06 - Data Integrity - Classroom value in Edit Event UI follows the target classroom tile.

**Preconditions:**
- Logged in as HQ or CM Staff to Salesforce org.
- Daily Classroom view is enabled.
- Draft Activity Event `Draft Classroom Event` exists in Classroom A from 2026-09-14 10:00 to 11:00 JST.
- Classroom B exists in Tokyo Center.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open SF Lesson Calendar Daily Classroom view for 2026-09-14 and select Draft status. | `Draft Classroom Event` appears under Classroom A. | original_classroom = Classroom A |
| 2 | Drag the event to Classroom B at 13:00. | Edit Activity Event UI opens. | target_classroom = Classroom B; dropped_time = 13:00 |
| 3 | Inspect Edit Event UI. | Date = 2026-09-14, Start Time = 13:00, End Time = 14:00, Classrooms contains Classroom B and no longer contains Classroom A. | expected_classrooms = Classroom B |

**Severity:** critical
**Priority:** high

---

### [Core] SF Calendar - Drag Draft Event to no-classroom row - Classroom is cleared

**Description:** AC 06 - Data Integrity - Dropping to the no-classroom row clears Activity Event classrooms.

**Preconditions:**
- Logged in as HQ or CM Staff to Salesforce org.
- Daily Classroom view is enabled.
- Draft Activity Event `Draft Classroom Event` exists in Classroom A.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open SF Lesson Calendar Daily Classroom view and select Draft status. | `Draft Classroom Event` appears under Classroom A. | original_classroom = Classroom A |
| 2 | Drag the event to the no-classroom row at 15:00. | Edit Activity Event UI opens. | target_classroom = none |
| 3 | Inspect Edit Event UI. | Classrooms field is empty; Date = selected date; Start Time = 15:00; End Time preserves original duration. | expected_classrooms = [] |

**Severity:** major
**Priority:** high

---

### [Core] Learner App Calendar - Draft Activity Event remains hidden

**Description:** AC 09 - Regression - SF Calendar visibility does not expose Draft Event to Learner app Calendar.

**Preconditions:**
- Logged in as a learner or parent user.
- Draft Activity Event `Draft Workshop A` is assigned/targeted to the learner and exists on 2026-09-14.
- Published Activity Event `Published Workshop A` is assigned/targeted to the learner on the same date.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Learner app Calendar for 2026-09-14. | Calendar date opens. | today = 2026-08-12; learner = Student A |
| 2 | Inspect event list or event dots for the date. | Published event is visible; Draft event is not visible. | expected_hidden = Draft Workshop A |
| 3 | Search or refresh the date. | Draft event remains hidden. | status = Draft |

**Severity:** critical
**Priority:** high

---

### [Core] Booking System - Draft Activity Event remains hidden

**Description:** AC 09 - Regression - Booking system only exposes Published Activity Events.

**Preconditions:**
- Event Master `Core Draft Calendar Event` is open to Booking System.
- Draft Activity Event `Draft Workshop A` and Published Activity Event `Published Workshop A` exist under the Event Master.
- Logged in as a target learner or parent user.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Booking System event list for the Event Master. | Booking event list loads. | today = 2026-08-12; Event Master open to booking = true |
| 2 | Inspect available activity schedules. | `Published Workshop A` is shown; `Draft Workshop A` is not shown. | published_status = visible; draft_status = hidden |
| 3 | Try direct access to Draft Activity Event booking detail if a URL is known. | Access is blocked or no booking detail is shown for Draft event. | activity_status = Draft |

**Severity:** critical
**Priority:** high

---

### [Core] Get Event API - Draft Activity Event excluded from public event response

**Description:** AC 09 - Regression - Public event response continues to return Published Activity Events only.

**Preconditions:**
- Public Get Event API access is configured.
- Event Master `Core Draft Calendar Event` has one Draft and one Published Activity Event in the request date range.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Call Get Event API for 2026-09-01 to 2026-09-30. | API returns event master data for matching published schedules. | start_date = 2026-09-01; end_date = 2026-09-30 |
| 2 | Inspect activity schedules in the response. | Published Activity Event is returned; Draft Activity Event is not returned. | statuses = Draft, Published |
| 3 | Confirm response status fields. | No schedule with status `draft` appears in the response. | forbidden_status = draft |

**Severity:** critical
**Priority:** high
