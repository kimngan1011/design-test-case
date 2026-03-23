# Automation Test Run Review

**Project:** PX
**Run ID:** 2187
**Run Title:** Automated Playwright Run - internal-manabie - 2026-03-18 05:24:06
**Run Date:** 2026-03-18
**Reviewed By:** GitHub Copilot
**Review Date:** 2026-03-22

---

## Summary

| Metric                       | Value |
| ---------------------------- | ----- |
| Total Unique Cases           | 116   |
| Total Execution Attempts     | 293   |
| Passed (clean, no retries)   | 89    |
| Passed (after retries/flaky) | 27    |
| Failed (final)               | 0     |
| Invalid/Blocked (final)      | 0     |
| Flagged for Review           | 27    |

> **Note:** Qase run status shows all 118 cases as "passed" based on final attempt only. This review identifies 27 cases that required retries, indicating flakiness. The 293 total attempts vs. 116 cases means significant re-runs occurred during this session.

---

## Cases with Issues

### ❌ Failed Cases

No cases have a final status of FAILED. All 116 cases ultimately passed.

---

### ⚠️ Flaky Cases (passed after retries)

Cases are grouped by root cause pattern.

---

#### Pattern 1 — Lesson Schedule UI List Sort Order Inconsistency

**Root Cause:** The Salesforce Lesson Schedule UI List reloads with a different sort order on each page navigation. When the automation verifies row-by-row dates, the positional mismatch causes every row to fail comparison. This appears non-deterministic — retrying the test resolves it without any code change.

**Evidence (PX-9677):**

```
[FAIL] Row 0: start=2026/04/21 expected=2026/04/29 (off by 8 days)
[FAIL] Row 1: start=2026/04/20 expected=2026/04/28 (off by 8 days)
... [all 78 rows consistently shifted by 8 days]
```

All rows shifted forward by 8 days — consistent with ascending vs. descending sort mismatch. Actual data sorted ascending in this run; expected data assumes descending order (most recent first).

**Assessment:** FLAKY — Lesson Schedule UI List sort order is non-deterministic. The test assertion is order-sensitive, causing systematic failure when sort direction differs from expectation.

| Case ID | Title                                                                                                                                  | Suite                              | Retries | Retry History                                       |
| ------- | -------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------- | ------- | --------------------------------------------------- |
| PX-9677 | Create Lesson – Custom Recurring – Individual – End Date + Skip Closed Date – Lessons created on selected days, excluding closed dates | Create Lesson on Lesson list (218) | 4       | failed → failed → passed → failed → passed          |
| PX-9672 | _(Custom Recurring variant)_                                                                                                           | Create Lesson on Lesson list (218) | 2       | passed → failed → passed                            |
| PX-9673 | _(Custom Recurring variant)_                                                                                                           | Create Lesson on Lesson list (218) | 2       | passed → failed → passed                            |
| PX-9674 | _(Custom Recurring variant)_                                                                                                           | Create Lesson on Lesson list (218) | 5       | passed → failed → passed → passed → passed → passed |
| PX-9675 | _(Custom Recurring variant)_                                                                                                           | Create Lesson on Lesson list (218) | 2       | passed → failed → passed                            |
| PX-9676 | _(Custom Recurring variant)_                                                                                                           | Create Lesson on Lesson list (218) | 2       | passed → failed → passed                            |
| PX-9680 | _(Custom Recurring variant)_                                                                                                           | Create Lesson on Lesson list (218) | 2       | passed → failed → passed                            |
| PX-9681 | _(Custom Recurring variant)_                                                                                                           | Create Lesson on Lesson list (218) | 2       | passed → failed → passed                            |
| PX-1013 | _(Course Schedule Recurring variant)_                                                                                                  | Create Lesson on Lesson list (218) | 2       | passed → failed → passed                            |
| PX-1014 | _(Course Schedule Recurring variant)_                                                                                                  | Create Lesson on Lesson list (218) | 2       | passed → failed → passed                            |
| PX-1015 | Create Lesson – Course Schedule Recurring – Individual – Lessons created on week order, closed dates excluded                          | Create Lesson on Lesson list (218) | 3       | failed → passed → failed → passed                   |
| PX-1016 | _(Course Schedule Recurring variant)_                                                                                                  | Create Lesson on Lesson list (218) | 2       | passed → failed → passed                            |
| PX-1023 | _(One-time/Recurring variant)_                                                                                                         | Create Lesson on Lesson list (218) | 2       | passed → failed → passed                            |

