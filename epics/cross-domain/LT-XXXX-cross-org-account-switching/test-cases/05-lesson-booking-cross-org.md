# Test Cases: LT-XXXX — Cross-organization account switching

## Suite: Lesson Booking

### Account Switch – Lesson Booking – Cross-org students – Booking is created for selected student

**Description:** AC PX-2762.01 — Scenario — A parent switches between students in different organizations and books one eligible lesson for each selected student.

**Preconditions:**
- Parent CrossOrg is logged in to the mobile app.
- Parent CrossOrg is linked to Student Renseikai at Renseikai.
- Parent CrossOrg is linked to Student Asojuku at Asojuku.
- Student Renseikai has an eligible, unbooked lesson `Renseikai Booking Lesson`.
- Student Asojuku has an eligible, unbooked lesson `Asojuku Booking Lesson`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Parent CrossOrg selects Student Renseikai, opens `Renseikai Booking Lesson`, and confirms the booking. | A booking confirmation is displayed for Student Renseikai and `Renseikai Booking Lesson` appears in that student's lesson list. | selected student = Student Renseikai |
| 2 | Parent CrossOrg switches to Student Asojuku, opens `Asojuku Booking Lesson`, and confirms the booking. | A booking confirmation is displayed for Student Asojuku and `Asojuku Booking Lesson` appears in that student's lesson list. | selected student = Student Asojuku |
| 3 | Parent CrossOrg returns to Student Renseikai's lesson list. | The list contains `Renseikai Booking Lesson` and does not show Student Asojuku's booked lesson as Student Renseikai's booking. | selected student = Student Renseikai |

**Severity:** minor
**Priority:** medium
