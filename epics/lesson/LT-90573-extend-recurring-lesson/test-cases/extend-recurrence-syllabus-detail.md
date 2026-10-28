# Test Cases: LT-90573 — Extend Recurring Lesson Settings

## Suite: [Nichibei] Extend Recurrence — Syllabus Detail

### [Nichibei] Extend Recurrence – Syllabus Detail – End Date Extension – Mapped descriptions appear on every new lesson

**Description:** AC 01.4 — CRUD + Regression — Extending the recurrence end date applies the syllabus description mapped to each newly generated lesson code.

**Preconditions:**
- HQ or CM Staff is logged in to the Nichibei Salesforce organization.
- A syllabus master is associated with the course of recurring lesson schedule `NB-ER-01`.
- The syllabus master contains code `6` with description `Unit 6: Conversation`, code `7` with description `Unit 7: Reading`, and code `8` with description `Unit 8: Writing`.
- Recurring lesson schedule `NB-ER-01` has a weekly recurrence on Monday.
- Recurring lesson schedule `NB-ER-01` ends on `2026-04-06`.
- The last existing lesson in recurring lesson schedule `NB-ER-01` has lesson code `5`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff opens the detail page for recurring lesson schedule `NB-ER-01`. | The schedule detail page displays the existing recurrence ending on `2026-04-06`. | `schedule = NB-ER-01; recurrence = weekly Monday; current_end_date = 2026-04-06; last_lesson_code = 5` |
| 2 | HQ or CM Staff selects **Extend Recurrence** and sets the recurrence end date to `2026-04-27`. | The form accepts the later end date and indicates that three new weekly lessons will be created. | `requested_end_date = 2026-04-27; new_lesson_dates = 2026-04-13, 2026-04-20, 2026-04-27; expected_codes = 6, 7, 8` |
| 3 | HQ or CM Staff saves the extension. | Three new lessons are created in the recurring chain with lesson codes `6`, `7`, and `8`. | `created_lesson_count = 3; status = DRAFT` |
| 4 | HQ or CM Staff opens each newly created lesson. | The syllabus descriptions are `Unit 6: Conversation` for code `6`, `Unit 7: Reading` for code `7`, and `Unit 8: Writing` for code `8`. | `6 → Unit 6: Conversation; 7 → Unit 7: Reading; 8 → Unit 8: Writing` |

**Severity:** minor
**Priority:** medium

---

### [Nichibei] Extend Recurrence – Syllabus Detail – Lesson Count Increase – Mapped descriptions appear on every new lesson

**Description:** AC 01.4 — CRUD + Regression — Increasing the lesson count applies the syllabus description mapped to each newly generated lesson code.

**Preconditions:**
- HQ or CM Staff is logged in to the Nichibei Salesforce organization.
- A syllabus master is associated with the course of recurring lesson schedule `NB-ER-02`.
- The syllabus master contains code `11` with description `Chapter 11: Review` and code `12` with description `Chapter 12: Assessment`.
- Recurring lesson schedule `NB-ER-02` has a weekly recurrence on Thursday.
- Recurring lesson schedule `NB-ER-02` has lesson count `10`.
- The last existing lesson in recurring lesson schedule `NB-ER-02` has lesson code `10`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff opens the detail page for recurring lesson schedule `NB-ER-02`. | The schedule detail page displays lesson count `10` and last lesson code `10`. | `schedule = NB-ER-02; current_lesson_count = 10; last_lesson_code = 10` |
| 2 | HQ or CM Staff selects **Extend Recurrence** and increases the lesson count to `12`. | The form accepts the increased count and indicates that two new lessons will be created. | `requested_lesson_count = 12; increase = 2; expected_codes = 11, 12` |
| 3 | HQ or CM Staff saves the extension. | Two new lessons are created in the recurring chain with lesson codes `11` and `12`. | `created_lesson_count = 2; status = DRAFT` |
| 4 | HQ or CM Staff opens the new lesson with code `11`. | The syllabus description shows `Chapter 11: Review`. | `lesson_code = 11; mapped_description = Chapter 11: Review` |
| 5 | HQ or CM Staff opens the new lesson with code `12`. | The syllabus description shows `Chapter 12: Assessment`. | `lesson_code = 12; mapped_description = Chapter 12: Assessment` |

**Severity:** minor
**Priority:** medium

---

### [Nichibei] Extend Recurrence – Syllabus Detail – Unmapped Lesson Code – No unrelated description is assigned

**Description:** AC 01.4 — Negative + Regression — A new lesson whose code has no syllabus-detail mapping remains without a syllabus description and does not inherit another code's description.

**Preconditions:**
- HQ or CM Staff is logged in to the Nichibei Salesforce organization.
- A syllabus master is associated with the course of recurring lesson schedule `NB-ER-03`.
- The syllabus master contains code `21` with description `Module 21: Grammar`.
- The syllabus master does not contain a syllabus detail for code `22`.
- Recurring lesson schedule `NB-ER-03` has a weekly recurrence on Tuesday.
- Recurring lesson schedule `NB-ER-03` has lesson count `20`.
- The last existing lesson in recurring lesson schedule `NB-ER-03` has lesson code `20`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff opens the detail page for recurring lesson schedule `NB-ER-03`. | The schedule detail page displays lesson count `20` and last lesson code `20`. | `schedule = NB-ER-03; current_lesson_count = 20; last_lesson_code = 20` |
| 2 | HQ or CM Staff selects **Extend Recurrence** and increases the lesson count to `22`. | The form accepts the increased count and indicates that lessons with codes `21` and `22` will be created. | `requested_lesson_count = 22; increase = 2; expected_codes = 21, 22` |
| 3 | HQ or CM Staff saves the extension. | Two new lessons are created in the recurring chain with lesson codes `21` and `22`. | `created_lesson_count = 2; status = DRAFT` |
| 4 | HQ or CM Staff opens the new lesson with code `21`. | The syllabus description shows `Module 21: Grammar`. | `lesson_code = 21; mapped_description = Module 21: Grammar` |
| 5 | HQ or CM Staff opens the new lesson with code `22`. | The syllabus description is empty and does not show `Module 21: Grammar`. | `lesson_code = 22; syllabus_mapping = none; expected_description = empty` |

**Severity:** minor
**Priority:** medium

---
