# Test Cases: LT-107255 — Lesson Assignment Reconciliation

## Suite: Lesson Assignment Update

### Lesson Assignment – Create Class Lesson – Existing Manual Session – Manual Session Retained

**Description:** AC-07, AC-08 — State Transition — Creating a class lesson assigns the eligible student automatically without deleting a session that staff assigned manually.

**Preconditions:**
- Logged in as HQ or CM Staff to the Salesforce org.
- Student A has an active LA for Course A from 2026-08-01 to 2026-12-31.
- Student A is a Class A member from 2026-08-01 to 2026-12-31 and is auto-assigned to existing Lesson A.
- Staff manually assigned Student A to Lesson B, a Course A lesson for Class B, on 2026-08-15.
- today = 2026-08-10; new_lesson_date = 2026-08-20.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Create a new Course A group lesson with Class A. | The new Class A lesson is created. | new_lesson_date = 2026-08-20; class = Class A |
| 2 | Run or wait for class-based lesson assignment to finish. | Student A is automatically assigned to the new Class A lesson. | class member duration covers 2026-08-20 |
| 3 | Open Lesson B student list. | The manually created Student A session remains in Lesson B. | manual session = Lesson B on 2026-08-15 |

**Severity:** critical
**Priority:** high

---

### Lesson Assignment – Change Class on LA – Automatic Old-Class Session – Manual Session Retained

**Description:** AC-07, AC-08 — State Transition — Changing an LA class removes obsolete automatic sessions, creates new eligible sessions, and retains manual sessions.

**Preconditions:**
- Logged in as HQ or CM Staff to the Salesforce org.
- Student A has an active LA for Course A from 2026-08-01 to 2026-12-31 and is a Class A member.
- Student A is auto-assigned to Lesson A for Class A and manually assigned to Lesson B for Class B.
- Class C belongs to Course A and has Lesson C on 2026-08-20.
- today = 2026-08-10; class_change_date = 2026-08-10.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Change Student A's LA class from Class A to Class C with the effective date. | The Class Member history ends Class A and starts Class C on 2026-08-10. | old_class = Class A; new_class = Class C; effective_date = 2026-08-10 |
| 2 | Run or wait for class-based lesson assignment to finish. | The automatic Student A session is removed from ineligible Lesson A and Student A is assigned to eligible Lesson C. | Lesson A = Class A; Lesson C = Class C |
| 3 | Open Lesson B student list. | The manually created Student A session remains in Lesson B. | manual session = Lesson B, Class B |

**Severity:** critical
**Priority:** high

---

### Lesson Assignment – Add Class on LA – Existing Manual Session – Manual Session Retained

**Description:** AC-07, AC-08 — State Transition — Adding a class creates eligible automatic sessions without changing a manual session in another class.

**Preconditions:**
- Logged in as HQ or CM Staff to the Salesforce org.
- Student A has an active LA for Course A from 2026-08-01 to 2026-12-31 and is a Class A member.
- Staff manually assigned Student A to Lesson B, a Course A lesson for Class B, on 2026-08-15.
- Class C belongs to Course A and has Lesson C on 2026-08-20.
- today = 2026-08-10; added_class_start = 2026-08-10.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Add Class C to Student A's LA with the effective date. | A Class C member record is created from 2026-08-10 through 2026-12-31. | class = Class C; effective_date = 2026-08-10 |
| 2 | Run or wait for class-based lesson assignment to finish. | Student A is automatically assigned to eligible Lesson C; existing Class A automatic sessions remain eligible. | Lesson C date = 2026-08-20 |
| 3 | Open Lesson B student list. | The manually created Student A session remains in Lesson B. | manual session = Lesson B, Class B |

**Severity:** critical
**Priority:** high

---

### Lesson Assignment – Cancel Scheduled Class – Automatic Future-Class Session – Manual Session Retained

**Description:** AC-07, AC-08 — State Transition — Cancelling a scheduled class update removes only automatic sessions made ineligible by that scheduled class.

**Preconditions:**
- Logged in as HQ or CM Staff to the Salesforce org.
- Student A has an active LA for Course A through 2026-12-31 and has Class A active from 2026-08-01.
- A scheduled Class C update begins on 2026-09-01; Student A is auto-assigned to Lesson C on 2026-09-10.
- Staff manually assigned Student A to Lesson B for Class B on 2026-09-10.
- today = 2026-08-10; scheduled_class_start = 2026-09-01.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | On Student A's LA, select Cancel Scheduled Class Update for Class C and confirm. | The scheduled Class C member update is cancelled. | scheduled class = Class C; effective_date = 2026-09-01 |
| 2 | Run or wait for class-based lesson assignment to finish. | The automatic Student A session is removed from Lesson C because Class C is no longer active. | automatic session = Lesson C on 2026-09-10 |
| 3 | Open Lesson B student list. | The manually created Student A session remains in Lesson B. | manual session = Lesson B on 2026-09-10 |

**Severity:** critical
**Priority:** high

---

### Lesson Assignment – Lesson Schedule Class Change – Automatic Session – Manual Session Retained

**Description:** AC-07, AC-08 — State Transition — Changing a lesson's class removes only an automatic session that becomes ineligible and retains a manual session elsewhere.

**Preconditions:**
- Logged in as HQ or CM Staff to the Salesforce org.
- Student A has an active LA for Course A and is a Class A member from 2026-08-01 to 2026-12-31.
- Student A is auto-assigned to Lesson A for Class A on 2026-08-20.
- Staff manually assigned Student A to Lesson B for Class B on 2026-08-20.
- Class C belongs to Course A; today = 2026-08-10.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Lesson A's Lesson Schedule Detail and replace Class A with Class C. | Lesson A is associated with Class C. | Lesson A date = 2026-08-20; old_class = Class A; new_class = Class C |
| 2 | Run or wait for class-based lesson assignment to finish. | Student A is removed from Lesson A because its existing session was automatic and Student A is not a Class C member. | Student Session origin = auto-assignment |
| 3 | Open Lesson B student list. | The manually created Student A session remains in Lesson B. | Student Session origin = manual assignment |

**Severity:** critical
**Priority:** high

---

### Lesson Assignment – Import Class Member – Existing Manual Session – Manual Session Retained

**Description:** AC-07, AC-08 — State Transition — Importing a Class Member auto-assigns eligible lessons and retains an existing manual session.

**Preconditions:**
- Logged in as HQ or CM Staff to the Salesforce org.
- Student A has an active LA for Course A from 2026-08-01 to 2026-12-31.
- Class C belongs to Course A and has Lesson C on 2026-08-20.
- Staff manually assigned Student A to Lesson B for Class B on 2026-08-15.
- today = 2026-08-10; imported_class_start = 2026-08-10; imported_class_end = 2026-12-31.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Import a valid Class Member row that assigns Student A to Class C. | The import completes and creates the Class C member record with the imported duration. | student = Student A; class = Class C; start = 2026-08-10; end = 2026-12-31 |
| 2 | Run or wait for class-based lesson assignment to finish. | Student A is automatically assigned to eligible Lesson C. | Lesson C date = 2026-08-20 |
| 3 | Open Lesson B student list. | The manually created Student A session remains in Lesson B. | manual session = Lesson B on 2026-08-15 |

**Severity:** critical
**Priority:** high
