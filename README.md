# design-test-case

A Claude Code–powered workspace for automating the full QA test design pipeline — from a Jira ticket to test cases imported into Qase.

## Demo

▶️ [Watch the full pipeline demo](https://drive.google.com/file/d/12WghFmQ2miYe3IPJRVXIeKqRWgiWxx8J/view?usp=sharing)

---

## Overview

This workspace uses a set of Claude Code Skills and Agents to guide you through four phases of QA work. Each Jira epic gets its own folder under `epics/` that contains the spec, test coverage, and test cases for that epic.

```
Jira Ticket
    ↓
Phase 1 — Analyze Requirements    →  epics/<bucket>/<TICKET-ID>-<slug>/spec.md
    ↓
Phase 2 — Define Test Coverage    →  epics/<bucket>/<TICKET-ID>-<slug>/test-coverage.md
    ↓
Phase 3 — Generate Test Cases     →  epics/<bucket>/<TICKET-ID>-<slug>/test-cases/
    ↓
Phase 4 — Import to Qase          →  Qase project (suites + cases)
```

You can run all phases end-to-end with a single prompt, or run each phase individually.

---

## Quick Start

### Run the full pipeline

```
Process ticket https://manabie.atlassian.net/browse/LT-XXXXX end-to-end.
Import to Qase: https://app.qase.io/project/PX?suite=YYYY
```

Claude will pause after each phase and ask for confirmation before continuing.

### Run a single phase

| Goal | Example prompt |
|---|---|
| Analyze a Jira ticket | `Analyze ticket LT-XXXXX` |
| Define test coverage | `Define test coverage for LT-XXXXX` |
| Generate test cases | `Generate test cases for LT-XXXXX` |
| Import to Qase | `Import test cases to Qase https://app.qase.io/project/PX?suite=YYYY` |

---

## Workspace Structure

```
.claude/
  agents/                              # Orchestrator agents (≤150 lines each)
    analyze-requirement.agent.md       # Phase 1 master agent (7 internal phases)
    full-qa-pipeline.agent.md          # End-to-end pipeline
    review-e2e-scenario.agent.md       # E2E coverage audit
  skills/                              # Workflow skills (≤150 lines each)
    fetch-requirement/  read-domain-knowledge/  search-current-system/
    check-lesson-learned/  analyze-impact/  formulate-questions/
    workspace-cleanup/  update-domain-knowledge/  update-e2e-scenarios/
    define-test-coverage/  generate-test-cases/  import-to-qase/
    create-test-runs/  review-automation-tests/  update-report-confluence/
    verify-bug/  save-slack-issue/  full-workflow/
  references/                          # Rules, templates, schemas (extracted from skills)

epics/                                 # Per-epic artifacts
  LT-<TICKET-ID>-<slug>/
    spec.md                            # Required YAML front-matter; produced by Phase 1
    test-coverage.md                   # Produced by Phase 2
    test-cases/                        # Produced by Phase 3
      <feature>.md
      <feature>.csv

knowledge/                             # Cross-epic resources
  domain-knowledge/<team>/             # Domain rules + lesson-learned
  e2e-scenario/e2e-scenarios.md        # E2E business flow scenarios
  diagram/                             # Domain diagrams

reports/
  automation-reviews/                  # Output of review-automation-tests
  qase-snapshots/                      # Qase project exports

temp/                                  # Transient data bus (auto-cleaned)
automation/                            # Playwright automation source
```

See `.claude/references/epic-folder-convention.md` for the full epic folder spec (naming, slug rules, required front-matter, legacy `LT-XXXX-` handling).

---

## Integrations

The workspace connects to the following tools via MCP servers (configured in `.vscode/mcp.json`):

| Tool | Purpose |
|---|---|
| **Jira** | Fetch ticket requirements, ACs, and linked resources |
| **Confluence** | Read PRDs and supplementary documentation; update QA report pages |
| **Figma** | Reference UI designs; spec–Figma mismatch detection |
| **Qase** | Create suites, import test cases, create test runs |
| **Slack** | Read production-issue threads (save-slack-issue) |
| **Playwright** | Browser automation for bug verification |

> **Security:** `.vscode/mcp.json` is listed in `.gitignore` and must never be committed — it contains API tokens.

---

## Path conventions

| Artifact | Path pattern |
|---|---|
| Spec | `epics/<bucket>/<TICKET-ID>-<slug>/spec.md` |
| Coverage matrix | `epics/<bucket>/<TICKET-ID>-<slug>/test-coverage.md` |
| Test cases (MD) | `epics/<bucket>/<TICKET-ID>-<slug>/test-cases/<feature>.md` |
| Test cases (CSV) | `epics/<bucket>/<TICKET-ID>-<slug>/test-cases/<feature>.csv` |
| Domain knowledge | `knowledge/domain-knowledge/<team>/<team>-domain-knowledge.md` |
| Lesson-learned | `knowledge/domain-knowledge/<team>/lesson-learned/{core,oop}.md` |
| E2E scenarios | `knowledge/e2e-scenario/e2e-scenarios.md` |

Legacy work without a Jira ticket uses `epics/LT-XXXX-<descriptive-slug>/` as a placeholder; the prefix is renamed once the real ticket ID is assigned.

---

## Prerequisites

- **Claude Code** (CLI, desktop app, or VS Code extension)
- MCP servers installed and configured in `.vscode/mcp.json`:
  - `jira-mcp`, `confluence-mcp-server`, `qase-mcp-server`, `figma-developer-mcp`, `slack-mcp-server`, `playwright`
- Access to Jira, Confluence, Qase, and Figma for your project
