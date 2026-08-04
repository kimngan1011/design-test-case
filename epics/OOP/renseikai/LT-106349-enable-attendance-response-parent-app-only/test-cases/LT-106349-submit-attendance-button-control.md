# Test Cases: LT-106349 – [Renseikai] Enable Attendance Response in Parent App Only

## Suite: [Renseikai] Lesson Attendance – Submit Attendance Button Control

### [Renseikai] Lesson Attendance – Submit Attendance – Config audience=["parent"] – Button visible in Parent App

**Description:** Decision Table — When `lesson.submit_attendance.audience = ["parent"]`, the Submit Attendance button is shown to the parent user in the Learner App.

**Preconditions:**
- Config `lesson.submit_attendance.audience = ["parent"]` is set for the Renseikai tenant
- Lesson L1 is Published and visible in the Learner App
- Parent A is linked to Student A assigned to Lesson L1
- Parent A is logged into the Learner App (parent mode)

| #   | Action | Expected Result | Test Data |
| --- | ------ | --------------- | --------- |
| 1   | Open Learner App as Parent A and navigate to Lesson L1 detail | Lesson detail screen is displayed | Lesson L1 |
| 2   | Observe the lesson action area | Submit Attendance button is visible and tappable | Parent A |

**Severity:** critical
**Priority:** high

---

### [Renseikai] Lesson Attendance – Submit Attendance – Config audience=["parent"] – Button hidden in Student App

**Description:** Decision Table — When `lesson.submit_attendance.audience = ["parent"]`, the Submit Attendance button is NOT shown to the student in the Learner App.

**Preconditions:**
- Config `lesson.submit_attendance.audience = ["parent"]` is set for the Renseikai tenant
- Lesson L1 is Published and visible in the Learner App
- Student A is assigned to Lesson L1 and logged into the Learner App (student mode)

| #   | Action | Expected Result | Test Data |
| --- | ------ | --------------- | --------- |
| 1   | Open Learner App as Student A and navigate to Lesson L1 detail | Lesson detail screen is displayed | Lesson L1 |
| 2   | Observe the lesson action area | Submit Attendance button is NOT visible | Student A |

**Severity:** critical
**Priority:** high

---

### [Renseikai] Lesson Attendance – Submit Attendance – Config audience=["student"] – Button visible for student, hidden for parent

**Description:** Decision Table — When `lesson.submit_attendance.audience = ["student"]`, the Submit Attendance button is shown to the student but NOT to the parent.

**Preconditions:**
- Config `lesson.submit_attendance.audience = ["student"]` is set for the Renseikai tenant
- Lesson L2 is Published and visible in the Learner App
- Student B is assigned to Lesson L2; Parent B is linked to Student B
- Both Student B and Parent B are logged into their respective Learner App sessions

| #   | Action | Expected Result | Test Data |
| --- | ------ | --------------- | --------- |
| 1   | Open Learner App as Student B and navigate to Lesson L2 detail | Lesson detail screen is displayed | Lesson L2 |
| 2   | Observe the lesson action area as Student B | Submit Attendance button is visible and tappable | Student B |
| 3   | Open Learner App as Parent B and navigate to Lesson L2 detail | Lesson detail screen is displayed | Lesson L2 |
| 4   | Observe the lesson action area as Parent B | Submit Attendance button is NOT visible | Parent B |

**Severity:** critical
**Priority:** high

---

### [Renseikai] Lesson Attendance – Submit Attendance – Config audience=["student","parent"] – Button visible for both user types

**Description:** Decision Table — When `lesson.submit_attendance.audience = ["student","parent"]`, the Submit Attendance button is shown to both student and parent.

**Preconditions:**
- Config `lesson.submit_attendance.audience = ["student","parent"]` is set for the Renseikai tenant
- Lesson L3 is Published and visible in the Learner App
- Student C is assigned to Lesson L3; Parent C is linked to Student C
- Both Student C and Parent C are logged into their respective Learner App sessions

| #   | Action | Expected Result | Test Data |
| --- | ------ | --------------- | --------- |
| 1   | Open Learner App as Student C and navigate to Lesson L3 detail | Lesson detail screen is displayed | Lesson L3 |
| 2   | Observe the lesson action area as Student C | Submit Attendance button is visible | Student C |
| 3   | Open Learner App as Parent C and navigate to Lesson L3 detail | Lesson detail screen is displayed | Lesson L3 |
| 4   | Observe the lesson action area as Parent C | Submit Attendance button is visible | Parent C |

**Severity:** critical
**Priority:** high

---

### [Renseikai] Lesson Attendance – Submit Attendance – Config audience=[] with is_enable=true – Both user types see button (legacy fallback)

**Description:** Decision Table — When `lesson.submit_attendance.audience = []` (empty array), the system falls back to `lesson.submit_attendance.is_enable`. With `is_enable = true`, both student and parent see the Submit Attendance button.

