# Test Cases: LT-102395 - [Renseikai] Core: Event Attendance to be the same as Lesson

## Suite: Event Attendance Response Flow (Qase Suite ID: 2617)

### [Renseikai] Event Attendance - Setting ON (Student + Parent) - Student submits response as Attend

**Description:** Verify that when the event allows both student and parent responses, a student can submit attendance response in advance from Learner App with status **Attend**.

**Preconditions:**
- Event E1 exists, published, and visible in Learner App for Student A
- Event setting "Allow attendance response" is enabled
- Event setting "Responders" includes both Student and Parent
- Student A and Parent A are linked correctly
- Student A has not submitted a response for Event E1 yet

| #   | Action | Expected Result | Test Data |
| --- | ------ | --------------- | --------- |
| 1   | Open Learner App as Student A and navigate to Event E1 detail | Event detail screen is displayed with attendance response action available | Event E1 |
| 2   | Tap attendance response action | Response form opens with lesson-like options | Student A |
| 3   | Select status = Attend and tap Submit | Submission succeeds and success feedback is shown | Status: Attend |
| 4   | Re-open Event E1 detail | Submitted response is shown as Attend | Event E1 |

**Severity:** critical
**Priority:** high

---

### [Renseikai] Event Attendance - Setting ON (Student + Parent) - Parent submits response as Absent

**Description:** Verify parent can submit response when parent is allowed by event settings.

**Preconditions:**
- Event E2 exists and allows attendance response from both Student and Parent
- Parent B is linked to Student B who is assigned to Event E2
- No prior response submitted by Parent B for Event E2

| #   | Action | Expected Result | Test Data |
| --- | ------ | --------------- | --------- |
| 1   | Open Parent App as Parent B and go to Event E2 detail | Event detail is displayed and attendance response action is visible | Event E2 |
| 2   | Tap attendance response action | Response form opens | Parent B |
| 3   | Select status = Absent and submit | Submission succeeds | Status: Absent |
| 4   | Re-open Event E2 detail | Submitted response is shown as Absent | Event E2 |

**Severity:** critical
**Priority:** high

---

### [Renseikai] Event Attendance - Status Options - All lesson-like statuses are available

**Description:** Verify event response form provides the same attendance statuses as lesson flow (Attend, Absent, Late, Leave Early).

**Preconditions:**
- Event E3 allows attendance response
- Student C can access Event E3 in Learner App

| #   | Action | Expected Result | Test Data |
| --- | ------ | --------------- | --------- |
| 1   | Open Event E3 detail and tap attendance response action | Response form opens | Event E3 |
| 2   | Observe status options list | Options include Attend, Absent, Late, Leave Early | Student C |

**Severity:** critical
**Priority:** high

---

### [Renseikai] Event Attendance - Student only setting - Parent cannot submit

**Description:** Verify parent cannot submit response when event responder scope is Student only.

**Preconditions:**
- Event E4 allows attendance response
- Event E4 responder scope = Student only
- Parent D is linked to Student D assigned to Event E4

| #   | Action | Expected Result | Test Data |
| --- | ------ | --------------- | --------- |
| 1   | Open Parent App as Parent D and navigate to Event E4 | Event detail is displayed | Event E4 |
| 2   | Observe event actions | Attendance response action is hidden or disabled for Parent D | Parent D |

**Severity:** major
**Priority:** high

---

### [Renseikai] Event Attendance - Parent only setting - Student cannot submit

**Description:** Verify student cannot submit response when event responder scope is Parent only.

**Preconditions:**
- Event E5 allows attendance response
- Event E5 responder scope = Parent only
- Student E is assigned to Event E5

| #   | Action | Expected Result | Test Data |
| --- | ------ | --------------- | --------- |
| 1   | Open Learner App as Student E and navigate to Event E5 detail | Event detail is displayed | Event E5 |
| 2   | Observe event actions | Attendance response action is hidden or disabled for Student E | Student E |

**Severity:** major
**Priority:** high

---

### [Renseikai] Event Attendance - Event response setting OFF - No response action for all users

**Description:** Verify no response submission is possible when event attendance response feature is disabled for the event.

**Preconditions:**
- Event E6 exists
- Event E6 attendance response setting is OFF
- Student F and Parent F can both open Event E6 detail

| #   | Action | Expected Result | Test Data |
| --- | ------ | --------------- | --------- |
| 1   | Open Event E6 detail as Student F | Attendance response action is not available | Event E6 |
| 2   | Open Event E6 detail as Parent F | Attendance response action is not available | Event E6 |

**Severity:** major
**Priority:** high

