# Test Cases: LT-57816 — Lesson Report Detail Value Synchronization

## Suite: Lesson Report Detail

### [Renseikai] Lesson Report Detail – SF published Group lesson – Stored shared values – Shown to enrolled student on Learner App

**Description:** AC 01.5 — State Transition and Regression — After the Lesson and Lesson Report are Published, the enrolled student sees the three exact values stored in that student's detail.

**Preconditions:**
- Actor: HQ or CM Staff logged in to Salesforce; `Aiko Tanaka` can log in to the Learner App.
- Group lesson `LR-57816-MOB-SF` is Published; its Lesson Report is Draft and has Aiko Tanaka and Haruto Sato as enrolled students.
- `content_v2 = "Quadratic equations: factoring"`; `announcement_v2 = "Submit quiz by 2026-08-06"`; `homework_v2 = "Workbook pp. 22-23"`.

| # | Action | Expected Result | Test Data |
| --- | --- | --- | --- |
| 1 | Open the Group Lesson Report Detail in SF and save the three shared values. | The source Lesson Report saves `content_v2`, `announcement_v2`, and `homework_v2`. | `lesson = LR-57816-MOB-SF; teaching_method = Group; values = content_v2, announcement_v2, homework_v2` |
| 2 | For Aiko Tanaka and Haruto Sato, open the Student Lesson Allocation record in SF, select **Report History**, and locate the target lesson in the **Lesson Report Details** table. | Each student's row displays Content = `content_v2`, Next Lesson - Homework = `homework_v2`, and Next Lesson - Announcement = `announcement_v2`. | `students = Aiko Tanaka, Haruto Sato; columns = Content, Next Lesson - Homework, Next Lesson - Announcement` |
| 3 | In BO, open the target Lesson and open each student's **Report History**. Locate the target lesson in the Lesson Report Details list. | Each student's BO Report History row displays Content = `content_v2`, Next Lesson - Homework = `homework_v2`, and Next Lesson - Announcement = `announcement_v2`. | `students = Aiko Tanaka, Haruto Sato; columns = Content, Next Lesson - Homework, Next Lesson - Announcement` |
| 4 | Publish the Lesson Report. | Lesson Report status is Published while the Lesson remains Published. | `lesson_status = Published; report_status = Published` |
| 5 | Sign in to the Learner App as Aiko Tanaka and open the lesson report. | Aiko Tanaka sees `content_v2`, `announcement_v2`, and `homework_v2`. | `student = Aiko Tanaka; expected = content_v2, announcement_v2, homework_v2` |

**Severity:** major
**Priority:** high

---

### [Renseikai] Lesson Report Detail – BO published Group lesson – Stored shared values – Shown to enrolled student on Learner App

**Description:** AC 01.5 — State Transition and Regression — After the Lesson and Lesson Report are Published, the enrolled student sees the three exact values stored from BO.

**Preconditions:**
- Actor: HQ or CM Staff logged in to Back Office; `Haruto Sato` can log in to the Learner App.
- Group lesson `LR-57816-MOB-BO` is Published; its Lesson Report is Draft and has Aiko Tanaka and Haruto Sato as enrolled students.
- `content_v2 = "Quadratic equations: factoring"`; `announcement_v2 = "Submit quiz by 2026-08-06"`; `homework_v2 = "Workbook pp. 22-23"`.

| # | Action | Expected Result | Test Data |
| --- | --- | --- | --- |
| 1 | Open the Group Lesson Report Detail in BO and save the three shared values. | The source Lesson Report saves `content_v2`, `announcement_v2`, and `homework_v2`. | `lesson = LR-57816-MOB-BO; teaching_method = Group; values = content_v2, announcement_v2, homework_v2` |
| 2 | For Aiko Tanaka and Haruto Sato, open the Student Lesson Allocation record in SF, select **Report History**, and locate the target lesson in the **Lesson Report Details** table. | Each student's row displays Content = `content_v2`, Next Lesson - Homework = `homework_v2`, and Next Lesson - Announcement = `announcement_v2`. | `students = Aiko Tanaka, Haruto Sato; columns = Content, Next Lesson - Homework, Next Lesson - Announcement` |
| 3 | In BO, open the target Lesson and open each student's **Report History**. Locate the target lesson in the Lesson Report Details list. | Each student's BO Report History row displays Content = `content_v2`, Next Lesson - Homework = `homework_v2`, and Next Lesson - Announcement = `announcement_v2`. | `students = Aiko Tanaka, Haruto Sato; columns = Content, Next Lesson - Homework, Next Lesson - Announcement` |
| 4 | Publish the Lesson Report. | Lesson Report status is Published while the Lesson remains Published. | `lesson_status = Published; report_status = Published` |
| 5 | Sign in to the Learner App as Haruto Sato and open the lesson report. | Haruto Sato sees `content_v2`, `announcement_v2`, and `homework_v2`. | `student = Haruto Sato; expected = content_v2, announcement_v2, homework_v2` |

