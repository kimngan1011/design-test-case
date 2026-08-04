# Test Coverage: LT-98512 — Riso Classroom Reassignment by Student

**Jira:** https://manabie.atlassian.net/browse/LT-98512  
**Primary requirement source:** [PRD v8](https://manabie.atlassian.net/wiki/spaces/PRDM/pages/2416181249/Riso+OOP+Classroom+Reassignment+by+Student+Classroom+Optimization)  
**Date:** 2026-07-23  
**Qase baseline:** PX suite 3231 exists and contains 0 cases.

> The unresolved PRD questions remain product-review items. Coverage below creates explicit decision tests for them; no expected behavior is invented where the PRD is ambiguous.

---

## 1. Business Rules Extracted

| # | AC | Business Rule |
|---:|---|---|
| 1 | AC-01 | Put Classroom Adjustment above Print Out. |
| 2 | AC-02 | Expose the action only in Daily View. |
| 3 | AC-03, AC-06 | Limit processing to the current Location, Lesson Date, and Individual teaching method. |
| 4 | AC-04 | Show the exact success message and five result counters. |
| 5 | AC-05 | Keep Print Out available after adjustment. |
| 6 | AC-07 | Group lessons by student. |
| 7 | AC-07 | Sort each student's lessons by start time ascending. |
| 8 | AC-07 | Break equal-start-time ties with Lesson ID ascending. |
| 9 | AC-08 | For a later lesson, try the most recently processed earlier lesson's classroom first. |
| 10 | AC-09 | Fall back to Rule 2 if Rule 1 cannot apply. |
| 11 | AC-08–09 | Rule 1/Rule 2 outcome becomes the candidate for the next chronological lesson. |
| 12 | AC-10 | Rule 2 chooses the eligible classroom with lowest Classroom Sequence. |
| 13 | AC-11 | Eligible classroom belongs to the selected Location. |
| 14 | AC-11 | Eligible classroom has Type = Private. |
| 15 | AC-11 | Eligible classroom is not assigned to another lesson in the same slot. |
| 16 | AC-12 | Never select a classroom that would clash. |
| 17 | AC-13 | Re-evaluate every lesson for a student with 3+ lessons. |
| 18 | AC-14 | Continue after an individual assignment failure. |
| 19 | AC-15 | With no available room, skip and retain the current classroom (subject to the PRD conflict decision). |
| 20 | AC-16 | With two students, skip and retain the current classroom. |
| 21 | AC-17 | Detect pre-existing duplicate classroom/slot assignments at process start. |
| 22 | AC-17–18 | Preserve one duplicate and reassign other duplicates by Rule 2; if impossible, keep current room and mark unresolved. |
| 23 | AC-19 | Preserve duplicate by chronological order, then Lesson ID ascending. |
| 24 | US03 (duplicate AC-17) | Allow manual classroom editing after the run. |
| 25 | Config | Enable Optimize Classroom Assignment for Riso only. |
| 26 | NFR-01 | Process Riso workload within an approved SLA (not yet specified). |
| 27 | NFR-08 | Concurrent actions must not produce inconsistent results. |

## 2. Logic Type Categorization

| Business Rule # | AC | Logic Type |
|---|---|---|
| 1–2 | AC-01–02 | Display completeness; Conditional logic |
| 3 | AC-03, AC-06 | Conditional logic; Data integrity |
| 4 | AC-04 | Display completeness; Data integrity |
| 5 | AC-05 | Cross-system impact; State transition |
| 6–8 | AC-07 | Ordering / Sort; Data integrity |
| 9–11 | AC-08–09 | Conditional logic; Data integrity; Ordering / Sort |
| 12 | AC-10 | Ordering / Sort; Conditional logic |
| 13–16 | AC-11–12 | Validation logic; Data integrity; Boundary/range logic |
| 17–20 | AC-13–16 | Conditional logic; Data integrity |
| 21–23 | AC-17–19 | Data integrity; Ordering / Sort; Conditional logic |
| 24 | US03 duplicate AC-17 | Cross-system impact; State transition |
| 25 | Config | Conditional logic; Permission logic |
| 26 | NFR-01 | Boundary/range logic; Data integrity |
| 27 | NFR-08 | Data integrity; Cross-system impact |

## 3. Test Technique Selection

| Logic Type | Applicable Techniques |
|---|---|
| Validation logic | Equivalence Partitioning; Negative |
| Boundary/range logic | Boundary Value Analysis; Negative |
| Conditional logic | Decision Table; Negative |
| Permission logic | Permission Matrix; Decision Table |
| Data integrity | CRUD; Regression; Decision Table |
| Cross-system impact | Regression; CRUD |
| Display completeness | Component; Negative |
| Ordering / Sort | Scenario; Pairwise |

## 4. Structured Coverage Strategy

| AC | Business Rule Summary | Logic Type | Test Technique | Risk Level | Coverage Depth |
|---|---|---|---|---|---|
| AC-01 | Action is above Print Out in Daily View. | Display completeness | Component; Regression | Medium | Standard |
| AC-02 | Action appears only in Daily View, not Month/Week or non-Daily contexts. | Conditional logic | Decision Table; Negative | Medium | Standard |
| AC-03/06 | Trigger uses exactly selected Location/date and Individual lessons; no out-of-scope lesson changes. | Conditional logic; Data integrity | Decision Table; CRUD | High | Deep |
| AC-04 | Show exact “Classroom adjustment completed” plus all five counters; test counter reconciliation once category rules are confirmed. | Display completeness; Data integrity | Component; Decision Table | High | Deep |
| AC-05 | Print Out remains actionable after a completed run and uses resulting assignments. | Cross-system impact | Regression; Scenario | High | Deep |
| AC-07 | Process per student, chronological start-time order, then Lesson ID tie-breaker. | Ordering / Sort | Scenario; Pairwise | High | Deep |
| AC-08 | Reuse the most recently processed earlier classroom when it is eligible. | Conditional logic; Data integrity | Decision Table; CRUD | High | Deep |
| AC-09 | Fall back to Rule 2 when Rule 1's candidate is unavailable. | Conditional logic | Decision Table; Negative | High | Deep |
| AC-10 | Rule 2 selects the lowest eligible Classroom Sequence. | Ordering / Sort | Scenario; Pairwise | High | Deep |
| AC-11 | Eligibility requires same Location, Private type, and no same-slot clash; status/selectability is a pending V1 decision. | Validation logic; Data integrity | Equivalence Partitioning; Negative | High | Deep |
| AC-12 | Reject Rule 1/2 candidate that clashes, including partial-overlap regression coverage. | Data integrity | CRUD; Regression; Decision Table | High | Deep |
| AC-13 | Apply Rules 1/2 repeatedly for 3+ lessons; verify room continuity after a Rule 2 switch. | Conditional logic; Data integrity | Decision Table; Scenario | High | Deep |
| AC-14 | One failed assignment does not stop remaining lessons. | Data integrity | CRUD; Negative | High | Deep |
| AC-15 | No-room handling retains the room or other approved outcome; cover each resolved branch. | Conditional logic; Data integrity | Decision Table; Negative | High | Deep |
| AC-16 | Two-student lessons are skipped without overwriting their classroom. | Conditional logic; Data integrity | Equivalence Partitioning; Regression | High | Deep |
| AC-17 | Detect pre-existing duplicate classroom/slot allocations and preserve one. | Data integrity; Ordering / Sort | CRUD; Scenario | High | Deep |
| AC-18 | When duplicate clash cannot be resolved, retain current room, mark unresolved, and continue. | Data integrity | CRUD; Negative | High | Deep |
| AC-19 | Choose preserved duplicate by chronology and then Lesson ID. | Ordering / Sort | Scenario; Pairwise | High | Deep |
| US03 duplicate AC-17 | Manual classroom edit remains possible and clash validation still applies after automation. | Display completeness; State transition; Cross-system impact | Component; CRUD; Regression | High | Deep |
| Config | Feature is visible/enabled only when the Riso Optimize Classroom Assignment setting is ON. | Conditional logic; Permission logic | Decision Table; Permission Matrix | High | Deep |
| NFR-01 | Benchmark at the final approved data-volume/runtime thresholds; report timeout/error behavior. | Boundary/range logic | Boundary Value Analysis; Negative | High | Deep |
| NFR-08 | Concurrent run, retry, and manual edit produce one consistent, explainable result. | Data integrity; Cross-system impact | CRUD; Regression; Decision Table | Critical | Deep |

## 5. High-Risk Areas Requiring Deeper Testing

### 🔴 Critical Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| Concurrent classroom writes | A partial or racing run can leave conflicting room assignments, breaking daily operations. | Multi-user/multi-tab decision table; verify exactly-once outcome, all changed lessons, counters, and error feedback. |

### 🟠 High Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| Scope isolation | Wrong Location/date or group lesson updates are unintended data writes. | Seed selected and non-selected locations/dates/methods; assert every unaffected classroom remains unchanged. |
| Rule 1/Rule 2 sequencing | A wrong prior-room candidate or sort tie-breaker changes many assignments. | Multi-lesson, multi-student scenarios with start-time and Lesson-ID ties. |
| Availability and overlap | Existing partial-overlap clash behavior must remain intact. | Include exact-slot and partial-overlap fixtures across Private/non-Private and foreign Location rooms. |
| Existing clashes / no-room fallback | The PRD has competing no-room statements and unresolved clashes are safety-sensitive. | Run only after product decision; assert preservation/reassignment, counter category, continuation, and manual follow-up. |
| Tenant configuration / manual follow-up | Incorrect exposure changes partner behavior or locks staff out of daily correction. | Feature-flag and role matrix plus post-run manual edit and Print Out regression. |

### 🟡 Medium Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| Menu and result summary | Daily operational UX depends on action placement and readable feedback. | Required-field component assertion, exact success text, zero-result empty outcome, and navigation regression. |

## 6. Coverage Gaps vs. Existing Test Cases

| Gap Area | Existing Test Case | Overlap | New Coverage Needed |
|---|---|---|---|
| Classroom overlap detection | `calendar/LT-XXXX-drag-drop-edit-lesson-time` CSV | Existing manual change treats partial overlap as clash. | ✅ Automated adjustment must reject exact and partial overlaps. |
| Daily View reachability | `calendar/LT-89471-calendar-bug-fix` Daily View scrollbar cases | Baseline navigation only. | ✅ Action placement/visibility and post-run Print Out continuity. |
| Riso Calendar action/config | `calendar/LT-98532-bulk-publish-lessons-by-student` | Different action/config. | ✅ Riso-only Optimize Classroom Assignment config and scope isolation. |
| Classroom reassignment algorithm | PX suite 3231 (0 cases) | None. | ✅ All Rule 1/Rule 2, sequencing, skips, duplicate-clash, and concurrency coverage. |
| Summary and manual review | No matching case found. | None. | ✅ Exact result summary, counters, manual edit, and failure feedback. |
| Performance | No matching case found. | None. | ✅ Approved benchmark/timeout tests after NFR-01 values are confirmed. |

## G. Downstream Effects Inventory

| Primary Action | Downstream Effect | Affected Entity / Surface | Verification Owner (planned suite) |
|---|---|---|---|
| Run adjustment | Classroom field is updated only for eligible in-scope lessons. | Lesson record / Salesforce Daily View | `scope-and-config` |
| Run adjustment | Unaffected Location/date/group lessons retain their classroom. | Lesson records outside scope | `scope-and-config` |
| Run adjustment | Room becomes unavailable for later overlapping lessons in the same run. | Subsequent assignment decision | `assignment-rules` |
| Run adjustment | Pre-existing duplicate is retained or reassigned; unresolved duplicate remains traceable. | Lesson records / result summary | `clash-and-failure-handling` |
| Run adjustment | Summary counters describe the final result. | Daily View result summary | `action-and-summary` |
| Run adjustment | User can continue to Print Out and review changed rooms. | Existing Print Out flow | `action-and-summary` |
| Run adjustment / retry | No duplicate or conflicting write occurs under retry/concurrency. | Server and Daily View | `concurrency-and-performance` |
| Manual edit after run | Classroom can be corrected and existing clash safeguards apply. | Lesson record / Daily View | `manual-follow-up` |

## H. Display & Ordering Inventory

| Screen / Component | Required Fields | Conditional Fields | Sort Rule | Tooltip / Text to Assert |
|---|---|---|---|---|
| Daily View action menu | Classroom Adjustment action; existing Print Out action | Adjustment visible only for Daily View and flag ON | Adjustment is above Print Out | None specified |
| Completion summary | Previous room applied; Sequence assigned; Skipped; Clash resolved; Clash unresolved (kept as-is) | Display after successful run, including zero-update result | N/A — fixed counter labels | `Classroom adjustment completed` |
| Student lesson processing | Classroom selected for each eligible lesson | Rule 1 vs Rule 2; skipped/unresolved branches | start time ascending, then Lesson ID ascending; Rule 2 sequence ascending | None specified |
| Classroom manual edit | Existing classroom value and edit affordance | Available after adjustment | Existing Calendar behavior | None specified |

### H.1 Spec–Figma Mismatch Report

**N/A:** no Figma URL is present in the Jira ticket or primary PRD.

## 7. Suggested Test Suite Structure

```text
epics/OOP/riso/LT-98512-classroom-reassignment-student/test-cases/
├── action-and-summary.md            → AC-01–05: Daily View action, summary, Print Out
├── scope-and-config.md              → AC-02–03, AC-06, Config: tenant flag and scope isolation
├── assignment-rules.md              → AC-07–13: ordering, Rule 1, Rule 2, eligibility
├── clash-and-failure-handling.md    → AC-12, AC-14–19: overlaps, skips, pre-existing clashes
├── manual-follow-up.md              → US03 duplicate AC-17: edit after adjustment
└── concurrency-and-performance.md   → NFR-01, NFR-08: benchmark and concurrent writes
```

## 8. Open Decisions Carried Forward

The following must be resolved before test cases assert a single expected outcome: AC-15 no-room result, overlap definition, AC-04 counter reconciliation, Rule 1 candidate after an invalid/changed earliest lesson, Classroom Status/selectability in V1, non-1/non-2 student behavior, duplicate AC identifier, NFR-01 benchmark/timeout, concurrency outcome, and Salesforce/BO role scope.
