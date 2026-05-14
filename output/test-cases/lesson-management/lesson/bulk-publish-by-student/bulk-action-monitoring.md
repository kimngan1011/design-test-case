# Test Cases: LT-98532 — Bulk Publish Lessons by Student

## Suite: [Riso] Bulk Publish by Student – Bulk Action Monitoring

---

### [Riso] Bulk Action Monitoring – Riso User with Permission – Monitoring Page Is Accessible

**Description:** AC 03.1 — Permission Matrix — A Riso HQ Admin or CM user with the "Bulk Action Monitoring" permission can access the Bulk Action Monitoring page.

**Preconditions:**

- Bulk Action Monitoring config is **ON** for the Riso partner
- User A is a Riso HQ Admin with the "Bulk Action Monitoring" permission assigned
- User B is a Riso CM with the "Bulk Action Monitoring" permission assigned

| #   | Action                                                                                                | Expected Result                                                         | Test Data          |
| --- | ----------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------- | ------------------ |
| 1   | Log into SF as User A (Riso HQ Admin with permission) and navigate to the Bulk Action Monitoring page | Bulk Action Monitoring page loads successfully; job records are visible | User A credentials |
| 2   | Log out and log in as User B (Riso CM with permission); navigate to the Bulk Action Monitoring page   | Bulk Action Monitoring page loads successfully; job records are visible | User B credentials |

**Severity:** major
**Priority:** high

---

### [Riso] Bulk Action Monitoring – Riso User Without Permission – Monitoring Page Is Not Accessible

**Description:** AC 03.1 — Permission Matrix + Negative Testing — A Riso user who does not have the "Bulk Action Monitoring" permission cannot access the monitoring page, even though the config is ON for the Riso partner.

**Preconditions:**

- Bulk Action Monitoring config is **ON** for the Riso partner
- User C is a Riso staff member **without** the "Bulk Action Monitoring" permission

| #   | Action                                                      | Expected Result                                                                                   | Test Data          |
| --- | ----------------------------------------------------------- | ------------------------------------------------------------------------------------------------- | ------------------ |
| 1   | Log into SF as User C (Riso user, no monitoring permission) | Login succeeds                                                                                    | User C credentials |
| 2   | Attempt to navigate to the Bulk Action Monitoring page      | Page is **not accessible**; either the menu item is hidden or an "Access Denied" message is shown | ""                 |

**Severity:** major
**Priority:** high

---

### [Riso] Bulk Action Monitoring – Non-Riso Partner – Monitoring Page Not Available

**Description:** AC 03.1 — Permission Matrix + Negative Testing — A user from a partner for which the Bulk Action Monitoring config is OFF cannot access the monitoring page regardless of their role.

**Preconditions:**

- Bulk Action Monitoring config is **OFF** for Partner X (a non-Riso partner)
- User D is an HQ Admin at Partner X

| #   | Action                                                 | Expected Result                                                    | Test Data          |
| --- | ------------------------------------------------------ | ------------------------------------------------------------------ | ------------------ |
| 1   | Log into SF as User D (Partner X HQ Admin)             | Login succeeds                                                     | User D credentials |
| 2   | Attempt to navigate to the Bulk Action Monitoring page | Page is **not accessible**; menu item is hidden or "Access Denied" | ""                 |

**Severity:** major
**Priority:** high

---

### [Riso] Bulk Action Monitoring – Bulk Publish – One Record Created per Student+Location Pairing

**Description:** AC 03.1 — CRUD Testing — After a Bulk Publish job completes, exactly one monitoring record is created for each student+location pairing in the batch. Multiple students in the same batch each get their own record.

**Preconditions:**

- User is logged into SF as a Riso HQ Admin with "Bulk Action Monitoring" permission
- Bulk Publish was submitted for a period with 3 students (Student A, Student B, Student C) all at the same location "Hanoi Branch"
- The "Apply to selected students" checkbox was activated

| #   | Action                                                                            | Expected Result                                                                                                                                          | Test Data |
| --- | --------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- | --------- |
| 1   | After the Bulk Publish job completes, navigate to the Bulk Action Monitoring page | Monitoring page loads                                                                                                                                    | ""        |
| 2   | Observe the number of records created for this batch                              | Exactly **3 records** are present — one for each student+location pairing (Student A / Hanoi Branch, Student B / Hanoi Branch, Student C / Hanoi Branch) | ""        |
| 3   | Confirm each record shows the same Batch ID (grouped together)                    | All 3 records share the **same Batch ID**                                                                                                                | ""        |