**Preconditions:**
- Config `lesson.submit_attendance.audience = []` (empty array) is set for the Renseikai tenant
- Config `lesson.submit_attendance.is_enable = true` is set (fallback enabled)
- Lesson L4 is Published and visible in the Learner App
- Student D is assigned to Lesson L4; Parent D is linked to Student D
- Both Student D and Parent D are logged into their respective Learner App sessions

| #   | Action | Expected Result | Test Data |
| --- | ------ | --------------- | --------- |
| 1   | Open Learner App as Student D and navigate to Lesson L4 detail | Lesson detail screen is displayed | Lesson L4 |
| 2   | Observe the lesson action area as Student D | Submit Attendance button is visible (fallback: is_enable = true) | Student D |
| 3   | Open Learner App as Parent D and navigate to Lesson L4 detail | Lesson detail screen is displayed | Lesson L4 |
| 4   | Observe the lesson action area as Parent D | Submit Attendance button is visible (fallback: is_enable = true) | Parent D |

**Severity:** critical
**Priority:** high

---

### [Renseikai] Lesson Attendance – Submit Attendance – Config audience=[] with is_enable=false – Button hidden for all users (legacy fallback)

**Description:** Decision Table — When `lesson.submit_attendance.audience = []` (empty array) and `lesson.submit_attendance.is_enable = false`, the Submit Attendance button is hidden for all user types.

**Preconditions:**
- Config `lesson.submit_attendance.audience = []` (empty array) is set for the Renseikai tenant
- Config `lesson.submit_attendance.is_enable = false` is set (fallback disabled)
- Lesson L5 is Published and visible in the Learner App
- Student E and linked Parent E can both view Lesson L5

| #   | Action | Expected Result | Test Data |
| --- | ------ | --------------- | --------- |
| 1   | Open Learner App as Student E and navigate to Lesson L5 detail | Lesson detail screen is displayed | Lesson L5 |
| 2   | Observe the lesson action area as Student E | Submit Attendance button is NOT visible | Student E |
| 3   | Open Learner App as Parent E and navigate to Lesson L5 detail | Lesson detail screen is displayed | Lesson L5 |
| 4   | Observe the lesson action area as Parent E | Submit Attendance button is NOT visible | Parent E |

**Severity:** critical
**Priority:** high

---

### [Renseikai] Lesson Attendance – Submit Attendance – Config audience=["parent"] – All status options available for parent

**Description:** Happy Path — When `lesson.submit_attendance.audience = ["parent"]`, the parent can open the response form and all four status options (Attend, Absent, Late, Leave Early) are available. Parent submits successfully.

**Preconditions:**
- Config `lesson.submit_attendance.audience = ["parent"]` is set for the Renseikai tenant
- Lesson L6 is Published and upcoming; Parent F is linked to Student F assigned to Lesson L6
- Parent F has not submitted an attendance response for Lesson L6

| #   | Action | Expected Result | Test Data |
| --- | ------ | --------------- | --------- |
| 1   | Open Learner App as Parent F and navigate to Lesson L6 detail | Lesson detail is displayed; Submit Attendance button is visible | Lesson L6 |
| 2   | Tap the Submit Attendance button | Attendance response form opens | Parent F |
| 3   | Observe the list of available status options | Options shown: Attend, Absent, Late, Leave Early (4 options total) | — |
| 4   | Select status = Attend and tap Submit | Submission succeeds; success feedback is shown | Status: Attend |
| 5   | Re-open Lesson L6 detail | Submitted attendance response is displayed as Attend | Lesson L6 |

**Severity:** critical
**Priority:** high

---

### [Renseikai] Lesson Attendance – Submit Attendance – Config audience=["parent"] – Parent updates previously submitted response

**Description:** State Transition — When `lesson.submit_attendance.audience = ["parent"]`, a parent who already submitted an attendance response can open the form again and change the status.

**Preconditions:**
- Config `lesson.submit_attendance.audience = ["parent"]` is set for the Renseikai tenant
- Lesson L7 is Published and not yet started; Parent G is linked to Student G assigned to Lesson L7
- Parent G has already submitted attendance status = Absent for Lesson L7

| #   | Action | Expected Result | Test Data |
| --- | ------ | --------------- | --------- |
| 1   | Open Learner App as Parent G and navigate to Lesson L7 detail | Lesson detail is displayed; existing response shown as Absent | Lesson L7 |
| 2   | Tap the Submit Attendance button again | Attendance response form opens with Absent pre-selected | Parent G |
| 3   | Change status to Late and tap Submit | Submission succeeds; success feedback is shown | New status: Late |
| 4   | Re-open Lesson L7 detail | Attendance response is updated to Late | Lesson L7 |

**Severity:** major
**Priority:** medium

---