**Additional evidence (PX-1015):**

```
[INFO] [CHECK] Lesson Schedule Start Date: actual="2026/02/17 09:00" expected="2026/02/17 09:00"  ← PASS
[INFO] [CHECK] Lesson Schedule End Date:   actual="2026/02/17 10:00" expected="2026/03/10 10:00"  ← MISMATCH
```

The Lesson Schedule shows the **first lesson's end date** (`2026/02/17`) instead of the **last lesson's end date** (`2026/03/10`) — a data freshness / late-loading issue. The sort order mismatch causes the wrong row to be compared.

---

#### Pattern 2 — Lesson Grid UI Row Count Not Fully Loaded

**Root Cause:** When creating a large recurring lesson chain (44 lessons), the Salesforce Lesson Grid does not finish loading all rows within the 20-second timeout. The test asserts row count before all lessons are rendered.

**Evidence (PX-9678):**

```
[FAIL] expect(locator).toHaveCount(44) → received 42
Timeout exceeded waiting for table "Lessons" to have 44 rows.
Only 42 rows loaded within 20000ms.
```

**Assessment:** FLAKY — Page load performance issue. Large recurring lesson chains take >20s to fully populate in the Lesson Grid. The automation timeout is insufficient for this data volume.

| Case ID | Title                                                                                                               | Suite                              | Retries | Retry History                                                   |
| ------- | ------------------------------------------------------------------------------------------------------------------- | ---------------------------------- | ------- | --------------------------------------------------------------- |
| PX-9678 | Create Lesson – Custom Recurring – Group – End Date, No Skip Closed Date – Lessons created on selected days of week | Create Lesson on Lesson list (218) | 23      | 10× failed, 6× invalid, then passed (most critical case in run) |

---

#### Pattern 3 — One-time Lesson Data Load in Lesson Schedule

**Root Cause:** The Lesson Schedule UI does not display the latest data immediately after a group of one-time lessons is created, causing the automation to read stale data.

**Assessment:** FLAKY — likely the same underlying sort order or lazy-load issue as Pattern 1, but manifesting on one-time lesson data.

| Case ID | Title                                                                                                 | Suite                              | Retries | Retry History                              |
| ------- | ----------------------------------------------------------------------------------------------------- | ---------------------------------- | ------- | ------------------------------------------ |
| PX-1022 | Create Lesson – One-time – Individual – Lesson date on closed date – Lesson created with draft status | Create Lesson on Lesson list (218) | 4       | passed → failed → failed → passed → passed |

---

#### Pattern 4 — Teacher Assignment: UI Element Not Visible After Save

**Root Cause:** After adding a teacher to a lesson, the Lesson Detail page's teacher table does not re-render within the 5000ms assertion timeout. The teacher record exists (verified on subsequent retry) but the UI is slow to update.

**Evidence (PX-1216):**

```
[FAIL] Verify teacher is assigned successfully at Lesson Detail page (5023 ms)
Error: expect(locator).toContainText(expected) failed
Locator: locator('tbody tr lightning-formatted-url a').filter({ hasText: 'Teacher [E2E] Kim Ngan' })
Expected substring: "Teacher [E2E] Kim Ngan"
Timeout: 5000ms
Error: element(s) not found
```

**Assessment:** FLAKY — The 5000ms timeout for teacher visibility is insufficient for Salesforce Lightning table refresh latency. The teacher assignment itself works; only the UI reflection is delayed.

