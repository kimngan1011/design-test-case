# Definition vs. Execution Comparison Report

# PX Run 2187 — Automation Coverage Gaps

**Project:** PX  
**Run ID:** 2187  
**Reviewed By:** GitHub Copilot  
**Review Date:** 2026-03-23  
**Scope:** Comparing what automation actually executed (step-results.md) against what is defined in each Qase test case (preconditions, actions, expected results)

---

## Executive Summary

After comparing the final execution step-results against the original Qase definitions for representative cases across Suites 218, 260, and 401, **7 categories of gaps** were identified:

| #     | Gap Type                                                                                                                                                                        | Severity    | Scope                                                                   |
| ----- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------- | ----------------------------------------------------------------------- |
| GAP-1 | Automation runs a step **not defined** in Qase                                                                                                                                  | 🔴 Critical | All Suite 218 (28 cases)                                                |
| GAP-2 | Defined step is **never executed** by automation                                                                                                                                | 🔴 Critical | PX-3391 + Suite 401                                                     |
| GAP-3 | BO verification is **too shallow** (misses 3 expected results)                                                                                                                  | 🟠 High     | All Suite 218 (28 cases)                                                |
| GAP-4 | A form field is **silently skipped** — test still passes                                                                                                                        | 🟡 Medium   | PX-3391 + Suite 401                                                     |
| GAP-5 | Skip Closed Date expected result is **never explicitly asserted**                                                                                                               | 🟠 Medium   | PX-1015 + all Course Schedule skip-date cases                           |
| GAP-6 | Automation creates/verifies **wrong lesson type** (通常特訓 vs. 通常特訓（時間変更）) — definitions and execution contradict each other, yet tests pass                         | 🔴 High     | PX-9678 + PX-9677 (+ all Suite 218 cases defining 通常特訓（時間変更）) |
| GAP-7 | Definition does **not specify scope of "other lessons"**; negative assertion (teacher absent from other lessons) and "following lessons" teacher propagation are never verified | 🟠 Medium   | PX-1218 (Suite 260)                                                     |

---

## Gap 1 — Undocumented Automation Step: `Verify Lesson Schedule UI List`

**Severity:** 🔴 Critical  
**Affects:** All cases in Suite 218 (Create Lesson on Lesson list) — confirmed for PX-9678, PX-9677, PX-1015, PX-1022, and by pattern all 28 cases in this suite

### What automation executes

Every Suite 218 case runs exactly these 5 steps in `step-results.md`:

```
1. Precondition Data Snapshot
2. Verify Lesson Grid UI
3. Verify Lesson Report
4. Verify Lesson Schedule UI List   ← ⚠️ NOT in any Qase definition
5. Verify BackOffice Details
```

**Step "Verify Lesson Schedule UI List" checks:**

