# Assign/Unassign a Student by Add Student Popup

## View the Add Student Popup

### TC-1261: View add student popup

**Preconditions:**

* User has created a lesson


* User has created some LAs with Require Allocation flag = True and False for the student

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | * Go to the lesson detail<br>* On Student Sessions, click \"Add Students\" | * User sees the student list is filtered by lesson location<br>* User sees the student list that student location = lesson location<br><br>* User sees the student list that the user has an affiliation<br><br>* User sees the student list that has lesson allocation with the Require Allocation flag = True | - |

---

### TC-1262: Search by student name

**Preconditions:** -

_Steps TBD_

---

### TC-1266: Filter a student

**Preconditions:**

* User has created a lesson
* User has created some LAs with Require Allocation flag = True

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Filter by location | * User sees the student list is filtered by selected location | - |
| 2 | Filter by Course | * User sees the student list is filtered by selected course | - |
| 3 | Filter by Grade | * User sees the student list is filtered by selected grade | - |
| 4 | Filter by Type | * User sees the student list is filtered by selected type | - |
| 5 | Filter by School | * User sees the student list is filtered by selected school | - |
| 6 | Combine multiple criteria | * User sees the student list is filtered by selected criteria | - |

---

### TC-11638: Hide "Closed Down" location on add student session dialog and 'closed down' location data will be not shown

**Preconditions:** -

_Steps TBD_

---

### TC-13081: View the Academic Year filter

