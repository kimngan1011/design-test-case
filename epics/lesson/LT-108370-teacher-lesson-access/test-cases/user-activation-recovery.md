# Test Cases: LT-108370 — Teacher Lesson Access

## Suite: User Activation Recovery

### Teacher Lesson Access – New active user – Existing assignment – Assigned lesson becomes visible

**Description:** AC-01 — State Transition, Regression — An active user created after a lesson assignment receives access to that lesson.

**Preconditions:**

- HQ or CM Staff is logged in to Salesforce.
- Teacher Contact A is assigned to Lesson Alpha.
- Teacher Contact A has no Salesforce User.
- Lesson Alpha has the visible name `LT108370 Alpha`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff creates an active Salesforce User linked to Teacher Contact A. | The new user is active and linked to Teacher Contact A. | User status = Active; Contact = Teacher Contact A |
| 2 | Teacher A signs in to Back Office and opens the lesson list. | The lesson list contains `LT108370 Alpha`. | Expected lesson = LT108370 Alpha |

**Severity:** major
**Priority:** high

---

### Teacher Lesson Access – Reactivated user – Existing assignment – Assigned lesson becomes visible

**Description:** AC-02 — State Transition, Decision Table — Reactivating a user repairs access that was missed while the user was inactive.

**Preconditions:**

- HQ or CM Staff is logged in to Salesforce.
- Teacher Contact B is assigned to Lesson Bravo.
- Teacher Contact B has an inactive Salesforce User.
- Lesson Bravo has the visible name `LT108370 Bravo`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff changes Teacher B's Salesforce User status from inactive to active. | Teacher B's Salesforce User is active. | Previous status = Inactive; New status = Active |
| 2 | Teacher B signs in to Back Office and opens the lesson list. | The lesson list contains `LT108370 Bravo`. | Expected lesson = LT108370 Bravo |

**Severity:** major
**Priority:** high

---

### Teacher Lesson Access – New active user – Multiple existing assignments – Every assigned lesson becomes visible

**Description:** AC-01 — Regression — Recovery applies to every lesson already assigned to the same teacher.

**Preconditions:**

- HQ or CM Staff is logged in to Salesforce.
- Teacher Contact C is assigned to Lesson Charlie and Lesson Delta.
- Teacher Contact C has no Salesforce User.
- The two lessons have visible names `LT108370 Charlie` and `LT108370 Delta`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff creates an active Salesforce User linked to Teacher Contact C. | The new user is active and linked to Teacher Contact C. | User status = Active; Contact = Teacher Contact C |
| 2 | Teacher C signs in to Back Office and opens the lesson list. | The lesson list contains both `LT108370 Charlie` and `LT108370 Delta`. | Expected lessons = LT108370 Charlie, LT108370 Delta |

**Severity:** major
**Priority:** high

---

### Teacher Lesson Access – New active user – Existing assignment – Background recovery request is created

**Description:** AC-01 — CRUD, Regression — An eligible user creation produces one asynchronous recovery request.

**Preconditions:**

- HQ or CM Staff is logged in to Salesforce.
- Teacher Contact D is assigned to Lesson Echo.
- Teacher Contact D has no Salesforce User.
- No unfinished lesson-access recovery request exists for Teacher Contact D.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff creates an active Salesforce User linked to Teacher Contact D. | Salesforce accepts the user creation without a mixed-data-operation error. | User status = Active; Contact = Teacher Contact D |
| 2 | HQ or CM Staff opens the background recovery request list for Teacher Contact D. | One unfinished lesson-access recovery request exists for Teacher Contact D. | Contact = Teacher Contact D; Expected request count = 1 |

**Severity:** major
**Priority:** high