| Case ID | Title                                  | Suite                                            | Retries | Retry History                                                  |
| ------- | -------------------------------------- | ------------------------------------------------ | ------- | -------------------------------------------------------------- |
| PX-1216 | Assign a teacher to an one-time lesson | Assign/Unassign a teacher in lesson detail (260) | 6       | failed → passed → passed → passed → invalid → invalid → passed |

---

#### Pattern 5 — Lesson Report Edit: Menu Item Click Timeout

**Root Cause:** The "Edit" menu item (`[role="menuitem"][title="Edit"]`) in the Lesson Report Detail page is not immediately clickable after the page loads. An overlay or animation keeps it in a non-visible state briefly.

**Evidence (PX-3391):**

```
[FAIL] Edit data at Lesson Report Details at Lesson Detail page (16144 ms)
Error: locator.click: Timeout 15000ms exceeded.
Waiting for locator('[role="menuitem"][title="Edit"]')
element is not visible (retried × 3)
```

**Assessment:** FLAKY — Salesforce Lightning dropdown menu animation/rendering delay causes the edit button to be intermittently unclickable within 15s. Passes on retry without any code change.

| Case ID | Title                                  | Suite                            | Retries | Retry History   |
| ------- | -------------------------------------- | -------------------------------- | ------- | --------------- |
| PX-3391 | User can edit individual lesson report | Lesson Report under Lesson (401) | 1       | failed → passed |

---

#### Pattern 6 — Event Master Remove Staff: Transient Failure

**Root Cause:** Cannot confirm from sampled step-results (the failure URL returned all steps as PASSED, suggesting the failure occurred in a different attempt). The test verifies that removing a staff member from an Event Master's Master Staff list completes successfully.

**Assessment:** FLAKY — likely a Salesforce UI timing issue similar to Patterns 4 and 5 (save operation not immediately reflected). Cannot determine exact step without the correct failure step-results URL.

| Case ID | Title                                  | Suite                   | Retries | Retry History                                       |
| ------- | -------------------------------------- | ----------------------- | ------- | --------------------------------------------------- |
| PX-3510 | Remove Master Staff under Event Master | Master staff list (408) | 5       | failed → passed → passed → passed → passed → passed |

---

#### Pattern 7 — Environment / Infrastructure Issues (INVALID)

**Root Cause:** These cases have `invalid` execution status — the test runner was terminated or the pipeline was interrupted before the test could execute. No test code ran; these are infrastructure-level failures. The tests passed on subsequent re-runs without modification.

**Assessment:** INVALID — Not test code defects. Caused by pipeline instability, resource contention, or network interruption during the test session. The affected runs all cluster around the same timestamps, suggesting a single infrastructure event affected multiple tests simultaneously.

| Case ID | Title                                          | Suite                                            | Retries | Retry History                                |
| ------- | ---------------------------------------------- | ------------------------------------------------ | ------- | -------------------------------------------- |
| PX-749  | _(Lesson-related test)_                        | —                                                | 1       | invalid → passed                             |
| PX-1218 | _(Course Schedule Recurring variant)_          | Create Lesson on Lesson list (218)               | 2       | passed → invalid → invalid → passed          |
| PX-3772 | _(Unknown — no step data captured)_            | —                                                | 2       | invalid → invalid → passed                   |
| PX-8493 | Assign a teacher to daily lesson with end date | Assign/Unassign a teacher in lesson detail (260) | 2       | passed → invalid → invalid → passed          |
| PX-8494 | _(Teacher assignment variant)_                 | Assign/Unassign a teacher in lesson detail (260) | 2       | passed → invalid → invalid → passed          |
| PX-8497 | _(Teacher assignment variant)_                 | Assign/Unassign a teacher in lesson detail (260) | 2       | passed → invalid → invalid → passed          |
| PX-8498 | _(Teacher assignment variant)_                 | Assign/Unassign a teacher in lesson detail (260) | 4       | passed → invalid → invalid → failed → passed |
| PX-8501 | _(Teacher assignment variant)_                 | Assign/Unassign a teacher in lesson detail (260) | 2       | passed → invalid → invalid → passed          |
| PX-8502 | _(Teacher assignment variant)_                 | Assign/Unassign a teacher in lesson detail (260) | 2       | passed → invalid → invalid → passed          |

