# Copilot Instructions

## Available Skills

This workspace has domain-specific skills. All skill files live in `.claude/skills/<skill-name>/SKILL.md`.
When a user request matches a skill's domain, read the corresponding skill file to get
the full instructions before proceeding.

### 0. Full QA Workflow (End-to-End)

**Trigger:** User asks to run the full pipeline, process a ticket full workflow, do everything from Jira to Qase, or run all phases at once.
**Skill file:** `.claude/skills/full-workflow/SKILL.md`

### 1. Analyze Requirements (Master Agent)

**Trigger:** User asks to analyze a Jira ticket, onboard a new ticket, fetch requirements, or produce a spec file.
**Agent file:** `.claude/agents/analyze-requirement.agent.md`
**Sub-skills:** fetch-requirement, read-domain-knowledge, search-current-system, check-lesson-learned, analyze-impact, formulate-questions, update-domain-knowledge, update-e2e-scenarios, workspace-cleanup

> **Note:** The old `analyze-requirements` skill has been deleted. Use the master agent above.

### 2. Define Test Coverage

**Trigger:** User asks to define test coverage, create a coverage matrix, plan test strategy, or categorize business rules.
**Skill file:** `.claude/skills/define-test-coverage/SKILL.md`

### 3. Generate Test Cases

**Trigger:** User asks to generate test cases, write test steps, produce preconditions/expected results, or create `.md`/`.csv` test case output files.
**Skill file:** `.claude/skills/generate-test-cases/SKILL.md`

### 4. Import to Qase

**Trigger:** User asks to import test cases to Qase, upload test cases, create Qase suites, or sync local test case files with Qase.
**Skill file:** `.claude/skills/import-to-qase/SKILL.md`

### 5. Review Automation Test Run

**Trigger:** User asks to review an automation test run, check test results from Qase, analyze step-results.md files, compare execution vs. test case definitions, or export a review report.
**Skill file:** `.claude/skills/review-automation-tests/SKILL.md`

### 6. Execute Test Cases (Manual via Playwright)

**Trigger:** User asks to execute a test case, run a Qase test case manually, perform a test on SF sandbox, verify test steps on Salesforce, or create an execution record.
**Skill file:** `.claude/skills/execute-test-cases/SKILL.md`

### 7. Update QA Report

**Trigger:** User asks to update the QA report, update QA test report on Confluence, add test results to a Confluence report page, publish test coverage and results to Confluence, or update the acceptance test coverage table.
**Skill file:** `.claude/skills/update-report-confluence/SKILL.md`

### 8. Create Test Runs from Qase Test Plan

**Trigger:** User asks to create test runs from a Qase test plan, set up test runs for team members, bulk-create runs from a plan template, or create regression test runs from a plan.
**Skill file:** `.claude/skills/create-test-runs/SKILL.md`

### 9. Save Slack Issue to Lesson Learned

**Trigger:** User asks to save a Slack thread, document a production incident, log a post-mortem, record a lesson learned from Slack, or add an issue entry to domain knowledge.
**Skill file:** `.claude/skills/save-slack-issue/SKILL.md`

### 10. Verify Bug

**Trigger:** User asks to verify a bug, reproduce a Jira bug ticket, check if a bug is still present, confirm a reported issue on staging/uat/prod.
**Skill file:** `.claude/skills/verify-bug/SKILL.md`

### 11. Convert Test Cases to JSON

**Trigger:** User asks to convert test cases to JSON, structure test cases for automation, save test cases as JSON for Playwright execution.
**Skill file:** `.claude/skills/convert-test-cases/SKILL.md`

---

## Skill Index

All skills are in `.claude/skills/`. Each skill is a subfolder containing a `SKILL.md` file.

```
.claude/agents/
├── analyze-requirement.agent.md      # Master agent — requirement analysis (7 phases)
├── automation-test-runner.agent.md   # Convert + execute test cases via Playwright
└── review-e2e-scenario.agent.md      # Audit E2E scenario coverage

.claude/skills/
├── fetch-requirement/SKILL.md        # Phase 1a: Fetch Jira + Confluence + Figma
├── read-domain-knowledge/SKILL.md    # Phase 1b: Load domain context
├── search-current-system/SKILL.md    # Phase 1c: Search local specs/tests/e2e
├── check-lesson-learned/SKILL.md     # Phase 2a: Cross-reference past incidents
├── analyze-impact/SKILL.md           # Phase 2b: Conflict & gap analysis
├── formulate-questions/SKILL.md      # Phase 3a: Generate clarification questions
├── update-domain-knowledge/SKILL.md  # Phase 6a: Update domain knowledge (post-approval)
├── update-e2e-scenarios/SKILL.md     # Phase 6b: Update E2E scenarios (post-approval)
├── workspace-cleanup/SKILL.md        # Phase 7: Clean temp/ data bus files
├── convert-test-cases/SKILL.md
├── create-test-runs/SKILL.md
├── define-test-coverage/SKILL.md
├── execute-test-cases/SKILL.md
├── full-workflow/SKILL.md
├── generate-test-cases/SKILL.md
├── import-to-qase/SKILL.md
├── review-automation-tests/SKILL.md
├── save-slack-issue/SKILL.md
├── update-report-confluence/SKILL.md
└── verify-bug/SKILL.md
```

---

## Workspace Structure

- `.claude/skills/` — skill definition files, one subfolder per skill
- `.claude/agents/` — agent definition files (`.agent.md`)
- `input/specs/` — spec files produced by the analyze-requirements skill
- `input/templates/` — reusable templates (test-case-rules, qase-format, test-coverage, test-report)
- `input/domain-knowledge/` — domain knowledge files (scheduling rules, lesson-learned)
- `output/test-cases/` — generated test case files (`.md` and `.csv`)
- `output/test-coverages/` — coverage matrix files
- `output/test-reports/` — test report files
- `output/review-automation-tests/` — automation run review reports
- `output/execute-test-cases/` — manual test execution records (organised by Jira ticket)
- `e2e/` — Playwright + TypeScript automation project
  - `e2e/src/pages/` — Page Object Model (sf/ and bo/ sub-folders)
  - `e2e/src/fixtures/` — Playwright fixtures (page objects injected into tests)
  - `e2e/src/helpers/` — qase.ts, step.ts, test-data.ts
  - `e2e/tests/` — spec files mirroring `output/test-cases/lesson-management/`
