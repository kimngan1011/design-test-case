# Test Cases: LT-57816 — Lesson Report under Lesson Value Synchronization

## Suite: Lesson Report under Lesson

### [Renseikai] Lesson Report under Lesson – SF Group lesson – Initial shared values – Copied to every student detail

**Description:** AC 01.1 / AC 01.4 — CRUD and Component — Saving all three shared values from SF copies the exact values to each enrolled student's detail and BO views.

**Preconditions:**
- Actor: HQ or CM Staff logged in to Salesforce.
- Group lesson `LR-57816-SF-01` has students `Aiko Tanaka` and `Haruto Sato`; Lesson Report status is Draft.
- `content_v1 = "Linear equations: solving two variables"`; `announcement_v1 = "Bring calculator on 2026-08-05"`; `homework_v1 = "Workbook pp. 20-21"`.

| # | Action | Expected Result | Test Data |
| --- | --- | --- | --- |
| 1 | Open Lesson `LR-57816-SF-01` and select **Report**. | The Group Lesson Report is open and editable. | `lesson = LR-57816-SF-01; teaching_method = Group; students = Aiko Tanaka, Haruto Sato` |
| 2 | Enter and save Content, Next Lesson's Announcement, and Next Lesson's Homework. | The source Lesson Report shows `content_v1`, `announcement_v1`, and `homework_v1`. | `content_v1; announcement_v1; homework_v1` |
| 3 | For Aiko Tanaka and Haruto Sato, open the Student Lesson Allocation record in SF, select **Report History**, and locate the target lesson in the **Lesson Report Details** table. | Each student row displays Content = `content_v1`, Next Lesson - Homework = `homework_v1`, and Next Lesson - Announcement = `announcement_v1`. | `expected for both students = content_v1, announcement_v1, homework_v1` |
| 4 | In BO, open the target Lesson and open the Report History for each student. Locate the target lesson in the Lesson Report Details list. | The BO Report History row for each student displays Content = `content_v1`, Next Lesson - Homework = `homework_v1`, and Next Lesson - Announcement = `announcement_v1`. | `students = Aiko Tanaka, Haruto Sato; columns = Content, Next Lesson - Homework, Next Lesson - Announcement` |

**Severity:** major
**Priority:** high

---

### [Renseikai] Lesson Report under Lesson – BO Group lesson – Initial shared values – Copied to every student detail

**Description:** AC 01.1 / AC 01.4 — CRUD and Component — Saving all three shared values from BO copies the exact values to each enrolled student's detail and SF views.

**Preconditions:**
- Actor: HQ or CM Staff logged in to Back Office.
- Group lesson `LR-57816-BO-01` has students `Aiko Tanaka` and `Haruto Sato`; Lesson Report status is Draft.
- `content_v1 = "Linear equations: solving two variables"`; `announcement_v1 = "Bring calculator on 2026-08-05"`; `homework_v1 = "Workbook pp. 20-21"`.

| # | Action | Expected Result | Test Data |
| --- | --- | --- | --- |
| 1 | Open Lesson `LR-57816-BO-01` and select **Lesson Report under Lesson**. | The Group Lesson Report is open and editable. | `lesson = LR-57816-BO-01; teaching_method = Group; students = Aiko Tanaka, Haruto Sato` |
| 2 | Enter and save Content, Next Lesson's Announcement, and Next Lesson's Homework. | The source Lesson Report shows `content_v1`, `announcement_v1`, and `homework_v1`. | `content_v1; announcement_v1; homework_v1` |
| 3 | For Aiko Tanaka and Haruto Sato, open the Student Lesson Allocation record in SF, select **Report History**, and locate the target lesson in the **Lesson Report Details** table. | Each student row displays Content = `content_v1`, Next Lesson - Homework = `homework_v1`, and Next Lesson - Announcement = `announcement_v1`. | `expected for both students = content_v1, announcement_v1, homework_v1` |
| 4 | In BO, open the target Lesson and open the Report History for each student. Locate the target lesson in the Lesson Report Details list. | The BO Report History row for each student displays Content = `content_v1`, Next Lesson - Homework = `homework_v1`, and Next Lesson - Announcement = `announcement_v1`. | `students = Aiko Tanaka, Haruto Sato; columns = Content, Next Lesson - Homework, Next Lesson - Announcement` |