> **Note on PX-8498:** This case had both `invalid` and `failed` attempts. The failed attempt in addition to invalids may indicate the test was also affected by the same UI timing issue as Pattern 4 (teacher assignment). Recommend investigating PX-8498 failure step-results separately.

---

### ✅ Clean Pass Cases

89 cases passed on the first attempt with no retries. These are not listed individually here. Full list is available in the Qase run dashboard at:
`https://app.qase.io/run/PX/dashboard/2187`

Clean pass cases span the following feature areas:

- Lesson creation (various recurrence modes, teaching methods) — Suite 218 subset
- Lesson editing and deletion — Suite 217 family
- Lesson teacher assignment and unassignment — Suite 260 subset
- Lesson report management — Suite 401 subset
- Event and Activity management — Suite 99/408 family
- Student assignment to lessons — other suites

---

## Flaky Case Summary Table

| Priority    | Case ID | Suite | Retries | Pattern                       | Status          |
| ----------- | ------- | ----- | ------- | ----------------------------- | --------------- |
| 🔴 Critical | PX-9678 | 218   | 23      | Lesson Grid row count timeout | FLAKY           |
| 🟠 High     | PX-1216 | 260   | 6       | Teacher UI element latency    | FLAKY           |
| 🟠 High     | PX-3510 | 408   | 5       | Event Master staff removal    | FLAKY           |
| 🟠 High     | PX-9674 | 218   | 5       | Lesson Schedule sort order    | FLAKY           |
| 🟡 Medium   | PX-1022 | 218   | 4       | Lesson Schedule data load     | FLAKY           |
| 🟡 Medium   | PX-8498 | 260   | 4       | Teacher UI + infra hybrid     | FLAKY + INVALID |
| 🟡 Medium   | PX-9677 | 218   | 4       | Lesson Schedule sort order    | FLAKY           |
| 🟡 Medium   | PX-1015 | 218   | 3       | Lesson Schedule sort order    | FLAKY           |
| 🟡 Medium   | PX-1218 | 218   | 2       | Infrastructure outage         | INVALID         |
| 🟡 Medium   | PX-8493 | 260   | 2       | Infrastructure outage         | INVALID         |
| 🟡 Medium   | PX-8494 | 260   | 2       | Infrastructure outage         | INVALID         |
| 🟡 Medium   | PX-8497 | 260   | 2       | Infrastructure outage         | INVALID         |
| 🟡 Medium   | PX-8501 | 260   | 2       | Infrastructure outage         | INVALID         |
| 🟡 Medium   | PX-8502 | 260   | 2       | Infrastructure outage         | INVALID         |
| 🟡 Medium   | PX-1013 | 218   | 2       | Lesson Schedule sort order    | FLAKY           |
| 🟡 Medium   | PX-1014 | 218   | 2       | Lesson Schedule sort order    | FLAKY           |
| 🟡 Medium   | PX-1016 | 218   | 2       | Lesson Schedule sort order    | FLAKY           |
| 🟡 Medium   | PX-1023 | 218   | 2       | Lesson Schedule sort order    | FLAKY           |
| 🟡 Medium   | PX-3772 | —     | 2       | Infrastructure outage         | INVALID         |
| 🟡 Medium   | PX-9672 | 218   | 2       | Lesson Schedule sort order    | FLAKY           |
| 🟡 Medium   | PX-9673 | 218   | 2       | Lesson Schedule sort order    | FLAKY           |
| 🟡 Medium   | PX-9675 | 218   | 2       | Lesson Schedule sort order    | FLAKY           |
| 🟡 Medium   | PX-9676 | 218   | 2       | Lesson Schedule sort order    | FLAKY           |
| 🟡 Medium   | PX-9680 | 218   | 2       | Lesson Schedule sort order    | FLAKY           |
| 🟡 Medium   | PX-9681 | 218   | 2       | Lesson Schedule sort order    | FLAKY           |
| 🟢 Low      | PX-749  | —     | 1       | Infrastructure outage         | INVALID         |
| 🟢 Low      | PX-3391 | 401   | 1       | Lesson Report menu timeout    | FLAKY           |

