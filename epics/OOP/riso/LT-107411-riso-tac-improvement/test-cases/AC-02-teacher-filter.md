# Test Cases: LT-107411 — Riso | Core | TAC improvement (July)

## Suite: AC-02 — Teacher Filter

### AC 02.1 – Teacher Filter – Search by name returns matches

**Description:** AC 02 — CRUD + Decision Table — Teacher search by Name field returns matching teacher records.

**Preconditions:**
- User role: HQ/CM Staff
- Location: Riso TAC
- Teacher records configured: [{"name": "Tanaka Yuki", "phonetic": "たなかゆき", "external_id": "T001"}, {"name": "Suzuki Hana", "phonetic": "すずきはな", "external_id": "T002"}]
- Teacher filter dropdown opened

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to Riso TAC Teacher filter | Teacher filter control visible | filter_section = "Filters" |
| 2 | Type "Tanaka" in Teacher filter field | Dropdown updates with matching names | search_field = "name", search_term = "Tanaka" |
| 3 | Verify "Tanaka Yuki" appears in dropdown | Teacher name displayed in filtered list | result_contains = "Tanaka Yuki" |
| 4 | Click "Tanaka Yuki" to select | Teacher filter applied; "Tanaka Yuki" shown as selected | selected_teacher = "Tanaka Yuki" |

**Severity:** major
**Priority:** high

---

### AC 02.2 – Teacher Filter – Search by phonetic name matches

**Description:** AC 02 — CRUD + Decision Table — Teacher search by Phonetic Name field returns matching teacher records.

**Preconditions:**
- User role: HQ/CM Staff
- Location: Riso TAC
- Teacher records configured with phonetic names: [{"name": "Tanaka Yuki", "phonetic": "たなかゆき"}]
- Teacher filter dropdown opened
- Locale set to JP (Japanese input method available)

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to Riso TAC Teacher filter | Teacher filter control visible | locale = "JP" |
| 2 | Type "たなか" (phonetic) in Teacher filter field | Dropdown updates with matching phonetic names | search_field = "phonetic", search_term = "たなか" |
| 3 | Verify "Tanaka Yuki (たなかゆき)" appears | Teacher with matching phonetic displayed | result_contains = "Tanaka Yuki" |
| 4 | Click to select | Teacher filter applied | selected_teacher = "Tanaka Yuki" |

**Severity:** major
**Priority:** high

---

### AC 02.3 – Teacher Filter – Search by external ID matches

**Description:** AC 02 — CRUD + Decision Table — Teacher search by External User ID field returns matching teacher records.

**Preconditions:**
- User role: HQ/CM Staff
- Location: Riso TAC
- Teacher records configured: [{"name": "Tanaka Yuki", "external_id": "EMP-2024-001"}]
- Teacher filter dropdown opened

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to Riso TAC Teacher filter | Teacher filter control visible | filter_section = "Filters" |
| 2 | Type "EMP-2024-001" in Teacher filter field | Dropdown updates | search_field = "external_id", search_term = "EMP-2024-001" |
| 3 | Verify "Tanaka Yuki (EMP-2024-001)" appears | Teacher with matching external ID displayed | result_contains = "Tanaka Yuki" |
| 4 | Click to select | Teacher filter applied; external ID shown for reference | selected_teacher = "Tanaka Yuki" |

**Severity:** major
**Priority:** high

---

### AC 02.4 – Teacher Filter – No match for search term

**Description:** AC 02 — CRUD + Decision Table (Negative) — Teacher search returns no results when term does not match any field.

**Preconditions:**
- User role: HQ/CM Staff
- Location: Riso TAC
- Teacher list configured: [{"name": "Tanaka Yuki", "phonetic": "たなかゆき", "external_id": "T001"}]
- Teacher filter dropdown opened

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Type "NonexistentTeacher123" in Teacher filter field | Search processes | search_term = "NonexistentTeacher123" |
| 2 | Verify no results displayed | Empty state or "No matching teachers" message shown | result_list = [] |
| 3 | Clear search term | Filter resets to initial state | clear_action = "backspace_all" |

**Severity:** minor
**Priority:** medium

---

### AC 02.5 – Teacher Filter – Placeholder text in English locale

**Description:** AC 02 — Component — Teacher filter placeholder text displays correct localized text in English.

