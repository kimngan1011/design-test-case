# Test Coverage: LT-102371 — [Riso] OOP | Lesson Window

**Jira:** https://manabie.atlassian.net/browse/LT-102371
**PRD:** https://manabie.atlassian.net/wiki/spaces/PRDM/pages/2604597491
**Date:** 2026-07-14

---

## H.1 — Spec–Figma Mismatch Report

> **⚠️ Figma MCP tool not available in this session.**
> Spec has Figma URL: `https://www.figma.com/design/PQ0TNOtuOiqlvJrYdcHHVG/Lesson-Master-and-Mana-Calendar?node-id=13267-63959`
> Automated frame extraction could not be performed.
>
> **Required manual check before Phase 3:**
> Open the Figma frame and verify the following against spec (AC-01.1, AC-01.2):
> - Lesson Window tab label matches JA: `授業完了期間`
> - Tab list columns: Academic Year, Start Date, End Date, Status, Last Modified Date, Last Modified By
> - Creation form fields: Academic Year (auto-fill), Month (dropdown), Start Date, End Date, Status
> - Delete button visibility (Status=Open only; staff with `full_access_v2` PS only)
> - LLW List View: Location column as clickable link; no Complete/Reopen actions
>
> **Decision:** ⏳ Proceed with coverage strategy (no confirmed spec–Figma 🔴 mismatch known). Confirm visually before UAT.

---

## 1. Business Rules Extracted

| # | AC | Business Rule |
|---|---|---|
| BR-01 | AC-02 | No two LLW records for same Location + Academic Year may have overlapping date ranges. Trigger on before-insert/before-update. Error: "A Lesson Window already exists for this location and period." |
| BR-02 | AC-09, AC-12 | `Lesson_Date__c` on creation or update blocked if it falls within `Start_Date__c`–`End_Date__c` of any LLW with **Status = Complete** for the **same location AND same Academic Year**. A Complete LLW for a different Academic Year does NOT block. Fires on `Lesson__c` before-insert/before-update. |
| BR-03 | AC-06, AC-07 | CM can set Complete → Open only if LLW's month = current or immediately preceding calendar month. Older months cannot be reopened by CM. |
| BR-04 | AC-01.1 | Audit trail via SF standard system fields: `CreatedById`, `CreatedDate`, `LastModifiedById`, `LastModifiedDate`. No custom fields required. |
| BR-05 | AC-03 | LBAC — record level: OWD = Private. CM can only see/manage LLW records for own assigned location(s). HQ/Admin see all. |
| BR-06 | AC-12 | Same LLW validation (BR-02) fires when `Lesson_Date__c` is changed on an existing lesson (edit form or DnD). |
| BR-07 | AC-04 | Complete action can be set at any time. No date or content validation required at completion (v1). |
| BR-09 | AC-05 | LLW can only be deleted if Status = **Open** AND no linked detail records exist. Salesforce standard data dependency behavior applies. |
| BR-10 | AC-02 | Uniqueness scoped per Location + Academic Year. Same date range is allowed for same location under a **different academic year** without conflict. |
| BR-11a | AC-01.1 | Month dropdown defaults to current month. Academic Year mandatory, defaults to current. If AY cleared → Month, Start Date, End Date **disabled**. When Month selected → Start Date and End Date auto-populate from AY calendar range. Manual override allowed. |
| BR-11b | AC-20 | LLW fields (AY, Month, Start Date, End Date) editable only when Status = Open. Status = Complete → record is read-only (except via Reopen action). Academic Year always read-only on edit. |
| BR-CRUD | AC-01.1, AC-03, AC-05, AC-08 | Create: all staff. Read: all staff. Update: all staff (CM with BR-03 reopen restriction). Delete: **staff with `full_access_v2` PS only**. BO Teacher: no access. All subject to LBAC (object + record level). |

---

## 2. Logic Type Categorization

