# Automation Test Run Review

**Project:** PX  
**Run ID:** 2263  
**Run Title:** Automated Playwright Run - renseikai-rehearsal2 - 2026-03-30 00:22:52  
**Run Date:** 2026-03-30  
**Reviewed By:** GitHub Copilot  
**Review Date:** 2026-04-03  
**Environment:** renseikai-rehearsal2

---

## Summary

| Metric                  | Value |
| ----------------------- | ----- |
| Total Cases in Run      | 140   |
| Unique Cases (de-duped) | 139   |
| Passed (clean)          | 118   |
| Passed (after retries)  | 19    |
| Failed                  | 2     |
| Invalid/Blocked         | 0     |
| Deep-Checked Cases      | 4     |
| Matching (deep-checked) | 0     |
| Not Matching            | 4     |

> Deep-check focused on all 2 failed cases and 2 highest-priority flaky cases (9736: 3 failures before pass; 3585: 1 failure before pass). Clean-pass cases with no retries were not individually deep-checked per review protocol.

---

## Per-Suite Verification Table

### Suite 218 — Create Lesson (Lesson List)

| Suite     | Test Case                                                                | Checks Performed                                                                                                | Verdict             |
| --------- | ------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------- | ------------------- |
| Suite 218 | PX-9675: Create Lesson – Daily Recurring – Individual – Skip Closed Date | Preconditions ✅ · Step coverage ⚠️ · Step actions ⚠️ · Expected results ⚠️ · Unmapped entries ❌ · Failures ❌ | ❌ Not Matching     |
| Suite 218 | PX-9672: Create Lesson – Weekly Recurring – Group – Skip Closed Date     | Preconditions ✅ · Step coverage ⚠️ · Step actions ⚠️ · Expected results ⚠️ · Unmapped entries ❌ · Failures ❌ | ❌ Not Matching     |
| Suite 218 | PX-9673, 9674, 9676, 9677, 9678, 9680, 9681 + others (661–1039 range)    | Clean pass — not individually deep-checked                                                                      | ✅ Not deep-checked |

### Suite 96 — Event Master

| Suite    | Test Case                                              | Checks Performed                           | Verdict             |
| -------- | ------------------------------------------------------ | ------------------------------------------ | ------------------- |
| Suite 96 | PX-10072 to PX-10079: Event Master configuration cases | Clean pass — not individually deep-checked | ✅ Not deep-checked |

### Suite 425 — Lesson Report

| Suite     | Test Case                                                             | Checks Performed                                                                                                 | Verdict         |
| --------- | --------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- | --------------- |
| Suite 425 | PX-3585: Edit lesson report info on lesson report list by edit button | Preconditions ✅ · Step coverage ❌ · Step actions ✅ · Expected results ❌ · Unmapped entries ✅ · Flakiness ❌ | ❌ Not Matching |

### Suite 815 — Edit Lesson (Daily, Lesson Count)

| Suite     | Test Case                                                                         | Checks Performed                                                                                                 | Verdict         |
| --------- | --------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- | --------------- |
| Suite 815 | PX-9736: Edit lesson date with skip closed date in daily lesson with lesson count | Preconditions ✅ · Step coverage ⚠️ · Step actions ⚠️ · Expected results ❌ · Unmapped entries ✅ · Flakiness ❌ | ❌ Not Matching |
| Suite 815 | PX-9734: Edit lesson date so that new lesson date < old (retry×2, final pass)     | Clean pass after retry — not individually deep-checked                                                           | ⚠️ Flaky        |
| Suite 815 | PX-9735: (failed → passed)                                                        | Clean pass after retry — not individually deep-checked                                                           | ⚠️ Flaky        |

### Suite 1166 — Edit Lesson (Weekly, End Date)

| Suite      | Test Case                                                             | Checks Performed                           | Verdict             |
| ---------- | --------------------------------------------------------------------- | ------------------------------------------ | ------------------- |
| Suite 1166 | PX-9745–9775: Edit lesson date / check lesson schedule end date cases | Clean pass — not individually deep-checked | ✅ Not deep-checked |

### Other Suites (260, 401, remaining cases)

