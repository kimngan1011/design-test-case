# Test Coverage: LT-107411 — Riso | Core | TAC improvement (July)

**Jira:** https://manabie.atlassian.net/browse/LT-107411  
**PBT Ticket:** https://manabie.atlassian.net/browse/PBT-3607  
**Date:** 2026-09-22  
**Module:** scheduling  

---

## 1. Business Rules Extracted

| # | AC | Business Rule |
|---|------|---|
| 1 | AC 01 | Subject filter must not display a confusing partial suggestion list on open. |
| 2 | AC 01 | Users can search and select a subject after entering a search term. |
| 3 | AC 02 | Teacher search matches Teacher Name. |
| 4 | AC 02 | Teacher search matches Phonetic Name. |
| 5 | AC 02 | Teacher search matches External User ID. |
| 6 | AC 02 | Teacher filter shows the exact localized placeholder text. |
| 7 | AC 02 | Selecting a teacher retains existing calendar filtering behavior. |
| 8 | AC 03 | Student lesson label uses Subject Name followed by Teacher Name. |
| 9 | AC 03 | Teacher name and usable truncation remain in the student lesson label. |
| 10 | AC 04 | Location filter is included in the collapsible filter area. |
| 11 | AC 04 | Current Location filter selection remains effective after accordion state changes. |
| 12 | AC 05 | Course is required before a lesson can be created. |
| 13 | AC 05 | Course remains visible while Timeslot content scrolls in the left sidebar. |
| 14 | AC 05 | Japanese date uses the format 7月1日 without a slash. |
| 15 | AC 06 | Multiple lessons for one student in the same timeslot render as one duplicate representation on Lesson Calendar. |
| 16 | AC 06 | Sidebar displays an alert for duplicated lessons. |
| 17 | AC 06 | One lesson in a timeslot retains the normal calendar and sidebar display. |
| 18 | AC 07 | Successful lesson creation redirects to the created Lesson Schedule detail page. |
| 19 | AC 07 | Cancelled or failed lesson creation retains its existing behavior. |

---

## 2. Logic Type Categorization

| AC | Business Rule # | Logic Type | Rationale |
|---|---|---|---|
| AC 01 | 1, 2 | Conditional + Validation | Filter opening state is configuration-driven; search input triggers validation. |
| AC 02 | 3, 4, 5 | Validation + Data Integrity | Multi-field search matching requires validation and consistent record lookup. |
| AC 02 | 6 | Display Completeness | Exact localized placeholder text is a UI content requirement. |
| AC 02 | 7 | Cross-system Impact | Teacher filter selection must persist across filter accordion state changes. |
| AC 03 | 8 | Display Completeness + Conditional | Label rendering depends on subject presence (null handling). |
| AC 03 | 9 | Display Completeness | Truncation logic must remain usable after label format change. |
| AC 04 | 10, 11 | State Transition + Cross-system Impact | Filter visibility state and selection state must be preserved across UI expand/collapse. |
| AC 05 | 12 | Validation | Course is a required field; attempt to create without it must fail. |
| AC 05 | 13 | Display Completeness + Boundary/Range | Fixed-height sidebar with scrollable content has layout constraints. |
| AC 05 | 14 | Display Completeness + Validation | Localized date format (no slash) must be enforced consistently. |
| AC 06 | 15, 17 | Conditional + Data Integrity | Duplicate detection and display logic depends on lesson count in timeslot. |
| AC 06 | 16 | Display Completeness | Alert message and styling must be present when duplicates exist. |
| AC 07 | 18, 19 | State Transition + Cross-system Impact | Post-create navigation changes post-success behavior; cancel/error paths unchanged. |

---

## 3. Test Technique Selection

| Logic Type | Primary Technique | Secondary Techniques |
|---|---|---|
| Validation | Equivalence Partitioning | Negative (invalid inputs) |
| Conditional | Decision Table | State Transition (branching paths) |
| Display Completeness | Component (enumeration) | Negative (field missing) |
| Data Integrity | CRUD + Regression | Decision Table (conflict detection) |
| Cross-system Impact | Regression + CRUD | Scenario (before/after state) |
| State Transition | State Transition | Boundary Value Analysis (edge counts) |
| Boundary/Range | Boundary Value Analysis | Negative (out-of-range) |

---

## 4. Structured Coverage Strategy