| AC / BR | Logic Type(s) |
|---|---|
| BR-01, BR-10, AC-02 | Data integrity, Validation logic |
| BR-02, BR-06, AC-09, AC-10, AC-12 | Conditional logic, Cross-system impact, Boundary/range |
| BR-03, AC-06, AC-07 | Boundary/range, State transition, Permission logic |
| BR-04, AC-01.1 (audit) | Display completeness |
| BR-05, BR-CRUD, AC-03 | Permission logic |
| BR-07, AC-04 | State transition |
| BR-09, AC-05 | State transition, Conditional logic, Permission logic |
| BR-11a, AC-01.1 | Conditional logic, Display completeness, Validation logic |
| BR-11b, AC-20 | State transition, Conditional logic |
| AC-01.1 (tab + form) | Display completeness, CRUD |
| AC-01.2 | CRUD, Data integrity, Display completeness |
| AC-08 | State transition, Permission logic |
| AC-11 | Conditional logic |
| AC-13 | State transition |
| AC-21 | State transition |
| AC-14–AC-19 | Cross-system impact |

---

## 3. Test Technique Selection

| Logic Type | Primary Technique | Secondary Technique |
|---|---|---|
| Validation logic | Equivalence Partitioning | Negative |
| Boundary/range | Boundary Value Analysis | Negative |
| Conditional logic | Decision Table | Negative |
| State transition | State Transition | CRUD |
| Permission logic | Permission Matrix | Decision Table |
| Data integrity | CRUD | Regression |
| Cross-system impact | Regression | CRUD |
| Display completeness | Component | Negative (field absent) |

---

## 4. Edge-Case Checklist (Step 4.5)

### A. Configuration-driven thresholds
- [x] BR-03 reopen restriction (1-month window for CM): **BVA at boundary** — current month (allowed), preceding month (allowed), 2 months ago (blocked)
- [N/A] No capacity/numeric config thresholds in this feature

### B. Date / Time logic
- [x] BR-02: Lesson date = first day of LLW Start_Date (boundary inclusive) → blocked
- [x] BR-02: Lesson date = last day of LLW End_Date (boundary inclusive) → blocked
- [x] BR-02: Lesson date = day before Start_Date → allowed
- [x] BR-02: Lesson date = day after End_Date → allowed
- [x] BR-11a: Month auto-populate — verify correct start/end dates for each month in the Academic Year
- [x] BR-03: "Current month" vs "preceding month" at month boundary — test on the 1st of a new month
- [N/A] DST — JST does not observe DST (N/A for Riso)

### C. Concurrent / stale state
- [x] Stale UI: CM loads Account page (LLW=Open), HQ marks Complete in another tab → CM tries to create lesson → must be blocked (backend validation, not UI)
- [x] Double-submit: Rapid double-click on "Complete" button → only one Complete record created, no duplicate status flip
- [N/A] Multi-seat booking (not applicable to LLW)

### D. Permission & role
- [x] Every role tested for LLW CRUD: Admin, HQ Admin, CM, BO Teacher (no access)
- [x] CM cross-location: CM at Location A cannot see/manage LLW for Location B
- [x] Feature flag: Riso org only — no impact to other partner orgs

### E. State transition
- [x] Open → Complete: positive test (any user)
- [x] Complete → Open (CM, current month): positive test
- [x] Complete → Open (CM, preceding month): positive test
- [x] Complete → Open (CM, 2+ months ago): negative test (blocked)
- [x] Complete → Open (HQ/Admin, any month): positive test
- [x] Create (Status=Open default): positive test
- [N/A] No "Draft" state, no "Cancelled" state in LLW

### F. Cross-system / cross-surface
- [x] LLW Complete → Lesson creation blocked on SF Lesson List
- [x] LLW Complete → Lesson creation blocked on Lesson Schedule detail
- [x] LLW Complete → Lesson creation blocked on SF Calendar (create + DnD)
- [x] LLW Complete → Lesson creation blocked via CSV import
- [x] LLW Complete → Lesson creation blocked for Recurring lesson
- [x] LLW Reopen → Lesson creation immediately unblocked on all surfaces
- [x] LLW Complete → Lesson date update (edit form) blocked
- [x] ACI closed-date validation vs LLW validation: both active on same date → LLW shows error, ACI silently skips (no conflict per clarification)

