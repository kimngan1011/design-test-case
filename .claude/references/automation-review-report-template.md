# Automation Review — Report Template

Save the final report to: `reports/automation-reviews/<project>-run-<run_id>-review.md`

(Example: `reports/automation-reviews/PX-run-2187-review.md`)

---

## Template

```markdown
# Automation Test Run Review

**Project:** <PROJECT>
**Run ID:** <RUN_ID>
**Run Title:** <title>
**Run Date:** <start_time>
**Reviewed By:** GitHub Copilot
**Review Date:** <today>

---

## Summary

| Metric                 | Value |
| ---------------------- | ----- |
| Total Cases            | N     |
| Passed (clean)         | N     |
| Passed (after retries) | N     |
| Failed                 | N     |
| Invalid/Blocked        | N     |
| Matching               | N     |
| Not Matching           | N     |

---

## Per-Suite Verification Table

One row per test case, organized by suite.

| Suite | Test Case | Checks Performed | Verdict |
|-------|-----------|------------------|---------|
| <Suite> | PX-<id>: <title> | Preconditions ✅ · Step coverage ✅ · Step actions ✅ · Expected results ✅ · Unmapped entries ✅ · No extra actions ✅ | ✅ Matching |
| <Suite> | PX-<id>: <title> | Preconditions ✅ · Step coverage ✅ · Step actions ✅ · Expected results ⚠️ · Unmapped entries ⚠️ · No extra actions ✅ | ❌ Not Matching |

> "Checks Performed" must enumerate every individual check with ✅/⚠️/❌.

---

## ⚠️ Unmapped Automation Test Cases

| Suite | Case ID | Step Position | Unmapped Entry Type | Content (truncated) | Impact |
|-------|---------|---------------|---------------------|---------------------|--------|
| <Suite> | PX-<id> | Step N | ACTION / EXPECTED | `<first 80 chars>` | No defined step to trace this back to |

> Only list cases with at least one unmapped entry.

---

## Not Matching Cases — Detail

For each ❌ row, provide a detail block:

### <Suite> — PX-<id>: <title>

**Verdict:** Not Matching
**Mismatch type(s):** DEFINITION_MISMATCH | EXPECTED_RESULT_FAIL | PRECONDITION_FAIL | EXTRA_ACTION | FLAKY | INVALID | SCOPE_AMBIGUITY | DEFINITION_QUALITY | MISSING_STEP

#### What to Check in the Test Run
- Step N: <which log line/section shows the problem>
- Paste evidence:
  ```
  [FAIL] <log line>
  [ERROR] <log line>
  ```
- Missing check: state which sub-condition has no matching log line.
- False green: show `expectedValue` vs `actualValue` in Precondition Snapshot and explain why both are wrong.

#### How to Fix the Test Case Definition
- Qase field to update: `preconditions` | `step N action` | `step N expected_result`.
- Current wording: > "User does not see the teacher is added to other lessons in the chain"
- Should be: > "User does not see the teacher in lessons 1, 3, and 4 (only the selected lesson 2 is affected)"
- If it touches a shared step, note this — the fix propagates to all using cases.
- If a new/split step is needed, describe the new structure.

---

## Cases with Issues (Technical)

### ❌ Failed Cases

#### PX-<id>: <title>
- **Suite:** <suite>
- **Final Status:** FAILED
- **Retries:** N
- **Step that failed:** <step name>
- **Failure evidence:**
  ```
  [FAIL] <log line>
  [ERROR] <log line>
  ```
- **Expected result (definition):** <text>
- **Assessment:** EXPECTED_RESULT_FAIL | PRECONDITION_FAIL | DEFINITION_MISMATCH

### ⚠️ Flaky Cases (passed after retries)

#### PX-<id>: <title>
- **Suite:** <suite>
- **Retry history:** failed → failed → passed
- **Step that was unstable:** <step name>
- **Assessment:** FLAKY — recommend investigation

### ✅ Clean Pass Cases

| Case ID | Title | Steps | Duration |
|---------|-------|-------|----------|
| PX-<id> | <title> | N | Xs |

---

## Automation Status Updates

| Case ID | Title | Verdict | Updated To | Method | Date |
|---------|-------|---------|-----------|--------|------|
| PX-<id> | <title> | ✅ Matching | Automated | API / UI | YYYY-MM-DD |
| PX-<id> | <title> | ❌ Not Match | Manual | API / UI | YYYY-MM-DD |

---

## Recommendations

- Specific cases to re-run or investigate.
- Environment issues if patterns suggest infra instability.
- Test case definition updates if mismatches found.
- For shared-step fixes: list the shared step hash + all affected case IDs.
```
