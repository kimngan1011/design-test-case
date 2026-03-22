---
description: >
  **WORKFLOW SKILL** — Generate structured test cases from a test coverage file.
  USE FOR: producing test cases after the coverage matrix is defined; writing preconditions,
  step actions, expected results, and test data; creating md and CSV output files.
  INPUT: test coverage file path from `output/test-coverages/` + test-case-rules.md.
  OUTPUT: `.md` test case file saved to `output/test-cases/` matching the suggested suite
  structure from the coverage file.
  DO NOT USE FOR: analyzing requirements (use analyze-requirements skill) or defining coverage
  strategy (use define-test-coverage skill).
---

# Skill: Generate Test Cases

You are a senior QA automation architect working on the Manabie lesson-management system.

---

## Input

- **Coverage file** — path to a coverage `.md` in `output/test-coverages/` (e.g. `output/test-coverages/LT-90573-extend-recurring-lesson.md`)
- **Rules file** — always read `input/templates/test-case-rules.md` before writing any test case

---

## Workflow

### Step 1 — Read All Required Files

Read the following files in parallel before writing a single test case:

1. The **coverage file** — extract:
   - Section 1: Business Rules table (all numbered rules with AC IDs)
   - Section 4: Coverage Strategy table (AC → technique → risk level → depth)
   - Section 5: High-Risk Areas
   - Section 6: Coverage Gaps (to know what is NOT yet covered by existing TCs)
   - Section 7: Suggested Test Suite Structure (folder/file layout to follow)

2. `input/templates/test-case-rules.md` — internalize all design rules before writing a single test case title or step. Rules must be applied throughout.

3. **Existing test cases** in the same feature folder (from the suite structure in Section 7) — to avoid duplicating coverage already present.

---

### Step 2 — Apply Test Case Design Rules

Before generating any test case, enforce these rules from `test-case-rules.md`:

**Title format:**

```
[Feature] – [Sub-feature] – [Component] – Condition – Expected Behavior
```

Examples:

- `Extend Recurrence Form – Date Field – End Date + 7 Days – Auto-calculated and non-editable`
- `Extend Recurrence – New Lessons – Duplicate Date Exists – Lesson not created for that date`

**Forbidden title words:** Verify, Check, Test, Properly, Correctly, Successfully

**One test case = one logical validation** — do not combine two business rules or two conditions into a single test case.

**Avoid UI-only test cases** — the test must represent a user scenario, system behavior, or business rule.

**OOP prefix rule:**

- Core tests → no prefix
- Tenant-specific tests (Nichibei, Renseikai, etc.) → prefix with `[TenantName]`

---

### Step 3 — Generate Test Cases per AC

Work through each AC row in the Coverage Strategy table. For each AC:

1. **Check the test technique** and apply the correct generation pattern:

| Technique                    | Generation pattern                                                                                            |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------- |
| **Equivalence Partitioning** | One TC per valid partition + one TC per invalid partition                                                     |
| **Boundary Value Analysis**  | TC for: exact boundary (reject), one below boundary (reject), one above boundary (accept), far above (accept) |
| **Decision Table**           | One TC per meaningful combination of conditions and outcomes                                                  |
| **State Transition Testing** | TC for each valid transition + TC for each invalid/blocked transition                                         |
| **Pairwise Testing**         | Construct the minimum set of combinations that covers all pairs of input values                               |
| **CRUD Testing**             | TC for Create, Read, Update, Delete — include happy path and conflict/error path                              |
| **Permission Matrix**        | One TC per role per action (allowed + denied)                                                                 |
| **Regression Analysis**      | Identify existing TC IDs at risk; write new TCs that exercise the changed flow                                |
| **Negative Testing**         | TC for each invalid input, blocked action, or error state                                                     |

2. **Check Coverage Depth** (from Section 4 of coverage file):
   - `Deep` → generate BVA boundaries, multiple decision table rows, cross-surface verifications
   - `Standard` → happy path + 1–2 negative cases
   - `Smoke` → primary happy path only

3. **Check Risk Level**:
   - `Critical` / `High` → always generate negative and boundary test cases even if not the primary technique
   - `Medium` / `Low` → stick to the selected technique at standard depth

4. **Skip rules:** Do NOT generate a test case for a business rule that is already fully covered by an existing TC listed in Section 6 (Overlap = Full).

---

### Step 4 — Write Each Test Case

For each test case, produce all of the following fields. No field may be left blank unless explicitly marked optional.

#### Title

Follow format: `[Feature] – [Sub-feature] – Condition – Expected Behavior`

- Concise, specific, no forbidden words
- Must describe the observable outcome, not the action being performed

#### Description

- Reference the AC ID (e.g. `AC 01.2`)
- Name the test technique used (e.g. `BVA`, `Decision Table`, `Negative Testing`)
- One sentence describing what this test case validates

