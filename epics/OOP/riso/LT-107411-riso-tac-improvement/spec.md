---
ticket_id: LT-107411
ticket_url: https://manabie.atlassian.net/browse/LT-107411
title: "Riso | Core | TAC improvement (July)"
module: scheduling
status: In Analysis
internal_uat_date: null
production_release_date: null
last_updated: 2026-09-22
---

# LT-107411: Riso | Core | TAC improvement (July)

## Summary

This epic improves the Teacher Availability Calendar (TAC) for Riso by enhancing filter behavior, display clarity, and navigation workflow. Changes include: refining the Subject filter opening state to show no options when opened empty, updating lesson labels to display Subject Name (Teacher Name) with safe handling of missing subjects, consolidating duplicate lesson display on the calendar, and redirecting users to the Lesson Schedule detail page after successful lesson creation.

---

## Acceptance Criteria

### AC 01: Subject filter

- The Subject filter does not show a confusing partial suggestion list; it either shows no options until text is entered or the full pull-down list, according to the selected design.
- Users can search and select subjects normally.

### AC 02: Teacher filter

- Teacher search matches Teacher Name, Phonetic Name, and External User ID.
- The English placeholder is Search Teacher Name, External User ID.
- The Japanese placeholder is 講師名、外部IDで検索.
- Existing teacher selection remains compatible.

### AC 03: Student lesson display

- Student lesson labels show Subject Name (Teacher Name) instead of Lesson Name (Teacher Name).
- Teacher name, layout, and truncation remain usable.

### AC 04: Filter accordion

- Location is in the collapsible filter area.
- Collapsing hides Location with the other filters.
- Filtering remains unchanged after expand or collapse.

### AC 05: Left sidebar

- Course is required to create a lesson.
- Course remains fixed while only Timeslot scrolls.
- Japanese date does not include an unnecessary slash, for example 7月1日 rather than 7月/1日.

### AC 06: Duplicate lessons

- When a student has multiple lessons in one timeslot, Lesson Calendar shows a duplicate representation instead of every lesson separately.
- The sidebar displays a duplicate-lesson alert.
- A single lesson still uses the normal display.

### AC 07: Post-create navigation

- After creation, users are redirected to the created Lesson Schedule detail page.
- Users are not redirected to Lesson Calendar.
- Cancel and error behavior remains unchanged.

---

## Business Rules (Extracted)

| # | AC | Business Rule | Field | Field Behavior | Platform |
|---|----|----|---|---|---|
| 1 | AC 01 | Subject filter must not display a confusing partial suggestion list on open. | Subject filter | conditional | SF |
| 2 | AC 01 | Users can search and select a subject after entering a search term. | Subject filter | optional | SF |
| 3 | AC 02 | Teacher search matches Teacher Name. | Teacher filter | searchable | SF |
| 4 | AC 02 | Teacher search matches Phonetic Name. | Teacher filter | searchable | SF |
| 5 | AC 02 | Teacher search matches External User ID. | Teacher filter | searchable | SF |
| 6 | AC 02 | Teacher filter shows the exact localized placeholder text. | Teacher filter placeholder | computed | SF |
| 7 | AC 02 | Selecting a teacher retains existing calendar filtering behavior. | Teacher filter | optional | SF |
| 8 | AC 03 | Student lesson label uses Subject Name followed by Teacher Name. | Student lesson label | computed | SF |
| 9 | AC 03 | Teacher name and usable truncation remain in the student lesson label. | Student lesson label | computed | SF |
| 10 | AC 04 | Location filter is included in the collapsible filter area. | Location filter | conditional | SF |
| 11 | AC 04 | Current Location filter selection remains effective after accordion state changes. | Location filter | optional | SF |
| 12 | AC 05 | Course is required before a lesson can be created. | Course | required | SF |
| 13 | AC 05 | Course remains visible while Timeslot content scrolls in the left sidebar. | Left sidebar | locked | SF |
| 14 | AC 05 | Japanese date uses the format 7月1日 without a slash. | Date display | computed | SF |
| 15 | AC 06 | Multiple lessons for one student in the same timeslot render as one duplicate representation on Lesson Calendar. | Lesson Calendar display | conditional | SF |
| 16 | AC 06 | Sidebar displays an alert for duplicated lessons. | Sidebar alert | conditional | SF |
| 17 | AC 06 | One lesson in a timeslot retains the normal calendar and sidebar display. | Lesson Calendar display | conditional | SF |
| 18 | AC 07 | Successful lesson creation redirects to the created Lesson Schedule detail page. | Post-create navigation | computed | SF |
| 19 | AC 07 | Cancelled or failed lesson creation retains its existing behavior. | Post-create navigation | conditional | SF |

