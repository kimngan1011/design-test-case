---
name: check-lesson-learned
description: >
  **WORKFLOW SKILL** — Read lesson-learned files and identify which past production incidents are relevant to a new requirement being analyzed.
  USE FOR: Phase 2a of analyze-requirement agent — runs before analyze-impact.
  INPUT: temp/business_rules.json + temp/raw_requirement.json (already on disk).
  OUTPUT: temp/lesson_learned_assessment.json written to disk.
  DO NOT USE FOR: general incident documentation (use save-slack-issue for that).
---

# Skill: Check Lesson Learned

You are cross-referencing past production incidents against a new requirement to surface hidden risks. Your output feeds directly into `analyze-impact` and `formulate-questions`.

---

## Input

Read from disk (do not rely on chat context):
- `temp/business_rules.json` — the extracted business rules for the new requirement
- `temp/raw_requirement.json` — keywords, module, roles, feature name

---

## Workflow

### Step 1 — Read all lesson-learned files

Read the following files in full:
- `input/domain-knowledge/scheduling/lesson-learned/core.md`
- `input/domain-knowledge/scheduling/lesson-learned/oop.md`

If the module is not `scheduling`, search `input/domain-knowledge/` for any `lesson-learned/` subdirectory and read all `.md` files found.

### Step 2 — Match incidents to the new requirement

For each lesson-learned entry, evaluate relevance using a **two-factor test**:

**Factor 1 — Entity overlap:** Does the incident involve the same entity or entities as the new requirement?
- Look for entity names from `temp/raw_requirement.json` keywords: e.g., "student session", "lesson", "lesson allocation", "notification"

**Factor 2 — Operation overlap:** Does the incident involve the same type of operation?
- Operations: assign, unassign, import, sync, publish, create, delete, bulk assign, auto-assign, export, deduct, calculate

> **Both factors must match for relevance.** "Student session" alone (Factor 1 only) is too broad. "Student session + bulk assign" (both factors) is specific enough.

> **Never fabricate relevance.** If the lesson-learned entry is about payment processing and the requirement is about calendar UI, do NOT force a connection. Explicitly state there is no match.

### Step 3 — Assess impact on the new requirement

For each relevant incident:

1. **Root cause analysis:** What was the underlying design flaw?
2. **Pattern recognition:** Does the new requirement introduce the same design pattern that caused the incident?
   - Example: "The Aso incident was caused by TWO independent flows that both created student sessions. AC 02.1 of this new requirement introduces a second notification trigger alongside the existing publish flow — same dual-path pattern."
3. **Specific risk statement:** What exactly could go wrong? Be concrete.
   - GOOD: "AC 02.1 introduces a new notification path. If the existing publish flow already triggers a notification in some partner configurations, this creates a dual-trigger pattern similar to the 2026-04-07 Aso incident (1,655 duplicates)."
   - BAD: "This could cause similar issues."
4. **Guardrail recommendation:** What specific thing should be verified or asked about?

### Step 4 — Write output

Write `temp/lesson_learned_assessment.json`:

```json
{
  "ticket_id": "LT-XXXXX",
  "assessment_date": "2026-04-14",
  "incidents_checked": 3,
  "relevant_incidents": [
    {
      "incident_title": "Aso — Duplicate Student Sessions from Manual Assign + Auto Assign",
      "incident_date": "2026-04-13",
      "source_file": "input/domain-knowledge/scheduling/lesson-learned/core.md",
      "entity_overlap": ["student session"],
      "operation_overlap": ["assign", "auto-assign"],
      "relevance_reason": "New requirement adds a second notification trigger (publish action) alongside an existing trigger (lesson status change). Same dual-path pattern that caused 1,655 duplicate sessions in Aso incident.",
      "risk_statement": "If the existing lesson publish flow already sends a notification for some partners, AC 02.1's new 'Publish & Notify' button creates a second trigger — potentially sending duplicate notifications to students.",
      "guardrail_recommendation": "Verify: does the existing Draft→Published status change trigger any notification? If yes, deduplication logic is required to prevent double-sending.",
      "tag": "[LESSON-LEARNED RISK]"
    }
  ],
  "no_match_incidents": [
    {
      "incident_title": "Nichibei — Student Sessions Missing LA → Points Not Deducted",
      "reason_not_relevant": "This incident involves OOP-specific SPO sync flow. New requirement is about push notifications for Core/Renseikai — different entity (points vs notifications) and different operation."
    }
  ],
  "summary": "1 relevant incident found. Risk: dual-trigger notification pattern may cause duplicate push notifications."
}
```

If no incidents are relevant:
```json
{
  "relevant_incidents": [],
  "summary": "No relevant historical incidents found. All lesson-learned entries checked — none match the entity+operation combination of this requirement."
}
```

---

## Quality Checks

- [ ] Read ALL lesson-learned files (core.md + oop.md + any others in the domain)
- [ ] Applied two-factor test (entity + operation) for every incident
- [ ] No fabricated relevance — unrelated incidents explicitly noted as non-matching
- [ ] Risk statements are concrete and specific (not vague warnings)
- [ ] Guardrail recommendations are actionable
- [ ] If no matches: explicitly states "No relevant historical incidents found"
- [ ] Output written to `temp/lesson_learned_assessment.json`
