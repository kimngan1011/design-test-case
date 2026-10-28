# Test Cases: LT-108370 — Teacher Lesson Access

## Suite: Sharing Integrity

### Teacher Lesson Access – Lesson permission – Recovered user – Edit permission is created for the assigned lesson

**Description:** AC-03 — CRUD, Permission Matrix — The recovered teacher receives the required Edit permission for the assigned lesson.

**Preconditions:**

- HQ or CM Staff is logged in to Salesforce.
- Teacher Contact E is assigned to Lesson Foxtrot.
- Teacher Contact E has no Salesforce User.
- Lesson Foxtrot has no teacher permission for Teacher Contact E.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff creates an active Salesforce User linked to Teacher Contact E. | The lesson-access recovery completes for Teacher Contact E. | User status = Active; Contact = Teacher Contact E |
| 2 | HQ or CM Staff opens the lesson permissions for Lesson Foxtrot. | Exactly one teacher permission exists for Teacher E with Edit access and the lesson-teacher assignment reason. | Recipient = Teacher E; Access = Edit; Permission count = 1 |

**Severity:** major
**Priority:** high

---

### Teacher Lesson Access – Lesson allocation permission – Active student session – Edit permission is created

**Description:** AC-03 — Decision Table, CRUD — A lesson allocation connected by a non-deleted student session receives the missing teacher permission.

**Preconditions:**

- HQ or CM Staff is logged in to Salesforce.
- Teacher Contact F is assigned to Lesson Golf.
- Lesson Golf has a non-deleted student session linked to Lesson Allocation Golf-1.
- Teacher Contact F has no Salesforce User.
- Lesson Allocation Golf-1 has no teacher permission for Teacher Contact F.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff creates an active Salesforce User linked to Teacher Contact F. | The lesson-access recovery completes for Teacher Contact F. | User status = Active; Contact = Teacher Contact F |
| 2 | HQ or CM Staff opens the permissions for Lesson Allocation Golf-1. | Exactly one teacher permission exists for Teacher F with Edit access and the lesson-teacher assignment reason. | Session status = Not deleted; Allocation = Golf-1; Permission count = 1 |

**Severity:** major
**Priority:** high

---

### Teacher Lesson Access – Lesson allocation permission – Deleted student session – No allocation permission is created

**Description:** AC-03 — Decision Table, Negative — A deleted student session cannot create allocation access.

**Preconditions:**

- HQ or CM Staff is logged in to Salesforce.
- Teacher Contact G is assigned to Lesson Hotel.
- Lesson Hotel has only one deleted student session linked to Lesson Allocation Hotel-1.
- Teacher Contact G has no Salesforce User.
- Lesson Allocation Hotel-1 has no teacher permission for Teacher Contact G.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff creates an active Salesforce User linked to Teacher Contact G. | The lesson-access recovery completes for Teacher Contact G. | User status = Active; Contact = Teacher Contact G |
| 2 | HQ or CM Staff opens the permissions for Lesson Allocation Hotel-1. | No teacher permission exists for Teacher G. | Session status = Deleted; Expected permission count = 0 |

**Severity:** minor
**Priority:** medium

---

### Teacher Lesson Access – Repeated recovery – Existing teacher permissions – No duplicate or cross-teacher change occurs

**Description:** AC-04 — State Transition, Regression — Two activation events keep one permission for the target teacher and preserve another teacher's permission.

**Preconditions:**

- HQ or CM Staff is logged in to Salesforce.
- Teacher Contact H and Teacher Contact I are assigned to Lesson India.
- Teacher H has an inactive Salesforce User and has no teacher permission for Lesson India.
- Teacher I has an active Salesforce User and already has one Edit permission for Lesson India.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff changes Teacher H's Salesforce User status from inactive to active. | One recovery request is created for Teacher H. | First activation; Previous status = Inactive |
| 2 | HQ or CM Staff waits for Teacher H's first recovery request to finish. | The first recovery request has status Success. | Recovery run = 1 |
| 3 | HQ or CM Staff changes Teacher H's Salesforce User status from active to inactive. | Teacher H's Salesforce User is inactive. | Intermediate status = Inactive |
| 4 | HQ or CM Staff changes Teacher H's Salesforce User status from inactive to active. | A new recovery request is created for Teacher H. | Second activation; Previous status = Inactive |
| 5 | HQ or CM Staff waits for Teacher H's second recovery request to finish. | The second recovery request has status Success. | Recovery run = 2 |
| 6 | HQ or CM Staff opens the lesson permissions for Lesson India. | Teacher H has exactly one Edit permission and Teacher I still has exactly one Edit permission. | Expected permissions: Teacher H = 1; Teacher I = 1 |

**Severity:** major
**Priority:** high

---

### Teacher Lesson Access – User without lesson assignment – Active user creation – No recovery request or permission is created

**Description:** AC-05 — Equivalence Partitioning, Negative — A non-teacher Contact remains unaffected.

**Preconditions:**

- HQ or CM Staff is logged in to Salesforce.
- Staff Contact J has no lesson-teacher assignment.
- Staff Contact J has no Salesforce User.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff creates an active Salesforce User linked to Staff Contact J. | The new user is active and linked to Staff Contact J. | User status = Active; Contact = Staff Contact J |
| 2 | HQ or CM Staff searches lesson-access recovery requests and teacher permissions for Staff Contact J. | No recovery request and no teacher permission are found for Staff Contact J. | Expected request count = 0; Expected permission count = 0 |

**Severity:** minor
**Priority:** medium