**Severity:** major
**Priority:** high

---

### [Renseikai] Lesson Report under Lesson – SF Group lesson – Content update – Replaced on every student detail

**Description:** AC 01.2 / AC 01.4 — CRUD and Regression — Updating Content from SF replaces only Content on every student detail and preserves the other shared values.

**Preconditions:**
- Actor: HQ or CM Staff logged in to Salesforce.
- Group lesson `LR-57816-SF-02` has students `Aiko Tanaka` and `Haruto Sato`; its source report and both details hold `content_v1`, `announcement_v1`, and `homework_v1`.
- `content_v2 = "Quadratic equations: factoring"`.

| # | Action | Expected Result | Test Data |
| --- | --- | --- | --- |
| 1 | Open Lesson `LR-57816-SF-02` and select **Report**. | The saved Group Lesson Report is open and editable. | `lesson = LR-57816-SF-02; teaching_method = Group` |
| 2 | Replace only Content with `content_v2` and save. | The source report shows `content_v2`; Announcement and Homework remain `announcement_v1` and `homework_v1`. | `changed = content_v2; preserved = announcement_v1, homework_v1` |
| 3 | For Aiko Tanaka and Haruto Sato, open the Student Lesson Allocation record in SF, select **Report History**, and locate the target lesson in the **Lesson Report Details** table. | Each student row displays Content = `content_v2`, Next Lesson - Homework = `homework_v1`, and Next Lesson - Announcement = `announcement_v1`. | `expected for both students = content_v2, announcement_v1, homework_v1` |
| 4 | In BO, open the target Lesson and open the Report History for each student. Locate the target lesson in the Lesson Report Details list. | The BO Report History row for each student displays Content = `content_v2`, Next Lesson - Homework = `homework_v1`, and Next Lesson - Announcement = `announcement_v1`. | `students = Aiko Tanaka, Haruto Sato; columns = Content, Next Lesson - Homework, Next Lesson - Announcement` |

**Severity:** major
**Priority:** high

---

### [Renseikai] Lesson Report under Lesson – SF Group lesson – Announcement update – Replaced on every student detail

**Description:** AC 01.2 / AC 01.4 — CRUD and Regression — Updating Next Lesson's Announcement from SF replaces only that value on every student detail.

**Preconditions:**
- Actor: HQ or CM Staff logged in to Salesforce.
- Group lesson `LR-57816-SF-03` has students `Aiko Tanaka` and `Haruto Sato`; its source report and both details hold `content_v1`, `announcement_v1`, and `homework_v1`.
- `announcement_v2 = "Submit quiz by 2026-08-06"`.

| # | Action | Expected Result | Test Data |
| --- | --- | --- | --- |
| 1 | Open Lesson `LR-57816-SF-03` and select **Report**. | The saved Group Lesson Report is open and editable. | `lesson = LR-57816-SF-03; teaching_method = Group` |
| 2 | Replace only Next Lesson's Announcement with `announcement_v2` and save. | The source report shows `announcement_v2`; Content and Homework remain `content_v1` and `homework_v1`. | `changed = announcement_v2; preserved = content_v1, homework_v1` |
| 3 | For Aiko Tanaka and Haruto Sato, open the Student Lesson Allocation record in SF, select **Report History**, and locate the target lesson in the **Lesson Report Details** table. | Each student row displays Content = `content_v1`, Next Lesson - Homework = `homework_v1`, and Next Lesson - Announcement = `announcement_v2`. | `expected for both students = content_v1, announcement_v2, homework_v1` |
| 4 | In BO, open the target Lesson and open the Report History for each student. Locate the target lesson in the Lesson Report Details list. | The BO Report History row for each student displays Content = `content_v1`, Next Lesson - Homework = `homework_v1`, and Next Lesson - Announcement = `announcement_v2`. | `students = Aiko Tanaka, Haruto Sato; columns = Content, Next Lesson - Homework, Next Lesson - Announcement` |

