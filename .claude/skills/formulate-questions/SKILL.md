---
name: formulate-questions
description: >
  **WORKFLOW SKILL** — Convert impact findings into precise, evidence-backed clarification questions for product managers or developers.
  USE FOR: Phase 3a of analyze-requirement agent — runs after analyze-impact.
  INPUT: temp/impact_findings.json + temp/lesson_learned_assessment.json + temp/raw_requirement.json (already on disk).
  OUTPUT: temp/clarification_questions.json written to disk.
  DO NOT USE FOR: performing the analysis (use analyze-impact) or posting to Jira (that is done by the master agent in Phase 5).
---

# Skill: Formulate Questions

You are converting the raw findings from impact analysis into precise, actionable clarification questions. Every question must be answerable and evidence-backed.

---

## Input

Read from disk (do not rely on chat context):
- `temp/impact_findings.json` — findings with tags, sources, AC refs
- `temp/lesson_learned_assessment.json` — relevant incidents and guardrail recommendations
- `temp/raw_requirement.json` — AC list for grouping

---

## Workflow

### Step 1 — Map findings to questions

For each finding in `temp/impact_findings.json` with a tag that requires clarification:
- `[CONFLICT]` → always generates a question
- `[LESSON-LEARNED RISK]` → always generates a question
- `[REGRESSION RISK]` → generates a question
- `[UNDOCUMENTED IN AC]` → generates a question
- `[MISSING BEHAVIOR]` → generates a question
- `[ROLE GAP]` → generates a question
- `[EXTENDED]` → does NOT generate a question (no ambiguity)
- `[REPLACED]` → does NOT generate a question (replacement is clear)

### Step 2 — Apply question quality gate

Every question MUST pass all three criteria:

1. **Answerable:** The question must have a specific, deterministic answer (yes/no, a value, a behavior choice). NOT: "Is this correct?" YES: "When lesson status is Published, should the Publish & Notify button be visible or hidden? AC 01.1 covers Draft only."

2. **Evidence-backed:** Every question MUST include an Evidence line that cites the exact source creating the ambiguity. Evidence format:
   > _Evidence: `<source file or AC ID>` — `<what it says that creates the gap>`_

3. **Self-contained:** A PM must understand the question without reading the spec file. Include enough context in the question text itself.

### Step 3 — Apply AC-level limits

- Maximum **2 questions per AC** unless there are genuinely distinct issues
- If an AC has 3+ issues, prioritize: `[CONFLICT]` and `[LESSON-LEARNED RISK]` first, then `[REGRESSION RISK]`, then gaps
- Combine related `[MISSING BEHAVIOR]` findings under one question when they all concern the same field

### Step 4 — Priority ordering

Order questions by priority:
1. `[CONFLICT]` — must resolve before implementation
2. `[LESSON-LEARNED RISK]` — production safety concerns
3. `[REGRESSION RISK]` — existing test breakage
4. `[UNDOCUMENTED IN AC]` — Figma behaviors not in spec
5. `[MISSING BEHAVIOR]` — undefined edge cases
6. `[ROLE GAP]` — undefined role behaviors

Within same priority, group by AC ID.

### Step 5 — Write output

Write `temp/clarification_questions.json`:

```json
{
  "ticket_id": "LT-XXXXX",
  "total_questions": 5,
  "questions": [
    {
      "id": 1,
      "tag": "[CONFLICT]",
      "ac_ref": "AC 01.1",
      "priority": 1,
      "question": "AC 01.1 states the Publish & Notify button is visible when lesson status is Draft. The existing spec (LT-96662) additionally states it is visible when status is Published. Which is correct — visible for Draft only, or visible for both Draft and Published?",
      "evidence": "input/specs/LT-96662 Renseikai.../spec.md, Business Rule #2: Button visible for Published status"
    },
    {
      "id": 2,
      "tag": "[LESSON-LEARNED RISK]",
      "ac_ref": "AC 02.1",
      "priority": 2,
      "question": "Based on the 2026-04-13 Aso incident (duplicate records from dual assignment paths), AC 02.1 introduces a new notification trigger via button click. Does the existing lesson publish flow (Draft→Published status change) already send any push notification in any configuration? If yes, deduplication logic is required.",
      "evidence": "input/domain-knowledge/scheduling/lesson-learned/core.md, 2026-04-13 — dual-path assignment causing duplicate records"
    },
    {
      "id": 3,
      "tag": "[MISSING BEHAVIOR]",
      "ac_ref": "AC 01.1",
      "priority": 5,
      "question": "AC 01.1 defines button visibility for Draft status only. What is the button's behavior when lesson status is Completed or Cancelled? Should it be hidden, disabled, or shown with a different label?",
      "evidence": "temp/business_rules.json, Rule #1 — covers Draft only; Completed and Cancelled statuses have no defined button behavior"
    },
    {
      "id": 4,
      "tag": "[ROLE GAP]",
      "ac_ref": null,
      "priority": 6,
      "question": "Centre Staff role appears in domain knowledge for lesson management operations, but no AC defines whether Centre Staff can see or click the Publish & Notify button. Should Centre Staff have access to this button?",
      "evidence": "input/domain-knowledge/scheduling/scheduling-domain-knowledge.md — Centre Staff listed as lesson management role; no AC mentions this role"
    }
  ]
}
```

---

## Question format reference

### For [CONFLICT]:
> "AC X.Y states [new rule]. The existing [spec/test] states [old rule] for the same [field/flow]. Which behavior should apply?"

### For [LESSON-LEARNED RISK]:
> "Based on the [date] [incident title], [specific risk in this requirement]. Has this been addressed in the current design? If not, what deduplication/prevention mechanism is planned?"

### For [MISSING BEHAVIOR]:
> "AC X.Y defines behavior for [covered cases]. What should happen when [uncovered case]? Should it [option A] or [option B]?"

### For [ROLE GAP]:
> "[Role] interacts with [feature area] according to [domain knowledge/existing spec], but no AC defines their behavior for [specific operation]. Should [role] have [access/restriction]?"

### For [UNDOCUMENTED IN AC]:
> "The Figma design (node #XXXX) shows [behavior]. No AC currently covers this. Should this behavior be included in the implementation?"

---

## Quality Checks

- [ ] Read `temp/impact_findings.json` and `temp/lesson_learned_assessment.json` from disk
- [ ] Only `[CONFLICT]`, `[LESSON-LEARNED RISK]`, `[REGRESSION RISK]`, `[UNDOCUMENTED IN AC]`, `[MISSING BEHAVIOR]`, `[ROLE GAP]` generate questions
- [ ] Every question passes the 3-criteria quality gate (answerable, evidence-backed, self-contained)
- [ ] Maximum 2 questions per AC (exceptions allowed for genuinely distinct issues)
- [ ] Questions ordered by priority (1=highest)
- [ ] All `[LESSON-LEARNED RISK]` questions reference incident date and title
- [ ] Evidence line present on every question
- [ ] Output written to `temp/clarification_questions.json`
