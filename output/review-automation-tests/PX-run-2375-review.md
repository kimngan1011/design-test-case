# Automation Test Run Review

| Field | Value |
|-------|-------|
| **Project** | PX |
| **Run ID** | 2375 |
| **Run Title** | Automated Playwright Run - renseikai-rehearsal2 - 2026-04-12 17:01:57 |
| **Run Date** | 2026-04-12T17:02:09+00:00 |
| **Environment** | renseikai-rehearsal2 (Salesforce sandbox) |
| **Scope** | Lesson Management (Suite 192) only |
| **Reviewed By** | GitHub Copilot |
| **Review Date** | 2026-04-16 |

---

## 1. Run Summary

| Metric | Count |
|--------|-------|
| Total cases in run | 154 (valid) |
| Lesson Management cases reviewed | 114 |
| Non-Lesson Management (excluded) | 40 (Event Master suites 96, 97, 107, 125) |
| Passed (clean) | 110 |
| Passed (after retry / duplicate submit) | 4 (PX-8293, PX-9734, PX-9735, PX-9736) |
| Failed | 1 (PX-1479) |
| No step-results available | 2 (PX-1479, PX-10533) |
| **Execution vs Definition: Matching** | **2** |
| **Execution vs Definition: Not Matching** | **~112** |

> **Excluded from Lesson Management:** cases 661–786 (Event Master creation / editing), 10072–10079 (Event Master), 11285 (Activity Event).  
> **Duplicate entries:** PX-8293, PX-9734, PX-9735, PX-9736 each have 2 result entries (Playwright retry mechanism submitted both attempts even though the first passed). Both entries show `passed`. **Not true flakiness.**  
> **PX-10533** (Suite 1294 — Lesson Allocation): no step-results URL; the automation result was submitted without a steps attachment. Case definition is `automation=0` (manual), suggesting test was run without step logging enabled.

---

## 2. Per-Suite Verification Table

| Suite ID | Suite Name | Cases Sampled | Pass/Fail | Matching? | Issue Types |
|----------|-----------|---------------|-----------|-----------|-------------|
| 218 | Create Lesson on Lesson list | PX-1013, 1014, 1015, 1016, 1022, 1023, 1039, 9672–9791 (~75 cases) | ✅ Pass | ❌ Not Matching | EXTRA_ACTION, EXPECTED_RESULT_FAIL, PRECONDITION_FAIL, DEFINITION_QUALITY |
| 815 | Edit lesson information in daily lesson | PX-8293, 8294, 8447, 8451, 8455, 8481, 8487, 8493–8518 (~19 cases) | ✅ Pass | ❌ Not Matching | EXTRA_ACTION, DEFINITION_MISMATCH, EXPECTED_RESULT_FAIL |
| 287 | Change lesson status in detailed lesson page | PX-1456 | ✅ Pass | ❌ Not Matching | MISSING_STEP × 2, EXPECTED_RESULT_FAIL |
| 260 | Assign/Unassign a teacher in lesson detail | PX-1216, PX-1218 | ✅ Pass | ✅ Matching | — |
| 326 | Collect Attendance on BO | PX-1919 | ✅ Pass | ❌ Not Matching | MISSING_STEP × 5, EXPECTED_RESULT_FAIL × 3 |
| 1649 | Assign/Unassign a student by Add student popup | PX-1263, PX-1265, PX-11538 | ✅ Pass | ❌ Not Matching | MISSING_STEP × 3, EXPECTED_RESULT_FAIL |
| 425 | Lesson Report List (SF) | PX-3144, PX-1377 | ✅ Pass | ❌ Not Matching | MISSING_STEP × 2, EXPECTED_RESULT_FAIL |
| 1748 | Lesson Report Detail (BO) | PX-13747, 13748, 13749, 13750 | ✅ Pass | ❌ Not Matching | MISSING_STEP (Mobile), DEFINITION_MISMATCH (edit flow SF→BO) |
| 290 | Trial Student in one-time lesson | PX-1479 | ❌ FAILED | ❌ N/A — test invalid | INVALID (test data issue) |
| 1294 | Lesson Allocation assign by class | PX-10533 | ✅ Pass | ⚪ Unknown | No step-results available |

---

## 3. Detailed Findings by Suite

---

### Suite 218 — Create Lesson on Lesson list (~75 cases)

**Representative cases:** PX-1013, PX-9672 (Create Lesson Group)