- Lesson Schedule Lesson Name
- Lesson Schedule Lesson Code
- Lesson Schedule Lesson Type
- Lesson Schedule Start Date (first lesson's start datetime)
- Lesson Schedule End Date (first lesson's end datetime)

**Evidence from PX-9678 pass run:**

```
[CHECK] Lesson Schedule Lesson Name: actual="9678CustomEndOn_8679" expected="9678CustomEndOn_8679"
[CHECK] Lesson Schedule Lesson Code: actual="4" expected="4"
[CHECK] Lesson Schedule Lesson Type: actual="通常特訓" expected="通常特訓"
[CHECK] Lesson Schedule Start Date: actual="2026/03/19 09:00" expected="2026/03/19 09:00"
[CHECK] Lesson Schedule End Date: actual="2026/04/30 10:00" expected="2026/04/30 10:00"
```

### What the Qase definition says

**PX-9678 (8 defined steps), PX-9677 (8 steps), PX-1015 (2 steps), PX-1022 (3 steps):**  
None of these test cases include any step about the Salesforce Lesson Schedule object. The defined steps cover:

- Input lesson data and click Save
- Check all lessons in chain (Lesson Grid)
- Check lesson code
- Check lesson type
- Check closed date handling
- Check lesson report
- Login BO and view lessons

**No step mentions "Lesson Schedule", the `MANAERP__Lesson_Schedule__c` object, or Start/End Date fields on that object.**

### Impact

When `Verify Lesson Schedule UI List` fails (as seen in 13 cases in this run), the failure reports a problem in a step that is **not traceable to any defined expected result**. The Qase system marks the test as failing but there is no test case step to reference for root cause or re-test planning.

Additionally, the most common flakiness pattern (sort order inconsistency) occurs entirely within this undocumented step.

### Recommendation

**Option A (preferred):** Add a new step to all applicable Suite 218 test cases documenting the Lesson Schedule verification:

> **Action:** Verify the Lesson Schedule record is created with correct data  
> **Expected result:** User sees the Lesson Schedule record with:
>
> - Lesson Name = created lesson name
> - Lesson Code = first lesson's code
> - Lesson Type = 通常特訓
> - Start Date = first lesson's start datetime
> - End Date = first lesson's end datetime

**Option B:** If the Lesson Schedule check is considered infrastructure-level (not a user-visible business requirement), document it as an automation-internal technical check and exclude it from Qase step definitions. Add a note to the automation code.

---

## Gap 2 — Missing Step: Student Mobile Verification Not Executed

**Severity:** 🔴 Critical  
**Affects:** PX-3391 (User can edit individual lesson report) and likely all similar lesson report cases in Suite 401

### What automation executes

PX-3391 final pass run (`d2f0887.../step-results.md`) executed these steps:

```
1. Go to Lesson Detail Page              → adds student to lesson ✅
2. Edit Lesson Report at Lesson Detail   → edits lesson report ✅
3. Verify updated Lesson Report          → verifies draft status, remarks, CM note ✅
4. Edit data at Lesson Report Details    → edits Lesson Report Detail fields ✅ (with one skip)
5. Verify all fields of Student report detail after update ✅
6. Verify published Lesson Report at Report tab ✅
7. Verify updated lesson report content at BackOffice → verifies BO ✅
```

### What the Qase definition says

**PX-3391 has 6 defined steps**, including:

| Step  | Action                                   | Expected Result                                  | Status              |
| ----- | ---------------------------------------- | ------------------------------------------------ | ------------------- |
| 1     | Go to Lesson Detail → Report tab         | —                                                | ✅ Executed         |
| 2     | Edit all fields of Lesson report detail  | All fields updated on SF                         | ✅ Executed         |
| 3     | Edit all fields of Student report detail | All fields updated on SF                         | ✅ Executed         |
| 4     | Publish lesson report                    | LR status updated on SF                          | ✅ Executed         |
| 5     | Teacher login BO                         | Teacher sees updated LRD + SRD on BO             | ✅ Executed         |
| **6** | **Student login Mobile**                 | **Student sees updated lesson report on Mobile** | ❌ **NOT EXECUTED** |

### Impact

**Step 6 of PX-3391 is completely absent from automation.** The defined expected result — "Student sees lesson report is updated on Mobile" — is never verified in any run. This is a **permanent blind spot**: the mobile app's display of published lesson report data is not covered by the existing automation.

### Recommendation

Either:

1. **Implement mobile verification** in the automation script for lesson report cases (requires mobile automation tooling)
2. **Explicitly exclude this step from automation scope** — mark it in Qase as "manual only" and document the exclusion in the test case's automation notes
3. If mobile is already tested elsewhere, cross-reference the mobile test cases and note the dependency

---

## Gap 3 — Partial Expected Result Verification: "Content" Field Silently Skipped

**Severity:** 🟡 Medium  
**Affects:** PX-3391 and likely all lesson report edit cases

### What automation executes

In PX-3391 pass run, step "Edit data at Lesson Report Details at Lesson Detail page" logs:

```
[INFO] I temporarily skipped the field "content" because I don't see this field
       to edit on the lesson report detail form.
[PASS] Verified success message: was saved.
```

The automation explicitly acknowledges it CANNOT find the "content" field on the form and silently skips it. The step still passes because the save action succeeded.

### What the Qase definition says

Step 2 says: "Edit all fields of Lesson report detail" — **all fields**.  
The defined expected result is: "User sees all fields is updated accordingly on SF."

### Impact

- The "content" field of the Lesson Report Detail is never verified
- The test step PASSES despite incomplete verification — giving a false green signal
- This has been happening silently across all lesson report edit test runs

### Recommendation

1. **Investigate if the "content" field still exists** on the Lesson Report Detail form in the current Salesforce build
2. If the field was **removed from the UI**, update the Qase definition to remove it from the "Edit all fields" expected result
3. If the field **still exists but the automation cannot locate it** (CSS selector issue), fix the automation's locator for the content field
4. Change the automation log from `[INFO]` (silent skip) to `[WARN]` so it's more visible in step-results review

---

## Gap 4 — Shallow BackOffice Verification (Suite 218)

**Severity:** 🟠 High  
**Affects:** All Suite 218 cases — PX-9678, PX-9677, PX-1015, PX-1022, and the entire suite

### What automation executes

The "Verify BackOffice Details" step in Suite 218 cases logs only:

```
[INFO] Navigated to Back Office URL: https://administration.manabie.net/...
[INFO] [BO DEBUG] Found field [Lesson Name]: "9678CustomEndOn_8679"
```

Only the **Lesson Name** field is verified on the Back Office.

### What the Qase definitions say

Multiple Suite 218 cases (PX-9678, PX-9677, PX-1015) have a shared BO step that expects:

> "User sees these lessons on BO"  
> "User sees the **lesson code, lesson type is read-only** on BO"  
> "User sees the **lesson report** on Lesson detail → Report tab **and Lesson Report list** on BO"

The automation verifies **only lesson name** — it does not verify:

- ❌ Lesson code on BO
- ❌ Lesson type field and its read-only status on BO
- ❌ Lesson report presence on the Report tab
- ❌ Lesson report on the Lesson Report list (BO list view)

### Impact

The BO step passes even when the lesson code is wrong, the lesson type is editable (which it shouldn't be), or the lesson report is missing from BO. These are meaningful expected results in the test definition that are currently unverified.

### Recommendation

Enhance the "Verify BackOffice Details" automation step to:

1. Verify lesson code field value on BO lesson detail
2. Verify lesson type field is present and read-only
3. Navigate to the Report tab and verify at least one lesson report exists
4. Navigate to Lesson Report list and verify the lesson report appears

---

## Gap 5 — Missing Negative Assertion: Closed Date Exclusion Not Verified

**Severity:** 🟠 Medium  
**Affects:** PX-1015 and all Course Schedule cases where `skipCloseDate: true`

### What automation executes

In the PX-1015 pass run, the `Verify Lesson Grid UI` step checks:

```
[CHECK] Lesson Grid Row 1: date=2026/02/17, code=2, type=通常特訓 ✅
[CHECK] Lesson Grid Row 2: date=2026/02/24, code=3, type=通常特訓 ✅
[CHECK] Lesson Grid Row 3: date=2026/03/03, code=4, type=通常特訓 ✅
[CHECK] Lesson Grid Row 4: date=2026/03/10, code=5, type=通常特訓 ✅
[CHECK] Total lessons: 4 ✅
```

The automation verifies the **presence** of 4 expected lessons with correct dates, codes, and types. It verifies that exactly 4 rows exist (no more, no less).

**What is never logged:**

```
[CHECK] Closed date 2026/01/12 is absent from lesson list  ← MISSING
[CHECK] Closed date 2026/03/21 is absent from lesson list  ← MISSING
[CHECK] Closed date 2026/04/30 is absent from lesson list  ← MISSING
```

No assertion of the form `expect(lessonDates).not.toContain('2026/03/21')` or equivalent exists in the execution log.

### What the Qase definition says

**PX-1015 Step 1 Expected Result:**

> "User does not see a lesson that has lesson date = closed date"

The definition explicitly requires verifying that a lesson on a closed date is **absent** from the lesson grid — not merely that the 4 expected lessons are present.

### Why this matters

The automation's positive assertion (4 rows match 4 expected dates) provides **indirect** coverage: if the expected dates were pre-calculated to exclude closed dates and the total count is enforced, a leaked closed-date lesson would cause a count mismatch. However:

1. This indirect coverage is **not equivalent to an explicit assertion** — the Qase definition says "User does NOT see a lesson on a closed date", which is a distinct, named expected result
2. If the expected-date calculation logic itself has a bug that also includes a closed date, both the count check and the date check would still pass (because expected and actual would both include the wrong date)
3. The same pattern likely applies to all Course Schedule cases with `skipCloseDate: true` in the suite

Compare with **PX-9677** (skip closed date, Custom Recurring): the step-results confirm the date 2026/03/21 is absent from the list (lessonCount=41, with 03/21 being a Friday that week — explicitly not in the result set). PX-1015 never makes this kind of direct absence check.

### Recommendation

1. **Add an explicit absence assertion** to the `Verify Lesson Grid UI` step for all `skipCloseDate: true` cases:
   - After verifying expected rows, iterate over the system's configured closed dates
   - Assert none of those dates appear in the rendered lesson grid
   - Log: `[CHECK] Closed date {date} is absent from lesson list ✅`
2. **Update PX-1015's Qase step definition** to separate the positive check (expected lessons present) from the negative check (closed-date lessons absent) — making them two individually verifiable assertions
3. **Audit all Course Schedule test cases** in Suite 218 with `skipCloseDate: true` to confirm the same gap exists and apply the fix consistently

---

## Gap 6 — Wrong Lesson Type: Automation Creates and Verifies 通常特訓 Instead of 通常特訓（時間変更）

**Severity:** 🔴 High  
**Affects:** PX-9678 and PX-9677 (and likely all Suite 218 cases whose definitions specify 通常特訓（時間変更）)

### What the Qase definitions say

**PX-9678 Step 1 Input:**

> "Lesson type: 通常特訓（時間変更）"

**PX-9678 Step 5 Expected Result:**

> "User sees the default lesson type = **通常特訓（時間変更）** for all lessons."

**PX-9677 Step 1 Input** and **Step 5 Expected Result:** identical to PX-9678.

### What automation executes

From PX-9678 Precondition Data Snapshot:

```json
"lessonType": "通常特訓"
```

From PX-9678 `Verify Lesson Grid UI` (43 rows):

```
[PASS] Pass LessonType: [通常特訓] vs [通常特訓]   ← repeated 43 times
```

From PX-9677 Precondition Data Snapshot:

```json
"lessonType": "通常特訓",
"skipCloseDate": true
```

From PX-9677 `Verify Lesson Grid UI` (41 rows):

```
[PASS] Pass LessonType: [通常特訓] vs [通常特訓]   ← repeated 41 times
```

### Why this is a problem

1. **Input mismatch**: The test case definition specifies lesson type = `通常特訓（時間変更）` (Standard Special Training — Time Change). The automation creates lessons with `通常特訓` (Standard Special Training, base type). These are distinct types in the Manabie lesson management system.
2. **Expected result mismatch**: The verification passes because **both the expected value and the actual value are set to the same wrong type** (`通常特訓`). The test never even attempts to check `通常特訓（時間変更）`.
3. **Silent false positive**: The automation reports a green pass for the lesson type step, but it is not testing the behavior defined in the Qase test case.
4. **Business risk**: If a bug causes `通常特訓（時間変更）` lessons to be incorrectly created as `通常特訓`, this automation would NOT detect it — it would still pass.

### Comparison with PX-1015, PX-1022

Note: PX-1015 and PX-1022 correctly specify `通常特訓` (without 時間変更) in both their definitions and automation. The discrepancy is specific to PX-9677 and PX-9678 which intentionally test the `通常特訓（時間変更）` type variant.

### Recommendation

1. **Update the automation for PX-9677 and PX-9678** to create lessons with `lessonType = 通常特訓（時間変更）` and set the expected value in the lesson type check to `通常特訓（時間変更）`
2. **Audit all Suite 218 cases** to identify which ones specify `通常特訓（時間変更）` vs. `通常特訓` and ensure the automation matches the definition
3. **Add a validation check at test setup** that confirms the `lessonType` in the precondition data snapshot matches the Qase step 1 definition

### Related Definition Quality Issue — PX-9678 Step 1

PX-9678 is titled "No Skip Closed Date" but its Step 1 action incorrectly lists "Check the Skip Closed Date" as an input parameter (it shares step 1 text with PX-9677). The automation correctly uses `skipCloseDate: false` (evidenced by 43 lessons including closed dates 03/21 and 04/30). However, the definition is misleading: a human tester following PX-9678 step 1 literally would enable Skip Closed Date and produce wrong results. This definition error should be corrected in Qase.

---

## Gap 7 — Undefined "Other Lessons" Scope: Negative Teacher Assertion and Following-Lesson Propagation Never Verified

**Severity:** 🟠 Medium  
**Affects:** PX-1218 (Assign a teacher to lesson course schedule) — Suite 260

### What the Qase definition says

The test has a 4-lesson chain (Course Schedule, Week 1 / 3 / 5 / 10 — per the precondition referencing PX-1015).

**Step 1 expected result:**

> "User sees the teacher is added to selected lesson"  
> "User does **not** see the teacher is added to **other lessons in the chain**"

**Step 2 expected result:**

> "User sees the teacher is added to **this and the following lesson**"  
> "User sees the 2 teachers in the **2nd lesson**"

**Step 3 expected result:**

> "User sees the teacher is added to Lesson"

### Definition ambiguities

| Issue | Location        | Ambiguity                                                                                                                                                                            |
| ----- | --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 1     | Step 1 expected | "other lessons in the chain" — which lessons? Lesson 1, 3, 4? All three? How many must be navigated to and verified?                                                                 |
| 2     | Step 2 expected | "this and the following lesson" — "lesson" is singular; the chain has 4 lessons. Does "following" mean only the 2nd lesson (immediate next), or lessons 2, 3, and 4 (all following)? |
| 3     | Step 2 expected | "User sees the 2 teachers in the 2nd lesson" — only the 2nd lesson is mentioned. What are the expected states of lessons 3 and 4?                                                    |
| 4     | Step 3 expected | "User sees the teacher is added to Lesson" — which lesson? Which teacher? No BO scope defined.                                                                                       |

### What automation executes

**Step 1** (`Open 2nd lesson and assign Teacher — Only this Lesson`):

```
[PASS] Pass Verified: User "Teacher [E2E] Kim Ngan" is successfully assigned.
```

Only checks that the teacher was added to the 2nd lesson. Never navigates to lessons 1, 3, or 4 to verify teacher is absent.

**Step 2** (`Open 1st lesson and assign Teacher — This and following`):

```
[PASS] Verified success message: assigned teacher successfully
[PASS] Pass Verified: User "Teacher 20250303" is successfully assigned.
```

Only verifies the success message and that Teacher 20250303 appears in lesson 1. Never checks whether Teacher 20250303 was propagated to lessons 3 and 4.

**Step 3** (`Verify Teacher assignments at BackOffice`):

```
[PASS] PASS [BO Teacher Check [Following Teacher]] → "Teacher 20250303"           (lesson 1)
[PASS] PASS [BO Teacher Check [Only This Teacher]] → "Teacher [E2E] Kim Ngan, Teacher 20250303"  (lesson 2 — 2 teachers)
```

Verifies lesson 1 and lesson 2 on BO. Never checks lesson 3 or lesson 4.

### Gaps identified

1. **Step 1 negative assertion never verified**: The expected result "User does NOT see teacher in other lessons" is completely absent from the automation. No log line shows verification of Teacher [E2E] Kim Ngan being absent from lesson 1, 3, or 4.

2. **Step 2 propagation scope unclear**: Automation only checks that Teacher 20250303 is in lesson 1 (via success message). Whether lessons 3 and 4 also received Teacher 20250303 (as "following lessons") is never verified.

3. **BO step partial coverage**: BO check covers only 2 of 4 lessons. Lessons 3 and 4 state (teacher presence/absence) is never checked.

### Root cause

The definition uses vague scoping phrases ("other lessons in the chain", "the following lesson") without specifying:

- Which lesson numbers to navigate to
- How many lessons to verify
- The expected teacher state for each lesson individually

Because the scope is undefined, the automation implemented a minimal check (2-lesson scope) without violating any explicit rule in the definition. The vague wording made it easy to implement an incomplete test without triggering a review.

### Recommendation

**For QA (definition update):** Revise PX-1218 steps to explicitly name each lesson:

- Step 1 expected: "User does not see Teacher [E2E] Kim Ngan in Lesson 1, Lesson 3, Lesson 4 (navigate to each and verify teacher list)"
- Step 2 expected: "User sees Teacher 20250303 in Lesson 1, Lesson 2, Lesson 3, Lesson 4" (if "following" means all) — OR "User sees Teacher 20250303 in Lesson 1 and Lesson 2 only" (if "following" means immediate next only — need product clarification)
- Step 3 expected: Specify which lesson to verify on BO and which teachers are expected (e.g. "Lesson 2 shows Teacher [E2E] Kim Ngan + Teacher 20250303 on BO")

**For automation:** Add explicit absence assertions for Teacher [E2E] Kim Ngan in lessons 1, 3, 4 after step 1. Add explicit presence assertions for Teacher 20250303 in all applicable lessons after step 2.

---

## Step Coverage Matrix

> **Status legend:**
>
> - ✅ Fully covered
> - ⚠️ Partially covered (see note)
> - ❌ Not executed
> - ➕ Extra step (exists in automation but not in Qase)

---

### PX-9678 — Create Lesson: Custom Recurring / Group / End Date / No Skip Closed Date

| #   | Qase Action                                     | Expected Result (Qase)                             | Automation Step                | Status                                                                                                                                                              |
| --- | ----------------------------------------------- | -------------------------------------------------- | ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Input lesson data (type = 通常特訓（時間変更）) | —                                                  | Precondition Data Snapshot     | ⚠️ Automation sets type = 通常特訓 (not 通常特訓（時間変更）) — see GAP-6; also: step 1 definition incorrectly includes "Check Skip Closed Date" for a No-Skip test |
| 2   | Click Save                                      | Lessons created from start to end date             | Verify Lesson Grid UI          | ✅ 43 rows verified                                                                                                                                                 |
| 3   | Check all lessons in chain                      | Day of week = selected days                        | Verify Lesson Grid UI          | ✅ Embedded per row                                                                                                                                                 |
| 4   | Check lesson code                               | Code increments for each lesson                    | Verify Lesson Grid UI          | ✅ Codes 4→46 verified                                                                                                                                              |
| 5   | Check lesson type                               | Default type = **通常特訓（時間変更）** for all    | Verify Lesson Grid UI          | ⚠️ Verifies 通常特訓 vs 通常特訓 — wrong type, both sides set to base type — see GAP-6                                                                              |
| 6   | Check closed date (no skip)                     | Lesson on closed date still exists                 | Verify Lesson Grid UI          | ✅ 03/21 + 04/30 present                                                                                                                                            |
| 7   | Check lesson report                             | Group lesson report auto-created                   | Verify Lesson Report           | ✅ 43 reports verified                                                                                                                                              |
| 8   | Login BO, view lessons                          | Lesson code + type read-only on BO; report visible | Verify BackOffice Details      | ⚠️ Only lesson name checked on BO                                                                                                                                   |
| —   | _(not in Qase)_                                 | _(not in Qase)_                                    | Verify Lesson Schedule UI List | ➕ Extra step, no definition                                                                                                                                        |

---

### PX-9677 — Create Lesson: Custom Recurring / Individual / End Date / Skip Closed Date

| #   | Qase Action                                                            | Expected Result (Qase)                       | Automation Step                | Status                                                                                 |
| --- | ---------------------------------------------------------------------- | -------------------------------------------- | ------------------------------ | -------------------------------------------------------------------------------------- |
| 1   | Input lesson data (Skip Closed Date = ON; type = 通常特訓（時間変更）) | —                                            | Precondition Data Snapshot     | ⚠️ Automation sets type = 通常特訓 (not 通常特訓（時間変更）) — see GAP-6              |
| 2   | Click Save                                                             | Lessons created from start to end date       | Verify Lesson Grid UI          | ✅ 41 rows verified                                                                    |
| 3   | Check all lessons in chain                                             | Day of week = selected                       | Verify Lesson Grid UI          | ✅ Embedded                                                                            |
| 4   | Check lesson code                                                      | Code increments                              | Verify Lesson Grid UI          | ✅                                                                                     |
| 5   | Check lesson type                                                      | Default = **通常特訓（時間変更）**           | Verify Lesson Grid UI          | ⚠️ Verifies 通常特訓 vs 通常特訓 — wrong type, both sides set to base type — see GAP-6 |
| 6   | Check skip closed date                                                 | No lesson on closed dates                    | Verify Lesson Grid UI          | ✅ 03/21 absent; count = 41                                                            |
| 7   | Check lesson report                                                    | Individual lesson report auto-created        | Verify Lesson Report           | ✅ 41 reports verified                                                                 |
| 8   | Login BO, view lessons                                                 | Lesson code + type read-only; report visible | Verify BackOffice Details      | ⚠️ Only lesson name checked on BO                                                      |
| —   | _(not in Qase)_                                                        | _(not in Qase)_                              | Verify Lesson Schedule UI List | ➕ Extra step, no definition                                                           |

---

### PX-1015 — Create Lesson: Course Schedule / Individual

| #   | Qase Action                                         | Expected Result (Qase)                                    | Automation Step                              | Status                                                                      |
| --- | --------------------------------------------------- | --------------------------------------------------------- | -------------------------------------------- | --------------------------------------------------------------------------- |
| 1a  | Fill in details; select Course Schedule; click Save | Lessons on correct week order; code +1; type = 通常特訓   | Verify Lesson Grid UI + Verify Lesson Report | ✅ 4 lessons (02/17, 02/24, 03/03, 03/10); codes 2→5; type verified         |
| 1b  | _(same save action)_                                | **No lesson on closed date** (01/12, 03/21, 04/30 absent) | Verify Lesson Grid UI                        | ⚠️ Absence of closed-date lessons **never explicitly asserted** — see GAP-5 |
| 2   | Login BO, view lesson                               | Lessons + reports on BO; code + type read-only            | Verify BackOffice Details                    | ⚠️ Only lesson name checked on BO                                           |
| —   | _(not in Qase)_                                     | _(not in Qase)_                                           | Verify Lesson Schedule UI List               | ➕ Extra step, no definition                                                |

---

### PX-1022 — Create Lesson: One-time / Individual / Lesson date = Closed Date

| #   | Qase Action                         | Expected Result (Qase)                                                       | Automation Step                              | Status                                      |
| --- | ----------------------------------- | ---------------------------------------------------------------------------- | -------------------------------------------- | ------------------------------------------- |
| 1   | Fill in lesson details (Individual) | —                                                                            | Precondition Data Snapshot                   | ✅                                          |
| 2   | Create lesson on closed date        | Lesson + report = Draft; info correct; type = 通常特訓; lesson still created | Verify Lesson Grid UI + Verify Lesson Report | ✅ 1 lesson on 05/15, code=1, type=通常特訓 |
| 3   | Login BO, view lesson               | Lesson + report on BO; code + type read-only; report = Draft                 | Verify BackOffice Details                    | ⚠️ Only lesson name checked on BO           |
| —   | _(not in Qase)_                     | _(not in Qase)_                                                              | Verify Lesson Schedule UI List               | ➕ Extra step, no definition                |

---

### PX-1216 — Assign a Teacher to an One-time Lesson

| #   | Qase Action                                      | Expected Result (Qase)          | Automation Step                               | Status                      |
| --- | ------------------------------------------------ | ------------------------------- | --------------------------------------------- | --------------------------- |
| 1   | Go to lesson detail → Add Teachers → Add teacher | Teacher added to lesson         | Add teacher + Verify teacher at Lesson Detail | ✅ Teacher visible in table |
| 2   | Login BO, view teacher                           | Teacher visible in lesson on BO | Verify teacher assignment at BackOffice       | ✅ Teacher name found on BO |

> ✅ **No gaps** — PX-1216 is fully covered.

---

### PX-1218 — Assign a Teacher to Lesson Course Schedule

**Context:** 4-lesson chain (Week 1 / 3 / 5 / 10; Course Schedule). Two teacher assignments: "Only this Lesson" on lesson 2, "This and following" on lesson 1.

| #   | Qase Action                                                    | Expected Result (Qase)                                     | Automation Step                                         | Status                                                                                              |
| --- | -------------------------------------------------------------- | ---------------------------------------------------------- | ------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| 1a  | Open 2nd lesson; Add teacher with "Only this Lesson"           | Teacher added to 2nd lesson                                | Open 2nd lesson and assign Teacher (Only this Lesson)   | ✅ Teacher [E2E] Kim Ngan assigned to lesson 2                                                      |
| 1b  | _(same action)_                                                | Teacher is **absent** from all other lessons in chain      | _(none)_                                                | ❌ Never verified — automation does not navigate to lessons 1, 3, or 4 to check absence — see GAP-7 |
| 2a  | Open 1st lesson; Add teacher with "This and following lessons" | Teacher added to lesson 1                                  | Open 1st lesson and assign Teacher (This and following) | ✅ Teacher 20250303 assigned to lesson 1                                                            |
| 2b  | _(same action)_                                                | Teacher propagated to **all following lessons** (2, 3, 4?) | _(limited)_                                             | ⚠️ BO step verifies lesson 2 has 2 teachers; lessons 3 and 4 never checked — see GAP-7              |
| 3   | Login BO, view teacher                                         | Teacher visible in lesson (unspecified which)              | Verify Teacher assignments at BackOffice                | ⚠️ Lessons 1 and 2 verified on BO; lessons 3 and 4 never checked — see GAP-7                        |

---

### PX-3391 — User Can Edit Individual Lesson Report

| #     | Qase Action                              | Expected Result (Qase)                | Automation Step                              | Status                                                                                                                                                                                            |
| ----- | ---------------------------------------- | ------------------------------------- | -------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1     | Go to Lesson Detail → Report tab         | —                                     | Go to Lesson Detail Page                     | ⚠️ Automation also **adds student to lesson** in this step — extra action not defined in Qase step 1 or precondition (precondition says "with a student" but student is created during execution) |
| 2     | Edit all fields of Lesson report detail  | All fields updated on SF              | Edit Lesson Report + Edit data at LR Details | ⚠️ "content" field silently skipped                                                                                                                                                               |
| 3     | Edit all fields of Student report detail | All fields updated on SF              | Verify all fields of Student report detail   | ✅ Understanding, Quiz, Homework, CM Note, Remarks                                                                                                                                                |
| 4     | Publish lesson report                    | LR status updated on SF               | Verify published LR at Report tab            | ✅ Status = Published                                                                                                                                                                             |
| 5     | Teacher login BO                         | Teacher sees updated LRD + SRD on BO  | Verify LR content at BackOffice              | ✅ CM Note, Remark, Homework verified                                                                                                                                                             |
| **6** | **Student login Mobile**                 | **Student sees updated LR on Mobile** | _(none)_                                     | ❌ **NOT EXECUTED**                                                                                                                                                                               |

---

## Consolidated Gap Summary

| Gap ID | Description                                                                                                                                                                                                                                     | Scope                                                                     | Priority  |
| ------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------- | --------- |
| GAP-1  | `Verify Lesson Schedule UI List` runs in automation but is not in any Qase step definition                                                                                                                                                      | All Suite 218 (28 cases)                                                  | 🔴 High   |
| GAP-2  | Step 6 "Student login Mobile" never executed — permanent blind spot                                                                                                                                                                             | PX-3391 + Suite 401                                                       | 🔴 High   |
| GAP-3  | BO verification only checks Lesson Name; misses lesson code, type, report                                                                                                                                                                       | All Suite 218 (28 cases)                                                  | 🟠 Medium |
| GAP-4  | "content" field in Lesson Report Detail silently skipped; test still passes green                                                                                                                                                               | PX-3391 + Suite 401                                                       | 🟡 Medium |
| GAP-5  | Skip Closed Date expected result ("no lesson on closed date") never explicitly asserted; automation only verifies presence of expected lessons                                                                                                  | PX-1015 + Course Schedule skip-date cases                                 | 🟠 Medium |
| GAP-6  | Automation creates and verifies lesson type `通常特訓` but definitions for PX-9677 and PX-9678 require `通常特訓（時間変更）`; tests pass with false green because both expected and actual values are set to the wrong type                    | PX-9677 + PX-9678 (+ other Suite 218 cases defining 通常特訓（時間変更）) | 🔴 High   |
| GAP-7  | PX-1218 definition does not specify which "other lessons" to check for teacher absence, nor how many "following lessons" should receive the teacher; automation never verifies the negative assertion ("does not see teacher in other lessons") | PX-1218 (Suite 260)                                                       | 🟠 Medium |

---

## Action Items

### For QA (Test Case Definition Updates)

1. **[GAP-1] Add Lesson Schedule verification step** to all Suite 218 test cases
   - Document what fields are expected and their values
   - Assign to the test case author (Suite 218 owner)

2. **[GAP-2] Decide fate of Student Mobile step** in PX-3391 and Suite 401 cases
   - Option A: Implement mobile automation
   - Option B: Mark as manual-only in Qase, remove from automation scope

3. **[GAP-3] Expand BO step expected results** in Suite 218 definitions
   - Currently: "User sees lessons on BO" (vague)
   - Should specify: lesson code, lesson type (read-only), lesson report on Report tab

### For Automation Engineers

4. **[GAP-1] Confirm whether Lesson Schedule verification is intentional** and not part of any definition — if so, add it to definitions; if exploratory, document it as an extra check

5. **[GAP-3] Enhance `Verify BackOffice Details` step** to cover:
   - Lesson code: verify value matches
   - Lesson type: verify field is read-only
   - Report tab: verify at least one lesson report present

6. **[GAP-4] Fix or document the "content" field skip** in lesson report edit steps
   - Investigate if the Salesforce `content` field is visible / was removed
   - Change silent `[INFO]` skip to `[WARN]` so it appears in automated review

7. **[GAP-5] Add explicit closed-date absence assertion** for all `skipCloseDate: true` cases (PX-1015 + Course Schedule suite)
   - After verifying expected lesson rows, assert each system closed date does NOT appear in the lesson grid
   - Log: `[CHECK] Closed date {date} is absent from lesson list` for each closed date
   - This makes the negative expected result verifiable and traceable to the Qase step definition

8. **[GAP-6] Fix lesson type mismatch for PX-9677 and PX-9678**:
   - Change `lessonType` in the automation data setup from `通常特訓` → `通常特訓（時間変更）` for both cases
   - Change the expected type in the `Verify Lesson Grid UI` assertion to match `通常特訓（時間変更）`
   - After the fix, the automation will actually test the right lesson type variant

9. **[Definition fix] Correct PX-9678 Step 1 in Qase**:
   - Remove "Check the Skip Closed Date" from PX-9678's step 1 input list, or change it to "Do NOT check Skip Closed Date"
   - This is a copy-paste error from PX-9677 — PX-9678 is the No Skip variant, so Skip Closed Date should be OFF

10. **[GAP-7] Clarify "other lessons" and "following lessons" scope in PX-1218** (QA definition update):
    - Add explicit lesson number references to each expected result (e.g. "lesson 2 has teacher X", "lessons 1, 3, 4 do NOT have teacher X")
    - Confirm with product whether "this and the following lesson" means the immediate next lesson only, or ALL subsequent lessons in the chain — then update the definition accordingly
    - After clarification, add absence assertions in automation for lessons 1, 3, 4 (Step 1 negative check) and presence assertions for all applicable following lessons (Step 2 propagation)

11. **[GAP-3] Standardize automation step names to match Qase step actions** for traceability
    - Example: rename "Verify BackOffice Details" → "Check lesson code, lesson type read-only, lesson report on BO"

---

## Notes on Precondition Capture

For all Suite 218 cases, the `Precondition Data Snapshot` step correctly captures all input data including:

- Login user and environment
- All lesson creation parameters (location, academic year, teaching method, recurrence settings, closed dates)
- Expected output (dates of all lessons in chain)

This is well-designed and provides full traceability of test inputs. No gaps in precondition coverage.
