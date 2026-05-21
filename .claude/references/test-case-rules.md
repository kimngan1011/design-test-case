# Test Case Design Rules

Standard rules for designing test cases. The `generate-test-cases` skill MUST apply these throughout.

---

## 1. One test case = one logical validation
Each test case validates ONE business rule, system behavior, or validation logic. Do not combine multiple logics or conditions.

## 2. Avoid vague titles
**Forbidden words in titles:** Verify, Check, Test, Properly, Correctly, Successfully.

Bad → `Page A – Verify display correctly`
Good → `Feature X – Page A – All components rendered`

## 3. Avoid UI-only test cases
Each TC must represent a user scenario, system behavior, or business rule — not isolated UI element existence.

Bad → `Verify header title displayed`, `Verify field A displayed`
Good → `Registration Form – All fields and labels displayed as design`

## 4. Avoid over-combination
Different logics → different TCs.

Bad → `Verify assignment access`
Good →
- `Student can view assignment details`
- `Teacher can edit assignment details`
- `Parent can view assignment status`

## 5. Core vs OOP naming
- Core test cases → **no prefix**.
- OOP/tenant-specific → **prefix with `[TenantName]`** (e.g. `[Renseikai]`, `[Nichibei]`).

Example:
- Core: `Lesson Schedule – Create Lesson – Successfully created`
- OOP: `[Renseikai] Lesson Schedule – Create Lesson – Successfully created`

## 6. Title format
```
[Feature] – [Sub-feature] – [Component] – Condition – Expected Behavior
```

Examples:
- `Extend Recurrence Form – Date Field – End Date + 7 Days – Auto-calculated and non-editable`
- `Dynamic Form – Header Title – Exceeds 60 characters – Validation message shown`

The title must describe the observable outcome, not the action.

## 7. Human-readable language
- Plain language for non-technical readers (PMs, business stakeholders, new joiners).
- No jargon, internal code names, API/endpoint names, DB column names, CSS selectors, or implementation details.
- Describe user-visible actions/outcomes: ✅ "Click the **Save** button", "The **End Date** field shows `2026-03-17`". ❌ "POST /lessons returns 200".
- Short, simple sentences. Spell out acronyms on first use unless they are common business terms.

## 8. Actor rule (CRITICAL)
- **Default actor is `HQ or CM Staff`.** Never use "Admin" as default.
- Only use "Admin" if the test explicitly requires admin-only access AND the ticket calls it out.
- ✅ `Logged in as HQ or CM Staff to the Salesforce org`
- ✅ `Logged in as HQ Staff to the Back Office`
- ❌ `Logged in as Admin to the Renseikai Salesforce org` (unless Admin role is explicit)

## 9. Required fields per test case
Every TC MUST have all of:
- **Title** (per §6)
- **Description** — AC ID (e.g. `AC 01.2`) + technique used (e.g. `BVA`, `Decision Table`) + one-sentence summary.
- **Preconditions** — bulleted state requirements with explicit test data values and actor role.
- **Step actions** — numbered, atomic, present tense ("Open…", "Click…", "Enter…"). Include exact value entered.
- **Step results** — deterministic ("Date field shows 2026-03-17", not "Date field is correct"). One per step.
- **Steps data** — one entry per step (can be `""` if N/A). For BVA: exact boundary value. For Decision Table: combination tested.
- **Severity** — see mapping below.
- **Priority** — see mapping below.

## 10. Severity & priority mapping

| Risk Level | Severity | Priority |
|---|---|---|
| Critical | `critical` | `high` |
| High | `major` | `high` |
| Medium | `minor` | `medium` |
| Low | `trivial` | `low` |

`normal` is NOT a valid Qase severity slug.

## 11. Test Data Anchoring Rule (mandatory for date/time/config-driven TCs)
Whenever the expected result depends on a date, time, deadline, or partner config value, **Step 1's Test Data MUST declare base values explicitly**; later steps derive calculations from those values.

**Step 1 format:**
```
today = YYYY-MM-DD; <other_date_var> = YYYY-MM-DD; <config_var> = <value>
```

**Derived/comparison step format:**
```
threshold = YYYY-MM-DD (today+X); <var> <comparison> threshold → <visible|hidden|allowed|blocked>
```

**Forbidden vague values (never use without anchoring):**
- "today", "yesterday", "tomorrow", "next week" — declare `today = 2026-05-19`.
- "near midnight", "device time" — declare both clocks: `today (JST) = 2026-05-19; today (device/ICT) = 2026-05-18`.
- "current config" — declare `X = 3` or `capacity = 1`.

**Correct:**
| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Browse Lessons | Browse shown | today = 2026-05-19; lesson_date = 2026-05-26; X = 3 |
| 2 | View the lesson card | Lesson is visible | threshold = 2026-05-22 (today+3); lesson_date 2026-05-26 ≥ threshold → visible |

**Forbidden:**
| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Browse Lessons | Lesson is visible | lesson is in the future, within window |

## 12. Suite grouping
- Each `.md` file = one suite. Files match the Suggested Test Suite Structure from the coverage file.
- Within each file, group cases under `## Suite: <Suite Name>` headings.
- Order: happy path → edge cases → negative cases → cross-system.
