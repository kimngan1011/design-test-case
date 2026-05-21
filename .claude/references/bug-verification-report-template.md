# Bug Verification Report Template

Output format for `verify-bug` Step 7. Print directly in chat.

---

```markdown
## Bug Verification Report

**Bug:** <Bug summary>
**Ticket:** <Jira URL or "N/A">
**Env:** <env name> (<URL used>)
**Verified by:** Claude (Playwright automation)
**Date:** <today's date>

---

### Verdict: REPRODUCED / NOT REPRODUCED / PARTIALLY REPRODUCED

**Reason:** <One-sentence explanation>

---

### Steps Executed

| # | Action | Result |
|---|--------|--------|
| 1 | ... | Pass/Fail |
| 2 | ... | Pass/Fail |

---

### Actual Behavior Observed
<What actually happened during execution>

### Expected Behavior
<From the bug report>

### Console Errors (if any)
<Paste relevant console errors, or "None">

### Network Errors (if any)
<Paste relevant failed requests, or "None">

---

### Recommendation
- **If REPRODUCED:** Confirm bug is valid. Suggest assigning for fix.
- **If NOT REPRODUCED:** State possible reasons (env difference, already fixed, wrong steps).
- **If PARTIALLY REPRODUCED:** Describe which steps succeeded and which did not.
```
