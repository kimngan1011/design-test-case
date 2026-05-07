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

You are the core analytical engine of the requirement analysis workflow. Your job is to compare every new business rule against the existing system — field by field, rule by rule — and produce a comprehensive findings table.

---

## Input

Read all of the following from disk (do not rely on chat context):
- `temp/business_rules.json` — new business rules extracted from the requirement
- `temp/current_system_inventory.json` — existing specs, test cases, field/behavior registry
- `temp/domain_context.json` — domain knowledge context
- `temp/lesson_learned_assessment.json` — relevant past incidents

---

## Finding Tags

| Tag | Meaning |
|-----|---------|
| `[CONFLICT]` | New rule directly contradicts an existing spec or test assertion |
| `[REGRESSION RISK]` | New behavior may break an existing test without contradicting the spec |
| `[EXTENDED]` | New rule adds to existing behavior without contradiction |
| `[REPLACED]` | New rule fully supersedes an existing rule (cite the old rule) |
| `[UNDOCUMENTED IN AC]` | Figma or Confluence shows behavior absent from any AC |
| `[MISSING BEHAVIOR]` | An existing system scenario has no new AC rule |
| `[ROLE GAP]` | A role interacts with the feature but has no defined behavior in the AC |
| `[LESSON-LEARNED RISK]` | A past incident pattern is relevant to this requirement |

---

## Workflow

### Step 1 — Business Rule Delta (field-by-field comparison)

Use the **field/behavior registry** from `temp/current_system_inventory.json` as the primary comparison surface.

For each entry in the registry:
1. Find the matching field in `temp/business_rules.json`
2. Compare: does the new rule define the same field with the same behavior, different behavior, or extended behavior?
3. Tag the finding using the table above

For each new business rule in `temp/business_rules.json`:
1. Check if any existing spec or test case defines the same field or operation with **different** behavior → `[CONFLICT]`
2. Check if the new rule changes behavior that an existing test case asserts → `[REGRESSION RISK]`
3. Check if the new rule builds on existing behavior without contradiction → `[EXTENDED]`
4. Check if the new rule completely replaces an old rule → `[REPLACED]`

> **Traceability rule:** Every `[CONFLICT]` MUST cite exact source file path + specific rule/line. Every `[REGRESSION RISK]` MUST identify the specific test assertion that would break.

### Step 2 — Negative test surface

For every "when X, do Y" rule in `temp/business_rules.json`:
- Ask: "when NOT X, what happens?"
- If the AC does not define the negative case → tag `[MISSING BEHAVIOR]`
- Example: AC says "button visible when Draft" → check: "what happens when status is Completed? Cancelled?" → if AC is silent → `[MISSING BEHAVIOR]`

> **Conditional exhaustion rule:** If a rule covers N conditions (e.g., 3 statuses), the AC must define behavior for ALL possible statuses. Any undefined status = `[MISSING BEHAVIOR]`.

### Step 3 — Implicit dependencies and data cascade

For every rule that creates, modifies, or deletes a record:
1. Look up the entity in `temp/domain_context.json`
2. Trace downstream cascade dependencies from the "data_relationships" section
3. Check: does the new behavior affect any downstream entity in a way the AC does not address?

Example:
- New requirement: "clicking Publish & Notify button changes lesson status to Published"
- Domain cascade: "Lesson Published → Lesson Report status auto-updates → Mobile visibility triggered"
- Check: does the AC define the Lesson Report behavior after this new publish path?

### Step 4 — Role and permission coverage

From `temp/raw_requirement.json` roles list:
1. For each role, verify the AC defines their behavior or explicitly excludes them
2. Roles in `temp/domain_context.json` entities that are NOT in the AC roles list → `[ROLE GAP]`

### Step 5 — Lesson-learned risk overlay

From `temp/lesson_learned_assessment.json` relevant_incidents:
1. For each relevant incident, tag the specific AC rule or design pattern that triggers the same risk
2. Tag: `[LESSON-LEARNED RISK]`
3. Include: incident date, title, and specific risk statement

### Step 6 — E2E scenario impact

From `temp/current_system_inventory.json` e2e_scenarios_relevant:
1. For each relevant E2E scenario, assess: do any new rules change the expected behavior of existing steps?
2. List which scenarios need updating and why

