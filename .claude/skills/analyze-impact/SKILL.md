---
name: analyze-impact
description: >
  **WORKFLOW SKILL** — Core conflict and gap analysis: compare new requirement against current system inventory to detect conflicts, regression risks, and gaps.
  USE FOR: Phase 2b of analyze-requirement agent — runs after check-lesson-learned.
  INPUT: All temp/*.json files from Phase 1 and 2a (already on disk).
  OUTPUT: temp/impact_findings.json written to disk.
  DO NOT USE FOR: generating questions (use formulate-questions) or fetching external sources.
---

# Skill: Analyze Impact

Core analytical engine. Compare every new business rule against the existing system — field by field, rule by rule — and produce a comprehensive findings table.

## Input
Read all from disk (do not rely on chat context):
- `temp/business_rules.json` — new rules.
- `temp/current_system_inventory.json` — existing specs, test cases, field/behavior registry.
- `temp/domain_context.json` — domain knowledge.
- `temp/lesson_learned_assessment.json` — relevant past incidents.

## References
- Full schemas for all temp/*.json files (input + output) → `.claude/references/data-bus-schemas.md`

## Output
`temp/impact_findings.json` — schema defined in `.claude/references/data-bus-schemas.md` § `impact_findings.json`.

---

## Finding tags

| Tag | Meaning |
|---|---|
| `[CONFLICT]` | New rule directly contradicts an existing spec or test assertion. |
| `[REGRESSION RISK]` | New behavior may break an existing test without contradicting the spec. |
| `[EXTENDED]` | New rule adds to existing behavior without contradiction. |
| `[REPLACED]` | New rule fully supersedes an existing rule (cite the old rule). |
| `[UNDOCUMENTED IN AC]` | Figma or Confluence shows behavior absent from any AC. |
| `[MISSING BEHAVIOR]` | An existing system scenario has no new AC rule. |
| `[ROLE GAP]` | A role interacts with the feature but has no defined behavior in the AC. |
| `[LESSON-LEARNED RISK]` | A past incident pattern is relevant to this requirement. |

---

## Workflow

### Step 1 — Business rule delta (field-by-field)
Use the **field/behavior registry** from `current_system_inventory.json` as the primary comparison surface.

For each registry entry:
1. Find the matching field in `business_rules.json`.
2. Compare: same field with same / different / extended behavior?
3. Tag using the table above.

For each new rule:
1. Existing spec/TC defines the same field/operation with **different** behavior → `[CONFLICT]`.
2. New rule changes behavior an existing TC asserts → `[REGRESSION RISK]`.
3. New rule builds on existing without contradiction → `[EXTENDED]`.
4. New rule completely replaces an old rule → `[REPLACED]`.

> **Traceability rule:** Every `[CONFLICT]` MUST cite exact source file path + specific rule/line. Every `[REGRESSION RISK]` MUST identify the specific test assertion that would break.

### Step 2 — Negative test surface
For every "when X, do Y" rule:
- Ask "when NOT X, what happens?"
- If the AC does not define the negative case → tag `[MISSING BEHAVIOR]`.

> **Conditional exhaustion rule:** If a rule covers N conditions (e.g., 3 statuses), the AC must define behavior for ALL possible statuses. Any undefined status = `[MISSING BEHAVIOR]`.

### Step 3 — Implicit dependencies and data cascade
For every rule that creates, modifies, or deletes a record:
1. Look up the entity in `domain_context.json`.
2. Trace downstream cascade dependencies (`data_relationships`).
3. Check: does the new behavior affect any downstream entity in a way the AC does not address?

#### Step 3a — Cross-partner cascade warnings (advisory only)

After tracing core data cascades above, check for partner-cascade triggers. These produce a **warning message in chat** — they do NOT auto-emit findings or clarification questions, and they do NOT auto-load any partner file. The warning lets the user decide whether to dig deeper.

| Trigger condition (in the new requirement) | Action |
|---|---|
| Spec is a **core feature** (no partner scope) AND any rule covers **assign or unassign student to a lesson** (manual add, class auto-assign, reallocation, recurring scope, import) | Print this warning verbatim to chat at the end of the skill: _"⚠️ Core feature touches student assign/unassign. Nichibei extends this with point consumption (priority chain + refund). If you want me to assess Nichibei impact, ask and I will deep-read `partner-rules/nichibei-lesson-allocation.md` and re-run impact analysis."_ Then continue — do NOT add a finding, do NOT add a question. |

**On-demand expansion** — only when the user explicitly asks ("check Nichibei", "yes assess partner impact", etc.):
1. Deep-read `knowledge/domain-knowledge/scheduling/partner-rules/nichibei-lesson-allocation.md`.
2. Re-run Steps 1–7 of this skill with that extra context.
3. Add findings (tagged `[LESSON-LEARNED RISK]`) and overwrite `temp/impact_findings.json`.

### Step 4 — Role and permission coverage
From `raw_requirement.json` `roles` list:
1. For each role, verify the AC defines their behavior or explicitly excludes them.
2. Roles in `domain_context.json` entities NOT in the AC roles list → `[ROLE GAP]`.

### Step 5 — Lesson-learned risk overlay
From `lesson_learned_assessment.json` `relevant_incidents`:
1. For each relevant incident, tag the specific AC rule or design pattern that triggers the same risk.
2. Tag `[LESSON-LEARNED RISK]`. Include incident date, title, specific risk statement.

### Step 6 — E2E scenario impact
From `current_system_inventory.json` `e2e_scenarios_relevant`:
1. For each scenario, assess: do any new rules change the expected behavior of existing steps?
2. List which scenarios need updating and why → `e2e_scenario_impact` section of output.

### Step 7 — Anti-shallow verification (Check #13)
For each new rule, verify:
- Explicit **positive assertion** (what SHOULD happen).
- Explicit **negative assertion** (what should NOT happen, or what error occurs).

If either missing → flag as needing coverage in clarification questions.

---

## Output

Write `temp/impact_findings.json` per the schema in `.claude/references/data-bus-schemas.md`.

Each finding includes: `id`, `tag`, `source_file`, `source_rule`, `ac_ref`, `description`, `positive_assertion`, `negative_assertion`.

> **Minimum findings rule:** If `zero_findings_acs` is non-empty (an AC with zero findings), this is suspicious — a genuinely clean AC is rare for features touching existing entities. The master agent's Phase 4 review will flag this for re-examination.

---

## Quality checks
- Read all 4 input files from `temp/` (not chat context).
- Field/behavior registry used as primary comparison surface.
- Every `[CONFLICT]` cites exact source file + rule.
- Every `[REGRESSION RISK]` identifies the specific test assertion that breaks.
- Every `[LESSON-LEARNED RISK]` includes incident date + title.
- Negative test surface checked for every "when X, do Y" rule.
- Data cascade checked for every create/modify/delete.
- All AC roles checked against domain knowledge roles.
- E2E scenario impact assessed.
- Both positive and negative assertions noted per finding.
- Output written to `temp/impact_findings.json` with schema-conformant structure.