**Preconditions:**
- User role: HQ/CM Staff
- Location: Riso TAC
- Locale configured: EN (English)
- Teacher filter visible on page

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to Riso TAC in English locale | TAC page loads with EN language settings | locale = "EN" |
| 2 | Locate Teacher filter control | Filter control visible with placeholder text | filter_section = "Filters" |
| 3 | Verify placeholder text matches spec | Placeholder shows localized English text (e.g., "Search by teacher name, phonetic, or ID") | placeholder_text_en = "Search by teacher name, phonetic, or ID" |

**Severity:** trivial
**Priority:** low

---

### AC 02.6 – Teacher Filter – Placeholder text in Japanese locale

**Description:** AC 02 — Component — Teacher filter placeholder text displays correct localized text in Japanese.

**Preconditions:**
- User role: HQ/CM Staff
- Location: Riso TAC
- Locale configured: JP (Japanese)
- Teacher filter visible on page

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to Riso TAC in Japanese locale | TAC page loads with JP language settings | locale = "JP" |
| 2 | Locate Teacher filter control | Filter control visible with Japanese placeholder | filter_section = "Filters" |
| 3 | Verify placeholder text is Japanese | Placeholder shows localized Japanese text (e.g., "教師名、フォネティック、またはIDで検索") | placeholder_text_jp = "教師名、フォネティック、またはIDで検索" |

**Severity:** trivial
**Priority:** low

---

### AC 02.7 – Teacher Filter – Selection persists after accordion collapse and expand

**Description:** AC 02 — Regression + State Transition — Teacher selection retains value when filter accordion is collapsed and re-expanded.

**Preconditions:**
- User role: HQ/CM Staff
- Location: Riso TAC
- Teacher records exist: ["Tanaka Yuki", "Suzuki Hana"]
- Filter accordion is visible (can be collapsed/expanded)
- Teacher "Tanaka Yuki" has been selected and applied

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Select "Tanaka Yuki" in Teacher filter | Teacher filter applied; "Tanaka Yuki" shown as active selection | selected_teacher = "Tanaka Yuki" |
| 2 | Verify calendar shows only lessons for Tanaka Yuki | Calendar filtered by selected teacher | display_state = "filtered_by_tanaka" |
| 3 | Collapse filter accordion (click collapse button) | Accordion collapses; Teacher filter still active (applied to calendar) | accordion_state = "collapsed" |
| 4 | Expand filter accordion again (click expand button) | Accordion expands; "Tanaka Yuki" still selected in Teacher filter field | accordion_state = "expanded" |
| 5 | Verify calendar display unchanged | Calendar still shows lessons for Tanaka Yuki only; no reset | expected_display = "still_filtered_by_tanaka" |

**Severity:** major
**Priority:** high

---

### AC 02.8 – Teacher Filter – Selection persists with other filter changes

**Description:** AC 02 — Regression + State Transition — Teacher selection retains value when other filters (Subject, Location, Date) are changed.

**Preconditions:**
- User role: HQ/CM Staff
- Location: Riso TAC
- Teacher "Tanaka Yuki" selected and applied
- Subject, Location, and Date filters available
- Calendar shows Tanaka Yuki's lessons filtered

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Verify current state: Teacher="Tanaka Yuki", Subject="All", Location="All" | Starting state confirmed | initial_filters = {"teacher": "Tanaka Yuki", "subject": "All"} |
| 2 | Change Subject filter to "Mathematics" | Subject filter applied | new_subject = "Mathematics" |
| 3 | Verify Teacher filter still shows "Tanaka Yuki" | Teacher selection unchanged | teacher_after_subject_change = "Tanaka Yuki" |
| 4 | Change Location filter to "Room A" | Location filter applied | new_location = "Room A" |
| 5 | Verify Teacher filter still shows "Tanaka Yuki" | Teacher selection persists | teacher_after_location_change = "Tanaka Yuki" |
| 6 | Observe calendar | Calendar shows lessons: Tanaka Yuki + Mathematics + Room A (intersection) | expected_display = "all_three_filters_applied" |

**Severity:** major
**Priority:** high

---

## Test Data Dictionary

- `filter_section`: UI section containing filter controls ("Filters", "Advanced Filters", etc.)
- `search_field`: Field being searched (name, phonetic, external_id)
- `search_term`: User-entered text for searching
- `locale`: Language/region setting (EN = English, JP = Japanese)
- `placeholder_text_en`: Localized placeholder in English
- `placeholder_text_jp`: Localized placeholder in Japanese
- `selected_teacher`: Teacher chosen from dropdown
- `accordion_state`: State of filter accordion (collapsed, expanded)
- `initial_filters`: Starting state of all active filters
- `new_subject`: Subject filter value after change
- `new_location`: Location filter value after change
- `expected_display`: Calendar display after all filters applied (intersection)