**Severity:** major
**Priority:** high

---

### [Renseikai] Lesson Report Detail – SF Group lesson – Content update – Replaced for every student

**Description:** AC 01.2 / AC 01.4 — CRUD and Regression — Editing Content from the SF Lesson Report Detail updates every student detail and BO read-back.

**Preconditions:**
- Actor: HQ or CM Staff logged in to Salesforce.
- Group lesson `LR-57816-SFD-01` has students Aiko Tanaka and Haruto Sato; all source and detail values are `content_v1`, `announcement_v1`, and `homework_v1`.
- `content_v2 = "Quadratic equations: factoring"`.

| # | Action | Expected Result | Test Data |
| --- | --- | --- | --- |
| 1 | Open the Group Lesson Report Detail for Lesson `LR-57816-SFD-01` in SF. | The editable Group Lesson Report Detail is shown. | `lesson = LR-57816-SFD-01; teaching_method = Group` |
| 2 | Replace only Content with `content_v2` and save. | The source report shows `content_v2`; Announcement and Homework remain `announcement_v1` and `homework_v1`. | `changed = content_v2; preserved = announcement_v1, homework_v1` |
| 3 | For Aiko Tanaka and Haruto Sato, open the Student Lesson Allocation record in SF, select **Report History**, and locate the target lesson in the **Lesson Report Details** table. | Each student row displays Content = `content_v2`, Next Lesson - Homework = `homework_v1`, and Next Lesson - Announcement = `announcement_v1`. | `expected for both students = content_v2, announcement_v1, homework_v1` |
| 4 | In BO, open the target Lesson and open the Report History for each student. Locate the target lesson in the Lesson Report Details list. | The BO Report History row for each student displays Content = `content_v2`, Next Lesson - Homework = `homework_v1`, and Next Lesson - Announcement = `announcement_v1`. | `students = Aiko Tanaka, Haruto Sato; columns = Content, Next Lesson - Homework, Next Lesson - Announcement` |

**Severity:** major
**Priority:** high

---

### [Renseikai] Lesson Report Detail – SF Group lesson – Announcement update – Replaced for every student

**Description:** AC 01.2 / AC 01.4 — CRUD and Regression — Editing Next Lesson's Announcement from the SF Lesson Report Detail updates every student detail and BO read-back.

**Preconditions:**
- Actor: HQ or CM Staff logged in to Salesforce.
- Group lesson `LR-57816-SFD-02` has students Aiko Tanaka and Haruto Sato; all source and detail values are `content_v1`, `announcement_v1`, and `homework_v1`.
- `announcement_v2 = "Submit quiz by 2026-08-06"`.

| # | Action | Expected Result | Test Data |
| --- | --- | --- | --- |
| 1 | Open the Group Lesson Report Detail for Lesson `LR-57816-SFD-02` in SF. | The editable Group Lesson Report Detail is shown. | `lesson = LR-57816-SFD-02; teaching_method = Group` |
| 2 | Replace only Next Lesson's Announcement with `announcement_v2` and save. | The source report shows `announcement_v2`; Content and Homework remain `content_v1` and `homework_v1`. | `changed = announcement_v2; preserved = content_v1, homework_v1` |
| 3 | For Aiko Tanaka and Haruto Sato, open the Student Lesson Allocation record in SF, select **Report History**, and locate the target lesson in the **Lesson Report Details** table. | Each student row displays Content = `content_v1`, Next Lesson - Homework = `homework_v1`, and Next Lesson - Announcement = `announcement_v2`. | `expected for both students = content_v1, announcement_v2, homework_v1` |
| 4 | In BO, open the target Lesson and open the Report History for each student. Locate the target lesson in the Lesson Report Details list. | The BO Report History row for each student displays Content = `content_v1`, Next Lesson - Homework = `homework_v1`, and Next Lesson - Announcement = `announcement_v2`. | `students = Aiko Tanaka, Haruto Sato; columns = Content, Next Lesson - Homework, Next Lesson - Announcement` |

