---
name: update-e2e-scenarios
description: >
  **WORKFLOW SKILL** — Update or create E2E scenarios to cover a new requirement, with mandatory AC-mapping for every step.
  USE FOR: Phase 6b of analyze-requirement agent — runs after user approves questions posted to Jira.
  INPUT: temp/impact_findings.json + temp/raw_requirement.json (already on disk).
  OUTPUT: Updated input/e2e-scenario/e2e-scenarios.md (after user diff review and approval).
  DO NOT USE FOR: auditing existing E2E coverage (use review-e2e-scenario agent for that).
---

# Skill: Update E2E Scenarios

You are updating or creating E2E scenarios to cover the business flows introduced by a new requirement. Every step you propose must be mapped to an AC reference.

---

## Input

Read from disk (do not rely on chat context):
- `temp/impact_findings.json` — `e2e_scenario_impact` section (which scenarios need updating, which are new)
- `temp/raw_requirement.json` — feature name, AC list (for AC-mapping)

Also read `input/e2e-scenario/e2e-scenarios.md` in full to understand existing format.

---

## Workflow

### Step 1 — Understand existing scenario format

From `input/e2e-scenario/e2e-scenarios.md`, note:
- How scenarios are numbered (E2E-XX)
- Table format for steps (# | Platform | Action | Expected)
- Platform tags: `[SF]`, `[BO]`, `[Mobile]`, `[System]`
- "Features covered" section format at end of each scenario

### Step 2 — Determine update vs new

From `temp/impact_findings.json` → `e2e_scenario_impact`:

| action_needed | Decision |
|--------------|----------|
| `UPDATE` | Extend existing scenario with new steps |
| `CREATE` | Draft a new scenario |

> **Prefer extending over creating.** If adding 1–3 steps covers the new requirement within an existing scenario, extend it. Only create a new scenario if the new feature represents a genuinely distinct business flow.

### Step 3 — Draft changes with AC-Mapping

For every step you propose to ADD (whether updating or creating):

**Mandatory: Build AC-Mapping Table first**

```
| Step # | Step Description              | AC Ref  | Platform  | Mapped? |
|--------|-------------------------------|---------|-----------|---------|
| 15     | Click "Publish & Notify"      | AC 01.1 | [SF]      | ✅      |
| 16     | Verify confirmation modal     | AC 02.2 | [SF]      | ✅      |
| 17     | Click "Send" in modal         | AC 02.1 | [SF]      | ✅      |
| 18     | Verify notification on Mobile | AC 02.1 | [Mobile]  | ✅      |
```

**Auto-flag unmapped steps:**
If a step cannot be mapped to any AC → mark as `⚠️ UNMAPPED_STEP — no AC reference`

**Do NOT add unmapped steps** to the scenario unless user explicitly confirms. Unmapped steps create automation failures when the automation tries to map steps to Qase ACs.

### Step 4 — Apply E2E standards

Before finalizing proposed changes:

- **Step count:** Each scenario must have ≤ 20 steps. If adding steps would exceed 20 → split the scenario
- **Platform tags:** Every step must have a platform tag (`[SF]`, `[BO]`, `[Mobile]`, `[System]`)
- **Format:** Must match exact format of surrounding scenarios (numbered table, same column headers)
- **Features covered:** Update the "Features covered" section to reflect new Qase suite areas

For new scenarios:
- Assign the next available E2E-XX number
- Must include a "Features covered" section
- Must follow the Core Verification Principle: Create Lesson → Assign Students → Publish → Verify Mobile (or explicitly state which step is excluded and why)

### Step 5 — Present diff for user review

**MANDATORY before writing.** Show the complete preview of all changes:

```
=== E2E SCENARIO CHANGES PREVIEW ===

📝 UPDATED scenarios:

E2E-02 — "Create recurring lesson + assign student"
Current steps: 14
Proposed additions:
  + Step 15: [SF] Click "Publish & Notify" button on lesson detail   (AC 01.1) ✅
  + Step 16: [SF] Confirm sending in modal — click "Send"             (AC 02.2, AC 02.1) ✅
  + Step 17: [Mobile] Student receives push notification              (AC 02.1) ✅
New step count: 17 ✅ (≤ 20)

AC-Mapping Table:
| Step # | Description                    | AC Ref       | Platform | Mapped? |
|--------|-------------------------------|--------------|----------|---------|
| 15     | Click "Publish & Notify"      | AC 01.1      | [SF]     | ✅      |
| 16     | Confirm in modal              | AC 02.2+02.1 | [SF]     | ✅      |
| 17     | Verify notification           | AC 02.1      | [Mobile] | ✅      |

🆕 NEW scenarios:

E2E-37 — "[Renseikai] Publish lesson and notify student"
Steps:
  Step 1: [SF] Create Draft lesson with required fields      (AC 01.1) ✅
  Step 2: [SF] Assign student to lesson                      (AC 02.1) ✅
  Step 3: [SF] Click "Publish & Notify" button               (AC 01.1) ✅
  Step 4: [SF] Confirm sending in modal — click "Send"       (AC 02.2) ✅
  Step 5: [SF] Verify lesson status changed to Published     (AC 01.2) ✅
  Step 6: [Mobile] Login as assigned student                 (AC 02.1) ✅
  Step 7: [Mobile] Verify push notification received         (AC 02.1) ✅
  Step 8: [Mobile] Tap notification — navigate to Lesson     (AC 03.1) ✅
Total steps: 8 ✅ (≤ 20)

AC-Mapping Table:
| Step # | Description              | AC Ref  | Platform | Mapped? |
|--------|--------------------------|---------|----------|---------|
| 1      | Create Draft lesson      | AC 01.1 | [SF]     | ✅      |
| 2      | Assign student           | AC 02.1 | [SF]     | ✅      |
| 3      | Click Publish & Notify   | AC 01.1 | [SF]     | ✅      |
| 4      | Confirm in modal         | AC 02.2 | [SF]     | ✅      |
| 5      | Verify Published status  | AC 01.2 | [SF]     | ✅      |
| 6      | Login as student         | AC 02.1 | [Mobile] | ✅      |
| 7      | Verify notification      | AC 02.1 | [Mobile] | ✅      |
| 8      | Deep-link navigation     | AC 03.1 | [Mobile] | ✅      |

Confirm apply these changes? (Y/N)
```

### Step 6 — Apply confirmed changes

Only write to `input/e2e-scenario/e2e-scenarios.md` after user explicitly confirms Y.

If user says N → log "E2E update cancelled by user" and proceed to Phase 7.
If user modifies proposed steps → incorporate edits and re-show the diff before writing.

---

## Quality Checks

- [ ] Read `temp/impact_findings.json` and `temp/raw_requirement.json` from disk
- [ ] Read `input/e2e-scenario/e2e-scenarios.md` for existing format
- [ ] Preferred extending existing scenarios over creating new ones
- [ ] AC-Mapping Table built for every proposed step
- [ ] No unmapped steps added without explicit user confirmation
- [ ] Step count ≤ 20 per scenario (split if needed)
- [ ] Platform tags on every step
- [ ] Format matches existing document style exactly
- [ ] "Features covered" section updated
- [ ] Full diff preview shown to user before any write
- [ ] Waited for explicit Y before writing
