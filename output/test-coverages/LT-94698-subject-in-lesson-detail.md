# Test Coverage: LT-94698 — Riso | Subject in Lesson Detail

**Jira:** https://manabie.atlassian.net/browse/LT-94698
**Date:** 2026-03-25

---

## 1. Business Rules Extracted

| #   | AC      | Business Rule                                                                        |
| --- | ------- | ------------------------------------------------------------------------------------ |
| 1   | AC 01.1 | User can set Subject on a lesson via Subject Master lookup                           |
| 2   | AC 01.2 | Subject field is optional — lesson can be saved without a subject                    |
| 3   | AC 01.3 | Subject is single-select — only one subject per lesson                               |
| 4   | AC 02.1 | User can specify subject in CSV import; subject mapped to Subject Master             |
| 5   | AC 03.1 | Subject displayed in SF Lesson Details, positioned above Location                    |
| 6   | AC 03.2 | Subject displayed in SF Calendar Lesson Info                                         |
| 7   | AC 03.3 | Subject displayed in BO Lesson Details, positioned above Location                    |
| 8   | AC 03.4 | Subject displayed in BO Calendar Lesson Info                                         |
| 9   | AC 03.5 | Subject displayed in Mobile Learning App                                             |
| 10  | AC 04.1 | SF Lessons list supports search by Subject; Subject not added to list columns (core) |
| 11  | AC 04.2 | BO Lesson Management supports search by Subject                                      |
| 12  | AC 05.1 | SF Calendar supports filtering by Subject                                            |
| 13  | AC 05.2 | BO Calendar supports filtering by Subject                                            |
| 14  | AC 05.3 | BO Lesson Management supports Subject filter with cross-field validation             |
| 15  | AC 06.1 | Aver custom page must NOT show Subject field                                         |
| 16  | AC 06.2 | No teacher-subject validation — any teacher can be assigned regardless of subject    |
| 17  | AC 06.3 | No course-subject relationship — subject is per-lesson, not per-course               |

---

## 2. Logic Type Categorization

| #   | AC      | Logic Type(s)                         |
| --- | ------- | ------------------------------------- |
| 1   | AC 01.1 | Validation logic, Cross-system impact |
| 2   | AC 01.2 | Validation logic, Conditional logic   |
| 3   | AC 01.3 | Validation logic                      |
| 4   | AC 02.1 | Validation logic, Data integrity      |
| 5   | AC 03.1 | Cross-system impact                   |
| 6   | AC 03.2 | Cross-system impact                   |
| 7   | AC 03.3 | Cross-system impact                   |
| 8   | AC 03.4 | Cross-system impact                   |
| 9   | AC 03.5 | Cross-system impact                   |
| 10  | AC 04.1 | Conditional logic                     |
| 11  | AC 04.2 | Conditional logic                     |
| 12  | AC 05.1 | Conditional logic                     |
| 13  | AC 05.2 | Conditional logic                     |
| 14  | AC 05.3 | Conditional logic, Data integrity     |
| 15  | AC 06.1 | Permission logic, Conditional logic   |
| 16  | AC 06.2 | Permission logic                      |
| 17  | AC 06.3 | Data integrity                        |

---

## 3. Test Technique Selection

