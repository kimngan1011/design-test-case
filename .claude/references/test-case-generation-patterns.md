# Test Case Generation Patterns

Per-technique generation rules + overrides by Coverage Depth and Risk Level. Used by `generate-test-cases` Step 3.

---

## Generation pattern per technique

| Technique | Generation pattern |
|---|---|
| **Equivalence Partitioning** | One TC per valid partition + one TC per invalid partition. |
| **Boundary Value Analysis** | TC for: exact boundary (reject), one below (reject), one above (accept), far above (accept). |
| **Decision Table** | One TC per meaningful combination of conditions and outcomes. |
| **State Transition** | TC for each valid transition + TC for each invalid/blocked transition. |
| **Pairwise** | Minimum set of combinations covering all pairs of input values. |
| **CRUD** | TC for Create, Read, Update, Delete — happy + conflict/error paths. |
| **Permission Matrix** | One TC per role per action (allowed + denied). |
| **Regression** | Identify existing TC IDs at risk; write new TCs that exercise the changed flow. |
| **Negative** | TC for each invalid input, blocked action, or error state. |
| **Component** | One TC asserts ALL required fields simultaneously on a populated component. |
| **Scenario** | Construct 2+ items differing on the sort/order criterion; assert the visible order explicitly. |

---

## Coverage Depth overrides

| Depth | Behavior |
|---|---|
| **Deep** | Generate BVA boundaries, multiple decision-table rows, cross-surface verifications. |
| **Standard** | Happy path + 1–2 negative cases. |
| **Smoke** | Primary happy path only. |

---

## Risk Level overrides

| Risk | Behavior |
|---|---|
| **Critical / High** | Always generate negative AND boundary TCs, even if not the primary technique. |
| **Medium / Low** | Stick to the selected technique at standard depth. |

---

## Skip rule

Do NOT generate a TC for a business rule already fully covered by an existing TC in the coverage file's Section 6 (Overlap = Full). Reference the existing TC ID in the gap analysis instead.
