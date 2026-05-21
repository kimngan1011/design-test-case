# Spec Output Template

Final structure for `epics/<epic-folder>/spec.md`. Used by the `analyze-requirement` agent (Phase 3b "Save Spec").

The file MUST start with YAML front-matter as defined in `.claude/references/epic-folder-convention.md` § Required YAML front-matter.

---

## Finding tags (used in §Conflict & Gap Analysis)

| Tag | Meaning | Generates question? |
|---|---|---|
| `[CONFLICT]` | New rule directly contradicts an existing spec or test assertion. | Yes — always |
| `[REGRESSION RISK]` | New behavior may break an existing test without contradicting the spec. | Yes |
| `[EXTENDED]` | New rule adds to existing behavior without contradiction. | No |
| `[REPLACED]` | New rule fully supersedes an existing rule (cite the old rule). | No |
| `[UNDOCUMENTED IN AC]` | Figma/Confluence shows behavior absent from any AC. | Yes |
| `[MISSING BEHAVIOR]` | Existing system scenario has no new AC rule. | Yes |
| `[ROLE GAP]` | A role interacts with the feature but has no defined behavior in the AC. | Yes |
| `[LESSON-LEARNED RISK]` | A past incident pattern is relevant to this requirement. | Yes — always |

All skills (`analyze-impact`, `formulate-questions`, this template) MUST use this single vocabulary.

---

## Spec template

```markdown
---
ticket_id: LT-XXXXX
ticket_url: https://manabie.atlassian.net/browse/LT-XXXXX
title: <Feature Name>
module: <module>
status: <Jira epic status verbatim>
internal_uat_date: <YYYY-MM-DD or null>
production_release_date: <YYYY-MM-DD or null>
last_updated: <YYYY-MM-DD>
---

# <TICKET-ID>: <Feature Name>

## Summary

<2–3 sentences: what the feature does and why>

---

## Acceptance Criteria

<Full AC from Jira, preserving US/AC numbering. Include field-behavior tables where applicable.>

---

## Business Rules (Extracted)

| # | AC | Business Rule | Field | Field Behavior | Platform |
|---|----|----|---|---|---|
| 1 | AC XX.X | ... | ... | editable / locked / auto-calc | [SF] |

---

## Conflict & Gap Analysis

### Conflicts with Existing System

| # | Tag | Source | AC | Description |
|---|---|---|----|----|
| 1 | [CONFLICT] | epics/LT-XXXXX-... | AC XX.X | ... |

### Missing in Requirements

| # | Tag | Source | Description |
|---|---|---|---|
| 1 | [UNDOCUMENTED IN AC] | Figma node #XXXX | ... |
| 2 | [MISSING BEHAVIOR] | epics/.../test-cases/... | ... |
| 3 | [ROLE GAP] | AC (all sections) | ... |

### Lesson-Learned Risks

| # | Incident | Date | AC | Risk | Guardrail |
|---|---|---|---|---|---|
| 1 | <incident title> | <date> | AC XX.X | <specific risk> | <what to verify> |

### E2E Scenario Impact

| Scenario | Title | Impact | Action |
|---|---|---|---|
| E2E-XX | ... | ... | UPDATE / CREATE |

### Assumptions Made

- <Any inference made due to missing or ambiguous information>

---

## Clarification Questions

1. **[TAG]** <Question>
   _Evidence: `<source>` — `<what creates the gap>`_

> Update this section after questions are posted to Jira:
> ✅ Posted to Jira on YYYY-MM-DD — [view comment](url)

---

## Related Specs

- `epics/<epic-folder>/spec.md` — <why related>

## Related Test Cases

- `epics/<epic-folder>/test-cases/<file>` — <what may be impacted>

## QASE Coverage Gaps

- AC XX.X — <business rule with no existing test case>
```

---

## Source mapping (which temp file feeds which section)

| Spec section | Source `temp/` file |
|---|---|
| Front-matter (`ticket_id`, `title`, `module`) | `raw_requirement.json` |
| Summary | Synthesized from `raw_requirement.json` |
| Acceptance Criteria | `raw_requirement.json` § `user_stories` |
| Business Rules (Extracted) | `business_rules.json` |
| Conflicts | `impact_findings.json` (`[CONFLICT]` tag) |
| Missing in Requirements | `impact_findings.json` (`[UNDOCUMENTED IN AC]`, `[MISSING BEHAVIOR]`, `[ROLE GAP]`) |
| Lesson-Learned Risks | `lesson_learned_assessment.json` + `impact_findings.json` (`[LESSON-LEARNED RISK]`) |
| E2E Scenario Impact | `impact_findings.json` § `e2e_scenario_impact` |
| Clarification Questions | `clarification_questions.json` |
| Related Specs / Test Cases | `current_system_inventory.json` |
