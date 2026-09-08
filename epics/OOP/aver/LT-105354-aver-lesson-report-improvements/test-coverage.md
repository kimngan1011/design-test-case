# Test Coverage: LT-105354 - Aver Lesson Report Improvement Items

**Jira:** https://manabie.atlassian.net/browse/LT-105354
**Date:** 2026-09-08
**Module:** scheduling / OOP/aver
**Platforms:** Salesforce, Back Office, Student App, PDF

---

## 1. Business Rules Extracted

| # | AC | Business Rule |
|---|---|---|
| 1 | AC 01.1 | Long Japanese textbook names render in PDF without duplicated characters. |
| 2 | AC 01.2 | Textbook names over five rendered lines preserve the full original string. |
| 3 | AC 01.3 | Multiple long textbook rows remain readable in one generated PDF. |
| 4 | AC 02.1 | Breakthrough Test `Next Time` copies to next lesson `Today's Result`. |
| 5 | AC 02.2 | Copy target is calculated by same Lesson Schedule only. |
| 6 | AC 02.3 | Existing next lesson `Today's Result` is not overwritten silently. |
| 7 | AC 03.1 | Next Week Homework PDF shows `Remark` under textbook name. |
| 8 | AC 03.2 | Long textbook and remark values remain aligned in the same homework item. |
| 9 | AC 04.1 | BO copies Next Week Homework `Remarks` when adding same textbook homework to next lesson. |
| 10 | AC 04.2 | The latest previous same-schedule lesson value is used as source. |
| 11 | AC 04.3 | Edited copied remark becomes source for following lesson. |
| 12 | AC 04.4 | Different textbook does not trigger remark copy. |
| 13 | AC 04.5 | First lesson/no previous same-schedule lesson does not copy remark. |
| 14 | AC 05.1 | Student App PDF title displays `指導簿 【生徒用・MM月X回目】`. |
| 15 | AC 05.2 | Monthly count is sorted by lesson date for that student. |
| 16 | AC 05.3 | Monthly count resets per month. |
| 17 | AC 06.1 | Previous Week Homework edit controls are hidden in Edit Lesson Report mode. |
| 18 | AC 06.2 | Previous Week Homework fields are read-only in Edit Lesson Report mode. |
| 19 | AC 07.1 | Instructor's Comment 3 copies from previous same-schedule lesson. |
| 20 | AC 07.2 | Copied Instructor's Comment 3 remains editable. |
| 21 | AC 07.3 | Edited Instructor's Comment 3 becomes source for following lesson. |
| 22 | AC 08.1 | Add homework dialogs display homework date ranges without year. |
| 23 | AC 08.2 | Japanese date range format uses `MM月DD日`. |
| 24 | AC 08.3 | Cross-year date range still hides year. |
| 25 | AC 09.1 | Lesson List includes `Next Lesson` column. |
| 26 | AC 09.2 | Customizable Columns includes `Next Lesson`. |
| 27 | AC 09.3 | Next Lesson value is same-schedule next lesson date and hyperlink. |
| 28 | AC 09.4 | Last same-schedule lesson has no clickable Next Lesson value. |
| 29 | AC 10.1 | Homework, Lesson Report, and Lesson previous/next logic uses same Lesson Schedule only. |
| 30 | AC 10.2 | Same-student lesson in another Lesson Schedule is ignored. |
| 31 | AC 10.3 | Copy-forward behavior follows same Lesson Schedule-only logic. |

## 2. Logic Type Categorization

| AC | Business Rule # | Logic Type |
|---|---|---|
| AC 01.* | 1, 2, 3 | PDF rendering, Text wrapping, Regression |
| AC 02.* | 4, 5, 6 | Copy-forward, Data integrity, Same-schedule filtering |
| AC 03.* | 7, 8 | PDF layout, Display completeness |
| AC 04.* | 9, 10, 11, 12, 13 | Conditional logic, Copy-forward, Negative |
| AC 05.* | 14, 15, 16 | Date sorting, Counting, Mobile/PDF |
| AC 06.* | 17, 18 | Permission/editability, Negative |
| AC 07.* | 19, 20, 21 | Copy-forward, Editability, Regression |
| AC 08.* | 22, 23, 24 | Date formatting, Localization, Boundary |
| AC 09.* | 25, 26, 27, 28 | List display, Customizable columns, Navigation |
| AC 10.* | 29, 30, 31 | Cross-feature regression, Same-schedule filtering |

## 3. Test Technique Selection

