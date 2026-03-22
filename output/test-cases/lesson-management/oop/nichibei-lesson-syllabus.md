# Lesson Syllabus

## Lesson Syllabus

### TC-2839: Register a new syllabus master

**Preconditions:** -

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Open Syllabus Master ta | - | - |
| 2 | Create a syllabus maste | User sees syllabus master is created successfully | - |

---

### TC-6387: Import a new syllabus master

**Preconditions:** -

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Open Syllabus Master ta | - | - |
| 2 | Import a syllabus maste | User sees syllabus master is created successfully | - |

---

### TC-2840: Register a new syllabus detail

**Preconditions:**

User has created a syllabus master

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Open syllabus master detail | - | - |
| 2 | Create a Syllabus Detail | User sees syllabus detail is created successfully | Syllabus Code: 1<br>Syllabus Description: <br>これはテスト用に作成された日本語のサンプル文章です。文字数が正確に500文字になるように構成されています。長いテキスト入力や改行の処理、マルチバイト文字の表示確認など、さまざまな自動化テストや検証に使用できます。この文をコピーして、フォームやテキストエリアに貼り付けて試すことで、アプリケーションの入力制限やレイアウトの影響を確認することができます。文字数やエンコーディングの影響も重要な要素となるため、正確な処理が求められます。 |

---

### TC-6388: Import a new syllabus detail

**Preconditions:**

User has created a syllabus master

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Open syllabus detail ta | - | - |
| 2 | Prepare CSV file and import | User sees syllabus detail is created successfully | Syllabus Code: 1,2,3,4,...,100<br>Syllabus Description:<br>これはテスト用に作成された日本語のサンプル文章です。文字数が正確に500文字になるように構成されています。長いテキスト入力や改行の処理、マルチバイト文字の表示確認など、さまざまな自動化テストや検証に使用できます。この文をコピーして、フォームやテキストエリアに貼り付けて試すことで、アプリケーションの入力制限やレイアウトの影響を確認することができます。文字数やエンコーディングの影響も重要な要素となるため、正確な処理が求められます。 |

---

### TC-2841: Associate a syllabus master to a course master

**Preconditions:**

User has created a course master, syllabus master+syllabus detail

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Open course master detail | - | - |
| 2 | Associated syllabus maste | User sees syllabus master is associated to course maste | - |

---

### TC-6389: Import a course master with syllabus master

**Preconditions:**

User has created a course master, syllabus master+syllabus detail

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Open course master ta | - | - |
| 2 | Prepare CSV file and import | User sees course master with syllabus master is created successfully | - |

---

### TC-2842: Create an one-time group lesson with syllabus detail

**Preconditions:**

User has associated syllabus master to course master

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Create an one-time group lesson with lesson code = syllabus code | User sees auto-fill lesson's syllabus description = syllabus detail's syllabus description follow lesson code and syllabus code | - |

---

### TC-2843: Create a recurring group lesson with syllabus detail on Calendar

**Preconditions:**

User has associated syllabus master to course master

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Create a recurring group lesson with lesson code = syllabus code on Calenda | User sees auto-fill lesson's syllabus description = syllabus detail's syllabus description in all lessons follow lesson code and syllabus code | - |

---

### TC-2844: Create a lesson course schedule with syllabus detail

**Preconditions:**

User has associated syllabus master to course master

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Create a group lesson course schedule with lesson code = syllabus code | User sees auto-fill lesson's syllabus description = syllabus detail's syllabus description in all lessons follow lesson code and syllabus code | - |

---

### TC-2845: Add lesson in lesson schedule with syllabus detail

**Preconditions:**

User has associated syllabus master to course master
User has created a recurring group lesson

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Open lesson schedule, add lesson with lesson code to lesson schedule | User sees auto-fill lesson's syllabus description = syllabus detail's syllabus description in all lessons follow lesson code and syllabus code | - |

---

### TC-2846: Import an one-time lesson with syllabus detail

**Preconditions:**

