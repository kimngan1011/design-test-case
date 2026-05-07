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

You are building an inventory of what the current system already knows about the feature being analyzed. Your output is the primary comparison surface for the `analyze-impact` skill.

---

## Input

Read `temp/raw_requirement.json` to get:

- `keywords` — feature keywords to search with
- `module` — module folder name (e.g., `lesson-management`)

---

## Workflow

### Step 1 — Build keyword variations

From the provided keywords, generate search variations to maximize recall:

- Original keywords (e.g., "publish lesson")
- Synonyms and abbreviations (e.g., "publish", "notification", "notify")
- Entity names from domain (e.g., "lesson", "student session", "lesson report")
- Status values (e.g., "Draft", "Published", "Completed")
- Field names from the AC (e.g., "Publish & Notify button", "push notification")

### Step 2 — Search local workspace

Search the following directories using all keyword variations:

| Directory / File                                                         | What to look for                                                                                                                        |
| ------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------- |
| `input/specs/`                                                           | Spec files for the same feature or module                                                                                               |
| `output/test-cases/`                                                     | Test case files that may overlap or be impacted                                                                                         |
| `output/test-coverages/`                                                 | Coverage matrices for the same module                                                                                                   |
| `input/e2e-scenario/e2e-scenarios.md`                                    | E2E scenarios covering the same feature area                                                                                            |
| `input/domain-knowledge/<domain>/<domain>-feature-permission-matrix.csv` | Existing role/permission baseline for any feature touched by the requirement (always scan, even if keywords do not mention permissions) |

### Step 3 — Relevance scoring and Top-5 limit

**Token protection rule:** When search returns many matching files, apply relevance scoring:

1. Score each file by:
   - **Name match** (2 pts): file name contains keyword
   - **Snippet density** (1 pt per match up to 3): keyword appears in first 50 lines
   - **Module match** (1 pt): file is in the same module folder
2. Sort by score descending
3. **Read FULL content of the Top 5 files only**
4. For remaining files: record name and path only — do NOT read content

Present the list of all found files (with scores) and indicate which 5 were read in full. User can ask to read additional files if needed.

### Step 4 — Build field/behavior registry

From the full content of the Top 5 files, extract a flat registry of every field name and its documented behavior:

```
field_name | behavior | source_file | AC_ref
```

Example:

```
Lesson Status   | transitions: Draft→Published via Publish button | input/specs/LT-XXXXX/spec.md | AC 01.1
Lesson Status   | transitions: Published→Completed after end date  | output/test-cases/lesson/publish.md | TC-042
```

This registry is the primary comparison surface for `analyze-impact` — it enables field-by-field conflict detection rather than rule-by-rule.

### Step 5 — Extract e2e scenario coverage

From `input/e2e-scenario/e2e-scenarios.md`, identify which scenarios cover the same feature area:

- Scenario ID and title
- Steps that touch the same entities or operations
- "Features covered" section matches

### Step 6 — Write output

Write `temp/current_system_inventory.json`:

```json
{
  "keywords_searched": ["publish lesson", "publish", "notification", "lesson status"],
  "search_summary": {
    "total_files_found": 12,
    "files_read_in_full": 5,
    "files_recorded_only": 7
  },
  "files_read": [
    {
      "path": "input/specs/LT-96662 Renseikai Receive notifications when a new lesson is published/spec.md",
      "relevance_score": 7,
      "key_business_rules": [
        "Button visible for Draft and Published status",
        "Sends push notification to assigned students and parents"
      ],
      "related_acs": ["AC 01.1", "AC 01.2", "AC 02.1"],
      "test_assertions": ["button_hidden_for_completed: true", "notification_sent_to_parents: true"]
    }
  ],
  "files_noted_only": [{ "path": "output/test-cases/lesson/lesson-publish.md", "relevance_score": 3 }],
  "field_behavior_registry": [
    {
      "field": "Publish & Notify button",
      "behavior": "visible",
      "condition": "status = Draft",
      "source": "input/specs/LT-96662/spec.md",
      "ac_ref": "AC 01.1"
    },
    {
      "field": "Publish & Notify button",
      "behavior": "hidden",
      "condition": "status = Completed",
      "source": "output/test-cases/lesson/publish.md",
      "ac_ref": "TC-042"
    }
  ],
  "e2e_scenarios_relevant": [
    {
      "id": "E2E-02",
      "title": "Create recurring lesson + assign student",
      "relevant_steps": [14, 15],
      "reason": "Covers lesson publish flow — may need updating for new notify button"
    }
  ]
}
```

---

## Quality Checks

- [ ] Searched with multiple keyword variations (not just exact keyword)
- [ ] All 4 target directories searched
- [ ] Top-5 files read in full; remaining files only noted
- [ ] Field/behavior registry built as flat table
- [ ] e2e-scenarios.md scanned for relevant scenarios
- [ ] "Related Specs" chains followed one level deep (if a spec references another spec, note it)
- [ ] Output written to `temp/current_system_inventory.json`
- [ ] Files-noted-only list shown to user with note "ask me to read more if needed"