| Logic Type | Applicable Techniques |
|---|---|
| PDF rendering/layout | Visual comparison, Equivalence Partitioning, Regression |
| Copy-forward | State Transition, Decision Table, CRUD |
| Same-schedule filtering | Decision Table, Negative |
| Counting/sorting | Boundary Value Analysis, Data integrity |
| Editability | Negative, Permission Matrix |
| Date formatting | Boundary Value Analysis, Localization |
| List column/navigation | Component, Regression |

## 4. Structured Coverage Strategy

| AC | Business Rule Summary | Logic Type | Test Technique | Risk Level | Coverage Depth |
|---|---|---|---|---|---|
| AC 01.1-01.3 | Long textbook names render in PDF exactly once and stay readable. | PDF rendering | Visual comparison, Regression | High | Deep |
| AC 02.1-02.3 | Breakthrough Test `Next Time` copies to next lesson `Today's Result` safely. | Copy-forward | State Transition, Negative | High | Deep |
| AC 03.1-03.2 | PDF homework Remark is moved under textbook name. | PDF layout | Component, Visual comparison | Medium | Standard |
| AC 04.1-04.5 | BO homework Remarks copy only for same-textbook same-schedule next homework. | Conditional copy | Decision Table | High | Deep |
| AC 05.1-05.3 | Student App PDF title includes monthly count by student/date. | Counting | Boundary Value Analysis | High | Deep |
| AC 06.1-06.2 | Previous Week Homework is read-only during edit. | Editability | Negative | High | Standard |
| AC 07.1-07.3 | Instructor's Comment 3 copies forward and remains editable. | Copy-forward | State Transition | Medium | Standard |
| AC 08.1-08.3 | Add homework date range hides year in JP format. | Date formatting | Localization, Boundary | Medium | Standard |
| AC 09.1-09.4 | Lesson List shows hyperlinked Next Lesson date from same Lesson Schedule. | List/navigation | Component, Regression | High | Standard |
| AC 10.1-10.3 | Previous/next logic ignores different Lesson Schedule records. | Same-schedule filtering | Decision Table, Negative | High | Deep |

## 5. High-Risk Areas Requiring Deeper Testing

### Critical Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| Copy-forward overwrite safety | Copying data into a future lesson can destroy teacher input if overwrite behavior is wrong. | Include existing-value negative cases for Today's Result, Remarks, and Instructor's Comment 3. |
| Same Lesson Schedule-only logic | The ticket explicitly changes previous/next resolution; wrong matching can copy from the wrong student allocation. | Use data where the same student has lessons in two schedules on adjacent dates. |

### High Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| Student App monthly count | Count depends on student/month/date sort and can be wrong around month boundaries. | Include first/second lesson and month reset cases. |
| PDF long Japanese text | The original bug is visual and appears with long Japanese text. | Use exact long textbook strings from Jira and compare no duplication/truncation. |
| Previous Week Homework edit lock | A regression can allow unintended edits from BO Edit Lesson Report mode. | Assert both absence of add/edit buttons and read-only fields. |

### Medium Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| Homework date range localization | Year hiding is display-only but user-facing. | Include normal and cross-year date ranges. |
| Lesson List column | New column can be hidden by customizable-column defaults. | Cover default display, customizable columns, hyperlink, and last-lesson blank state. |

## 6. Coverage Gaps vs. Existing Test Cases

| Gap Area | Existing Test Case | Overlap | New Coverage Needed |
|---|---|---|---|
| Aver previous/next lesson logic | `LT-104011` covers navigation buttons only. | Partial | Add logic cases for copy-forward source/target selection. |
| Lesson report field edit/save | Existing lesson report cases cover basic report lifecycle. | Partial | Add Aver-specific fields and copy-forward behavior. |
| Student App PDF monthly count | Mobile report viewing exists in domain knowledge. | Partial | Add PDF title count cases. |
| Long Japanese PDF text | Aso syllabus PDF cases cover PDF generation, not Aver lesson report. | Partial | Add Aver lesson report PDF text wrapping cases. |
| Lesson List Next Lesson column | Existing list/navigation cases do not cover this column. | None | Add Lesson List column/customization/hyperlink cases. |

## 7. Suggested Test Suite Structure

```text
epics/OOP/aver/LT-105354-aver-lesson-report-improvements/test-cases/
|- aver-lesson-report-improvements.md -> AC 01.1-10.3 complete Aver lesson report improvement coverage
|- aver-lesson-report-improvements.csv -> Qase import format for the same cases
```

