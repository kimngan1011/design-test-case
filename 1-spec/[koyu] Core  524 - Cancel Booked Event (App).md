# Koyu | Core | App - Cancel Booked Event

## Table of Contents

- [Overview](#overview)
- [Flow and Design](#flow-and-design)
- [Background & Objective](#background--objective)
  - [Background](#background)
  - [Objectives](#objectives)
- [User Experiences Target](#user-experiences-target)
  - [Student / Parent Experience](#student--parent-experience)
  - [Staff Experience](#staff-experience)
- [Technical & Data Design Requirements](#technical--data-design-requirements)
  - [Data Entities and Scope](#data-entities-and-scope)
    - [A - Timezone & Evaluation Rule](#a---timezone--evaluation-rule)
    - [B - Cancellation Deadline Evaluation Strategy](#b---cancellation-deadline-evaluation-strategy)
    - [C. Master Event – Cancellation Deadline (Hours)](#c-master-event--cancellation-deadline-hours)
    - [D. Event Master – Response Notification Setting](#d-event-master--response-notification-setting)
    - [E. Event Master – Cancellation Permission Settings](#e-event-master--cancellation-permission-settings)
    - [F. Participant – Cancellation Reason](#f-participant--cancellation-reason)
    - [G. Cancellation Reason Detail (optional)](#g-cancellation-reason-detail-optional)
    - [H. Cancellation Request Date](#h-cancellation-request-date)
  - [User Flow](#user-flow)
    - [Main Flow-01: Cancel Reservation (Cancel Now – Immediate Removal)](#main-flow-01-cancel-reservation-cancel-now--immediate-removal)
    - [Main Flow-02: Cancel Reservation (Cancel Request – No Removal)](#main-flow-02-cancel-reservation-cancel-request--no-removal)
    - [US01 Configure Cancellation Settings](#us01-configure-cancellation-settings)
    - [US02 – Learner App | Display Cancel Reservation Action](#us02--learner-app--display-cancel-reservation-action)
    - [US03: Cancel Event Booking (Cancel Now)](#us03-cancel-event-booking-cancel-now)
    - [US04 – Cancel Reservation (Cancel Request)](#us04--cancel-reservation-cancel-request)
    - [US05: Input Cancellation Reason](#us05-input-cancellation-reason)
    - [US06: Check Cancellation Status](#us06-check-cancellation-status)
    - [US07: Receive Cancellation Notifications](#us07-receive-cancellation-notifications)
    - [US08: Cancellation Status List](#us08-cancellation-status-list)
    - [US09: Handle Post-Cancellation Actions](#us09-handle-post-cancellation-actions)
    - [US010: Re-book After Cancellation](#us010-re-book-after-cancellation)
- [Localization & Messaging (EN / JP)](#localization--messaging-en--jp)
- [Cross-Platform Impact Matrix](#cross-platform-impact-matrix)
- [Out of Scope](#out-of-scope)

---

## Document Info

| Item | Value |
|------|-------|
| Target release | 2026 Q1 (UAT starts from April) |
| Document status | IN PROGRESS |
| Document owner | @Maria Nawatani @Angelica Pitogo Abu |
| PBT Ticket | [PBT-1697: \[koyu\] Core \| 524 - Cancel Booked Event (App)](https://manabie.atlassian.net/browse/PBT-1697) READY FOR DEVELOPMENT |
| Client | CORE KOYU |
| Require Config? | No |
| LT Ticket | TBC |
| Designer | @Hai Doan |
| Engineer | TBC |
| QA | TBC |

---

## Overview

This project aims to improve the Cancel Booked Event (Reservation) on the learner app. The primary goal is to provide a more flexible and robust cancellation flow that accommodates both Paid and Free Events, while ensuring proper record-keeping and timely staff notifications.

---

## Flow and Design

- Wireframe: Koyu - Event
- Official Figma: [Eng] Event Management

---

## Background & Objective

### Background

Currently, Manabie's student app has an event booking cancellation feature, but it is rarely used. As a result, when students or parents want to cancel their event participation, the following challenges occur:

**Student/Parent Challenges:**
- Need to contact by phone or in-person, only available during business hours
- Difficult to respond quickly to sudden schedule changes
- High psychological barrier due to need to verbally explain cancellation reasons

**Staff Challenges:**
- Time consumed handling cancellations via phone or counter
- Risk of errors or omissions due to manual input of cancellation information
- Difficulty in centralized cancellation status management

### Objectives

This feature enhancement will solve the following business challenges:

1. **Improve Student/Parent Convenience:** Enable easy cancellation anytime through the app
2. **Improve Staff Operational Efficiency:** Reduce burden of phone responses and manual input
3. **Improve Cancellation Management Transparency:** Enable centralized management of all cancellation information in the system for appropriate responses
4. **Flexible Operations:** Allow selection of immediate cancellation or approval-based cancellation according to each school's operational policy

**Why This Feature is Needed:**
- **Improve Customer Satisfaction:** Service experience improves as students/parents can process cancellations at their own pace
- **Operational Efficiency:** Staff can spend time on what they should focus on - student guidance and lesson preparation
- **Data-Driven Operations:** Service improvements can be made by analyzing cancellation reasons and patterns

---

## User Experiences Target

1. **24/7 Cancellation Availability**
   Students and parents can cancel event bookings anytime through the app, eliminating the need to wait for business hours or make phone calls.

2. **Reduced Psychological Barriers**
   App-based cancellation removes the discomfort of verbally explaining reasons to staff, making the process more accessible.

3. **Immediate Processing and Confirmation**
   Cancellation operations are reflected immediately in the system, and users can confirm their cancellation status on the calendar screen.

4. **Flexible Cancellation Management**
   School managers can choose between immediate cancellation or approval-based cancellation according to their operational policies and event types.

5. **Efficient Staff Response**
   Staff receive instant notifications when cancellations occur, allowing them to quickly implement follow-up actions (alternative lesson guidance, seat management, etc.).

6. **Centralized Cancellation Visibility**
   Event participant lists clearly display cancellation statuses, making event preparation (attendance adjustment, material preparation) more efficient.

7. **Reduced Administrative Work**
   Phone response time for cancellations is reduced, and manual data entry is eliminated as student-entered information is automatically reflected in the system.

8. **Data-Driven Service Improvement**
   Cancellation reasons can be collected and analyzed to identify patterns and improve services.

### Student / Parent Experience

Cancellation must feel:
- simple
- explicit
- final (especially for Cancel Now)

Required inputs must be clearly communicated:
- mandatory cancellation reason
- conditional "Other" detail field

Users must always understand:
- whether cancellation is allowed
- why it is not allowed (if disabled)

**Key UX Rules:**

- **Cancel Reservation button:**
  - Visible but disabled when cancellation is not allowed
  - Tooltip explains the reason (deadline passed or permission restricted)

- **Confirmation modal:**
  - Clearly indicates required fields
  - Blocks submission until all validations pass

- **Status visibility:**
  - Users can always see the final status on the calendar
  - Event is never silently removed from the calendar view

### Staff Experience

Staff should:
- Immediately see updated participant status
- Clearly distinguish between:
  - Canceled
  - Cancel Requested
- Cancellation reason and detail must be visible in participant details

Participant removal for Cancel Now should:
- Reflect immediately in participant list
- Update capacity without manual refresh (where technically feasible)

---

## Technical & Data Design Requirements

### Data Entities and Scope

| Entity | Type | Notes |
|--------|------|-------|
| Master Event | Master | Stores who is allowed to cancel, cancellation type and notification settings |
| Event Participant | Transaction | Stores response status and cancellation reason |

> **NOTE:** Turn on field tracking to all new fields that will be seen on the UI. For tech/internal fields, technical team can decide.

### A - Timezone & Evaluation Rule

- All cancellation deadline evaluations must be based on the Event's timezone.
- User device timezone and locale must not affect eligibility.

### B - Cancellation Deadline Evaluation Strategy

**Requirement:**
Cancellation eligibility must be evaluated dynamically at the time the user attempts to cancel.

**Recommended Approach:**
Calculate the cancellation cutoff datetime on the fly, not at Activity creation.

> To Tech: Check any potential challenge on concurrency and performance.

**Rationale:**
- Event start time may change after booking
- Activity may inherit updated Event settings
- Avoids stale precomputed values
- Reduces backfill and sync complexity

**Evaluation Logic (Conceptual):**

```
Cancellation Cutoff Datetime = Event Start Datetime – Cancellation Deadline (hours)
```

Current time is evaluated in Event timezone.

### C. Master Event – Cancellation Deadline (Hours)

| Attribute | Value |
|-----------|-------|
| Field Label | Cancellation Deadline (Hours) |
| API Name | Cancellation_Deadline_Hours__c (TBC) |
| Object | Master Event |
| Type | Number |
| Format | Integer (no decimals) |
| Min / Max | 0 to 4 digits |
| Default | 0 |
| Required | No |
| Unit | Hours before Event Start Datetime |
| Timezone Rule | Always evaluated using Event timezone |

### D. Event Master – Response Notification Setting

| Attribute | Value |
|-----------|-------|
| Field Label | Response Notification Setting |
| API Name | Response_Notification_Setting__c |
| Object | Master Event |
| Type | Picklist |
| Values | none, Cancel → In the future, Attend and Absent will be added |
| Default | None |
| Required | No |
| Behavior | Controls whether staff receive Salesforce in-app (bell) notifications |
| Notes | Admin/manual updates and imports do not trigger notifications regardless of this setting |

### E. Event Master – Cancellation Permission Settings

**Allow Cancellation (Directly Added Participants):**

| Attribute | Value |
|-----------|-------|
| Field Label | Allow Cancellation (Directly Added Participants) |
| API Name | Allow_Cancel_Direct__c |
| Type | Checkbox |
| Default | False |
| Description | Controls whether participants added manually by staff can cancel |

**Allow Cancellation (Booking System Participants):**

| Attribute | Value |
|-----------|-------|
| Field Label | Allow Cancellation (Booking System Participants) |
| API Name | Allow_Cancel_Booked__c |
| Type | Checkbox |
| Default | True |
| Description | Controls whether participants who booked via booking system (UI or API) can cancel |

**Behavior Rules:**
Cancellation eligibility is determined by:
- a. Participant source (Direct vs Booked)
- b. Corresponding allow-cancel flag
- c. Cancellation deadline

### F. Participant – Cancellation Reason

**Cancellation Reason (Pre-defined):**

| Attribute | Value |
|-----------|-------|
| Field Label | Cancellation Reason |
| API Name | Cancellation_Reason__c (TBC) |
| Type | Picklist |
| Required | No (conditional) |
| Description | When cancelling, user must select one predefined reason |

**Suggested Picklist Values:**
- Schedule conflict
- Not feeling well / Health reason
- School event / Exam
- Family reason
- Transportation issue
- Forgot / Mistaken booking
- No longer interested
- Other

### G. Cancellation Reason Detail (optional)

Use the existing `MANAERP__Response_Note__c` field.

| Attribute | Value |
|-----------|-------|
| Field Label | MANAERP__Response_Note__c |
| Type | Text Area (255) |
| Required | No (conditional) |
| Description | [Existing] "Response Note" field is used when, on an activity event, we check "Propose new time." [New - in addition] Use the field for cancellation reason - details. Required if "Others" is selected from the Cancellation Reason. |

### H. Cancellation Request Date

| Attribute | Value |
|-----------|-------|
| Field Label | Cancellation Request Date |
| API Name | Cancellation_Request_Date__c (TBC) |
| Type | Date |
| Required | No (conditional) |
| Description | DateTime stamp when the Cancellation Request was received |

---

## User Flow

### Main Flow-01: Cancel Reservation (Cancel Now – Immediate Removal)

**Actor:** Student / Parent

**Preconditions:**
- Cancel Type = Cancel
- Participant source is allowed to cancel (Direct or Booked)
- Current time (Event timezone) is before cancellation cutoff
- Response status is not already Canceled or Cancel Requested

**Trigger:** User taps "Cancel Reservation" from the learner's mobile app

**Steps:**
1. System displays cancellation confirmation modal
2. User selects a mandatory cancellation reason
   - a. If "Other" is selected, user enters reason detail (required)
3. User confirms cancellation
   - a. Success message
4. System sets Response Status = "Canceled"
5. System REMOVES participant from participant list
6. System saves cancellation reason data
7. System updates SF Activity Event, SF Calendar and capacity

**Expected Result:**
- Participant no longer appears in participant list
- Event capacity is updated immediately
- Event card is still shown on the Calendar student/parent calendar as "Cancelled"

### Main Flow-02: Cancel Reservation (Cancel Request – No Removal)

Same as Main Flow-01 | Steps 1-4, Step 6, Step 7

**Step 5:** System KEEPS participant in participant list

**Differences from MF-01:**
- Participant remains in participant list
- Response Status = "Cancel Requested"

---

## User Stories Summary

| ID | Feature | User Story |
|----|---------|------------|
| US01 | Configure Cancellation Settings | As a school manager or branch manager, I want to set cancellation policies - who can cancel, cancellation type and cancellation deadline per event, so that I can conduct flexible management according to my school's operational policy and event nature. |
| US02 | Cancel Event Booking | As a student or parent, I want to easily cancel a registered event from the app, so that I can respond quickly even outside business hours when a sudden schedule change occurs. |
| US03 | Cancel Event Booking (Cancel Now) | As a student or parent, I want to directly cancel the event when possible. |
| US04 | Cancel Event Booking (Cancellation Request) | As a student or parent, I want to request for cancellation to be able to get refunds when possible. |
| US05 | Input Cancellation Reason | As a student or parent, I want to briefly communicate my cancellation reason, so that staff can understand my situation and provide appropriate support. |
| US06 | Check Cancellation Status | As a student or parent, I want to check the status of my canceled event in the app, so that I can have peace of mind that my cancellation was processed correctly. |
| US07 | Receive Cancellation Notifications | As a staff responsible for the event, I want to quickly receive notifications when students cancel, so that I can grasp cancellation status and quickly implement necessary responses (alternative lesson guidance, follow-up, etc.). |
| US08 | View Cancellation Status List | As admin/CM/staff, I want to check cancellation status at a glance in the event participant list, so that I can appropriately prepare for event operations (attendance adjustment, material preparation, etc.). |
| US09 | Handle Post-Cancellation Actions | As staff, I want to conduct student follow-up and refund processing based on cancellation information, so that I can maintain student satisfaction and continue appropriate service provision. |
| US10 | Re-book After Cancellation | As a student/parent, I want to be able to join again after cancelling in case my schedule becomes free. |

---

## US01 Configure Cancellation Settings

As a school manager or branch manager, I want to set cancellation policies - who can cancel, cancellation type and cancellation deadline per event, so that I can conduct flexible management according to my school's operational policy and event nature.

### AC 01.1 – Allow Cancellation Settings

**Cancellation Settings Section – Add Allow Cancellation for Directly Added Participants and Allow Cancellation for Booking System Participants:**

- **Allow Cancellation for Directly Added Participants:**
  - When selected, allows participants added through Salesforce "Assign To Event" to cancel
  - Enable/Disable the "Cancel Reservation" on the mobile app for the direct participant.

- **Allow Cancellation for Booking System Participants:**
  - When selected, allows participants added through the external booking link to cancel
  - Enable/Disable the "Cancel Reservation" on the mobile app for the booking participant.

- Both options are un-selected by default

### AC 01.1 – Control of the Cancel Button in mobile app

**Mobile's Cancel Button (visibility control):**

- Cancellation Type is Cancel or Cancel Request
- Event Activity Date/Time is in the future
- The existing Cancel Config is no longer controls the visibility of the Cancel button.
- For partners with Cancel Config = On, then migrate all existing events to Cancel Type = Cancel.
- For partners with Cancel Config = Off, then migrate all existing events to Cancel Type = Do not allow.

### AC 01.2 – Cancellation Type

**Cancellation Settings Section – Add a Cancellation Type:**

- Enabled by default
- When one or both of the checkboxes from **ALLOW CANCELLATION...** is selected, then enable and require the Cancellation Type

**Cancellation Type options:**
- Do not allow → Hides cancel button from mobile; Other cancel related fields are disabled
- Cancel
- Cancellation Request
- Single select only

### AC 01.3 – Cancellation Deadline

**Cancellation Settings Section – Add Cancellation Deadline:**

- Disabled by default
- When Cancellation Type is Cancel or Cancel Request, then enable Cancellation Deadline fields
- Specifies the number of hours until cancellation is accepted

**Example:**
- Event Date = Feb 1, 2026 8:00 am
- Cancellation Deadline = 24 hrs
- Actual Cancellation Deadline Date = Feb 2, 2026 8am; students/parents can cancel before this date.

- If cancellation deadline is 0 or null, then it means that cancellation deadline is the same as the event date

**[Case: Update Cancellation Deadline]**
- When the user updates the Cancellation Deadline & the event has already started (current date >= any of the activity event date):
  - Then display a message: "This event is already in progress. Changes to the cancellation deadline will only apply to activities that have not yet started."
  - Confirm: Recompute for the cancellation deadline of each activity
  - Cancel: Close the popup message
- Else: No message is needed; Recompute the cancellation deadline

### AC 01.4 – Reminders and Notification Settings

**Reminders and Notification Section – Add Response Notification, Move Reminders:**

- Reminder (existing; just move inside this section)
- Response Notification (new)
  - Add a new field "Response Notification"
  - Options available are the possible responses:
    - none (default)
    - Cancel → Applies to both Cancel and Cancellation Request
  - Tooltip: "Send a Salesforce notification when the mobile app user submits a response."

> **Note:** In case a Cancel Notification is set up yet the cancellation settings are not, it's expected that no notification will be triggered since the Cancel Button is not visible.

### AC 01.5 – Booking Information (Read-only)

**Open to Booking:**
- Who can Reserve and Cancel
- Reservation Deadline (hours)
- Cancellation policy
- Create application
- Booking Period
- Booking Start Date
  - Controls when the event can be available for booking.
  - When the current date < booking start date, then:
    - Show a message on the mobile app and web app: "This event will be available for booking from \<Start Date\>"
    - Disable the Reserve button
- End Date (previously expiration date) – No logic change
- Open to Booking

### AC 01.6 – Updated Event Master View

Update the Event Master - View to reflect new sections and fields:
- Cancellation Settings
- Reminders & Notifications
- Booking Settings

---

## US02 – Learner App | Display Cancel Reservation Action

As a student or parent, I want to easily cancel a registered event from the app, so that I can respond quickly even outside business hours when a sudden schedule change occurs.

### AC 02.1 – Display Cancel Reservation button (Eligible Case)

**Given:** A Student or Parent is viewing the details of an event they have booked

**When:**
- Cancel Type is Cancel or Cancellation Request
- Current Date > the calculated actual cancellation deadline and Event Date
- The participant's current Response Status is not `Canceled` and not `Cancellation Request`
- Then participant is allowed to cancel based on participant source:
  - Participant Source = Direct (added manually in SF) AND Allow_Cancel_Direct__c = true or Allow_Cancel_Booking__c = true
  - OR Participant Source = Booked (from Booking Link) AND Allow_Cancel_Booked__c = true or Allow_Cancel_Booking__c = true

**Then:** The Cancel Reservation button is visible and enabled

### AC 02.1 – Display Cancel Reservation button (Deadline is empty or 0)

**Given:** A Student or Parent is viewing the details of an event they have booked

**When:** Eligible for cancellation

**Then:** Hide the Cancellation Deadline section

### AC 02.2 – Cancel Reservation button Disabled (Deadline Expired)

**Given:** A Student or Parent is viewing the event details screen; Participants are allowed to cancel

**When** any of the following conditions are true:
- Cancellation deadline is expired
- Event is in the past

**Then:** The Cancel Reservation button is disabled

### AC 02.3 – Cancel Reservation button Hidden (Ineligible Case)

**Given:** A Student or Parent is viewing the event details screen

**When** any of the following conditions are true:
- The participant is not allowed to cancel based on participant source and settings

**Then:** The Cancel Reservation button is hidden

---

## US03: Cancel Event Booking (Cancel Now)

As a student or parent, I want to cancel an event when possible.

### AC 03.1 – Display Cancellation Confirmation Modal

**Given:** The Cancel Reservation button is enabled

**When:** The user taps Cancel Reservation

**Then:** A Cancel Reservation modal is displayed containing:
- EN: "Are you sure you want to cancel your reservation to this event?"
- Event Activity name
- Event Activity date and time
- Cancellation reason and detail (if Others is selected as cancellation reason)
- Cancellation Deadline Date

### AC 03.2 – Mandatory Cancellation Reason Selection

**When:** The cancellation confirmation modal is displayed

**Then:**
- Require the user to select one Cancellation Reason
- Options:
  - Schedule conflict
  - Not feeling well / Health reason
  - School event / Exam
  - Family reason
  - Transportation issue
  - Forgot / Mistaken booking
  - No longer interested
  - Other → Requires the Cancellation Reason Details. Append "Cancel Reason: \<user reason here\>" (Ex. Cancel Reason: I will take this in another location.)
- The Confirm Cancellation button is disabled until the Cancellation Reason is provided

### AC 03.3 – "Other" Reason Requires Detail

**Given:** The user selects Other as the cancellation reason

**When:** The Cancellation Reason Detail field is empty

**Then:** The Confirm Cancellation button is disabled

### AC 03.4 – Execute Cancel (Immediate Cancellation)

**Given:**
- Cancellation mode is Cancel
- All validation requirements are satisfied

**When:** The user taps Confirm Cancellation

**Then:** The system:
- Updates Response Status to `Canceled`
- Saves the selected Cancellation Reason
- Saves the Cancellation Reason Detail if provided
- Removes the participant from the participant list
- Updates event capacity immediately
- The user is returned to the calendar screen
- A success confirmation message is displayed:
  - EN: "Your reservation to this event is cancelled"
  - JP: イベントの予約がキャンセルされました
- The event card on the calendar reflects the `Canceled` status

---

## US04 – Cancel Reservation (Cancel Request)

As a student or parent, I want to request for cancellation to be able to get refunds when possible.

### AC 04.1 – Display Cancellation Confirmation Modal

**Given:** The Cancel Reservation button is enabled

**When:** The user taps Cancel Reservation

**Then:** A confirmation modal is displayed containing:
- EN: "Are you sure you want to send cancellation request for this event?"
- JP: キャンセルリクエストが送信されました
- Event Activity name
- Event Activity date and time
- Cancellation reason

### AC 04.2 – Execute Cancel Request (Approval-Based Cancellation)

**Given:**
- Cancellation mode is Cancel Request
- All validation requirements are satisfied

**When:** The user taps Confirm Cancellation

**Then:** The system:
- Updates Response Status to `Cancel Requested`
- Saves the selected Cancellation Reason
- Saves the Cancellation Reason Detail if provided
- Does NOT remove the participant from the participant list
- The user is returned to the calendar screen
- A message indicating the request has been submitted is displayed:
  - EN: "Your cancellation request has been submitted."
  - JP: キャンセルリクエストが送信されました
- No system-level approval or rejection actions are provided
- Store the `Cancellation Request Date` which is the time the user sends the cancellation request.

---

## US05: Input Cancellation Reason

As a student or parent, I want to briefly communicate my cancellation reason, so that staff can understand my situation and provide appropriate support.

### AC 05.1 – Cancellation Reason Options

**Given:** The cancellation confirmation modal is displayed

**When:** The user views the Cancellation Reason field

**Then:** The following predefined options are available:
- Schedule conflict
- Health reason
- School event / exam
- Family reason
- Transportation issue
- Mistaken booking
- No longer interested
- Other

### AC 05.2 – Cancellation Reason Detail Constraints

**Given:** The Cancellation Reason Detail field is displayed

**When:** The user enters text

**Then:**
- The maximum allowed length is 255 characters
- A character counter is displayed
- If the limit is exceeded, an inline error message is shown

---

## US06: Check Cancellation Status

As a student or parent, I want to check the status of my canceled event in the app, so that I can have peace of mind that my cancellation was processed correctly.

### AC 06.1 – Display Cancellation Status on Calendar

**Given:** A user has canceled an event or submitted a cancel request

**When:** The user views their calendar

**Then:**
- The event remains visible on the calendar
- The event card displays:
  - Status text: `Canceled` or `Cancel Requested`
  - A visual indicator (color, icon, or label)
- The user can still tap the event to view details

---

## US07: Receive Cancellation Notifications

As a staff responsible for the event, I want to quickly receive notifications when students cancel, so that I can grasp cancellation status and quickly implement necessary responses (alternative lesson guidance, follow-up, etc.).

### AC 07.1 – Send In-App Notification to Staff

**Given:** A Student or Parent completes a Cancel Now or Cancel Request action via the mobile app

**When:** The cancellation is processed

**Then:**
- The system should send a notification to staff via Salesforce in-app notification (bell notification)
- Notification recipients are determined by the master event's Master Participant - Master Staff List.
- Notification content should include:
  - Student name
  - Event Activity name
  - Cancellation type (Cancel or Cancellation Request)
  - Cancellation reason and details (if provided)
- Notification timing: Immediately after cancellation is processed
- Notification recipients: Event Staff

---

## US08: Cancellation Status List

As staff, I want to check cancellation status at a glance in the event participant list, so that I can appropriately prepare for event operations (attendance adjustment, material preparation, etc.).

### AC 08.1 – [View] Display Response in Event Participant List

**Given:** Staff is viewing all the event participant list

**When:** They view the list

**Then:**
- Each participant's Response should be displayed with one of the following values:
  - Attend: Planning to attend (previously Accept)
  - Absent: Planning to be absent (previously Declined)
  - Canceled: Canceled
  - Cancel Requested: Cancel request submitted
- Response should be displayed in a dedicated column
- Show the "Requested Date" which is the date and time the cancellation was requested.

### AC 08.2 – [View] Display Cancellation Reason in Event Participant List

**Given:** Staff views the details of a participant who canceled or requested cancellation

**When:** The participant detail view is displayed

**Then:**
- The selected `Cancellation Reason` is shown
- The `Cancellation Reason Detail` is shown if provided

### AC 08.3 – [Edit] Participants Cancellation Reason

**Given:** Staff views the details of a participant who canceled or requested cancellation

**When:** The user edits the participant details

**Then:** Show the new set of Response selections (Attend, Absent, Cancel, Cancel Request), Cancellation Reason and Cancellation Reason Details

### AC 08.3 – [Filter] Participant Response

**When:** The user clicks Event Participant - View All, Opened the Filter

**Then:** Show the new set of Response options on the filter

---

## US09: Handle Post-Cancellation Actions

As staff, I want to conduct student follow-up and refund processing based on cancellation information, so that I can maintain student satisfaction and continue appropriate service provision.

### AC 09.1 – Manual Staff Actions After Cancellation

**Given:** Staff receives a cancellation notification

**When:** They view the event participant list

**Then:** Staff should be able to manually perform the following actions:
- Remove the participant from the event (affects capacity)
- Set participant as absent
- Process refunds (if applicable)
- Contact student/parent for follow-up

> These actions are manual and not automated. No system-level approval/rejection workflow is provided. Staff determines appropriate actions based on school policy.

---

## US010: Re-book After Cancellation

As a student/parent, I want to be able to join again after cancelling in case my schedule becomes free.

### AC 10.1 – Allow Re-booking After Cancellation

**Given:**
- A student has canceled an event and already removed from the participant list either automatically or manually
- The event has available capacity

**When:** The student attempts to book the same event again

**Then:**
- The booking is allowed
- The previous cancellation record remains retained for audit purposes
- New/Rebooked record - cancellation response, cancellation reason, cancellation reason details are blank again
- Previous booking record - cancellation response, cancellation reason, cancellation reason details are retained for historical checking (native SF field tracking)

---

## Localization & Messaging (EN / JP)

| # | Section | English (EN) | Japanese (JP) | Description |
|---|---------|-------------|---------------|-------------|
| 1 | Master Event | Cancellation Setting | キャンセル設定 | Section title |
| 2 | Master Event | Cancellation Type | キャンセルタイプ | Picklist value: notifications sent only for Cancel Request actions. |
| 3 | Master Event | Cancellation Deadline | キャンセル締切時間 | Cancellation deadline in hours |
| 4 | Master Event | This event is already in progress. Changes to the cancellation deadline will only apply to activities that have not yet started. | 進行中のイベントです。新しいキャンセル締切時間はまだ開始していないアクティビティイベントにのみ適用されます。 | Message when the user tries to update the cancellation deadline for an ongoing event (at least 1 activity is on the current date or in the past). |
| 5 | Master Event | Reminders and Notification Settings | リマインダーと通知の設定 | Section title |
| 6 | Master Event | Response Notification | キャンセル通知設定 | Selection of responses that will trigger SF notifications |
| 7 | Master Event | Send a Salesforce notification when the mobile app user submits a response | 参加者がアプリで返信した際にSalesfoceで通知する | Tooltip message for Response Notification |
| 8 | Participant / Transaction | Cancellation Reason | キャンセル理由 | Required picklist. User must select one predefined cancellation reason when cancelling. |
| 9 | Participant / Transaction | Cancellation Reason Detail | キャンセル理由詳細 | Text Area (255). Required only when "Other" is selected as Cancellation Reason. |
| 10 | Cancellation Reason – Picklist | Schedule conflict | 予定があわなくなった | Predefined cancellation reason |
| 11 | Cancellation Reason – Picklist | Not feeling well / Health reason | 体調不良 | Predefined cancellation reason (education / juku scope). |
| 12 | Cancellation Reason – Picklist | School event / Exam | 学校行事 | Predefined cancellation reason. |
| 13 | Cancellation Reason – Picklist | Family reason | 家庭の理由 | Predefined cancellation reason. |
| 14 | Cancellation Reason – Picklist | Transportation issue | 交通機関 | Predefined cancellation reason. |
| 15 | Cancellation Reason – Picklist | Forgot / Mistaken booking | 忘れた/予約ミス | Predefined cancellation reason. |
| 16 | Cancellation Reason – Picklist | No longer interested | 興味がなくなった | Predefined cancellation reason. |
| 17 | Cancellation Reason – Picklist | Other | その他 | Requires Cancellation Reason Detail input. |
| 18 | Mobile App – Message | This event will be available for booking from \<Booking Start Date\> | このイベントは\<booking start date\>以降予約可能になります | Message when the booking link is accessed and event is not yet ready to accept reservations. |
| 19 | Mobile App – Buttons & Labels | Cancel Reservation | 予約をキャンセルする | Primary action button shown on Event Activity detail when cancellation is eligible. |
| 20 | Mobile App – Modal | [Button] Cancel | キャンセル内容の確認 | Confirmation CTA after entering cancellation details. |
| 21 | Mobile App – Modal | Cancellation Reason | キャンセル理由 | Label for required cancellation reason selection field. |
| 22 | Mobile App – Modal | [Button] Request Cancellation | キャンセルを希望する | — |
| 23 | Mobile App – Modal | Cancellation Deadline | キャンセル締切時間 | Actual date of cancellation calculated from the Event Master.Cancellation Deadline (hours) |
| 24 | Mobile App – Confirmation | Your reservation to this event is cancelled | イベントの予約がキャンセルされました | Success message for Cancel Now (immediate cancellation). |
| 25 | Mobile App – Confirmation | Your cancellation request has been submitted | キャンセルリクエストが送信されました | Success message for Cancel Request submission. |
| 26 | Mobile App – Confirmation | Are you sure you want to send cancellation request for this event? | イベントのキャンセルリクエストを送信してもよろしいですか？ | Confirmation message for Cancel Request |
| 27 | Mobile App – Confirmation | Are you sure you want to cancel this event? | イベントをキャンセルしてもよろしいですか？ | Confirmation message for Cancel |
| 28 | Calendar / Status Display | Cancel Requested | キャンセルリクエストが送信されました | Response Status displayed when cancellation requires staff handling. |
| 29 | Notifications (Staff) | Cancellation notification (in-app) | キャンセル通知（アプリから） | Salesforce bell notification triggered by mobile-initiated cancellation actions, subject to Cancel Notification Setting. |
| 30 | Notifications – Content | Event Activity name | アクティビティイベント名 | Included in staff notification payload. |
| 31 | Notifications – Content | Cancellation type | キャンセルタイプ | Indicates Cancel or Cancel Request. |

---

## Cross-Platform Impact Matrix

| Area | Salesforce Core | Mobile App |
|------|----------------|------------|
| Cancellation permission logic | ✔ | ✔ |
| Deadline evaluation | ✔ | ✔ |
| Cancellation reason capture | ✔ | ✔ |
| Participant removal (Cancel Now) | ✔ | — |
| Calendar status display | ✔ | ✔ |
| Staff notifications | ✔ | — |
| Localization | ✔ | ✔ |
| Audit tracking | ✔ | ✔ |

---

## Out of Scope

The following features are not included in this scope and are considerations for the future:

### 1. Automatic Processing After Cancellation
- Automatic capacity update (mechanism to automatically increase available slots after cancellation)
- Automatic notification to waitlisted students

### 2. Cancel Request Approval/Rejection Feature
- System-level approval/rejection buttons
- Automated approval workflow
- Approval history tracking

### 3. Integration with Refund Processing
- Automatic refund processing
- Link to refund procedures
- Display of refund eligibility information at cancellation
- Cancellation fee calculation

### 4. Advanced Notification Features
- Email/SMS notification to students
- Individual notification to parents
- Customizable notification templates
- Notification scheduling

### 5. Analysis/Report Features
- Cancellation statistics reports
- Cancellation reason analysis dashboard
- Trend analysis and predictive analytics
- Export functionality for cancellation data

### 6. Batch Operations
- Batch cancellation of multiple events
- Bulk cancellation processing by staff
- Import/export of cancellation data

### 7. Confirmation Modal Detail Information
- Display of event name, date/time, cancellation policy in confirmation modal
- Cancellation policy enforcement
- Cancellation deadline warnings

### 8. Advanced Cancellation Features
- Partial cancellation (cancel only certain sessions in a series)
- Temporary hold instead of cancellation
- Cancellation undo functionality
- Waitlist management integration