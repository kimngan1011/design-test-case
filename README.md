# design-test-case

A GitHub Copilot-powered workspace for automating the full QA test design pipeline — from a Jira ticket to test cases imported into Qase.

## Demo

▶️ [Watch the full pipeline demo](https://drive.google.com/file/d/12WghFmQ2miYe3IPJRVXIeKqRWgiWxx8J/view?usp=sharing)

---

## Overview

This workspace uses a set of Copilot Agent Skills to guide you through four phases of QA work:

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

You can run all phases end-to-end with a single prompt, or run each phase individually.

---

## Quick Start

### Run the full pipeline

```
Process ticket https://manabie.atlassian.net/browse/LT-XXXXX end-to-end.
Import to Qase: https://app.qase.io/project/PX?suite=YYYY
```

Copilot will pause after each phase and ask for confirmation before continuing.

### Run a single phase

| Goal                  | Example prompt                                                        |
| --------------------- | --------------------------------------------------------------------- |
| Analyze a Jira ticket | `Analyze ticket LT-XXXXX`                                             |
| Define test coverage  | `Define test coverage for LT-XXXXX`                                   |
| Generate test cases   | `Generate test cases for LT-XXXXX`                                    |
| Import to Qase        | `Import test cases to Qase https://app.qase.io/project/PX?suite=YYYY` |

---

## Workspace Structure

```
.github/
  copilot-instructions.md     # Registers all skills with Copilot
  skills/
    full-workflow.SKILL.md           # End-to-end pipeline skill
    analyze-requirements.SKILL.md    # Phase 1
    define-test-coverage.SKILL.md    # Phase 2
    generate-test-cases.SKILL.md     # Phase 3
    import-to-qase.SKILL.md          # Phase 4

input/
  specs/                      # Spec files produced by Phase 1
  templates/
    test-case-rules.md        # Test design rules and conventions
    test-coverage.md          # Coverage matrix template
    generate-testcases.md     # Test case generation guide
    qase-format.csv           # Qase CSV import format reference
    test-report.md            # Test report template

output/
  test-cases/                 # Generated .md and .csv test case files
  test-coverages/             # Coverage matrix files
  test-reports/               # Test report files
```

---

## Integrations

The workspace connects to the following tools via MCP servers (configured in `.vscode/mcp.json`):

| Tool           | Purpose                                              |
| -------------- | ---------------------------------------------------- |
| **Jira**       | Fetch ticket requirements, ACs, and linked resources |
| **Confluence** | Read PRD and supplementary documentation             |
| **Figma**      | Reference UI designs                                 |
| **Qase**       | Create suites and import test cases                  |
| **Slack**      | Notify or share results (optional)                   |

> **Security:** `.vscode/mcp.json` is listed in `.gitignore` and must never be committed — it contains API tokens.

---

## Output Naming Conventions

| Artifact         | Path pattern                                                                 |
| ---------------- | ---------------------------------------------------------------------------- |
| Spec file        | `input/specs/<TICKET-ID>: <Feature Name>`                                    |
| Coverage matrix  | `output/test-coverages/<ticket-id>-<feature>.md`                             |
| Test cases (MD)  | `output/test-cases/<module>/<submodule>/<feature>/<name>.md`                 |
| Test cases (CSV) | `output/test-cases/<module>/<submodule>/<feature>/<ticket-id>-<feature>.csv` |

---

## Prerequisites

- VS Code with **GitHub Copilot** (agent mode enabled)
- MCP servers installed and configured in `.vscode/mcp.json`:
  - `jira-mcp`, `confluence-mcp-server`, `qase-mcp-server`, `figma-developer-mcp`, `slack-mcp-server`
- Access to Jira, Confluence, Qase, and Figma for your project
