# Coverage — Mandatory Edge-Case Patterns Checklist

Used in Step 4.5 of `define-test-coverage`. For **every business rule** of the relevant logic type, answer each item.

- "N/A" requires a stated reason.
- "Yes" requires a row in the Coverage Strategy table AND the gap analysis.
- Missing an item without justification is a defect in the coverage file.

---

## A. Configuration-driven thresholds
Trigger: rule mentions tenant/partner config (advance days, max capacity, cancellation deadline).
- [ ] BVA at default config value (boundary, boundary−1, boundary+1)
- [ ] BVA at minimum supported value (incl. 0 or 1)
- [ ] BVA at maximum supported value
- [ ] Config decrease while data exists → previously hidden items now visible after refresh
- [ ] Config increase while data exists → previously visible items now hidden after refresh
- [ ] Config = 0 / disabled (if allowed)

## B. Date / Time logic
Trigger: rule depends on current time, date comparison, or deadline.
- [ ] TZ gap — device TZ BEHIND business TZ near midnight → which date is used?
- [ ] TZ gap — device TZ AHEAD of business TZ near midnight → which date is used?
- [ ] Cross-midnight while UI open (23:58 → 00:01)
- [ ] Past date / yesterday always hidden/blocked
- [ ] Today as input — boundary treatment?
- [ ] DST transition (JST does not observe — usually N/A)

Every date-related TC must declare `today = YYYY-MM-DD` and `target_date = YYYY-MM-DD` in test data.

## C. Concurrent / stale state
Trigger: shared resource (capacity, booking, seat) or time-based gate (deadline, expiry).
- [ ] Stale cache — last seat taken between page load and Reserve tap
- [ ] Stale UI — deadline expires while on confirmation screen
- [ ] Double-submit / rapid re-tap
- [ ] Multi-tab / multi-device same account

## D. Permission & role (any role gate)
- [ ] Every role tested (Admin, CM, Teacher, Student, Parent, Guest)
- [ ] Cross-tenant — User in Tenant A cannot access Tenant B
- [ ] Feature flag OFF — graceful behavior

## E. State transition (entity has status field)
- [ ] Every documented transition has a positive test
- [ ] Every undocumented transition has a negative test (Cancelled → Published blocked)
- [ ] Side-effects propagate to all surfaces (BO, App, SF, notifications)

## F. Cross-system / cross-surface
- [ ] Change in surface 1 visible in surface 2 within SLA
- [ ] Surface 2 down / sync fails → surface 1 still consistent (no partial write)

## G. Downstream effects — MANDATORY for every CREATE/UPDATE/DELETE rule
The primary action is half the test. Every record the action writes/increments/decrements/deletes/flips-flag-on/notifies must have its own verification row.

- [ ] Inverse action exists? (book↔cancel, publish↔unpublish). Every "+1 / create" needs a matching "−1 / delete" on the inverse.
- [ ] Counter fields incremented/decremented? → One TC per counter, both directions if mirrored.
- [ ] Auto-created child records? → One TC per child verifying creation, fields, linkage.
- [ ] Auto-deleted child records on inverse action? → One TC per entity.
- [ ] Flag flips on parent/sibling entities? → One TC for flip + one per downstream consumer.
- [ ] Staff-facing surface (BO) reflects the change? → One TC per affected BO screen.
- [ ] Peer-facing surface (other students/teachers) reflects the change? → One TC per peer surface.
- [ ] Continuation flows enabled by the action? → One TC per continuation, end-to-end.
- [ ] Idempotency under rapid double-tap / retry? → One TC verifying exactly-once semantics.

Fill the **Downstream Effects Inventory Table** before writing Coverage Strategy rows:

| Primary Action | Downstream Effect | Affected Entity / Surface | Verification Owner (TC) |
|---|---|---|---|
| Student books lesson | Student Session created | SF Student_Session | TC-XX |
| Student books lesson | LA Lesson_Allocated +1 | SF Lesson Allocation | TC-XX |
| Student books lesson | Lesson Report Detail auto-created | SF Lesson_Report_Detail | TC-XX |
| Student books lesson | Visible in BO Lesson Detail student tab | BO Lesson Detail | TC-XX |
| Student books lesson | Staff can mark attendance in Collect Attendance | BO Collect Attendance | TC-XX |
| Student books lesson | Student can Submit Attendance | Learner App | TC-XX |
| Student books lesson | Draft → Published; visible to peers | Learner App (peers) | TC-XX |
| Student books lesson | Points deducted from Point LA | SF Lesson Allocation | TC-XX |
| Student books lesson | Idempotent under rapid double-tap | Server | TC-XX |
| Student cancels booking | (mirror of above) | … | … |

## H. Display completeness & ordering — MANDATORY for every screen/card/list
- [ ] Required field inventory — one TC asserts ALL required fields are present simultaneously.
- [ ] Conditional/dynamic fields — one TC for condition TRUE, one for FALSE.
- [ ] Tooltip/helper/error exact text — verbatim assertion required.
- [ ] Sort/ordering rule — at least one TC with 2+ items differing on the sort key.
- [ ] Empty state — placeholder shown, no crash.
- [ ] Pagination/scroll — items beyond first page accessible.

**Display & Ordering Inventory Table** — fill before Coverage Strategy:

| Screen / Component | Required Fields | Conditional Fields | Sort Rule | Tooltip / Text to Assert |
|---|---|---|---|---|
| Booking List card | lesson name, date, center, teacher | Cancel button (if booked) | none | none |

Every non-empty "Required Fields" → one row with Logic Type = Display completeness.
Every non-empty "Sort Rule" → one row with Logic Type = Ordering / Sort.
Every non-empty "Tooltip" → that exact text in the Expected Result of a TC step.

## H.1 — Spec–Figma display mismatch — MANDATORY when spec has Figma URL
1. Fetch each Figma URL via `mcp_figma_get_figma_data`.
2. Extract visible text labels, field names, component names from relevant frames.
3. Build the Spec–Figma Mismatch Table:

| Screen / Component | Field | In Spec? | In Figma? | Mismatch Type | Action |
|---|---|---|---|---|---|
| Browse card | teacher name | ✅ | ❌ | Spec has, Figma absent | 🔴 Review needed |

Mismatch types:
- **Spec has field, Figma absent** — 🔴 must resolve.
- **Figma has field, Spec absent** — 🔴 must resolve.
- **Label mismatch** — 🟡 confirm wording.
- **Conditional field** — 🟡 confirm condition.

4. **STOP** and surface all 🔴 and 🟡 rows to the user. Do not generate Coverage Strategy until the user resolves each row.
5. After resolution:
   - Confirmed required → add to Display Inventory.
   - Confirmed not required → mark N/A.
   - Label corrections → update "Tooltip / Text to Assert" with Figma-confirmed label.

If no Figma URL in spec: skip and note `H.1 — N/A: No Figma URL in spec.`