**Severity:** major
**Priority:** high

---

### [Renseikai] Lesson Report Detail – SF Group lesson – Homework update – Replaced for every student

**Description:** AC 01.2 / AC 01.4 — CRUD and Regression — Editing Next Lesson's Homework from the SF Lesson Report Detail updates every student detail and BO read-back.

**Preconditions:**
- Actor: HQ or CM Staff logged in to Salesforce.
- Group lesson `LR-57816-SFD-03` has students Aiko Tanaka and Haruto Sato; all source and detail values are `content_v1`, `announcement_v1`, and `homework_v1`.
- `homework_v2 = "Workbook pp. 22-23"`.

| # | Action | Expected Result | Test Data |
| --- | --- | --- | --- |
| 1 | Open the Group Lesson Report Detail for Lesson `LR-57816-SFD-03` in SF. | The editable Group Lesson Report Detail is shown. | `lesson = LR-57816-SFD-03; teaching_method = Group` |
| 2 | Replace only Next Lesson's Homework with `homework_v2` and save. | The source report shows `homework_v2`; Content and Announcement remain `content_v1` and `announcement_v1`. | `changed = homework_v2; preserved = content_v1, announcement_v1` |
| 3 | For Aiko Tanaka and Haruto Sato, open the Student Lesson Allocation record in SF, select **Report History**, and locate the target lesson in the **Lesson Report Details** table. | Each student row displays Content = `content_v1`, Next Lesson - Homework = `homework_v2`, and Next Lesson - Announcement = `announcement_v1`. | `expected for both students = content_v1, announcement_v1, homework_v2` |
| 4 | In BO, open the target Lesson and open the Report History for each student. Locate the target lesson in the Lesson Report Details list. | The BO Report History row for each student displays Content = `content_v1`, Next Lesson - Homework = `homework_v2`, and Next Lesson - Announcement = `announcement_v1`. | `students = Aiko Tanaka, Haruto Sato; columns = Content, Next Lesson - Homework, Next Lesson - Announcement` |

**Severity:** major
**Priority:** high

---

### [Renseikai] Lesson Report Detail – SF Group lesson – Unrelated field update – Shared values retained

**Description:** AC 01.3 / AC 01.4 — Negative and Regression — Saving Remarks from the SF Lesson Report Detail preserves the three stored shared values for every student.

**Preconditions:**
- Actor: HQ or CM Staff logged in to Salesforce.
- Group lesson `LR-57816-SFD-04` has students Aiko Tanaka and Haruto Sato; all source and detail values are `content_v1`, `announcement_v1`, and `homework_v1`.
- `remarks_v2 = "Student questions collected for review"`.

| # | Action | Expected Result | Test Data |
| --- | --- | --- | --- |
| 1 | Open the Group Lesson Report Detail for Lesson `LR-57816-SFD-04` in SF. | The editable Group Lesson Report Detail is shown. | `lesson = LR-57816-SFD-04; teaching_method = Group` |
| 2 | Replace only Remarks with `remarks_v2` and save. | Remarks shows `remarks_v2`; the source report retains `content_v1`, `announcement_v1`, and `homework_v1`. | `changed = remarks_v2; retained = content_v1, announcement_v1, homework_v1` |
| 3 | For Aiko Tanaka and Haruto Sato, open the Student Lesson Allocation record in SF, select **Report History**, and locate the target lesson in the **Lesson Report Details** table. | Each student row displays Content = `content_v1`, Next Lesson - Homework = `homework_v1`, and Next Lesson - Announcement = `announcement_v1`. | `expected for both students = content_v1, announcement_v1, homework_v1` |
| 4 | In BO, open the target Lesson and open the Report History for each student. Locate the target lesson in the Lesson Report Details list. | The BO Report History row for each student displays Content = `content_v1`, Next Lesson - Homework = `homework_v1`, and Next Lesson - Announcement = `announcement_v1`. | `students = Aiko Tanaka, Haruto Sato; columns = Content, Next Lesson - Homework, Next Lesson - Announcement` |

