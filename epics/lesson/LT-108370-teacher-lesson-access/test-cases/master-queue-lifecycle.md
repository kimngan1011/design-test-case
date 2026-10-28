# Test Cases: LT-108370 — Teacher Lesson Access

## Suite: Master Queue Lifecycle

### Teacher Lesson Access – Pending recovery request – Repeated activation event – Duplicate request is not created

**Description:** AC-06 — State Transition, Decision Table — A pending recovery request blocks another request for the same teacher.

**Preconditions:**

- HQ or CM Staff is logged in to Salesforce.
- Teacher Contact K is assigned to Lesson Kilo.
- Teacher K has an active Salesforce User.
- One unfinished recovery request for Teacher Contact K has status Pending.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff causes a second eligible activation event for Teacher K. | Salesforce accepts the event without creating an additional Pending recovery request. | Existing request status = Pending |
| 2 | HQ or CM Staff counts unfinished recovery requests for Teacher Contact K. | The count is one. | Expected unfinished request count = 1 |

**Severity:** major
**Priority:** high

---

### Teacher Lesson Access – Failed recovery request – Repeated activation event – Duplicate request is not created

**Description:** AC-06 — State Transition, Decision Table — A failed recovery request remains the retry candidate and blocks a duplicate request.

**Preconditions:**

- HQ or CM Staff is logged in to Salesforce.
- Teacher Contact L is assigned to Lesson Lima.
- Teacher L has an active Salesforce User.
- One unfinished recovery request for Teacher Contact L has status Failed.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff causes a second eligible activation event for Teacher L. | Salesforce accepts the event without creating another recovery request. | Existing request status = Failed |
| 2 | HQ or CM Staff counts unfinished recovery requests for Teacher Contact L. | The count is one and the existing request remains the retry candidate. | Expected unfinished request count = 1 |

**Severity:** major
**Priority:** high

---

### Teacher Lesson Access – Completed recovery request – Later activation event – New reconciliation request is created

**Description:** AC-06 — State Transition, CRUD — A successful earlier run does not prevent a later recovery request.

**Preconditions:**

- HQ or CM Staff is logged in to Salesforce.
- Teacher Contact M is assigned to Lesson Mike.
- Teacher M has an inactive Salesforce User.
- One earlier recovery request for Teacher Contact M has status Success.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff changes Teacher M's Salesforce User status from inactive to active. | A new unfinished recovery request is created for Teacher Contact M. | Previous request status = Success; New user status = Active |
| 2 | HQ or CM Staff opens the recovery requests for Teacher Contact M. | The earlier successful request remains unchanged and one newer unfinished request exists. | Expected successful requests = 1; Expected unfinished requests = 1 |

**Severity:** minor
**Priority:** medium
