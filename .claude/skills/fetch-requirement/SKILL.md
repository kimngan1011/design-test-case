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

You are extracting the complete requirement from a Jira ticket and all its linked external sources. Your output feeds every downstream skill in the analyze-requirement workflow.

---

## Fetch Policy (no permission required)

| Source | When to fetch | How |
|--------|--------------|-----|
| **Jira ticket** | Always — first action | `mcp_jira_jira_get_ticket` |
| **Confluence pages** linked in Jira description/AC/comments | Always — mandatory | `mcp_confluence_confluence_get_page` for each link found |
| **Figma URLs** linked in Jira or in fetched Confluence pages | Always — mandatory | Figma MCP tool |
| **Qase suite** | Only if user provided a Qase link | `mcp_qase_list_cases` |

**Never ask permission** before fetching these sources. They are the requirement definition — skipping any of them produces an incomplete spec.

---

## Workflow

### Step 1 — Fetch the Jira ticket

Use `mcp_jira_jira_get_ticket`. Read:
- Title, description, all Acceptance Criteria (all US and AC sections)
- Linked Confluence page URLs
- Figma URLs (in description, AC, comments)
- Sub-tasks and comments

Extract immediately:
- **Feature name** — short name for the feature (e.g., "Publish and Notify Student")
- **Module** — which domain this belongs to (e.g., `lesson-management`, `event`, `calendar`)
- **Key terms** — field names, entity names, operation names from the AC
- **US/AC IDs** — preserve exact numbering (US 01, AC 01.1, etc.)
- **All roles mentioned** — every user role referenced anywhere in the ticket

### Step 2 — Fetch all linked Confluence pages

For every Confluence URL found in Step 1:
1. Fetch the full page content using `mcp_confluence_confluence_get_page`
2. Extract: business rules, constraints, architecture notes, role/permission rules
3. Scan fetched pages for additional Figma URLs not found in Jira

### Step 3 — Fetch all Figma designs

For every Figma URL found in Jira or Confluence pages:
1. Extract from the design:
   - Field names, labels, placeholders
   - Field states: editable / locked / auto-calculated / optional / required
   - Error messages, empty states, loading states, confirmation dialogs
   - Role-specific UI differences (different views per role)
2. Cross-reference Figma against the AC:
   - Any behavior visible in Figma but absent from any AC → tag `[UNDOCUMENTED IN AC]`

### Step 4 — Fetch Qase test cases (if link provided)

If the user provided a Qase link:
1. Fetch test case titles from the linked suite using `mcp_qase_list_cases`
2. Note which ACs or feature areas they cover (title-level only, no step details)

### Step 5 — Extract business rules

Consolidate all information into a structured business rules table. For each AC, extract:

- The **explicit rule** stated in the AC
- **Field behavior**: editable / locked / auto-filled / optional / required
- **Role/permission constraints**: which roles can see/do this
- **Conditional logic**: if X then Y, else Z (decompose into separate rules)
- **Default values**: what value is pre-populated
- **Auto-calculation**: how a value is derived
- **Conflict handling**: what happens when two conditions clash

> **Conditional explosion rule:** Every business rule with conditions MUST be decomposed into separate cases.
> Example: "Button visible for Draft and Published, hidden for Completed and Cancelled" = **4 separate rules**, not 1.
> This prevents coverage gaps in downstream test case generation.

> **Field classification rule:** Every field mentioned MUST be classified as one of:
> `editable` / `locked` / `auto-calculated` / `optional` / `required`

---

## Output

Write two files to `temp/`:

### `temp/raw_requirement.json`

```json
{
  "ticket_id": "LT-XXXXX",
  "ticket_url": "https://manabie.atlassian.net/browse/LT-XXXXX",
  "feature_name": "Publish and Notify Student",
  "module": "lesson-management",
  "keywords": ["publish lesson", "push notification", "notify student", "draft", "published"],
  "roles": ["Centre Manager", "HQ Admin", "Student", "Parent Contact"],
  "user_stories": [
    {
      "id": "US 01",
      "title": "Button UI",
      "acceptance_criteria": [
        {"id": "AC 01.1", "text": "Button visible when lesson status is Draft"},
        {"id": "AC 01.2", "text": "Button visible when lesson status is Published"}
      ]
    }
  ],
  "figma_discrepancies": [
    {
      "tag": "[UNDOCUMENTED IN AC]",
      "figma_node": "#1234",
      "description": "Confirmation modal shown before sending — no AC covers this"
    }
  ],
  "qase_coverage": [
    {"suite": "Lesson / Publish", "title": "Verify publish button visible for Draft lesson"}
  ]
}
```

### `temp/business_rules.json`

```json
{
  "ticket_id": "LT-XXXXX",
  "rules": [
    {
      "id": 1,
      "ac_ref": "AC 01.1",
      "rule": "Publish & Notify button is visible when lesson status = Draft",
      "field": "Publish & Notify button",
      "field_behavior": "visible",
      "role_constraint": "All roles with lesson edit access",
      "conditional_logic": "status = Draft",
      "default_value": null,
      "platform": ["SF"]
    },
    {
      "id": 2,
      "ac_ref": "AC 01.2",
      "rule": "Publish & Notify button is visible when lesson status = Published",
      "field": "Publish & Notify button",
      "field_behavior": "visible",
      "role_constraint": "All roles with lesson edit access",
      "conditional_logic": "status = Published",
      "default_value": null,
      "platform": ["SF"]
    },
    {
      "id": 3,
      "ac_ref": "AC 01.1",
      "rule": "Publish & Notify button is HIDDEN when lesson status = Completed",
      "field": "Publish & Notify button",
      "field_behavior": "hidden",
      "role_constraint": null,
      "conditional_logic": "status = Completed",
      "default_value": null,
      "platform": ["SF"]
    }
  ]
}
```

---

## Quality Checks

- [ ] Jira ticket fetched in full (title, description, all US/AC, comments)
- [ ] All Confluence pages linked in ticket fetched
- [ ] All Figma URLs found in ticket and Confluence pages fetched
- [ ] Conditional rules decomposed into separate cases (no combined "if A or B" rules)
- [ ] Every field classified with a behavior type
- [ ] All roles extracted and listed in `raw_requirement.json`
- [ ] All `[UNDOCUMENTED IN AC]` Figma discrepancies recorded
- [ ] Both `temp/raw_requirement.json` and `temp/business_rules.json` written
- [ ] Original US/AC numbering preserved