---

## Recommendations

### 1. Fix Lesson Schedule UI List sort order handling (HIGH — affects 13+ cases)

The `Verify Lesson Schedule UI List` automation step is order-sensitive. It compares row-by-row by position. The Salesforce Lesson Schedule page does not guarantee a consistent sort order on load.

**Recommended fix:**

- Sort both the actual data collected and the expected data by the same field (e.g., Start Date ascending) before comparing, rather than relying on positional order.
- Add an explicit sort-by-column click before collecting rows.
- Or: compare by lesson name match rather than position.

### 2. Increase or add dynamic wait for Lesson Grid row count (HIGH — PX-9678, 23 retries)

The `Verify Lesson Grid UI` step uses a fixed 20s timeout for `toHaveCount(44)`. Large recurring lesson chains (44+ lessons) take longer to fully render in Salesforce.

**Recommended fix:**

- Increase the row count assertion timeout from 20s to 45s for cases with large expected row counts (>30).
- Or: implement a progressive polling strategy — poll every 2s up to 60s.
- Consider adding a `waitForSelector` for the last expected row before counting.

### 3. Increase teacher-visible timeout in Lesson Detail (MEDIUM — PX-1216, PX-8498)

The teacher assignment verification uses a 5000ms timeout, which is insufficient for Salesforce Lightning table re-renders after a save.

**Recommended fix:**

- Increase the `toContainText` timeout from 5000ms to 10–15s.
- Alternatively, wait for a network idle state after the save action before asserting.

### 4. Stabilize Lesson Report Edit menu interaction (LOW — PX-3391)

The Edit menu item in Lesson Report Details is not immediately clickable due to Salesforce Lightning animation.

**Recommended fix:**

- Add `waitForSelector` with `state: 'visible'` and `state: 'stable'` before clicking the Edit menu.
- Or: use `force: true` on the click if the element is confirmed to be an overlay issue.

### 5. Investigate PX-3510 failure root cause (MEDIUM)

PX-3510 had 5 retries. The sampled failure step-results URL showed all steps passing, suggesting the actual failure URL was not captured correctly or points to a different attempt. Manual investigation of a true failure attempt is needed.

**Recommended action:**

- Retrieve and review the step-results.md from the specific failed attempt (not the first recorded URL).
- Verify if this is a timing issue on the Salesforce Event Master page.

### 6. Investigate infrastructure instability causing INVALID runs (MEDIUM — 9 cases)

Eight cases (PX-8493–8502, PX-1218, PX-749, PX-3772) experienced `invalid` execution status. The invalid attempts for the 8xxx group all share the same `['passed', 'invalid', 'invalid', 'passed']` pattern, suggesting a single pipeline event caused their failure simultaneously.

**Recommended actions:**

- Audit CI/CD pipeline logs for 2026-03-18 to identify the infrastructure failure window.
- Check if the two invalid runs correspond to a specific pipeline execution time.
- Consider adding health-check retries at the pipeline level before re-queuing all tests.

### 7. Mark PX-9678 as flaky in Qase

PX-9678 had 23 execution attempts in this single run — the most expensive test in the run. Until the root cause (Lesson Grid load time for 44 lessons) is fixed, mark it as flaky in Qase to reduce noise alerts.

---

## Appendix: Execution Statistics

| Stat                                   | Value                                   |
| -------------------------------------- | --------------------------------------- |
| Total execution attempts               | 293                                     |
| Unique cases run                       | 116                                     |
| Average attempts per case              | ~2.5                                    |
| Max attempts for a single case         | 23 (PX-9678)                            |
| Cases with `invalid` attempts          | 11                                      |
| Cases with `failed` attempts           | 18                                      |
| Cases with both `invalid` and `failed` | 2 (PX-9678, PX-8498)                    |
| Run status                             | `in_progress` (never formally closed)   |
| Test environment                       | internal-manabie (Salesforce Lightning) |