---

### [Renseikai] Event Attendance - Resubmission flow - User can update previously submitted response

**Description:** Verify user can edit and resubmit attendance response before event starts.

**Preconditions:**
- Event E7 allows attendance response for Student G
- Student G already submitted status = Attend for Event E7
- Event E7 has not started yet

| #   | Action | Expected Result | Test Data |
| --- | ------ | --------------- | --------- |
| 1   | Open Event E7 detail as Student G | Existing response is shown as Attend | Event E7 |
| 2   | Open attendance response form again | Current selected status is Attend | Student G |
| 3   | Change status to Late and submit | Submission succeeds | New status: Late |
| 4   | Re-open Event E7 detail | Response is updated to Late | Event E7 |

**Severity:** major
**Priority:** medium

---

### [Renseikai] Event Attendance - Notification - Event staff and CM receive notification on submission

**Description:** Verify event staff and CM of event location are notified after attendance response is submitted.

**Preconditions:**
- Event E8 allows attendance response
- Student H can submit response
- Event E8 has assigned event staff and CM users for the same location
- Notification channels are configured and operational

| #   | Action | Expected Result | Test Data |
| --- | ------ | --------------- | --------- |
| 1   | Submit attendance response from Learner App as Student H | Submission succeeds | Event E8 |
| 2   | Check notification center/inbox for Event Staff user | Notification about submitted attendance response is received | Staff account |
| 3   | Check notification center/inbox for CM user of event location | Notification about submitted attendance response is received | CM account |

**Severity:** critical
**Priority:** high

---

### [Renseikai] Event Attendance - Invalid access - Unassigned user cannot submit response

**Description:** Verify users not assigned/linked to event participant cannot submit attendance response.

**Preconditions:**
- Event E9 allows attendance response
- Student I is assigned to Event E9
- Student X is not assigned to Event E9

| #   | Action | Expected Result | Test Data |
| --- | ------ | --------------- | --------- |
| 1   | Open Learner App as Student X and try to access Event E9 | Event is not listed or detail is inaccessible | Student X |
| 2   | Attempt direct deep link to Event E9 detail | Access denied or not found; no attendance response action available | Event E9 deep link |

**Severity:** major
**Priority:** high

---

### [Renseikai] Event Attendance - Regression - Existing lesson attendance response flow unchanged

**Description:** Regression check for explicit scope statement that lesson attendance response submission must work as before.

**Preconditions:**
- Lesson L1 exists with Student J assigned
- Student J can submit lesson attendance response in current release baseline

| #   | Action | Expected Result | Test Data |
| --- | ------ | --------------- | --------- |
| 1   | Open Learner App as Student J and navigate to Lesson L1 detail | Lesson detail displays attendance response action as before | Lesson L1 |
| 2   | Submit lesson response = Leave Early | Submission succeeds | Status: Leave Early |
| 3   | Re-open Lesson L1 detail | Response remains saved and displayed correctly | Lesson L1 |

**Severity:** critical
**Priority:** high

---

### [Renseikai] Event Attendance - Regression - No BO flow change for lesson attendance collection

**Description:** Verify BO behavior remains unchanged as ticket scope states no BO/SF change.

**Preconditions:**
- BO user with permission to collect attendance
- Existing lesson and event records available for baseline comparison

| #   | Action | Expected Result | Test Data |
| --- | ------ | --------------- | --------- |
| 1   | Open BO lesson attendance collection page | Existing UI and actions remain unchanged from baseline | BO lesson page |
| 2   | Open BO event attendance related page | Existing UI and actions remain unchanged from baseline (except data from app submission visible if already supported) | BO event page |

**Severity:** major
**Priority:** medium

---

### [Renseikai] Event Attendance - Multi-role conflict - Student and parent submit different statuses

**Description:** Verify system behavior when both student and parent are allowed and submit different statuses for same event participant.

> Note: Final expected conflict-resolution rule must be confirmed with product/engineering if not defined in PRD.

**Preconditions:**
- Event E10 allows both Student and Parent responses
- Student K and Parent K are linked and both can access Event E10
- No prior response for Event E10

| #   | Action | Expected Result | Test Data |
| --- | ------ | --------------- | --------- |
| 1   | Student K submits status = Attend | Submission succeeds | Event E10 |
| 2   | Parent K submits status = Absent for same event | Submission behavior follows defined conflict rule | Event E10 |
| 3   | Re-open event detail in both apps and check backend record | Final stored status and displayed status are consistent with product rule (latest-wins or role-priority) | Student K / Parent K |

**Severity:** major
**Priority:** high
