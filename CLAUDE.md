# CLAUDE.md — QA Test Design Workspace

This workspace automates the full QA test design pipeline for the Manabie lesson-management system.

## Pipeline Overview

```
Jira Ticket
    ↓
Phase 1 — Analyze Requirements    →  epics/<TICKET-ID>-<slug>/spec.md
    ↓
Phase 2 — Define Test Coverage    →  epics/<TICKET-ID>-<slug>/test-coverage.md
    ↓
Phase 3 — Generate Test Cases     →  epics/<TICKET-ID>-<slug>/test-cases/
    ↓
Phase 4 — Import to Qase          →  Qase project (suites + cases)
```

## Available Slash Commands

| Command | Trigger | Definition |
|---------|---------|------------|
| `/analyze-requirements` | Analyze a Jira ticket, fetch requirements, produce spec file | `.claude/agents/analyze-requirement.agent.md` |
| `/define-test-coverage` | Define coverage matrix, plan test strategy | `.claude/skills/define-test-coverage/SKILL.md` |
| `/generate-test-cases` | Generate test cases from a coverage file | `.claude/skills/generate-test-cases/SKILL.md` |
| `/import-to-qase` | Import test cases to Qase | `.claude/skills/import-to-qase/SKILL.md` |
| `/create-test-runs` | Create test runs from a Qase test plan | `.claude/skills/create-test-runs/SKILL.md` |
| `/verify-bug` | Verify a bug report using Playwright | `.claude/skills/verify-bug/SKILL.md` |
| `/full-workflow` | Run all phases end-to-end | `.claude/skills/full-workflow/SKILL.md` |
| `/review-automation-tests` | Review automation results from a Qase run | `.claude/skills/review-automation-tests/SKILL.md` |
| `/update-report-confluence` | Update a Confluence QA report from a Qase run | `.claude/skills/update-report-confluence/SKILL.md` |
| `/save-slack-issue` | Save a Slack production-issue thread as a lesson-learned entry | `.claude/skills/save-slack-issue/SKILL.md` |

## Quick Start

### Full pipeline (end-to-end)

```
/full-workflow https://manabie.atlassian.net/browse/LT-XXXXX
Import to Qase: https://app.qase.io/project/PX?suite=YYYY
```

### Single phase

```
/analyze-requirements LT-XXXXX
/define-test-coverage epics/LT-XXXXX-<slug>/spec.md
/generate-test-cases epics/LT-XXXXX-<slug>/test-coverage.md
/import-to-qase https://app.qase.io/project/PX?suite=YYYY epics/LT-XXXXX-<slug>/test-cases/<file>.csv
```

### Bug verification

```
/verify-bug LT-XXXXX on staging
```

## Workspace Structure

- `epics/<TICKET-ID>-<slug>/` — per-epic artifacts (spec + test-coverage + test-cases)
- `knowledge/domain-knowledge/` — domain knowledge files (per-team folders, lesson-learned)
- `knowledge/e2e-scenario/` — cross-epic E2E scenarios
- `knowledge/diagram/` — domain diagrams
- `reports/test-reports/` — QA test reports
- `reports/automation-reviews/` — automation run review reports
- `reports/manual-executions/` — manual test execution records
- `temp/` — transient data bus for the analyze-requirement workflow (auto-cleaned)
- `automation/` — Playwright automation source

## Conventions

- Epic folders, naming, and `spec.md` front-matter: `.claude/references/epic-folder-convention.md`
- Data bus schemas (`temp/*.json`): `.claude/references/data-bus-schemas.md`
- Test case design rules: `.claude/references/test-case-rules.md`
- Coverage rules + edge-case checklist: `.claude/references/coverage-rules.md` + `coverage-edge-case-checklist.md`

## MCP Tools Available

- **Playwright** — browser automation for bug verification
- **Jira** — fetch tickets, add comments
- **Qase** — list/create suites, cases, test runs
- **Confluence** — read/update documentation pages
- **Slack** — read threads (for save-slack-issue)
- **Figma** — extract design data (for spec–Figma mismatch checks)

## Domain Knowledge

Always read relevant domain knowledge files before analyzing requirements:
- `knowledge/domain-knowledge/scheduling/overview.md` — file index + system overview + master data + data relationships
- `knowledge/domain-knowledge/scheduling/{lesson-management,event,calendar,partner-rules}/*.md` — per-domain detail (read by filename match)
- `knowledge/domain-knowledge/scheduling/lesson-learned/{core,oop}.md` — known issues and design notes

## Memory

Environment credentials are stored in:
`/Users/manabie/.claude/projects/-Users-manabie-design-test-case/memory/environments.md`
