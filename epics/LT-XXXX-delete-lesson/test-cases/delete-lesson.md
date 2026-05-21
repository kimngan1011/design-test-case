# Delete Lesson

## Delete lesson

### TC-1209: Delete a daily lesson by end date

**Preconditions:**

* User has created a daily lesson by end date with a teacher and student
* User has updated the student session info

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | * Go to the lesson detail<br><br>* Click on \"Delete\" button<br><br>* Confirm deleting a lesson | * User sees the lesson, lesson report, student session info are deleted<br>* User sees the lesson allocation is updated | - |

---

### TC-9781: Delete a daily lesson by lesson count

**Preconditions:**

* User has created a daily lesson by lesson count with a teacher and student
* User has updated the student session info

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | * Go to the lesson detail<br><br>* Click on \"Delete\" button<br><br>* Confirm deleting a lesson | * User sees the lesson, lesson report, student session info are deleted<br>* User sees the lesson allocation is updated | - |

---

### TC-9782: Delete a weekly lesson by end date

**Preconditions:**

* User has created a weekly lesson by end date with a teacher and student
* User has updated the student session info

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | * Go to the lesson detail<br><br>* Click on \"Delete\" button<br><br>* Confirm deleting a lesson | * User sees the lesson, lesson report, student session info are deleted<br>* User sees the lesson allocation is updated | - |

---

### TC-9783: Delete a weekly lesson by lesson count

**Preconditions:**

* User has created a weekly lesson by lesson count with a teacher and student
* User has updated the student session info

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | * Go to the lesson detail<br><br>* Click on \"Delete\" button<br><br>* Confirm deleting a lesson | * User sees the lesson, lesson report, student session info are deleted<br>* User sees the lesson allocation is updated | - |

---

### TC-9784: Delete a custom lesson by end date

**Preconditions:**

* User has created a custom lesson by end date with a teacher and student
* User has updated the student session info

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | * Go to the lesson detail<br><br>* Click on \"Delete\" button<br><br>* Confirm deleting a lesson | * User sees the lesson, lesson report, student session info are deleted<br>* User sees the lesson allocation is updated | - |

---

### TC-9785: Delete a custom lesson by lesson count

**Preconditions:**

* User has created a custom lesson by lesson count with a teacher and student
* User has updated the student session info

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | * Go to the lesson detail<br><br>* Click on \"Delete\" button<br><br>* Confirm deleting a lesson | * User sees the lesson, lesson report, student session info are deleted<br>* User sees the lesson allocation is updated | - |

---

### TC-10487: Delete lesson with a student

**Preconditions:**

* User has created a daily/weekly/custom/lesson schedule/one time lesson
* User has added a student to all lessons in the chain by following lessons

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Open lesson detail | - | - |
| 2 | Click Delete button | * User sees the lesson, lesson report are deleted | - |
| 3 | Check lesson allocation | * User sees the student sessions linked to the delete lessons are deleted | - |

---

### TC-1210: Bulk delete lesson with student

**Preconditions:**

* User has created some daily/weekly/custom by end date/lesson count with a teacher and student
* User has updated the student session info

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | * Select some lessons including draft, published, completed, cancelled on the lesson list<br>* Click on \"Delete\" button<br><br>* Confirm deleting a lesson | * User sees the lesson, lesson report and student session of all lessons are deleted<br>* User still sees the completed lesson on the lesson list | - |
| 2 | Check lesson allocation | * User sees the student sessions linked to the delete lessons are deleted | - |

---

### TC-1213: Hide the delete lesson button in completed lesson

**Preconditions:** -

_Steps TBD_

---
