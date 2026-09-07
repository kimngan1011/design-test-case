# Test Cases: LT-107175 — Remote Attendance Status and Tag

## Suite: [Renseikai] Remote Attendance — Notifications

### [Renseikai] Remote Attendance Notification – Lesson Teacher – App submission – Notification Center entry created

**Description:** AC 04.3 — Scenario — T1 receives one attendance notification for APP-301.

**Preconditions:**

- APP-301 is eligible
- teacher T1 is assigned to the lesson.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Student submits Attended Remotely, then opens T1 Notification Center | T1 receives one attendance notification for APP-301 | APP-301; recipient=T1; channel=Notification Center |

**Severity:** major
**Priority:** high

---
### [Renseikai] Remote Attendance Notification – Lesson Teacher – App submission – Salesforce Chatter entry created

**Description:** AC 04.3 — Scenario — T1 receives one attendance notification for APP-302.

**Preconditions:**

- APP-302 is eligible
- teacher T1 is assigned to the lesson.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Student submits Attended Remotely, then opens T1 Salesforce Chatter | T1 receives one attendance notification for APP-302 | APP-302; recipient=T1; channel=Salesforce Chatter |

**Severity:** major
**Priority:** high

---
### [Renseikai] Remote Attendance Notification – Lesson Teacher – Different Centre Manager location – Teacher still notified

**Description:** AC 04.3 — Decision Table — T1 receives the established attendance notification.

**Preconditions:**

- APP-303 teacher T1 is assigned
- Centre Manager location differs from lesson location.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Student submits Attended Remotely | T1 receives the established attendance notification | APP-303; teacher=T1; CM location≠lesson location |

**Severity:** major
**Priority:** high

---
### [Renseikai] Remote Attendance Notification – Centre Manager – Lesson location under Centre Manager brand – Notification delivered

**Description:** AC 04.3 — Decision Table — CM1 receives the established attendance notification.

**Preconditions:**

- APP-304 lesson location is Tokyo
- Centre Manager CM1 is affiliated with Tokyo.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Student submits Attended Remotely, then opens CM1 notification channel | CM1 receives the established attendance notification | APP-304; lesson_location=Tokyo; CM1 location=Tokyo |

**Severity:** major
**Priority:** high

---
### [Renseikai] Remote Attendance Notification – Centre Manager – Different lesson location – Notification withheld

**Description:** AC 04.3 — Negative — CM2 receives no notification for APP-305.

**Preconditions:**

- APP-305 lesson location is Tokyo
- CM2 is affiliated only with Osaka.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Student submits Attended Remotely, then opens CM2 notification channel | CM2 receives no notification for APP-305 | APP-305; lesson_location=Tokyo; CM2 location=Osaka |

**Severity:** major
**Priority:** high

---
### [Renseikai] Remote Attendance Notification – Centre Manager – Matching lesson location – Notification delivered

**Description:** AC 04.3 — Decision Table — CM3 receives the established attendance notification.

**Preconditions:**

- APP-306 is assigned to Location Tokyo.
- Location Tokyo belongs to Brand A.
- CM3 is affiliated with Brand A.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Student submits Attended Remotely, then opens CM3 notification channel | CM3 receives the established attendance notification | APP-306; lesson_location=Tokyo; location_brand=Brand A; CM3 brand=Brand A |

**Severity:** major
**Priority:** high

---
### [Renseikai] Remote Attendance Notification – Centre Manager – Lesson location under a different brand – Notification withheld

**Description:** AC 04.3 — Negative — CM4 receives no notification for APP-307.

**Preconditions:**

- APP-307 is assigned to Location Tokyo.
- Location Tokyo belongs to Brand A.
- CM4 is affiliated only with Brand B.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Student submits Attended Remotely, then opens CM4 notification channel | CM4 receives no notification for APP-307 | APP-307; lesson_location=Tokyo; location_brand=Brand A; CM4 brand=Brand B |

**Severity:** major
**Priority:** high

---
