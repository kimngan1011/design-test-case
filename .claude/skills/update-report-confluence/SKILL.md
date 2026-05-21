---
name: update-report-confluence
description: >
  **WORKFLOW SKILL** — Update QA Report on Confluence with test results from a Qase run.
  USE FOR: updating a Confluence QA Test Report page with acceptance test coverage, results
  from a Qase test run, and acceptance criteria from a Jira PBT ticket; adding a new row to
  the "Acceptance Test Coverage Summary & Result" table on an existing Confluence report page.
  INPUT: Jira ticket ID (LT-xxxxx), Confluence page ID or URL, Qase test run URL or run ID.
  OUTPUT: updated Confluence page with a new row in the acceptance test coverage table.
  DO NOT USE FOR: generating test cases (use generate-test-cases skill), analyzing requirements
  (use analyze-requirements skill), or importing to Qase (use import-to-qase skill).
---

# Skill: Update QA Report

Senior QA analyst. Append a new row to the "Acceptance Test Coverage Summary & Result" table on a Confluence QA report page, sourcing data from a Jira LT/PBT pair + a Qase test run + the epic's coverage file.

## Input
- Jira ticket — URL or ID (`LT-12345`).
- Confluence page — page ID or URL of the existing QA Test Report page.
- Qase test run — URL or `<project_code> run <id>` (e.g. `PX run 2187`).

## References
- Row preview + Result format + HTML template + insertion rule → `.claude/references/confluence-qa-report-template.md`

## Pre-flight
Before any work, confirm each of the 3 inputs with the user one by one. Only proceed after explicit confirmation of all three.

---

## Workflow

### Step 1 — Fetch LT + linked PBT ticket
1. `mcp_jira_jira_get_ticket(LT-...)`.
2. Find the linked PBT ticket from the LT's issue links (key `PBT-XXXX`).
3. `mcp_jira_jira_get_ticket(PBT-...)`.
4. Extract from the PBT ticket:
   - PBT item ID (e.g. `PBT-1303`).
   - Full Acceptance Criteria (all AC sections — Overview, Functional Requirements / User Stories, sub-sections).
5. Note the Qase public report link from the LT ticket comments (used later in Result column).

### Step 2 — Read the test coverage file
1. Locate `epics/LT-<id>-*/test-coverage.md`.
2. Read in full.
3. Summarize for the **Acceptance Test** column:
   - Coverage categories (e.g. Functional, Negative & validation, Permission & access, Data integrity, Integration).
   - Bullet the key areas covered per category.

### Step 3 — Fetch Qase run results
1. Parse the Qase input → project code + run ID.
2. `mcp_qase_get_run` → title, status, total/passed/failed/blocked/skipped, total cases.
3. `mcp_jira_jira_search` for Bug tickets under the LT epic (`issueType = Bug AND parentEpic = LT-<id>`). Count:
   - Total bugs detected.
   - Fixed = `Closed` status.
   - Unresolved = `New` status.
4. Compose the **Result** column content using the format in `.claude/references/confluence-qa-report-template.md` § Result column format.

### Step 4 — Preview row for user review
Show the row preview using the table in `.claude/references/confluence-qa-report-template.md` § Row preview. Ask: **"Does this look correct? Should I update the Confluence page now?"** Only proceed after explicit confirmation.

### Step 5 — Read current Confluence page
1. `mcp_confluence_confluence_get_page` with `body.storage`.
2. Parse HTML to find the **"Acceptance Test Coverage Summary & Result"** table.
3. **Use nesting-aware parsing** (see § Insertion rule in the reference). The Acceptance Test cells contain nested tables — track `<table>`/`</table>` depth to find the OUTER `</tbody>`.
4. Count outer-level `<tr>` rows (depth = 1) → determine next row number.
5. Find the last numbered row — insert new row immediately after.

### Step 6 — Build the new `<tr>` HTML
Use the HTML template in `.claude/references/confluence-qa-report-template.md` § HTML row template — exactly 7 `<td>` cells. Apply the cell formatting rules for Acceptance Criteria, Acceptance Test, and Result cells.

### Step 7 — Update the page
1. Insert the new `<tr>` after the last numbered row in the OUTER table (NOT inside any nested table).
2. `mcp_confluence_confluence_update_page` — increment version by 1; keep title + space key unchanged.
3. Confirm success to the user with the updated page URL.

---

## Quality checks
- PBT key correctly extracted from LT issue links.
- Acceptance Criteria complete (all ACs from PBT).
- Acceptance Test summary reflects the coverage file accurately.
- Test case count + pass/fail/blocked match Qase run stats.
- Row number correct (no duplicates, no gaps).
- HTML well-formed; nested tables preserved.
- User explicitly confirmed row content before write.

## Error handling
- No coverage file found → ask user: proceed without Acceptance Test summary, or run define-test-coverage first.
- Qase run not found or still in progress → ask: wait or proceed with partial data.
- Confluence update fails (stale version) → re-fetch page, retry with latest version.