### G. Downstream Effects Inventory

| Primary Action | Downstream Effect | Affected Surface | TC Owner |
|---|---|---|---|
| LLW Status → Complete | Lesson creation blocked for this location within date range (all 5 creation paths) | SF Lesson creation forms, Triggers | llw-lesson-validation.md |
| LLW Status → Complete | Lesson date update blocked (edit form + DnD) | SF Lesson edit, SF Calendar DnD | llw-lesson-validation.md |
| LLW Status → Open (Reopen) | Lesson creation immediately unblocked (no cache) | All lesson creation paths | llw-lesson-validation.md |
| LLW dates edited + Status → Complete | New date range scope blocks lessons in new range | Lesson__c trigger | llw-create-manage.md |
| LLW Created | Record visible in Lesson Window tab on Account detail page | Account detail page | llw-create-manage.md |
| LLW Created | Record visible in LLW List View | LLW List View | llw-create-manage.md |
| LLW Deleted (Status=Open) | Location period no longer blocked | Lesson creation for that period now allowed | llw-create-manage.md |
| Overlap LLW creation attempted | Error message displayed; no record created | LLW creation form | llw-create-manage.md |

### H. Display & Ordering Inventory

| Screen / Component | Required Fields | Conditional Fields | Sort Rule | Tooltip / Text to Assert |
|---|---|---|---|---|
| Lesson Window tab (Account page — Path A) | Academic Year, Start Date, End Date, Status, Last Modified Date, Last Modified By | Delete button (visible: Status=Open, **staff with `full_access_v2` PS** only; hidden: Status=Complete or CM without PS) | Not defined in spec | "A Lesson Window already exists for this location and period." (overlap) / "この期間のレコードは既に存在します。" |
| LLW creation form | Academic Year (auto-fill=current), Month (dropdown, default=current), Start Date (auto-populate), End Date (auto-populate), Status (Open default), Location (auto-fill, non-editable) | Month + Start Date + End Date disabled when Academic Year cleared | None | None |
| LLW List View (Path B) | Location (clickable link), Academic Year, Start Date, End Date, Status | No Complete/Reopen actions in List View | Not defined in spec | None |
| Lesson creation error | Error message inline or system error | Shown only when lesson date in Complete LLW range | N/A | EN: "Selected lesson date is already closed." · JA: "選択された授業期間は既に完了済です" |
| CM Reopen blocked error | Error message | Shown only when CM tries to reopen LLW older than 1 month | N/A | EN: "This window can no longer be reopened. Please contact HQ." · JA: "未完了状態に戻すことはできません。本部に連絡してください。" |

---

## 5. Structured Coverage Strategy