**Severity:** major
**Priority:** high

---

### [Riso] Bulk Action Monitoring – Job Record Fields – All Required Fields Populated Correctly

**Description:** AC 03.2 — Equivalence Partitioning — Every Bulk Publish monitoring record contains all required fields populated with correct values.

**Preconditions:**

- User is logged into SF as a Riso HQ Admin with "Bulk Action Monitoring" permission
- A Bulk Publish job was completed for Student A at "Hanoi Branch" for the period May 1–31, 2026
- The job created 5 lessons; all 5 were published successfully; the job was created by User A and completed at a known time

| #   | Action                                                                                | Expected Result                                                                   | Test Data |
| --- | ------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- | --------- |
| 1   | Navigate to the Bulk Action Monitoring page and open the record for Student A's batch | Record detail is displayed                                                        | ""        |
| 2   | Confirm the **Action** field                                                          | Field shows **"Bulk Publish"**                                                    | ""        |
| 3   | Confirm the **Job Status** field                                                      | Field shows **"Completed"**                                                       | ""        |
| 4   | Confirm the **Location** field                                                        | Field shows **"Hanoi Branch"**                                                    | ""        |
| 5   | Confirm the **Student** field                                                         | Field shows **"Student A"**                                                       | ""        |
| 6   | Confirm the **Lesson Start Date** and **Lesson End Date** fields                      | Start Date = May 1, 2026; End Date = May 31, 2026                                 | ""        |
| 7   | Confirm the **Total Lessons** field                                                   | Field shows **5**                                                                 | ""        |
| 8   | Confirm the **Success** count                                                         | Field shows **5**                                                                 | ""        |
| 9   | Confirm the **Failed** count                                                          | Field shows **0**                                                                 | ""        |
| 10  | Confirm the **Processed Count** field                                                 | Field shows **5** (= 5 Success + 0 Failed)                                        | ""        |
| 11  | Confirm **Created By** and **Created Time** fields                                    | Created By shows User A's name; Created Time shows the time the job was submitted | ""        |

**Severity:** minor
**Priority:** medium

---

### [Riso] Bulk Action Monitoring – Job Status Lifecycle – Pending to Processing to Completed

**Description:** AC 03.3 — State Transition Testing — A Bulk Publish job progresses through the expected status lifecycle: Pending → Processing → Completed.

**Preconditions:**

- User is logged into SF as a Riso HQ Admin with "Bulk Action Monitoring" permission
- A Bulk Publish request has just been submitted (job is in the queue)

| #   | Action                                                                                    | Expected Result                                          | Test Data |
| --- | ----------------------------------------------------------------------------------------- | -------------------------------------------------------- | --------- |
| 1   | Immediately after submitting the Bulk Publish request, navigate to Bulk Action Monitoring | The record for this job shows Job Status = **"Pending"** | ""        |
| 2   | Refresh the Bulk Action Monitoring page while the job is being processed                  | Job Status transitions to **"Processing"**               | ""        |
| 3   | Refresh again after the job finishes                                                      | Job Status is now **"Completed"**                        | ""        |
| 4   | Confirm Processed Count = Success + Failed (e.g. 3 success + 0 failed = 3)                | Processed Count = **3**                                  | ""        |

**Severity:** major
**Priority:** high

---

### [Riso] Bulk Action Monitoring – Processed Count – Auto-Calculated as Success Plus Failed

**Description:** AC 03.3 — Equivalence Partitioning — The Processed Count field in a monitoring record always equals the sum of Success Count and Failed Count.

**Preconditions:**

- User is logged into SF as a Riso HQ Admin with "Bulk Action Monitoring" permission
- A Bulk Publish job completed with: Total Lessons = 5, Success = 3, Failed = 2 (partial failure simulated)

| #   | Action                                                                               | Expected Result       | Test Data |
| --- | ------------------------------------------------------------------------------------ | --------------------- | --------- |
| 1   | Navigate to Bulk Action Monitoring and open the record for the partial-failure batch | Record is displayed   | ""        |
| 2   | Read the **Success** field                                                           | Shows **3**           | ""        |
| 3   | Read the **Failed** field                                                            | Shows **2**           | ""        |
| 4   | Read the **Processed Count** field                                                   | Shows **5** (= 3 + 2) | ""        |

**Severity:** minor
**Priority:** medium

---

### [Riso] Bulk Action Monitoring – Partial Failure – Job Status Becomes "Completed with Errors"

