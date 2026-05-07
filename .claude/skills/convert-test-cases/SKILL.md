---
name: convert-test-cases
description: >
  **WORKFLOW SKILL** — Convert test cases from Qase, Markdown, or user description into
  structured JSON format for automation execution.
  USE FOR: converting test cases from any source into JSON; saving to input/test-cases/ for reuse.
  INPUT: Qase case URL/ID, local MD file path, or manual test case description in chat.
  OUTPUT: JSON file saved to input/test-cases/<module>/<feature>.json.
  DO NOT USE FOR: executing test cases (use execute-test-cases); generating new test cases
  from requirements (use generate-test-cases).
argument-hint: "Qase case URL, MD file path, or describe test steps directly"
---

# Skill: Convert Test Cases to JSON

You are a senior QA engineer. Convert test cases from any source into structured JSON
for automated execution via Playwright.

**Before starting, read the format specification:**
`input/templates/automation-json-format.md` — contains JSON schema, action types, and
NL-to-action mapping rules. This is the single source of truth for the output format.

---

## Workflow

### Step 1 — Determine Source

Parse user's message for source type:
- **Qase URL/ID** — contains `qase.io` or pattern `PX-1234`, `LM-567`
- **MD file path** — ends with `.md`
- **User description** — numbered steps or natural language in chat

If unclear, ask in ONE prompt.

### Step 2 — Fetch Raw Test Cases

- **Qase:** `mcp_qase_get_case` (single) or `mcp_qase_list_cases` (suite) → extract title, preconditions, steps
- **MD file:** Read → parse headings + step tables
- **User description:** Parse numbered steps from message

### Step 3 — Convert to JSON

Follow the mapping rules in `input/templates/automation-json-format.md`:
1. Map each NL action → action type (click/fill/select/navigate/verify...)
2. Extract `role` from preconditions (default: `CM`)
3. Extract `start_url` from first navigate step if present
4. Set `expected` to null for action-only steps
5. Assign severity from Qase data or infer
6. Generate sequential IDs (`TC-001`, `TC-002`, ...) or use Qase IDs

### Step 4 — Save File

1. Determine path: `input/test-cases/<module>/<feature>.json`
   - If unsure about module/feature, ask user
2. Show preview of first 2 cases
3. Ask user to confirm path and content
4. Save file
5. Output summary with ready-to-run command:
   ```
   Saved N test cases to input/test-cases/<module>/<feature>.json
   Ready: /execute-test-cases input/test-cases/<module>/<feature>.json on <env>
   ```

---

## Quality Checks

- [ ] Every step has a valid action type
- [ ] Steps needing verification have `expected` populated
- [ ] `role` extracted correctly
- [ ] File saved to `input/test-cases/`
- [ ] JSON is valid

---

## Examples

> `/convert-test-cases` https://app.qase.io/case/PX-1234

> `/convert-test-cases` output/test-cases/lesson-management/lesson/create-lesson/create-lesson-list.md

> `/convert-test-cases`
> Title: Create lesson | Role: CM | Steps: 1. Navigate to Lesson List 2. Click Create 3. Fill name "Test" 4. Click Save | Expected: Lesson created