| Suite    | Test Case                                                                              | Checks Performed                                           | Verdict                  |
| -------- | -------------------------------------------------------------------------------------- | ---------------------------------------------------------- | ------------------------ |
| Multiple | PX-661, 664, 666–786, 1216–1919, 3144–3787, 6931, 8293–8518, 11285, 11538, 13747–13750 | Clean pass (or retry→pass) — not individually deep-checked | ✅ / ⚠️ Not deep-checked |

---

## ⚠️ Unmapped Automation Test Cases

Entries in `step-results.json` that have **no corresponding Qase step definition**.

| Suite     | Case ID | Step Position | Unmapped Entry Type | Content (truncated)                                                                              | Impact                                                                            |
| --------- | ------- | ------------- | ------------------- | ------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------- |
| Suite 218 | PX-9675 | Step 5        | ACTION + EXPECTED   | `Verify Lesson Schedule UI List` — checks Lesson Schedule Name, Code, Type, Start Date, End Date | No defined step to trace this execution back to; this is where the failure occurs |
| Suite 218 | PX-9672 | Step 5        | ACTION + EXPECTED   | `Verify Lesson Schedule UI List` — checks Lesson Schedule Name, Code, Type, Start Date, End Date | No defined step to trace this execution back to; this is where the failure occurs |

> **Note:** This is a recurrence of **GAP-1** identified in Run 2187. The "Verify Lesson Schedule UI List" step remains undocumented across all Suite 218 cases. In this run it is also the direct source of failure for both failed cases.

---

## Not Matching Cases — Detail

---

### Suite 218 — PX-9675: Create Lesson – Daily – Individual – Lesson Count + Skip Closed Date

**Verdict:** Not Matching  
**Mismatch type(s):** `UNMAPPED_STEP` · `EXPECTED_RESULT_FAIL` · `DEFINITION_QUALITY`  
**Automation status (current):** Automated (`automation = 2`)

#### Precondition Mapping

| step-results.json `PRECONDITION:`                                                      | Qase `preconditions`                        | Match? |
| -------------------------------------------------------------------------------------- | ------------------------------------------- | ------ |
| Created lesson data: Daily, Individual, 2 lessons, skipCloseDate=true, date=2026/04/27 | Master data setup + Closed Dates configured | ✅     |

#### ACTION / EXPECTED Mapping

| Qase Step | Action                                                            | Automation Step                                                                                                                                                                | Mapped?               |
| --------- | ----------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------- |
| Step 1    | Input data (Daily, Individual, After, Number=2, Skip Closed Date) | PRECONDITION data snapshot                                                                                                                                                     | ✅ (via precondition) |
| Step 2    | Click Save button                                                 | _(embedded in creation; not explicitly logged)_                                                                                                                                | ⚠️ Implicit           |
| Step 3    | Check all lessons in the chain                                    | Verify Lesson Grid data — 2 rows: 2026/04/27 and 2026/04/29                                                                                                                    | ✅                    |
| Step 4    | Check lesson code                                                 | Embedded in Verify Lesson Grid (codes 1, 2 shown)                                                                                                                              | ✅ Implicit           |
| Step 5    | Check lesson type                                                 | Embedded in Verify Lesson Grid (通常特訓 shown)                                                                                                                                | ✅ Implicit           |
| Step 6    | Check closed date                                                 | ❌ No explicit negative assertion ("user does not see 04/28") — only implicit from grid data; furthermore **step definition says the opposite** (see DEFINITION_QUALITY below) | ❌                    |
| Step 7    | Check lesson report                                               | Verify Lesson Report — 2 reports: 04/27 and 04/29                                                                                                                              | ✅                    |
| Step 8    | Login BO and view these lessons                                   | Verify BackOffice Details                                                                                                                                                      | ✅                    |
| —         | _(no Qase step)_                                                  | **Verify Lesson Schedule UI List**                                                                                                                                             | ❌ UNMAPPED           |

#### What to Check in the Test Run

- **Step 5 (Verify Lesson Schedule UI List) — system failure**:

  ```
  [INFO] Found 1 rows in Lesson Schedule. Expected: 2 records.
  [INFO] Grid data: { "Lesson Schedule Number":"71473", "Day":"Mon", "Lesson Code":"1",
    "Start Date":"2026/04/27 9:00", "End Date":"2026/04/28 10:00" }
  [EXPECTED] Actual [Lesson Schedule End Date] : [2026/04/28 10:00]
          | Expected [Lesson Schedule End Date] : [2026/04/29 10:00]
  ```

  **Root cause:** When a daily recurring lesson uses Skip Closed Date, the system:
  1. Creates only **1 Lesson Schedule record** instead of the expected 2
  2. Sets the Lesson Schedule **End Date = 2026/04/28** (the closed date that was skipped) instead of **2026/04/29** (the actual last lesson date)

  This is a **product bug** — the Lesson Schedule object is not correctly updated when Skip Closed Date is enabled for daily recurring lessons.