**Automation execution pattern:**
1. `[PRECONDITION]` Create lesson via API setup (hidden from Qase steps 1–2)
2. Search created lesson in Lesson Grid
3. Verify Lesson Grid data (date, time, teacher, course, class, lesson type)
4. Verify Lesson Report created
5. **Verify Lesson Schedule UI List** ← extra step
6. Verify BackOffice Details (lesson code, type, date, teacher, course, status)

**Qase steps (8 steps):**
1. Input lesson data + Click Save → (image-only expected result)
2. Check lesson is created (Lesson Detail)
3. Check student is assigned to lesson
4. Check lesson schedule → lesson is added to the list
5. Check lesson in BO
6. Check Lesson is NOT on closed date
7. Check lesson report is created
8. Check BO lesson detail (code, type = read-only)

**Issues:**

| # | Issue Type | Details |
|---|-----------|---------|
| 1 | EXTRA_ACTION | Automation step "Verify Lesson Schedule UI List" has no corresponding Qase step. This is an extra navigation/verification not described in the definition. |
| 2 | PRECONDITION_FAIL | Qase steps 1–2 ("Input lesson data + Click Save" + verify creation) are embedded in the Precondition API setup. The test action (user clicking Save) is never performed via browser. |
| 3 | DEFINITION_QUALITY | Qase step 1 expected result is an image only — no textual assertion to verify against. |
| 4 | EXPECTED_RESULT_FAIL | Qase step 8 expected "lesson code, lesson type is read-only on BO" — automation logs verify CODE and TYPE values (e.g. `通常特訓`) but does NOT assert read-only state. |
| 5 | GAP-SILENT | Qase step 6 "lesson is NOT on closed date" — automation checks lesson count matches expected number (implicit pass), but no explicit `[EXPECTED]` log asserts the absence of a closed-date lesson. |

**Verdict: ❌ Not Matching**

---

### Suite 815 — Edit lesson information in daily lesson (~19 cases)

**Representative cases:** PX-8293 (edit teacher), PX-8447 (edit lesson date with skip closed date)

**Automation execution pattern (PX-8293):**
1. Search lesson (before update) and list recurring chain
2. Select a middle lesson in the chain
3. Edit lesson (teacher change) and verify update success
4. Verify data after update (SF lesson detail)

**Automation execution pattern (PX-8447):**
1. Search lesson and list recurring chain (by lesson name)
2. Select a middle lesson
3. Edit lesson date (2026/04/15 → 2026/04/16), scope = "Only this lesson" (`recalculatedImpact=1`)
4. Verify data after update

**Qase steps for PX-8293 (3 steps):**
1. Open a middle lesson in the chain (shared step)
2. Edit lesson with a new teacher → Expected: teacher is updated, all lessons in recurring chain are recalculated
3. Check the last lesson in the chain → Expected: User sees the last lesson within end date

**Qase steps for PX-8447 (4 steps):**
1. Open a middle lesson (shared step)
2. Edit lesson date with skip closed date → Expected: lesson date ≠ closed date
3. Check the previous lessons → Expected: no changes to previous lessons
4. Check the last lesson in the chain → Expected: last lesson within end date

**Issues:**

| # | Issue Type | Details |
|---|-----------|---------|
| 1 | EXTRA_ACTION | Automation step "Search lesson and list recurring chain" has no corresponding Qase step — test starts from Qase step 1 (open middle lesson), skipping the search navigation. |
| 2 | DEFINITION_MISMATCH (PX-8293) | Qase step 2 expected "all lessons in chain are recalculated" (full chain impact). Automation uses `recalculatedImpact=1` which means "Only this lesson" scope — contradicts definition. |
| 3 | EXPECTED_RESULT_FAIL | Qase step 3/4 "User sees the last lesson within end date" — automation logs chain dates but no `[EXPECTED]` assertion explicitly confirms the last lesson falls within the end date boundary. |
| 4 | EXPECTED_RESULT_FAIL (PX-8447) | Qase step 2 expected "User does not see the lesson date = closed date" — automation edits date but no explicit closed-date absence check in `[EXPECTED]` logs. |

**Verdict: ❌ Not Matching**

---

### Suite 287 — Change lesson status in detailed lesson page (PX-1456)

**Automation execution pattern:**
1. Precondition (lesson created and published via API)
2. Open BackOffice tab
3. Draft → Published (verify SF + BO)
4. Published → Completed (verify SF + BO)
5. Completed → Published (verify SF + BO)
6. Published → Cancelled (verify SF + BO)