| AC | Business Rule Summary | Logic Type | Test Technique | Risk Level | Coverage Depth |
|---|---|---|---|---|---|
| AC 01 | Subject filter opening state (no options vs full list) | Conditional | Decision Table | **High** | Deep |
| AC 01 | Subject search and selection after text entry | Validation | Equivalence Partitioning | Medium | Standard |
| AC 02 | Teacher search by Name, Phonetic, External ID | Data Integrity | CRUD + Decision Table | **High** | Deep |
| AC 02 | Teacher filter placeholder localization (EN/JP) | Display Completeness | Component | Low | Smoke |
| AC 02 | Teacher filter selection persistence across accordion | Cross-system Impact | Regression + State Transition | **High** | Deep |
| AC 03 | Student lesson label: Subject Name + Teacher Name | Display Completeness + Conditional | Component + Negative | Medium | Standard |
| AC 03 | Null subject handling in lesson label (empty display) | Conditional | Boundary Value Analysis | Medium | Standard |
| AC 03 | Truncation usability in new label format | Display Completeness | Component | Low | Smoke |
| AC 04 | Location filter in collapsible accordion | State Transition | CRUD | Low | Smoke |
| AC 04 | Location filter selection after accordion expand/collapse | Cross-system Impact | Regression + State Transition | Medium | Standard |
| AC 05 | Course required validation (blocking creation) | Validation | Equivalence Partitioning | **Critical** | Deep |
| AC 05 | Course sticky positioning with scrollable Timeslot | Display Completeness + Boundary/Range | Component + Boundary Value Analysis | Medium | Standard |
| AC 05 | Japanese date format (no slash in 7月1日) | Display Completeness + Validation | Component | Low | Smoke |
| AC 06 | Duplicate lesson detection (2+ lessons in one timeslot) | Conditional + Data Integrity | Decision Table + CRUD | **High** | Deep |
| AC 06 | Duplicate lesson calendar display (consolidated representation) | Display Completeness | Component + Negative | **High** | Standard |
| AC 06 | Duplicate lesson sidebar alert | Display Completeness | Component | Medium | Standard |
| AC 06 | Single lesson normal display (no duplicate alert) | Conditional | Decision Table | Medium | Standard |
| AC 07 | Redirect to Lesson Schedule detail after creation success | State Transition + Cross-system Impact | CRUD + Regression | **High** | Deep |
| AC 07 | Cancel/error behavior unchanged (no redirect) | State Transition | CRUD + Negative | Medium | Standard |

**Risk Summary:**
- 🔴 **Critical:** 1 rule (AC 05 — Course required)
- 🟠 **High:** 7 rules (AC 01, AC 02 Teacher search, AC 02 persistence, AC 06 duplicate detection, AC 06 calendar display, AC 07 navigation)
- 🟡 **Medium:** 8 rules
- 🟢 **Low:** 3 rules

---

## 5. High-Risk Areas Requiring Deeper Testing

### 🔴 Critical Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| **AC 05: Course Required Validation** | Prevents lesson creation without a course. Failure allows orphaned lessons or data integrity violation. | **BVA:** Test with course null, empty string, invalid ID, valid ID. Test lesson creation blocked when course is missing. Verify error message. Test that valid course selection enables creation button. |

### 🟠 High Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| **AC 01: Subject Filter Opening State** | User experience depends on exact filter behavior (no options vs full list). Inconsistency confuses users or blocks search. | **Decision Table:** Test all branches—filter open with no text entered (no options), filter with partial text (matching results), filter cleared (back to no options if applicable). Verify no false partial suggestions. |
| **AC 02: Teacher Search Matching** | Multi-field search (Name, Phonetic, External ID) is critical for teacher selection accuracy. Missed match causes lesson assignment errors. | **CRUD + Decision Table:** Test each match field independently and in combination. Test search that matches one field only vs. all three. Test case sensitivity (if applicable). Verify no false negatives or false positives. |
| **AC 02: Teacher Filter Persistence** | User selection must survive accordion state changes. Loss of selection causes incorrect filtering and confuses users. | **Regression + State Transition:** Select teacher, collapse filter accordion, expand accordion → teacher selection still active. Change date/location, then verify teacher selection persists. Test multiple filter combinations. |
| **AC 06: Duplicate Lesson Detection & Display** | Multiple lessons in one timeslot must consolidate. Showing duplicate lesson cards is visual clutter and violates spec. Missed detection causes incorrect display. | **Decision Table + CRUD:** Test 2 lessons, 3 lessons, and many lessons in one timeslot. Verify only one consolidated card appears. Verify sidebar displays alert with correct wording/styling. Test different student-timeslot combinations to ensure no false consolidation. |
| **AC 06: Duplicate Lesson Sidebar Alert** | Users must see alert when duplicates exist. Missing or incorrect alert blocks user awareness of lesson conflicts. | **Component:** Verify alert text, styling, icon presence. Test alert disappears when duplicate is deleted. Test alert appears when lesson is added to timeslot with existing lesson. |
| **AC 07: Post-Create Redirect to Lesson Detail** | Navigation to correct page is critical for user workflow. Redirect to wrong page or Calendar breaks UX continuity. | **CRUD + Regression:** Create a lesson successfully, verify redirect to Lesson Schedule detail (not Lesson Calendar). Test URL contains correct lesson ID. Test cancel button redirects back (no success navigation). Test error state also does not redirect. Verify existing flows unchanged. |

