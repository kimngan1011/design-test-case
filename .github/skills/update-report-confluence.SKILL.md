---
description: >
  **WORKFLOW SKILL** — Update QA Report on Confluence with test results from a Qase run.
  USE FOR: updating a Confluence QA Test Report page with acceptance test coverage, results
  from a Qase test run, and acceptance criteria from a Jira PBT ticket; adding a new row to
  the "Acceptance Test Coverage Summary & Result" table on an existing Confluence report page.
  INPUT: Jira ticket ID (LT-xxxxx), Confluence page ID or URL, Qase test run URL or run ID.
  OUTPUT: updated Confluence page with a new row in the acceptance test coverage table.
  DO NOT USE FOR: generating test cases (use generate-testcases skill), analyzing requirements
  (use analyze-requirements skill), or importing to Qase (use import-to-qase skill).
---

# Skill: Update QA Report

You are a senior QA analyst updating the QA Test Report on Confluence for the Manabie lesson-management system.

---

## Input

- **Jira ticket** — URL or ID (e.g. `LT-12345` or `https://manabie.atlassian.net/browse/LT-12345`)
- **Confluence page** — page ID or URL of the existing QA Test Report page (e.g. `2331312239` or full URL)
- **Qase test run** — URL or run ID + project code (e.g. `https://app.qase.io/run/PX/dashboard/2187` or `PX run 2187`)

---

## Pre-flight: Review All Inputs with User

**Before doing any work**, confirm the inputs with the user:

1. Display the Jira ticket ID and ask: "Is this the correct PBT ticket?"
2. Display the Confluence page URL and ask: "Is this the correct QA Test Report page to update?"
3. Display the Qase run ID and project code and ask: "Is this the correct test run?"

Only proceed after the user confirms all three inputs.

---

## Workflow

### Step 1 — Fetch the Jira LT Ticket and Linked PBT Ticket (Acceptance Criteria)

1. Extract the Jira ticket ID from the input (e.g. `LT-90573`).
2. Use `mcp_jira_jira_get_ticket` to fetch the LT ticket.
3. Find the **linked PBT ticket** — the PBT item is always linked from the LT ticket. Look in the ticket's issue links for a `PBT-XXXX` key.
4. Use `mcp_jira_jira_get_ticket` again to fetch the **PBT ticket** by its key.
5. Extract from the PBT ticket:
   - **PBT item ID** (e.g. `PBT-1303`)
   - **Full Acceptance Criteria** — all AC sections from the PBT ticket description. This includes Overview, Functional Requirements / User Stories, and any sub-sections.
6. Store the full AC text — this will go into the **Acceptance Criteria** column.

### Step 2 — Read the Test Coverage File (Acceptance Test)

1. Search `output/test-coverages/` for a file matching the Jira ticket ID (e.g. `LT-90573-*.md`).
2. Read the full coverage file.
3. Summarize the test coverage into a concise report for the **Acceptance Test** column. The summary should include:
   - **Coverage categories** (e.g. Functional, Negative & validation, Permission & access, Data integrity, Integration)
   - For each category, list the key areas covered (bullet points)

### Step 3 — Fetch Qase Test Run Results (Result)

1. Parse the Qase input to extract the **project code** and **run ID**.
2. Use `mcp_qase_get_run` to fetch the run summary:
   - Get: title, status, total/passed/failed/blocked/skipped stats
   - Get the **total number of test cases** from the run stats
3. Use `mcp_jira_jira_search` to find all **Bug** tickets under the LT epic (e.g. `issueType = Bug AND parentEpic = LT-XXXXX`). Count:
   - **Total bugs detected** = total bug count
   - **# of Fixed** = bugs with `Closed` status
   - **# of Unresolved** = bugs with `New` status
4. Get the Qase public report link from the Jira ticket comment (already extracted in Step 1).
5. Compose the **Result** column content using this exact format:

```
Create new test cases: X test cases

Completion rate: 100%
  - X of total test cases
  - Status: Passed

Total bugs detected: X bugs
  - # of Fixed: X
  - # of Unresolved: X

Environment:
  - STAG: <Qase public report link from Jira comment>
```

