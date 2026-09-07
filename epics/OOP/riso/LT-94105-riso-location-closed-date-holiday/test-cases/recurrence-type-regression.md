# Test Cases: LT-94105 — Riso Location Closed Date and Holiday

## Suite: Closed Date Type Change Regression

### [Riso] Closed Date – Type update – Future Holiday occurrence – Regeneration creates the future occurrence

**Description:** AC 01.2 / AC 02.1 — State Transition — Confirms a future occurrence uses the current Type when recurrence generation runs.

**Preconditions:**
- Logged in as HQ Staff with Closed Date edit access for Riso Center A.
- today = `2026-07-01`; `2026-07-20` is Closed Date; a schedule has no generated occurrence for `2026-07-20` yet.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Change `2026-07-20` Type from `Closed Date` to `Holiday`. | The ACI record saves with Type `Holiday`. | target_date = 2026-07-20 |
| 2 | Run or wait for recurrence generation for the three-Monday schedule. | The schedule is evaluated using Type `Holiday`. | dates = 2026-07-13, 07-20, 07-27 |
| 3 | Open occurrences. | A normal recurring lesson exists on `2026-07-20`. | expected occurrences on 07-20 = 1 |

**Severity:** major
**Priority:** high

---

### [Riso] Closed Date – Type update – Existing generated lessons – Historical occurrences remain unchanged

**Description:** AC 01.2 — Regression — Confirms the documented non-retroactive ACI behavior for a Type change after lesson generation.

**Preconditions:**
- Logged in as HQ Staff with Closed Date edit access for Riso Center A.
- `2026-07-20` is Closed Date and an already-generated schedule has no lesson on that date.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Change `2026-07-20` Type from `Closed Date` to `Holiday`. | The record saves with Type `Holiday`. | target_date = 2026-07-20 |
| 2 | Inspect the existing generated lesson chain without running a new generation cycle. | The original chain remains unchanged. | existing occurrence on 07-20 = 0 |
| 3 | Search for a newly created lesson on `2026-07-20`. | No historical occurrence is added by the Type update alone. | expected occurrences on 07-20 = 0 |

**Severity:** major
**Priority:** high

---

### [Riso] Learner Calendar – Type update while open – Refresh – New Type appearance is displayed

**Description:** AC 01.2 / AC 01.3 — State Transition / Regression — Confirms the mobile surface does not retain a stale Type after refresh.

**Preconditions:**
- A Riso learner has July 2026 Calendar open on `2026-07-20`, currently a Closed Date.
- Logged in separately as HQ Staff with Closed Date edit access for Riso Center A.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Change `2026-07-20` Type from `Closed Date` to `Holiday` in the staff surface. | The ACI record saves with Type `Holiday`. | target_date = 2026-07-20 |
| 2 | Refresh the learner's July 2026 Calendar. | The `2026-07-20` date text uses `#295ACB` instead of Closed Date gray/diagonal treatment. | expected color = #295ACB |
| 3 | Open day detail for `2026-07-20`. | The detail contains `祝日`. | expected label = 祝日 |

**Severity:** major
**Priority:** high

---