**Severity:** major
**Priority:** high

---

### [Renseikai] Lesson Report Detail – BO Group lesson – Content update – Replaced for every student

**Description:** AC 01.2 / AC 01.4 — CRUD and Regression — Editing Content from the BO Lesson Report Detail updates every student detail and SF read-back.

**Preconditions:**
- Actor: HQ or CM Staff logged in to Back Office.
- Group lesson `LR-57816-BOD-01` has students Aiko Tanaka and Haruto Sato; all source and detail values are `content_v1`, `announcement_v1`, and `homework_v1`.
- `content_v2 = "Quadratic equations: factoring"`.

| # | Action | Expected Result | Test Data |
| --- | --- | --- | --- |
| 1 | Open the Group Lesson Report Detail for Lesson `LR-57816-BOD-01` in BO. | The editable Group Lesson Report Detail is shown. | `lesson = LR-57816-BOD-01; teaching_method = Group` |
| 2 | Replace only Content with `content_v2` and save. | The source report shows `content_v2`; Announcement and Homework remain `announcement_v1` and `homework_v1`. | `changed = content_v2; preserved = announcement_v1, homework_v1` |
| 3 | For Aiko Tanaka and Haruto Sato, open the Student Lesson Allocation record in SF, select **Report History**, and locate the target lesson in the **Lesson Report Details** table. | Each student row displays Content = `content_v2`, Next Lesson - Homework = `homework_v1`, and Next Lesson - Announcement = `announcement_v1`. | `expected for both students = content_v2, announcement_v1, homework_v1` |
| 4 | In BO, open the target Lesson and open the Report History for each student. Locate the target lesson in the Lesson Report Details list. | The BO Report History row for each student displays Content = `content_v2`, Next Lesson - Homework = `homework_v1`, and Next Lesson - Announcement = `announcement_v1`. | `students = Aiko Tanaka, Haruto Sato; columns = Content, Next Lesson - Homework, Next Lesson - Announcement` |

**Severity:** major
**Priority:** high

---

### [Renseikai] Lesson Report Detail – BO Group lesson – Announcement update – Replaced for every student

**Description:** AC 01.2 / AC 01.4 — CRUD and Regression — Editing Next Lesson's Announcement from the BO Lesson Report Detail updates every student detail and SF read-back.

**Preconditions:**
- Actor: HQ or CM Staff logged in to Back Office.
- Group lesson `LR-57816-BOD-02` has students Aiko Tanaka and Haruto Sato; all source and detail values are `content_v1`, `announcement_v1`, and `homework_v1`.
- `announcement_v2 = "Submit quiz by 2026-08-06"`.

| # | Action | Expected Result | Test Data |
| --- | --- | --- | --- |
| 1 | Open the Group Lesson Report Detail for Lesson `LR-57816-BOD-02` in BO. | The editable Group Lesson Report Detail is shown. | `lesson = LR-57816-BOD-02; teaching_method = Group` |
| 2 | Replace only Next Lesson's Announcement with `announcement_v2` and save. | The source report shows `announcement_v2`; Content and Homework remain `content_v1` and `homework_v1`. | `changed = announcement_v2; preserved = content_v1, homework_v1` |
| 3 | For Aiko Tanaka and Haruto Sato, open the Student Lesson Allocation record in SF, select **Report History**, and locate the target lesson in the **Lesson Report Details** table. | Each student row displays Content = `content_v1`, Next Lesson - Homework = `homework_v1`, and Next Lesson - Announcement = `announcement_v2`. | `expected for both students = content_v1, announcement_v2, homework_v1` |
| 4 | In BO, open the target Lesson and open the Report History for each student. Locate the target lesson in the Lesson Report Details list. | The BO Report History row for each student displays Content = `content_v1`, Next Lesson - Homework = `homework_v1`, and Next Lesson - Announcement = `announcement_v2`. | `students = Aiko Tanaka, Haruto Sato; columns = Content, Next Lesson - Homework, Next Lesson - Announcement` |