**Qase steps (6 steps):**
1. Draft → Published (SF + BO) with Mobile parent view
2. Published → Completed (SF + BO) with Mobile parent view
3. Completed → Published (SF + BO) with Mobile parent view
4. Published → Cancelled (SF + BO) with Mobile parent view
5. **Cancelled → Draft** (SF + BO) + Mobile: "Parent does not see the lesson"
6. **Draft → Cancelled** (SF + BO) + Mobile: "Parent does not see the lesson"

**Issues:**

| # | Issue Type | Details |
|---|-----------|---------|
| 1 | MISSING_STEP | Qase step 5 "Change Cancelled → Draft" is entirely absent from automation. |
| 2 | MISSING_STEP | Qase step 6 "Change Draft → Cancelled" is entirely absent from automation. |
| 3 | EXPECTED_RESULT_FAIL | Each Qase step includes a Mobile sub-step "Parent login Mobile and view the lesson" — automation has NO Mobile verification for any status transition. |

**Verdict: ❌ Not Matching**

---

### Suite 260 — Assign/Unassign a teacher in lesson detail (PX-1216, PX-1218)

**Automation execution pattern (PX-1216):**
1. Precondition (lesson exists)
2. Add teacher via SF lesson detail
3. Verify teacher visible in SF
4. Verify teacher visible in BO

**Qase steps (PX-1216, 2 steps):**
1. Add teacher → Teacher appears in SF lesson detail
2. Check BO → Teacher appears in BO lesson detail

**Assessment:** Automation steps align correctly with Qase step definitions. Both SF and BO verifications are present. No extra steps. No missing steps.

**Verdict: ✅ Matching**

---

### Suite 326 — Collect Attendance on BO (PX-1919)

**Automation execution pattern (17 steps):**
- Verifies 5 attendance status values: Attend, Absent, Late Leave Early, Late, Leave Early
- For each status: sets via BO → verifies in BO → verifies in SF (2 platforms × 5 statuses = ~10 action+verify pairs)
- Additional setup/navigation steps

**Qase steps (6 steps, each with sub-steps):**
1. Precondition setup
2. Set "Attend" → Expected: status updated in BO, SF, **Mobile**; Attendance Note visible
3. Set "Absent" → Expected: same + Reason field verified
4. Set "Late Leave Early" → Expected: same + Notice field
5. Set "Late" → Expected: same + Notice field
6. Set "Leave Early" → Expected: same

**Issues:**

| # | Issue Type | Details |
|---|-----------|---------|
| 1 | MISSING_STEP × 5 | Each Qase step (2–6) contains sub-step "Login Mobile and view the attendance status" — NOT present in automation for any of the 5 status changes. |
| 2 | EXPECTED_RESULT_FAIL | Qase steps 3–6 include verifying Attendance Reason, Attendance Notice, and Attendance Note fields — automation does NOT log verification of these fields. |
| 3 | EXPECTED_RESULT_FAIL | Qase steps mention "student session tab in Lesson Allocation detail" verification — automation does NOT navigate to LA Detail. |

**Verdict: ❌ Not Matching**

---

### Suite 1649 — Assign/Unassign a student by Add student popup (PX-1263, PX-1265, PX-11538)

**Automation execution pattern (PX-1263, 4 steps):**
1. Precondition (lesson published, LA created)
2. Add student via SF "Add student" popup
3. Verify student visible in SF lesson detail
4. Verify student visible in BO lesson detail

**Qase steps (PX-1263, 6 steps):**
1. Add student via popup → Expected: lesson report detail auto-created for student
2. **Check lesson report of added student** → LR detail auto-created
3. **Check lesson allocation** → Lesson Allocated, LA Status, Report History updated
4. Login BO → student visible + LR created on BO
5. **Student login Mobile and view the lesson** → student sees lesson + LR
6. (Unassign variant from PX-1265) Unassign and verify removal

**Issues:**

| # | Issue Type | Details |
|---|-----------|---------|
| 1 | EXPECTED_RESULT_FAIL | Qase step 1 expected "lesson report detail is auto-created" — automation does NOT verify LR creation after student add. |
| 2 | MISSING_STEP | Qase step 2 "Check lesson report of added student" — no equivalent automation step. |
| 3 | MISSING_STEP | Qase step 3 "Check lesson allocation" (Lesson Allocated, LA Status, Report History) — NOT in automation. |
| 4 | MISSING_STEP | Qase step 5 "Student login Mobile and view the lesson" — NOT in automation. |

