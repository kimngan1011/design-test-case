# Duplicate Lesson

### TC-1207: Duplicate the one-time lesson

**Preconditions:**

* User has created a one-time individual lesson

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Open lesson detail, click on Duplicate button | * Pre-filter all information in the duplicate form | - |
| 2 | Edit to the recurring group lesson by end date | * User sees a group lesson chain is created on the selected weekday within the repeat duration with \"Draft\" status and same lesson info with previous selected lesson<br><br>* User sees the lesson code +1 for following lessons<br><br>* User sees the group lesson report is created with \"Draft\" status for all lessons in the chain | - |
| 3 | Login BO and view the recurring group lesson | * User sees a new lesson and lesson report on BO | - |

---

### TC-1211: Duplicate the lesson course schedule

**Preconditions:**

* Create a course lesson schedule with program master having week order separate
    Refer TC: [ERP-1015](https://app.qase.io/case/ERP-1015)

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Open lesson detail, click on Duplicate button | * Pre-filter all information in the duplicate form | - |
| 2 | Edit to the one-time group lesson | * User sees an one-time group lesson is created with Draft status and same lesson info with previous selected lesson<br><br>* User sees the group lesson report is created with \"Draft\" status | - |
| 3 | Login BO and view the lesson | * User sees a new lesson and lesson report on BO | - |

---

### TC-1208: Duplicate the lesson with closed date

**Preconditions:** -

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Create a recurring group lesson | - | - |
| 2 | Duplicate to the one-time individual lesson with lesson date = closed date | * User sees the one-time lesson is created | - |
| 3 | Create an one-time group lesson | - | - |
| 4 | Duplicate to the recurring lesson so that the lesson in the middle of the chain is closed date | * User sees a recurring group lesson + lesson report are created for all lessons with \"Draft\" status<br>* User does not see a lesson that has lesson date = closed date<br>* User sees lesson code +1 for following lessons<br>* User sees default lesson type = 通常特訓 for all lessons | - |

---

### TC-1212: Duplicate the weekly group lesson with end date

**Preconditions:**

* User has created daily/weekly/custom lesson
* User has opened lesson detail

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Click on Duplicate button | * Pre-filter all information in the duplicate form | - |
| 2 | Edit to the the weekly group lesson with end date | * User sees that the weekly lesson is created successfully. | - |
| 3 | Login BO and view the lesson | * User sees a new lesson and lesson report on BO | - |

---

### TC-7185: Duplicate the weekly individual lesson with lesson count

**Preconditions:**

* User has created daily/weekly/custom lesson
* User has opened lesson detail

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Click on Duplicate button | - | - |
| 2 | Edit to the the weekly individual lesson with lesson count | * User sees that the weekly lesson is created successfully | - |
| 3 | Login BO and view these lessons | * User sees these lessons on BO<br>* User sees the lesson code, lesson type is read-only on BO<br>* User sees the lesson report on Lesson detail -> Report tab and Lesson Report list on BO | - |

---

### TC-7181: Duplicate the daily individual lesson with end date

**Preconditions:**

* User has created daily/weekly/custom lesson
* User has opened lesson detail

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Click on Duplicate button | * Pre-filter all information in the duplicate form | - |
| 2 | Edit to the daily individual lesson with end date | * User sees that the daily lesson is created successfully.<br><br> | - |
| 3 | Login BO and view these lessons | * User sees these lessons on BO<br>* User sees the lesson code, lesson type is read-only on BO<br>* User sees the lesson report on Lesson detail -> Report tab and Lesson Report list on BO | - |

---

### TC-7182: Duplicate the daily group lesson with lesson count

**Preconditions:**

* User has created daily/weekly/custom lesson
* User has opened lesson detail

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Click on Duplicate button | * Pre-filter all information in the duplicate form | - |
| 2 | Edit to the daily group lesson with lesson count | * User sees that the daily lesson is created successfully.<br><br> | - |
| 3 | Login BO and view these lessons | * User sees these lessons on BO<br>* User sees the lesson code, lesson type is read-only on BO<br>* User sees the lesson report on Lesson detail -> Report tab and Lesson Report list on BO | - |

---

### TC-7183: Duplicate custom group lesson with end date

**Preconditions:**

* User has created daily/weekly/custom lesson
* User has opened lesson detail

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Click on Duplicate button | * Pre-filter all information in the duplicate form | - |
| 2 | Edit to the custom group lesson with end date | * User sees that the custom lesson is created successfully.<br><br> | - |
| 3 | Login BO and view these lessons | * User sees these lessons on BO<br>* User sees the lesson code, lesson type is read-only on BO<br>* User sees the lesson report on Lesson detail -> Report tab and Lesson Report list on BO | - |

---

### TC-7184: Duplicate custom individual lesson with lesson count

**Preconditions:**

* User has created daily/weekly/custom lesson
* User has opened lesson detail

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Click on Duplicate button | * Pre-filter all information in the duplicate form | - |
| 2 | Edit to the custom individual lesson with lesson count | * User sees that the custom lesson is created successfully.<br><br> | - |
| 3 | Login BO and view these lessons | * User sees these lessons on BO<br>* User sees the lesson code, lesson type is read-only on BO<br>* User sees the lesson report on Lesson detail -> Report tab and Lesson Report list on BO | - |

---
