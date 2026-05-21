# Analyze-Requirement — Phase 4 Validation + Effectiveness Rules

Reference for the master agent's Phase 4 (Active Validation Loop) and overall analysis quality.

---

## 13-point review checklist

Run by reading `temp/*.json` files. On failure, retry the responsible skill with a specific fix instruction. Max 2 retry rounds per check.

| # | Category | Check | Retry Target |
|---|---|---|---|
| 1 | Completeness | Every AC has at least one extracted business rule | `fetch-requirement` |
| 2 | Completeness | Every role mentioned has defined behavior OR `[ROLE GAP]` finding | `analyze-impact` |
| 3 | Completeness | Every field has a defined state or is flagged | `fetch-requirement` |
| 4 | Completeness | Related Specs + Related Test Cases populated (or explicitly empty with reason) | `search-current-system` |
| 5 | Consistency | No two extracted business rules contradict each other | `formulate-questions` |
| 6 | Consistency | Every `[CONFLICT]` has a corresponding clarification question | `formulate-questions` |
| 7 | Consistency | Every `[LESSON-LEARNED RISK]` has a question or "addressed by AC X.Y" note | `formulate-questions` |
| 8 | Consistency | Spec summary accurately reflects AC content | (self-fix in spec) |
| 9 | Depth | At least one finding per AC (zero findings = suspicious) | `analyze-impact` |
| 10 | Depth | Lesson-learned files were consulted | `check-lesson-learned` |
| 11 | Depth | E2E scenario impact assessed | `analyze-impact` |
| 12 | Depth | Cross-entity dependencies checked via domain `data_relationships` | `analyze-impact` |
| 13 | Anti-Shallow | Every new Business Rule has both positive AND negative flow assertions | `analyze-impact` |

---

## Active retry logic

1. Run the 13-point checklist by reading the relevant `temp/` files.
2. For each failed check:
   a. Identify the retry target skill.
   b. Re-read that skill's `SKILL.md`.
   c. Re-run the skill with a **specific fix instruction** (e.g. "Re-run analyze-impact: AC 03.2 has zero findings — check role coverage for Centre Staff").
   d. The retried skill overwrites its `temp/` output file.
   e. Re-read the updated file and re-check.
3. **Max 2 retry rounds per check.**
4. If still failing after 2 retries → add a clarification question and proceed.
5. After validation completes, update the spec file with any changes from retries.

## Validation report format

```
=== Internal Review ===

Passed: 12/13
Auto-fixed: Check #2 — AC 03.2 Centre Staff role gap added (retry 1)
Still open: Check #13 — AC 01.1 negative assertion for Cancelled status (added as question #7)
```

---

## Analysis effectiveness rules

### Anti-hallucination
1. Never invent business rules — if not in AC/Confluence/Figma/domain knowledge, flag `[MISSING BEHAVIOR]`.
2. Never assume field behavior — if AC says "button shown" but not "clickable" or "disabled", flag it.
3. Never fabricate conflict evidence — requires existing documented rule + contradicting new rule.
4. Never skip files — if the inventory has 5 files, analyze all 5.

### Depth
5. **Conditional explosion** — decompose conditional rules into separate cases.
6. **Cross-platform verification** — for every rule, check SF / BO / Mobile via domain sync rules.
7. **Negative test surface** — for every "when X, do Y" → consider "when NOT X" → flag if AC silent.
8. **Data cascade** — trace downstream entities for any create/modify/delete using domain `data_relationships`.

### Quality gates
9. **Minimum findings threshold** — zero findings across all tags is suspicious → review expert re-examines.
10. **Question quality gate** — every question must be (a) answerable, (b) evidence-backed, (c) understandable without reading spec.
11. **Traceability chain** — business rule → AC ID → Jira ticket; finding → source file; question → finding tag.

### Efficiency
12. Each sub-skill reads from `temp/` files, not chat context — prevents hallucination on long conversations.
13. No redundant fetching — if domain knowledge already documents a rule, reference it.
14. Each sub-skill produces focused output, not raw copy.

---

## Error handling

- **Jira fetch fails** → stop and report. Do not proceed without the ticket.
- **Confluence/Figma fetch fails** → log warning, continue with available data. Note missing source in spec assumptions.
- **No local matches (search-current-system)** → proceed. This is a genuinely new feature area. Note in spec: "No existing specs or test cases found."
- **No lesson-learned matches** → proceed. Note in assessment: "No relevant historical incidents found."
- **Phase 4 retry exhausted** → add clarification question and proceed. Never loop infinitely.
