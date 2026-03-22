# [Nichibei] Assign a Student with Specific Lesson Number

## UI & Input Validation

### TC-14942: HQ/CM Verify the Apply to Next X Lessons option

**Preconditions:** -

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | HQ/CM Verify the Apply to Next X Lessons option | Show on assign student popup:<br><br>* Lesson detail SF<br>* Calendar SF<br>* Lesson detail BO | - |

---

### TC-14943: HQ/CM Input accepts positive integer only

**Preconditions:** -

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | HQ/CM Input accepts positive integer only | Accepted and processed | - |

---

### TC-14944: HQ/CM Input value = 0

**Preconditions:** -

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | HQ/CM Input value = 0 | Show an error message? | - |

---

### TC-14945: HQ/CM Input negative value

**Preconditions:** -

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | HQ/CM Input negative value | Cannot input | - |

---

### TC-14946: HQ/CM Input non-numeric value

**Preconditions:** -

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | HQ/CM Input non-numeric value | Cannot input | - |

---

### TC-14947: HQ/CM Input very large number

**Preconditions:** -

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | HQ/CM Input very large number (500) | Accepted and processed | - |

---

### TC-14949: HQ/CM Cancel assignment

**Preconditions:** -

_Steps TBD_

---

### TC-14950: Verify the confirmation alert when assign student to exactly X next lessons with remaining < X

**Preconditions:** -

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | HQ/CM Assign student to exactly X next lessons when remaining < X | “There are fewer remaining lessons than the number you selected. Do you want to assign the student to all remaining lessons instead?” | - |

---

### TC-14951: Verify the confirmation alert when assign student to exactly X next lessons with over assigned

**Preconditions:** -

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | HQ/CM Assign student to exactly X next lessons with over assigned | Show an alert of over assignment than expected for user to confirm to create more student session | - |

---

### TC-14970: Verify translation

**Preconditions:** -

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Verify an error message | - | - |
| 2 | Verify new UI | - | - |

---

## Assign a student on Lesson Detail SF

### TC-14934: HQ/CM Assign a student to lesson course schedule with remaining lessons > X lessons

**Preconditions:**

