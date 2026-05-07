# CLAUDE.md — QA Test Design Workspace

This workspace automates the full QA test design pipeline for the Manabie lesson-management system.

## Pipeline Overview

```
Jira Ticket
    ↓
Phase 1 — Analyze Requirements    →  input/specs/
    ↓
Phase 2 — Define Test Coverage    →  output/test-coverages/
    ↓
Phase 3 — Generate Test Cases     →  output/test-cases/
    ↓
Phase 4 — Import to Qase          →  Qase project (suites + cases)
```

## Available Slash Commands

| Command | Trigger | Skill file |
|---------|---------|------------|
| `/analyze-requirements` | Analyze a Jira ticket, fetch requirements, produce spec file | `.claude/agents/analyze-requirement.agent.md` |
| `/define-test-coverage` | Define coverage matrix, plan test strategy | `.claude/commands/define-test-coverage.md` |
| `/generate-test-cases` | Generate test cases from a coverage file | `.claude/commands/generate-test-cases.md` |
| `/import-to-qase` | Import test cases to Qase | `.claude/commands/import-to-qase.md` |
| `/convert-test-cases` | Convert test cases to JSON for automation | `.claude/commands/convert-test-cases.md` |
| `/execute-test-cases` | Execute JSON test cases via Playwright | `.claude/commands/execute-test-cases.md` |
| `/create-test-runs` | Create test runs from a Qase test plan | `.claude/commands/create-test-runs.md` |
| `/verify-bug` | Verify a bug report using Playwright | `.claude/commands/verify-bug.md` |
| `/full-workflow` | Run all phases end-to-end | `.claude/commands/full-workflow.md` |

## Quick Start

### Full pipeline (end-to-end)

```
/full-workflow https://manabie.atlassian.net/browse/LT-XXXXX
Import to Qase: https://app.qase.io/project/PX?suite=YYYY
```

### Single phase

```
/analyze-requirements LT-XXXXX
/define-test-coverage input/specs/LT-XXXXX: Feature Name
/generate-test-cases output/test-coverages/LT-XXXXX-feature-name.md
/import-to-qase https://app.qase.io/project/PX?suite=YYYY output/test-cases/...
```

### Bug verification

```
/verify-bug LT-XXXXX on staging
```

### Test execution

```
/convert-test-cases output/test-cases/lesson-management/feature/file.md
/execute-test-cases input/test-cases/module/feature.json on staging
```

## Workspace Structure

- `input/specs/` — spec files produced by analyze-requirements
- `input/templates/` — reusable templates (test-case-rules, qase-format, test-coverage, test-report)
- `input/test-cases/` — structured JSON test cases for automation
- `input/domain-knowledge/` — domain knowledge files (scheduling rules, lesson-learned)
- `output/test-cases/` — generated test case files (`.md` and `.csv`)
- `output/test-coverages/` — coverage matrix files
- `output/test-reports/` — test report files
- `output/review-automation-tests/` — automation run review reports
- `output/execute-test-cases/` — manual test execution records

## MCP Tools Available

- **Playwright** — browser automation for bug verification and test execution
- **Jira** — fetch tickets, add comments
- **Qase** — list/create suites, cases, test runs
- **Confluence** — read documentation pages

## Domain Knowledge

Always read relevant domain knowledge files before analyzing requirements:
- `input/domain-knowledge/scheduling-domain-knowledge.md` — scheduling business rules
- `input/domain-knowledge/lesson-learned/core.md` — known issues and design notes

## Memory

Environment credentials are stored in:
`/Users/manabie/.claude/projects/-Users-manabie-design-test-case/memory/environments.md`