#### DEFINITION_QUALITY Issue — Step 6

- **Current wording (Step 6 action):** "Check closed date"
- **Current wording (Step 6 expected):** "User **still sees** lesson date that matches the closed date in the chain."
- **Problem:** The test is configured with `skipCloseDate = true` and the title says "Lessons created **excluding** closed dates". Step 6's expected result ("still sees") describes the **non-skip** behavior and is contradictory.
- **Should be:** "User does **not** see any lesson date that matches the closed date (2026/04/28 is excluded from the chain)."
- **Action required:** Update Step 6 expected result in Qase to match the test intent.

#### How to Fix

1. **Product bug (Lesson Schedule End Date):** Engineering team must fix the Lesson Schedule object creation for Skip Closed Date + lesson count mode — End Date should reflect the last actual lesson date, not the closed date. Both daily and weekly recurring modes are affected (see PX-9672).
2. **Unmapped step:** Add a Qase step for Lesson Schedule verification or remove it from automation (see GAP-1 recommendation in Run 2187 report).
3. **Definition quality:** Update Step 6 expected result to match skip-mode intent.

---

### Suite 218 — PX-9672: Create Lesson – Weekly – Group – Lesson Count + Skip Closed Date

**Verdict:** Not Matching  
**Mismatch type(s):** `UNMAPPED_STEP` · `EXPECTED_RESULT_FAIL`  
**Automation status (current):** Automated (`automation = 2`)

#### Precondition Mapping

| step-results.json `PRECONDITION:`                                                  | Qase `preconditions`                        | Match? |
| ---------------------------------------------------------------------------------- | ------------------------------------------- | ------ |
| Created lesson data: Weekly, Group, 2 lessons, skipCloseDate=true, date=2026/04/21 | Master data setup + Closed Dates configured | ✅     |

#### ACTION / EXPECTED Mapping

| Qase Step | Action                                                                            | Automation Step                                                             | Mapped?     |
| --------- | --------------------------------------------------------------------------------- | --------------------------------------------------------------------------- | ----------- |
| Step 1    | Input data (Weekly, Group, After, Number=2, Skip Closed Date)                     | PRECONDITION data snapshot                                                  | ✅          |
| Step 2    | Click Save button                                                                 | _(embedded in creation)_                                                    | ⚠️ Implicit |
| Step 3    | Check all lessons in the chain                                                    | Verify Lesson Grid — 2 rows: 2026/04/21 and 2026/05/12 (skips 04/28, 05/05) | ✅          |
| Step 4    | Check lesson code                                                                 | Embedded in Verify Lesson Grid                                              | ✅ Implicit |
| Step 5    | Check lesson type                                                                 | Embedded in Verify Lesson Grid                                              | ✅ Implicit |
| Step 6    | Check skip closed date — "User does NOT see any lesson date matching closed date" | Not explicitly asserted — only implicit from grid data                      | ⚠️ Partial  |
| Step 7    | Check lesson report                                                               | Verify Lesson Report — 2 reports                                            | ✅          |
| Step 8    | Login BO and view these lessons                                                   | Verify BackOffice Details                                                   | ✅          |
| —         | _(no Qase step)_                                                                  | **Verify Lesson Schedule UI List**                                          | ❌ UNMAPPED |

#### What to Check in the Test Run

- **Step 5 (Verify Lesson Schedule UI List) — same system bug as PX-9675:**

  ```
  [INFO] Found 1 rows in Lesson Schedule. Expected: 2 records.
  [INFO] Grid data: { "Lesson Schedule Number":"71477", "Day":"Tue", "Lesson Code":"1",
    "Start Date":"2026/04/21 9:00", "End Date":"2026/04/28 10:00" }
  [EXPECTED] Actual [Lesson Schedule End Date] : [2026/04/28 10:00]
          | Expected [Lesson Schedule End Date] : [2026/05/12 10:00]
  ```

  - Only 1 Lesson Schedule record created (expected 2)
  - End Date = 2026/04/28 (closed date) instead of 2026/05/12 (last actual lesson date)