---

## Conflict & Gap Analysis

### Conflicts with Existing System

_None identified._

### Missing in Requirements

#### [MISSING BEHAVIOR] AC 01: Subject filter opening state

**Source:** LT-107415 Acceptance criteria

**Description:** The selected opening behavior is not specified, so the expected empty-state and keyboard behavior cannot be asserted deterministically.

**Resolution:** ✅ **APPROVED** — Show no options when Subject filter is opened empty.

**Positive Assertion:** Opening the filter follows the approved no-options behavior (no partial list implied).

**Negative Assertion:** A partial list that implies only some subjects exist is never shown.

---

#### [MISSING BEHAVIOR] AC 03: Lesson label when Subject is missing

**Source:** knowledge/domain-knowledge/scheduling/partner-rules/riso-lesson-allocation.md — Riso Subject is optional

**Description:** The new label format requires Subject Name (Teacher Name), but the requirement does not define the label when a lesson has no subject.

**Resolution:** ✅ **APPROVED** — Display as null/empty (no subject label shown).

**Positive Assertion:** A lesson with Subject and Teacher displays Subject Name (Teacher Name).

**Negative Assertion:** A lesson without Subject does not render a literal blank, undefined value, or malformed parentheses like "(Teacher Name)".

---

#### [UNDOCUMENTED IN AC] AC 06: Duplicate lesson display

**Source:** LT-107411 Description — updated Figma URL; LT-107420 Acceptance criteria

**Description:** The requirement does not define the visual duplicate representation, sidebar alert text, or behavior for three or more lessons in the same student-timeslot.

**Resolution:** ✅ **APPROVED** — Use Figma design image as reference for duplicate lesson display and alert.

**Positive Assertion:** Duplicate lessons show the approved consolidated representation and alert as per Figma design.

**Negative Assertion:** The calendar does not render individual conflicting lessons as if they were normal independent entries.

---

### Regression Risks

#### [REGRESSION RISK] AC 01: Subject filter change may impact existing filtering

**Source:** epics/OOP/riso/LT-94698-subject-in-lesson-detail/test-coverage.md

**Risk:** Changing the Subject filter opening behavior may regress existing subject search, selection, and calendar result filtering.

**Mitigation:** No-options behavior removes early-filter confusion; search selection remains unchanged. Verify calendar filtering logic after filter selection.

**Test Assertion:** A selected Subject continues to filter the calendar to matching lessons. An unmatched or cleared search does not retain stale subject filtering.

---

#### [REGRESSION RISK] AC 05: Timeslot scrolling may obscure content

**Source:** epics/OOP/riso/LT-98529-lesson-note-timeslot-app/test-coverage.md

**Risk:** Making Course fixed while Timeslot scrolls may obscure the selected Timeslot or render the sidebar incorrectly with long/empty timeslot content.

**Mitigation:** Verify scrolling behavior and layout integrity in test cases.

**Test Assertion:** Course remains visible and the full Timeslot list is reachable by scrolling. Timeslot content does not overlap, disappear, or scroll the fixed Course section away.

---

#### [REGRESSION RISK] AC 07: Post-create navigation affects lesson lifecycle

**Source:** knowledge/e2e-scenario/e2e-scenarios.md § E2E-01

**Risk:** The post-create destination replaces the existing Calendar landing path in the core lesson lifecycle.

**Mitigation:** E2E scenarios and test cases will verify post-create navigation.

**Test Assertion:** A successful creation opens the created Lesson Schedule detail and its identity matches the created record. The flow does not land on Lesson Calendar or leave stale create-form data after success.

---

### Lesson-Learned Risks

**Assessment:** No relevant historical incidents found. All lesson-learned entries were checked; none match the entity-and-operation combination of this Riso calendar UI and navigation epic. Existing Calendar and lesson lifecycle regression paths remain in scope.

---

### E2E Scenario Impact

| Scenario | Title | Impact | Action |
|---|---|---|---|
| E2E-01 | Lesson Lifecycle — Create, Teach, Report, View | Post-create navigation changes the destination after the create step; calendar verification remains a separate explicit step. | UPDATE |