| AC | Business Rule Summary | Logic Type | Test Technique | Risk Level | Coverage Depth |
|---|---|---|---|---|---|
| AC-01.1 | Lesson Window tab exists on Account detail page; displays required columns | Display completeness | Component | Medium | Standard |
| AC-01.1 | New button: auto-fill AY=current, Status=Open, Location=current (non-editable) | Display completeness, Validation | Component, Negative | Medium | Standard |
| AC-01.1 | Month dropdown defaults to current month; selecting Month auto-populates Start/End Date from AY calendar | Conditional logic | Decision Table | Medium | Standard |
| AC-01.1 | Manual override of Start/End Date after auto-population works | Conditional logic | Negative | Medium | Standard |
| AC-01.1 | If Academic Year cleared → Month, Start Date, End Date disabled | Conditional logic | Decision Table | Medium | Standard |
| AC-01.1 | Delete button visible only when Status=Open; hidden when Status=Complete | Conditional logic, State transition | Decision Table | High | Standard |
| AC-01.1 | Delete button only visible/accessible to **staff with `full_access_v2` PS**; hidden for CM without this PS | Permission logic | Permission Matrix | High | Standard |
| AC-01.1 | Audit trail fields (Created Date, Last Modified Date, Last Modified By) auto-populated | Display completeness | Component | Low | Smoke |
| AC-01.2 | LLW List View: New button with multi-select Location field | CRUD | CRUD | Medium | Standard |
| AC-01.2 | Multi-location creation: overlap in one location → skip that location, create for rest | Data integrity | CRUD, Negative | Medium | Standard |
| AC-01.2 | Location column in List View renders as clickable link | Display completeness | Component | Medium | Smoke |
| AC-01.2 | List View: no Complete or Reopen actions available | Display completeness | Component | Medium | Smoke |
| AC-02 | Create LLW with overlapping date range for same Location + Academic Year → blocked with EN error | Validation logic, Data integrity | Equivalence Partitioning, Negative | Critical | Deep |
| AC-02 | Create LLW with overlapping date range → error message in JA | Validation logic | Negative | Medium | Standard |
| AC-02 | Create LLW with non-overlapping date range for same Location + AY → allowed | Validation logic | Equivalence Partitioning | High | Standard |
| BR-10 | Create LLW with same date range for same Location under **different AY** → allowed (no conflict) | Data integrity | CRUD | High | Standard |
| AC-03 | CM can only view LLW records for own location(s) | Permission logic | Permission Matrix | High | Deep |
| AC-03 | CM cannot access/create LLW for a location they are not assigned to | Permission logic | Permission Matrix | High | Deep |
| AC-03 | HQ/Admin can see all LLW records across all locations | Permission logic | Permission Matrix | High | Standard |
| BR-CRUD | BO Teacher has no access to LLW object (cannot see, create, or interact) | Permission logic | Permission Matrix | High | Standard |
| AC-04 | Admin/HQ/CM can set LLW to Complete at any point (no date or content validation) | State transition | State Transition | High | Standard |
| AC-05 | Delete only available when Status=Open; button hidden/disabled when Complete | State transition, Conditional logic | State Transition, Negative | High | Standard |
| AC-05 | Delete blocked when LLW has linked detail records (Salesforce standard) | Data integrity | CRUD | Medium | Standard |
| AC-05 | Delete only for **staff with `full_access_v2` PS**; CM without this PS cannot delete | Permission logic | Permission Matrix | High | Standard |
| AC-06 | CM can reopen LLW whose month = **current calendar month** → Status=Open | State transition, Boundary/range | State Transition, BVA | Critical | Deep |
| AC-06 | CM can reopen LLW whose month = **immediately preceding calendar month** → Status=Open | State transition, Boundary/range | State Transition, BVA | Critical | Deep |
| AC-06 | Lesson creation in that date range is immediately unblocked after CM reopen (no cache) | State transition | State Transition | Critical | Standard |
| AC-07 | CM tries to reopen LLW whose month is **2+ months ago** → blocked with EN error | State transition, Boundary/range | BVA, Negative | Critical | Deep |
| AC-07 | CM reopen blocked → correct JA error message shown | Display completeness | Component | Medium | Standard |
| AC-08 | HQ/Admin can reopen **any** Complete LLW regardless of month age → success | State transition, Permission logic | State Transition, Permission Matrix | High | Standard |
| AC-09 | Lesson creation on **SF Lesson List** with date in Complete LLW → blocked | Conditional logic | Decision Table, Negative | Critical | Deep |
| AC-09 | Lesson creation on **Lesson Schedule detail page** with date in Complete LLW → blocked | Conditional logic | Decision Table, Negative | Critical | Deep |
| AC-09 | Lesson creation on **SF Calendar** with date in Complete LLW → blocked | Cross-system impact | Regression, Negative | Critical | Deep |
| AC-09 | Lesson creation via **Lesson Schedule CSV import** with date in Complete LLW → blocked | Cross-system impact | Regression, Negative | Critical | Deep |
| AC-09 | **Recurring lesson creation** where date in Complete LLW → blocked | Conditional logic | Decision Table, Negative | Critical | Deep |
| AC-09 | Lesson date = **first day** of Complete LLW Start_Date (inclusive BVA) → blocked | Boundary/range | BVA | Critical | Deep |
| AC-09 | Lesson date = **last day** of Complete LLW End_Date (inclusive BVA) → blocked | Boundary/range | BVA | Critical | Deep |
| AC-09 | Lesson date = **day before** Start_Date → allowed | Boundary/range | BVA | Critical | Deep |
| AC-09 | Lesson date = **day after** End_Date → allowed | Boundary/range | BVA | Critical | Deep |
| AC-09 | Lesson date NOT in any Complete LLW for same location → creation succeeds | Conditional logic | Equivalence Partitioning | High | Standard |
| AC-10 | EN error message shown: "Selected lesson date is already closed." | Display completeness | Component | High | Standard |
| AC-10 | JA error message shown: "選択された授業期間は既に完了済です" | Display completeness | Component | Medium | Standard |
| AC-11 | Lesson non-date fields (teacher, time, etc.) can still be edited when lesson date is in Complete LLW range | Conditional logic | Decision Table | Medium | Standard |
| AC-12 | Edit lesson date via **edit form** to date in Complete LLW → update blocked with same error | Conditional logic, Cross-system | Regression, Negative | Critical | Deep |
| AC-12 | **DnD** lesson on SF Calendar to date in Complete LLW → move blocked with error | Cross-system impact | Regression, Negative | Critical | Deep |
| AC-12 | Edit lesson date from Complete LLW range to a date in **Open LLW range** → allowed | Conditional logic | Equivalence Partitioning | High | Standard |
| AC-13 | Reopen LLW → lesson creation in that date range immediately unblocked (test on all creation paths, at least 1) | State transition | State Transition | Critical | Standard |
| AC-14, AC-15 | GET API returns all required fields: Location ID, Name, AY, Start Date, End Date, Status, Last Modified Date, Last Modified By | Cross-system impact | CRUD | Medium | Standard |
| AC-19 | GET API supports nightly batch call (response time acceptable, no rate limit error) | Cross-system impact | Regression | Medium | Smoke |
| AC-20 | Edit LLW when Status=Open → edits to Start Date, End Date, Month, Status succeed | State transition | State Transition | High | Standard |
| AC-20 | Edit LLW when Status=Complete → all fields read-only (cannot edit) | State transition | State Transition, Negative | High | Standard |
| AC-20 | Academic Year field is read-only on edit (even when Status=Open) | Conditional logic | Negative | Medium | Standard |
| AC-20 | Overlap validation fires on edit save | Data integrity | CRUD, Negative | High | Standard |
| AC-21 | Edit Start/End Date, then mark Complete → new date range locks lessons in new scope | State transition | State Transition | High | Standard |
| BR-11a | Month auto-populates Start Date = first day, End Date = last day of selected month for the AY | Conditional logic | Decision Table | Medium | Standard |
| BR-11a | Manual override of auto-populated Start/End Date persists on save | Validation logic | CRUD | Medium | Standard |
| LLW+ACI | LLW validation (error) and ACI validation (silent skip) coexist on same lesson date — no simultaneous error conflict | Cross-system impact | Regression | High | Standard |

