---
name: generate-test-cases
description: >
  **WORKFLOW SKILL** — Generate structured test cases from a test coverage file.
  USE FOR: producing test cases after the coverage matrix is defined; writing preconditions,
  step actions, expected results, and test data; creating md and CSV output files.
  INPUT: test coverage file path `epics/<bucket>/<epic-folder>/test-coverage.md`.
  OUTPUT: `.md` + `.csv` test case files saved to `epics/<bucket>/<epic-folder>/test-cases/` matching the
  suggested suite structure from the coverage file.
  DO NOT USE FOR: analyzing requirements (use analyze-requirements skill) or defining coverage
  strategy (use define-test-coverage skill).
---

# Skill: Generate Test Cases

Senior QA automation architect. Convert a populated `test-coverage.md` into concrete test cases — one MD + one CSV per suite — saved alongside the epic's other artifacts.

## Input
- Coverage file: `epics/<bucket>/<epic-folder>/test-coverage.md`.
- Existing test cases in `epics/<bucket>/<epic-folder>/test-cases/` (to avoid duplicates).

## References
- Design rules (titles, language, actor, severity/priority, anchoring, fields) → `.claude/references/test-case-rules.md`
- Generation patterns per technique + depth/risk overrides → `.claude/references/test-case-generation-patterns.md`
- MD + CSV output template → `.claude/references/test-case-output-template.md`
- Qase CSV header reference → `.claude/references/qase-format.csv`
- Epic folder convention → `.claude/references/epic-folder-convention.md`

---

## Workflow

### Step 1 — Read inputs (parallel)
1. **Coverage file**, extract:
   - Section 1 Business Rules (numbered, with AC IDs)
   - Section 4 Coverage Strategy (AC → technique → risk → depth)
   - Section 5 High-Risk Areas
   - Section 6 Coverage Gaps (Overlap = Full → skip; ✅ → must cover)
   - Section 7 Suggested Test Suite Structure
2. **Design rules**: `.claude/references/test-case-rules.md`.
3. **Existing test cases** in `epics/<bucket>/<epic-folder>/test-cases/` — to avoid duplication.

### Step 2 — Apply design rules
Before writing any TC, internalize `.claude/references/test-case-rules.md`:
- Title format `[Feature] – [Sub-feature] – [Component] – Condition – Expected Behavior`.
- Forbidden words: Verify, Check, Test, Properly, Correctly, Successfully.
- One TC = one logical validation.
- OOP prefix `[TenantName]` for tenant-specific cases; Core has no prefix.
- Default actor `HQ or CM Staff` (NOT "Admin" unless explicit).
- Human-readable language; no jargon, API names, DB columns, selectors.

### Step 3 — Generate test cases per AC
Iterate each AC row in Section 4. For each:
1. Apply the technique pattern from `.claude/references/test-case-generation-patterns.md` (EP, BVA, Decision Table, State Transition, Pairwise, CRUD, Permission Matrix, Regression, Negative, Component, Scenario).
2. Honor **Coverage Depth** (Deep / Standard / Smoke) and **Risk Level** overrides (Critical/High always adds negative + boundary).
3. **Timezone coverage rule (MANDATORY)**: if the spec or AC references **any** time-related field — including but not limited to `start date`, `end date`, `start date time`, `end date time`, `lesson date`, `lesson time`, `schedule date/time`, `published date`, `created date`, or similar — you **MUST** generate test cases covering both **JST (Asia/Tokyo, UTC+9)** and **UTC** timezones. Specifically:
   - At least one TC where the date/time falls on a **date boundary** between JST and UTC (e.g., `2025-07-01 00:30 JST` = `2025-06-30 15:30 UTC` — different calendar dates in each timezone).
   - At least one TC confirming correct behavior when input/display uses JST while storage/API uses UTC (or vice-versa, per the system design).
   - Step Data must anchor **both** the JST and UTC representations explicitly (e.g., `lessonDate = 2025-07-01 00:30 JST (= 2025-06-30 15:30 UTC)`).
   - This rule applies regardless of Coverage Depth — even Smoke-level suites must include at least one timezone boundary TC when time fields are present.
4. **Skip rule**: if Section 6 marks Overlap = Full, do NOT regenerate — reference the existing TC ID.

