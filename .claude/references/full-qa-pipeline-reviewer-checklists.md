# Full QA Pipeline — Reviewer Checklists

Used by the `full-qa-pipeline` agent's Internal Reviewer after each phase, before the user approval gate.

---

## Reviewer mechanics

1. Read artifacts from disk (do NOT rely on chat memory).
2. Run the phase-specific checklist below.
3. For each failed check, classify:
   - **Auto-fixable** → cosmetic, formatting, trivial missing fields. Fix directly.
   - **Re-run required** → substantive gap. Re-invoke the phase's skill with a specific fix instruction. Max 2 retries.
   - **Open issue** → cannot be auto-fixed or fully resolved within 2 retries. Surface in the approval gate.
4. Tally: `✅ <passed> / ⚠️ <auto-fixed> / ❌ <open>`.

---

## Phase 1 — Analyze Requirements

The `analyze-requirement` sub-agent already runs its own 13-point validation. This top-level integrity check is additive.

| # | Check | Action on fail |
|---|---|---|
| 1 | Spec file exists at `epics/<bucket>/<TICKET-ID>-<slug>/spec.md` | Re-run analyze-requirement |
| 2 | All required spec sections present (Summary, Acceptance Criteria, Business Rules, Conflict & Gap Analysis, Clarification Questions, Related Specs, Related Test Cases, QASE Coverage Gaps) | Auto-fix: add missing section headers with "_None_" placeholder |
| 3 | Business Rules table is non-empty | Re-run |
| 4 | At least one finding tag used in Conflict & Gap Analysis (or explicit "no findings" reason) | Re-run analyze-impact |
| 5 | Clarification Questions section reflects Jira post status (✅ Posted or "not posted") | Auto-fix |
| 6 | `temp/` directory cleaned (workspace-cleanup ran) | Run workspace-cleanup |

---

## Phase 2 — Define Test Coverage

| # | Check | Action on fail |
|---|---|---|
| 1 | Coverage file saved to `epics/<bucket>/<TICKET-ID>-<slug>/test-coverage.md` | Re-run |
| 2 | Section 1 Business Rules table matches the Phase 1 spec (count + AC IDs) | Re-run define-test-coverage |
| 3 | Every business rule has a Logic Type assigned (Section 2) | Re-run |
| 4 | Every Logic Type has at least one Test Technique (Section 3) | Re-run |
| 5 | Every AC row in Section 4 has Risk Level + Coverage Depth | Re-run |
| 6 | At least one Critical/High risk area identified in Section 5 (if feature has state changes, data writes, or cross-system sync) | Re-run |
| 7 | Section 6 gap table marks new coverage needed with ✅ | Auto-fix |
| 8 | Section 7 suite structure groups related ACs logically | Open issue if illogical |
| 9 | For every UI card/list/form in the spec, the coverage table has at least one row with Logic Type = **Display completeness** | Re-run with explicit instruction |
| 10 | For every sort/ordering rule in the spec, the coverage table has at least one row with Logic Type = **Ordering / Sort** | Re-run with explicit instruction |
| 11 | For every tooltip/disabled-state message/exact UI text in the spec, the coverage table has at least one row asserting that exact text | Re-run with explicit instruction |
| 12 | For every CREATE/UPDATE/DELETE rule, the Downstream Effects Inventory Table (Section G) is filled; every non-empty row maps to a Coverage Strategy row | Re-run downstream effects analysis |
| 13 | If spec has Figma URL: Section H.1 Spec–Figma Mismatch Report produced AND every 🔴 row resolved by user before Coverage Strategy was written. If no Figma URL: note reads "H.1 — N/A" | **Block** — do NOT advance to Phase 3 until user has acknowledged all mismatch rows |

---

## Phase 3 — Generate Test Cases

| # | Check | Action on fail |
|---|---|---|
| 1 | Both `.md` and `.csv` files saved at the paths in Section 7 of the coverage file | Re-run |
| 2 | Every AC in Section 4 of the coverage file has at least one test case | Re-run |
| 3 | Every Critical/High risk area has at least one negative or boundary case | Re-run |
| 4 | No title contains forbidden words: Verify, Check, Test, Properly, Correctly, Successfully | Auto-fix titles |
| 5 | Title format `[Feature] – [Sub-feature] – Condition – Expected Behavior` | Auto-fix where possible |
| 6 | OOP/tenant-specific cases prefixed with `[TenantName]` | Auto-fix |
| 7 | Every TC has explicit preconditions with concrete test data | Re-run case-by-case |
| 8 | Every step has deterministic expected result (no "correct"/"as expected") | Re-run case-by-case |
| 9 | Severity ∈ {critical, major, minor, trivial} — never `normal` | Auto-fix (`normal` → `minor`) |
| 10 | Priority ∈ {high, medium, low} mapped from Risk Level | Auto-fix |
| 11 | CSV columns match the Qase schema in `.claude/references/qase-format.csv` | Auto-fix headers |
| 12 | Each TC = one logical validation (no combined assertions) | Open issue |
| 13 | For every CREATE/UPDATE/DELETE AC, at least one TC verifies a downstream effect (counter, child record creation/deletion, flag flip, surface change) — not only the primary entity | Re-run for that AC |
| 14 | For every **Display completeness** row, the TC asserts every required field with a concrete expected value (not vague "field is shown") | Re-run case-by-case |
| 15 | For every **Ordering / Sort** row, the TC sets up 2+ items differing on sort keys and asserts the relative order explicitly | Re-run case-by-case |
| 16 | For every **tooltip / exact UI text**, the TC step expected result contains the verbatim string from the spec | Re-run case-by-case |

---

## Phase 4 — Import to Qase

| # | Check | Action on fail |
|---|---|---|
| 1 | All suite names resolved to real Qase suite IDs (no placeholders) | Re-run import |
| 2 | No duplicate cases created — duplicates skipped with log entry | Surface skipped list |
| 3 | Spot-check ≥1 case via `mcp_qase_get_case` — multi-line fields render with real line breaks (no literal `\n` or `/n`) | Update affected case |
| 4 | Local `.csv` updated with real Qase suite IDs | Auto-fix |
| 5 | Import summary printed with totals (suites created/existed, cases created/skipped/failed) | Auto-fix |
