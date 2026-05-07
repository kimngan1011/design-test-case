---
name: workspace-cleanup
description: >
  **WORKFLOW SKILL** — Delete all temp/ data bus files generated during the analyze-requirement workflow, keeping only the official spec output.
  USE FOR: Phase 7 of analyze-requirement agent — final step, also triggered by Stop Hook on Ctrl+C.
  INPUT: None (scans temp/ directory).
  OUTPUT: temp/ directory cleared of all analysis files.
  SAFE TO RUN: Multiple times, independently, even if workflow was interrupted.
---

# Skill: Workspace Cleanup

You are removing all intermediate files generated during the requirement analysis workflow. This is the final step — runs after Phase 6, or automatically when the workflow is stopped.

---

## Cleanup Targets

Delete all of the following if they exist:

| File | Created by |
|------|------------|
| `temp/raw_requirement.json` | `fetch-requirement` |
| `temp/business_rules.json` | `fetch-requirement` |
| `temp/domain_context.json` | `read-domain-knowledge` |
| `temp/current_system_inventory.json` | `search-current-system` |
| `temp/lesson_learned_assessment.json` | `check-lesson-learned` |
| `temp/impact_findings.json` | `analyze-impact` |
| `temp/clarification_questions.json` | `formulate-questions` |

Also delete any files matching:
- `temp/*.tmp`
- `temp/*.draft`
- `temp/*.raw`

---

## Files to PRESERVE (never delete)

- `input/specs/` — all spec files
- `input/domain-knowledge/` — domain knowledge (already updated in Phase 6)
- `input/e2e-scenario/` — e2e scenarios (already updated in Phase 6)
- `output/` — all test case outputs

---

## Workflow

### Step 1 — Scan and list

List all files in `temp/` that match the cleanup targets.

If `temp/` directory does not exist or is empty → log:
```
[workspace-cleanup] No temp files found. Nothing to clean.
```
And exit gracefully.

### Step 2 — Dry-run preview (no user confirmation needed)

Print the list of files that will be deleted (for audit log only — user does not need to approve):

```
[workspace-cleanup] Cleaning up temp/ data bus files:
  - temp/raw_requirement.json
  - temp/business_rules.json
  - temp/domain_context.json
  - temp/current_system_inventory.json
  - temp/lesson_learned_assessment.json
  - temp/impact_findings.json
  - temp/clarification_questions.json
Deleting...
```

### Step 3 — Delete files

Use Bash to delete each file:
```bash
rm -f temp/raw_requirement.json temp/business_rules.json temp/domain_context.json temp/current_system_inventory.json temp/lesson_learned_assessment.json temp/impact_findings.json temp/clarification_questions.json temp/*.tmp temp/*.draft temp/*.raw 2>/dev/null
```

### Step 4 — Confirm completion

Print:
```
[workspace-cleanup] Done. Official outputs preserved:
  - input/specs/<TICKET-ID>/spec.md
  - input/domain-knowledge/ (if updated)
  - input/e2e-scenario/e2e-scenarios.md (if updated)
```

---

## Safety Rules

- **Never delete anything outside `temp/`**
- **Never prompt user** for cleanup confirmation — this is automatic
- **Graceful on failure:** if a file doesn't exist, skip it (use `-f` flag in rm)
- **Idempotent:** safe to run multiple times

---

## Stop Hook Configuration

This skill is also invoked via a Stop Hook in `.claude/settings.json` to handle Ctrl+C:

```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'rm -f temp/raw_requirement.json temp/business_rules.json temp/domain_context.json temp/current_system_inventory.json temp/lesson_learned_assessment.json temp/impact_findings.json temp/clarification_questions.json temp/*.tmp temp/*.draft temp/*.raw 2>/dev/null; echo \"[workspace-cleanup] temp/ cleared on stop\"'"
          }
        ]
      }
    ]
  }
}
```

The Stop Hook runs the same cleanup automatically whenever the Claude process is stopped, ensuring `temp/` is never left with stale data.

---

## Quality Checks

- [ ] Scanned `temp/` for all 7 data bus files + wildcard patterns
- [ ] Dry-run preview printed (no user confirmation needed)
- [ ] All found files deleted with `rm -f` (graceful on missing files)
- [ ] No files outside `temp/` touched
- [ ] Completion message printed with list of preserved official outputs