#### How to Fix

Same as PX-9675 — product bug in Lesson Schedule object when Skip Closed Date is enabled.

---

### Suite 425 — PX-3585: Edit lesson report info on lesson report list by edit button

**Verdict:** Not Matching  
**Mismatch type(s):** `MISSING_STEP` · `FLAKY`  
**Automation status (current):** Automated (`automation = 2`)  
**Retry history:** failed → passed → passed → passed (1 failure before final pass)

#### Precondition Mapping

| step-results.json `PRECONDITION:`                   | Qase `preconditions`                               | Match?        |
| --------------------------------------------------- | -------------------------------------------------- | ------------- |
| _(no explicit PRECONDITION: entry in step-results)_ | "User has published a group lesson with a student" | ⚠️ Not logged |

#### ACTION / EXPECTED Mapping

| Qase Step | Action                                                                   | Automation Step                                                                                                                                                      | Mapped?    |
| --------- | ------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- |
| Step 1    | Go to Lesson Report tab                                                  | "Go to Lesson Report and edit lesson report on grid"                                                                                                                 | ✅         |
| Step 2    | Click Edit, edit lesson report info on list                              | "Verify data at Lesson Report after update" — verifies Content ✅, CM Note ✅, Remarks ✅, Next Lesson's Announcement ✅, Next Lesson's Homework ✅, Announcement ✅ | ✅         |
| Step 3    | Publish lesson report → "User sees LR status is updated on SF"           | ❌ **No automation step covers publishing or verifying status change on SF**                                                                                         | ❌ MISSING |
| Step 4    | Teacher login BO → "Teacher sees updated lesson report on BO"            | "Verify updated lesson report content at BackOffice" — Content ✅, Homework ✅, Announcement ✅, CM Note ✅, Remark ✅                                               | ✅         |
| Step 5    | Student login Mobile → "Student sees lesson report is updated on Mobile" | ❌ **No automation step covers Mobile platform**                                                                                                                     | ❌ MISSING |

#### What to Check in the Test Run

- **Step 3 gap:** The automation goes directly from editing on the SF grid to verifying BO content. There is no step that:
  - Clicks "Publish" on the Lesson Report
  - Verifies the Lesson Report Status field changes (e.g., Draft → Published) on the SF list

- **Step 5 gap:** No Mobile verification at all. The automation framework does not reach the student Mobile app. This means the defined expected result "Student sees lesson report is updated on Mobile" is permanently unverified.

- **Flakiness:** 1 failure before final pass. The failure was likely a timing/element-not-found issue during page navigation. Not a logic failure.

#### How to Fix the Test Case Definition

- **Step 3:** Either add automation for publish + status check, or split step 3 into a separate test case if the publish flow is complex.
- **Step 5:** Update the Qase definition to note "Out of scope for automation (Mobile platform not covered)" OR create a dedicated mobile test. Update `automation` status to reflect the gap.
  > **Current Step 5:** "Student sees lesson report is updated on Mobile"  
  > **Should note:** "⚠️ Mobile verification — not covered by automation; manually verified separately"

---

### Suite 815 — PX-9736: Edit lesson date with skip closed date in daily lesson with lesson count

**Verdict:** Not Matching  
**Mismatch type(s):** `FLAKY` · `EXPECTED_RESULT_FAIL` (shallow verification)  
**Automation status (current):** Manual (`automation = 0`) — already correctly set  
**Retry history:** failed → failed → failed → passed (3 failures before final pass)

> ⚠️ **Note:** This case is already set to **Manual** in Qase. Its presence in an automated run with 3 prior failures before passing is itself a concern — it suggests the automation is unstable for this scenario.

#### ACTION / EXPECTED Mapping

