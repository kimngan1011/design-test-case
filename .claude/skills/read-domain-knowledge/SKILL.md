---
name: read-domain-knowledge
description: >
  **WORKFLOW SKILL** — Load relevant domain context from the domain knowledge file for a given feature area.
  USE FOR: Phase 1b of analyze-requirement agent — run in parallel with fetch-requirement.
  INPUT: Feature keywords + domain folder (default: scheduling).
  OUTPUT: temp/domain_context.json written to disk.
  DO NOT USE FOR: fetching Jira tickets or searching local specs (use fetch-requirement and search-current-system).
---

# Skill: Read Domain Knowledge

You are loading domain context to support requirement analysis. Your job is to extract the relevant subset of the domain knowledge file for the feature area being analyzed, and write it to `temp/domain_context.json` for downstream skills to consume.

---

## Input

- `keywords` — feature keywords (e.g., "publish lesson", "push notification", "student session")
- `domain` — domain folder name (default: `scheduling`)

If keywords are not provided directly, read them from `temp/raw_requirement.json` if it exists.

---

## Workflow

### Step 1 — Read the full domain knowledge file

Read `input/domain-knowledge/<domain>/<domain>-domain-knowledge.md` **in its entirety**.

> **Rule:** Do NOT skip sections based on keyword matching alone. Cross-entity dependencies are often hidden in sections that do not mention the keywords directly. You must read the whole file.

### Step 1b — Read the feature permission matrix

Also read `input/domain-knowledge/<domain>/<domain>-feature-permission-matrix.csv` **in its entirety** (e.g. `input/domain-knowledge/scheduling/scheduling-feature-permission-matrix.csv`).

This CSV documents which roles (`full_access`, `center_level_edit`, `bo_teacher`, etc.) are allowed to perform each feature action. It is the source of truth for permission/role behavior and must be loaded for every analysis — even when keywords do not explicitly mention permissions, because:

- New features almost always interact with at least one role
- Conflicts often emerge when a new AC grants/denies access in a way that contradicts the existing matrix
- Missing role coverage in the AC must be flagged against this baseline

If the file does not exist for the given domain, log a warning and continue.

### Step 2 — Identify relevant sections

From the full file, identify sections relevant to the provided keywords:

1. For each keyword, find all sections that mention related entities, operations, or field names
2. When a keyword matches a sub-section (e.g., "recurring lesson" → "Lesson Schedule"), **also include**:
   - The parent section (e.g., "Lesson")
   - Sibling sub-sections that share data dependencies
3. **Always include** the "Key Data Relationships" section (or equivalent) regardless of keywords — it documents cascade dependencies that affect impact analysis

### Step 3 — Extract structured context

From the relevant sections, extract:

- **Entities** — name, key fields, field behaviors (editable/locked/auto-calculated), status transitions
- **CRUD rules** — what create/update/delete operations trigger, what they cascade to
- **Platform behaviors** — which behaviors apply to SF only, BO only, or Mobile (Learner App)
- **Data relationships** — which entities are linked, how changes cascade (e.g., deleting a lesson → deletes lesson reports + student sessions)
- **Non-obvious edge cases** — behaviors that are surprising or commonly misunderstood
- **Permission matrix rows** — from the CSV in Step 1b, extract every row whose `Feature` matches the keywords or relevant entities. Capture: feature name, allowed roles (`TRUE`/`FALSE` per role column), and any `Note`.

### Step 4 — Write output

Write `temp/domain_context.json` with the following structure:

```json
{
  "domain": "scheduling",
  "keywords_used": ["keyword1", "keyword2"],
  "entities": [
    {
      "name": "Entity Name",
      "key_fields": ["field1", "field2"],
      "field_behaviors": {
        "field1": "editable",
        "field2": "auto-calculated"
      },
      "status_transitions": ["Draft → Published", "Published → Completed"],
      "crud_rules": {
        "create": "Triggers creation of lesson report",
        "update": "If recurring, applies scope (only this / this and following)",
        "delete": "Cascades to student sessions and lesson reports"
      },
      "platform": ["SF", "BO", "Mobile"]
    }
  ],
  "data_relationships": [
    "Lesson → (1:1) LessonReport",
    "LessonReport → (1:N) LessonReportDetail (one per assigned student)",
    "StudentSession → linked to LessonAllocation"
  ],
  "platform_specific_behaviors": [
    "SF: source of truth for lesson creation and student assignment",
    "BO: read-only view of lessons, can manage attendance",
    "Mobile: student views published lessons, submits attendance"
  ],
  "non_obvious_edge_cases": [
    "Closed dates are skipped when creating recurring lessons",
    "Lesson code is auto-generated and cannot be edited"
  ],
  "permission_matrix": {
    "source": "input/domain-knowledge/scheduling/scheduling-feature-permission-matrix.csv",
    "role_columns": ["full_access", "center_level_edit", "bo_teacher"],
    "relevant_features": [
      {
        "category": "Lesson",
        "feature": "Edit Lesson",
        "permissions": { "full_access": true, "center_level_edit": true, "bo_teacher": true },
        "note": ""
      },
      {
        "category": "Lesson",
        "feature": "Change Location Course",
        "permissions": { "full_access": true, "center_level_edit": false, "bo_teacher": false },
        "note": ""
      }
    ]
  }
}
```

---

## Output size rule

Produce a **focused summary** — approximately 200–300 lines of JSON. Do NOT copy the raw domain knowledge file content verbatim. Summarize entity rules into concise key-value pairs.

---

## Quality Checks

- [ ] Read the ENTIRE domain knowledge file before extracting (no selective skipping)
- [ ] Read the feature permission matrix CSV (`<domain>-feature-permission-matrix.csv`) in full
- [ ] "Key Data Relationships" section always included
- [ ] Parent + sibling sections included when a sub-section matches keywords
- [ ] Every entity has field behaviors, CRUD rules, and platform scope defined
- [ ] `permission_matrix.relevant_features` populated for every feature touched by the requirement
- [ ] Output is written to `temp/domain_context.json`
- [ ] Output is a focused summary, not a raw copy
