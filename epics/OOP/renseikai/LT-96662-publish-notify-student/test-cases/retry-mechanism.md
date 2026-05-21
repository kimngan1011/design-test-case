# Test Cases: LT-96662 — Publish and Notify Student

## Suite: Publish and Notify Student – Retry Mechanism

### Notification Retry – First Attempt Fails – System retries up to 3 times before stopping

**Description:** AC 02.3 — Negative Testing — When the first notification delivery attempt fails, the system automatically retries up to 3 times with a short delay between attempts before giving up.

> ⚠️ **Note:** This test case requires the ability to simulate a notification delivery failure in the staging/testing environment (e.g., mock or backend tooling). Coordinate with the engineering team to set up the failure scenario.

**Preconditions:**
- User is logged into SF with the "Publish Lesson With Notification" custom permission (member of the Renseikai OOP Permission Set)
- A lesson exists with status = **Published** with Student A assigned
- Notification delivery pipeline is configured to **fail on all attempts** (simulated failure via mock/backend override)
- Access to system logs or admin dashboard to verify retry attempts

| #   | Action | Expected Result | Test Data |
| --- | ------ | --------------- | --------- |
| 1   | Navigate to the SF Lesson Detail page of the Published lesson | Lesson Detail page opens | Published lesson ID |
| 2   | Click "Publish and notify student", then click "Send" | Modal closes without error shown to SF user | "" |
| 3   | On the SF page, observe for any visible failure indicator | No error banner or blocking UI shown to the operator (retry happens silently in background) | "" |
| 4   | In the system audit log / admin dashboard, verify retry attempts | Exactly 3 delivery attempts are logged for this notification event, each marked as failed with a short interval between attempts | System audit log or admin dashboard |
| 5   | Verify no further retry beyond 3 attempts | No 4th attempt is logged; retry loop has stopped | System audit log |

**Severity:** normal
**Priority:** medium

---

### Notification Retry – Retry Succeeds – Only one notification delivered to recipient

**Description:** AC 02.3 — Negative Testing + Regression Analysis — When delivery fails on the first attempt but succeeds on a subsequent retry, the recipient receives exactly one push notification (no duplicates).

> ⚠️ **Note:** Requires simulated failure on attempt 1 and success on attempt 2 via backend tooling.

**Preconditions:**
- User is logged into SF with the "Publish Lesson With Notification" custom permission (member of the Renseikai OOP Permission Set)
- A Published lesson with Student A assigned
- Notification delivery is configured to **fail on attempt 1, succeed on attempt 2**
- Student A is logged into the Learner App on Device 1 with push notifications enabled

| #   | Action | Expected Result | Test Data |
| --- | ------ | --------------- | --------- |
| 1   | Navigate to the SF Lesson Detail page of the Published lesson | Lesson Detail page opens | Published lesson ID |
| 2   | Click "Publish and notify student", then click "Send" | Modal closes | "" |
| 3   | Wait for retry interval to elapse (backend delivers on 2nd attempt) | System completes delivery on attempt 2 | "" |
| 4   | On Device 1, check Student A's Learner App notification inbox | Student A receives **exactly one** push notification with title "Lesson Published" — no duplicate notification present | Student A Learner App account |
| 5   | In the system audit log, verify attempt records | Log shows attempt 1: FAILED, attempt 2: SUCCESS; no further attempts logged | System audit log |

**Severity:** major
**Priority:** high

---

### Notification Retry – All Attempts Logged – Each attempt recorded in system audit log

**Description:** AC 02.3 — Regression Analysis — Every notification delivery attempt (success or failure) is recorded in the system audit log for monitoring and audit purposes.

> ⚠️ **Note:** Smoke test. Requires access to backend logs or admin dashboard.

**Preconditions:**
- User is logged into SF with the "Publish Lesson With Notification" custom permission (member of the Renseikai OOP Permission Set)
- A Published lesson with Student A assigned
- Access to system audit log or admin dashboard

| #   | Action | Expected Result | Test Data |
| --- | ------ | --------------- | --------- |
| 1   | Navigate to the SF Lesson Detail page of the Published lesson | Lesson Detail page opens | Published lesson ID |
| 2   | Click "Publish and notify student", then click "Send" | Modal closes; notification delivered successfully on first attempt | "" |
| 3   | In the system audit log, locate the log entry for this notification event | A log entry exists for the notification attempt with status SUCCESS, timestamp, lesson ID, and recipient ID | System audit log |

**Severity:** normal
**Priority:** medium

---

### Notification Retry – All 3 Attempts Fail – Failure event logged in system

**Description:** AC 02.3 — Negative Testing — When all 3 delivery attempts fail, a clear failure event is logged in the error log or admin dashboard for monitoring and incident response.

> ⚠️ **Note:** Requires simulated failure on all 3 attempts via backend tooling. Verify the failure log is visible to the engineering/ops team.

**Preconditions:**
- User is logged into SF with the "Publish Lesson With Notification" custom permission (member of the Renseikai OOP Permission Set)
- A Published lesson with Student A assigned
- Notification delivery pipeline is configured to **fail on all 3 attempts** (simulated failure)
- Access to system error log or admin dashboard

| #   | Action | Expected Result | Test Data |
| --- | ------ | --------------- | --------- |
| 1   | Navigate to the SF Lesson Detail page of the Published lesson | Lesson Detail page opens | Published lesson ID |
| 2   | Click "Publish and notify student", then click "Send" | Modal closes; no error shown to SF user in the UI | "" |
| 3   | Wait for all 3 retry attempts to complete (based on configured delay intervals) | No notification is delivered to the recipient device | "" |
| 4   | In the system error log / admin dashboard, locate the failure record for this event | A clear failure log entry exists indicating all 3 attempts failed; log includes lesson ID, recipient ID, and failure reason for each attempt | System error log / admin dashboard |

**Severity:** normal
**Priority:** medium

---
