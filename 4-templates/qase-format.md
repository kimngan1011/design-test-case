# Qase Format Reference – Lesson Syllabus

> **Source:** `qase-format.csv`  
> **Suite:** Lesson Syllabus (suite_id: 376, parent_id: 371)

---

## CSV Column Reference

| Column | Description |
|--------|------------|
| v2.id | Qase test case ID |
| title | Test case title |
| description | Detailed description |
| preconditions | Required setup before execution |
| postconditions | State after execution |
| tags | Labels for filtering |
| priority | high / medium / low / undefined |
| severity | blocker / critical / major / normal / minor / trivial |
| type | functional / regression / etc. |
| behavior | undefined / positive / negative / destructive |
| automation | is-not-automated / automated / to-be-automated |
| status | draft / actual / deprecated |
| is_flaky | yes / no |
| layer | unknown / e2e / api / unit |
| steps_type | classic / gherkin |
| steps_actions | Numbered step actions |
| steps_result | Expected result per step |
| steps_data | Test data per step |
| milestone_id | Milestone reference |
| milestone | Milestone name |
| suite_id | Suite ID |
| suite_parent_id | Parent suite ID |
| suite | Suite name |
| suite_without_cases | 1 = suite-only row (no test case) |
| parameters | Parameterized test values |
| is_muted | yes / no |
| cf_2 | Custom field 2 |
| cf_3 | Custom field 3 |

---

## Test Cases

### TC-2839: Register a new syllabus master

| Field | Value |
|-------|-------|
| **Priority** | high |
| **Severity** | critical |
| **Type** | functional |
| **Behavior** | undefined |
| **Automation** | is-not-automated |
| **Status** | draft |
| **Is Flaky** | no |
| **Layer** | unknown |
| **Steps Type** | classic |

| Step | Action | Expected Result | Test Data |
|------|--------|----------------|-----------|
| 1 | Open Syllabus Master tab | — | — |
| 2 | Create a syllabus master | User sees syllabus master is created successfully | — |

---

### TC-6387: Import a new syllabus master

| Field | Value |
|-------|-------|
| **Tags** | csv_import |
| **Priority** | high |
| **Severity** | critical |
| **Type** | functional |
| **Behavior** | undefined |
| **Automation** | is-not-automated |
| **Status** | draft |
| **Is Flaky** | no |
| **Layer** | unknown |
| **Steps Type** | classic |

| Step | Action | Expected Result | Test Data |
|------|--------|----------------|-----------|
| 1 | Open Syllabus Master tab | — | — |
| 2 | Import a syllabus master | User sees syllabus master is created successfully | — |

---

### TC-2840: Register a new syllabus detail

| Field | Value |
|-------|-------|
| **Preconditions** | User has created a syllabus master |
| **Priority** | high |
| **Severity** | critical |
| **Type** | functional |
| **Behavior** | undefined |
| **Automation** | is-not-automated |
| **Status** | draft |
| **Is Flaky** | no |
| **Layer** | unknown |
| **Steps Type** | classic |

| Step | Action | Expected Result | Test Data |
|------|--------|----------------|-----------|
| 1 | Open syllabus master detail | — | — |
| 2 | Create a Syllabus Detail | User sees syllabus detail is created successfully | Syllabus Code: 1, Syllabus Description: これはテスト用に作成された日本語のサンプル文章です。文字数が正確に500文字になるように構成されています。長いテキスト入力や改行の処理、マルチバイト文字の表示確認など、さまざまな自動化テストや検証に使用できます。この文をコピーして、フォームやテキストエリアに貼り付けて試すことで、アプリケーションの入力制限やレイアウトの影響を確認することができます。文字数やエンコーディングの影響も重要な要素となるため、正確な処理が求められます。 |

---

### TC-6388: Import a new syllabus detail

| Field | Value |
|-------|-------|
| **Preconditions** | User has created a syllabus master |
| **Tags** | csv_import |
| **Priority** | high |
| **Severity** | critical |
| **Type** | functional |
| **Behavior** | undefined |
| **Automation** | is-not-automated |
| **Status** | draft |
| **Is Flaky** | no |
| **Layer** | unknown |
| **Steps Type** | classic |

| Step | Action | Expected Result | Test Data |
|------|--------|----------------|-----------|
| 1 | Open syllabus detail tab | — | — |
| 2 | Prepare CSV file and import | User sees syllabus detail is created successfully | Syllabus Code: 1,2,3,4,...,100; Syllabus Description: これはテスト用に作成された日本語のサンプル文章です。(500文字 JP sample text) |

---

### TC-2841: Associate a syllabus master to a course master