### Step 7 — Anti-shallow verification (Check #13)

For each new business rule, verify:
- Is there an explicit **positive assertion** (what SHOULD happen)?
- Is there an explicit **negative assertion** (what should NOT happen, or what error occurs)?

If either is missing → flag as needing coverage in clarification questions.

---

## Output

Write `temp/impact_findings.json`:

```json
{
  "ticket_id": "LT-XXXXX",
  "findings": [
    {
      "id": 1,
      "tag": "[CONFLICT]",
      "source_file": "input/specs/LT-96662 Renseikai.../spec.md",
      "source_rule": "Business Rule #8: Button hidden for Completed/Cancelled",
      "ac_ref": "AC 01.1",
      "description": "New AC 01.1 states button visible for Draft only. Existing spec states button visible for both Draft AND Published. These conflict on Published status behavior.",
      "positive_assertion": "Button visible when Draft",
      "negative_assertion": "Button behavior when Published — undefined or conflicting"
    },
    {
      "id": 2,
      "tag": "[LESSON-LEARNED RISK]",
      "source_file": "input/domain-knowledge/scheduling/lesson-learned/core.md",
      "incident_date": "2026-04-13",
      "incident_title": "Aso — Duplicate Student Sessions",
      "ac_ref": "AC 02.1",
      "description": "AC 02.1 introduces a new notification trigger via button click. If existing publish flow (Draft→Published status change) already triggers notification for some partners, this creates a dual-trigger pattern — same as Aso incident.",
      "positive_assertion": "New button triggers push notification",
      "negative_assertion": "Existing publish flow notification behavior — not addressed in AC"
    },
    {
      "id": 3,
      "tag": "[MISSING BEHAVIOR]",
      "source_file": "temp/business_rules.json",
      "ac_ref": "AC 01.1",
      "description": "AC 01.1 defines button visible for Draft. No AC covers button visibility for Cancelled status.",
      "positive_assertion": null,
      "negative_assertion": "Button when status = Cancelled — undefined"
    },
    {
      "id": 4,
      "tag": "[ROLE GAP]",
      "source_file": "AC (all sections)",
      "ac_ref": null,
      "description": "Centre Staff role appears in domain knowledge for lesson management but has no defined behavior for the Publish & Notify button in any AC.",
      "positive_assertion": null,
      "negative_assertion": null
    }
  ],
  "e2e_scenario_impact": [
    {
      "scenario_id": "E2E-02",
      "scenario_title": "Create recurring lesson + assign student",
      "impact": "Step 14 (publish lesson) now has a new button path. Scenario needs a step for 'Publish & Notify' vs standard publish, and a Mobile verification step for notification receipt.",
      "action_needed": "UPDATE"
    }
  ],
  "summary": {
    "total_findings": 4,
    "by_tag": {
      "CONFLICT": 1,
      "REGRESSION_RISK": 0,
      "EXTENDED": 0,
      "REPLACED": 0,
      "UNDOCUMENTED_IN_AC": 0,
      "MISSING_BEHAVIOR": 1,
      "ROLE_GAP": 1,
      "LESSON_LEARNED_RISK": 1
    },
    "zero_findings_acs": [],
    "e2e_scenarios_to_update": ["E2E-02"],
    "e2e_scenarios_to_create": []
  }
}
```

> **Minimum findings rule:** If `zero_findings_acs` is non-empty (an AC has zero findings), this is suspicious — a genuinely clean AC is rare for features touching existing entities. The master agent's Phase 4 review will flag this for re-examination.

---

## Quality Checks

- [ ] Read all 4 input files from `temp/` (not from chat context)
- [ ] Field/behavior registry used as primary comparison surface
- [ ] Every `[CONFLICT]` cites exact source file + rule
- [ ] Every `[REGRESSION RISK]` identifies specific test assertion that breaks
- [ ] Every `[LESSON-LEARNED RISK]` includes incident date + title
- [ ] Negative test surface checked for every "when X, do Y" rule
- [ ] Data cascade checked for every create/modify/delete operation
- [ ] All roles from AC checked against domain knowledge roles
- [ ] E2E scenario impact assessed
- [ ] Both positive and negative assertions noted for each finding
- [ ] Output written to `temp/impact_findings.json`