**Severity:** major
**Priority:** high

---

### [Renseikai] Lesson Report under Lesson – SF Group lesson – Homework update – Replaced on every student detail

**Description:** AC 01.2 / AC 01.4 — CRUD and Regression — Updating Next Lesson's Homework from SF replaces only that value on every student detail.

**Preconditions:**
- Actor: HQ or CM Staff logged in to Salesforce.
- Group lesson `LR-57816-SF-04` has students `Aiko Tanaka` and `Haruto Sato`; its source report and both details hold `content_v1`, `announcement_v1`, and `homework_v1`.
- `homework_v2 = "Workbook pp. 22-23"`.

| # | Action | Expected Result | Test Data |
| --- | --- | --- | --- |
| 1 | Open Lesson `LR-57816-SF-04` and select **Report**. | The saved Group Lesson Report is open and editable. | `lesson = LR-57816-SF-04; teaching_method = Group` |
| 2 | Replace only Next Lesson's Homework with `homework_v2` and save. | The source report shows `homework_v2`; Content and Announcement remain `content_v1` and `announcement_v1`. | `changed = homework_v2; preserved = content_v1, announcement_v1` |
| 3 | For Aiko Tanaka and Haruto Sato, open the Student Lesson Allocation record in SF, select **Report History**, and locate the target lesson in the **Lesson Report Details** table. | Each student row displays Content = `content_v1`, Next Lesson - Homework = `homework_v2`, and Next Lesson - Announcement = `announcement_v1`. | `expected for both students = content_v1, announcement_v1, homework_v2` |
| 4 | In BO, open the target Lesson and open the Report History for each student. Locate the target lesson in the Lesson Report Details list. | The BO Report History row for each student displays Content = `content_v1`, Next Lesson - Homework = `homework_v2`, and Next Lesson - Announcement = `announcement_v1`. | `students = Aiko Tanaka, Haruto Sato; columns = Content, Next Lesson - Homework, Next Lesson - Announcement` |

**Severity:** major
**Priority:** high

---

### [Renseikai] Lesson Report under Lesson – SF Group lesson – Unrelated field update – Shared values retained

**Description:** AC 01.3 / AC 01.4 — Negative and Regression — Saving Remarks from SF does not clear or change any stored shared value.

**Preconditions:**
- Actor: HQ or CM Staff logged in to Salesforce.
- Group lesson `LR-57816-SF-05` has students `Aiko Tanaka` and `Haruto Sato`; its source report and both details hold `content_v1`, `announcement_v1`, and `homework_v1`.
- `remarks_v2 = "Student questions collected for review"`.

| # | Action | Expected Result | Test Data |
| --- | --- | --- | --- |
| 1 | Open Lesson `LR-57816-SF-05` and select **Report**. | The saved Group Lesson Report is open and editable. | `lesson = LR-57816-SF-05; teaching_method = Group` |
| 2 | Replace only Remarks with `remarks_v2` and save. | Remarks shows `remarks_v2`; the source report still shows `content_v1`, `announcement_v1`, and `homework_v1`. | `changed = remarks_v2; retained = content_v1, announcement_v1, homework_v1` |
| 3 | For Aiko Tanaka and Haruto Sato, open the Student Lesson Allocation record in SF, select **Report History**, and locate the target lesson in the **Lesson Report Details** table. | Each student row displays Content = `content_v1`, Next Lesson - Homework = `homework_v1`, and Next Lesson - Announcement = `announcement_v1`. | `expected for both students = content_v1, announcement_v1, homework_v1` |
| 4 | In BO, open the target Lesson and open the Report History for each student. Locate the target lesson in the Lesson Report Details list. | The BO Report History row for each student displays Content = `content_v1`, Next Lesson - Homework = `homework_v1`, and Next Lesson - Announcement = `announcement_v1`. | `students = Aiko Tanaka, Haruto Sato; columns = Content, Next Lesson - Homework, Next Lesson - Announcement` |