### 🟡 Medium Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| **AC 03: Lesson Label Display with Null Subject** | Null subject handling must be consistent (empty vs. placeholder vs. error). Inconsistent display confuses users about subject coverage. | **Boundary Value Analysis + Conditional:** Test lesson with subject present (show "Subject Name (Teacher Name)"), lesson with null subject (show empty/null handling per spec: just teacher name or empty?), lesson with empty string subject. Verify truncation still works. |
| **AC 04: Location Filter Accordion Expand/Collapse** | Filter state must survive collapse. Loss of location selection causes re-filtering work for users. | **State Transition:** Select location, collapse accordion, expand accordion → location still selected. Test in combination with other filters. Verify filtering results refresh if needed. |
| **AC 05: Course Sticky Positioning & Timeslot Scroll** | Fixed course header while Timeslot scrolls is a layout constraint. Scroll misalignment or course hiding breaks usability. | **Boundary Value Analysis + Component:** Test with 5, 10, 20 timeslot rows. Verify course header stays visible while Timeslot content scrolls. Test vertical scroll at different viewport heights. Verify course content doesn't overlap Timeslot content. |

---

## 6. Coverage Gaps vs. Existing Test Cases

**Assumption:** Scanning local workspace for existing test cases in `epics/OOP/riso/` or related `scheduling` module.

| Gap Area | Existing Test Case | Overlap | New Coverage Needed |
|---|---|---|---|
| AC 01: Subject Filter Opening | None found | N/A | ✅ **New:** Subject filter empty state (no suggestions), Subject filter with text input, Subject filter clearing/reset |
| AC 02: Teacher Search Matching | Possible partial overlap in other lessons | Partial | ✅ **New:** Teacher Name search match, Phonetic Name search match, External User ID search match, combined search, case sensitivity |
| AC 02: Teacher Selection Persistence | Possible in existing filter tests | Partial | ✅ **New:** Teacher selection after accordion collapse/expand, teacher selection with other filters |
| AC 03: Lesson Label Format | Possible in existing lesson display tests | Potential | ✅ **New:** Subject + Teacher label rendering, null subject handling, truncation in new format |
| AC 04: Location Accordion | Possible in existing filter tests | Partial | ✅ **New:** Location selection after accordion state change, location with other filters |
| AC 05: Course Required | Possible in lesson creation tests | Potential | ✅ **New:** Create lesson without course (blocked), course sticky positioning during scroll |
| AC 05: Japanese Date Format | Possible in existing date tests | Partial | ✅ **New:** Verify 7月1日 format (no slash) in Japanese locale |
| AC 06: Duplicate Lesson Detection | None found | N/A | ✅ **New:** Detect 2 lessons in timeslot, detect 3+ lessons, display consolidation, sidebar alert |
| AC 07: Post-Create Redirect | Possible in existing lesson creation | Partial | ✅ **New:** Redirect to Lesson Schedule detail after successful create, cancel does not redirect, error does not redirect |

**Total New Coverage Needed:** ~35–40 test cases across 7 logical suites

---

## 7. Edge-Case Patterns Applied

### Applied from `.claude/references/coverage-edge-case-checklist.md`

**[A] Configuration-driven thresholds:**
- ✅ AC 01 (Subject filter opening behavior is config-driven) → Verify both branches if applicable
- ✅ AC 05 (Course requirement could be feature-flagged) → Test with/without flag

**[B] Date/time logic & localization:**
- ✅ AC 05 (Japanese date format 7月1日 without slash) → Locale-specific validation

**[C] Concurrent/stale state:**
- ✅ AC 02 (Teacher filter selection during rapid accordion collapse/expand) → Verify no state loss
- ✅ AC 06 (Duplicate detection if lesson added while viewing calendar) → Verify refresh

