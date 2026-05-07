---
name: update-domain-knowledge
description: >
  **WORKFLOW SKILL** — Update the domain knowledge file with confirmed new business rules from an analyzed requirement.
  USE FOR: Phase 6a of analyze-requirement agent — runs after user approves questions posted to Jira.
  INPUT: temp/impact_findings.json + temp/business_rules.json (already on disk).
  OUTPUT: Updated input/domain-knowledge/<domain>/<domain>-domain-knowledge.md (after user approval).
  DO NOT USE FOR: documenting production incidents (use save-slack-issue for that).
---

# Skill: Update Domain Knowledge

You are adding confirmed new business rules to the domain knowledge file so future analyses of related tickets will have accurate context. This is a write operation — never auto-update without user approval.

---

## Input

Read from disk (do not rely on chat context):
- `temp/impact_findings.json` — to identify rules tagged `[EXTENDED]` or `[REPLACED]`
- `temp/business_rules.json` — full content of new business rules

---

## Workflow

### Step 1 — Identify update candidates

From `temp/impact_findings.json`, filter rules that should be added to domain knowledge:

| Finding tag | Action |
|-------------|--------|
| `[EXTENDED]` | Add as new sub-rule to existing section |
| `[REPLACED]` | Mark old rule as superseded + add new rule |
| `[CONFLICT]` with confirmed resolution | Add the winning rule, mark the losing rule as superseded |
| `[CONFLICT]` unresolved | Skip — do not add until resolved |
| `[MISSING BEHAVIOR]` confirmed by PM | Add as new rule |

> Rules tagged `[MISSING BEHAVIOR]` that were NOT clarified → do not add (still ambiguous).

### Step 2 — Locate the correct section

Read `input/domain-knowledge/<domain>/<domain>-domain-knowledge.md` to find where each rule belongs:
- Match entity name (e.g., "Lesson", "Student Session", "Notification")
- Match operation type (e.g., "CRUD Operations", "Status Transitions", "Platform Behaviors")
- If no section matches: propose a new sub-section under the closest parent

### Step 3 — Draft proposed changes

For each update candidate, draft the proposed addition:

**For `[EXTENDED]` rules:**
```markdown
#### [EXISTING SUBSECTION NAME]
... existing content ...
- **[NEW RULE]**: [Rule description]. Added from LT-XXXXX ([date]).
```

**For `[REPLACED]` rules:**
```markdown
- ~~**[OLD RULE]**: [Old description].~~ _(Superseded by LT-XXXXX — see below)_
- **[NEW RULE]**: [New rule description]. Replaces previous rule as of LT-XXXXX ([date]).
```

### Step 4 — Present diff to user

Before writing any changes, present the full proposed diff:

```
=== DOMAIN KNOWLEDGE UPDATE PREVIEW ===

File: input/domain-knowledge/scheduling/scheduling-domain-knowledge.md

Section: 2.1 Lesson → Status Transitions
PROPOSED ADDITIONS:
+ - **Publish & Notify path**: When "Publish & Notify" button is clicked on a Draft lesson,
+   lesson status changes to Published AND push notification is sent to assigned students
+   and their parent contacts. Added from LT-XXXXX (2026-04-14).

Section: 2.3 Notification System
PROPOSED ADDITIONS:
+ #### Lesson Publish Notifications (Renseikai-specific, feature flag: publish_notify_student)
+ - Triggered by "Publish & Notify" button click on SF Lesson Detail
+ - Recipients: assigned students + all related parent contacts (Relationship-linked)
+ - Retry: up to 3 attempts, idempotent delivery
+ Added from LT-XXXXX (2026-04-14).

Apply these changes? (Y/N)
```

### Step 5 — Apply approved changes

Only write to the file after user explicitly confirms Y.

If user says N → log "Domain knowledge update declined by user" and proceed to next phase.

If user modifies the proposed text → incorporate their edits before writing.

---

## Safety Rules

- **NEVER auto-update** — always present diff and wait for explicit Y
- **Only add confirmed rules** — no speculative rules, no "probably" behaviors
- **Never remove existing rules** — only mark as superseded (strikethrough + note)
- **Always include source reference** — every addition must cite the ticket ID and date
- **Maintain existing document style** — match heading levels, list format, table format of surrounding content

---

## Quality Checks

- [ ] Read temp/impact_findings.json and temp/business_rules.json from disk
- [ ] Only `[EXTENDED]`, `[REPLACED]`, and confirmed `[MISSING BEHAVIOR]` rules are update candidates
- [ ] Correct section identified by reading the full domain knowledge file
- [ ] Full diff presented to user before any write
- [ ] Waited for explicit Y before writing
- [ ] Every addition cites ticket ID and date
- [ ] Existing rules not deleted — only marked as superseded if `[REPLACED]`
- [ ] Document style preserved (headings, lists, tables)
