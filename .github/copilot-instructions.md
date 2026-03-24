# Copilot Instructions

## Available Skills

This workspace has five domain-specific skills. When a user request matches a skill's domain, read the corresponding skill file to get the full instructions before proceeding.

### 0. Full QA Workflow (End-to-End)

**Trigger:** User asks to run the full pipeline, process a ticket full workflow, do everything from Jira to Qase, or run all phases at once.
**Skill file:** `.github/skills/full-workflow.SKILL.md`

### 1. Analyze Requirements

**Trigger:** User asks to analyze a Jira ticket, onboard a new ticket, fetch requirements, or produce a spec file.
**Skill file:** `.github/skills/analyze-requirements.SKILL.md`

### 2. Define Test Coverage

**Trigger:** User asks to define test coverage, create a coverage matrix, plan test strategy, or categorize business rules.
**Skill file:** `.github/skills/define-test-coverage.SKILL.md`

### 3. Generate Test Cases

**Trigger:** User asks to generate test cases, write test steps, produce preconditions/expected results, or create `.md`/`.csv` test case output files.
**Skill file:** `.github/skills/generate-test-cases.SKILL.md`

### 4. Import to Qase

**Trigger:** User asks to import test cases to Qase, upload test cases, create Qase suites, or sync local test case files with Qase.
**Skill file:** `.github/skills/import-to-qase.SKILL.md`

### 5. Review Automation Test Run

**Trigger:** User asks to review an automation test run, check test results from Qase, analyze step-results.md files, compare execution vs. test case definitions, or export a review report.
**Skill file:** `.github/skills/review-automation-tests.SKILL.md`

### 6. Execute Test Cases (Manual via Playwright)

**Trigger:** User asks to execute a test case, run a Qase test case manually, perform a test on SF sandbox, verify test steps on Salesforce, or create an execution record.
**Skill file:** `.github/skills/execute-test-cases.SKILL.md`

---

## Workspace Structure

- `input/specs/` — spec files produced by the analyze-requirements skill
- `input/templates/` — reusable templates (test-case-rules, qase-format, test-coverage, test-report)
- `output/test-cases/` — generated test case files (`.md` and `.csv`)
- `output/test-coverages/` — coverage matrix files
- `output/test-reports/` — test report files
- `output/review-automation-tests/` — automation run review reports
- `output/execute-test-cases/` — manual test execution records (organised by Jira ticket)