### Step 4 — Preview the Row for User Review

Before updating Confluence, present the composed row to the user in a table format:

| Column                  | Content                                                          |
| ----------------------- | ---------------------------------------------------------------- |
| **#**                   | _(next row number — will be determined from the existing table)_ |
| **Team**                | Lesson                                                           |
| **PBT item**            | `<PBT ticket key>` (linked to Jira)                              |
| **Acceptance Criteria** | _(full AC text from Step 1)_                                     |
| **Acceptance Test**     | _(coverage summary from Step 2)_                                 |
| **Result**              | _(test run results from Step 3)_                                 |

Ask the user: **"Does this look correct? Should I update the Confluence page now?"**

Only proceed after explicit confirmation.

### Step 5 — Read the Current Confluence Page

1. Use `mcp_confluence_confluence_get_page` to fetch the current page content (with `body.storage`).
2. Parse the HTML body to find the **"Acceptance Test Coverage Summary & Result"** table.
3. **CRITICAL: Use nesting-aware parsing** to find the OUTER table boundaries. The acceptance test cells may contain nested `<table>` elements. Track `<table>` / `</table>` depth to find the correct outer `</tbody>`.
4. Count outer-level `<tr>` rows only (depth = 1) to determine the next row number.
5. Find the **last numbered row** (the last `<tr>` whose first `<td>` contains a number) and insert the new row immediately after it.

### Step 6 — Build the New Table Row HTML

Construct the new `<tr>` element with **exactly 7 `<td>` cells** matching the 7-column header (#, Team, PBT item, Acceptance Criteria, Acceptance Test, Result, QA sign-off):

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
  <td><!-- Acceptance Criteria content --></td>
  <td><!-- Acceptance Test summary --></td>
  <td><!-- Result content --></td>
</tr>
```

**Formatting rules for the Acceptance Criteria cell:**

- Use `<h2>` for major section headers (Overview, Functional Requirements, etc.)
- Use `<p>` for body text
- Use `<ul><li>` for bulleted lists
- Preserve the original structure from the Jira ticket

**Formatting rules for the Acceptance Test cell:**

- Use headers for each coverage category
- Use bullet lists for areas covered
- Include summary stats at the bottom (total test cases, completion rate)

**Formatting rules for the Result cell:**

Use this exact structure:

```
Create new test cases: X test cases

Completion rate: 100%
  - X of total test cases
  - Status: Passed

Total bugs detected: X bugs
  - # of Fixed: X (Closed status)
  - # of Unresolved: X (New status)

Environment:
  - STAG: <link to Qase public report from Jira comment>
```

- Use `<p>` for each section
- Use `<ul><li>` for sub-items
- Use `<a href="...">` for the STAG environment link

### Step 7 — Update the Confluence Page

1. Insert the new `<tr>` **after the last numbered row** in the outer table (NOT inside any nested table).
2. **Do NOT use simple `find('</tbody>')` or `find('</table>')` — these will match nested tables.** Always use nesting-aware depth tracking to find the correct outer insertion point.
3. Use `mcp_confluence_confluence_update_page` to push the updated content.
   - Increment the version number by 1.
   - Keep title and space key unchanged.
4. Confirm success to the user with the updated page URL.

---

## Quality Checks

Before updating the Confluence page, verify:

- [ ] PBT item key is correctly extracted from the LT ticket's links
- [ ] Acceptance Criteria is complete (all ACs from the PBT ticket)
- [ ] Acceptance Test summary accurately reflects the test coverage file
- [ ] Test case count matches the Qase run stats
- [ ] Test run results (pass/fail counts) match the Qase run data
- [ ] Row number is correct (no duplicates, no gaps)
- [ ] HTML is well-formed and won't break the existing table
- [ ] User has explicitly confirmed the row content

---

## Error Handling

- **No test coverage file found:** inform the user and ask if they want to proceed without the Acceptance Test summary, or run the define-test-coverage skill first.
- **Qase run not found or still in progress:** inform the user and ask whether to wait or proceed with partial data.
- **Confluence page update fails:** show the error, check if the version number is stale (another edit happened), and retry with the latest version.