**Verdict: ❌ Not Matching**

---

### Suite 425 — Lesson Report List (SF) (PX-3144, PX-1377)

**Automation execution pattern (PX-3144 "bulk publish lesson report status", 3 steps):**
1. Navigate to Lesson Report list on SF
2. Click Publish button for a lesson
3. Verify LR status updated in BO

**Qase steps:**
1. Navigate to LR list and trigger publish
2. Verify "Lesson report update successfully" success message appears
3. Verify teacher BO list view shows updated status
4. **Verify student sees lesson report on Mobile**

**Issues:**

| # | Issue Type | Details |
|---|-----------|---------|
| 1 | EXPECTED_RESULT_FAIL | Qase step 2 "Lesson report update successfully" toast/message — automation does NOT verify success toast. |
| 2 | MISSING_STEP | Qase step 3 "Teacher BO list view" verification — automation only checks BO status value, not the teacher's BO list perspective. |
| 3 | MISSING_STEP | Qase step 4 "Student sees lesson report on Mobile" — entirely absent from automation. |

**Verdict: ❌ Not Matching**

---

### Suite 1748 — Lesson Report Detail (BO) (PX-13747, 13748, 13749, 13750)

**Automation execution pattern (PX-13748, 5 steps):**
1. Precondition (lesson + student created via API)
2. Navigate to BO lesson → open Lesson Report detail
3. Edit LR fields in BO (Content, Homework Assignment, Announcement, CM Note, Remark)
4. Verify BO Report Detail fields updated
5. Verify BO Student Report Detail fields (Homework Completion, CM Note, Remark)

**Qase steps (6 steps):**
1. Open Lesson Report detail page
2. **Edit LR fields in SF** (Content, Homework, Announcement, CM Note)
3. **Edit Student Report in SF** (Homework Completion, CM Note, Remark)
4. Publish Lesson Report from SF
5. Teacher login BO → verify fields updated
6. **Student login Mobile** → verify lesson report visible and correct

**Issues:**

| # | Issue Type | Details |
|---|-----------|---------|
| 1 | DEFINITION_MISMATCH | Qase steps 2–3 describe editing from **SF** first. Automation edits directly from **BO**. The editing platform is different from the definition. |
| 2 | MISSING_STEP | Qase step 6 "Student login Mobile and sees lesson report updated" — entirely absent from automation. |
| 3 | EXPECTED_RESULT_FAIL | Qase step 4 "Publish LR from SF" — automation does not perform the publish action; it only edits fields. No publish step in automation. |

**Verdict: ❌ Not Matching**

---

### Suite 290 — Trial Student in one-time lesson (PX-1479)

**Status: ❌ FAILED**

**Error message:**
```
Error: Grid has 0 row(s) but none matched [Student Name] = "ho hang01".
Check if the data was loaded by the UI.
```

**Evidence files:** `test-failed-1.png`, `error-context.md`, `video.webm`

**Root cause analysis:**
The lesson "1479Trial student to an one-time lesson_2509" was found successfully in Published status. The test failed when trying to find student "ho hang01" in the grid. The trial lesson allocation for "ho hang01" was not created or not visible at the time of test execution.

**Classification: INVALID** — Test data / environment issue. The prerequisite "ho hang01" student trial LA was not properly set up before the test ran. This is NOT a product defect or automation code bug.

**Verdict: ❌ Not Matching (INVALID — data issue)**

---

### Suite 1294 — Lesson Allocation assign by class (PX-10533)

**Status:** Passed (no step-results.json available)

**Case definition:** `automation=0` (manual/to-be-automated), 6 steps including Lesson Report check, Lesson Allocation update, BO verification, and Mobile student view.

**Note:** The result was submitted without a step-results attachment. Cannot compare execution vs. definition. Case is marked manual in Qase — if this was run via automation, it should be reclassified to `automation=2`.

**Verdict: ⚪ Unknown — no step-results available**

---

## 4. Issue Summary

### Issue Type Frequency