| #   | AC      | Logic Type(s)               | Primary Technique        | Secondary Technique |
| --- | ------- | --------------------------- | ------------------------ | ------------------- |
| 1   | AC 01.1 | Validation, Cross-system    | Equivalence Partitioning | Regression Analysis |
| 2   | AC 01.2 | Validation, Conditional     | Equivalence Partitioning | Negative Testing    |
| 3   | AC 01.3 | Validation                  | Equivalence Partitioning | Negative Testing    |
| 4   | AC 02.1 | Validation, Data integrity  | Equivalence Partitioning | Negative Testing    |
| 5   | AC 03.1 | Cross-system                | Regression Analysis      | CRUD Testing        |
| 6   | AC 03.2 | Cross-system                | Regression Analysis      | CRUD Testing        |
| 7   | AC 03.3 | Cross-system                | Regression Analysis      | CRUD Testing        |
| 8   | AC 03.4 | Cross-system                | Regression Analysis      | CRUD Testing        |
| 9   | AC 03.5 | Cross-system                | Regression Analysis      | CRUD Testing        |
| 10  | AC 04.1 | Conditional                 | Decision Table           | Negative Testing    |
| 11  | AC 04.2 | Conditional                 | Decision Table           | Negative Testing    |
| 12  | AC 05.1 | Conditional                 | Decision Table           | Negative Testing    |
| 13  | AC 05.2 | Conditional                 | Decision Table           | Negative Testing    |
| 14  | AC 05.3 | Conditional, Data integrity | Decision Table           | Negative Testing    |
| 15  | AC 06.1 | Permission, Conditional     | Permission Matrix        | Negative Testing    |
| 16  | AC 06.2 | Permission                  | Permission Matrix        | Decision Table      |
| 17  | AC 06.3 | Data integrity              | CRUD Testing             | Regression Analysis |

---

## 4. Coverage Strategy Table

| AC      | Business Rule Summary                             | Logic Type                  | Test Technique           | Risk Level | Coverage Depth |
| ------- | ------------------------------------------------- | --------------------------- | ------------------------ | ---------- | -------------- |
| AC 01.1 | Set Subject via lookup on lesson                  | Validation, Cross-system    | Equivalence Partitioning | High       | Deep           |
| AC 01.2 | Subject is optional                               | Validation, Conditional     | Equivalence Partitioning | Medium     | Standard       |
| AC 01.3 | Single-select subject                             | Validation                  | Equivalence Partitioning | Medium     | Standard       |
| AC 02.1 | Subject in CSV import                             | Validation, Data integrity  | Equivalence Partitioning | Critical   | Deep           |
| AC 03.1 | Subject displayed in SF Lesson Details            | Cross-system                | Regression Analysis      | High       | Standard       |
| AC 03.2 | Subject displayed in SF Calendar                  | Cross-system                | Regression Analysis      | Medium     | Standard       |
| AC 03.3 | Subject displayed in BO Lesson Details            | Cross-system                | Regression Analysis      | High       | Standard       |
| AC 03.4 | Subject displayed in BO Calendar                  | Cross-system                | Regression Analysis      | Medium     | Standard       |
| AC 03.5 | Subject displayed in Mobile Learning App          | Cross-system                | Regression Analysis      | High       | Standard       |
| AC 04.1 | SF search by Subject                              | Conditional                 | Decision Table           | Medium     | Standard       |
| AC 04.2 | BO search by Subject                              | Conditional                 | Decision Table           | Medium     | Standard       |
| AC 05.1 | SF Calendar filter by Subject                     | Conditional                 | Decision Table           | Medium     | Standard       |
| AC 05.2 | BO Calendar filter by Subject                     | Conditional                 | Decision Table           | Medium     | Standard       |
| AC 05.3 | BO Lesson Management Subject filter + cross-field | Conditional, Data integrity | Decision Table           | High       | Deep           |
| AC 06.1 | Aver page must NOT show Subject                   | Permission, Conditional     | Permission Matrix        | High       | Standard       |
| AC 06.2 | No teacher-subject validation                     | Permission                  | Permission Matrix        | Low        | Smoke          |
| AC 06.3 | No course-subject relationship                    | Data integrity              | CRUD Testing             | Low        | Smoke          |

---

## 5. High-Risk Areas

### 🔴 Critical Risk

| Area                 | Risk Reason                                                                     | Recommended Approach                                                                      |
| -------------------- | ------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| CSV Import (AC 02.1) | Bulk data operation — invalid subject values could corrupt lesson data at scale | Deep: valid subject, empty subject, invalid subject, multiple lessons with mixed subjects |

### 🟠 High Risk