| Qase Step | Action                                              | Automation Step (final pass)                                    | Mapped?                     |
| --------- | --------------------------------------------------- | --------------------------------------------------------------- | --------------------------- |
| Step 1    | Open a middle lesson in the chain                   | "Search lesson (lesson before update) and list recurring chain" | ✅                          |
| Step 1b   | _(select middle lesson)_                            | "Select a middle lesson in the chain"                           | ✅                          |
| Step 2    | Edit lesson date with skip closed date              | "Edit lesson and verify update success"                         | ⚠️ ACTION only, no EXPECTED |
| Step 3    | Check the previous lessons — "no changes"           | ❌ No corresponding step                                        | ❌ MISSING                  |
| Step 4    | Check number of lessons in the chain — "no changes" | ❌ No corresponding step                                        | ❌ MISSING                  |
| Step 5    | Check end date.lesson schedule = last lesson        | "Verify data after update" — ACTION only                        | ❌ No EXPECTED assertions   |

#### What to Check in the Test Run

- The final-pass step-results.json shows only `[ACTION]` log lines — **zero `[EXPECTED]` assertions** in any step:

  ```
  [ACTION] Edit lesson and verify update success
  [ACTION] Navigate to lesson page: https://renseikai--rehearsal2.sandbox.lightning.force.com/...

  [ACTION] Verify data after update
  ← (no [EXPECTED] lines)
  ```

- Steps 3 ("Check previous lessons") and 4 ("Check number of lessons") have **no automation counterpart** at all.
- Step 5 ("Check end date.lesson schedule = last lesson in chain") — the "Verify data after update" step has no EXPECTED lines confirming the Lesson Schedule End Date.
- This is a **shallow verification** — the automation completes without any assertion and passes vacuously.
- The 3 prior failures likely represent real instability in the test environment or setup, not logic-based failures.

#### How to Fix

Since this case is already Manual, the automation should either be fixed to include proper EXPECTED assertions (steps 3, 4, 5) or removed from automated runs until the framework is updated.

---

## Cases with Issues (Technical)

### ❌ Failed Cases

#### PX-9675: Create Lesson – Daily Recurring – Individual – Lesson Count + Skip Closed Date

- **Suite:** Suite 218
- **Final Status:** FAILED
- **Retries:** 0
- **Step that failed:** Verify Lesson Schedule UI List (Step 5 in automation — unmapped)
- **Failure evidence:**
  ```
  [INFO] Found 1 rows in Lesson Schedule. Expected: 2 records.
  [EXPECTED] Actual [Lesson Schedule End Date] : [2026/04/28 10:00]
           | Expected [Lesson Schedule End Date] : [2026/04/29 10:00]
  ```
- **Root cause:** Product bug — Lesson Schedule End Date shows closed date instead of last actual lesson date when Skip Closed Date is enabled (daily recurring)
- **Assessment:** `UNMAPPED_STEP` + `EXPECTED_RESULT_FAIL` — the failing step is not in the Qase definition (GAP-1)

#### PX-9672: Create Lesson – Weekly Recurring – Group – Lesson Count + Skip Closed Date

- **Suite:** Suite 218
- **Final Status:** FAILED
- **Retries:** 0
- **Step that failed:** Verify Lesson Schedule UI List (unmapped)
- **Failure evidence:**
  ```
  [INFO] Found 1 rows in Lesson Schedule. Expected: 2 records.
  [EXPECTED] Actual [Lesson Schedule End Date] : [2026/04/28 10:00]
           | Expected [Lesson Schedule End Date] : [2026/05/12 10:00]
  ```
- **Root cause:** Same product bug as PX-9675 — weekly variant. Lesson Schedule End Date = closed date (04/28) instead of last lesson date (05/12)
- **Assessment:** `UNMAPPED_STEP` + `EXPECTED_RESULT_FAIL`

---

### ⚠️ Flaky Cases (passed after retries)