**Description:** ![image.png](https://d2cxucsjd6xvsd.cloudfront.net/public/team/b5f684e60ab1a64567fb280d07faed2c4132e041/attachment/b58ec9c2fe554104dcb576d0c4a9312addaa18a7/image.png)

**Preconditions:** -

_Steps TBD_

---

### TC-13082: Filter Academic Year

**Preconditions:** -

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Filter by default | - | - |
| 2 | Filter combine multiple AY | - | - |
| 3 | Filter combine multiple criteria | - | - |
| 4 | Remove filte | - | - |
| 5 | Reset filte | - | - |

---

## Assign/Unassign a student

### TC-9306: View student in lesson detail

**Preconditions:** -

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | View nickname of the student | Format `Student name (Phonetic name)/(Nickname)` | - |
| 2 | And if student have no nickname | Format: Student name without empty () or \"Null\" words | - |
| 3 | And if student have no `Phonetic name` | Format: Student name without empty () or \"Null\" words | - |

---

### TC-1448: Sort the student list

**Description:** [https://manabie.atlassian.net/browse/LT-63216](https://manabie.atlassian.net/browse/LT-63216)

**Preconditions:** -

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | * 山下 晃弘(ヤマシタ アキヒロ) <br><br>* 板澤 山口 <br>* 中野 遼介(ナカノ リョウスケ) <br>* 体験会 デモ用 <br>* 生徒テスト 英(セイトテスト エイ) <br>* De <br>* Alpha <br>* Em <br>* Imort <br>* cons <br>* \\<link> <br>* Vie <br>* 2024student <br>* student0724 | 生徒テスト 英(セイトテスト エイ)<br>中野 遼介(ナカノ リョウスケ)<br>山下 晃弘(ヤマシタ アキヒロ)<br>体験会 デモ用<br>板澤 山口<br>Alpha<br>cons<br>De<br>Em<br>Imort<br>Vie<br>student0724<br>2024student<br>\\<link | - |
| 2 | New example: [https://dev-staging.lightning.force.com/lightning/r/MANAERP__Lesson__c/a1mIU000005ZRrrYAG/view](https://dev-staging.lightning.force.com/lightning/r/MANAERP__Lesson__c/a1mIU000005ZRrrYAG/view) | ![image.png](https://d2cxucsjd6xvsd.cloudfront.net/public/team/b5f684e60ab1a64567fb280d07faed2c4132e041/attachment/5eca7dcba74532d31d097aa6b6e38bcb312c758a/image.png) | - |

---

### TC-1263: Assign a student to an one-time lesson

**Preconditions:**

* User has created an one-time individual/group lesson
* User has published the lesson and lesson report
* User has created some LAs with Require Allocation flag = True

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | * Go to the lesson detail<br>* On Student Session, click \"Add Student\"<br>* Add a student to Lesson | * User sees the student is added to Lesson and redirect to Student’s Lesson Allocation detail page when click<br>* User sees the lesson report detail is created for the student | - |
| 2 | Check lesson report of added student | * User sees the lesson report detail is auto-created for the student | - |
| 3 | Check lesson allocation | * User sees the student session is auto-created = assigned lessons (no empty student session)<br>* User sees the lesson allocation of the student is updated (Lesson Allocated, Lesson Allocation Status, Report History) | - |
| 4 | Login BO and view a student in lesson | * User sees the student in detailed lesson page on BO<br>* User sees the lesson report detail is created for the student on BO | - |
| 5 | Login Mobile and view the student's lesson | * Student/Parent sees the lesson and lesson report with correct information | - |

---

### TC-1270: Unassign a student from an one-time lesson

**Preconditions:**

* Refer to test case [ERP-1263](https://app.qase.io/case/ERP-1263)

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | * Go to the lesson detail<br>* Remove the student from the lesson | * User does not see the student in detailed lesson page | - |
| 2 | Check lesson report of removed student | * User does not see the lesson report detail of the removed student | - |
| 3 | Check lesson allocation | * User sees the student sessions linked to the lessons which the removed student is deleted<br>* User sees the lesson allocation of the student is updated (Lesson Allocated, Lesson Allocation Status, Report History) | - |
| 4 | Login BO and view a student in lesson | * User does not see the student in detailed lesson page on BO | - |
| 5 | Student login Mobile | * Student does not see the lesson | - |

---

### TC-1265: Assign a student to lesson course schedule

**Preconditions:**

* Create a course lesson schedule with program master having week order separate
    Refer TC: [ERP-1015](https://app.qase.io/case/ERP-1015)
* User has published lesson and lesson report
* User has created some LAs with Require Allocation flag = True

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | * Open the 2nd lesson<br>* On Student Session, click \"Add Student\"<br>* Add a Student A to Lesson with \"Only this Lesson\" option | * User sees the student is added to selected lesson<br>* User does not see the student is added to other lessons in the chain | - |
| 2 | * Open the 1st lesson<br>* On Student Session, click \"Add Student\"<br>* Add a Student B to Lesson with \"This and the following lessons\" option | * User sees the student is added to this and the following lesson<br>* User sees the 2 students in the 2nd lesson | - |
| 3 | Check lesson report of added student | * User sees the lesson report detail is auto-created for the student | - |
| 4 | Check lesson allocation | * User sees the student session is auto-created = assigned lessons (no empty student session)<br>* User sees the lesson allocation of the student is updated (Lesson Allocated, Lesson Allocation Status, Report History) | - |
| 5 | Login BO and view a student in lesson | * User sees the student is added to Lesson | - |
| 6 | Student A login Mobile | * Student/Parent A sees the lesson and lesson report with correct information | - |
| 7 | Student B login Mobile | * Student/Parent B sees the lesson and lesson report with correct information | - |

---

### TC-1264: Assign a student to a recurring lesson that are out of student course duration.

**Preconditions:**

* User has created a recurring individual/group lesson
* User has created some LAs with Require Allocation flag = True

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | * Open the 2nd lesson<br>* On Student Session, click \"Add Student\"<br>* Add a student to Lesson that are out of student course duration with \"Only this Lesson\" option | * User sees the student is added to the selected lesson<br>* User sees the warning message and indicator on the selected lesson<br>* User can remove an indicato | - |
| 2 | * Open the 1st lesson<br>* On Student Session, click \"Add Student\"<br>* Add a student to Lesson that are out of student course duration with \"This and the following\" | * User sees the student is added to this and the following lesson<br>* User sees the warning message and indicator on the lessons that are out of student course duration | - |
| 3 | Check lesson report of added student | * User sees the lesson report detail is auto-created for the student | - |
| 4 | Check lesson allocation | * User sees the student session is auto-created = assigned lessons (no empty student session)<br>* User sees the lesson allocation of the student is updated (Lesson Allocated, Lesson Allocation Status, Report History) | - |
| 5 | Login BO and view a student in lesson | * User sees the warning message and indicator on the selected lesson on BO<br>* User can remove an indicato | - |

---

### TC-8509: Assign a student to a daily lesson with end date

**Preconditions:**

* User has created a daily lesson by end date
* User has published all lessons in the chain

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | * Open the 2nd lesson<br>* On Student Session, click \"Add Student\"<br>* Add a student to Lesson with \"Only this Lesson\" option | * User sees the student is added to selected lesson<br>* User does not see the student is added to other lessons in the chain | - |
| 2 | * Open the 1st lesson<br>* On Student Session, click \"Add Student\"<br>* Add a student to Lesson with \"This and the following lessons\" option | * User sees the student is added to this and the following lesson<br>* User sees the 2 students in the 2nd lesson | - |
| 3 | Check lesson report of added student | * User sees the lesson report detail is auto-created for the student | - |
| 4 | Check lesson allocation | * User sees the student session is auto-created = assigned lessons (no empty student session)<br>* User sees the lesson allocation of the student is updated (Lesson Allocated, Lesson Allocation Status, Report History) | - |
| 5 | Login BO and view a student in lesson | * User sees the student is added to Lesson | - |
| 6 | Student A login Mobile | * Student A sees the lesson and lesson report with correct information | - |
| 7 | Parent B login Mobile | * Parent B sees the lesson and lesson report with correct information | - |

---

### TC-8511: Unassign a student from a daily lesson with end date

**Preconditions:**

* User has assigned a student to a daily lesson with end date

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | * Open the 2nd lesson<br>* On Student Session, click \"Remove Student\" button<br>* Remove a student to Lesson with \"Only this Lesson\" option | * User does not see the student in detailed lesson page<br>* User still sees the student in other lessons in the chain | - |
| 2 | * Open the 1st lesson<br>* On Student Session, click \"Remove Student\" button<br>* Remove a student to Lesson with \"This and the following lessons\" option | * User does not see the student in this and the following lesson | - |
| 3 | Check lesson report of removed student | * User does not see the lesson report detail of the removed student | - |
| 4 | Check lesson allocation | * User sees the student sessions linked to the lessons which the removed student is deleted<br>* User sees the lesson allocation of the student is updated (Lesson Allocated, Lesson Allocation Status, Report History) | - |
| 5 | Login BO and view a student in lesson | * User does not see the student in detailed lesson page on BO | - |
| 6 | Student A login Mobile | * Student A does not see the lesson | - |
| 7 | Parent B login Mobile | * Parent B does not see the lesson | - |

---

### TC-8510: Assign a student to a daily lesson with lesson count

**Preconditions:**

* User has created a daily lesson by lesson count
* User has published all lessons in the chain

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | * Open the 2nd lesson<br>* On Student Session, click \"Add Student\"<br>* Add a student to Lesson with \"Only this Lesson\" option | * User sees the student is added to selected lesson<br>* User does not see the student is added to other lessons in the chain | - |
| 2 | * Open the 1st lesson<br>* On Student Session, click \"Add Student\"<br>* Add a student to Lesson with \"This and the following lessons\" option | * User sees the student is added to this and the following lesson<br>* User sees the 2 students in the 2nd lesson | - |
| 3 | Check lesson report of added student | * User sees the lesson report detail is auto-created for the student | - |
| 4 | Check lesson allocation | * User sees the student session is auto-created = assigned lessons (no empty student session)<br>* User sees the lesson allocation of the student is updated (Lesson Allocated, Lesson Allocation Status, Report History) | - |
| 5 | Login BO and view a student in lesson | * User sees the student is added to Lesson | - |
| 6 | Student A login Mobile | * Student A sees the lesson and lesson report with correct information | - |
| 7 | Parent B login Mobile | * Parent B sees the lesson and lesson report with correct information | - |

---

### TC-8512: Unassign a student from a daily lesson with lesson count

**Preconditions:**

* User has assigned a student to a daily lesson with lesson count

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | * Open the 2nd lesson<br>* On Student Session, click \"Remove Student\" button<br>* Remove a student to Lesson with \"Only this Lesson\" option | * User does not see the student in detailed lesson page<br>* User still sees the student in other lessons in the chain | - |
| 2 | * Open the 1st lesson<br>* On Student Session, click \"Remove Student\" button<br>* Remove a student to Lesson with \"This and the following lessons\" option | * User does not see the student in this and the following lesson | - |
| 3 | Check lesson report of removed student | * User does not see the lesson report detail of the removed student | - |
| 4 | Check lesson allocation | * User sees the student sessions linked to the lessons which the removed student is deleted<br>* User sees the lesson allocation of the student is updated (Lesson Allocated, Lesson Allocation Status, Report History) | - |
| 5 | Login BO and view a student in lesson | * User does not see the student in detailed lesson page on BO | - |
| 6 | Student A login Mobile | * Student A does not see the lesson | - |
| 7 | Parent B login Mobile | * Parent B does not see the lesson | - |

---

### TC-8513: Assign a student to a weekly lesson with end date

**Preconditions:**

* User has created a weekly lesson by end date
* User has published all lessons in the chain

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | * Open the 2nd lesson<br>* On Student Session, click \"Add Student\"<br>* Add a student to Lesson with \"Only this Lesson\" option | * User sees the student is added to selected lesson<br>* User does not see the student is added to other lessons in the chain | - |
| 2 | * Open the 1st lesson<br>* On Student Session, click \"Add Student\"<br>* Add a student to Lesson with \"This and the following lessons\" option | * User sees the student is added to this and the following lesson<br>* User sees the 2 students in the 2nd lesson | - |
| 3 | Check lesson report of added student | * User sees the lesson report detail is auto-created for the student | - |
| 4 | Check lesson allocation | * User sees the student session is auto-created = assigned lessons (no empty student session)<br>* User sees the lesson allocation of the student is updated (Lesson Allocated, Lesson Allocation Status, Report History) | - |
| 5 | Login BO and view a student in lesson | * User sees the student is added to Lesson | - |
| 6 | Student A login Mobile | * Student A sees the lesson and lesson report with correct information | - |
| 7 | Parent B login Mobile | * Parent B sees the lesson and lesson report with correct information | - |

---

### TC-8515: Unassign a student from a weekly lesson with end date

**Preconditions:**

* User has assigned a student to a weekly lesson with end date

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | * Open the 2nd lesson<br>* On Student Session, click \"Remove Student\" button<br>* Remove a student to Lesson with \"Only this Lesson\" option | * User does not see the student in detailed lesson page<br>* User still sees the student in other lessons in the chain | - |
| 2 | * Open the 1st lesson<br>* On Student Session, click \"Remove Student\" button<br>* Remove a student to Lesson with \"This and the following lessons\" option | * User does not see the student in this and the following lesson | - |
| 3 | Check lesson report of removed student | * User does not see the lesson report detail of the removed student | - |
| 4 | Check lesson allocation | * User sees the student sessions linked to the lessons which the removed student is deleted<br>* User sees the lesson allocation of the student is updated (Lesson Allocated, Lesson Allocation Status, Report History) | - |
| 5 | Login BO and view a student in lesson | * User does not see the student in detailed lesson page on BO | - |
| 6 | Student A login Mobile | * Student A does not see the lesson | - |
| 7 | Parent B login Mobile | * Parent B does not see the lesson | - |

---

### TC-8514: Assign a student to a weekly lesson with lesson count

**Preconditions:**

* User has created a weekly lesson by lesson count
* User has published all lessons in the chain

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | * Open the 2nd lesson<br>* On Student Session, click \"Add Student\"<br>* Add a student to Lesson with \"Only this Lesson\" option | * User sees the student is added to selected lesson<br>* User does not see the student is added to other lessons in the chain | - |
| 2 | * Open the 1st lesson<br>* On Student Session, click \"Add Student\"<br>* Add a student to Lesson with \"This and the following lessons\" option | * User sees the student is added to this and the following lesson<br>* User sees the 2 students in the 2nd lesson | - |
| 3 | Check lesson report of added student | * User sees the lesson report detail is auto-created for the student | - |
| 4 | Check lesson allocation | * User sees the student session is auto-created = assigned lessons (no empty student session)<br>* User sees the lesson allocation of the student is updated (Lesson Allocated, Lesson Allocation Status, Report History) | - |
| 5 | Login BO and view a student in lesson | * User sees the student is added to Lesson | - |
| 6 | Student A login Mobile | * Student A sees the lesson and lesson report with correct information | - |
| 7 | Parent B login Mobile | * Parent B sees the lesson and lesson report with correct information | - |

---

### TC-8516: Unassign a student from a weekly lesson with lesson count

**Preconditions:**

* User has assigned a weekly lesson with lesson count

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | * Open the 2nd lesson<br>* On Student Session, click \"Remove Student\" button<br>* Remove a student to Lesson with \"Only this Lesson\" option | * User does not see the student in detailed lesson page<br>* User still sees the student in other lessons in the chain | - |
| 2 | * Open the 1st lesson<br>* On Student Session, click \"Remove Student\" button<br>* Remove a student to Lesson with \"This and the following lessons\" option | * User does not see the student in this and the following lesson | - |
| 3 | Check lesson report of removed student | * User does not see the lesson report detail of the removed student | - |
| 4 | Check lesson allocation | * User sees the student sessions linked to the lessons which the removed student is deleted<br>* User sees the lesson allocation of the student is updated (Lesson Allocated, Lesson Allocation Status, Report History) | - |
| 5 | Login BO and view a student in lesson | * User does not see the student in detailed lesson page on BO | - |
| 6 | Student A login Mobile | * Student A does not see the lesson | - |
| 7 | Parent B login Mobile | * Parent B does not see the lesson | - |

---

### TC-8517: Assign a student to a custom lesson with end date

**Preconditions:**

* User has created a custom lesson by end date
* User has published all lessons in the chain

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | * Open the 2nd lesson<br>* On Student Session, click \"Add Student\"<br>* Add a student to Lesson with \"Only this Lesson\" option | * User sees the student is added to selected lesson<br>* User does not see the student is added to other lessons in the chain | - |
| 2 | * Open the 1st lesson<br>* On Student Session, click \"Add Student\"<br>* Add a student to Lesson with \"This and the following lessons\" option | * User sees the student is added to this and the following lesson<br>* User sees the 2 students in the 2nd lesson | - |
| 3 | Check lesson report of added student | * User sees the lesson report detail is auto-created for the student | - |
| 4 | Check lesson allocation | * User sees the student session is auto-created = assigned lessons (no empty student session)<br>* User sees the lesson allocation of the student is updated (Lesson Allocated, Lesson Allocation Status, Report History) | - |
| 5 | Login BO and view a student in lesson | * User sees the student is added to Lesson | - |
| 6 | Student A login Mobile | * Student A sees the lesson and lesson report with correct information | - |
| 7 | Parent B login Mobile | * Parent B sees the lesson and lesson report with correct information | - |

---

### TC-8519: Unassign a student from a custom lesson with end date

**Preconditions:**

* User has assigned a student to a custom lesson with end date

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | * Open the 2nd lesson<br>* On Student Session, click \"Remove Student\" button<br>* Remove a student to Lesson with \"Only this Lesson\" option | * User does not see the student in detailed lesson page<br>* User still sees the student in other lessons in the chain | - |
| 2 | * Open the 1st lesson<br>* On Student Session, click \"Remove Student\" button<br>* Remove a student to Lesson with \"This and the following lessons\" option | * User does not see the student in this and the following lesson | - |
| 3 | Check lesson report of removed student | * User does not see the lesson report detail of the removed student | - |
| 4 | Check lesson allocation | * User sees the student sessions linked to the lessons which the removed student is deleted<br>* User sees the lesson allocation of the student is updated (Lesson Allocated, Lesson Allocation Status, Report History) | - |
| 5 | Login BO and view a student in lesson | * User does not see the student in detailed lesson page on BO | - |
| 6 | Student A login Mobile | * Student A does not see the lesson | - |
| 7 | Parent B login Mobile | * Parent B does not see the lesson | - |

---

### TC-8518: Assign a student to a custom lesson with lesson count

**Preconditions:**

* User has created a custom lesson by lesson count
* User has published all lessons in the chain

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | * Open the 2nd lesson<br>* On Student Session, click \"Add Student\"<br>* Add a student to Lesson with \"Only this Lesson\" option | * User sees the student is added to selected lesson<br>* User does not see the student is added to other lessons in the chain | - |
| 2 | * Open the 1st lesson<br>* On Student Session, click \"Add Student\"<br>* Add a student to Lesson with \"This and the following lessons\" option | * User sees the student is added to this and the following lesson<br>* User sees the 2 students in the 2nd lesson | - |
| 3 | Check lesson report of added student | * User sees the lesson report detail is auto-created for the student | - |
| 4 | Check lesson allocation | * User sees the student session is auto-created = assigned lessons (no empty student session)<br>* User sees the lesson allocation of the student is updated (Lesson Allocated, Lesson Allocation Status, Report History) | - |
| 5 | Login BO and view a student in lesson | * User sees the student is added to Lesson | - |
| 6 | Student A login Mobile | * Student A sees the lesson and lesson report with correct information | - |
| 7 | Parent B login Mobile | * Parent B sees the lesson and lesson report with correct information | - |

---

### TC-8520: Unassign a student from a custom lesson with lesson count

**Preconditions:**

* User has assigned a student to a custom lesson with lesson count

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | * Open the 2nd lesson<br>* On Student Session, click \"Remove Student\" button<br>* Remove a student to Lesson with \"Only this Lesson\" option | * User does not see the student in detailed lesson page<br>* User still sees the student in other lessons in the chain | - |
| 2 | * Open the 1st lesson<br>* On Student Session, click \"Remove Student\" button<br>* Remove a student to Lesson with \"This and the following lessons\" option | * User does not see the student in this and the following lesson | - |
| 3 | Check lesson report of removed student | * User does not see the lesson report detail of the removed student | - |
| 4 | Check lesson allocation | * User sees the student sessions linked to the lessons which the removed student is deleted<br>* User sees the lesson allocation of the student is updated (Lesson Allocated, Lesson Allocation Status, Report History) | - |
| 5 | Login BO and view a student in lesson | * User does not see the student in detailed lesson page on BO | - |
| 6 | Student A login Mobile | * Student A does not see the lesson | - |
| 7 | Parent B login Mobile | * Parent B does not see the lesson | - |

---

### TC-11538: Assign a student to a lesson with over assigned

**Preconditions:**

* User has created multiple recurring lessons
* User has created a LA

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Select a LA | - | - |
| 2 | Select a recurring lesson with following lessons so that **Assigned Sessions + new assignments > Total Session Count** | * User sees a warning modal | - |
| 3 | Confirm to assign | * User sees a student in all lessons in the chain <br>* User sees lesson allocation status as Over Assigned | - |

---

### TC-1267: Cannot assign/unassign a student

**Preconditions:**

* User create a recurring lesson
* User has completed lesson in the chain

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Open the completed lesson | Disable the Add Student and Remove Student button | - |
| 2 | * Open the lesson before the completed lesson<br>* Add a student with this and the following | User does not sees a student is added to completed lesson | - |
| 3 | * Open the lesson before the completed lesson<br>* Delete a student with this and the following | Retain a student in completed lesson | - |

---
