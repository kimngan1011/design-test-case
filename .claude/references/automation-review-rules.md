# Automation Review — Deep-Check Rules

Mandatory checks applied during Step 5 of `review-automation-tests`. Apply ALL — do not skip any even if a step is marked ✅.

---

## Mandatory checks

### 1. Input values vs. Precondition Snapshot
- Read the Precondition Data Snapshot in `step-results.json` (JSON block after `[INFO] Precondition :`).
- Compare each field individually against what Qase step 1 specifies.
- Flag if automation uses a different value (e.g. wrong `lessonType`, `teachingMethod`, `skipCloseDate`).
- **False green**: `expectedValue = actualValue = WRONG_VALUE` passes green but tests the wrong thing — always trace back to the definition.

### 2. Expected results — check every sub-condition
- Each `expected_result` may contain multiple bullet sub-conditions. Trace one `[CHECK]`/`[PASS]`/`[INFO]` log per sub-condition.
- A sub-condition with no matching log is **not verified** → flag `⚠️ Partial`.
- **Negative assertions**: "User does NOT see X" needs an explicit absence check, not just presence of expected items.

### 3. Precondition vs. execution start state
- Compare Qase `preconditions` against what automation does in step 1.
- If automation creates/modifies precondition state inside a test step, flag `⚠️ Precondition setup embedded in test step`.
- Flag if precondition specifies attributes that don't exist before step 1.

### 4. Extra automation actions
- For each automation step, check if it does MORE than the Qase action.
- Common: adding students, creating data, navigating to extra screens, extra verification loops.
- Flag as `➕ Extra action (not in definition)`. Flag entire steps with no Qase counterpart.

### 5. Step action vs. automation step name
- Automation step name should correspond to Qase step action.
- Mismatched or vague names (e.g. "Verify BackOffice Details" covering 4 expected results) → flag as traceability gap.

### 6. Shallow verification — what is NOT logged
- "User sees all fields" requires field-level checks in the log.
- `[PASS] Pass SUCCESS: <step>` without field-level checks is shallow — list missing field checks.
- For BO/backend verification, confirm lesson code, lesson type (with correct value), report status, read-only attributes are ALL verified.

### 7. Lesson type verification (critical for Manabie)
- System has multiple similar types: `通常特訓`, `通常特訓（時間変更）`, etc.
- Extract `lessonType` from Precondition Snapshot and compare to Qase step 1 input.
- Extract `[PASS] Pass LessonType: [actual] vs [expected]` and compare BOTH to the Qase definition.
- A check showing `[actual] = [expected] = WRONG_TYPE` is a false green.

### 8. Definition quality issues
- Step action contains contradictory data (e.g. "Check Skip Closed Date" in a "No Skip" case).
- Expected result defined only as an image (no textual assertion).
- Multiple cases sharing the same step hash but different scenarios (copy-paste error).
- Note as `⚠️ Definition quality issue — requires correction in Qase`.

### 9. Defined vs. executed steps — beyond count (GAP-2)
- Do NOT rely on count alone. A count match can hide a missing step if automation runs an extra undocumented step.
- For each defined Qase step, confirm a corresponding automation step exists by position+action.
- Common miss: high-numbered step (mobile login, external API verification) absent while extra undocumented step keeps count equal.
- Flag as `MISSING_STEP` — more severe than count mismatch.

### 10. Silent skip log pattern (GAP-3)
- Scan every step log for skip-like messages before accepting PASSED:
  - `[INFO] I temporarily skipped the field`
  - `[WARN] skipping`, `cannot find this field`, `skipped due to`, "not found on form" followed by continuing execution.
- A PASSED step with a skip log is NOT verified.
- Flag `⚠️ Silent skip — <field/action> not verified`. Do not treat skip as a definition change.

### 11. Recurring lesson chain scope (GAP-7)
- Chain-scope selection requires verifying EACH affected lesson explicitly:
  - **Only this Lesson**: open every other lesson in chain, confirm change is ABSENT.
  - **This and following lessons**: open every lesson from selected to last, confirm change is PRESENT.
- Read precondition to count lessons in chain.
- Missing lesson checks = `SCOPE_AMBIGUITY` + `EXPECTED_RESULT_FAIL` combined.
- Required evidence: one `[CHECK] absent`/`[CHECK] present` log per relevant lesson.
- If Qase uses vague language ("other lessons", singular "the following lesson"), flag `DEFINITION_QUALITY` for explicit lesson-number scope.

---

## Verdict codes

| Code | Meaning |
|---|---|
| `DEFINITION_MISMATCH` | Executed steps don't match defined steps |
| `EXPECTED_RESULT_FAIL` | Defined sub-condition has no matching log line |
| `PRECONDITION_FAIL` | Precondition data wrong or missing |
| `EXTRA_ACTION` | Automation performs extra undocumented actions |
| `FLAKY` | Passed after retries with no code change |
| `INVALID` | Could not run due to environment/infra |
| `SCOPE_AMBIGUITY` | Vague scope prevents full verification |
| `DEFINITION_QUALITY` | Contradictory data, image-only result, copy-paste |
| `MISSING_STEP` | Defined step has no corresponding executed step |

---

## Operational notes

- Qase results API may return 293+ entries for 118 cases — deduplicate by `case_id` using latest `end_time`.
- `step-results.json` can be large (≤ 52KB) — focus on `[FAIL]`, `[ERROR]`, `[PASS] Pass SUCCESS` lines.
- `status=invalid` usually means env/infra, not test logic — note this distinction.
- Clean-pass cases with no retries: full step-by-step comparison is optional unless requested.

---

## Quality checklist (apply before finalizing report)

**Coverage:**
- Every test case appears in the Per-Suite Verification Table.
- Cases grouped by suite, not mixed across suites.
- "Checks Performed" column enumerates every individual check with ✅/⚠️/❌.
- Every ❌ Not Matching row has a detail block.
- Each detail block has both "What to Check" AND "How to Fix".
- Shared-step mismatches list the shared step hash + affected case IDs.

**PRECONDITION/ACTION/EXPECTED mapping:**
- Every `PRECONDITION:` compared against `case.preconditions`.
- Every `ACTION:` matched to `steps[N].action` by position.
- Every `EXPECTED:` matched to `steps[N].expected_result` (all sub-conditions).
- Unmapped entries listed in "⚠️ Unmapped Automation Test Cases" table.

**Deep checks:**
- Every sub-condition checked against a log line, not just overall status.
- Negative assertions verified with explicit absence check.
- `lessonType` in snapshot matches Qase step 1 value.
- `[PASS] Pass LessonType: [actual] vs [expected]` — BOTH match Qase definition.
- Extra automation actions within a step are flagged.
- Precondition state set up BEFORE step 1.
- Definition quality issues noted.
- Rule 9: every defined step has a corresponding executed step.
- Rule 10: every log scanned for silent skip messages.
- Rule 11: every individual lesson in chain scope explicitly verified.

**Automation status updates (Step 7):**
- Pre-update approval table shown before any API calls.
- Matching cases with "In Review" → updated to Automated (`automation=2`).
- Not Matching cases with "In Review" → updated to Manual (`automation=0`).
- Each update verified by re-fetching the case.
- All updates recorded in the "Automation Status Updates" table.