---

## 6. High-Risk Areas

### 🔴 Critical Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| BR-02 / AC-09: Lesson creation block (all 5 paths) | Core enforcement mechanism. If any path bypasses LLW validation, Riso's monthly closing process is worthless. Data integrity for timesheet calculations is compromised. | Deep: test every creation path independently. BVA on Start_Date and End_Date boundaries. |
| BR-06 / AC-12: Lesson date update block (edit form + DnD) | Lesson date change via edit or DnD is equally dangerous if not blocked. Bypass = CM can silently re-date existing lessons into closed periods. | Deep: test both edit form path and DnD path explicitly. |
| BR-03 / AC-06 / AC-07: CM reopen restriction — month boundary | If the month comparison fails (off-by-one or timezone issue at month start/end), CM could reopen windows they shouldn't. | BVA: test on last day of preceding month, first day of current month, 2+ months ago. |
| AC-13: Immediate unblock after Reopen | If unblocking is delayed or cached, CM may be incorrectly blocked from creating lessons after Reopen, creating support incidents. | Test immediately after Reopen (no delay). |

### 🟠 High Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| BR-01 / AC-02: Uniqueness at trigger level (NFR-03) | Uniqueness must be enforced at Apex trigger, not just UI. If only UI-side validation, concurrent requests or API calls could insert duplicates. | Test overlapping date range creation via API as well as UI. |
| BR-05 / AC-03: LBAC record-level (Sharing_Setting__c) | If OWD or Sharing_Setting__c config is misconfigured for the new object, CM at Location A can see LLW of Location B. Data privacy breach. | Test CM at Location A cannot access any LLW endpoint/view for Location B. |
| AC-04 / AC-07: State transitions (Complete, Reopen) | State machine is the core of the feature. Any invalid transition leaves LLW in an inconsistent state. | State transition diagram: all documented transitions positive; all undocumented transitions negative. |
| BR-CRUD / AC-03: CM cannot delete | CM delete is explicitly prohibited (PRD). If UI accidentally shows Delete to CM, it's a permission defect. | Permission Matrix: verify Delete button absent for CM in both Account page tab and List View. |