**Severity:** major
**Priority:** high

---

### [Renseikai] Lesson Report Detail – BO Group lesson – Homework update – Replaced for every student

**Description:** AC 01.2 / AC 01.4 — CRUD and Regression — Editing Next Lesson's Homework from the BO Lesson Report Detail updates every student detail and SF read-back.

**Preconditions:**
- Actor: HQ or CM Staff logged in to Back Office.
- Group lesson `LR-57816-BOD-03` has students Aiko Tanaka and Haruto Sato; all source and detail values are `content_v1`, `announcement_v1`, and `homework_v1`.
- `homework_v2 = "Workbook pp. 22-23"`.

| # | Action | Expected Result | Test Data |
| --- | --- | --- | --- |
| 1 | Open the Group Lesson Report Detail for Lesson `LR-57816-BOD-03` in BO. | The editable Group Lesson Report Detail is shown. | `lesson = LR-57816-BOD-03; teaching_method = Group` |
| 2 | Replace only Next Lesson's Homework with `homework_v2` and save. | The source report shows `homework_v2`; Content and Announcement remain `content_v1` and `announcement_v1`. | `changed = homework_v2; preserved = content_v1, announcement_v1` |
| 3 | For Aiko Tanaka and Haruto Sato, open the Student Lesson Allocation record in SF, select **Report History**, and locate the target lesson in the **Lesson Report Details** table. | Each student row displays Content = `content_v1`, Next Lesson - Homework = `homework_v2`, and Next Lesson - Announcement = `announcement_v1`. | `expected for both students = content_v1, announcement_v1, homework_v2` |
| 4 | In BO, open the target Lesson and open the Report History for each student. Locate the target lesson in the Lesson Report Details list. | The BO Report History row for each student displays Content = `content_v1`, Next Lesson - Homework = `homework_v2`, and Next Lesson - Announcement = `announcement_v1`. | `students = Aiko Tanaka, Haruto Sato; columns = Content, Next Lesson - Homework, Next Lesson - Announcement` |

**Severity:** major
**Priority:** high

---

### [Renseikai] Lesson Report Detail – BO Group lesson – Unrelated field update – Shared values retained

**Description:** AC 01.3 / AC 01.4 — Negative and Regression — Saving Remarks from the BO Lesson Report Detail preserves the three stored shared values for every student.

**Preconditions:**
- Actor: HQ or CM Staff logged in to Back Office.
- Group lesson `LR-57816-BOD-04` has students Aiko Tanaka and Haruto Sato; all source and detail values are `content_v1`, `announcement_v1`, and `homework_v1`.
- `remarks_v2 = "Student questions collected for review"`.

| # | Action | Expected Result | Test Data |
| --- | --- | --- | --- |
| 1 | Open the Group Lesson Report Detail for Lesson `LR-57816-BOD-04` in BO. | The editable Group Lesson Report Detail is shown. | `lesson = LR-57816-BOD-04; teaching_method = Group` |
| 2 | Replace only Remarks with `remarks_v2` and save. | Remarks shows `remarks_v2`; the source report retains `content_v1`, `announcement_v1`, and `homework_v1`. | `changed = remarks_v2; retained = content_v1, announcement_v1, homework_v1` |
| 3 | For Aiko Tanaka and Haruto Sato, open the Student Lesson Allocation record in SF, select **Report History**, and locate the target lesson in the **Lesson Report Details** table. | Each student row displays Content = `content_v1`, Next Lesson - Homework = `homework_v1`, and Next Lesson - Announcement = `announcement_v1`. | `expected for both students = content_v1, announcement_v1, homework_v1` |
| 4 | In BO, open the target Lesson and open the Report History for each student. Locate the target lesson in the Lesson Report Details list. | The BO Report History row for each student displays Content = `content_v1`, Next Lesson - Homework = `homework_v1`, and Next Lesson - Announcement = `announcement_v1`. | `students = Aiko Tanaka, Haruto Sato; columns = Content, Next Lesson - Homework, Next Lesson - Announcement` |

**Severity:** major
**Priority:** high