**Action Detail:** Add or update the creation-to-schedule-detail assertion; retain the calendar verification step.

---

### Assumptions Made

- Jira acceptance criteria are the source of truth; Figma design serves as a visual reference only (confirmed by user resolution).
- Teacher filter behavior and Location filter behavior are unchanged and preserved from existing system.
- "Duplicate lessons" refers to multiple lesson records assigned to the same student in the same timeslot.

---

## Clarification Questions

### Status: ✅ ALL RESOLVED

1. **[UNDOCUMENTED IN AC]** — Figma Design Source of Truth
   
   > **Resolution:** Jira ACs are source of truth. Figma design serves as a visual reference only.
   
   _Evidence: LT-107411 Description — updated Figma URL; repository coverage rule H.1 requires a Spec–Figma mismatch review._

2. **[MISSING BEHAVIOR]** — Subject Filter Empty State (AC 01)
   
   > **Resolution:** Show no options when opened empty.
   
   _Evidence: LT-107415 Acceptance criteria — permits no-options or full-list behavior; each produces different keyboard behavior._

3. **[MISSING BEHAVIOR]** — Missing Subject Label (AC 03)
   
   > **Resolution:** Display as null/empty (no subject label shown).
   
   _Evidence: LT-107417 Acceptance criteria requires Subject Name (Teacher Name); knowledge/domain-knowledge/scheduling/partner-rules/riso-lesson-allocation.md — Subject is optional._

4. **[MISSING BEHAVIOR]** — Duplicate Lesson Display (AC 06)
   
   > **Resolution:** Use Figma design image as reference for duplicate lesson display and alert.
   
   _Evidence: LT-107420 Acceptance criteria — requires duplicate representation and alert but does not define visual/text behavior._

---

## Related Specs

- [epics/OOP/riso/LT-94698-subject-in-lesson-detail/spec.md](../../LT-94698-subject-in-lesson-detail/spec.md) — Subject field behavior on lesson details; AC 01 and AC 03 may regress existing subject filtering.
- [epics/OOP/riso/LT-98529-lesson-note-timeslot-app/spec.md](../../LT-98529-lesson-note-timeslot-app/spec.md) — Timeslot display and sidebar layout; AC 05 changes Course/Timeslot scrolling behavior.
- [epics/lesson/LT-107960-duplicate-lesson-duration-validation/spec.md](../../../lesson/LT-107960-duplicate-lesson-duration-validation/spec.md) — Duplicate lesson creation and lifecycle; AC 06 affects calendar display.

---

## Related Test Cases

- [epics/OOP/riso/LT-94698-subject-in-lesson-detail/test-cases/](../../LT-94698-subject-in-lesson-detail/test-cases/) — Subject filtering test cases; verify regression on AC 01 and AC 03.
- [epics/OOP/riso/LT-98529-lesson-note-timeslot-app/test-cases/](../../LT-98529-lesson-note-timeslot-app/test-cases/) — Timeslot and sidebar layout cases; verify scrolling behavior on AC 05.
- [epics/lesson/LT-107960-duplicate-lesson-duration-validation/test-cases/](../../../lesson/LT-107960-duplicate-lesson-duration-validation/test-cases/) — Duplicate lesson creation and validation; verify display consolidation on AC 06.

---

## QASE Coverage Gaps

The following business rules require new test case coverage:

- **AC 01** — Subject filter opening state (no-options behavior) and empty-state keyboard navigation.
- **AC 01** — Subject filter search and selection after text entry.
- **AC 02** — Teacher filter search matching (Name, Phonetic Name, External User ID).
- **AC 02** — Teacher filter placeholder text localization (English and Japanese).
- **AC 03** — Student lesson label format with Subject Name (Teacher Name).
- **AC 03** — Lesson label display when Subject is missing (null/empty behavior).
- **AC 04** — Location filter in accordion; filtering remains unchanged after expand/collapse.
- **AC 05** — Course remains required before lesson creation.
- **AC 05** — Course fixed; Timeslot scrolls in sidebar.
- **AC 05** — Japanese date format (7月1日 without slash).
- **AC 06** — Duplicate lessons consolidated on calendar; sidebar alert.
- **AC 06** — Single lesson retains normal display.
- **AC 07** — Successful creation redirects to Lesson Schedule detail.
- **AC 07** — Cancel and error behavior unchanged.