**Severity:** major
**Priority:** high

---

### [Renseikai] Lesson Report under Lesson – BO Group lesson – Content update – Replaced on every student detail

**Description:** AC 01.2 / AC 01.4 — CRUD and Regression — Updating Content from BO replaces only Content on every student detail and preserves the other shared values.

**Preconditions:**
- Actor: HQ or CM Staff logged in to Back Office.
- Group lesson `LR-57816-BO-02` has students `Aiko Tanaka` and `Haruto Sato`; its source report and both details hold `content_v1`, `announcement_v1`, and `homework_v1`.
- `content_v2 = "Quadratic equations: factoring"`.

| # | Action | Expected Result | Test Data |
| --- | --- | --- | --- |
| 1 | Open Lesson `LR-57816-BO-02` and select **Lesson Report under Lesson**. | The saved Group Lesson Report is open and editable. | `lesson = LR-57816-BO-02; teaching_method = Group` |
| 2 | Replace only Content with `content_v2` and save. | The source report shows `content_v2`; Announcement and Homework remain `announcement_v1` and `homework_v1`. | `changed = content_v2; preserved = announcement_v1, homework_v1` |
| 3 | For Aiko Tanaka and Haruto Sato, open the Student Lesson Allocation record in SF, select **Report History**, and locate the target lesson in the **Lesson Report Details** table. | Each student row displays Content = `content_v2`, Next Lesson - Homework = `homework_v1`, and Next Lesson - Announcement = `announcement_v1`. | `expected for both students = content_v2, announcement_v1, homework_v1` |
| 4 | In BO, open the target Lesson and open the Report History for each student. Locate the target lesson in the Lesson Report Details list. | The BO Report History row for each student displays Content = `content_v2`, Next Lesson - Homework = `homework_v1`, and Next Lesson - Announcement = `announcement_v1`. | `students = Aiko Tanaka, Haruto Sato; columns = Content, Next Lesson - Homework, Next Lesson - Announcement` |

**Severity:** major
**Priority:** high

---

### [Renseikai] Lesson Report under Lesson – BO Group lesson – Announcement update – Replaced on every student detail

**Description:** AC 01.2 / AC 01.4 — CRUD and Regression — Updating Next Lesson's Announcement from BO replaces only that value on every student detail.

**Preconditions:**
- Actor: HQ or CM Staff logged in to Back Office.
- Group lesson `LR-57816-BO-03` has students `Aiko Tanaka` and `Haruto Sato`; its source report and both details hold `content_v1`, `announcement_v1`, and `homework_v1`.
- `announcement_v2 = "Submit quiz by 2026-08-06"`.

| # | Action | Expected Result | Test Data |
| --- | --- | --- | --- |
| 1 | Open Lesson `LR-57816-BO-03` and select **Lesson Report under Lesson**. | The saved Group Lesson Report is open and editable. | `lesson = LR-57816-BO-03; teaching_method = Group` |
| 2 | Replace only Next Lesson's Announcement with `announcement_v2` and save. | The source report shows `announcement_v2`; Content and Homework remain `content_v1` and `homework_v1`. | `changed = announcement_v2; preserved = content_v1, homework_v1` |
| 3 | For Aiko Tanaka and Haruto Sato, open the Student Lesson Allocation record in SF, select **Report History**, and locate the target lesson in the **Lesson Report Details** table. | Each student row displays Content = `content_v1`, Next Lesson - Homework = `homework_v1`, and Next Lesson - Announcement = `announcement_v2`. | `expected for both students = content_v1, announcement_v2, homework_v1` |
| 4 | In BO, open the target Lesson and open the Report History for each student. Locate the target lesson in the Lesson Report Details list. | The BO Report History row for each student displays Content = `content_v1`, Next Lesson - Homework = `homework_v1`, and Next Lesson - Announcement = `announcement_v2`. | `students = Aiko Tanaka, Haruto Sato; columns = Content, Next Lesson - Homework, Next Lesson - Announcement` |

