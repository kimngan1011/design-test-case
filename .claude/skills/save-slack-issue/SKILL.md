---
name: save-slack-issue
description: >
  **WORKFLOW SKILL** — Read a Slack thread about a production issue and save a structured
  lesson-learned entry to the correct domain knowledge file.
  USE FOR: documenting post-mortems, production incidents, partner-specific bugs, or data-fix
  events discovered in Slack threads. Keeps institutional knowledge searchable and actionable.
  INPUT: Slack thread URL + team name (e.g. scheduling, payment, lesson) + type (core or oop).
  OUTPUT: a structured entry appended to knowledge/domain-knowledge/<team>/lesson-learned/core.md
  or oop.md.
  DO NOT USE FOR: verifying bugs (use verify-bug skill); generating test cases (use
  generate-test-cases skill); analyzing Jira tickets (use analyze-requirements skill).
argument-hint: "<slack-thread-url> <team> <core|oop>"
---

# Skill: Save Slack Issue to Lesson Learned

Senior QA/engineering analyst. Read a Slack thread about a production issue, synthesize the incident, append a structured entry to the team's lesson-learned file.

## Input
1. Slack thread URL — e.g. `https://manabie.slack.com/archives/C037409QQ4S/p1775610509175129`.
2. Team — folder name under `knowledge/domain-knowledge/` (e.g. `scheduling`, `payment`, `lesson`).
3. Type — `core` (issue affects all partners) or `oop` (partner-specific).

If any are missing, ask for ALL missing fields in ONE prompt before proceeding.

## References
- Entry template, headers, file destinations, writing rules → `.claude/references/lesson-learned-entry-template.md`

---

## Workflow

### Step 1 — Fetch the Slack thread
Parse the URL:
- `channel_id` = segment after `/archives/` and before `/p...`.
- `timestamp` = the `p` number with `.` inserted before the last 6 digits (e.g. `p1775610509175129` → `1775610509.175129`).

Read the Slack token from `.vscode/mcp.json`:
- Primary: `SLACK_MCP_XOXB_TOKEN` (bot token).
- Fallback: `SLACK_USER_TOKEN` (xoxp user token) if bot returns `not_in_channel`.

```bash
curl -s "https://slack.com/api/conversations.replies?channel=<channel_id>&ts=<timestamp>&limit=50" \
  -H "Authorization: Bearer <token>"
```

If both tokens fail, report the error and stop.

### Step 2 — Analyze the thread
Extract:

| Field | Source |
|---|---|
| Date reported | First message `ts` field → YYYY-MM-DD |
| Partner name | Customer/partner mentioned (Aso, Nichibei, KEC, …) |
| Issue title | Concise summary of what went wrong |
| Root cause | Technical reason — be accurate, do not assume |
| Data/metrics | Numbers of records affected, if any |
| Resolution | What was done: data fix and/or code fix |
| Lessons learned | Forward-looking, actionable design/code improvements |

Synthesize scattered messages into a coherent narrative. Be concise.

### Step 3 — Write the entry
Append to the destination file using the template in `.claude/references/lesson-learned-entry-template.md`. NEVER overwrite — always append.

If the destination file does not exist, create it with the appropriate header (from the reference).

### Step 4 — Confirm
Report to the user:
- File path that was updated.
- Entry title added.
- One-line summary of the issue.

---

## Quality checks
- All three inputs provided (URL, team, type) before proceeding.
- Slack thread fetched.
- Date extracted from first message timestamp.
- Root cause is technical and specific — not vague ("unknown issue").
- Entry appended, not overwritten.
- Destination file created with correct header if it did not exist.
- Data section omitted when no metrics are available.
- Lessons Learned section is actionable (not a repeat of root cause).
- Confirmed to user with file path + entry title + one-line summary.

## Example
```
/save-slack-issue https://manabie.slack.com/archives/C037409QQ4S/p1775610509175129 scheduling core
```
Fetches the thread, extracts the incident, appends to `knowledge/domain-knowledge/scheduling/lesson-learned/core.md`, confirms.

If team/type missing:
> "I need two more pieces of information before I can save this:
> 1. **Team** — which domain? (e.g. scheduling, payment, lesson)
> 2. **Type** — `core` (affects all partners) or `oop` (partner-specific)?"