#### Preconditions

- List all system state requirements before the test starts
- Include specific test data values that must exist (user role, entity state, field values)
- Use bullet points; be explicit — "Admin has created a recurring lesson schedule with End Date = 2026-03-10"

#### Step Actions

- Number each step
- Each step = one atomic user action or system trigger
- Use present tense: "Open...", "Click...", "Enter...", "Navigate to..."
- Include the exact value the user enters in the step (or reference Steps Data)

#### Step Results (Expected Results)

- One result per step
- State the exact observable outcome: field value, UI element state, status label, error message text
- Be deterministic — "Date field shows 2026-03-17" not "Date field is correct"

#### Steps Data

- One data entry per step (can be empty string `""` if no data for that step)
- For BVA: state the exact boundary value being used
- For Decision Table: state the combination being tested

#### Severity

Map from Risk Level in the coverage file:

| Risk Level | Severity |
| ---------- | -------- |
| Critical   | critical |
| High       | major    |
| Medium     | normal   |
| Low        | minor    |

#### Priority

Map from Risk Level:

| Risk Level | Priority |
| ---------- | -------- |
| Critical   | high     |
| High       | high     |
| Medium     | medium   |
| Low        | low      |

---

### Step 5 — Group Test Cases into Suites

Follow the **Suggested Test Suite Structure** from Section 7 of the coverage file.

- Each `.md` file = one suite
- Within each file, group test cases under `## Suite: <Suite Name>` headings
- Order test cases: happy path → edge cases → negative cases → cross-system

---

### Step 6 — Write the Markdown Output File

Save the `.md` file to the path specified in Section 7 of the coverage file:

```
output/test-cases/<module>/<feature>/<filename>.md
```

Use this exact structure per file:

```markdown
# Test Cases: <TICKET-ID> — <Feature Name>

## Suite: <Suite Name>

### <Test Case Title>

**Description:** <AC ID> — <Technique> — <one-sentence summary>

**Preconditions:**
<bullet list of preconditions with explicit test data>

| #   | Action | Expected Result | Test Data |
| --- | ------ | --------------- | --------- |
| 1   | ...    | ...             | ...       |
| 2   | ...    | ...             | ...       |

**Severity:** <critical / major / normal / minor>
**Priority:** <high / medium / low>

---
```

---

### Step 7 — Write the CSV Output File

In addition to the `.md` file, produce a Qase-compatible CSV file saved alongside the `.md`:

```
output/test-cases/<module>/<feature>/<filename>.csv
```

Follow the **strict Qase CSV format** from `input/templates/qase-format.csv`:

```
v2.id,title,description,preconditions,postconditions,tags,priority,severity,type,behavior,
automation,status,is_flaky,layer,steps_type,steps_actions,steps_result,steps_data,
milestone_id,milestone,suite_id,suite_parent_id,suite,suite_without_cases,parameters,is_muted
```

Fixed field values for all rows:

- `type`: `functional`
- `behavior`: `undefined`
- `automation`: `is-not-automated`
- `status`: `draft`
- `is_flaky`: `no`
- `layer`: `unknown`
- `steps_type`: `classic`

CSV formatting rules:

- Escape commas inside text fields with double-quotes
- Steps (actions, results, data) are newline-separated using `\n` inside the cell
- Each step value is wrapped in double-quotes: `"1. ""Step action here"""`
- Do not include markdown formatting inside CSV cells
- Do not include explanation rows outside of data rows

---

## Quality Checks

Before saving any file, verify:

- [ ] Every AC row in Section 4 of the coverage file has at least one test case generated
- [ ] Every `Critical` and `High` risk area from Section 5 has at least one negative or boundary test case
- [ ] Every `✅ New Coverage Needed` gap in Section 6 has at least one new test case
- [ ] No business rule from Section 6 marked "Overlap = Full" has been duplicated
- [ ] No test case title contains forbidden words: Verify, Check, Test, Properly, Correctly, Successfully
- [ ] Every test case has explicit preconditions with concrete test data values
- [ ] Every step has a deterministic expected result (exact value, not "correct" or "as expected")
- [ ] Every step has a corresponding data entry (may be empty string `""`)
- [ ] Severity and priority are assigned based on the risk level in the coverage file
- [ ] OOP/tenant-specific test cases are prefixed with `[TenantName]`
- [ ] Both `.md` and `.csv` files are saved to the correct folder

---

## Example Invocation

```
Generate test cases from output/test-coverages/LT-99999-feature-name.md
```

The skill will read the coverage file and test-case-rules.md, apply technique-specific generation
patterns per AC, write all test cases with complete preconditions, steps, results, and test data,
then save `.md` and `.csv` files to the path defined in the coverage file's suggested suite structure.