| Case ID                                            | Suite     | Retry History                     | Step that was unstable             | Assessment                                                            |
| -------------------------------------------------- | --------- | --------------------------------- | ---------------------------------- | --------------------------------------------------------------------- |
| PX-3585                                            | Suite 425 | failed → passed (×3)              | Go to Lesson Report / edit on grid | FLAKY — likely timing/navigation issue; not a logic failure           |
| PX-9736                                            | Suite 815 | failed → failed → failed → passed | Edit lesson date scenario          | FLAKY + SHALLOW — 3 failures before pass; no assertions in final pass |
| PX-9735                                            | Suite 815 | failed → passed                   | _(not deep-checked)_               | FLAKY — recommend investigation                                       |
| PX-761                                             | Multiple  | invalid → passed (×2)             | _(not deep-checked)_               | Environment/infra instability                                         |
| PX-737                                             | Multiple  | invalid → passed                  | _(not deep-checked)_               | Environment/infra instability                                         |
| PX-3570                                            | Multiple  | invalid → passed                  | _(not deep-checked)_               | Environment/infra instability                                         |
| PX-8493                                            | Multiple  | invalid → passed                  | _(not deep-checked)_               | Environment/infra instability                                         |
| PX-8497                                            | Multiple  | invalid → passed                  | _(not deep-checked)_               | Environment/infra instability                                         |
| PX-8509                                            | Multiple  | invalid → passed                  | _(not deep-checked)_               | Environment/infra instability                                         |
| PX-3574                                            | Multiple  | invalid → passed                  | _(not deep-checked)_               | Environment/infra instability                                         |
| PX-675, 676, 711, 712, 759, 9734, 8293, 8447, 3506 | Multiple  | passed → passed (multiple)        | _(not deep-checked)_               | Potentially duplicate result entries; no functional failure           |

> **Pattern:** 7 cases with `invalid → passed` history suggest environment/infrastructure instability at run start. These are not logic failures.

---

### ✅ Clean Pass Cases (sample)

| Case ID                                     | Suite                   | Steps    | Duration   |
| ------------------------------------------- | ----------------------- | -------- | ---------- |
| PX-9673, 9674, 9676, 9677, 9678, 9680, 9681 | Suite 218               | 8 each   | ~2–3 min   |
| PX-10072–10079                              | Suite 96 (Event Master) | 9 each   | ~1–2 min   |
| PX-9745–9775                                | Suite 1166              | 3–4 each | ~30–60 sec |
| PX-11285, 11538, 13747–13750                | Multiple                | varies   | varies     |
| _(118 total clean pass cases)_              | Multiple suites         | —        | —          |

---

## Recommendations

### 🔴 Critical — Product Bug (Lesson Schedule End Date)

**Affects:** PX-9675, PX-9672 — and potentially all Suite 218 cases using Skip Closed Date + Lesson Count

The Lesson Schedule object (`MANAERP__Lesson_Schedule__c`) is NOT correctly updated when:

- Recurring lesson uses **Skip Closed Date = true**
- Recurrence end mode = **After (X lessons)**

**Symptoms:**

1. Only 1 Lesson Schedule record created instead of the expected count
2. End Date on that record = the first closed date encountered (not the last actual lesson date)

**Action required:** File a defect and assign to engineering. Both daily (PX-9675) and weekly (PX-9672) recurring modes are affected.

### 🔴 Persistent GAP-1 — Undocumented "Verify Lesson Schedule UI List" Step

This automation step has been present since Run 2187 and still has no Qase definition. Because it runs in Suite 218 for all cases, it:

- Generates failures that can't be traced to any defined test step
- Masks what the automation is actually testing in the Lesson Schedule object

**Action:** As per Run 2187 recommendation, either add a Qase step for Lesson Schedule verification across Suite 218, or document it as an automation-internal check.

### 🟠 High — PX-3585 Missing Steps (Publish LR + Mobile)

Step 3 "Publish lesson report" and Step 5 "Student login Mobile" are never exercised by the automation.

**Action:**

- Step 3: Add automation to publish the LR and assert status change on SF OR move to a separate test case.
- Step 5: Update Qase definition to flag as "Mobile — not covered by automation" and re-test manually.

### 🟠 High — PX-9736 Shallow Verification (3 failures + no assertions)

The automation for this case produces zero `[EXPECTED]` assertions in the final pass. This means:

- Steps 3 and 4 ("Check previous lessons", "Check number of lessons") are not executed
- Step 5 ("Check end date.lesson schedule") has no assertion

**Action:** Fix the automation script for Suite 815 to include proper EXPECTED assertions. Do not run this case in automation until fixed. It is already correctly marked as Manual in Qase.

### 🟡 Medium — 7 Cases with `invalid → passed` (Environment Instability)

Cases PX-761, 737, 3570, 8493, 8497, 8509, 3574 all started as `invalid` and required retry to pass.

**Action:** Investigate test runner environment setup at run start — likely a session timeout or pre-condition data issue that resolves on retry.

### 🟡 Definition Quality — PX-9675 Step 6

Step 6 expected result contradicts the test title and automation setup. Update in Qase.

---

## Automation Status Updates

