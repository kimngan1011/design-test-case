# Assign/Unassign Teacher

## Assign/Unassign a teacher in lesson detail

### TC-1214: View add teacher popup

**Preconditions:**

* User has created an one-time individual/group lesson


* User has created an eligible subject with the staff and the subject

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | * Go to the lesson detail<br><br>* On Lesson Teacher, click \"Add Teachers\" | * User sees the teacher list that have affiliation = user's affiliation login<br>* User sees the teacher list is pre-filtered by<br>    1\\. Location = Lesson location \\(multi\\-select\\) | - |

---

### TC-1215: Search by teacher name

**Preconditions:** -

_Steps TBD_

---

### TC-1219: Filter a teacher

**Preconditions:**

* User has created an one-time individual/group lesson


* User has created an eligible subject with the staff and the subject
* User has created a working hour for a staff

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Filter by location | * User sees the teacher list is filtered by selected location | - |
| 2 | Filter by working type | * User sees the teacher list is filtered by selected working type | * Full-time<br>* Part-time |
| 3 | Filter by subject | * User sees the teacher list is filtered by selected subject | - |
| 4 | Filter by teacher working hours | * User sees the teacher list is filtered who has working hour within lesson date&time | - |
| 5 | Combine multiple criteria | * User sess the teacher list is filtered by selected criteria | - |

---

### TC-4943: Select all teachers

**Preconditions:** -

_Steps TBD_

---

### TC-1216: Assign a teacher to an one-time lesson

**Preconditions:**

* User has created an one-time individual/group lesson


* User has created an eligible subject with the staff and the subject

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | * Go to the lesson detail<br>* On Lesson Teacher, click \"Add Teachers\"<br><br>* Add a teacher to Lesson | * User sees the teacher is added to Lesson | - |
| 2 | Login BO and view a teacher in lesson | * User sees the teacher is added to Lesson | - |

---

### TC-1240: Unassign a teacher from an one-time lesson

**Preconditions:**

* User has added the teacher to the one-time lesson

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | * Go to the lesson detail<br>* Remove the teacher from the lesson | * User does not see the teacher in detailed lesson page | - |
| 2 | Login BO and view a teacher in lesson | * User does not see the teacher in detailed lesson page on BO | - |

---

### TC-1218: Assign a teacher to lesson course schedule

**Preconditions:**

