# Test Cases: LT-98530 — [Riso] OOP | Contract and Monthly Lesson history (App)

## Suite: [Riso] Permission, Scope & Cross-Surface Consistency

### [Riso] Contract Info and Lesson History – Non-Riso Tenant – Feature Entry Point Not Shown

**Description:** Cross-cutting — Permission Matrix — This is a Riso-only OOP feature; the entry points for Contract Info and Lesson History must not appear for non-Riso tenants.

**Preconditions:**
- Logged in as Student to a non-Riso tenant's Learner App (e.g. Renseikai)

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open the User Profile menu | No "Contract Info" entry point is shown | tenant=Renseikai (non-Riso); expected=hidden |
| 2 | Open the app main menu | No "Lesson History" entry point is shown | tenant=Renseikai (non-Riso); expected=hidden |

**Severity:** minor
**Priority:** medium

---

### [Riso] Contract Info – Student Own Data Only – Other Student's Contracts Not Accessible

**Description:** Cross-cutting — Permission Matrix — A student must never be able to view another student's Contract Info or Lesson Allocated data.

**Preconditions:**
- Logged in as Student A to the Riso Learner App
- Student B (a different student, no relationship to Student A) has active LAs and contracts

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Contract Info as Student A | Only Student A's own LA cards are shown; Student B's data is never displayed or reachable | logged_in_as=Student A; expected=only own data visible |

**Severity:** major
**Priority:** high

---

### [Riso] Contract Info and Lesson History – Parent With Multiple Linked Children – Data Scoped to Selected Child (Pending Confirmation)

**Description:** Cross-cutting — Permission Matrix — For a parent account linked to multiple children, both pages must scope strictly to whichever child is currently selected via the existing header selector (spec Clarification Question #9).

**Preconditions:**
- Logged in as Parent to the Riso Learner App, linked to Child A and Child B

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Select Child A in the profile header and open Contract Info | Only Child A's LA cards are shown | selected_child=A; expected=Child A data only |
| 2 | Switch the profile header selector to Child B and reopen Contract Info | Only Child B's LA cards are shown; Child A's data is no longer visible | selected_child=B; expected=Child B data only |

**Severity:** major
**Priority:** high

---

### [Riso] Contract Info – Data Sync Staleness Banner – Displayed Until New Contract Reflected

**Description:** Cross-cutting — Scenario — The info banner acknowledges eventual-consistency lag between the Riso ERP contract push (LT-98533 API) and its display on the App.

**Preconditions:**
- Logged in as Student to the Riso Learner App
- A new Riso Contract was just submitted via the API for this student's LA, not yet reflected in the App cache

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Contract Info immediately after the API submission | The info banner is shown; Total Slot may not yet reflect the new contract | contract_submitted_at=T+0; app_view_at=T+0; expected=banner shown, data may lag |
| 2 | Reopen Contract Info after the sync completes | Total Slot now reflects the new contract | app_view_at=T+sync_complete; expected=data updated |

**Severity:** minor
**Priority:** medium

---

### [Riso] Total Slot – Contract Created via API – Becomes Visible on Next Page Load

**Description:** Cross-cutting — Cross-system / Scenario — A Contract created via the LT-98533 API for an LA must be reflected in the App's Total Slot without requiring any App-side action.

**Preconditions:**
- Logged in as Student to the Riso Learner App
- Student's LA currently has Total Slot = 0 (no contracts yet)

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Submit a new Active Monthly-type Riso Contract via the API for this LA (start=2025-04, monthly slot=4, current selected month=Sep 2025) | Contract is created and linked to the LA | contract_slot=4; contract_start=2025-04 |
| 2 | Reopen the Contract Info page | Total Slot now shows the newly submitted contract's contribution | selected_month=2025-09; expected=Total Slot reflects new contract (pending confirmation of exact formula, see Clarification Q1) |

**Severity:** minor
**Priority:** medium

---

### [Riso] Lesson History – Draft Lesson – Never Displayed Regardless of Other Filters

**Description:** Cross-cutting — Negative / State Transition Guard — A Draft-status lesson must never appear in Lesson History, since Draft lessons are never synced to Mobile at the platform level.

**Preconditions:**
- Logged in as Student to the Riso Learner App
- Student has a Draft-status lesson on 2025-09-20 that would otherwise match the selected month

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Lesson History for September 2025 | The Draft lesson on 2025-09-20 is NOT shown (never reaches Mobile) | lesson_status=Draft; expected=excluded (platform-level guarantee) |

**Severity:** minor
**Priority:** medium

---

### [Riso] Total Slot and Lesson Allocated – Cross-Surface Regression – Contract Update Reflected Consistently Across App, SF Report, and API

**Description:** Cross-cutting — Regression — End-to-end check that a single Contract update via the API is reflected consistently (or its known divergence is documented) across all three consuming surfaces: this App, the SF Monthly Lesson Assignment report (LT-98531), and the raw API aggregation (LT-98533).

**Preconditions:**
- Logged in as Student to the Riso Learner App and as HQ or CM Staff to the Salesforce org (same student's LA)
- LA has one Active Monthly-type Riso Contract: start=2025-04, monthly slot=4

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Update the Contract's monthly slot from 4 to 6 via the API | LA aggregation recalculates | new_monthly_slot=6 |
| 2 | View Total Slot on the App for September 2025 | App shows updated value per PRD's prorated formula (6×6=36) | app_total_slot expected=36 (pending confirmation vs API aggregation) |
| 3 | View LA.Total_Session_Count on Salesforce | SF shows the flat aggregated value per LT-98533, compare against step 2 and log any discrepancy as pending confirmation (Clarification Q1) | sf_total_session_count = SUM(contract.total); compare vs app value |

**Severity:** major
**Priority:** high

---