| Area                                    | Risk Reason                                                                       | Recommended Approach                                                      |
| --------------------------------------- | --------------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| Set Subject on Lesson (AC 01.1)         | Core CRUD for the new field — foundation for all other ACs                        | Deep: create with subject, edit subject, clear subject, recurring lessons |
| SF Lesson Detail Display (AC 03.1)      | Primary user surface for Riso — subject must appear above Location                | Standard: with subject, without subject, after edit                       |
| BO Lesson Detail Display (AC 03.3)      | Primary admin surface — subject must appear and sync correctly                    | Standard: with subject, without subject, after edit                       |
| Mobile Display (AC 03.5)                | Student-facing — incorrect display impacts Riso's audit/reporting                 | Standard: with subject, without subject                                   |
| BO Subject Filter cross-field (AC 05.3) | Cross-field validation adds complexity; incorrect filter could hide valid lessons | Deep: filter alone, combined filters, reset filter                        |
| Aver Exclusion (AC 06.1)                | Negative test — field must NOT appear; regression risk if accidentally shown      | Standard: confirm field absent                                            |

### 🟡 Medium Risk

| Area                                 | Risk Reason                                         | Recommended Approach                        |
| ------------------------------------ | --------------------------------------------------- | ------------------------------------------- |
| Optional field (AC 01.2)             | Edge case — empty subject must not cause errors     | Standard: save without subject              |
| Single-select (AC 01.3)              | UI constraint — must not allow multiple selections  | Standard: confirm single-select behavior    |
| SF/BO Calendar display (AC 03.2/3.4) | Secondary surface — less frequently used            | Standard: confirm subject in lesson info    |
| Search (AC 04.1/04.2)                | Functional but lower risk — typical search behavior | Standard: search match, search empty result |
| Calendar filters (AC 05.1/05.2)      | Functional — standard filter behavior               | Standard: filter with subject, clear filter |

---

## 6. Coverage Gaps

| Gap Area                           | Existing Test Case                       | Overlap | New Coverage Needed                               |
| ---------------------------------- | ---------------------------------------- | ------- | ------------------------------------------------- |
| Subject field CRUD on lesson       | None                                     | None    | Full: set, edit, clear subject                    |
| Subject in CSV import              | `import-lesson.md` (TC-1031, TC-1034)    | Partial | Add subject column to CSV import tests            |
| Subject display (SF/BO/Mobile)     | `edit-lesson-bo.md`, `edit-lesson-sf.md` | None    | New: subject display on all surfaces              |
| Subject search                     | None                                     | None    | Full: SF and BO search by subject                 |
| Subject filter                     | None                                     | None    | Full: SF Calendar, BO Calendar, BO Lesson filters |
| Aver exclusion                     | None                                     | None    | New: confirm subject NOT on Aver page             |
| Create lesson form — Subject field | `create-lesson-list.md` (TC-5644)        | None    | Verify Subject appears in create lesson form      |

---

## 7. Proposed Test Suite Structure

```
output/test-cases/lesson-management/lesson/subject/
  ├── LT-94698-subject-in-lesson-detail.md    → AC 01.1–01.3, AC 03.1–03.5 — Set/edit/display subject on SF, BO, Mobile
  ├── LT-94698-subject-in-lesson-detail.csv   → Qase companion CSV
  ├── LT-94698-subject-import-search-filter.md   → AC 02.1, AC 04.1–04.2, AC 05.1–05.3, AC 06.1–06.3 — CSV import, search, filter, exclusions
  ├── LT-94698-subject-import-search-filter.csv  → Qase companion CSV
```

### Suite breakdown

| Suite Name                         | ACs Covered                | File                                     |
| ---------------------------------- | -------------------------- | ---------------------------------------- |
| Subject – Set & Display            | AC 01.1–01.3, AC 03.1–03.5 | LT-94698-subject-in-lesson-detail.md     |
| Subject – CSV Import               | AC 02.1                    | LT-94698-subject-import-search-filter.md |
| Subject – Search & Filter          | AC 04.1–04.2, AC 05.1–05.3 | LT-94698-subject-import-search-filter.md |
| Subject – Exclusions & Constraints | AC 06.1–06.3               | LT-94698-subject-import-search-filter.md |