* Create a course lesson schedule with program master having week order separate
    Refer TC: [ERP-1015](https://app.qase.io/case/ERP-1015)
* User has created an eligible subject with the staff and the subject

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | * Open the 2nd lesson<br>* On Lesson Teacher, click \"Add Teachers\"<br>* Add a teacher to Lesson with \"Only this Lesson\" option | * User sees the teacher is added to selected lesson<br>* User does not see the teacher is added to other lessons in the chain | - |
| 2 | * Open the 1st lesson<br>* On Lesson Teacher, click \"Add Teachers\"<br>* Add a teacher to Lesson with \"This and the following lessons\" option | * User sees the teacher is added to this and the following lesson<br>* User sees the 2 teachers in the 2nd lesson | - |
| 3 | Login BO and view a teacher in lesson | * User sees the teacher is added to Lesson | - |

---

### TC-1238: Add the teacher on lesson schedule

**Preconditions:**

* User has created some daily/weekly/custom by end date/lesson count
* User has created an eligible subject with the staff and the subject
* User has completed and cancelled some lessons

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | * Go to the lesson schedule detail<br>* Click on \"Add Teacher\" button<br><br>* Select teacher and click on \"Add\" button | * User sees the teacher is added to all lessons in the lesson schedule<br>* User does not see the teacher is added in completed lesson and cancelled lesson | - |
| 2 | Login BO and view a teacher in lesson | * User sees the teacher is added to Lesson | - |

---

### TC-8493: Assign a teacher to daily lesson with end date

**Preconditions:**

* User has created a daily lesson by end date with skip closed date

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | * Open the 2nd lesson<br>* On Lesson Teacher, click \"Add Teachers\"<br>* Add a teacher to Lesson with \"Only this Lesson\" option | * User sees the teacher is added to selected lesson<br>* User does not see the teacher is added to other lessons in the chain | - |
| 2 | * Open the 1st lesson<br>* On Lesson Teacher, click \"Add Teachers\"<br>* Add a teacher to Lesson with \"This and the following lessons\" option | * User sees the teacher is added to this and the following lesson<br>* User sees the 2 teachers in the 2nd lesson | - |
| 3 | Login BO and view a teacher in lesson | * User sees the teacher is added to Lesson | - |

---

### TC-8495: Unassign a teacher from daily lesson with end date

**Preconditions:**

* User has assigned a teacher to a daily lesson with end date

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | * Open the 2nd lesson<br>* On Lesson Teacher, click \"Delete\"<br>* Delete a teacher from Lesson with \"Only this Lesson\" option | * User does not see the teacher in selected lesson<br>* User still sees the teacher in other lessons in the chain | - |
| 2 | Open a middle lesson in the chain | - | - |
| 3 | * On Lesson Teacher, click \"Delete\"<br>* Delete a teacher from Lesson with \"This and the following lessons\" option | * User does not see the teacher in this and the following lessons | - |
| 4 | Check the previous lessons | * User sees the previous lessons has no changes | - |

---

### TC-8494: Assign a teacher to daily lesson with lesson count

**Preconditions:**

* User has created a daily lesson by lesson count without skip closed date

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | * Open the 2nd lesson<br>* On Lesson Teacher, click \"Add Teachers\"<br>* Add a teacher to Lesson with \"Only this Lesson\" option | * User sees the teacher is added to selected lesson<br>* User does not see the teacher is added to other lessons in the chain | - |
| 2 | * Open the 1st lesson<br>* On Lesson Teacher, click \"Add Teachers\"<br>* Add a teacher to Lesson with \"This and the following lessons\" option | * User sees the teacher is added to this and the following lesson<br>* User sees the 2 teachers in the 2nd lesson | - |
| 3 | Login BO and view a teacher in lesson | * User sees the teacher is added to Lesson | - |

---

### TC-8496: Unassign a teacher from daily lesson with lesson count

**Preconditions:**

* User has assigned a teacher to a daily lesson with lesson count

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | * Open the 2nd lesson<br>* On Lesson Teacher, click \"Delete\"<br>* Delete a teacher from Lesson with \"Only this Lesson\" option | * User does not see the teacher in selected lesson<br>* User still sees the teacher in other lessons in the chain | - |
| 2 | Open a middle lesson in the chain | - | - |
| 3 | * On Lesson Teacher, click \"Delete\"<br>* Delete a teacher from Lesson with \"This and the following lessons\" option | * User does not see the teacher in this and the following lessons | - |
| 4 | Check the previous lessons | * User sees the previous lessons has no changes | - |

---

### TC-8497: Assign a teacher to weekly lesson with end date

**Preconditions:**

* User has created a weekly lesson by end date with skip closed date

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | * Open the 2nd lesson<br>* On Lesson Teacher, click \"Add Teachers\"<br>* Add a teacher to Lesson with \"Only this Lesson\" option | * User sees the teacher is added to selected lesson<br>* User does not see the teacher is added to other lessons in the chain | - |
| 2 | * Open the 1st lesson<br>* On Lesson Teacher, click \"Add Teachers\"<br>* Add a teacher to Lesson with \"This and the following lessons\" option | * User sees the teacher is added to this and the following lesson<br>* User sees the 2 teachers in the 2nd lesson | - |
| 3 | Login BO and view a teacher in lesson | * User sees the teacher is added to Lesson | - |

---

### TC-8499: Unassign a teacher from weekly lesson with end date

**Preconditions:**

* User has assigned a teacher to a weekly lesson with end date

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | * Open the 2nd lesson<br>* On Lesson Teacher, click \"Delete\"<br>* Delete a teacher from Lesson with \"Only this Lesson\" option | * User does not see the teacher in selected lesson<br>* User still sees the teacher in other lessons in the chain | - |
| 2 | Open a middle lesson in the chain | - | - |
| 3 | * On Lesson Teacher, click \"Delete\"<br>* Delete a teacher from Lesson with \"This and the following lessons\" option | * User does not see the teacher in this and the following lessons | - |
| 4 | Check the previous lessons | * User sees the previous lessons has no changes | - |

---

### TC-8498: Assign a teacher to weekly lesson with lesson count

**Preconditions:**

* User has created a weekly lesson by lesson count without skip closed date

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | * Open the 2nd lesson<br>* On Lesson Teacher, click \"Add Teachers\"<br>* Add a teacher to Lesson with \"Only this Lesson\" option | * User sees the teacher is added to selected lesson<br>* User does not see the teacher is added to other lessons in the chain | - |
| 2 | * Open the 1st lesson<br>* On Lesson Teacher, click \"Add Teachers\"<br>* Add a teacher to Lesson with \"This and the following lessons\" option | * User sees the teacher is added to this and the following lesson<br>* User sees the 2 teachers in the 2nd lesson | - |
| 3 | Login BO and view a teacher in lesson | * User sees the teacher is added to Lesson | - |

---

### TC-8500: Unassign a teacher from weekly lesson with lesson count

**Preconditions:**

* User has assigned a teacher to a weekly lesson with lesson count

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | * Open the 2nd lesson<br>* On Lesson Teacher, click \"Delete\"<br>* Delete a teacher from Lesson with \"Only this Lesson\" option | * User does not see the teacher in selected lesson<br>* User still sees the teacher in other lessons in the chain | - |
| 2 | Open a middle lesson in the chain | - | - |
| 3 | * On Lesson Teacher, click \"Delete\"<br>* Delete a teacher from Lesson with \"This and the following lessons\" option | * User does not see the teacher in this and the following lessons | - |
| 4 | Check the previous lessons | * User sees the previous lessons has no changes | - |

---

### TC-8501: Assign a teacher to custom lesson with end date

**Preconditions:**

* User has created a custom lesson by end date with skip closed date

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | * Open the 2nd lesson<br>* On Lesson Teacher, click \"Add Teachers\"<br>* Add a teacher to Lesson with \"Only this Lesson\" option | * User sees the teacher is added to selected lesson<br>* User does not see the teacher is added to other lessons in the chain | - |
| 2 | * Open the 1st lesson<br>* On Lesson Teacher, click \"Add Teachers\"<br>* Add a teacher to Lesson with \"This and the following lessons\" option | * User sees the teacher is added to this and the following lesson<br>* User sees the 2 teachers in the 2nd lesson | - |
| 3 | Login BO and view a teacher in lesson | * User sees the teacher is added to Lesson | - |

---

### TC-8503: Unassign a teacher from custom lesson with end date

**Preconditions:**

* User has assigned a teacher to a custom lesson with end date

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | * Open the 2nd lesson<br>* On Lesson Teacher, click \"Delete\"<br>* Delete a teacher from Lesson with \"Only this Lesson\" option | * User does not see the teacher in selected lesson<br>* User still sees the teacher in other lessons in the chain | - |
| 2 | Open a middle lesson in the chain | - | - |
| 3 | * On Lesson Teacher, click \"Delete\"<br>* Delete a teacher from Lesson with \"This and the following lessons\" option | * User does not see the teacher in this and the following lessons | - |
| 4 | Check the previous lessons | * User sees the previous lessons has no changes | - |

---

### TC-8502: Assign a teacher to custom lesson with lesson count

**Preconditions:**

* User has created a custom lesson by lesson count without skip closed date

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | * Open the 2nd lesson<br>* On Lesson Teacher, click \"Add Teachers\"<br>* Add a teacher to Lesson with \"Only this Lesson\" option | * User sees the teacher is added to selected lesson<br>* User does not see the teacher is added to other lessons in the chain | - |
| 2 | * Open the 1st lesson<br>* On Lesson Teacher, click \"Add Teachers\"<br>* Add a teacher to Lesson with \"This and the following lessons\" option | * User sees the teacher is added to this and the following lesson<br>* User sees the 2 teachers in the 2nd lesson | - |
| 3 | Login BO and view a teacher in lesson | * User sees the teacher is added to Lesson | - |

---

### TC-8504: Unassign a teacher from custom lesson with lesson count

**Preconditions:**

* User has assigned a teacher to a custom lesson with lesson count

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | * Open the 2nd lesson<br>* On Lesson Teacher, click \"Delete\"<br>* Delete a teacher from Lesson with \"Only this Lesson\" option | * User does not see the teacher in selected lesson<br>* User still sees the teacher in other lessons in the chain | - |
| 2 | Open a middle lesson in the chain | - | - |
| 3 | * On Lesson Teacher, click \"Delete\"<br>* Delete a teacher from Lesson with \"This and the following lessons\" option | * User does not see the teacher in this and the following lessons | - |
| 4 | Check the previous lessons | * User sees the previous lessons has no changes | - |

---

### TC-9792: Skip duplicate teacher in lesson

**Preconditions:**

* User has created an recurring lesson

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | * Open the 2nd lesson<br>* On Lesson Teacher, click \"Add Teachers\"<br>* Add a teacher to Lesson with \"Only this Lesson\" option | * User sees the teacher is added to selected lesson<br>* User does not see the teacher is added to other lessons in the chain | - |
| 2 | * Open the 1st lesson<br>* On Lesson Teacher, click \"Add Teachers\"<br>* continue add this teacher to Lesson with \"This and the following lessons\" option | * User only sees the 1 teachers in the 2nd lesson | - |

---

### TC-1227: Cannot assign/unassign a teacher

**Preconditions:**

* User create a recurring lesson
* User has completed lesson in the chain

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Open the completed lesson | Disable the Add Teacher and Delete button | - |

---

### TC-11639: Hide "Closed Down" location on add lesson teacher dialog and the data of the 'closed down' location will not be shown

**Preconditions:** -

_Steps TBD_

---

### TC-13222: Assign a teacher on Lesson Teacher list with same lesson location

**Preconditions:** -

_Steps TBD_

---