### Step 4 — Write each test case
Produce every required field per `.claude/references/test-case-rules.md` §9:
- Title, Description (AC ID + technique + summary), Preconditions (with actor + explicit data), Step Actions, Step Results, Steps Data, Severity, Priority.
- **Severity/Priority mapping**: Critical→`critical`/`high`, High→`major`/`high`, Medium→`minor`/`medium`, Low→`trivial`/`low`. (`normal` is NOT a valid Qase slug.)
- **Test Data Anchoring Rule**: for any date/time/config-driven TC, Step 1's Test Data MUST declare base values (`today = YYYY-MM-DD; ...`); later steps show derived calculations. Forbidden vague values: "today/yesterday/tomorrow/near midnight/current config" without an anchor.

### Step 5 — Group into suites
Follow Section 7 of the coverage file. One `.md` file = one suite. Within each file, group cases under `## Suite: <Suite Name>`. Order: happy path → edge → negative → cross-system.

### Step 6 — Folder approval gate (MANDATORY before write)

Before writing any file, show the user the **proposed target folder + filenames** and wait for explicit approval. This prevents writing into the wrong epic, the wrong bucket, or under a stale folder structure.

Print this preview verbatim and STOP:

```
=== TEST CASE OUTPUT PREVIEW ===

Source coverage: epics/<bucket>/<epic-folder>/test-coverage.md
Target folder:   epics/<bucket>/<epic-folder>/test-cases/

Proposed files (<N> total: <N> .md + <N> .csv):
  - <filename-1>.md  /  <filename-1>.csv     (Suite: <Suite 1 Name>, <N> TCs)
  - <filename-2>.md  /  <filename-2>.csv     (Suite: <Suite 2 Name>, <N> TCs)
  ...

Reply:
- `approve` to write to the path above
- `move to <epics/<bucket>/<epic-folder>/test-cases/>` to override the target folder (e.g. different bucket, sub-folder, or different epic)
- `rename <old> -> <new>` to adjust a filename
- specific filenames to keep, others to skip
```

**Wait for the user's reply.** Do NOT write any file until the user explicitly approves.

- On **approve** → proceed to Step 7.
- On **move to ...** → update the target folder, re-print the preview with the new path, wait for approve.
- On **rename ...** → update the proposed filenames, re-print, wait for approve.
- On any other instruction → adjust and re-print. Loop until approved.

### Step 7 — Write the Markdown file
After approval, save to `<approved-folder>/<filename>.md` using the layout in `.claude/references/test-case-output-template.md`.

### Step 8 — Write the CSV file
Alongside the MD, save `<approved-folder>/<filename>.csv` using:
- Header row from `.claude/references/qase-format.csv`.
- Fixed field values + formatting rules from `.claude/references/test-case-output-template.md`.

---

## Quality gate

Before saving, verify (see `.claude/references/test-case-rules.md` for full rules):
- **Folder approval gate (Step 6) shown and explicitly approved** before any write.
- Every AC row in Section 4 has at least one TC.
- Every Critical/High risk area in Section 5 has at least one negative or boundary TC.
- Every ✅ "New Coverage Needed" gap in Section 6 is covered.
- No "Overlap = Full" rule has been duplicated.
- No title contains forbidden words.
- Every TC has concrete preconditions with explicit data + actor.
- Every date/time/config TC follows the Test Data Anchoring Rule (no vague values).
- **Timezone gate**: if the spec mentions any date/time field, at least one TC covers JST↔UTC date boundary conversion (Step 3 rule 3). Fail the gate if missing.
- Every step has a deterministic expected result and a data entry (may be `""`).
- Severity + priority match the Risk Level mapping.
- OOP/tenant TCs are prefixed `[TenantName]`.
- Language is human-readable — no jargon, API names, DB columns, selectors.
- Both `.md` and `.csv` are saved to the epic's `test-cases/` folder.

## Example invocation
```
Generate test cases from epics/<bucket>/LT-99999-feature-name/test-coverage.md
```
The skill reads the coverage file + design rules, applies technique-specific patterns per AC, builds the suite structure, then **presents the proposed folder + filenames and waits for user approval**. Only after approval, writes `.md` + `.csv` files under the approved folder.
