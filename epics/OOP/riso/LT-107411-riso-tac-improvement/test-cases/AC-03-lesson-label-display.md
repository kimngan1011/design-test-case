# Test Cases: LT-107411 — Riso | Core | TAC improvement (July)

## Suite: AC-03 — Lesson Label Display

### AC 03.1 – Lesson Label – Subject name and teacher name displayed in new format

**Description:** AC 03 — Component — Student lesson label displays Subject Name followed by Teacher Name in the new format.

**Preconditions:**
- User role: HQ/CM Staff or Teacher
- Location: Riso TAC (Teacher Availability Calendar)
- Lesson exists with: subject="Mathematics", teacher="Tanaka Yuki"
- Calendar page loaded and rendering lessons

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to Riso TAC | TAC page loads with lesson calendar | lesson_id = "LESSON-001" |
| 2 | Locate lesson card for the sample lesson | Lesson card visible on calendar at correct timeslot | timeslot = "09:00-10:00" |
| 3 | Verify lesson label text format | Label displays as "Mathematics (Tanaka Yuki)" or per Figma design spec | label_format = "subject (teacher)" |
| 4 | Verify label text is readable (not truncated excessively) | Full subject and teacher names visible or truncated with ellipsis per design | text_truncation = "design_compliant" |

**Severity:** major
**Priority:** medium

---

### AC 03.2 – Lesson Label – Null subject displays correctly (no confusing placeholder)

**Description:** AC 03 — Boundary Value Analysis + Conditional — Lesson label handles null subject field without confusing or error display.

**Preconditions:**
- User role: HQ/CM Staff
- Location: Riso TAC
- Lesson exists with: subject=null, teacher="Tanaka Yuki"
- Calendar page loaded

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to Riso TAC | TAC page loads | lesson_id = "LESSON-002" |
| 2 | Locate lesson card with null subject | Lesson visible on calendar | subject_value = null |
| 3 | Verify label format with null subject | Label displays as "null (Tanaka Yuki)", "(Tanaka Yuki)", or empty subject per spec resolution (no placeholder confusion) | label_with_null_subject = "display_as_null_or_empty" |
| 4 | Verify no error message or warning icon | Calendar displays cleanly without error indicators | error_state = "none" |

**Severity:** minor
**Priority:** medium

---

### AC 03.3 – Lesson Label – Truncation remains usable after label format change

**Description:** AC 03 — Component — Lesson label truncation (if applied) maintains usability with new Subject+Teacher format.

**Preconditions:**
- User role: HQ/CM Staff
- Location: Riso TAC
- Lesson with long subject name: "Advanced Physics with Laboratory Experiments", teacher="Yoshida Akira"
- Calendar responsive design configured
- Lesson card width limited (e.g., mobile view or narrow layout)

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to Riso TAC on narrow viewport (mobile or small container) | TAC loads with responsive layout | viewport_width = "375px" |
| 2 | Locate lesson card with long label | Lesson visible on calendar | subject_name = "Advanced Physics with Laboratory Experiments" |
| 3 | Verify label truncates gracefully | Subject or full label truncates with ellipsis (...) per design, not broken or unreadable | truncation_style = "ellipsis" |
| 4 | Verify teacher name remains visible or tooltip shows full text | Teacher name visible or full label accessible via hover/tooltip | teacher_name_visibility = "visible_or_tooltip" |

**Severity:** minor
**Priority:** low

---

## Test Data Dictionary

- `lesson_id`: Unique identifier for the lesson being displayed
- `timeslot`: Calendar time slot (e.g., "09:00-10:00")
- `label_format`: Expected label string format ("subject (teacher)" or per spec)
- `text_truncation`: Truncation behavior (design_compliant, visible, ellipsis)
- `subject_value`: Subject name or null
- `label_with_null_subject`: How to display when subject is null (display_as_null, display_as_empty, omit_subject)
- `error_state`: Presence of error indicators (none, warning_icon, error_message)
- `viewport_width`: Screen or container width in pixels
- `subject_name`: Long subject name that may trigger truncation
- `truncation_style`: Truncation method (ellipsis, line-clamp, abbreviation)
- `teacher_name_visibility`: Whether teacher name is visible after truncation (visible, tooltip, hidden)