User has associated syllabus master to course master

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Prepare CSV file with <br><br>* One-time group lesson and lesson code<br>* Recurring group lesson and lesson code | - | - |
| 2 | Import the file | - | - |
| 3 | Check one-time lesson | User sees auto-fill lesson's syllabus description = syllabus detail's syllabus description follow lesson code and syllabus code | - |
| 4 | Check recurring lesson | User sees auto-fill lesson's syllabus description = syllabus detail's syllabus description in all lessons follow lesson code and syllabus code | - |

---

### TC-2848: Create an lesson with lesson code but no matching syllabus detail

**Preconditions:**

User has associated syllabus master to course master

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Create an lesson with lesson code but no matching syllabus detail | User sees syllabus description as blank | - |

---

### TC-2849: Create an lesson without lesson code

**Preconditions:**

User has associated syllabus master to course master

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Create an lesson without lesson code | User sees syllabus description as blank | - |

---

### TC-2850: Edit lesson code after generating syllabus detail with only this lesson

**Preconditions:**

User has created recurring group lesson with lesson syllabus

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Open lesson detail and edit lesson code with only this | User sees syllabus description with no change | - |

---

### TC-2851: Edit lesson code after generating syllabus detail with this and the following

**Preconditions:**

User has created recurring group lesson with lesson syllabus

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Open lesson detail and edit lesson code with following lessons | User sees syllabus description with no change in all lessons | - |

---

### TC-2852: Edit syllabus detail in lesson with only this lesson

**Preconditions:**

User has created recurring group lesson with lesson syllabus

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Open lesson detail and edit syllabus description with only this | User sees lesson syllabus is updated in selected lesson | - |
| 2 | Check other lessons | User sees syllabus description with no change | - |

---

### TC-2853: Edit syllabus detail in lesson with this and the following

**Preconditions:**

User has created recurring group lesson with lesson syllabus

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Open the 2nd lesson, edit lesson syllabus and another fields (lesson date&time, lesson name,...) with following lessons | User sees lesson syllabus is updated in selected lesson | - |
| 2 | Check other lessons | User sees syllabus description with no change | - |

---

### TC-2854: Change syllabus master in course master after generating in lesson

**Preconditions:**

User has created recurring group lesson with lesson syllabus

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Open course master, change syllabus maste | - | - |
| 2 | Open the previous lesson | User sees syllabus description with no change | - |
| 3 | Create a new group lesson with the course maste | User sees auto-fill the new syllabus description | - |

---

### TC-2855: Change syllabus code in syllabus detail

**Preconditions:**

User has created recurring group lesson with lesson syllabus

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Open syllabus detail, change syllabus code | - | - |
| 2 | Open the previous lesson | User sees syllabus description with no change | - |
| 3 | Create a new group lesson with the course maste | User sees auto-fill the new syllabus description follow the new syllabus code | - |

---

### TC-2856: Change syllabus description in syllabus detail

**Preconditions:**

User has created recurring group lesson with lesson syllabus

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Open syllabus detail, change syllabus description | - | - |
| 2 | Open the previous lesson | User sees syllabus description with no change | - |
| 3 | Create a new group lesson with the course maste | User sees auto-fill the new syllabus description | - |

---

### TC-6414: Verify lesson syllabus on BO

**Preconditions:** -

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Create a group lesson with lesson syllabus<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ Login BO and open the lesson<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ Login BO and open the lesson on Calendar | - | - |
| 2 | Edit syllabus description<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ Login BO and open the lesson<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ Login BO and open the lesson on Calendar | - | - |

---

### TC-6415: Verify lesson syllabus on Mobile

**Preconditions:** -

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Published a group lesson with lesson syllabus and student<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ Login Mobile and open the lesson | - | - |
| 2 | Edit syllabus description<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ Login Mobile and open the lesson | - | - |

---

### TC-6432: Edit lesson with lesson syllabus on BO

**Preconditions:**

User has created a group lesson with lesson syllabus

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Login BO and edit lesson | User still sees the syllabus description | - |

---

### TC-8541: Create a daily/weekly/custom lesson with syllabus detail

**Preconditions:** -

_Steps TBD_

---