| Issue Type | Definition | Affected Suites |
|-----------|-----------|----------------|
| MISSING_STEP | A step defined in Qase is entirely absent from automation execution | 287, 325, 1649, 425, 1748 |
| EXPECTED_RESULT_FAIL | An expected result is not verified in automation (logged differently or omitted) | 218, 815, 287, 326, 1649, 425, 1748 |
| EXTRA_ACTION | Automation performs a step not in the Qase definition | 218, 815 |
| DEFINITION_MISMATCH | Automation flow contradicts the Qase step flow (wrong scope, wrong platform) | 815, 1748 |
| PRECONDITION_FAIL | Qase test actions are hidden inside the automation precondition/setup | 218 |
| DEFINITION_QUALITY | Qase step has insufficient expected result (image-only, no textual assertion) | 218 |
| INVALID | Test failed due to test data / environment issue, not product bug | 290 |

### Most Critical Gaps

1. **Mobile verification absent across all suites** — Suite 287, 326, 1649, 425, 1748 all define Mobile (student/parent) sub-steps that are completely missing from automation. This is a systemic gap.
2. **"Create Lesson" test flow bypasses UI** (~75 cases, Suite 218) — The lesson creation itself is done via API in the Precondition. Qase steps 1–2 (fill form, click Save) are never executed through the browser, meaning the create form UI is untested.
3. **Edit Lesson scope mismatch** (Suite 815) — Cases define "all lessons recalculated" (full chain) but automation uses "Only this lesson" scope. The recurring chain edit behavior is not tested as specified.
4. **Lesson Report checks absent** (Suites 1649, 1748, 425) — Multiple test cases defined to verify that LR is auto-created / updated / visible are missing from automation.

---

## 5. Execution Health

| Category | Count | % of LM cases |
|----------|-------|---------------|
| Clean pass | 110 | 96.5% |
| Passed after retry | 4 | 3.5% |
| Failed | 1 | 0.9% |
| Matching definition | 2 | 1.8% |
| Not matching definition | ~112 | 98.2% |

> Warning: 98.2% of Lesson Management cases have gaps between automation execution and Qase step definitions. The high pass rate gives a false sense of coverage quality. Actual test coverage is significantly lower than the definition describes.

---

## 6. Automation Status Updates

**Step 7 — Cases to update to automation=3 (In Review):**

After checking case definitions for representative cases across all suites:
- All analyzed cases are already at `automation=2` (Automated) or `automation=0` (Manual)
- **No cases are at `automation=3` (In Review)**

**No Qase automation status updates are required for this run.**

---

## 7. Recommendations

### High Priority

1. **Add Mobile verification steps** to automation for suites 287, 326, 1649, 425, 1748. Currently these steps are universally skipped, creating a coverage blind spot for the Mobile platform.

2. **Fix Edit Lesson scope** in Suite 815 — align automation `recalculatedImpact` value with Qase definition (full chain vs. single lesson). Re-check which behavior is actually intended and update either the automation or the Qase definition.

3. **Restore UI-driven Create Lesson flow** — If Suite 218 is meant to test the Create Lesson form, the automation should submit the form via browser interaction, not bypass it with API setup. Alternatively, split precondition setup cases from UI-interaction cases in Qase.

### Medium Priority

4. **Add Lesson Report creation verification** after student assignment (Suite 1649) and after LR publish (Suite 425).

5. **Update Lesson Report BO Detail automation** (Suite 1748) to match the Qase flow: edit from SF first, publish, then verify on BO — or update the Qase definition to reflect the BO-direct editing flow actually implemented.

6. **Add missing status transitions** Cancelled→Draft and Draft→Cancelled to Suite 287 automation.

### Low Priority

7. **Improve step logging** — Several automation steps produce `[INFO]` lines but no `[EXPECTED]` assertions. Add explicit `[EXPECTED]` log lines for each Qase expected result to allow automated comparison.

8. **Resolve PX-10533** (Suite 1294) no-step-results issue. If this was executed via Playwright, ensure the step-results.json attachment is submitted. Update `automation` field to `2` if appropriate.

9. **Fix PX-1479 test data** — Ensure "ho hang01" trial LA is provisioned before test execution. Trial LA setup should be part of the Precondition fixture for Suite 290 cases.

10. **Update Qase definition quality** — Suite 218 step 1 has image-only expected result. Replace with textual assertion criteria to enable comparison.

---

*Report generated by GitHub Copilot from Qase run PX-2375 analysis.*
*Lesson Management scope: Suite 192 and descendant suites.*
*Non-Lesson Management suites (Event Master, Activity Event) excluded.*