### 🟡 Medium Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| BR-11a: Month auto-populate from Academic Year | Incorrect month-to-date mapping (e.g., wrong year boundary for AY April–March) causes incorrect Start/End dates. | Decision Table: test each month for a non-standard AY (April–March). |
| AC-01.2: Path B multi-location creation + skip on overlap | Partial creation (some locations succeed, some skip) could leave inconsistent state if save is not transactional. | Test with 3 locations: 1 overlaps, 2 valid → verify exactly 2 created, 1 skipped. |
| AC-14/AC-15: GET API response fields | Missing fields in API response breaks Riso's nightly batch. | Component test asserting all 8 fields present for each record. |

---

## 7. Coverage Gaps vs. Existing Test Cases

| Gap Area | Existing Test Case | Overlap | New Coverage Needed |
|---|---|---|---|
| LLW object CRUD | None (new object) | None | ✅ All: Create (Path A & B), Uniqueness, Edit, Delete, Complete, Reopen, LBAC |
| Lesson creation blocking by LLW | None | None | ✅ All 5 paths + DnD + edit form |
| LLW state transitions | None | None | ✅ Open→Complete, Complete→Open (CM/HQ), restrictions |
| GET API | None | None | ✅ Response fields, nightly call |
| LLW + existing lesson flows (regression) | `LT-98532` bulk-publish test cases | Low overlap (bulk-publish tests create lessons; LLW could block if date overlaps) | ✅ Add LLW-awareness note to LT-98532 preconditions (ensure no Complete LLW covers bulk-publish test dates) |
| LLW + ACI validation coexistence | None | None | ✅ 1 regression test: same lesson date hits both validations; verify LLW error shown, ACI silent |

---

## 8. Suggested Test Suite Structure

```
epics/OOP/riso/LT-102371-lesson-window/test-cases/
├── llw-create-manage.md
│     AC-01.1, AC-01.2, AC-02, AC-03, AC-04, AC-05, AC-20, AC-21
│     BR-01, BR-05, BR-07, BR-09, BR-10, BR-11a, BR-11b, BR-CRUD
│     → LLW creation (Path A & B), uniqueness, edit, delete, Complete action, LBAC
│
├── llw-reopen.md
│     AC-06, AC-07, AC-08
│     BR-03
│     → Reopen operation: CM restrictions (current + preceding month), HQ unrestricted, error messages
│
├── llw-lesson-validation.md
│     AC-09, AC-10, AC-11, AC-12, AC-13
│     BR-02, BR-06
│     → Lesson creation/update blocking across all 5 paths + DnD + edit form; BVA on date boundaries
│
└── llw-get-api.md
      AC-14, AC-15, AC-18, AC-19
      → GET API response content; nightly batch support
```

**Estimated test case count:** 60–70 TCs total
- `llw-create-manage.md`: ~25 TCs
- `llw-reopen.md`: ~12 TCs
- `llw-lesson-validation.md`: ~25 TCs
- `llw-get-api.md`: ~5 TCs