**Severity:** major
**Priority:** high

---

### [Renseikai] Lesson Report under Lesson – BO Group lesson – Homework update – Replaced on every student detail

**Description:** AC 01.2 / AC 01.4 — CRUD and Regression — Updating Next Lesson's Homework from BO replaces only that value on every student detail.

**Preconditions:**
- Actor: HQ or CM Staff logged in to Back Office.
- Group lesson `LR-57816-BO-04` has students `Aiko Tanaka` and `Haruto Sato`; its source report and both details hold `content_v1`, `announcement_v1`, and `homework_v1`.
- `homework_v2 = "Workbook pp. 22-23"`.

| # | Action | Expected Result | Test Data |
| --- | --- | --- | --- |
| 1 | Open Lesson `LR-57816-BO-04` and select **Lesson Report under Lesson**. | The saved Group Lesson Report is open and editable. | `lesson = LR-57816-BO-04; teaching_method = Group` |
| 2 | Replace only Next Lesson's Homework with `homework_v2` and save. | The source report shows `homework_v2`; Content and Announcement remain `content_v1` and `announcement_v1`. | `changed = homework_v2; preserved = content_v1, announcement_v1` |
| 3 | For Aiko Tanaka and Haruto Sato, open the Student Lesson Allocation record in SF, select **Report History**, and locate the target lesson in the **Lesson Report Details** table. | Each student row displays Content = `content_v1`, Next Lesson - Homework = `homework_v2`, and Next Lesson - Announcement = `announcement_v1`. | `expected for both students = content_v1, announcement_v1, homework_v2` |
| 4 | In BO, open the target Lesson and open the Report History for each student. Locate the target lesson in the Lesson Report Details list. | The BO Report History row for each student displays Content = `content_v1`, Next Lesson - Homework = `homework_v2`, and Next Lesson - Announcement = `announcement_v1`. | `students = Aiko Tanaka, Haruto Sato; columns = Content, Next Lesson - Homework, Next Lesson - Announcement` |

**Severity:** major
**Priority:** high

---

### [Renseikai] Lesson Report under Lesson – BO Group lesson – Unrelated field update – Shared values retained

**Description:** AC 01.3 / AC 01.4 — Negative and Regression — Saving Remarks from BO does not clear or change any stored shared value.

**Preconditions:**
- Actor: HQ or CM Staff logged in to Back Office.
- Group lesson `LR-57816-BO-05` has students `Aiko Tanaka` and `Haruto Sato`; its source report and both details hold `content_v1`, `announcement_v1`, and `homework_v1`.
- `remarks_v2 = "Student questions collected for review"`.

| # | Action | Expected Result | Test Data |
| --- | --- | --- | --- |
| 1 | Open Lesson `LR-57816-BO-05` and select **Lesson Report under Lesson**. | The saved Group Lesson Report is open and editable. | `lesson = LR-57816-BO-05; teaching_method = Group` |
| 2 | Replace only Remarks with `remarks_v2` and save. | Remarks shows `remarks_v2`; the source report still shows `content_v1`, `announcement_v1`, and `homework_v1`. | `changed = remarks_v2; retained = content_v1, announcement_v1, homework_v1` |
| 3 | For Aiko Tanaka and Haruto Sato, open the Student Lesson Allocation record in SF, select **Report History**, and locate the target lesson in the **Lesson Report Details** table. | Each student row displays Content = `content_v1`, Next Lesson - Homework = `homework_v1`, and Next Lesson - Announcement = `announcement_v1`. | `expected for both students = content_v1, announcement_v1, homework_v1` |
| 4 | In BO, open the target Lesson and open the Report History for each student. Locate the target lesson in the Lesson Report Details list. | The BO Report History row for each student displays Content = `content_v1`, Next Lesson - Homework = `homework_v1`, and Next Lesson - Announcement = `announcement_v1`. | `students = Aiko Tanaka, Haruto Sato; columns = Content, Next Lesson - Homework, Next Lesson - Announcement` |

**Severity:** major
**Priority:** high
