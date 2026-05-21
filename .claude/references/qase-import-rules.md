# Qase Import Rules

Field mapping, multi-line formatting, and report template for `import-to-qase`.

---

## Field mapping (Step 5)

| Field | Source | Rules |
|---|---|---|
| `title` | TC title | Max 255 chars; strip markdown. |
| `description` | Description | Plain text; strip markdown bold/italic. |
| `preconditions` | Preconditions block | Plain text; preserve bullet structure as newlines. |
| `steps` | Table rows | Array of `{ action, expected_result, data }` objects. |
| `suite_id` | Resolved Qase suite ID | Integer. |
| `severity` | Severity field | Map: critical→critical, major→major, normal→**minor**, minor→minor. (`normal` is NOT a valid Qase slug.) |
| `priority` | Priority field | high→high, medium→medium, low→low. |
| `type` | Fixed | `functional` |
| `behavior` | Fixed | `undefined` |
| `automation` | Fixed | `is-not-automated` |
| `status` | Fixed | `draft` |
| `is_flaky` | Fixed | `false` |
| `layer` | Fixed | `unknown` |
| `steps_type` | Fixed | `classic` |

### Step object format
Each step is `{ action: "...", expected_result: "...", data: "..." }`:
- `action` = Action column value.
- `expected_result` = Expected Result column value.
- `data` = Test Data column value (`""` if blank).

---

## Multi-line content rule (CRITICAL)

When any field contains multiple items or lines (preconditions, description, step action/result/data):

1. **Use real newlines** — text sent to Qase MUST contain actual newline chars, NOT the literal two-char string `\n` or `/n`.
2. **Sanitize before import** — scan every text field for literal `\n`, `/n`, or `\\n` and replace with real newlines.
3. **Preserve list structure** — bullets (`- item`) and numbered (`1. item`) stay as separate lines joined by real newlines.
4. **HTML alternative** — if the API accepts HTML, use `<br>` tags. Prefer `<br>` when the field renders as HTML in Qase UI.
5. **Verify after import** — `mcp_qase_get_case` for at least one case to confirm line breaks render correctly (no literal `\n` text visible).

---

## Import summary template (Step 9)

```markdown
## Import Summary

**Project:** <project code>
**File:** <file path>
**Date:** <today's date>

### Suites
| Suite Name | Status | Qase Suite ID |
|---|---|---|
| Extend Recurrence Button | Created | 101 |
| Extend Recurrence Form | Existed | 88 |

### Test Cases
| Title | Suite | Status | Qase Case ID |
|---|---|---|---|
| Extend Recurrence Button – Recurring Lesson – Button Visible | Extend Recurrence Button | Created | 1042 |
| Extend Recurrence Form – Date Field – Auto-calculated | Extend Recurrence Form | Skipped (duplicate) | — |

### Totals
- Suites created: X
- Suites already existed: X
- Test cases created: X
- Test cases skipped (duplicates): X
- Test cases failed: X
```
