---
name: fetch-requirement
description: >
  **WORKFLOW SKILL** — Fetch a Jira ticket and all linked Confluence pages and Figma URLs to produce a structured raw requirement.
  USE FOR: Phase 1a of analyze-requirement agent.
  INPUT: Jira ticket ID or URL + optional Qase link.
  OUTPUT: temp/raw_requirement.json and temp/business_rules.json written to disk.
  DO NOT USE FOR: searching local specs or domain knowledge (use search-current-system and read-domain-knowledge).
---

# Skill: Fetch Requirement

Extract the complete requirement from a Jira ticket and all its linked external sources. Output feeds every downstream skill in the analyze-requirement workflow.

## Input
- Jira ticket ID or URL.
- Optional Qase link.

## Output
Two files in `temp/` — schemas in `.claude/references/data-bus-schemas.md`:
- `temp/raw_requirement.json`
- `temp/business_rules.json`

## References
- Output schemas → `.claude/references/data-bus-schemas.md`

---

## Fetch policy (no permission required)

| Source | When to fetch | How |
|---|---|---|
| Jira ticket | Always — first action | `mcp_jira_jira_get_ticket` |
| Confluence pages linked in Jira description/AC/comments | Always — mandatory | `mcp_confluence_confluence_get_page` for each link |
| Figma URLs linked in Jira or in fetched Confluence pages | Always — mandatory | Figma MCP tool |
| Qase suite | Only if user provided a Qase link | `mcp_qase_list_cases` |

**Never ask permission** before fetching — these are the requirement definition. Skipping any produces an incomplete spec.

---

## Workflow

### Step 1 — Fetch the Jira ticket
`mcp_jira_jira_get_ticket`. Read:
- Title, description, all Acceptance Criteria (all US and AC sections).
- Linked Confluence page URLs.
- Figma URLs (description, AC, comments).
- Sub-tasks and comments.

Extract immediately:
- **Feature name** (e.g. "Publish and Notify Student").
- **Module** (e.g. `lesson-management`, `event`, `calendar`).
- **Key terms** — field/entity/operation names from the AC.
- **US/AC IDs** preserving exact numbering (US 01, AC 01.1, etc.).
- **All roles** referenced anywhere in the ticket.

### Step 2 — Fetch all linked Confluence pages
For every Confluence URL found in Step 1:
1. `mcp_confluence_confluence_get_page` for full content.
2. Extract business rules, constraints, architecture notes, role/permission rules.
3. Scan fetched pages for additional Figma URLs.

### Step 3 — Fetch all Figma designs
For every Figma URL:
1. Extract field names, labels, placeholders.
2. Field states: editable / locked / auto-calculated / optional / required.
3. Error messages, empty states, loading states, confirmation dialogs.
4. Role-specific UI differences.
5. Cross-reference vs AC: any behavior visible in Figma but absent from any AC → tag `[UNDOCUMENTED IN AC]`.

### Step 4 — Fetch Qase test cases (if link provided)
`mcp_qase_list_cases` on the suite. Note which ACs or feature areas they cover (title-level only, no step details).

### Step 5 — Extract business rules
Consolidate into a structured rules table. For each AC, extract:
- Explicit rule stated in the AC.
- Field behavior: editable / locked / auto-filled / optional / required.
- Role/permission constraints.
- Conditional logic — decompose into separate rules.
- Default values.
- Auto-calculation derivation.
- Conflict handling.

> **Conditional explosion rule:** "Button visible for Draft and Published, hidden for Completed and Cancelled" = **4 separate rules**, not 1. Prevents coverage gaps downstream.

> **Field classification rule:** Every field mentioned MUST be classified as one of: `editable` / `locked` / `auto-calculated` / `optional` / `required`.

### Step 6 — Write outputs
Write both files to `temp/` per the schemas in `.claude/references/data-bus-schemas.md`. Every field listed in the schema must be present; use `null` or `[]` for missing values, never omit keys.

---

## Quality checks
- Jira ticket fetched in full (title, description, all US/AC, comments).
- All Confluence pages linked in ticket fetched.
- All Figma URLs found in ticket and Confluence pages fetched.
- Conditional rules decomposed into separate cases (no combined "if A or B" rules).
- Every field classified with a behavior type.
- All roles extracted and listed.
- All `[UNDOCUMENTED IN AC]` Figma discrepancies recorded.
- Both `temp/raw_requirement.json` and `temp/business_rules.json` written and conform to the data-bus schema.
- Original US/AC numbering preserved.
