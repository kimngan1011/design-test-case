# Test Coverage: LT-90306 — Lesson Allocation Soft Delete (Archive)

**Jira:** https://manabie.atlassian.net/browse/LT-90306
**Date:** 2026-10-02

> **Scope note:** Core coverage (SF/BO/Mobile archive, unarchive, de-duplication, calendar, reallocation, attendance, Zoom, etc.) was already executed in a prior session — see the ~50 files already in `test-cases/`. This file covers only the **newly-scoped OOP/Aver addition**: the "Aver Lesson Report" impact flagged as [MISSING BEHAVIOR — OPEN, TICKETED] Gap #6 in `spec.md` ("Aver's custom lesson report lives outside the package; package filters don't reach it. Ticket: `[SF][Aver] Check custom aver lesson report` — 4h"), cross-referenced against Qase project PX, suite path **OOP FEATURES (311) → Aver (327) → Lesson Report correct (548)**, 155 existing manual cases.

---

## 0. Code-Trace Finding (changes the shape of this coverage)

Direct repo check in `school-portal-admin` and `erp-salesforce` (2026-10-02), following this epic's established practice of citing file:line before writing a TC:

- **Aver's Lesson Report *detail* page — Add/Edit/Delete/Status-transition, Homework copy, PDF export — is not React/TS or Apex code in either repo.** `LessonReportRouter.tsx:19-28,41-63` routes the Aver tenant (`LessonDetailSF.tsx:46`, `isAver = domainName === "aver" || "aver-sandbox"`) to `LessonReportDetailEmbeddedSF.tsx:1-58`, which renders a bare `<iframe>` pointing at an external Salesforce **Experience Cloud site** (URL from feature config `lesson.lesson_management.lesson_report.experience_cloud_site_url`). No `Aver_Lesson_Report__c` Apex class, trigger, or digitalExperience metadata exists in `erp-salesforce`.
- **Consequence:** whether that Experience Cloud site's Add/Edit/Delete/Status/homework-copy/PDF-export logic checks `Lesson_Allocation__c.Archived_At__c` / `Student_Sessions__c.Is_Archived__c` **cannot be confirmed or denied by static code review** — the implementation lives in a Salesforce org outside both repos this workspace has access to. This is a stronger finding than the spec's original framing ("lives outside the package" — true, but it's also outside *any* repo we can inspect). All 155 existing Qase cases in suite 548 test exactly this iframe'd surface (CRUD, status Draft→Submitted→Published, homework previous/next-week copy, PDF export) and gate purely on `Lesson__c.Status` — none reference archive state.
- **Aver's *list/search* layer is separate, real, local code and is already fixed — not a gap.** `aver-lesson-report-filters.ts:56` carries `MANAERP__Is_Archived__c: { eq: false }`, patched in the same commit as Core's equivalent (`5e9fb50ecd7`, "[LT-111546] filter archived lesson allocation records out of SF queries"). This is suite-549-or-sibling territory (list, not detail) and is **not** in scope for suite 548 — noted here only to avoid wrongly flagging it as a gap.
- A shared Core+Aver **legacy raw-SOQL list path** (`useRetrieveAverLessonReportList.ts:218-246`, `Aver_Lesson_Report__c` query, active only when `LESSON_MANAGEMENT_SF_ALLOW_VIEW_LESSON_OTHER_LOCATIONS` is OFF) has no archive filter either — a pre-existing, tenant-agnostic gap, not an Aver-specific regression. Out of scope for suite 548 (detail), flagged for whoever later covers the list suite.

**Implication for this coverage:** test cases for suite 548 cannot be written as "confirmed gap, code gives wrong result at line N" (the style used elsewhere in this epic) because there is no inspectable code. They are instead written as **[UNVERIFIED — requires live manual check]** cases: precise preconditions + steps to run against the real Aver sandbox/UAT org, with the AC-5-derived expected result stated explicitly, so a QA engineer can determine actual behavior and decide whether `[SF][Aver] Check custom aver lesson report` needs to become the fix vehicle.

---

## 1. Business Rules Extracted (subset relevant to this addition)

| # | AC | Business Rule |
|---|---|---|
| 7 (from spec) | AC-5 | Every read path **inside the managed package** excludes archived rows (`Archived_At__c = NULL` / `Is_Archived__c = FALSE`). |
| Gap #6 (from spec) | AC-5 (out-of-package) | Aver's custom lesson report lives outside the package; package-wide filters don't reach it — archive-filter behavior unconfirmed. |
| New (this pass) | AC-5 (out-of-package, unverifiable) | Aver's Lesson Report *detail* page specifically is an iframe to an external Experience Cloud Salesforce org with no source in either repo — archive-filter behavior cannot be confirmed by code trace at all, only by live test. |
| 5 (from spec) | AC-3 | Unarchive reuses the existing LA Id; no new record created; attendance/report history must survive the round trip. |
| — (scope note, AC-5) | AC-5 | Archived records remain reachable by direct record Id / report filter — historical Lesson Report + Homework must stay viewable, not hard-blocked, even once the parent LA archives. |

---

## 2. Logic Type Categorization

| AC | Business Rule # | Logic Type |
|---|---|---|
| AC-5 | 7, Gap #6, New | Cross-system impact, State transition, Data integrity |
| AC-5 (historical access) | scope note | Display completeness |
| AC-3 | 5 | Regression (round-trip survival) |

---

## 3. Test Technique Selection

| Logic Type | Applicable Techniques |
|---|---|
| Cross-system impact | Regression, CRUD |
| State transition | State Transition, Decision Table |
| Data integrity | CRUD, Negative |
| Display completeness | Component |

---

## 4. Structured Coverage Strategy

| AC | Business Rule Summary | Logic Type | Test Technique | Risk Level | Coverage Depth |
|---|---|---|---|---|---|
| AC-5 | Add Lesson Report blocked for a student whose LA is archived, even if the Lesson itself is still active | State transition / Data integrity | Decision Table | 🔴 Critical | Standard |
| AC-5 | Edit/Delete existing Draft or Submitted Lesson Report blocked once the student's LA archives mid-lifecycle | State transition | Decision Table | 🔴 Critical | Standard |
| AC-5 | Status transition (Submit/Publish/Revert) blocked once the student's LA archives | State transition | State Transition | 🔴 Critical | Standard |
| AC-5 | Previous/Next-week Homework copy does not silently pull from or write into an archived-LA lesson's report | Cross-system impact | Decision Table | 🟠 High | Standard |
| AC-5 (historical access) | Already-Published report + homework for an archived LA remains viewable (read-only) and exportable to PDF — not hard-blocked | Display completeness | Component | 🟠 High | Smoke |
| AC-3 | After unarchive (same LA Id restored), Lesson Report editing/status actions resume normally with no duplicate report | Regression | Regression | 🟡 Medium | Smoke |
| Gap #6 / New | Ownership/feasibility: is the Aver Experience Cloud site in scope for `[SF][Aver] Check custom aver lesson report`, or does it need its own ticket since it's outside both repos? | Cross-system impact | Scenario (environment check) | 🟠 High | Smoke |

### Mandatory edge-case checklist (applied)
- **A. Config-driven thresholds** — N/A, no tenant config threshold involved in this behavior.
- **B. Date/time** — N/A, no new date/time field; archive timestamp itself isn't user-facing here.
- **C. Concurrent/stale state** — Yes: Lesson Report edit screen open in one tab while LA archives in another (SPO removed concurrently) → covered below.
- **D. Permission & role** — Partial: actor is HQ/CM Staff or Teacher via Aver BO/Experience Cloud; no distinct role-gated behavior documented beyond existing suite, so not separately tested — existing 155 cases already cover role variants for the non-archive dimension.
- **E. State transition** — Yes: Draft→Submitted→Published blocked/not-blocked by archive state — covered.
- **F. Cross-system** — Yes: SF LA archive → Aver Experience Cloud site visibility — covered, flagged unverifiable by code.
- **G. Downstream effects** — see table below.
- **H. Display completeness** — Yes: historical report/homework must remain visible post-archive — covered.

### Downstream Effects Inventory Table (Section G)

| Primary Action | Downstream Effect | Affected Entity / Surface | Verification Owner (TC) |
|---|---|---|---|
| Student's LA archives (order group fully removed) while Lesson stays non-Canceled | Add button for this student's report should become unavailable | Aver Lesson Report Detail (Experience Cloud iframe) | TC-1 |
| Student's LA archives with an existing Draft/Submitted report | Edit should become blocked | Aver Lesson Report Detail | TC-2 |
| Student's LA archives with an existing Draft report | Delete should become blocked (or explicitly still allowed — must be confirmed, not assumed) | Aver Lesson Report Detail | TC-3 |
| Student's LA archives | Submit/Publish/Revert status actions should become blocked | Aver Lesson Report Detail | TC-4 |
| Student's LA archives | Previous/Next-week Homework copy must not treat the archived lesson as a valid source/target | Aver Lesson Report Detail | TC-5 |
| Student's LA archives after report was already Published | Report + homework history remains viewable/exportable (read-only) | Aver Lesson Report Detail + PDF export | TC-6 |
| Student's LA unarchives (restored, same Id) | Report editing/status actions resume; no duplicate report created | Aver Lesson Report Detail | TC-7 |
| N/A — environment/ownership | Confirm whether Aver Experience Cloud site is covered by the same fix ticket or needs a separate one | Jira / engineering ownership | TC-8 |

---

## 5. High-Risk Areas Requiring Deeper Testing

### 🔴 Critical Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| Aver Lesson Report Add/Edit/Delete/Status gated only by `Lesson.Status`, never by LA/session archive state (confirmed: 0 of 155 existing cases reference archive; underlying code is an unverifiable external iframe) | A staff member could create, edit, or publish a Lesson Report — and consume the reporting workflow — for a student whose enrollment/allocation has already been archived (order cancelled/voided), producing a report for a student who, per the rest of this epic, should no longer be actively tracked on this lesson | Live manual verification against Aver UAT/sandbox (not code trace — unavailable); Decision Table across {LA archived vs active} × {Lesson status} × {report action} |

### 🟠 High Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| Homework copy (previous/next week) crossing an archive boundary | Spec's core risk framing applies verbatim here: "the biggest risk is not LA archive failing — it's a child record that still exists while some read path... keeps showing [something] as active" | Manual check: archive the LA between two adjacent lessons' reports, confirm copy behavior |
| Historical report/homework access after archive | AC-5's own scope note requires archived records stay reachable, not hard-deleted — must confirm Aver doesn't over-correct by hiding history entirely | Manual check: Published report before archive remains viewable + exportable after |
| Ownership gap: fix ticket `[SF][Aver] Check custom aver lesson report` (4h) was scoped before this code trace found the detail page is an *external* Experience Cloud site, not local Apex | A 4h estimate for an in-repo Apex/SOQL fix is very unlikely to cover changes to an external Salesforce org's Experience Cloud site | Flag to the ticket owner before QA sign-off; do not assume the existing ticket's scope covers this |

### 🟡 Medium Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| Unarchive round-trip on Aver Lesson Report | Lower risk since AC-3's same-Id-reuse guarantee is a Core-package behavior already covered elsewhere in this epic; Aver detail page just needs to reflect the restored state without duplicating | Smoke-level regression case |

---

## 6. Coverage Gaps vs. Existing Test Cases

Existing inventory: Qase PX suite 548 "Lesson Report correct" (parent: OOP FEATURES → Aver), 155 cases, fetched directly 2026-10-02. Representative sample reviewed in full (titles + preconditions + steps): #2311, #2313, #2319, #5645–#5665, #5717–#5723, #5764–#5771, #5957, #6009, #6011, #6020 — pattern confirmed across all 155: every precondition set states `Lesson status = <Draft|Canceled|Completed|Published>`; none state or reference `Lesson_Allocation.Archived_At` or `Student_Sessions.Is_Archived`.

| Gap Area | Existing Test Case | Overlap | New Coverage Needed |
|---|---|---|---|
| Add Lesson Report when student's LA is archived, Lesson not Canceled | #5645 "Can not add Lesson Report" (gates on Lesson=Canceled only), #5646 "Can create Lesson Report" (gates on lesson+student assigned, no archive dimension) | None — archive dimension entirely untested | ✅ New TC needed |
| Edit/Delete when student's LA is archived | #2311, #2313, #5651, #5653, #5655, #5656 (all gate on Lesson status / Lesson Report status only) | None | ✅ New TC needed |
| Status transition (Submit/Publish/Revert) when student's LA is archived | #2319, #5657–#5664 (all gate on Lesson status only) | None | ✅ New TC needed |
| Homework copy across an archive boundary | #5667 "Do not show Homework of different LA" (tests cross-LA isolation, not archive state), #5668–#5674, #5717–#5723 | Partial — isolation-by-LA pattern already exists and could extend naturally to archived LA, but is not tested today | ✅ New TC needed |
| Historical report/homework remains viewable + exportable post-archive | #5764 "View Report session on View Lesson Report detail mode", #5767–#5771 (PDF export) | None — these test normal/active state only | ✅ New TC needed |
| Unarchive round-trip, no duplicate report | None in suite 548 | None | ✅ New TC needed |
| Aver list/search `Is_Archived` filter | N/A (out of scope — suite 548 is detail, not list) | Full (fixed in LT-111546, same commit as Core) | Not needed for this suite |

---

## 7. Suggested Test Suite Structure

```
epics/lesson/LT-90306-lesson-allocation-soft-delete/test-cases/
└── oop/
    ├── aver-lesson-report-detail-archive-gap.md → AC-5 (out-of-package, unverifiable-by-code) — Aver Lesson Report
    │     Add/Edit/Delete/Status-transition/Homework-copy/PDF-export behavior when the student's Lesson
    │     Allocation is archived; maps to Qase suite 548 (OOP FEATURES → Aver → Lesson Report correct)
    │     as additive-only new cases.
    └── aso-lesson-survey-archive-gap.md → Gap #10-class (new, code-confirmed) — Aso Lesson Survey Response
          orphaned (never cleaned up) when the enrolling order is cancelled/voided and the student's Lesson
          Allocation archives; maps to Qase suite 331 (OOP FEATURES → Aso → Lesson Survey) as additive-only
          new cases.
```

OOP/tenant-specific test cases for this epic live under `test-cases/oop/`, separate from the Core cases directly in `test-cases/`.

---

## Addendum: OOP/Aso — `Lesson_Survey_Response__c` Orphaning (new gap, code-confirmed)

**Source:** Qase PX suite 331 "Lesson Survey" (OOP FEATURES → Aso, parent 330), 18 existing cases, fetched 2026-10-02. Four cases (#27137, #28915, #28916, #28917) explicitly assert that `Lesson_Survey_Response__c` ("Lesson Survey") records are **hard-deleted** as a side effect when a student is removed from a lesson — via full-order cancel, new-order void, LA end-date reduction, or manual removal.

### Code-trace finding

Direct repo check in `erp-salesforce` (2026-10-02):
- Survey deletion lives in `LessonSurveyHandler.removeRelatedLessonSurveys` (`packages/lesson/main/default/classes/LessonSurveyHandler.cls:167-194`), invoked from `StudentSessionsHandler.removeRelatedLessonSurvey` (`StudentSessionsHandler.cls:2176-2200`, gated by `Lesson_Custom_Settings__c.Delete_Lesson_Survey__c`). It fires only on two `Student_Sessions__c` trigger events: `afterDelete` (record actually deleted, `cls:2165-2170`) or `afterUpdate` when `Lesson__c` transitions non-null→null (`cls:1749`, condition at `cls:2188-2195`).
- **Under the archive flow, neither event ever fires.** `Student_Sessions__c.Is_Archived__c` is a formula — archiving the parent LA writes zero DML to `Student_Sessions__c`, so `Lesson__c` is never nulled and no delete/update trigger runs. Confirmed directly: `LessonAllocationHandler.afterUpdate` explicitly skips archived LAs (`Archived_At__c != null → continue`, `cls:1326-1332`) before reaching the cleanup enqueue, and `ManualSessionCleanupMasterQueueExecutor` filters `WHERE ... Archived_At__c = NULL` (`cls:7`) and `Is_Archived__c = FALSE` (`cls:53`) — once an LA archives, this entire cleanup pipeline (the thing that triggers survey deletion) is bypassed by design.
- `Lesson_Survey_Response__c`'s own fields (`Answer__c`, `Lesson__c`, `Question__c`, `Question_Name__c`, `Response__c`, `Student__c`) carry **no `Is_Archived__c` and no formula** referencing `Archived_At__c` or `Is_Archived__c` on either parent.
- The order-driven paths (cancel full order → `LessonClassMemberHandler.cls:349`) and the manual-removal UI path (`StudentSessionsHandler.cls:586,592`) both funnel through the same `unassignStudentSessionsFromLesson` mechanism (`cls:470-548`) — not a separate, out-of-scope flow.
- **Not affected:** the end-date-reduction path (#27137, `unassignStaleReallocatedSessions` / `ManualSessionCleanupMasterQueueExecutor`) only runs for LAs where `Archived_At__c = NULL` — i.e. it only applies while the LA is still alive (other orders remain), which is exactly the condition under which survey deletion already works correctly today. This path is unaffected by the archive refactor and is not part of this gap.

**Verdict:** confirmed new gap, parallel to spec Gap #10 (`Lesson_Report_Detail__c`, `Lesson_Schedule_Student__c`, `Enrollment__c`, `Zoom_Participant__c`, `Reallocation__c`) but for a previously unlisted OOP/Aso object. When a student's enrolling order is cancelled or voided and their Lesson Allocation group fully archives (AC-1), the associated `Lesson_Survey_Response__c` is **silently orphaned** instead of being cleaned up — it keeps existing, with no archived-state of its own, attached to a lesson the student is no longer actively on.

### Coverage Strategy (addendum)

| AC | Business Rule Summary | Logic Type | Test Technique | Risk Level | Coverage Depth |
|---|---|---|---|---|---|
| AC-1 / Gap #10-class | Cancelling the full order behind a student's sole enrollment archives the LA; the student's `Lesson_Survey_Response__c` is no longer deleted — contrasts with existing case #28916 | Data integrity | Regression / Decision Table | 🔴 Critical | Standard |
| AC-1 / Gap #10-class | Voiding the new order behind a student's sole enrollment archives the LA; the student's `Lesson_Survey_Response__c` is no longer deleted — contrasts with existing case #28917 | Data integrity | Regression / Decision Table | 🔴 Critical | Standard |
| AC-5 (downstream) | Teacher's "all student survey responses" BO list (#1987 baseline) has no `Is_Archived` filter — an orphaned survey for an archived student may still appear as if they were active | Cross-system impact | Negative | 🟠 High | Standard |
| AC-1 (parity) | End-date reduction while the LA stays alive (other orders remain) still deletes the survey normally — control case confirming the gap above is scoped to full-group archival only | Regression | Regression | 🟡 Medium | Smoke |
| AC-3 | Unarchive restores the same LA Id; no second `Lesson_Survey_Response__c` is created for the same (student, lesson) once editing resumes | Regression | Regression | 🟡 Medium | Smoke |

### Gap table (addendum)

| Gap Area | Existing Test Case | Overlap | New Coverage Needed |
|---|---|---|---|
| Survey orphaned when order cancelled, LA archives | #28916 "Auto-removal by cancelling a full order – Survey is deleted" (asserts legacy hard-delete only) | None for the archive-flag-ON path | ✅ New TC needed |
| Survey orphaned when order voided, LA archives | #28917 "Auto-removal by voiding a new order – Survey is deleted" (asserts legacy hard-delete only) | None for the archive-flag-ON path | ✅ New TC needed |
| Orphaned survey visible in Teacher BO list for an archived student | #1987 "Teacher views all student survey responses..." (no archive dimension) | None | ✅ New TC needed |
| End-date reduction (LA stays alive) | #27137 (asserts hard-delete; code-confirmed unaffected by archive) | Full — not impacted, no new TC, included as a control case only | Control case only |
| Unarchive round trip, no duplicate survey | None | None | ✅ New TC needed |

---

## Addendum 2: OOP/Nichibei — Point Consumption Priority Chain & Refund (new gap)

**Source:** Qase PX suite 372 "Point Consumption" (OOP FEATURES → Nichibei, parent 371), two sibling sub-suites exercising identical business logic from two entry points — suite 373 "Lesson detail" (15 cases) and suite 624 "Calendar" (16 cases). This is the area spec.md already flags as the epic's single highest-risk OOP impact: "LA is the financial authorization record... an archived LA must not be selected in the priority chain or have points consumed from it," a release blocker tied to a prior production incident (Lesson-Learned Risk #2, 2026-03-04: sessions ended up with no LA and incorrect point totals).

**Business logic (fully specified by the existing 15/16 cases, used as ground truth):** when a student is assigned to a lesson, the system picks ONE `Lesson_Allocation__c` to deduct points from, in this order: (1) prefer an LA whose course matches the lesson's course over a "general" LA; (2) prefer `Priority__c = TRUE`; (3) LA's duration must cover the lesson date; (4) prefer fewer remaining points (use up smaller allocations first); (5) tie-break on earlier `CreatedDate`. For a recurring lesson split across multiple LAs, each occurrence is evaluated independently and can draw from a different LA. When a student is removed from a lesson, or the lesson is deleted, the consumed points are returned to the same LA they were taken from. None of the 15/16 existing cases reference `Archived_At__c`/`Is_Archived__c` — the archive dimension is entirely new to this selection chain.

**Code-trace note:** the real production selection method for Nichibei (`StudentSessionHandlerOutSide.assignStudentToLesson`, invoked via Apex reflection from `LessonMiddlewareHandler.cls:85`) is not present in `erp-salesforce` — confirmed by an explicit test comment ("StudentSessionHandlerOutSide is not in this package"). The business logic is fully known from the Qase cases regardless; only the archive-filter *implementation* is unverifiable by static code trace, so the cases below are written against the known business logic and marked [UNVERIFIED] only where they depend on seeing the actual selection/refund implementation. One related, simpler fallback query (non-"custom assign" path, `BookingLessonHandlerOutSide.cls:638-651`) already filters `Archived_At__c = NULL` — included as a control case.

**Scope note on the open design question (confirmed with the user 2026-10-02):** spec Clarification Question #2 ("should consumed points for an archived-period session be refunded, held, or left as-is? does unarchive re-consume?") concerns a *forward-looking policy* question — whether archiving itself should trigger a NEW refund/consumption event. **Confirmed out of scope for this coverage pass** — no test case is written against it. The confirmed focus for this suite is narrower and unambiguous: (a) an archived LA must never be *selected* to take points from, under any priority-chain condition, and (b) once an LA is restored (unarchived, same Id), it must work normally again — both for new point-taking assignments and for leaving historical records untouched. The refund-on-normal-removal case (points returned to an LA that happens to have since archived) is also in scope, since it follows directly from AC-3/AC-8's "archive never deletes, never blocks a legitimate write" principle rather than from the open policy question.

### Coverage Strategy (addendum 2)

| AC | Business Rule Summary | Logic Type | Test Technique | Risk Level | Coverage Depth |
|---|---|---|---|---|---|
| AC-5 (financial) | Archived LA must never be selected in the priority chain, even if it would otherwise win on priority/course-match/points — contrasts with baseline #2794/#6779 | Data integrity | Decision Table | 🔴 Critical | Standard |
| AC-5 (financial) | Archived LA's duration still technically covering the lesson date does not make it eligible — archive overrides duration-match | Data integrity | Decision Table | 🔴 Critical | Standard |
| AC-5 (financial) | No non-archived LA available → same "no available LA" error as today, never a silent fallback to an archived LA — contrasts with baseline #2804/#6786/#6792 | Negative | Negative | 🔴 Critical | Standard |
| AC-5 (financial) | Recurring lesson: an LA archives between the first and a later split-assignment action; remaining occurrences re-split using only non-archived LAs — contrasts with baseline #2802/#6784/#8540 | Data integrity | State Transition | 🔴 Critical | Deep |
| AC-3 / AC-8 (financial) | Refund (student removal / lesson deletion) still writes the returned points to the same LA Id even if it has since archived — contrasts with baseline #2806/#2807/#2808/#2811 and Calendar twins | Data integrity | Regression | 🔴 Critical | Standard |
| AC-1 (parity) | Fallback (non-"custom assign") booking path already filters `Archived_At__c = NULL` — control case, not a gap | Data integrity | Regression | 🟡 Medium | Smoke |
| AC-3 | Unarchive does not retroactively re-trigger point consumption for sessions whose points were already recorded before archive | Regression | Regression | 🟡 Medium | Smoke |
| AC-3 (financial) | Restored LA is selectable again in the priority chain for a brand-new assignment — restore must leave no lingering "skip" state | Regression | Regression | 🔴 Critical | Standard |

### Gap table (addendum 2)

| Gap Area | Existing Test Case | Overlap | New Coverage Needed |
|---|---|---|---|
| Archived LA excluded from priority-chain selection | #2794/#6779 "Taking points from LA with specific cases" (no archive dimension) | None | ✅ New TC needed |
| Archived LA with matching duration still excluded | #2798/#6780 "Taking point from LA that has the duration to cover the lesson date" | None | ✅ New TC needed |
| No eligible LA when the only candidate is archived | #2804/#6786, #6492/#6792 "There is no available point/LA to take a point" | None | ✅ New TC needed |
| Recurring split re-evaluated after an LA archives mid-chain | #2802/#6784/#8540 "Taking point from LA for the recurring lesson" | None | ✅ New TC needed |
| Refund lands on the correct, possibly-archived LA | #2806/#2807/#2808/#2811 and suite 624 twins (#6788/#6789/#6790/#6793) | None | ✅ New TC needed |
| Fallback non-custom-assign path | N/A — code-confirmed already filters `Archived_At__c = NULL` | Full | Control case only |
| Unarchive does not re-consume | None | None | ✅ New TC needed |

### Suggested file structure (addendum 2)

```
epics/lesson/LT-90306-lesson-allocation-soft-delete/test-cases/oop/
├── nichibei-point-consumption-lesson-detail-archive-gap.md → maps to Qase suite 373 (Lesson detail entry point)
└── nichibei-point-consumption-calendar-archive-gap.md → maps to Qase suite 624 (Calendar entry point)
```
Both files cover the same business logic (shared selection/refund chain); kept as two files because the two Qase suites are tracked separately, mirroring how the existing 15/16 cases are already duplicated 1:1 across both suites.

---

## Addendum 3: OOP/Nichibei — Contract Page (Mobile) LA Visibility (new gap)

**Source:** Qase PX suite 504 "Lesson Mobile" (OOP FEATURES → Nichibei → Point Consumption, parent 372), 9 existing cases. This is the Learner mobile app's "Contract page," listing a student's Lesson Allocations with purchased slot, end date, remaining points, and product name — almost certainly the same screen spec.md's Gap #10 already flags: "Student App's points-consumption screen calls a generic Salesforce proxy (`/lessonAllocation/v2/getPointsConsumption`) whose Apex endpoint was not found... ownership and archive-filter behavior are unverified."

**Business logic (fully specified by the existing 9 cases):** an LA is hidden from the Contract page if it's inactive and outside the configured date range, if its slots are ≤ 0, or if `requiredAllocation = true`; shown otherwise with purchased slot/end date/remaining points/product name; the list updates live after duration/allocation/slots change; visibility is also scoped per-organization on cross-org account switch (Nichibei vs. Renseikai). None of the 9 cases reference `Archived_At__c`/`Is_Archived__c`.

**Code-trace confirmation:** repeated the search from spec's Gap #10 more broadly (grep across all of `erp-salesforce` packages/outside-packages for `PointsConsumption`, `/lessonAllocation/v2/*`, `ContractPage`, every `@RestResource` endpoint repo-wide, plus `school-portal-admin`'s SF proxy map) — confirmed this screen's backend is not present in either repo. It is unrelated to the different, already-archive-aware `BookingLessonHandlerOutSide.cls:638-651` query (that one picks an LA for a new booking; this one lists LAs for display). **Scope (per the same focus agreed for Addendum 2):** archived LA must not be shown/usable on this screen, and a restored LA must display normally again — no new ground is broken on the separate, still-open refund-policy question.

### Coverage Strategy (addendum 3)

| AC | Business Rule Summary | Logic Type | Test Technique | Risk Level | Coverage Depth |
|---|---|---|---|---|---|
| AC-5 | Archived LA hidden from the Contract page even when every other visibility rule would show it (slots > 0, requiredAllocation = false, within date range) — contrasts with baseline #16005 | Display completeness | Decision Table | 🔴 Critical | Standard |
| AC-5 | Contract page list updates live when an LA archives — a previously visible LA disappears without requiring a fresh login — extends baseline #16009 | Display completeness | Regression | 🟠 High | Standard |
| AC-3 | Unarchive restores the LA's visibility, with purchased slot/end date/remaining points/product name displayed correctly again — inverse of the hide case, extends baseline #16008 | Display completeness | Regression | 🔴 Critical | Standard |
| AC-5 (cross-system) | An archived LA for one student does not leak into the Contract page via a stale cached list when a parent switches away and back between students — extends baseline #29046 | Cross-system impact | Regression | 🟡 Medium | Smoke |

### Gap table (addendum 3)

| Gap Area | Existing Test Case | Overlap | New Coverage Needed |
|---|---|---|---|
| Archived LA hidden despite passing every other visibility rule | #16005 "Display LA when slots are greater than 0" (no archive dimension) | None | ✅ New TC needed |
| Live list update when LA archives | #16009 "The LA list is updated after updating the duration, required allocation and slots" (archive not included as a trigger) | None | ✅ New TC needed |
| Restore reinstates visibility and correct field values | #16008 "Verify contract page displays purchased slot, end date, remaining points, and product name" (assumes LA was never archived) | None | ✅ New TC needed |
| No stale-cache leak across account switch | #29046 "Account Switch – Point Consumption – Nichibei and Renseikai students" (org-boundary only, not archive) | None | ✅ New TC needed |

### Suggested file structure (addendum 3)

```
epics/lesson/LT-90306-lesson-allocation-soft-delete/test-cases/oop/
└── nichibei-contract-page-archive-gap.md → maps to Qase suite 504 (Lesson Mobile / Contract page)
```

---

## Addendum 4: OOP/Nichibei — "Apply to Next X Lessons" Bulk Assign (LT-92191) & Over Assigned Status

**Source:** Qase PX suite 2195 "Assign a student on Calendar SF" (under "Apply specific lesson number when assigning selected lessons onwards", LT-92191, OOP FEATURES → Nichibei → Point Consumption, parent 372), 7 cases. A bulk-assign flow: staff pick a Lesson Allocation first, then assign a student to a lesson chain starting at a selected lesson with "Apply to Next X Lessons" (a specific number, not "all following"). None of the 7 cases reference `Archived_At__c`/`Is_Archived__c`.

**Code-trace findings:**
- The "Select a LA" step reuses the same generic picker already confirmed elsewhere in this epic — `LessonMasterHandler.cls:46`, `WHERE Student__r.RecordTypeId = :contactRecordTypeId AND Archived_At__c = NULL`. **Not a gap** — included below as a control case since it's a different LWC entry point (`splitViewRightManaCalendarMultipleAssign`) worth locking in independently.
- The "existing student not duplicated" check (`StudentSessionsHandler.cls:2373-2385`) already filters `Is_Deleted__c = FALSE AND Is_Archived__c = FALSE` before building its dedup map — an archived-only existing session is correctly treated as "not currently assigned," so a fresh session is created rather than being wrongly skipped. **Not a gap** — included as a control case extending baseline #15533.
- **New finding:** "Lesson Allocation Status = Over Assigned" (`Status__c` formula: `IF(Allocated_Sessions__c > Total_Session_Count__c, Over_Assigned, …)`) compares a roll-up (`Allocated_Sessions__c`, filtered only by `Assigned_Lesson__c = TRUE AND Is_Deleted__c = FALSE` — no `Is_Archived__c` awareness) against `Total_Session_Count__c`. While an LA is archived this is inert (the LA is hidden everywhere else), but **AC-3 requires `Total_Session_Count__c`/`Purchased_Slot_Number__c` to be recomputed from only the living orders at restore time** — if that recomputed total comes back smaller than the actual session count retained through the archive/restore round trip (since archiving never deletes sessions), the LA can surface as "Over Assigned" immediately after restore even though it was never over-assigned before archiving. This is a genuine restore-correctness risk, not covered by any existing case.
- General hiding/restoring of sessions created via this specific bulk-assign LWC also needs its own confirmation, since it's a different code path from the single Add-Student picker already covered (`assign-unassign-student-lesson-schedule.md`).

**Scope:** consistent with the agreed focus — archived LA must not be selectable/usable in this flow, and restore must work normally (including surfacing, not silently absorbing, the Over Assigned edge case above so QA/dev know to check it).

### Coverage Strategy (addendum 4)

| AC | Business Rule Summary | Logic Type | Test Technique | Risk Level | Coverage Depth |
|---|---|---|---|---|---|
| AC-5 (parity) | "Select a LA" step in the bulk-assign flow already excludes archived LA — control case, not a gap | Data integrity | Regression | 🟡 Medium | Smoke |
| AC-5 (parity) | Bulk-assign duplicate check already treats an archived-only existing session as "not assigned" — control case, not a gap | Data integrity | Regression | 🟡 Medium | Smoke |
| AC-5 | Sessions created via this bulk-assign LWC are hidden when the LA archives and reappear correctly on restore — confirms the general formula principle holds for this separate code path | Display completeness | Regression | 🟠 High | Standard |
| AC-3 | Restored LA can surface "Over Assigned" status if the recomputed `Total_Session_Count__c` is smaller than the session count retained through the archive/restore round trip | Data integrity | Decision Table | 🔴 Critical | Standard |

### Gap table (addendum 4)

| Gap Area | Existing Test Case | Overlap | New Coverage Needed |
|---|---|---|---|
| LA picker excludes archived LA (this entry point) | None in suite 2195 | Full (code-confirmed same filter as elsewhere) | Control case only |
| Duplicate-student check vs. archived-only session | #15533 "Verify existing student is not duplicated" (no archive dimension) | Full (code-confirmed already correct) | Control case only |
| Bulk-assigned sessions hidden/restored with LA archive | None | None | ✅ New TC needed |
| Over Assigned status appears incorrectly post-restore | None | None | ✅ New TC needed |

### Suggested file structure (addendum 4)

```
epics/lesson/LT-90306-lesson-allocation-soft-delete/test-cases/oop/
└── nichibei-apply-next-x-lessons-archive-gap.md → maps to Qase suite 2195 (Assign a student on Calendar SF)
```

---

## Addendum 5: OOP/Nichibei — Reallocation (LT-85058) — Orphaned Requests & Unguarded Picker (new gap)

**Source:** Qase PX suite 1274 "SF Reallocation" (21 cases) + suite 1275 "BO Reallocate student" (7 cases), under "Reallocation" (LT-85058, OOP FEATURES → Nichibei, parent 371). This is spec.md's named "Nichibei Reallocation" High-risk OOP impact ("Reallocation requests must ignore archived LA/sessions; must not complete a request against an already-archived record") and directly instantiates spec Business Rule #10's gap list, which already names `Reallocation__c` as an object with "no archived state... not touched by archive." None of the 28 existing cases reference `Archived_At__c`/`Is_Archived__c`.

**Business logic (from the existing cases):** marking an absent student session `Reallocate = TRUE` creates a `Reallocation__c` request, visible in a "Reallocation list." Staff later link it to a new lesson via the "Reallocate Lesson" picker (filtered by location/date range/capacity), creating a linked "Reallocate" Student Session. The Reallocate session/request auto-deletes when the original is unflagged, its attendance reverts, the original student is removed, or the original lesson is deleted — but only while the linked new lesson is Draft/Published/Cancelled; once Completed, the system blocks the change instead. Removing the original also triggers a point refund (shared with the Point Consumption flow already covered in Addendum 2).

**Code-trace confirmation (same architecture as Addendum 1's Lesson Survey finding, confirmed independently):**
- Creation: `StudentSessionsHandler.cls:878` → `ReallocationHandler.createReallocationByStudentSessionId`. Cleanup: `ReallocationHandler.unflagReallocationStudentSession(s)`, `modifyReallocationAfterUnassignSessions`, `updateReallocationAfterRemoveStudentSessions` — **all bound to actual `Student_Sessions__c` DML** (deleted, or `Lesson__c` nulled). `unassignStudentSessionsFromLesson` is the same shared method used by the Point Consumption refund flow (PX-2806/2808, already covered).
- Archiving an LA (`LessonAllocationSyncService.cls:1450-1464`) only updates `Archived_At__c` — zero `Student_Sessions__c`/`Reallocation__c` DML, so none of the cleanup above ever fires. The one job that *does* reconcile Reallocation pairs, `ManualSessionCleanupMasterQueueExecutor`, is explicitly skipped for archived LAs (`LessonAllocationHandler.cls:1327-1329`, `if (Archived_At__c != null) continue;`; `ManualSessionCleanupMasterQueueExecutor.cls:8`, `WHERE ... Archived_At__c = NULL`).
- The "Reallocation list" query itself, `ReallocationHandler.buildReallocationListWithFilterQuery` (`cls:413-474`), has **no** `Is_Archived__c`/`Archived_At__c` filter at all — an open request for an archived student's session stays listed and actionable indefinitely.
- **More severe than the Lesson Survey case:** the "Reallocate Lesson" picker itself (`LessonHandler.getReallocateLessonList`, `cls:481-494`; `ReallocationHandler.updateReallocationBySessionTypeRegular/Reallocate`, `cls:113-164`; `ReallocationRepo.getDetailReallocationByIds`, `cls:6-17`) never checks the request's own `Original_Student_Sessions__r.Lesson_Allocation__r.Archived_At__c` before allowing a new lesson to be linked — unlike every other LA-selection picker already confirmed elsewhere in this epic (`LessonMasterHandler.cls:46`, `BookingLessonHandlerOutSide.cls:638-651`), which DO filter `Archived_At__c = NULL`. Staff can actively complete a reallocation against an archived record, not merely see a stale list entry.

### Coverage Strategy (addendum 5)

| AC | Business Rule Summary | Logic Type | Test Technique | Risk Level | Coverage Depth |
|---|---|---|---|---|---|
| AC-1 / Gap (Business Rule #10) | An open Reallocate request remains listed and actionable after its parent LA archives — the cleanup that would normally remove it (legacy hard-delete path) never fires under archive, a regression vs. AC-7 flag-off parity | Data integrity | Decision Table | 🔴 Critical | Standard |
| AC-5 | "Reallocate Lesson" picker has no archive filter — staff can complete (link a new lesson to) a request whose original session's LA is archived | Data integrity | Negative | 🔴 Critical | Standard |
| AC-1 / Gap | An already-linked (Approved) Reallocate pair is not cleaned up when the LA archives — both original and new sessions orphaned, pair stays "Approved" in the list | Data integrity | Decision Table | 🔴 Critical | Standard |
| AC-3 | Unarchive restores normal Reallocation behavior for a previously-orphaned request — no duplicate request/session created | Regression | Regression | 🟡 Medium | Smoke |

### Gap table (addendum 5)

| Gap Area | Existing Test Case | Overlap | New Coverage Needed |
|---|---|---|---|
| Open request orphaned, stays actionable after archive | #10392/#10406 "Update/Remove ... Reallocate flag" (legacy hard-delete path only) | None | ✅ New TC needed |
| Reallocate Lesson picker completes against archived source | #10393/#10394 "Verify the Reallocate popup" / "User reallocates student to the new lesson" (no archive dimension) | None | ✅ New TC needed |
| Linked (Approved) pair orphaned on archive | #10397-#10403, #10407-#10409 (all legacy hard-delete/status-based cleanup only) | None | ✅ New TC needed |
| Restore resumes normal behavior | None | None | ✅ New TC needed |

### Suggested file structure (addendum 5)

```
epics/lesson/LT-90306-lesson-allocation-soft-delete/test-cases/oop/
├── nichibei-reallocation-sf-archive-gap.md → maps to Qase suite 1274 (SF Reallocation)
└── nichibei-reallocation-bo-archive-gap.md → maps to Qase suite 1275 (BO Reallocate student)
```

---

## Addendum 6: OOP/Nichibei — Table/List-View Sweep (requested check: "does Nichibei reuse Core's archive filter, given how much outside-package code it has?")

**Trigger:** user asked to proactively check Nichibei's tables/list views for the same archived-LA exclusion Core already has, given how much of Nichibei runs on `outside-packages/` custom code (already proven true for Point Consumption's priority chain and the Reallocate Lesson picker, both found unguarded).

**Suites enumerated under Nichibei (parent 371) not yet covered by Addenda 1-5:** `376` Lesson Syllabus (already ruled out of scope — lesson/course metadata, no LA relation), `1276` Trial Lesson → `1411` Trial Student (already ruled out of scope — separate `TrialLessonAllocationHandler`, structurally independent of archive), `2759` "[Nichibei] Lesson Booking System" (LT-96620/LT-104607), `2783` "[Nichibei] Lesson List in BO (Smartphone view)" (LT-96616, 18 cases).

### Finding 1 — Suite 2783: already safe, not a gap

Code trace: the "Smartphone view" is **not** separate Nichibei-only code — it's the same `WrapperTableLessonSF` component responsive at a mobile breakpoint (`school-portal-admin/.../WrapperTableLessonSF.tsx:404`), wiring the identical `DialogsCollectAttendance` dialog already assessed for the desktop entry points (suite 2684, already covered). Its roster query, `Lesson_GetStudentSessionAttendance` (`lesson-student-session.query.graphql:113-121`), already filters `Is_Archived__c: { eq: false }` (line 119) — same as the generic list query. The "Attendance Remark"/"Booking Note" feature (cases 21098-21100) has no separate query either — both the Nichibei-booking write path (`BookingLessonHandlerOutSide.cls:667,716`) and the Mobile-submission write path (`LessonSubmitAttendanceEventHandler.cls:32-37,51-55`) write to the same already-filtered `Student_Sessions__c.Attendance_Response__c` field the roster reads. The Lesson Status filter (Published/Draft/Completed/Cancelled) is a clean, separate concern — it operates on `Lesson__c.Status__c` in an entirely different query, with no interaction with student/LA archive state. "Limit Teacher" is also a generic config flag, not Nichibei-exclusive code. **Verdict: no gap — locking in with a control case.**

### Finding 2 — Suite 2759: cannot be assessed, zero existing coverage

"[Nichibei] Lesson Booking System" (LT-96620/LT-104607) is the suite backing spec.md's named Critical risk ("Booking-candidate selection must only consider non-archived LA... old bookings/sessions must disappear from the Booking List / Collect Attendance"). Confirmed via Qase API: **this suite has 0 existing test cases and no discoverable child suites** ("Booking List", "Lesson Browse", "Book a Lesson", etc. mentioned in its own description don't exist as suites yet). There is no existing baseline to contrast against or extend — writing new cases here would be greenfield test design, not a gap-analysis addendum, and needs its own `/define-test-coverage` pass once the feature's actual business rules are available, not a quick archive-filter check. **Flagged, not actioned in this addendum.**

### Coverage Strategy (addendum 6)

| AC | Business Rule Summary | Logic Type | Test Technique | Risk Level | Coverage Depth |
|---|---|---|---|---|---|
| AC-5 (parity) | Smartphone-view Lesson List's Collect Attendance roster already excludes archived-LA students, including their booking/attendance remark — control case, not a gap | Display completeness | Regression | 🟡 Medium | Smoke |

### Gap table (addendum 6)

| Gap Area | Existing Test Case | Overlap | New Coverage Needed |
|---|---|---|---|
| Smartphone Collect Attendance roster vs. archived LA | #21094/#21101/#21102 (no archive dimension) | Full (code-confirmed already filtered, same component as suite 2684) | Control case only |
| Nichibei Lesson Booking System (named Critical risk) | None — suite has 0 cases | N/A — no baseline exists | Out of scope for this addendum; needs its own coverage pass first |

### Suggested file structure (addendum 6)

```
epics/lesson/LT-90306-lesson-allocation-soft-delete/test-cases/oop/
└── nichibei-lesson-list-smartphone-archive-gap.md → maps to Qase suite 2783 (Lesson List in BO, Smartphone view)
```

---

## Addendum 7: Nichibei Fork-vs-Shared Sweep — Add Student / Calendar / LA List Views (+ one new cross-tenant gap)

**Trigger:** user asked to specifically check whether Nichibei's versions of Core-covered surfaces (Add Student popup, Calendar student list, Lesson Allocation tab list views — "Required Allocation / Not Required Allocation") have been separately verified, given Nichibei's heavy reliance on `outside-packages/` code that sometimes forks from Core (already proven for the Point Consumption priority chain and the Reallocate Lesson picker).

### Findings — all three requested surfaces are SHARED with Core, not forked

1. **Add Student popup:** no Nichibei-specific LWC/Apex fork exists anywhere in `outside-packages/`. The modal (`DialogAddStandardStudentSF.tsx`) is used identically regardless of tenant; its underlying query goes through `/services/apexrest/MANAERP/lessonAllocations/retrieve/v1` → `LessonAllocationHandler.cls:92`, which already filters `Archived_At__c = NULL` — a **second**, previously-unenumerated archive-filtered query (distinct from the `LessonMasterHandler.cls:46` query already confirmed for the bulk-assign flow). No tenant/org branching found anywhere in this path.
2. **Calendar student list:** same shared GraphQL queries as Core (`lesson-student-session.query.graphql:85-139`, `student-session.query.graphql:1-30`), both already filtering `Is_Archived__c: { eq: false }` (and `Archived_At__c: { eq: null }` on the LA side). No tenant conditional found.
3. **Lesson Allocation tab / list views:** repo-wide search for `*.listView-meta.xml` under `Lesson_Allocation__c` returns only the already-confirmed 8 shared views; `outside-packages/` has zero `Lesson_Allocation__c` list-view metadata of its own, and the project has no per-tenant metadata partition (`sfdx-project.json` is a single flat layer) — confirmed no separate "Not Required Allocation" or other Nichibei-only view exists.

**Verdict: no new gap on the three requested surfaces** — all already covered by the existing control cases (`assign-unassign-student-lesson-schedule.md`, `lesson-calendar-display-archive.md`, `lesson-allocation-tab-list-views-archive.md`). Adding a lightweight control case below to explicitly lock in the newly-found second Add-Student query path.

### New finding — "Internal Dashboard" LA reconciliation tool (not Nichibei-exclusive, but surfaced by this sweep)

While tracing the above, a related `outside-packages/dlrs` tool was flagged: `InternalDashboardSearchHandler.cls` (LWC `intDashLessonAllocationSearch.js`), used by ops/support staff to look up an Order Group/Student/SPO/LA Id and diagnose backend-SPO ↔ Salesforce-LA sync gaps (flagging "needs attention" rows: deleted SPO, still processing, never synced). Its two `Lesson_Allocation__c` queries (`resolveByLessonAllocationId:393-397`, `getLessonAllocations:633-653`) have **no `Archived_At__c` filter at all**, even though that field is used for filtering elsewhere in the same file family (`BookingLessonHandlerOutSide.cls:307,570,648,904`) — confirming its absence here is a real gap, not a nonexistent field. Since this tool exists specifically to spot sync anomalies, an archived LA (a deliberate, correct state) could be misread by staff as a genuine "needs attention" sync gap, or mask a real one — a data-integrity/operational risk. This tool is shared `dlrs` infrastructure, not confirmed Nichibei-exclusive, but is included here since it surfaced directly from this sweep.

### Coverage Strategy (addendum 7)

| AC | Business Rule Summary | Logic Type | Test Technique | Risk Level | Coverage Depth |
|---|---|---|---|---|---|
| AC-5 (parity) | Add Student popup's REST-backed query path (`LessonAllocationHandler.cls:92`) already excludes archived LA — control case, locks in a second, previously unenumerated code path | Data integrity | Regression | 🟡 Medium | Smoke |
| AC-5 | Internal Dashboard LA reconciliation search has no archive filter — an archived LA can be misreported as a sync "needs attention" row, or a real gap can hide behind one | Data integrity | Negative | 🟠 High | Standard |

### Gap table (addendum 7)

| Gap Area | Existing Test Case | Overlap | New Coverage Needed |
|---|---|---|---|
| Add Student popup (REST path) vs. archived LA | None naming this specific path (only the LWC-level behavior was covered) | Partial — behavior already locked in, code path now explicitly confirmed | Control case only |
| Calendar student list vs. archived LA | `lesson-calendar-display-archive.md` (already covers this) | Full | None — already covered |
| LA tab "Not Required Allocation" view | N/A — confirmed not to exist | Full (confirmed non-existent) | None |
| Internal Dashboard reconciliation tool vs. archived LA | None | None | ✅ New TC needed |

### Suggested file structure (addendum 7)

```
epics/lesson/LT-90306-lesson-allocation-soft-delete/test-cases/oop/
└── internal-dashboard-la-reconciliation-archive-gap.md → cross-tenant outside-package tool (InternalDashboardSearchHandler.cls), not suite-mapped (no existing Qase suite found for this internal tool)
```

---

## Addendum 8: OOP/Nichibei — "Point Management" (Require_Allocation = False LA list) — unverifiable, no existing coverage

**Trigger:** user identified "Point Management" as Nichibei's counterpart to the Core "Lesson Allocation tab" — the screen that lists Lesson Allocations where `Require_Allocation__c = False` (the point-based/consumable allocations, as opposed to the 8 already-covered `Require_Allocation__c = True` list views).

**Code-trace result: not found anywhere in either repo.** Exhaustive search (grep for "point management"/"Point_Management"/"ポイント管理" across `erp-salesforce` packages/outside-packages and `school-portal-admin`; `find` for any tab/LWC/Visualforce/FlexiPage named with "point"; relaxed search for any `Require_Allocation__c = False` listing query or list view under any name) found nothing. The 8 confirmed `Lesson_Allocation__c` list views are exhaustively `Require_Allocation__c = True` only; no `= False` counterpart exists in source. **Conclusion: this is an org-specific Nichibei customization not checked into either repo** — the same category as Aver's Experience Cloud Lesson Report page and Nichibei's external `StudentSessionHandlerOutSide` priority-chain class (both already confirmed unverifiable-by-code elsewhere in this effort). No existing Qase case or suite references it either.

**Grounding used instead of code:** the fields/business context of `Require_Allocation__c = False` LAs are already well-established from the Point Consumption suites (373/624/504) already covered — Purchase Point, Priority flag, Duration, General-course flag, remaining points — so test cases below are written against that known shape, applying the same AC-5/AC-3 principle already proven for the Required-Allocation counterpart (8 list views), explicitly marked [UNVERIFIED] since no code or existing case confirms actual behavior.

### Coverage Strategy (addendum 8)

| AC | Business Rule Summary | Logic Type | Test Technique | Risk Level | Coverage Depth |
|---|---|---|---|---|---|
| AC-5 | Point Management list excludes an archived LA (Require_Allocation = False), mirroring the already-confirmed-safe Required-Allocation tab | Display completeness | Decision Table | 🟠 High | Standard |
| AC-3 | Point Management list correctly reinstates a restored LA, with its point/priority/duration fields intact | Regression | Regression | 🟡 Medium | Smoke |

### Gap table (addendum 8)

| Gap Area | Existing Test Case | Overlap | New Coverage Needed |
|---|---|---|---|
| Point Management vs. archived LA | None — no code, no Qase case found at all | None | ✅ New TC needed, [UNVERIFIED] |

### Suggested file structure (addendum 8)

```
epics/lesson/LT-90306-lesson-allocation-soft-delete/test-cases/oop/
└── nichibei-point-management-archive-gap.md → no known Qase suite; new area entirely, pending confirmation of its actual tab/page name for import
```

---

## Addendum 9: OOP/Nichibei — Lesson Booking System (LT-96620/LT-104607) — mostly safe, one known external risk

**Source:** Qase "[Nichibei] Lesson Booking System" (parent suite 2759) — previously believed empty (an earlier search for literal sub-suite names "Booking List"/"Lesson Browse" found nothing); now confirmed to actually contain 80 cases across 5 real sub-suites: "My Lessons" (2760, 11), "Lesson Lists" (2761, 21), "Book a Lesson" (2762, 19), "Cancel Booking" (2763, 17), "Cancellation Logging – CM Chatter Notification" (3100, 12). This is the suite backing spec.md's named Critical risk: "Booking-candidate selection must only consider non-archived LA. A student must not be able to book using an archived LA; old bookings/sessions must disappear from the Booking List." None of the 80 cases reference `Archived_At__c`/`Is_Archived__c`.

**Code-trace result — mostly already safe.** All traced in `BookingLessonHandlerOutSide.cls` (`outside-packages/dlrs/main/default/classes/booking-lesson/`):
- **LA selection for booking** (location-match → earliest start → earliest created tiebreak, matching Qase cases #20886-#20889): `reserveLesson()`'s query, `lines 638-651`, already filters `Archived_At__c = NULL` (line 648). Location-matching is a hard equality filter (line 643), not a priority step — non-matching-location LAs are excluded outright before the tiebreak ORDER BY runs.
- **"Active LA" gating** (Browse/Lesson Lists button visibility, cases #20856/#20857/#20860/#21674; mid-flow expiry at Confirmation, case #20893): `getReservationSetting()` (`lines 547-574`, `Archived_At__c = NULL` at line 570) and `getLessonBookingList()` (`lines 296-310`, line 307) both already filter; Confirmation-step re-validation reuses the same `reserveLesson()` query, throwing `NO_LESSON_ALLOCATION` if the LA has since archived.
- **"My Lessons" / Booking List** (cases #20853-#20855, #22992): `getReservationList()` (`lines 487-545`) already filters `Is_Archived__c = FALSE` (line 505) — an old booking under a now-archived LA will not show.
- **Point consumption during booking** (case #20937): rides the exact same external/unverifiable `StudentSessionHandlerOutSide.assignStudentToLesson` path already identified and covered in Addendum 2 (`nichibei-point-consumption-*-archive-gap.md`) — no separate new risk here, just the same already-tracked one reached via a new entry point. Not re-covered with new cases to avoid duplication.

**Scope:** per the user's request, control cases are written for the confirmed-safe paths (archived LA unusable for booking; restore works normally) so they can be manually re-verified on the live Nichibei org. The one already-known external risk (point consumption) is cross-referenced, not duplicated.

### Coverage Strategy (addendum 9)

| AC | Business Rule Summary | Logic Type | Test Technique | Risk Level | Coverage Depth |
|---|---|---|---|---|---|
| AC-5 (parity) | Browse/Reserve-More button hides when the student's only LA archives — control case | Display completeness | Regression | 🟡 Medium | Smoke |
| AC-5 (parity) | LA selection for booking excludes an archived LA even when it would otherwise win on location/date — control case | Data integrity | Regression | 🟡 Medium | Smoke |
| AC-5 (parity) | LA archives between Browse and Confirmation (replaces legacy "LA deleted mid-flow" scenario, case #20893) — booking correctly blocked with the existing error, now via archive instead of delete | Data integrity | Decision Table | 🟠 High | Standard |
| AC-5 / AC-3 (parity) | My Lessons hides a booking once its LA archives, and correctly restores it on unarchive — control case | Display completeness | Regression | 🟡 Medium | Smoke |

### Gap table (addendum 9)

| Gap Area | Existing Test Case | Overlap | New Coverage Needed |
|---|---|---|---|
| Browse button vs. archived-only LA | #20857 "no active LA" (never-created/expired, not archive-specific) | Partial | Control case to explicitly cover the archive trigger |
| LA selection vs. archived LA | #20886-#20889 (no archive dimension) | None | Control case |
| Mid-flow archive at Confirmation | #20893 "LA deleted mid-flow" (legacy wording, pre-dates this epic's archive mechanism) | Partial — same error path, new trigger | ✅ New TC needed (regression-contrast) |
| My Lessons vs. archived booking | #20853-#20855 (no archive dimension) | None | Control case |
| Point consumption during booking | Already covered in Addendum 2 via a different entry point | Full | None — cross-referenced only |

### Suggested file structure (addendum 9)

```
epics/lesson/LT-90306-lesson-allocation-soft-delete/test-cases/oop/
├── nichibei-booking-my-lessons-control.md → maps to Qase suite 2760 (My Lessons)
├── nichibei-booking-la-selection-control.md → maps to Qase suite 2762 (Book a Lesson)
├── nichibei-booking-lesson-lists-cancel-control.md → maps to Qase suites 2761 (Lesson Lists) and 2763 (Cancel Booking)
└── nichibei-booking-cancellation-logging-control.md → maps to Qase suite 3100 (Cancellation Logging – CM Chatter Notification)
```

---

## Addendum 10: OOP/WithUs Juku — Partner REST API (A07/A21) — confirmed instance of spec's already-accepted, un-fixable gap

**Source:** Qase PX suite 561 "Lesson/Course Management & API update" (LT-80592, OOP FEATURES → Withus Juku, parent 555), 9 cases. Two are LA-relevant: "[A07] Get all lesson allocation API" (returns `Lesson_Allocation__c` incl. `Status__c`, `Type__c`, `Lesson_Allocated__c`) and "[A21] Get Class Member API". This is a concrete instance of spec.md's already-documented Missing in Requirements #8: "Partner REST API consumers (WithUs Juku, Kyoiku, Riso UAT, and others) query `Lesson_Allocation__c`/`Student_Sessions__c`/`Class_Member__c` with partner-owned queries that don't filter archived rows. We can only update sample Postman requests and notify partners — cannot force a fix." (Ticket: `[SF] Check Partner REST API / Postman collection` — 4h).

**Code-trace confirmation.** Neither A07 nor A21 corresponds to a Manabie-owned Apex `@RestResource`. The only LA-related Apex REST endpoints in the repo (`LessonAllocationRestAPI.cls` → `/lessonAllocations/v1/*`, `LessonAllocationRestAPITransport.cls` → `/lessonAllocations/retrieve/v1/*`) expose narrow internal-UI actions only, not a flat bulk "get all" export matching A07's field list. No Apex REST resource exists for `Class_Member__c` at all. What does exist is `outside-packages/connections/main/default/connectedApps/Manabie_Open_API.connectedApp-meta.xml` — a Connected App granting generic OAuth `Api` scope via client-credentials flow, consistent with WithUs Juku authenticating once and then issuing its own raw SOQL (`/services/data/vXX.X/query/?q=...`) with a partner-constructed WHERE clause. **There is no Manabie Apex code in between to inject an `Archived_At__c`/`Is_Archived__c` filter — this is structurally unfixable server-side, exactly as spec's existing gap states.**

**Output here is deliberately not a pass/fail test case** (there is no fixable code path for a test to hold accountable) but a verification artifact: the exact current (unfiltered) query result vs. the corrected query WithUs Juku's sample Postman collection should be updated to use, to support the "update sample Postman requests and notify partners" mitigation already named in spec.

### Coverage Strategy (addendum 10)

| AC | Business Rule Summary | Logic Type | Test Technique | Risk Level | Coverage Depth |
|---|---|---|---|---|---|
| AC-5 (out-of-package, confirmed unfixable) | A07/A21 partner queries return archived LA/Class Member rows unless the partner's own query is updated to add the filter | Cross-system impact | Negative | 🟠 High | Smoke |

### Gap table (addendum 10)

| Gap Area | Existing Test Case | Overlap | New Coverage Needed |
|---|---|---|---|
| A07 Get all lesson allocation API vs. archived rows | #5863 (no archive dimension) | None | ✅ Verification artifact needed (not a fixable-code test) |
| A21 Get Class Member API vs. archived rows | #6007 (no archive dimension) | None | ✅ Verification artifact needed (not a fixable-code test) |

### Suggested file structure (addendum 10)

```
epics/lesson/LT-90306-lesson-allocation-soft-delete/test-cases/oop/
└── withus-juku-partner-api-archive-gap.md → maps to Qase suite 561 (Lesson/Course Management & API update); documents current vs. corrected query for the partner-notification mitigation
```

---

## Addendum 11: OOP/WithUs Juku — "Allow Class Member Start In The Past" (LT-107256) — one confirmed Import gap, rest safe

**Source:** Qase "Withus Juku | Allowing past dates for Classmember start date" (LT-107256, parent suite 3303), 23 cases across 4 sub-suites: "Direct Class Assignment" (3304, 8), "Class Member Import" (3305, 2), "Order Group Class Member" (3306, 8), "Class Member History" (3307, 5). Business logic: a custom setting lets staff backdate a `Class_Member__c`'s start date, no earlier than the target LA's own start date, across 3 entry points (Contact/Course, Location Course, LA Student Session) plus Bulk Assign, Import, and order-driven creation. None of the 23 cases reference `Archived_At__c`/`Is_Archived__c`.

**Code-trace confirmation — NOT a WithUs-Juku-specific implementation; it's generic shared code.** All 3 UI entry points share one LWC (`modalAssignClass.js`) calling `LessonClassMemberHandler.advancedClassRegister` (`cls:783-789`), gated by `LessonFeatureToggles.isClassMemberStartInThePastAllowed()`. Findings per suite:
- **Direct Class Assignment (picker-based entry points) — safe.** The Contact/Course picker already excludes archived LAs (`LessonAllocationController.cls:15`), so an archived LA is simply never selectable through the normal UI.
- **Order Group Class Member (Create Order / Add New Course) — safe, AC-3 correctly implemented.** `LessonAllocationSyncService.collectAllocationsToUnarchive` (line 660) + `buildUnarchivedAllocation` (line 1011, `Archived_At__c = null` at 1019) restore the existing LA by the same Id when a living order reappears for the same `Student_Course_ID__c`; `shouldSkipAllocationCreation` (line 880/901) prevents a duplicate LA regardless of archive state.
- **Class Member History (overlap/timeline state transitions) — safe.** Every query feeding the timeline logic already filters `Is_Archived__c = FALSE` (`LessonClassMemberRepo.cls:138-146`; `LessonClassMemberHandler.cls:515-529`) — an archived LA's old Class Members cannot interfere with a new assignment's history calculation.
- **Class Member Import — confirmed new gap.** The shared validator (`ClassMemberValidator.retrieveData`/`validateClassMember`, `LessonClassMemberHandler.cls:73-96`) looks up the target LA with `Archived_At__c = NULL`; if the LA is archived it's simply absent from the result map, and `validateClassMember` **returns early with no error** (line 94-96) instead of blocking the insert. This early-return path skips the date-range check entirely — it was designed to skip validation for a missing/invalid Id, not to explicitly reject an archived one. Since Import works from typed/file-provided references (not the UI picker that excludes archived LAs elsewhere), **a CSV import referencing an archived Lesson Allocation Id could silently create a backdated Class Member against it, with no error shown to the importing staff** — the one path in this feature not protected by the picker-level exclusion that makes every other entry point safe.

### Coverage Strategy (addendum 11)

| AC | Business Rule Summary | Logic Type | Test Technique | Risk Level | Coverage Depth |
|---|---|---|---|---|---|
| AC-5 | Class Member Import referencing an archived LA silently succeeds instead of being rejected | Data integrity | Negative | 🔴 Critical | Standard |
| AC-5 (parity) | Direct Class Assignment picker (Contact/Course entry point) already excludes archived LA — control case | Data integrity | Regression | 🟡 Medium | Smoke |
| AC-3 (parity) | Create Order / Add New Course restores an existing archived LA for the same Student_Course_ID group instead of duplicating — control case | Data integrity | Regression | 🟡 Medium | Smoke |
| AC-5 (parity) | Class Member History timeline calculation already excludes archived LA's old Class Members — control case | Data integrity | Regression | 🟡 Medium | Smoke |

### Gap table (addendum 11)

| Gap Area | Existing Test Case | Overlap | New Coverage Needed |
|---|---|---|---|
| Import vs. archived LA | #26091/#26093 (date-boundary only, no archive dimension) | None | ✅ New TC needed |
| Direct Class Assignment picker vs. archived LA | #26082-#26088/#26119 (no archive dimension) | None | Control case |
| Create Order / Add New Course vs. pre-existing archived LA | #26101-#26108 (assume brand-new LA, no re-enrollment scenario) | None | Control case |
| Class Member History vs. archived LA's old members | #26096-#26100 (no archive dimension) | None | Control case |

### Suggested file structure (addendum 11)

```
epics/lesson/LT-90306-lesson-allocation-soft-delete/test-cases/oop/
├── withus-juku-class-member-import-archive-gap.md → maps to Qase suite 3305 (Class Member Import)
└── withus-juku-class-member-past-date-control.md → maps to Qase suites 3304 (Direct Class Assignment), 3306 (Order Group Class Member), 3307 (Class Member History)
```

---

## Addendum 12: OOP/EEA — Custom Student Session Table (LT-101751) — external, unverifiable (same category as Aver)

**Source:** Qase PX suite 1424 "EEA" (OOP FEATURES → EEA, parent 311), 1 case: "[EEA] OOP | Custom Student Session Table in Lesson Detail" — columns: Student Name, Grade, Type, Attendance Response, Attendance Status, Attendance Reason, Reallocate Flag. This is exactly spec.md's already-ticketed gap: "EEA's custom `Student_Sessions__c` table lives outside the package; package filters don't reach it. Ticket: `[SF][EEA] Check custom Student Session table` — 1d."

**Code-trace result: not found in either repo.** Exhaustive search for "EEA" (case-insensitive) and for the specific column combination ("Attendance Reason" + "Reallocate") across `erp-salesforce` (`outside-packages/` and `outside-packages-ext/`) and `school-portal-admin` found nothing EEA-specific — every hit was a false-positive substring match. The named fields (`Attendance_Reason__c`, `Reallocate_Flag__c`) exist only as standard package fields consumed by standard Core LWCs, not by any EEA-specific component. **Same category as Aver's Lesson Report and Nichibei's priority-chain class: it exists live on EEA's org but is not checked into either repo this workspace has access to.**

### Coverage Strategy (addendum 12)

| AC | Business Rule Summary | Logic Type | Test Technique | Risk Level | Coverage Depth |
|---|---|---|---|---|---|
| AC-5 | EEA's custom Student Session table in Lesson Detail excludes an archived session | Display completeness | Decision Table | 🟠 High | Standard |
| AC-3 | Restore correctly reinstates the row with its fields intact | Regression | Regression | 🟡 Medium | Smoke |

### Suggested file structure (addendum 12)

```
epics/lesson/LT-90306-lesson-allocation-soft-delete/test-cases/oop/
└── eea-custom-student-session-table-archive-gap.md → maps to Qase suite 1424 (EEA)
```

---

## Addendum 13: "Lesson Point Consumption tracking" SF Report — confirmed instance of spec's already-known report-remediation gap

**Source:** Qase "SF Report" > "Lesson Point Consumption tracking" (suite 1090, under "OTHERS", not tenant-specific — a cross-tenant/Core reporting surface), 6 cases. Shows per student: all Lesson Allocations, Course Name, Total Purchased Points, Remaining Points, and per-row Lesson Date + Consumed Points. None of the 6 cases reference `Archived_At__c`/`Is_Archived__c`.

**Code-trace confirmation.** Not custom code — a declarative SF Report Type, `Student_Allocation_Report__c` (`packages/lesson/main/default/reportTypes/Student_Allocation_Report.reportType-meta.xml`, base `Contact` joined to `Lesson_Allocation__r`/`Student_Sessions__r`), with matching reports `Overall_Allocated_Report` and `Monthly_Allocation_Report`. Neither the report type nor either report filters or exposes `Archived_At__c`/`Is_Archived__c` as a column. **This is a specific, concrete instance of spec.md's already-documented Regression Risk #4: "77 Salesforce report types / 1,320 reports... do not filter `Archived_At__c`/`Is_Archived__c`... Not fixable by this epic's code; needs a separate report-remediation pass."**

**Nuance specific to this report:** unlike a headcount/active-enrollment report (where including archived rows inflates counts incorrectly), a *consumption-tracking* report arguably **should** keep showing archived LA's historical consumption per AC-5's "archived records remain reachable via report filter" scope note — the actual risk here is narrower: **archived and active LA rows are visually indistinguishable**, so staff could misread an archived LA's "Remaining Points" as still usable/consumable, when the underlying enrollment is no longer active. The fix (adding an Archived/Status column to the report type) is report metadata work, out of this epic's code scope — same mitigation class as the Partner API gap (Addendum 10): document current behavior + recommend the concrete report-level fix, not a pass/fail code test.

### Coverage Strategy (addendum 13)

| AC | Business Rule Summary | Logic Type | Test Technique | Risk Level | Coverage Depth |
|---|---|---|---|---|---|
| AC-5 (confirmed instance of existing Regression Risk #4) | Report correctly keeps showing archived LA's historical consumption (not a gap) but has no column to distinguish it from active LA rows | Display completeness | Negative | 🟡 Medium | Smoke |

### Suggested file structure (addendum 13)

```
epics/lesson/LT-90306-lesson-allocation-soft-delete/test-cases/oop/
└── lesson-point-consumption-report-archive-gap.md → maps to Qase suite 1090 (SF Report → Lesson Point Consumption tracking); verification artifact, not a fixable-code test (declarative report metadata)
```

---

## Note: Risk Flag Report (suite 2234) — reviewed, no impact

Qase "SF Report" > "Risk Flag Report" (suite 2234, LT-93054), 5 cases — lists students whose Contact-level risk flag is currently `true`. Already established in `student-risk-info-archive.md` (suite 1702) that the underlying Risk Flag/`Risk_History__c` mechanism is structurally independent of `Lesson_Allocation__c`/archive — it's a Contact-level flag with no query or trigger referencing `Archived_At__c`/`Is_Archived__c`. This report just lists that same flag; no new test cases added.

**Follow-up (user requested re-verification of every confirmed-safe path, not just the two already written):** two more already-safe paths from the same code trace had no dedicated control case yet:
- **Lesson Lists / Browse scope** (`getLessonBookingList()`, `cls:296-310`): `locationScopeIds` is derived only from the student's non-archived LAs (`Archived_At__c = NULL`, line 307) — if a student's only LA for a given location archives, lessons at that location should drop out of Browse entirely, not just become unselectable.
- **Cancel Booking refund** (case #20939 "Points refunded to Point LA on cancellation"): the self-service cancel flow's refund rides the same `unassignStudentSessionsFromLesson`-family code already confirmed in Addendum 2 to have no archive guard on the write side — meaning a refund still correctly lands on the target Point LA even if that LA has since archived (AC-8: archive must not block an otherwise-legitimate write). Worth its own control case since it's a different entry point (self-service app cancel, not staff-initiated removal).

**Second-pass deep check (user asked to re-verify this important feature thoroughly for anything missed):** re-reviewed all 80 cases against the archive dimension and traced two more candidate risk areas:
- Duplicate-booking check (case #20890) — **confirmed safe**: `reserveLesson()`'s existing-session subquery (`cls:601-605`) already filters `Is_Archived__c = FALSE`, so a student whose only session on a lesson is archived is correctly treated as not currently booked.
- Lesson capacity/"full" check (cases #20876/#20891) — **confirmed safe**: `isLessonFull()` (`cls:470`) compares against `.size()` of the same already-`Is_Archived__c = FALSE`-filtered subquery, not an unfiltered roll-up — an archived session never occupies a capacity slot.
- **New confirmed gap found while verifying the above:** `getLessonBookingList()` (the Browse list, same method already covered for location scope) has **two different exclusion checks for "already booked"** that disagree with each other. The `isBookedAlready` flag (`cls:289`) correctly filters `Is_Archived__c = FALSE`. But the separate `bookableOnly = true` exclusion filter (`cls:352`, `... MANAERP__Is_Deleted__c = FALSE` — **no `Is_Archived__c` filter**) does not. Reachable directly from the student app's Browse screen (`flutterCommunicate.js:911-921`) whenever the "Bookable Only" toggle is used (case #20871). **Symptom:** a lesson the student should be able to re-book (their old session is archived, `isBookedAlready` correctly reports `false`) is silently excluded from the list entirely when "Bookable Only" is toggled on — inconsistent with every other archive-exclusion check in this file, and a genuine new gap, not a control case.

**Third-pass: Cancellation Logging — CM Chatter Notification (suite 3100, 12 cases), explicitly raised by the user.** Directly addresses spec.md's own named risk for this feature: "Unarchive must not silently recreate a booking or resend a notification." Traced the full call chain:
- The Chatter-post-for-CM and the "last-student-cancels → revert to Draft" logic are BOTH gated behind a single platform event, `MANAERP__Lesson_Platform_Event__e` with `Operation__c = 'CancelLessonBooking'`, published from exactly one place in the entire codebase: `BookingLessonHandlerOutSide.cancelReservedLesson` (`cls:736-815`, publish calls at `:790,801-806`). `LessonPlatformEventSubscriber.trigger` → `LessonPlatformEventHandler.cancelLessonBooking` (`cls:281-342`) does both the Draft-revert (`:317-327`) and the Chatter post (`:329-333`) from that single event.
- Archiving an LA only ever runs `LessonAllocationHandler.afterUpdate`, which explicitly skips archived records before any further processing (`cls:1326-1329`, `if (Archived_At__c != null) continue;`) and never calls `publishCancelLessonEvent`/`cancelLessonBooking` anywhere. **Verdict: structurally impossible for an archive event to spuriously fire either the Chatter post or the Draft-revert** — there is no code path connecting them.
- The Chatter post's `[Student Name]` → LA-record hyperlink (`ChatterPostHandler.createCancelLessonChatterPost:131` → `LessonUtils.buildRecordUrl:388-396`) is a raw Id-based Lightning permalink built from string concatenation, with no SOQL and no `Archived_At__c` filter — it resolves correctly regardless of whether the LA is later archived, consistent with AC-5's "archived records remain reachable by direct Id" scope note.
- **Conclusion: fully safe, no gap.** Control cases below exist for live re-verification per the user's standing request, directly covering the spec's named concern.
