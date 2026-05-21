# Data Bus Schemas (`temp/*.json`)

The analyze-requirement pipeline passes data between skills via JSON files in `temp/`. This file is the single source of truth for each file's shape. Skills MUST conform to these schemas when producing or consuming a temp file.

Lifecycle: files live in `temp/` during a run and are wiped by `workspace-cleanup` at the end.

## Data flow

```
fetch-requirement
  ├→ raw_requirement.json ──→ read-domain-knowledge, search-current-system, check-lesson-learned
  └→ business_rules.json ───→ check-lesson-learned, analyze-impact, update-domain-knowledge, formulate-questions

read-domain-knowledge
  └→ domain_context.json ───→ analyze-impact

search-current-system
  └→ current_system_inventory.json ─→ analyze-impact

check-lesson-learned
  └→ lesson_learned_assessment.json ─→ analyze-impact, formulate-questions

analyze-impact
  └→ impact_findings.json ──→ update-domain-knowledge, formulate-questions, update-e2e-scenarios

formulate-questions
  └→ clarification_questions.json   (terminal: posted to Jira, not consumed)
```

## Schemas

### `raw_requirement.json`
Producer: `fetch-requirement`. Consumers: `read-domain-knowledge`, `search-current-system`, `check-lesson-learned`, `formulate-questions`.

| Field | Type | Description |
|---|---|---|
| `ticket_id` | string | Jira ticket ID (e.g. `LT-96620`). |
| `ticket_url` | string | Full Jira URL. |
| `feature_name` | string | Short human name. |
| `module` | string | Domain module (e.g. `scheduling`). |
| `keywords` | string[] | Search keywords extracted from ticket. |
| `roles` | string[] | Roles affected (student, teacher, BO admin…). |
| `user_stories[]` | object | `{ id, title, acceptance_criteria }`. |
| `figma_discrepancies[]` | object | `{ tag, figma_node, description }`. |
| `qase_coverage[]` | object | `{ suite, title }` existing Qase cases. |

### `business_rules.json`
Producer: `fetch-requirement`. Consumers: `check-lesson-learned`, `analyze-impact`, `update-domain-knowledge`, `formulate-questions`.

| Field | Type | Description |
|---|---|---|
| `ticket_id` | string | |
| `rules[]` | object | One rule per row. |
| `rules[].id` | string | Stable rule ID (e.g. `BR-01`). |
| `rules[].ac_ref` | string | AC anchor (e.g. `AC1.2`). |
| `rules[].rule` | string | Plain-language rule. |
| `rules[].field` | string | Field name when rule is field-scoped. |
| `rules[].field_behavior` | string | Required, optional, computed, etc. |
| `rules[].role_constraint` | string | Role-gated visibility/edit. |
| `rules[].conditional_logic` | string | Condition under which rule applies. |
| `rules[].default_value` | string | Default if any. |
| `rules[].platform` | string | web / app / both. |

### `domain_context.json`
Producer: `read-domain-knowledge`. Consumer: `analyze-impact`.

| Field | Type | Description |
|---|---|---|
| `domain` | string | e.g. `scheduling`. |
| `keywords_used` | string[] | Subset of raw_requirement.keywords actually matched. |
| `entities[]` | object | `{ name, key_fields, field_behaviors, status_transitions, crud_rules, platform }`. |
| `data_relationships` | string[] | Cross-entity relations. |
| `platform_specific_behaviors` | string[] | Web vs app deltas. |
| `non_obvious_edge_cases` | string[] | Subtle rules to test. |
| `permission_matrix` | object | `{ source, role_columns, relevant_features }`. |

### `current_system_inventory.json`
Producer: `search-current-system`. Consumer: `analyze-impact`.

| Field | Type | Description |
|---|---|---|
| `keywords_searched` | string[] | |
| `search_summary` | object | `{ total_files_found, files_read_in_full, files_recorded_only }`. |
| `files_read[]` | object | `{ path, relevance_score, key_business_rules, related_acs, test_assertions }`. |
| `files_noted_only[]` | object | `{ path, relevance_score }`. |
| `field_behavior_registry[]` | object | `{ field, behavior, condition, source, ac_ref }`. |
| `e2e_scenarios_relevant[]` | object | `{ id, title, relevant_steps, reason }`. |

### `lesson_learned_assessment.json`
Producer: `check-lesson-learned`. Consumers: `analyze-impact`, `formulate-questions`.

| Field | Type | Description |
|---|---|---|
| `ticket_id` | string | |
| `assessment_date` | string | ISO date. |
| `incidents_checked` | number | Count of lesson-learned entries scanned. |
| `relevant_incidents[]` | object | `{ incident_title, incident_date, source_file, entity_overlap, operation_overlap, relevance_reason, risk_statement, guardrail_recommendation, tag }`. |
| `no_match_incidents[]` | object | `{ incident_title, reason_not_relevant }`. |
| `summary` | string | One-paragraph summary. |

### `impact_findings.json`
Producer: `analyze-impact`. Consumers: `update-domain-knowledge`, `formulate-questions`, `update-e2e-scenarios`.

| Field | Type | Description |
|---|---|---|
| `ticket_id` | string | |
| `findings[]` | object | `{ id, tag, source_file, source_rule, ac_ref, description, positive_assertion, negative_assertion }`. |
| `e2e_scenario_impact[]` | object | `{ scenario_id, scenario_title, impact, action_needed }`. |
| `summary` | object | `{ total_findings, by_tag, zero_findings_acs, e2e_scenarios_to_update, e2e_scenarios_to_create }`. |

### `clarification_questions.json`
Producer: `formulate-questions`. Terminal output (posted to Jira).

| Field | Type | Description |
|---|---|---|
| `ticket_id` | string | |
| `total_questions` | number | |
| `questions[]` | object | `{ id, tag, ac_ref, priority, question, evidence }`. |

## Rules for skills

1. **Producers** must write the full schema; missing optional fields → use `null` or `[]`, never omit keys.
2. **Consumers** must read from the schema above. If a skill needs a new field, add it here first, then update producer.
3. **Tags** in findings/questions/incidents follow a controlled vocabulary defined per-skill (see each skill's SKILL.md).
4. **Traceability**: every finding/question references `source_file` + `ac_ref` so reviewers can trace claims.
5. **No schema drift**: when a SKILL.md describes JSON shape, it must link here rather than redefine.
