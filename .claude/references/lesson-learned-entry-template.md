# Lesson-Learned Entry Template

Used by `save-slack-issue` Step 3 to append a structured entry to the team's lesson-learned file.

---

## File destination
- Core (affects all partners): `knowledge/domain-knowledge/<team>/lesson-learned/core.md`
- OOP (partner-specific): `knowledge/domain-knowledge/<team>/lesson-learned/oop.md`

## Headers for new files

If the destination file does not exist, create it with the matching header:

**core.md:**
```markdown
# Lesson Learned — Core Domain Issues

---
```

**oop.md:**
```markdown
# Lesson Learned — OOP / Partner-Specific Issues

---
```

## Entry template (append, never overwrite)

```markdown
## [YYYY-MM-DD] <Partner> — <Issue Title>

**Slack thread:** <original Slack URL>

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

## Rules
- Write in **English**.
- Be specific — include numbers, field names, feature names.
- Omit the **Data** section if no metrics are available.
- Keep "Lessons Learned" forward-looking and actionable (not a repeat of root cause).
