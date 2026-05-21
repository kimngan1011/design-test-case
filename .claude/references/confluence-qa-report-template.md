# Confluence QA Report Row Template

Used by `update-report-confluence` Steps 4–6 to build the new row inserted into the "Acceptance Test Coverage Summary & Result" table.

---

## Row preview (Step 4 — user review)

Show this BEFORE updating Confluence:

| Column | Content |
|---|---|
| **#** | (next row number — determined from existing table) |
| **Team** | Lesson |
| **PBT item** | `<PBT ticket key>` (linked to Jira) |
| **Acceptance Criteria** | (full AC text from PBT ticket) |
| **Acceptance Test** | (coverage summary from test-coverage file) |
| **Result** | (test run results — see "Result column format" below) |

Ask: **"Does this look correct? Should I update the Confluence page now?"** Only proceed after explicit confirmation.

---

## Result column format (Step 3)

```
Create new test cases: X test cases

Completion rate: 100%
  - X of total test cases
  - Status: Passed

Total bugs detected: X bugs
  - # of Fixed: X (Closed status)
  - # of Unresolved: X (New status)

Environment:
  - STAG: <Qase public report link from Jira comment>
```

---

## HTML row template (Step 6)

Build a `<tr>` with **exactly 7 `<td>` cells** (matches 7-column header: `#`, Team, PBT item, Acceptance Criteria, Acceptance Test, Result, QA sign-off):

```html
<tr>
  <td><p>#</p></td>
  <td><p>Lesson</p></td>
  <td>
    <p>
      <ac:structured-macro ac:name="jira" ac:schema-version="1">
        <ac:parameter ac:name="key">PBT-XXXX</ac:parameter>
        <ac:parameter ac:name="serverId">69f9f6ff-fc4f-3917-b2ad-1f1d53e3704b</ac:parameter>
        <ac:parameter ac:name="server">System Jira</ac:parameter>
      </ac:structured-macro>
    </p>
  </td>
  <td><!-- Acceptance Criteria --></td>
  <td><!-- Acceptance Test summary --></td>
  <td><!-- Result --></td>
</tr>
```

### Cell formatting rules

**Acceptance Criteria cell:**
- `<h2>` for major section headers (Overview, Functional Requirements, etc.).
- `<p>` for body text.
- `<ul><li>` for bulleted lists.
- Preserve original structure from the Jira ticket.

**Acceptance Test cell:**
- Headers per coverage category.
- Bullet lists for areas covered.
- Summary stats at bottom (total test cases, completion rate).

**Result cell:**
- `<p>` for each section in the Result format above.
- `<ul><li>` for sub-items.
- `<a href="...">` for the STAG environment link.

---

## Insertion rule (CRITICAL — Step 7)

The Acceptance Test Coverage table can contain **nested tables** inside its cells. Naive search for `</tbody>` or `</table>` will hit the inner table first and corrupt the page.

- **Use nesting-aware depth tracking** — increment on `<table>`, decrement on `</table>`. Find the outer `</tbody>` at depth = 0.
- Count outer-level `<tr>` rows only (depth = 1) to determine the next row number.
- Find the last numbered row (its first `<td>` contains a number) and insert the new `<tr>` immediately after it.
- Do NOT use simple `body.find('</tbody>')` — it matches nested tables.
