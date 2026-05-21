# Epic Folder Convention

The workspace organizes QA artifacts **per epic**. One Jira epic = one folder containing all related files (spec, coverage, test cases). Epic folders are grouped by **domain bucket** under `epics/`.

## Layout

```
epics/
├── lesson/                       # Core lesson functionality
│   └── LT-<ID>-<slug>/
│       ├── spec.md
│       ├── test-coverage.md
│       └── test-cases/
│           ├── <feature>.md
│           └── <feature>.csv
├── event/                        # Core event functionality
├── calendar/                     # Core calendar functionality
├── cross-domain/                 # Features touching multiple domains (lesson + event + calendar + master data)
├── master-data/                  # Academic Calendar, Course Master, Location, etc.
└── OOP/                          # Partner-specific features (feature-flag or config gated per tenant)
    ├── aso/
    ├── koyu/
    ├── nichibei/
    ├── renseikai/
    └── riso/
```

## Bucket placement rules

Pick the bucket by primary effect of the epic:

| Bucket | When to use |
|---|---|
| `lesson/` | Lesson entity, student session, lesson teacher, lesson report, lesson mobile, configure-alert, attendance — all core (no partner gate). |
| `event/` | Event Master, Activity Event, Booking System, Events on Calendar — all core. |
| `calendar/` | SF/BO Calendar features (drag&drop, view, filter, bulk publish UI). Even if a calendar feature is partner-gated by config, place it here if the primary surface is the Calendar. |
| `cross-domain/` | Feature explicitly spans 2+ domains (e.g. student classification on event + lesson + calendar; deduplication across student + teacher; multi-class lessons that affect both lesson creation and class auto-assignment). |
| `master-data/` | Master data entities: Academic Calendar (ACM/ACI), Course Master, Course Category, Location, Class, Program Master, etc. |
| `OOP/<tenant>/` | Feature only enabled for a specific partner (`aso` / `koyu` / `nichibei` / `renseikai` / `riso`). Tenant subfolder is lowercased. |

> When in doubt between `cross-domain/` and a single bucket: if the spec dedicates dedicated AC sections to multiple domains, use `cross-domain/`. If most ACs live in one domain with side-effects elsewhere, use that domain's bucket.

## Folder naming

- **Format**: `LT-<JiraID>-<slug>`
- **Slug**: kebab-case, lowercase, **derived from the Jira title but shortened**.
  - Source: Jira ticket title is the canonical source of truth.
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
- Place in the correct bucket regardless of placeholder ID.

## File naming inside epic

| File | Required | Notes |
|---|---|---|
| `spec.md` | yes | Single spec file per epic. If multiple PBTs, sections within one file. |
| `test-coverage.md` | yes | One coverage matrix per epic. |
| `test-cases/<feature>.md` | yes (one+) | One file per feature/suite. Filename = feature slug. |
| `test-cases/<feature>.csv` | yes | Generated alongside `.md`, same basename. |

No `README.md` per epic — keep it lean.

## Required YAML front-matter (spec.md only)

Every `spec.md` MUST start with YAML front-matter. Tools resolve metadata without parsing prose.

```yaml
---
ticket_id: LT-96620
ticket_url: https://manabie.atlassian.net/browse/LT-96620
title: Nichibei App - Lesson Booking System
module: scheduling
bucket: OOP/nichibei                 # mirrors the bucket path under epics/
status: In Progress                  # mirror the Jira epic status verbatim
internal_uat_date: 2026-06-10        # ISO date, or null if not scheduled
production_release_date: 2026-07-01  # ISO date, or null if not scheduled
last_updated: 2026-05-21
---
```

### Rules

- `ticket_id` required and must match the parent folder ID.
- `bucket` mirrors the path under `epics/` (e.g. `lesson`, `event`, `calendar`, `cross-domain`, `master-data`, `OOP/nichibei`). When the bucket changes (e.g. promoted from `cross-domain` to a single domain), update this field.
- `status` mirrors the Jira epic status string verbatim (no local vocabulary). When the Jira ticket transitions, update.
- `internal_uat_date` and `production_release_date` use ISO date (`YYYY-MM-DD`). Use `null` if not committed.
- `last_updated` uses ISO date and reflects when the spec file (not the Jira ticket) was last edited.
- For legacy `LT-XXXX-*` folders, set `ticket_id: LT-XXXX` until the real ID is assigned.
- `test-coverage.md` and `test-cases/*.md` do NOT require front-matter — they inherit context from the parent epic folder.

## Path references in skills

Skills MUST reference epic paths via these patterns (never hard-code legacy paths):

| Artifact | Path pattern |
|---|---|
| Spec | `epics/<bucket>/<epic-folder>/spec.md` |
| Coverage | `epics/<bucket>/<epic-folder>/test-coverage.md` |
| Test case MD | `epics/<bucket>/<epic-folder>/test-cases/<feature>.md` |
| Test case CSV | `epics/<bucket>/<epic-folder>/test-cases/<feature>.csv` |

Where `<bucket>` is one of `lesson` / `event` / `calendar` / `cross-domain` / `master-data` / `OOP/<tenant>`.

When a skill receives a Jira ID and needs to resolve the epic folder, it must search across all buckets:
```
find epics -type d -name "LT-<ID>-*" -maxdepth 4
```

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