| Field | Value |
|-------|-------|
| **Preconditions** | User has created a course master, syllabus master+syllabus detail |
| **Priority** | high |
| **Severity** | critical |
| **Type** | functional |
| **Behavior** | undefined |
| **Automation** | is-not-automated |
| **Status** | draft |
| **Is Flaky** | no |
| **Layer** | unknown |
| **Steps Type** | classic |

| Step | Action | Expected Result | Test Data |
|------|--------|----------------|-----------|
| 1 | Open course master detail | — | — |
| 2 | Associated syllabus master | User sees syllabus master is associated to course master | — |

---

### TC-6389: Import a course master with syllabus master

| Field | Value |
|-------|-------|
| **Preconditions** | User has created a course master, syllabus master+syllabus detail |
| **Tags** | csv_import |
| **Priority** | high |
| **Severity** | critical |
| **Type** | functional |
| **Behavior** | undefined |
| **Automation** | is-not-automated |
| **Status** | draft |
| **Is Flaky** | no |
| **Layer** | unknown |
| **Steps Type** | classic |

| Step | Action | Expected Result | Test Data |
|------|--------|----------------|-----------|
| 1 | Open course master tab | — | — |
| 2 | Prepare CSV file and import | User sees course master with syllabus master is created successfully | — |

---

### TC-2842: Create an one-time group lesson with syllabus detail

| Field | Value |
|-------|-------|
| **Preconditions** | User has associated syllabus master to course master |
| **Priority** | high |
| **Severity** | critical |
| **Type** | functional |
| **Behavior** | undefined |
| **Automation** | is-not-automated |
| **Status** | draft |
| **Is Flaky** | no |
| **Layer** | unknown |
| **Steps Type** | classic |

| Step | Action | Expected Result | Test Data |
|------|--------|----------------|-----------|
| 1 | Create an one-time group lesson with lesson code = syllabus code | User sees auto-fill lesson's syllabus description = syllabus detail's syllabus description follow lesson code and syllabus code | — |

---

### TC-2843: Create a recurring group lesson with syllabus detail on Calendar

| Field | Value |
|-------|-------|
| **Preconditions** | User has associated syllabus master to course master |
| **Priority** | high |
| **Severity** | critical |
| **Type** | functional |
| **Behavior** | undefined |
| **Automation** | is-not-automated |
| **Status** | draft |
| **Is Flaky** | no |
| **Layer** | unknown |
| **Steps Type** | classic |

| Step | Action | Expected Result | Test Data |
|------|--------|----------------|-----------|
| 1 | Create a recurring group lesson with lesson code = syllabus code on Calendar | User sees auto-fill lesson's syllabus description = syllabus detail's syllabus description in all lessons follow lesson code and syllabus code | — |

---

### TC-2844: Create a lesson course schedule with syllabus detail

| Field | Value |
|-------|-------|
| **Preconditions** | User has associated syllabus master to course master |
| **Priority** | high |
| **Severity** | critical |
| **Type** | functional |
| **Behavior** | undefined |
| **Automation** | is-not-automated |
| **Status** | draft |
| **Is Flaky** | no |
| **Layer** | unknown |
| **Steps Type** | classic |

| Step | Action | Expected Result | Test Data |
|------|--------|----------------|-----------|
| 1 | Create a group lesson course schedule with lesson code = syllabus code | User sees auto-fill lesson's syllabus description = syllabus detail's syllabus description in all lessons follow lesson code and syllabus code | — |

---

### TC-2845: Add lesson in lesson schedule with syllabus detail

| Field | Value |
|-------|-------|
| **Preconditions** | User has associated syllabus master to course master; User has created a recurring group lesson |
| **Priority** | high |
| **Severity** | critical |
| **Type** | functional |
| **Behavior** | undefined |
| **Automation** | is-not-automated |
| **Status** | draft |
| **Is Flaky** | no |
| **Layer** | unknown |
| **Steps Type** | classic |

| Step | Action | Expected Result | Test Data |
|------|--------|----------------|-----------|
| 1 | Open lesson schedule, add lesson with lesson code to lesson schedule | User sees auto-fill lesson's syllabus description = syllabus detail's syllabus description in all lessons follow lesson code and syllabus code | — |

---

### TC-2846: Import an one-time lesson with syllabus detail

| Field | Value |
|-------|-------|
| **Preconditions** | User has associated syllabus master to course master |
| **Tags** | csv_import |
| **Priority** | high |
| **Severity** | critical |
| **Type** | functional |
| **Behavior** | undefined |
| **Automation** | is-not-automated |
| **Status** | draft |
| **Is Flaky** | no |
| **Layer** | unknown |
| **Steps Type** | classic |