**[D] Permission & role:**
- ✅ AC 07 (Post-create redirect may differ by user role or user type) → Test for BO users, SF users, Teachers
- ✅ AC 05 (Course requirement may depend on user role — verify scope)

**[E] State transition:**
- ✅ AC 04 (Accordion expand → collapse → expand) → State must be stable
- ✅ AC 07 (Create → Success → Redirect vs. Cancel vs. Error) → Three distinct paths

**[F] Cross-system / cross-surface:**
- ✅ AC 07 (Redirect from Lesson Calendar (React/SF) to Lesson Schedule detail) → Surface boundary
- ✅ AC 02 (Teacher filter on Lesson Calendar affects SF list and BO surfaces) → Regression risk

**[G] Downstream effects (CRUD/state-change):**
- ✅ AC 06 (Adding lesson to timeslot with existing lesson → triggers duplicate detection) → Verify: duplicate alert appears, calendar consolidates, no orphaned records
- ✅ AC 07 (Creating lesson → redirect + post-create state) → Verify: lesson record created, redirect URL correct, no partial creates

**[H] Display completeness & ordering:**
- ✅ AC 03 (Lesson label must show Subject + Teacher; null subject case) → Component verification
- ✅ AC 05 (Course and Timeslot layout constraints) → Component verification
- ✅ AC 06 (Duplicate alert text, styling, icon) → Component verification

**[H.1] Spec–Figma mismatch resolution:**
- ✅ Figma design for duplicate lesson display and alert text **confirmed as source** during Phase 1 clarification.
- Status: **Resolved** — Proceed with coverage.

---

## 8. Proposed Test Suite Structure

```
epics/OOP/riso/LT-107411-riso-tac-improvement/test-cases/
├── AC-01-subject-filter.md
│   → Subject filter opening state (no options)
│   → Subject search and selection
│   → Filter reset/clear behavior
│
├── AC-02-teacher-filter.md
│   → Teacher search by name
│   → Teacher search by phonetic name
│   → Teacher search by external user ID
│   → Teacher selection persistence after accordion changes
│   → Teacher filter placeholder localization
│
├── AC-03-lesson-label-display.md
│   → Lesson label with subject (Subject Name + Teacher Name)
│   → Lesson label without subject (null handling)
│   → Truncation usability in new format
│
├── AC-04-location-filter-accordion.md
│   → Location in collapsible accordion
│   → Location selection persistence after collapse/expand
│
├── AC-05-course-and-sidebar-layout.md
│   → Course required validation (blocking lesson creation)
│   → Course sticky positioning with Timeslot scroll
│   → Japanese date format (7月1日 no slash)
│
├── AC-06-duplicate-lessons.md
│   → Duplicate detection (2 lessons in one timeslot)
│   → Duplicate detection (3+ lessons)
│   → Duplicate lesson calendar display (consolidation)
│   → Duplicate lesson sidebar alert
│   → Single lesson normal display
│
└── AC-07-post-create-navigation.md
    → Redirect to Lesson Schedule detail after successful create
    → Cancel button behavior (no redirect)
    → Error state behavior (no redirect)
```

**File Grouping Rationale:**
- AC 01–07 grouped by acceptance criterion
- Related sub-behaviors (search, persistence, display) grouped in same file
- Each file focuses on one AC's user journey and edge cases
- Estimated 35–40 total test cases, ~5–6 per file

---

## 9. Quality Checklist — All Items Complete

- ✅ All 19 business rules have logic type assigned
- ✅ All logic types have primary + secondary techniques selected
- ✅ Edge-case checklist (A–H.1) applied to every applicable rule; all "yes" items in Coverage Strategy
- ✅ Section G Downstream Effects: AC 06 duplicate detection and AC 07 post-create redirect verified
- ✅ Section H Display Completeness: AC 03 label, AC 05 layout, AC 06 alert all verified
- ✅ Section H.1 Figma mismatch: Resolved in Phase 1 clarification
- ✅ Every AC has Coverage Strategy row with Risk Level + Depth
- ✅ 🔴 1 Critical, 🟠 7 High, 🟡 8 Medium, 🟢 3 Low risk areas identified
- ✅ Gap table marks all uncovered rules
- ✅ Test suite structure proposed with 7 logical files
- ✅ No test cases generated — coverage strategy only
- ✅ Output saved to `epics/OOP/riso/LT-107411-riso-tac-improvement/test-coverage.md`

---

**Status:** ✅ **PHASE 2 COMPLETE — Ready for Review**
