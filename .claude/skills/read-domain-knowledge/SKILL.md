---
name: read-domain-knowledge
description: >
  **WORKFLOW SKILL** — Load relevant domain context from the domain knowledge files for a given feature area.
  USE FOR: Phase 1b of analyze-requirement agent — run in parallel with fetch-requirement.
  INPUT: Feature keywords + domain folder (default: scheduling).
  OUTPUT: temp/domain_context.json written to disk.
  DO NOT USE FOR: fetching Jira tickets or searching local specs (use fetch-requirement and search-current-system).
---

# Skill: Read Domain Knowledge

Load domain context to support requirement analysis. Extract the relevant subset of domain knowledge for the feature area and write to `temp/domain_context.json` for downstream skills.

## Input
- `keywords` — feature keywords (e.g., "publish lesson", "push notification", "student session", "Renseikai", "Nichibei").
- `domain` — domain folder name (default: `scheduling`).

If keywords are not provided, read them from `temp/raw_requirement.json` if it exists.

## Output
`temp/domain_context.json` — schema in `.claude/references/data-bus-schemas.md`.

---

## Workflow

### Step 1 — Always read these files in full

These are mandatory regardless of keywords:

- `knowledge/domain-knowledge/<domain>/overview.md` — system overview, master data, customization-by-org, data relationships, test coverage summary, and the **file index**.
- `knowledge/domain-knowledge/<domain>/<domain>-feature-permission-matrix.csv` — role × feature access baseline. New features almost always touch at least one role; conflicts emerge when an AC grants/denies access contradicting this matrix.

If either file does not exist for the given domain, log a warning and continue.

### Step 2 — Scan all sub-domain filenames

List every `.md` file under `knowledge/domain-knowledge/<domain>/` (recursively, except `overview.md` which was already read in Step 1).

You will use the filenames + their location (sub-folder) as the matching index — NOT the file contents.

### Step 3 — Match filenames against keywords

For each file found in Step 2, decide whether to **deep-read** it based on filename + spec keywords:

- **Deep-read** if the filename (or its parent folder name) contains any of:
  - An entity/feature name mentioned in the spec keywords (e.g. `lesson`, `student-session`, `lesson-teacher`, `calendar-sf`, `event-master`, `multiple-classes`).
  - A partner/tenant name mentioned in the spec (e.g. `renseikai-*`, `nichibei-*`, `riso-*`, `koyu-*`).
  - A Jira ticket ID embedded in the filename if relevant.
- **Skip** if the filename has no keyword match.

> **When in doubt, read.** A file that might be relevant is worth reading. The cost of reading a 100-line file is much smaller than missing a cross-domain dependency.

> **Always read parent + sibling sub-domain files** when a sub-section matches. Example: keyword "recurring lesson" → read `lesson-management/lesson.md` (covers recurrence) AND `lesson-management/student-session.md` (recurring assignment scope rules). Use `overview.md` § File index to discover related files.

> **Do NOT auto-read partner files when the spec is core scope.** Partner files (Nichibei, Riso, Renseikai, Koyu) are only deep-read when (a) the spec explicitly mentions the partner, OR (b) the user asks for partner impact assessment after the core analysis (see `analyze-impact` § Step 3a warning).

### Step 4 — Extract structured context

From the files read (Step 1 + deep-read files from Step 3), extract:

- **Entities** — name, key fields, field behaviors (editable/locked/auto-calculated), status transitions.
- **CRUD rules** — what create/update/delete operations trigger; what they cascade to.
- **Platform behaviors** — which apply to SF only, BO only, Mobile only.
- **Data relationships** — entity links and cascade rules (e.g., deleting a lesson → deletes lesson reports + student sessions).
- **Non-obvious edge cases** — surprising or commonly misunderstood behaviors.
- **Permission matrix rows** — every row whose `Feature` matches keywords or relevant entities. Capture: feature name, allowed roles (`TRUE`/`FALSE` per role), `Note`.

### Step 5 — Write output

Write `temp/domain_context.json` per the schema in `.claude/references/data-bus-schemas.md`. Top-level fields: `domain`, `keywords_used`, `entities[]`, `data_relationships`, `platform_specific_behaviors`, `non_obvious_edge_cases`, `permission_matrix`.

Also include a `files_read` array listing which sub-domain files were deep-read (useful for traceability):

```json
{
  "files_read": [
    "knowledge/domain-knowledge/scheduling/overview.md",
    "knowledge/domain-knowledge/scheduling/lesson-management/lesson.md",
    "knowledge/domain-knowledge/scheduling/lesson-management/student-session.md",
    "knowledge/domain-knowledge/scheduling/partner-rules/renseikai-publish-notifications.md"
  ]
}
```

---

## Output size rule

Produce a **focused summary** — approximately 200–300 lines of JSON. Do NOT copy raw file content verbatim. Summarize entity rules into concise key-value pairs.

---

## Quality checks

- `overview.md` and `<domain>-feature-permission-matrix.csv` read in full (Step 1).
- All sub-domain filenames scanned (Step 2).
- Every file with a name matching spec keywords (or partner name in spec) was deep-read.
- Parent + sibling sub-domain files included when a sub-section matches (per `overview.md` § File index).
- "Data relationships" section from `overview.md` always reflected in output.
- Every entity has field behaviors, CRUD rules, and platform scope defined.
- `permission_matrix.relevant_features` populated for every feature touched by the requirement.
- `files_read` array lists all deep-read files (traceability).
- Output is a focused summary, not a raw copy.
- Output written to `temp/domain_context.json`.