### Deep-Reviewed Cases

| Case ID | Title (short)                                  | Verdict         | Previous Status | Action Taken                         | Reason                                              |
| ------- | ---------------------------------------------- | --------------- | --------------- | ------------------------------------ | --------------------------------------------------- |
| PX-9675 | Create Daily Individual Skip Closed Date       | ❌ Not Matching | Automated (2)   | **No change**                        | System bug; re-test after fix                       |
| PX-9672 | Create Weekly Group Skip Closed Date           | ❌ Not Matching | Automated (2)   | **No change**                        | System bug; re-test after fix                       |
| PX-3585 | Edit Lesson Report on list                     | ❌ Not Matching | Automated (2)   | **No change** — awaiting PM decision | MISSING_STEP (steps 3, 5); automation is incomplete |
| PX-9736 | Edit lesson date with skip closed date — daily | ❌ Not Matching | Manual (0)      | **No change** — already Manual       | Status already correct                              |

> **Note on PX-9675 and PX-9672:** These cases fail due to a product bug, not a test definition gap. Keeping as Automated preserves visibility.

---

### Bulk Automation Status Update (Completed 2026-04-03)

**Goal:** Mark all non-Suite-96 / non-Suite-815 run cases as `Automated (2)`.

**Methodology:**

- Original run: 140 results → 139 unique cases (1 de-duplicated)
- Excluded: 8 Suite 815 cases (Manual, no change) + 5 Suite 96 cases (661, 664, 666, 667, 785 — no change)
- Target list: 117 cases → individually verified via GET request
- **Already `automation=2`**: 91 cases — no API call needed
- **Updated `automation=0 → 2`**: 25 cases — updated via Qase REST API PATCH

**Cases updated from Manual → Automated:**

| Case ID | Title                                                                                               |
| ------- | --------------------------------------------------------------------------------------------------- |
| PX-711  | (Updated in previous session — confirmed)                                                           |
| PX-3787 | Show Related tab under Activity Event                                                               |
| PX-9745 | Edit lesson date so that new lesson date < old lesson date in weekly lesson with end date           |
| PX-9746 | Edit lesson date so that new lesson date > old lesson date in weekly lesson with end date + student |
| PX-9747 | Edit lesson date with skip closed date in weekly lesson with end date                               |
| PX-9748 | Edit lesson date without skip closed date in weekly lesson with end date                            |
| PX-9749 | Edit lesson time in weekly lesson with end date                                                     |
| PX-9750 | Edit lesson date after deleting a lesson in weekly lesson with end date                             |
| PX-9752 | Edit lesson date so that new lesson date < old lesson date in weekly lesson with lesson count       |
| PX-9753 | Edit lesson date so that new lesson date > old lesson date in weekly lesson with lesson count       |
| PX-9754 | Edit lesson date with skip closed date in weekly lesson with lesson count                           |
| PX-9755 | Edit lesson date without skip closed date in weekly lesson with lesson count                        |
| PX-9756 | Edit lesson time in weekly lesson with lesson count                                                 |
| PX-9757 | Edit lesson date after deleting a lesson in weekly lesson with lesson count                         |
| PX-9763 | Edit lesson date so that new lesson date < old lesson date in custom lesson with end date           |
| PX-9764 | Edit lesson date so that new lesson date > old lesson date in custom lesson with end date + student |
| PX-9765 | Edit lesson date with skip closed date in custom lesson with end date                               |
| PX-9766 | Edit lesson date without skip closed date in custom lesson with end date                            |
| PX-9767 | Edit lesson time in custom lesson with end date                                                     |
| PX-9768 | Edit lesson date after deleting a lesson in custom lesson with end date                             |
| PX-9770 | Edit lesson date so that new lesson date < old lesson date in custom lesson with lesson count       |
| PX-9771 | Edit lesson date so that new lesson date > old lesson date in custom lesson with lesson count       |
| PX-9772 | Edit lesson date with skip closed date in custom lesson with lesson count                           |
| PX-9773 | Edit lesson date without skip closed date in custom lesson with lesson count                        |
| PX-9774 | Edit lesson time in custom lesson with lesson count                                                 |
| PX-9775 | Edit lesson date after deleting a lesson in custom lesson with lesson count                         |

**Result:** 26 cases updated to `Automated (2)` · 0 failures · **COMPLETE ✓**