| Step | Action | Expected Result | Test Data |
|------|--------|----------------|-----------|
| 1 | Prepare CSV file with: One-time group lesson and lesson code, Recurring group lesson and lesson code | — | — |
| 2 | Import the file | — | — |
| 3 | Check one-time lesson | User sees auto-fill lesson's syllabus description = syllabus detail's syllabus description follow lesson code and syllabus code | — |
| 4 | Check recurring lesson | User sees auto-fill lesson's syllabus description = syllabus detail's syllabus description in all lessons follow lesson code and syllabus code | — |

---

### TC-2848: Create an lesson with lesson code but no matching syllabus detail

| Field | Value |
|-------|-------|
| **Preconditions** | User has associated syllabus master to course master |
| **Priority** | medium |
| **Severity** | major |
| **Type** | functional |
| **Behavior** | undefined |
| **Automation** | is-not-automated |
| **Status** | draft |
| **Is Flaky** | no |
| **Layer** | unknown |
| **Steps Type** | classic |

| Step | Action | Expected Result | Test Data |
|------|--------|----------------|-----------|
| 1 | Create an lesson with lesson code but no matching syllabus detail | User sees syllabus description as blank | — |

---

### TC-2849: Create an lesson without lesson code

| Field | Value |
|-------|-------|
| **Preconditions** | User has associated syllabus master to course master |
| **Priority** | medium |
| **Severity** | major |
| **Type** | functional |
| **Behavior** | undefined |
| **Automation** | is-not-automated |
| **Status** | draft |
| **Is Flaky** | no |
| **Layer** | unknown |
| **Steps Type** | classic |

| Step | Action | Expected Result | Test Data |
|------|--------|----------------|-----------|
| 1 | Create an lesson without lesson code | User sees syllabus description as blank | — |

---

### TC-2850: Edit lesson code after generating syllabus detail with only this lesson

| Field | Value |
|-------|-------|
| **Preconditions** | User has created recurring group lesson with lesson syllabus |
| **Priority** | medium |
| **Severity** | major |
| **Type** | functional |
| **Behavior** | undefined |
| **Automation** | is-not-automated |
| **Status** | draft |
| **Is Flaky** | no |
| **Layer** | unknown |
| **Steps Type** | classic |

| Step | Action | Expected Result | Test Data |
|------|--------|----------------|-----------|
| 1 | Open lesson detail and edit lesson code with only this | User sees syllabus description with no change | — |

---

### TC-2851: Edit lesson code after generating syllabus detail with this and the following

| Field | Value |
|-------|-------|
| **Preconditions** | User has created recurring group lesson with lesson syllabus |
| **Priority** | medium |
| **Severity** | major |
| **Type** | functional |
| **Behavior** | undefined |
| **Automation** | is-not-automated |
| **Status** | draft |
| **Is Flaky** | no |
| **Layer** | unknown |
| **Steps Type** | classic |

| Step | Action | Expected Result | Test Data |
|------|--------|----------------|-----------|
| 1 | Open lesson detail and edit lesson code with following lessons | User sees syllabus description with no change in all lessons | — |

---

### TC-2852: Edit syllabus detail in lesson with only this lesson

| Field | Value |
|-------|-------|
| **Preconditions** | User has created recurring group lesson with lesson syllabus |
| **Priority** | medium |
| **Severity** | major |
| **Type** | functional |
| **Behavior** | undefined |
| **Automation** | is-not-automated |
| **Status** | draft |
| **Is Flaky** | no |
| **Layer** | unknown |
| **Steps Type** | classic |

| Step | Action | Expected Result | Test Data |
|------|--------|----------------|-----------|
| 1 | Open lesson detail and edit syllabus description with only this | User sees lesson syllabus is updated in selected lesson | — |
| 2 | Check other lessons | User sees syllabus description with no change | — |

---

### TC-2853: Edit syllabus detail in lesson with this and the following

| Field | Value |
|-------|-------|
| **Preconditions** | User has created recurring group lesson with lesson syllabus |
| **Priority** | medium |
| **Severity** | major |
| **Type** | functional |
| **Behavior** | undefined |
| **Automation** | is-not-automated |
| **Status** | draft |
| **Is Flaky** | no |
| **Layer** | unknown |
| **Steps Type** | classic |

| Step | Action | Expected Result | Test Data |
|------|--------|----------------|-----------|
| 1 | Open the 2nd lesson, edit lesson syllabus and another fields (lesson date&time, lesson name,...) with following lessons | User sees lesson syllabus is updated in selected lesson | — |
| 2 | Check other lessons | User sees syllabus description with no change | — |

---

### TC-2854: Change syllabus master in course master after generating in lesson

| Field | Value |
|-------|-------|
| **Preconditions** | User has created recurring group lesson with lesson syllabus |
| **Priority** | medium |
| **Severity** | major |
| **Type** | functional |
| **Behavior** | undefined |
| **Automation** | is-not-automated |
| **Status** | draft |
| **Is Flaky** | no |
| **Layer** | unknown |
| **Steps Type** | classic |

