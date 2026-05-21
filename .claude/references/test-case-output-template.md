# Test Case Output Template

Output layout for `generate-test-cases` Steps 6–7. Two files per suite, saved alongside each other:

```
epics/<epic-folder>/test-cases/<filename>.md
epics/<epic-folder>/test-cases/<filename>.csv
```

---

## Markdown template

```markdown
# Test Cases: <TICKET-ID> — <Feature Name>

## Suite: <Suite Name>

### <Test Case Title>

**Description:** <AC ID> — <Technique> — <one-sentence summary>

**Preconditions:**
<bullet list of preconditions with explicit test data and actor>

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | ... | ... | ... |
| 2 | ... | ... | ... |

**Severity:** <critical / major / minor / trivial>
**Priority:** <high / medium / low>

---
```

---

## Qase CSV format

Header row (see `.claude/references/qase-format.csv` for the full template):

```
v2.id,title,description,preconditions,postconditions,tags,priority,severity,type,behavior,
automation,status,is_flaky,layer,steps_type,steps_actions,steps_result,steps_data,
milestone_id,milestone,suite_id,suite_parent_id,suite,suite_without_cases,parameters,is_muted
```

### Fixed field values for every row

| Field | Value |
|---|---|
| `type` | `functional` |
| `behavior` | `undefined` |
| `automation` | `is-not-automated` |
| `status` | `draft` |
| `is_flaky` | `no` |
| `layer` | `unknown` |
| `steps_type` | `classic` |

### Formatting rules

- Escape commas inside text fields with double-quotes.
- Steps (actions/results/data) are newline-separated using `\n` inside the cell.
- Each step value is wrapped in double-quotes: `"1. ""Step action here"""`.
- Do NOT include markdown formatting inside CSV cells.
- Do NOT include explanation rows outside data rows.
- One CSV row per test case.
