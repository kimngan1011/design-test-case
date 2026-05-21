---
name: update-e2e-scenarios
description: >
  **WORKFLOW SKILL** — Update or create E2E scenarios to cover a new requirement, with mandatory AC-mapping for every step.
  USE FOR: Phase 6b of analyze-requirement agent — runs after user approves questions posted to Jira.
  INPUT: temp/impact_findings.json + temp/raw_requirement.json (already on disk).
  OUTPUT: Updated knowledge/e2e-scenario/e2e-scenarios.md (after user diff review and approval).
  DO NOT USE FOR: auditing existing E2E coverage (use review-e2e-scenario agent for that).
---

# Skill: Update E2E Scenarios

Update or create E2E scenarios to cover business flows introduced by a new requirement. Every proposed step must be mapped to an AC reference.

## Input
Read from disk (do not rely on chat context):
- `temp/impact_findings.json` — `e2e_scenario_impact` section.
- `temp/raw_requirement.json` — feature name, AC list.

Also read `knowledge/e2e-scenario/e2e-scenarios.md` in full to understand existing format.

## References
- Schemas for `temp/*.json` → `.claude/references/data-bus-schemas.md`

---

## Workflow

### Step 1 — Understand existing scenario format
From `knowledge/e2e-scenario/e2e-scenarios.md`, note:
- Numbering (E2E-XX).
- Table format (# | Platform | Action | Expected).
- Platform tags: `[SF]`, `[BO]`, `[Mobile]`, `[System]`.
- "Features covered" section format at end of each scenario.

### Step 2 — Determine update vs create
From `temp/impact_findings.json` → `e2e_scenario_impact`:

| `action_needed` | Decision |
|---|---|
| `UPDATE` | Extend existing scenario with new steps. |
| `CREATE` | Draft a new scenario. |

> **Prefer extending over creating.** If 1–3 new steps fit within an existing scenario, extend it. Only create a new scenario for a genuinely distinct business flow.

### Step 3 — Draft changes with AC-mapping
For every proposed step (whether updating or creating), build an **AC-Mapping Table** FIRST:

| Step # | Step Description | AC Ref | Platform | Mapped? |
|--------|------------------|--------|----------|---------|
| 15 | Click "Publish & Notify" | AC 01.1 | [SF] | ✅ |
| 16 | Verify confirmation modal | AC 02.2 | [SF] | ✅ |
| 17 | Verify notification on Mobile | AC 02.1 | [Mobile] | ✅ |

Auto-flag unmapped steps: `⚠️ UNMAPPED_STEP — no AC reference`.

**Do NOT add unmapped steps** to the scenario unless the user explicitly confirms. Unmapped steps cause automation failures during the Qase AC mapping.

### Step 4 — Apply E2E standards
- **Step count ≤ 20** per scenario. If exceeded → split the scenario.
- **Platform tags** on every step (`[SF]`, `[BO]`, `[Mobile]`, `[System]`).
- **Format** matches existing document style exactly.
- **Features covered** section updated to reflect new Qase suite areas.

For new scenarios:
- Assign the next available E2E-XX number.
- Must include a "Features covered" section.
- Must follow the Core Verification Principle: Create Lesson → Assign Students → Publish → Verify Mobile (or explicitly state which step is excluded and why).

### Step 5 — Present diff for user review (MANDATORY before writing)
Show a complete preview structured as:

```
=== E2E SCENARIO CHANGES PREVIEW ===

📝 UPDATED scenarios:
  E2E-XX — "<title>"
  Current steps: N
  Proposed additions: + Step ... (AC Ref) ✅
  New step count: M ✅ (≤ 20)
  AC-Mapping Table: (full table per Step 3)

🆕 NEW scenarios:
  E2E-XX — "<title>"
  Total steps: N ✅ (≤ 20)
  Full step list with AC refs
  AC-Mapping Table: (full table per Step 3)

Confirm apply these changes? (Y/N)
```

Each updated/new scenario block must include its complete AC-Mapping Table.

### Step 6 — Apply confirmed changes
Write to `knowledge/e2e-scenario/e2e-scenarios.md` only after explicit `Y`.

If user says `N` → log "E2E update cancelled by user" and proceed to Phase 7.
If user modifies proposed steps → incorporate edits and re-show the diff before writing.

---

## Quality checks
- Read `temp/impact_findings.json` + `temp/raw_requirement.json` from disk.
- Read `knowledge/e2e-scenario/e2e-scenarios.md` for existing format.
- Preferred extending existing scenarios over creating new ones.
- AC-Mapping Table built for every proposed step.
- No unmapped steps added without explicit user confirmation.
- Step count ≤ 20 per scenario.
- Platform tags on every step.
- Format matches existing document style.
- "Features covered" section updated.
- Full diff preview shown before any write.
- Waited for explicit Y before writing.
