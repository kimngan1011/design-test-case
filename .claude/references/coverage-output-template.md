# Coverage Output Template

Final structure for `epics/<epic-folder>/test-coverage.md`. Used by `define-test-coverage` Step 9.

---

```markdown
# Test Coverage: <TICKET-ID> — <Feature Name>

**Jira:** <Jira URL>
**Date:** <today's date>

---

## 1. Business Rules Extracted

| # | AC | Business Rule |
|---|------|---|
| 1 | AC XX.X | ... |

---

## 2. Logic Type Categorization

| AC | Business Rule # | Logic Type |
|---|---|---|
| AC XX.X | 1, 2 | ... |

---

## 3. Test Technique Selection

| Logic Type | Applicable Techniques |
|---|---|
| ... | ... |

---

## 4. Structured Coverage Strategy

| AC | Business Rule Summary | Logic Type | Test Technique | Risk Level | Coverage Depth |
|---|---|---|---|---|---|
| ... | ... | ... | ... | ... | ... |

---

## 5. High-Risk Areas Requiring Deeper Testing

### 🔴 Critical Risk

| Area | Reason | Recommended Approach |
|---|---|---|

### 🟠 High Risk

| Area | Reason | Recommended Approach |
|---|---|---|

### 🟡 Medium Risk

| Area | Reason | Recommended Approach |
|---|---|---|

---

## 6. Coverage Gaps vs. Existing Test Cases

| Gap Area | Existing Test Case | Overlap | New Coverage Needed |
|---|---|---|---|

---

## 7. Suggested Test Suite Structure

\`\`\`
epics/<epic-folder>/test-cases/
├── <file>.md → AC XX.X — <description>
\`\`\`
```