**Description:** AC 03.4 — Decision Table — When a Bulk Publish job finishes processing all lessons but at least one lesson failed to publish, the Job Status is set to "Completed with Errors".

**Preconditions:**

- User is logged into SF as a Riso HQ Admin with "Bulk Action Monitoring" permission
- A Bulk Publish job completed with some failures (Failed Count > 0; all lessons were attempted)

| #   | Action                                                                                    | Expected Result                                   | Test Data |
| --- | ----------------------------------------------------------------------------------------- | ------------------------------------------------- | --------- |
| 1   | Navigate to Bulk Action Monitoring and find the record for the batch with partial failure | Record is displayed                               | ""        |
| 2   | Read the **Job Status** field                                                             | Job Status = **"Completed with Errors"**          | ""        |
| 3   | Confirm the **Failed** count is greater than 0                                            | Failed count shows a number > 0                   | ""        |
| 4   | Confirm the **Success** count is greater than 0                                           | Success count shows a number > 0 (not all failed) | ""        |

**Severity:** major
**Priority:** high

---

### [Riso] Bulk Action Monitoring – System Error – Job Status Becomes "Failed"

**Description:** AC 03.4 — Negative Testing — When the Bulk Publish job is terminated by a system error before all lessons are processed, the Job Status is set to "Failed".

**Preconditions:**

- User is logged into SF as a Riso HQ Admin with "Bulk Action Monitoring" permission
- A Bulk Publish job was submitted and a system error terminated it before completion (simulated via backend tooling)

| #   | Action                                                                      | Expected Result                            | Test Data |
| --- | --------------------------------------------------------------------------- | ------------------------------------------ | --------- |
| 1   | Navigate to Bulk Action Monitoring and find the record for the failed batch | Record is displayed                        | ""        |
| 2   | Read the **Job Status** field                                               | Job Status = **"Failed"**                  | ""        |
| 3   | Confirm the job was terminated early (not all lessons were processed)       | Processed Count is less than Total Lessons | ""        |

**Severity:** minor
**Priority:** medium

---

### [Riso] Bulk Action Monitoring – Default Filters – Created Date Defaults to This Week and Location Defaults to User's Assigned Location

**Description:** AC 03.6 — Decision Table — When the Bulk Action Monitoring page opens, the default filter state shows records for "this week" and the user's assigned location(s) only.

**Preconditions:**

- User is logged into SF as a Riso CM with permission; CM is assigned to "Hanoi Branch" only
- Job records exist for the current week at "Hanoi Branch" and also records from last week
- A record also exists for "Saigon Branch" (a location the CM is not assigned to) created this week

| #   | Action                                                | Expected Result                                                                            | Test Data |
| --- | ----------------------------------------------------- | ------------------------------------------------------------------------------------------ | --------- |
| 1   | Navigate to the Bulk Action Monitoring page           | Page loads with default filters applied                                                    | ""        |
| 2   | Observe the **Created Date** filter default value     | Filter is pre-set to **"This week"**                                                       | ""        |
| 3   | Observe the records shown                             | Only records from the **current week** are displayed; records from last week are not shown | ""        |
| 4   | Observe the **Location** filter and the records shown | Only records for **"Hanoi Branch"** are shown; records for "Saigon Branch" are not visible | ""        |

**Severity:** minor
**Priority:** medium

---

### [Riso] Bulk Action Monitoring – Data Retention – Records Purged After 2 Weeks

**Description:** AC 03.5 — Boundary Value Analysis (Smoke) — Job records that were created more than 2 weeks ago are automatically removed from the Bulk Action Monitoring page.

**Preconditions:**

- User is logged into SF as a Riso HQ Admin with "Bulk Action Monitoring" permission
- A Bulk Publish job record was created exactly 15 days ago (1 day past the 2-week retention window)
- Another job record was created exactly 14 days ago (at the boundary of retention)

| #   | Action                                                                                         | Expected Result                                                      | Test Data           |
| --- | ---------------------------------------------------------------------------------------------- | -------------------------------------------------------------------- | ------------------- |
| 1   | Navigate to Bulk Action Monitoring; set Created Date filter to show all time or the past month | Page loads with all accessible records                               | ""                  |
| 2   | Search for the record created 15 days ago                                                      | The record is **no longer present** (purged after 2-week retention)  | Record from day -15 |
| 3   | Search for the record created 14 days ago                                                      | The record is **still present** (within the 2-week retention window) | Record from day -14 |

**Severity:** trivial
**Priority:** low

---