* Create a course lesson schedule with program master having week order separate
    Refer TC: [ERP-1015](https://app.qase.io/case/ERP-1015)
* User has published lesson and lesson report
* User has created some LAs with Require Allocation flag = True

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | * Open the 1st lesson<br>* On Student Session, click \"Add Student\"<br>* Add a Student B to Lesson with \"Apply to Next X Lesson\" option so that remaining lessons > X lessons | Selected lesson and Exactly X lessons assigned | - |
| 2 | Check lesson report of added student | * User sees the lesson report detail is auto-created for the student | - |
| 3 | Check lesson allocation | * User sees the student session is auto-created = assigned lessons (no empty student session)<br>* User sees the lesson allocation of the student is updated (Lesson Allocated, Lesson Allocation Status, Report History) | - |
| 4 | Login BO and view a student in lesson | * User sees the student is added to Lesson | - |
| 5 | Student A login Mobile | * Student/Parent A sees the lesson and lesson report with correct information | - |
| 6 | Student B login Mobile | * Student/Parent B sees the lesson and lesson report with correct information | - |

---

### TC-14935: HQ/CM Assign a student to a daily lesson with end date with remaining lessons = X lessons

**Preconditions:**

* User has created a daily lesson by end date
* User has published all lessons in the chain

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | * Open the middle lesson<br>* On Student Session, click \"Add Student\"<br>* Add a student to Lesson with \"Apply to Next X Lesson\" option so that remaining lessons = X lessons | Selected lesson and Exactly X lessons assigned | - |
| 2 | Check lesson report of added student | * User sees the lesson report detail is auto-created for the student | - |
| 3 | Check lesson allocation | * User sees the student session is auto-created = assigned lessons (no empty student session)<br>* User sees the lesson allocation of the student is updated (Lesson Allocated, Lesson Allocation Status, Report History) | - |
| 4 | Login BO and view a student in lesson | * User sees the student is added to Lesson | - |
| 5 | Student A login Mobile | * Student A sees the lesson and lesson report with correct information | - |
| 6 | Parent B login Mobile | * Parent B sees the lesson and lesson report with correct information | - |

---

### TC-14936: HQ/CM Assign a student to a daily lesson with lesson count with remaining lessons < X lessons

**Preconditions:**

* User has created a daily lesson by lesson count
* User has published all lessons in the chain

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | * Open the last lesson<br>* On Student Session, click \"Add Student\"<br>* Add a student to Lesson with \"Apply to Next X Lessons\" option so that remaining lessons < X lessons | Selected lesson and Only the remaining lessons are assigned. | - |
| 2 | Check lesson report of added student | * User sees the lesson report detail is auto-created for the student | - |
| 3 | Check lesson allocation | * User sees the student session is auto-created = assigned lessons (no empty student session)<br>* User sees the lesson allocation of the student is updated (Lesson Allocated, Lesson Allocation Status, Report History) | - |
| 4 | Login BO and view a student in lesson | * User sees the student is added to Lesson | - |
| 5 | Student A login Mobile | * Student A sees the lesson and lesson report with correct information | - |
| 6 | Parent B login Mobile | * Parent B sees the lesson and lesson report with correct information | - |

---

### TC-14957: HQ/CM Assign a student to a imported daily lesson with remaining lessons > X lessons

**Preconditions:**

* User has imported a daily lesson
* User has published all lessons in the chain

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | * Open the last lesson<br>* On Student Session, click \"Add Student\"<br>* Add a student to Lesson with \"Apply to Next X Lessons\" option so that remaining lessons <= X lessons | Selected lesson and Only the remaining lessons are assigned. | - |
| 2 | Check lesson report of added student | * User sees the lesson report detail is auto-created for the student | - |
| 3 | Check lesson allocation | * User sees the student session is auto-created = assigned lessons (no empty student session)<br>* User sees the lesson allocation of the student is updated (Lesson Allocated, Lesson Allocation Status, Report History) | - |
| 4 | Login BO and view a student in lesson | * User sees the student is added to Lesson | - |
| 5 | Student A login Mobile | * Student A sees the lesson and lesson report with correct information | - |
| 6 | Parent B login Mobile | * Parent B sees the lesson and lesson report with correct information | - |

---

### TC-15561: HQ/CM Assign a student to lesson manual

**Preconditions:** -

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Before lesson manual | - | - |
| 2 | In lesson manual | - | - |

---

### TC-14948: HQ/CM Assign a trial student to a recurring lesson

**Preconditions:** -

_Steps TBD_

---

### TC-14941: HQ/CM Assign a student to a lesson with over assigned

**Preconditions:**

* User has created multiple recurring lessons
* User has created a LA

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Select a LA | - | - |
| 2 | Select a recurring lesson with Apply to Next X Lessons option so that **Assigned Sessions + new assignments > Total Session Count** | * User sees a student to specific lessons in the chain<br>* User sees lesson allocation status as Over Assigned | - |

---

### TC-14967: Verify existing student is not duplicated

**Preconditions:** -

_Steps TBD_

---

### TC-14978: HQ/CM Unassign the added student with following lessons

**Preconditions:** -

_Steps TBD_

---

### TC-15570: Skip assign a student to the completed and cancelled lesson

**Preconditions:** -

_Steps TBD_

---

## Assign a student on Calendar SF

### TC-14956: HQ/CM Assign multiple trial students to a recurring lesson

**Preconditions:** -

_Steps TBD_

---

### TC-14963: HQ/CM Assign multiple students to multiple lessons

**Preconditions:** -

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | HQ/CM Assign multiple students to multiple lessons with:<br><br>* remaining > X<br><br>* remaining = X<br><br>* remaining < X | Show confirmation alert when assign student to exactly X next lessons with remaining < X | - |
| 2 | Confirm to assign | For each selected lesson, the system must:<br><br>* Calculate remaining lessons from that lesson<br>* Determine the smaller of (remaining lessons) and (defined number)<br>* Assign the student to that number of lessons. | - |

---

### TC-14964: HQ/CM Assign multiple students to multiple lessons with over assigned

**Preconditions:** -

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | HQ/CM Assign multiple students to multiple lessons with:<br><br>* Lesson chain 1 is partially assigned<br>* Lesson chain 2 is fully assigned<br>* Lesson chain 3 is over assigned | Show confirmation alert when assign student to exactly X next lessons with over assigned | - |
| 2 | Confirm to assign | For each selected lesson, the system must:<br><br>* Calculate remaining lessons from that lesson<br>* Determine the smaller of (remaining lessons) and (defined number)<br>* Assign the student to that number of lessons. | - |

---

### TC-14965: HQ/CM Assign multiple students to multiple lessons with remaining > X and over assigned

**Preconditions:** -

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | HQ/CM Assign multiple students to multiple lessons with:<br><br>* remaining > X<br>* remaining = X<br>* remaining < X<br><br>AND<br><br>* Lesson chain 1 is partially assigned<br>* Lesson chain 2 is fully assigned<br>* Lesson chain 3 is over assigned | Show confirmation alert when assign student to exactly X next lessons with remaining < X | - |
| 2 | Confirm to assign | For each selected lesson, the system must:<br><br>* Calculate remaining lessons from that lesson<br>* Determine the smaller of (remaining lessons) and (defined number)<br>* Assign the student to that number of lessons. | - |

---

### TC-15585: HQ/CM Assign multiple teacher to multiple lessons

**Preconditions:** -

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | HQ/CM Assign multiple students to multiple lessons with:<br><br>* remaining > X<br><br>* remaining = X<br><br>* remaining < X | Show confirmation alert when assign student to exactly X next lessons with remaining < X | - |
| 2 | Confirm to assign | For each selected lesson, the system must:<br><br>* Calculate remaining lessons from that lesson<br>* Determine the smaller of (remaining lessons) and (defined number)<br>* Assign the student to that number of lessons. | - |

---

### TC-14966: HQ/CM Assign multiple students and teachers to multiple lessons

**Preconditions:** -

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | HQ/CM Assign multiple students and teachers to multiple lessons | For each selected lesson, the system must:<br><br>* Calculate remaining lessons from that lesson<br>* Determine the smaller of (remaining lessons) and (defined number)<br>* Assign the student to that number of lessons. | - |

---

### TC-14968: Verify existing student is not duplicated

**Preconditions:** -

_Steps TBD_

---

### TC-14979: HQ/CM Unassign the added student with following lessons

**Preconditions:** -

_Steps TBD_

---

### TC-15571: Skip assign a student to the completed and cancelled lesson

**Preconditions:** -

_Steps TBD_

---

## Assign a student on Lesson Detail BO

### TC-14958: Teacher Assign a student to a weekly lesson with end date remaining lessons > X lessons

**Preconditions:**

* User has created a weekly lesson by end date
* User has published all lessons in the chain

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | * Open the 1st lesson<br>* On Student Session, click \"Add Student\"<br>* Add a Student B to Lesson with \"Apply to Next X Lesson\" option so that remaining lessons > X lessons | Selected lesson and Exactly X lessons assigned | - |
| 2 | Check lesson report of added student | * User sees the lesson report detail is auto-created for the student | - |
| 3 | Check lesson allocation | * User sees the student session is auto-created = assigned lessons (no empty student session)<br>* User sees the lesson allocation of the student is updated (Lesson Allocated, Lesson Allocation Status, Report History) | - |
| 4 | Login BO and view a student in lesson | * User sees the student is added to Lesson | - |
| 5 | Student A login Mobile | * Student/Parent A sees the lesson and lesson report with correct information | - |
| 6 | Student B login Mobile | * Student/Parent B sees the lesson and lesson report with correct information | - |

---

### TC-14959: Teacher Assign a student to a imported weekly lesson with end date with remaining lessons = X lessons

**Preconditions:**

* User has imported a weekly lesson by end date
* User has published all lessons in the chain

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | * Open the middle lesson<br>* On Student Session, click \"Add Student\"<br>* Add a student to Lesson with \"Apply to Next X Lesson\" option so that remaining lessons = X lessons | Selected lesson and Exactly X lessons assigned | - |
| 2 | Check lesson report of added student | * User sees the lesson report detail is auto-created for the student | - |
| 3 | Check lesson allocation | * User sees the student session is auto-created = assigned lessons (no empty student session)<br>* User sees the lesson allocation of the student is updated (Lesson Allocated, Lesson Allocation Status, Report History) | - |
| 4 | Login BO and view a student in lesson | * User sees the student is added to Lesson | - |
| 5 | Student A login Mobile | * Student A sees the lesson and lesson report with correct information | - |
| 6 | Parent B login Mobile | * Parent B sees the lesson and lesson report with correct information | - |

---

### TC-14960: Teacher Assign a student to a weekly lesson with remaining lessons < X lessons

**Preconditions:**

* User has imported a weekly lesson
* User has published all lessons in the chain

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | * Open the last lesson<br>* On Student Session, click \"Add Student\"<br>* Add a student to Lesson with \"Apply to Next X Lessons\" option so that remaining lessons < X lessons | Selected lesson and Only the remaining lessons are assigned. | - |
| 2 | Check lesson report of added student | * User sees the lesson report detail is auto-created for the student | - |
| 3 | Check lesson allocation | * User sees the student session is auto-created = assigned lessons (no empty student session)<br>* User sees the lesson allocation of the student is updated (Lesson Allocated, Lesson Allocation Status, Report History) | - |
| 4 | Login BO and view a student in lesson | * User sees the student is added to Lesson | - |
| 5 | Student A login Mobile | * Student A sees the lesson and lesson report with correct information | - |
| 6 | Parent B login Mobile | * Parent B sees the lesson and lesson report with correct information | - |

---

### TC-14961: Teacher Assign a student to a lesson with over assigned

**Preconditions:**

* User has created multiple recurring lessons
* User has created a LA

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Select a LA | - | - |
| 2 | Select a recurring lesson with Apply to Next X Lessons option so that **Assigned Sessions + new assignments > Total Session Count** | * User sees a student to specific lessons in the chain<br>* User sees lesson allocation status as Over Assigned | - |

---

### TC-14962: Teacher Assign a trial student to a recurring lesson

**Preconditions:** -

_Steps TBD_

---

### TC-14969: Verify existing student is not duplicated

**Preconditions:** -

_Steps TBD_

---

### TC-14980: HQ/CM Unassign the added student with only this

**Preconditions:** -

_Steps TBD_

---

### TC-15572: Skip assign a student to the completed and cancelled lesson

**Preconditions:** -

_Steps TBD_

---

## Integration/Regression/Performance

### TC-14971: Teacher update attendance for added student

**Preconditions:** -

_Steps TBD_

---

### TC-14972: Teacher update report for added student

**Preconditions:** -

_Steps TBD_

---

### TC-14977: Teacher search lesson with added student on BO

**Preconditions:** -

_Steps TBD_

---

### TC-14973: HQ/CM assign student many times combining Only this/Following lessons/Specific lesson number

**Preconditions:** -

_Steps TBD_

---

### TC-14975: HQ/CM Assign a student to the long lesson chain (500 lessons) in lesson detail

**Preconditions:** -

_Steps TBD_

---

### TC-14976: HQ/CM Bulk Assign multiple students and multiple lessons on Calendar

**Description:** 30 students x 2 teachers x 10 lessons apply for 48 lessons

**Preconditions:** -

_Steps TBD_

---

### TC-14974: Added Student update attendance response on Mobile

**Preconditions:** -

_Steps TBD_

---
