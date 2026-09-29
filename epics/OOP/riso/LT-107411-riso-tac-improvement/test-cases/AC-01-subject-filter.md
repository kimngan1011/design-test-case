# Test Cases: LT-107411 — Riso | Core | TAC improvement (July)

## Suite: AC-01 — Subject Filter

### AC 01.1 – Subject Filter – No options displayed on open

**Description:** AC 01 — Decision Table — Subject filter shows no confusing partial suggestions when opened without text entry.

**Preconditions:**
- User role: HQ/CM Staff
- Location: Riso TAC (Teacher Availability Calendar)
- Subject list exists in system (≥3 subjects configured)
- No text entered in Subject filter field yet

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to Riso TAC page | TAC page loads successfully | locale = JP |
| 2 | Locate Subject filter dropdown | Subject filter control visible | filter_section = "Filters" |
| 3 | Click on Subject filter dropdown to open | Dropdown opens; no partial suggestions displayed | subject_list_size = 3 |
| 4 | Verify no autocomplete options shown | Empty state or placeholder text shown (per Figma design) | behavior = "no_options_on_open" |

**Severity:** major
**Priority:** high

---

### AC 01.2 – Subject Filter – Search matches subject by name

**Description:** AC 01 — Equivalence Partitioning — Subject search returns matching subjects after user enters search term.

**Preconditions:**
- User role: HQ/CM Staff
- Location: Riso TAC
- Subject list configured: ["Mathematics", "English", "Science", "History"]
- Subject filter dropdown opened

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Type "Math" in Subject filter field | Dropdown updates with matching subjects | search_term = "Math" |
| 2 | Verify filtered list contains "Mathematics" | "Mathematics" appears in dropdown list | subject_list_filtered = ["Mathematics"] |
| 3 | Click "Mathematics" to select | Subject filter applied; "Mathematics" shown as selected | selected_subject = "Mathematics" |
| 4 | Observe calendar display | Calendar shows lessons for Mathematics subject only | platform = "SF" |

**Severity:** major
**Priority:** high

---

### AC 01.3 – Subject Filter – Search no matches

**Description:** AC 01 — Equivalence Partitioning (Negative) — Subject search returns no results when search term has no matches.

**Preconditions:**
- User role: HQ/CM Staff
- Location: Riso TAC
- Subject list configured: ["Mathematics", "English", "Science", "History"]
- Subject filter dropdown opened

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Type "Xyz123" in Subject filter field (non-matching) | Dropdown updates | search_term = "Xyz123" |
| 2 | Verify no matching subjects displayed | Empty state message or "No results found" shown | subject_list_filtered = [] |
| 3 | Clear search field | Dropdown closes or returns to no-options state | clear_action = "backspace_all" |

**Severity:** minor
**Priority:** medium

---

### AC 01.4 – Subject Filter – Clear filter resets state

**Description:** AC 01 — Decision Table — Subject filter clear action returns to initial no-options state.

**Preconditions:**
- User role: HQ/CM Staff
- Location: Riso TAC
- Subject filter has search term entered and results visible
- Subject filter dropdown is open

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Subject filter shows "Math" search results | Results visible in dropdown | search_term = "Math" |
| 2 | Click clear button (X icon) or reset filter | Filter input cleared; dropdown closes or returns to no-options state | clear_button = "x_icon" |
| 3 | Verify calendar shows all lessons (no subject filter applied) | Subject filter removed; all lessons on TAC visible | expected_display = "all_subjects" |

**Severity:** minor
**Priority:** medium

---

## Test Data Dictionary

- `locale`: User interface language (JP = Japanese, EN = English)
- `subject_list_size`: Number of subjects configured in system
- `behavior`: Filter opening behavior configuration (no_options_on_open = no partial suggestions)
- `search_term`: Text entered by user in filter field
- `subject_list_filtered`: Array of subjects matching search criteria
- `selected_subject`: Subject chosen from dropdown
- `platform`: UI surface (SF = Salesforce, BO = Back Office, React)
- `clear_button`: UI control to reset filter (x_icon, reset_button, etc.)
- `expected_display`: Calendar display state after action
