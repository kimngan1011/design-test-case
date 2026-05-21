---
name: search-current-system
description: >
  **WORKFLOW SKILL** — Search local workspace to build an inventory of existing specs, test cases, and e2e scenarios related to a feature.
  USE FOR: Phase 1c of analyze-requirement agent — runs after fetch-requirement produces keywords.
  INPUT: Feature keywords from temp/raw_requirement.json + module name.
  OUTPUT: temp/current_system_inventory.json written to disk.
  DO NOT USE FOR: fetching external sources or analyzing impact (use fetch-requirement and analyze-impact).
---

# Skill: Search Current System

Build an inventory of what the workspace already knows about the feature being analyzed. Output is the primary comparison surface for `analyze-impact`.

## Input
Read `temp/raw_requirement.json`:
- `keywords` — feature keywords for search.
- `module` — module folder (e.g. `lesson-management`).

## Output
`temp/current_system_inventory.json` — schema in `.claude/references/data-bus-schemas.md`.

## References
- Output schema → `.claude/references/data-bus-schemas.md`

---

## Workflow

### Step 1 — Build keyword variations
From the provided keywords, generate search variations to maximize recall:
- Original keywords (e.g. "publish lesson").
- Synonyms / abbreviations ("publish", "notification", "notify").
- Entity names from domain ("lesson", "student session", "lesson report").
- Status values ("Draft", "Published", "Completed").
- Field names from AC ("Publish & Notify button", "push notification").

### Step 2 — Search local workspace
Search all keyword variations across:

| Directory / File | What to look for |
|---|---|
| `epics/<epic-folder>/spec.md` | Existing specs for the same feature or module |
| `epics/<epic-folder>/test-cases/` | TC files that may overlap or be impacted |
| `epics/<epic-folder>/test-coverage.md` | Coverage matrices for the same module |
| `knowledge/e2e-scenario/e2e-scenarios.md` | E2E scenarios covering the same area |
| `knowledge/domain-knowledge/<domain>/<domain>-feature-permission-matrix.csv` | Existing role/permission baseline (always scan, even if keywords don't mention permissions) |

### Step 3 — Relevance scoring + Top-5 limit
**Token protection rule:** when many files match, apply scoring:
1. Score each file by:
   - **Name match** (2 pts): file name contains keyword.
   - **Snippet density** (1 pt per match, up to 3): keyword appears in first 50 lines.
   - **Module match** (1 pt): file is in the same module folder.
2. Sort by score desc.
3. Read FULL content of the Top 5 only.
4. For remaining files: record path + score only — do NOT read content.

Present the list of all found files (with scores) and indicate which 5 were read in full. User can ask to read additional files if needed.

### Step 4 — Build field/behavior registry
From the Top-5 full content, extract a flat registry of every field name + documented behavior:

```
field_name | behavior | condition | source_file | AC_ref
```

Example:
```
Lesson Status | transitions Draft→Published via Publish button | — | epics/LT-XXXXX-.../spec.md | AC 01.1
Lesson Status | transitions Published→Completed after end date | — | epics/LT-XXXXX-.../test-cases/publish.md | TC-042
Publish & Notify button | visible | status = Draft | epics/LT-96662-.../spec.md | AC 01.1
Publish & Notify button | hidden | status = Completed | epics/LT-96662-.../test-cases/publish.md | TC-042
```

This registry enables field-by-field conflict detection (rather than rule-by-rule) in `analyze-impact`.

### Step 5 — Extract e2e scenario coverage
From `knowledge/e2e-scenario/e2e-scenarios.md`, identify scenarios covering the same area:
- Scenario ID and title.
- Steps that touch the same entities or operations.
- Match against "Features covered" section.

### Step 6 — Write output
Write `temp/current_system_inventory.json` per the schema in `.claude/references/data-bus-schemas.md`. Top-level fields: `keywords_searched`, `search_summary` (totals), `files_read[]` (with key business rules, related ACs, test assertions), `files_noted_only[]`, `field_behavior_registry[]`, `e2e_scenarios_relevant[]`.

---

## Quality checks
- Searched with multiple keyword variations (not just exact match).
- All 5 target directories/files searched.
- Top-5 files read in full; remaining only noted.
- Field/behavior registry built as flat table.
- `e2e-scenarios.md` scanned for relevant scenarios.
- "Related Specs" chains followed one level deep (if a spec references another spec, note it).
- Output written to `temp/current_system_inventory.json`.
- Files-noted-only list shown to user with note "ask me to read more if needed".
