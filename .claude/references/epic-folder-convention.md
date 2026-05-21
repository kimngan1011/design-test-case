# Epic Folder Convention

The workspace organizes QA artifacts **per epic**. One Jira epic = one folder under `epics/` containing all related files (spec, coverage, test cases).

## Layout

```
epics/
└── LT-XXXXX-<slug>/
    ├── spec.md              # produced by analyze-requirements
    ├── test-coverage.md     # produced by define-test-coverage
    └── test-cases/
        ├── <feature>.md     # produced by generate-test-cases
        └── <feature>.csv    # CSV mirror for Qase import
```

## Folder naming

- **Format**: `LT-<JiraID>-<slug>`
- **Slug**: kebab-case, lowercase, **derived from the Jira title but shortened**.
  - Source: the Jira ticket title is the canonical source of truth.
  - Shorten aggressively: drop filler words (`improve`, `add`, `update`, `system`, `feature`, articles), keep only the noun phrase that identifies the change.
  - Strip punctuation (`:`, parentheses, brackets) and lowercase everything.
  - Keep it ≤ 6 words.
  - Examples (Jira title → slug):
    - "Academic Calendar Closed Date per Location" → `academic-calendar-closed-date-per-location`
    - "Nichibei App - Lesson Booking System" → `nichibei-lesson-booking`
    - "Deduplicate Student and Teacher Assignments" → `deduplicate-student-teacher-assignments`
    - "Improve Course and Class Filter on Calendar" → `course-class-filter-calendar`

## Legacy / non-ticketed work

For artifacts without a Jira ID:
- Use placeholder `LT-XXXX-<existing-folder-name>` (e.g. `LT-XXXX-lesson-allocation`).
- Owner must replace `XXXX` with the real Jira ID later.

## File naming inside epic

| File | Required | Notes |
|---|---|---|
| `spec.md` | yes | Single spec file per epic. If multiple PBTs, sections within one file. |
| `test-coverage.md` | yes | One coverage matrix per epic. |
| `test-cases/<feature>.md` | yes (one+) | One file per feature/suite. Filename = feature slug. |
| `test-cases/<feature>.csv` | yes | Generated alongside `.md`, same basename. |

No `README.md` per epic — keep it lean.

## Required YAML front-matter (spec.md only)

Every `spec.md` MUST start with YAML front-matter. This makes the file self-describing and lets tools resolve metadata without parsing prose.

```yaml
---
ticket_id: LT-96620
ticket_url: https://manabie.atlassian.net/browse/LT-96620
title: Nichibei App - Lesson Booking System
module: scheduling
status: In Progress                  # mirror the Jira epic status verbatim
internal_uat_date: 2026-06-10        # ISO date, or null if not scheduled
production_release_date: 2026-07-01  # ISO date, or null if not scheduled
last_updated: 2026-05-21
---
```

### Rules

- `ticket_id` is required and must match the parent folder ID.
- `status` mirrors the Jira epic status string verbatim (no local vocabulary). When the Jira ticket transitions, update this field.
- `internal_uat_date` and `production_release_date` use ISO date (`YYYY-MM-DD`). Use `null` if the date is not yet committed.
- `last_updated` uses ISO date and reflects when this spec file (not the Jira ticket) was last edited.
- For legacy `LT-XXXX-*` folders, set `ticket_id: LT-XXXX` until the real ID is assigned.
- `test-coverage.md` and `test-cases/*.md` do NOT require front-matter — they inherit context from the parent epic folder.

## Path references in skills

Skills MUST reference epic paths via these patterns (never hard-code legacy paths):

| Artifact | Path pattern |
|---|---|
| Spec | `epics/<epic-folder>/spec.md` |
| Coverage | `epics/<epic-folder>/test-coverage.md` |
| Test case MD | `epics/<epic-folder>/test-cases/<feature>.md` |
| Test case CSV | `epics/<epic-folder>/test-cases/<feature>.csv` |

When a skill receives a Jira ID, it resolves the epic folder by listing `epics/LT-<ID>-*`.

## Cross-epic resources

These do NOT belong inside `epics/`:

| Resource | Lives in |
|---|---|
| Domain knowledge | `knowledge/domain-knowledge/` |
| E2E scenarios | `knowledge/e2e-scenario/` |
| Diagrams | `knowledge/diagram/` |
| QA test reports | `reports/test-reports/` |
| Automation review reports | `reports/automation-reviews/` |
| Manual execution records | `reports/manual-executions/` |
| Templates & rules for skills | `.claude/references/` |
| Pipeline data bus (transient) | `temp/` |