| Step | Action | Expected Result | Test Data |
|------|--------|----------------|-----------|
| 1 | Open course master, change syllabus master | — | — |
| 2 | Open the previous lesson | User sees syllabus description with no change | — |
| 3 | Create a new group lesson with the course master | User sees auto-fill the new syllabus description | — |

---

### TC-2855: Change syllabus code in syllabus detail

| Field | Value |
|-------|-------|
| **Preconditions** | User has created recurring group lesson with lesson syllabus |
| **Priority** | medium |
| **Severity** | major |
| **Type** | functional |
| **Behavior** | undefined |
| **Automation** | is-not-automated |
| **Status** | draft |
| **Is Flaky** | no |
| **Layer** | unknown |
| **Steps Type** | classic |

| Step | Action | Expected Result | Test Data |
|------|--------|----------------|-----------|
| 1 | Open syllabus detail, change syllabus code | — | — |
| 2 | Open the previous lesson | User sees syllabus description with no change | — |
| 3 | Create a new group lesson with the course master | User sees auto-fill the new syllabus description follow the new syllabus code | — |

---

### TC-2856: Change syllabus description in syllabus detail

| Field | Value |
|-------|-------|
| **Preconditions** | User has created recurring group lesson with lesson syllabus |
| **Priority** | medium |
| **Severity** | major |
| **Type** | functional |
| **Behavior** | undefined |
| **Automation** | is-not-automated |
| **Status** | draft |
| **Is Flaky** | no |
| **Layer** | unknown |
| **Steps Type** | classic |

| Step | Action | Expected Result | Test Data |
|------|--------|----------------|-----------|
| 1 | Open syllabus detail, change syllabus description | — | — |
| 2 | Open the previous lesson | User sees syllabus description with no change | — |
| 3 | Create a new group lesson with the course master | User sees auto-fill the new syllabus description | — |

---

### TC-6414: Verify lesson syllabus on BO

| Field | Value |
|-------|-------|
| **Priority** | high |
| **Severity** | critical |
| **Type** | functional |
| **Behavior** | undefined |
| **Automation** | is-not-automated |
| **Status** | draft |
| **Is Flaky** | no |
| **Layer** | unknown |
| **Steps Type** | classic |

| Step | Action | Expected Result | Test Data |
|------|--------|----------------|-----------|
| 1 | Create a group lesson with lesson syllabus | — | — |
| 1.1 | Login BO and open the lesson | User sees syllabus description with view-only | — |
| 1.2 | Login BO and open the lesson on Calendar | User sees syllabus description with view-only | — |
| 2 | Edit syllabus description | — | — |
| 2.1 | Login BO and open the lesson | User sees syllabus description is updated | — |
| 2.2 | Login BO and open the lesson on Calendar | User sees syllabus description is updated | — |

---

### TC-6415: Verify lesson syllabus on Mobile

| Field | Value |
|-------|-------|
| **Priority** | high |
| **Severity** | critical |
| **Type** | functional |
| **Behavior** | undefined |
| **Automation** | is-not-automated |
| **Status** | draft |
| **Is Flaky** | no |
| **Layer** | unknown |
| **Steps Type** | classic |

| Step | Action | Expected Result | Test Data |
|------|--------|----------------|-----------|
| 1 | Published a group lesson with lesson syllabus and student | — | — |
| 1.1 | Login Mobile and open the lesson | User sees syllabus description with view-only | — |
| 2 | Edit syllabus description | — | — |
| 2.1 | Login Mobile and open the lesson | User sees syllabus description is updated | — |

---

### TC-6432: Edit lesson with lesson syllabus on BO

| Field | Value |
|-------|-------|
| **Preconditions** | User has created a group lesson with lesson syllabus |
| **Priority** | high |
| **Severity** | critical |
| **Type** | functional |
| **Behavior** | undefined |
| **Automation** | is-not-automated |
| **Status** | draft |
| **Is Flaky** | no |
| **Layer** | unknown |
| **Steps Type** | classic |

| Step | Action | Expected Result | Test Data |
|------|--------|----------------|-----------|
| 1 | Login BO and edit lesson | User still sees the syllabus description | — |

---

### TC-8541: Create a daily/weekly/custom lesson with syllabus detail

| Field | Value |
|-------|-------|
| **Priority** | undefined |
| **Severity** | major |
| **Type** | functional |
| **Behavior** | undefined |
| **Automation** | is-not-automated |
| **Status** | draft |
| **Is Flaky** | no |
| **Layer** | unknown |
| **Steps Type** | classic |

*(No steps defined yet)*
