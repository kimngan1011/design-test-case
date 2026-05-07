---
name: save-slack-issue
description: >
  **WORKFLOW SKILL** — Read a Slack thread about a production issue and save a structured
  lesson-learned entry to the correct domain knowledge file.
  USE FOR: documenting post-mortems, production incidents, partner-specific bugs, or data-fix
  events discovered in Slack threads. Keeps institutional knowledge searchable and actionable.
  INPUT: Slack thread URL + team name (e.g. scheduling, payment, lesson) + type (core or oop).
  OUTPUT: a structured entry appended to input/domain-knowledge/<team>/lesson-learned/core.md
  or oop.md.
  DO NOT USE FOR: verifying bugs (use verify-bug skill); generating test cases (use
  generate-test-cases skill); analyzing Jira tickets (use analyze-requirements skill).
argument-hint: "<slack-thread-url> <team> <core|oop>"
---

# Skill: Save Slack Issue to Lesson Learned

You are a senior QA/engineering analyst. Your job is to read a Slack thread about a
production issue and save a structured entry into the correct lesson-learned file.

---

## Reference Files

Before writing the entry, be aware of the domain knowledge structure:

- `input/domain-knowledge/<team>/lesson-learned/core.md` — issues affecting all partners
- `input/domain-knowledge/<team>/lesson-learned/oop.md` — partner-specific / OOP issues
- `input/domain-knowledge/scheduling/` — example of an existing team folder

---

## Inputs

Parse from the user's message:

1. **Slack thread URL** — e.g. `https://manabie.slack.com/archives/C037409QQ4S/p1775610509175129`
2. **Team** — folder name under `input/domain-knowledge/` (e.g. `scheduling`, `payment`, `lesson`)
3. **Type** — `core` (issue affects all partners) or `oop` (partner-specific / OOP feature)

**If any are missing, ask for all missing fields in a single prompt before proceeding.**

---

## File Destination

- Core: `input/domain-knowledge/<team>/lesson-learned/core.md`
- OOP: `input/domain-knowledge/<team>/lesson-learned/oop.md`

If the destination file does not exist, create it with the appropriate header:

**core.md header:**

```markdown
# Lesson Learned — Core Domain Issues

---
```

**oop.md header:**

```markdown
# Lesson Learned — OOP / Partner-Specific Issues

---
```

---

## Workflow

### Step 1 — Fetch the Slack Thread

Parse the URL to extract:

- `channel_id` — segment after `/archives/` and before `/p...`
- `timestamp` — the `p` number with `.` inserted before last 6 digits
  (e.g. `p1775610509175129` → `1775610509.175129`)

Read the Slack token from `.vscode/mcp.json`:

- Primary: field `SLACK_MCP_XOXB_TOKEN` (bot token)
- Fallback: field `SLACK_USER_TOKEN` (xoxp user token) if bot returns `not_in_channel`

```bash
curl -s "https://slack.com/api/conversations.replies?channel=<channel_id>&ts=<timestamp>&limit=50" \
  -H "Authorization: Bearer <token>"
```

If both tokens fail, report the error to the user and stop.

---

### Step 2 — Analyze the Thread

Extract the following from the thread messages:

| Field               | Source                                               |
| ------------------- | ---------------------------------------------------- |
| **Date reported**   | First message `ts` field → YYYY-MM-DD                |
| **Partner name**    | Customer/partner mentioned (e.g. Aso, Nichibei, KEC) |
| **Issue title**     | Concise summary of what went wrong                   |
| **Root cause**      | Technical reason — be accurate, do not assume        |
| **Data/metrics**    | Numbers of records affected, if any                  |
| **Resolution**      | What was done: data fix and/or code fix              |
| **Lessons learned** | Forward-looking, actionable design/code improvements |

Synthesize scattered messages into a coherent narrative. Be concise — avoid over-explaining.

---

### Step 3 — Write the Entry

Append to the destination file (never overwrite existing content):

```markdown
## [YYYY-MM-DD] <Partner> — <Issue Title>

**Slack thread:** <original slack URL>

### Issue

<1-2 sentences: what happened from user/system perspective>

**Root cause:**
<Technical explanation. Numbered list if multiple causes.>

**Data:**

- <metric 1>
- <metric 2>

### Resolution

- <What was done to fix — data recovery and/or code fix>

### Lessons Learned / Design Notes

- <Actionable design/code improvement>

---
```

**Rules:**

- Write in **English**
- Be specific — include numbers, field names, feature names
- Omit the **Data** section if no metrics are available
- Keep "Lessons Learned" forward-looking and actionable

---

### Step 4 — Confirm

Report to the user:

- Which file was updated (full path)
- The entry title added
- One-line summary of the issue

---

## Quality Checks

- [ ] All three inputs provided (Slack URL, team, type) before proceeding
- [ ] Slack thread fetched — use user token
- [ ] Date extracted from first message timestamp
- [ ] Root cause is technical and specific — not vague ("unknown issue")
- [ ] Entry appended, not overwritten
- [ ] Destination file created with correct header if it did not exist
- [ ] Data section omitted when no metrics are available
- [ ] Lessons Learned section is actionable (not a repeat of root cause)
- [ ] Confirmed to user: file path + entry title + one-line summary

---

## Example Invocations

### Full input in one message

> User: `/save-slack-issue` https://manabie.slack.com/archives/C037409QQ4S/p1775610509175129 scheduling core

The skill fetches the thread, extracts the incident, appends to
`input/domain-knowledge/scheduling/lesson-learned/core.md`, and confirms.

### Partner-specific (OOP) issue

> User: `/save-slack-issue` https://manabie.slack.com/archives/CABC123/p1234567890123456 payment oop

Appends to `input/domain-knowledge/payment/lesson-learned/oop.md`.

### Missing fields — skill asks before proceeding

> User: `/save-slack-issue` https://manabie.slack.com/archives/CABC123/p1234567890123456
>
> Skill: "I need two more pieces of information before I can save this:
>
> 1. **Team** — which domain? (e.g. scheduling, payment, lesson)
> 2. **Type** — `core` (affects all partners) or `oop` (partner-specific)?"
>
> User: scheduling, core
>
> _(skill proceeds with fetch and save)_
