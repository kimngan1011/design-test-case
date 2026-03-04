# Edit Lesson

## Edit lesson info

### TC-1039: Edit an one-time lesson

**Preconditions:**

* User has published the one-time lesson with student

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | * Go to the lesson detail<br>* Click on \"Edit\" button<br>* Edit lesson name, lesson code, lesson date = closed date, lesson time, classroom, lesson capacity, lesson type<br>* Click on \"Save\" button | * User sees the lesson info is updated | - |
| 2 | Login BO and view this lesson | * User sees the lesson info is updated on BO | - |
| 3 | Student login Mobile | * Student sees the notification about lesson date&time is changed | - |
| 4 | Parent login Mobile | * Parent sees the notification about lesson date&time is changed for their children | - |

---

### TC-1044: Edit lesson with the lesson course schedule

**Preconditions:**

Create a course lesson schedule with program master having week order separate
Refer TC: [https://app.qase.io/case/PX-1015](https://app.qase.io/case/PX-1015)

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Open the 2nd lesson, edit with lesson date belong to week order with only this lesson | User sees the updated lesson date | - |
| 2 | Open the 1st lesson, edit with lesson date belong to week order with this and the following | User sees the updated lesson date for this and the following lessons follow by week orde | * Lesson 1 belong to Week 1<br>* Lesson 2 belong to Week 3<br>* Lesson 3 belong to Week 5<br>* Lesson 4 belong to Week 10 |
| 3 | Open the 1st lesson, edit with lesson date = start date's week order with this and the following | User sees the updated lesson date for this and the following lessons follow by week orde | * Lesson 1 belong to Week 1<br>* Lesson 2 belong to Week 3<br>* Lesson 3 belong to Week 5<br>* Lesson 4 belong to Week 10 |
| 4 | Open the 1st lesson, edit with lesson date = end date's week order with this and the following | User sees the updated lesson date for this and the following lessons follow by week orde | * Lesson 1 belong to Week 1<br>* Lesson 2 belong to Week 3<br>* Lesson 3 belong to Week 5<br>* Lesson 4 belong to Week 10 |

---

### TC-1045: Cannot edit lesson

**Preconditions:**

* User has created a recurring lesson
* User has completed and cancelled some lessons in the middle of the chain

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Open completed lesson | User sees the Edit button is disabled | - |
| 2 | Open the 1st lesson, edit lesson info with following lesson | User sees the completed and cancelled lesson with no change | - |

---

### TC-1503: Cannot edit lesson course schedule

**Preconditions:**

Create a course lesson schedule with program master having week order separate
Refer TC: [ERP-1015](https://app.qase.io/case/ERP-1015)

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Edit with lesson date doesn't belong to week order for 1st with this and the following | Show an error message | - |
| 2 | Edit with lesson date from the week to other week the 1st with this and the following | Show an error message | - |

---

### TC-1043: Change week order and edit lesson course schedule

**Preconditions:** -

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Add more week order and edit lesson | - | - |
| 2 | Change week order and edit lesson | - | - |
| 3 | Remove week order and edit lesson | - | - |

---

### TC-8841: Edit lesson date so that the start&end date separated by 1 day of the week

**Preconditions:**

Create recurring lesson with:

* Start date: Thursday
* End date: Saturday

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Edit start date to Friday | - | - |

---

### TC-13877: Edit a recurring lesson with location that have multiple ACs and skip closed date

**Preconditions:** -

_Steps TBD_

---

## Edit lesson information in daily lesson

### TC-8293: Edit lesson date so that new lesson date < old lesson date in daily lesson with end date

**Preconditions:**

* User has created a daily lesson by end date with skip closed date

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Open a middle lesson in the chain | - | - |
| 2 | Edit lesson date so that new lesson date < old lesson date | * User sees lesson date of all lessons are recalculated from selected new lesson date | - |
| 3 | Check the last lesson in the chain | * User sees the last lesson within end date.lesson schedule | - |

---

### TC-8294: Edit lesson date so that new lesson date > old lesson date in daily lesson with end date + student

**Preconditions:**

* User has created a daily lesson by end date with skip closed date
* User has added a student to all lessons in the chain by following lessons

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Open a middle lesson in the chain | - | - |
| 2 | Edit lesson date so that new lesson date > old lesson date | * User sees lesson date of all lessons are recalculated from selected new lesson date | - |
| 3 | Check the previous lessons | * User sees the previous lessons has no changes | - |
| 4 | Check the last lesson in the chain | * User sees the last lesson within end date.lesson schedule | - |
| 5 | Check lesson allocation | * User sees number of student session = assigned lesson (no empty student session) | - |

---

### TC-8447: Edit lesson date with skip closed date in daily lesson with end date

**Preconditions:**

* User has created a daily lesson by end date with skip closed date

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Open a middle lesson in the chain | - | - |
| 2 | Edit lesson date with skip closed date | User does not see the lesson date = closed date follow the new lesson date | - |
| 3 | Check the previous lessons | * User sees the previous lessons has no changes | - |
| 4 | Check the last lesson in the chain | * User sees the last lesson within end date.lesson schedule | - |

---

### TC-8451: Edit lesson date without skip closed date in daily lesson with end date

**Preconditions:**

* User has created a daily lesson by end date with skip closed date

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Open a middle lesson in the chain | - | - |
| 2 | Edit lesson date without skip closed date | User still sees the lesson date = closed date follow the new lesson date | - |
| 3 | Check the previous lessons | * User sees the previous lessons has no changes | - |
| 4 | Check the last lesson in the chain | * User sees the last lesson within end date.lesson schedule | - |

---

### TC-8455: Edit lesson time in daily lesson with end date

**Preconditions:**

* User has created a daily lesson by end date with skip closed date

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Open a middle lesson in the chain | - | - |
| 2 | Increase lesson time with only this | User only sees the lesson time is updated for selected lesson | - |
| 3 | Open lesson before updated lesson | - | - |
| 4 | Decrease lesson time with following lessons | User sees the lesson time is updated for this and the following lessons | - |
| 5 | Check the previous lessons | * User sees the previous lessons has no changes | - |

---

### TC-8487: Edit all info in daily lesson with end date

**Preconditions:**

* User has created a daily lesson by end date with skip closed date

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Open a middle lesson in the chain | - | - |
| 2 | Edit lesson date&time with only this | User only sees the lesson date&time is updated for selected lesson | - |
| 3 | Open lesson before updated lesson | - | - |
| 4 | Edit all lesson info except lesson date&time with following lessons | User sees the all lesson info is updated for this and the following lessons, except lesson date&time | - |
| 5 | Check the previous lessons | * User sees the previous lessons has no changes | - |

---

### TC-8481: Edit lesson date after deleting a lesson in daily lesson with end date

**Preconditions:**

* User has created a daily lesson by end date with skip closed date
* User has deleted some lessons

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Edit lesson date before the deleted lesson with following lessons | * User sees lesson date is recalculated for this and the following lessons follow the new lesson date | - |
| 2 | Edit lesson date after the deleted lesson with following lessons | * User sees lesson date is recalculated for this and the following lessons follow the new lesson date | - |
| 3 | Check the last lesson in the chain | * User sees the last lesson within end date.lesson schedule | - |

---

### TC-9734: Edit lesson date so that new lesson date < old lesson date in daily lesson with lesson count

**Preconditions:**

* User has created a daily lesson by lesson count without skip closed date

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Open a middle lesson in the chain | - | - |
| 2 | Edit lesson date so that new lesson date < old lesson date | * User sees lesson date of all lessons are recalculated from selected new lesson date | - |
| 3 | Check number of lessons in the chain | * User sees number of lessons has no changes | - |
| 4 | Check end date.lesson schedule | * User sees the end date.lesson schedule = the last lesson in the chain | - |

---

### TC-9735: Edit lesson date so that new lesson date > old lesson date in daily lesson with lesson count

**Preconditions:**

* User has created a daily lesson by lesson count without skip closed date

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Open a middle lesson in the chain | - | - |
| 2 | Edit lesson date so that new lesson date > old lesson date | * User sees lesson date of all lessons are recalculated from selected new lesson date | - |
| 3 | Check the previous lessons | * User sees the previous lessons has no changes | - |
| 4 | Check number of lessons in the chain | * User sees number of lessons has no changes | - |
| 5 | Check end date.lesson schedule | * User sees the end date.lesson schedule = the last lesson in the chain | - |

---

### TC-9736: Edit lesson date with skip closed date in daily lesson with lesson count

**Preconditions:**

* User has created a daily lesson by lesson count without skip closed date

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Open a middle lesson in the chain | - | - |
| 2 | Edit lesson date with skip closed date | User does not see the lesson date = closed date follow the new lesson date | - |
| 3 | Check the previous lessons | * User sees the previous lessons has no changes | - |
| 4 | Check number of lessons in the chain | * User sees number of lessons has no changes | - |
| 5 | Check end date.lesson schedule | * User sees the end date.lesson schedule = the last lesson in the chain | - |

---

### TC-9737: Edit lesson date without skip closed date in daily lesson with lesson count

**Preconditions:**

* User has created a daily lesson by lesson count without skip closed date

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Open a middle lesson in the chain | - | - |
| 2 | Edit lesson date without skip closed date | User still sees the lesson date = closed date follow the new lesson date | - |
| 3 | Check the previous lessons | * User sees the previous lessons has no changes | - |
| 4 | Check number of lessons in the chain | * User sees number of lessons has no changes | - |
| 5 | Check end date.lesson schedule | * User sees the end date.lesson schedule = the last lesson in the chain | - |

---

### TC-9738: Edit lesson time in daily lesson with lesson count

**Preconditions:**

* User has created a daily lesson by lesson count without skip closed date

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Open a middle lesson in the chain | - | - |
| 2 | Decrease lesson time with only this | User only sees the lesson time is updated for selected lesson | - |
| 3 | Open lesson before updated lesson | - | - |
| 4 | Increase lesson time with following lessons | User sees the lesson time is updated for this and the following lessons | - |
| 5 | Check the previous lessons | * User sees the previous lessons has no changes | - |

---

### TC-9740: Edit all info in daily lesson with lesson count

**Preconditions:**

* User has created a daily lesson by lesson count without skip closed date

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Open a middle lesson in the chain | - | - |
| 2 | Edit lesson date&time with only this | User only sees the lesson date&time is updated for selected lesson | - |
| 3 | Open lesson before updated lesson | - | - |
| 4 | Edit all lesson info except lesson date&time with following lessons | User sees the all lesson info is updated for this and the following lessons, except lesson date&time | - |
| 5 | Check the previous lessons | * User sees the previous lessons has no changes | - |
| 6 | Check number of lessons in the chain | * User sees number of lessons has no changes | - |
| 7 | Check end date.lesson schedule | * User sees the end date.lesson schedule = the last lesson in the chain | - |

---

### TC-9739: Edit lesson date after deleting a lesson in daily lesson with lesson count

**Preconditions:**

* User has created a daily lesson by lesson count without skip closed date

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Edit lesson date before the deleted lesson with following lessons | * User sees lesson date is recalculated for this and the following lessons follow the new lesson date | - |
| 2 | Edit lesson date after the deleted lesson with following lessons | * User sees lesson date is recalculated for this and the following lessons follow the new lesson date | - |
| 3 | Check number of lessons in the chain | * User sees number of lessons has no changes | - |
| 4 | Check end date.lesson schedule | * User sees the end date.lesson schedule = the last lesson in the chain | - |

---

## Edit lesson information in weekly lesson

### TC-9745: Edit lesson date so that new lesson date < old lesson date in weekly lesson with end date

**Preconditions:**

* User has created a weekly lesson by end date with skip closed date

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Open a middle lesson in the chain | - | - |
| 2 | Edit lesson date so that new lesson date < old lesson date | * User sees lesson date of all lessons are recalculated from selected new lesson date | - |
| 3 | Check the last lesson in the chain | * User sees the last lesson within end date.lesson schedule | - |

---

### TC-9746: Edit lesson date so that new lesson date > old lesson date in weekly lesson with end date + student

**Preconditions:**

* User has created a weekly lesson by end date with skip closed date
* User has added a student to all lessons in the chain by following lessons

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Open a middle lesson in the chain | - | - |
| 2 | Edit lesson date so that new lesson date > old lesson date | * User sees lesson date of all lessons are recalculated from selected new lesson date | - |
| 3 | Check the previous lessons | * User sees the previous lessons has no changes | - |
| 4 | Check the last lesson in the chain | * User sees the last lesson within end date.lesson schedule | - |
| 5 | Check lesson allocation | * User sees number of student session = assigned lesson (no empty student session) | - |

---

### TC-9747: Edit lesson date with skip closed date in weekly lesson with end date

**Preconditions:**

* User has created a weekly lesson by end date with skip closed date

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Open a middle lesson in the chain | - | - |
| 2 | Edit lesson date with skip closed date | User does not see the lesson date = closed date follow the new lesson date | - |
| 3 | Check the previous lessons | * User sees the previous lessons has no changes | - |
| 4 | Check the last lesson in the chain | * User sees the last lesson within end date.lesson schedule | - |

---

### TC-9748: Edit lesson date without skip closed date in weekly lesson with end date

**Preconditions:**

* User has created a weekly lesson by end date with skip closed date

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Open a middle lesson in the chain | - | - |
| 2 | Edit lesson date without skip closed date | User still sees the lesson date = closed date follow the new lesson date | - |
| 3 | Check the previous lessons | * User sees the previous lessons has no changes | - |
| 4 | Check the last lesson in the chain | * User sees the last lesson within end date.lesson schedule | - |

---

### TC-9749: Edit lesson time in weekly lesson with end date

**Preconditions:**

* User has created a weekly lesson by end date with skip closed date

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Open a middle lesson in the chain | - | - |
| 2 | Increase lesson time with only this | User only sees the lesson time is updated for selected lesson | - |
| 3 | Open lesson before updated lesson | - | - |
| 4 | Decrease lesson time with following lessons | User sees the lesson time is updated for this and the following lessons | - |
| 5 | Check the previous lessons | * User sees the previous lessons has no changes | - |

---

### TC-9751: Edit all info in weekly lesson with end date

**Preconditions:**

* User has created a weekly lesson by end date with skip closed date

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Open a middle lesson in the chain | - | - |
| 2 | Edit lesson date&time with only this | User only sees the lesson date&time is updated for selected lesson | - |
| 3 | Open lesson before updated lesson | - | - |
| 4 | Edit all lesson info except lesson date&time with following lessons | User sees the all lesson info is updated for this and the following lessons, except lesson date&time | - |
| 5 | Check the previous lessons | * User sees the previous lessons has no changes | - |

---

### TC-9750: Edit lesson date after deleting a lesson in weekly lesson with end date

**Preconditions:**

* User has created a weekly lesson by end date with skip closed date

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Edit lesson date before the deleted lesson with following lessons | * User sees lesson date is recalculated for this and the following lessons follow the new lesson date | - |
| 2 | Edit lesson date after the deleted lesson with following lessons | * User sees lesson date is recalculated for this and the following lessons follow the new lesson date | - |
| 3 | Check the last lesson in the chain | * User sees the last lesson within end date.lesson schedule | - |

---

### TC-9752: Edit lesson date so that new lesson date < old lesson date in weekly lesson with lesson count

**Preconditions:**

* User has created a weekly lesson by lesson count without skip closed date

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Open a middle lesson in the chain | - | - |
| 2 | Edit lesson date so that new lesson date < old lesson date | * User sees lesson date of all lessons are recalculated from selected new lesson date | - |
| 3 | Check number of lessons in the chain | * User sees number of lessons has no changes | - |
| 4 | Check end date.lesson schedule | * User sees the end date.lesson schedule = the last lesson in the chain | - |

---

### TC-9753: Edit lesson date so that new lesson date > old lesson date in weekly lesson with lesson count

**Preconditions:**

* User has created a weekly lesson by lesson count without skip closed date

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Open a middle lesson in the chain | - | - |
| 2 | Edit lesson date so that new lesson date > old lesson date | * User sees lesson date of all lessons are recalculated from selected new lesson date | - |
| 3 | Check the previous lessons | * User sees the previous lessons has no changes | - |
| 4 | Check number of lessons in the chain | * User sees number of lessons has no changes | - |
| 5 | Check end date.lesson schedule | * User sees the end date.lesson schedule = the last lesson in the chain | - |

---

### TC-9754: Edit lesson date with skip closed date in weekly lesson with lesson count

**Preconditions:**

* User has created a weekly lesson by lesson count without skip closed date

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Open a middle lesson in the chain | - | - |
| 2 | Edit lesson date with skip closed date | User does not see the lesson date = closed date follow the new lesson date | - |
| 3 | Check the previous lessons | * User sees the previous lessons has no changes | - |
| 4 | Check number of lessons in the chain | * User sees number of lessons has no changes | - |
| 5 | Check end date.lesson schedule | * User sees the end date.lesson schedule = the last lesson in the chain | - |

---

### TC-9755: Edit lesson date without skip closed date in weekly lesson with lesson count

**Preconditions:**

* User has created a weekly lesson by lesson count without skip closed date

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Open a middle lesson in the chain | - | - |
| 2 | Edit lesson date without skip closed date | User still sees the lesson date = closed date follow the new lesson date | - |
| 3 | Check the previous lessons | * User sees the previous lessons has no changes | - |
| 4 | Check number of lessons in the chain | * User sees number of lessons has no changes | - |
| 5 | Check end date.lesson schedule | * User sees the end date.lesson schedule = the last lesson in the chain | - |

---

### TC-9756: Edit lesson time in weekly lesson with lesson count

**Preconditions:**

* User has created a weekly lesson by lesson count without skip closed date

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Open a middle lesson in the chain | - | - |
| 2 | Decrease lesson time with only this | User only sees the lesson time is updated for selected lesson | - |
| 3 | Open lesson before updated lesson | - | - |
| 4 | Increase lesson time with following lessons | User sees the lesson time is updated for this and the following lessons | - |
| 5 | Check the previous lessons | * User sees the previous lessons has no changes | - |

---

### TC-9758: Edit all info in weekly lesson with lesson count

**Preconditions:**

* User has created a weekly lesson by lesson count without skip closed date

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Open a middle lesson in the chain | - | - |
| 2 | Edit lesson date&time with only this | User only sees the lesson date&time is updated for selected lesson | - |
| 3 | Open lesson before updated lesson | - | - |
| 4 | Edit all lesson info except lesson date&time with following lessons | User sees the all lesson info is updated for this and the following lessons, except lesson date&time | - |
| 5 | Check the previous lessons | * User sees the previous lessons has no changes | - |
| 6 | Check number of lessons in the chain | * User sees number of lessons has no changes | - |
| 7 | Check end date.lesson schedule | * User sees the end date.lesson schedule = the last lesson in the chain | - |

---

### TC-9757: Edit lesson date after deleting a lesson in weekly lesson with lesson count

**Preconditions:**

* User has created a weekly lesson by lesson count without skip closed date

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Edit lesson date before the deleted lesson with following lessons | * User sees lesson date is recalculated for this and the following lessons follow the new lesson date | - |
| 2 | Edit lesson date after the deleted lesson with following lessons | * User sees lesson date is recalculated for this and the following lessons follow the new lesson date | - |
| 3 | Check number of lessons in the chain | * User sees number of lessons has no changes | - |
| 4 | Check end date.lesson schedule | * User sees the end date.lesson schedule = the last lesson in the chain | - |

---

## Edit lesson information in custom lesson

### TC-9763: Edit lesson date so that new lesson date < old lesson date in custom lesson with end date

**Preconditions:**

* User has created a custom lesson by end date with skip closed date

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Open a middle lesson in the chain | - | - |
| 2 | Edit lesson date so that new lesson date < old lesson date | * User sees lesson date of all lessons are recalculated from selected new lesson date | - |
| 3 | Check the last lesson in the chain | * User sees the last lesson within end date.lesson schedule | - |

---

### TC-9764: Edit lesson date so that new lesson date > old lesson date in custom lesson with end date + student

**Preconditions:**

* User has created a custom lesson by end date with skip closed date
* User has added a student to all lessons in the chain by following lessons

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Open a middle lesson in the chain | - | - |
| 2 | Edit lesson date so that new lesson date > old lesson date | * User sees lesson date of all lessons are recalculated from selected new lesson date | - |
| 3 | Check the previous lessons | * User sees the previous lessons has no changes | - |
| 4 | Check the last lesson in the chain | * User sees the last lesson within end date.lesson schedule | - |
| 5 | Check lesson allocation | * User sees number of student session = assigned lesson (no empty student session) | - |

---

### TC-9765: Edit lesson date with skip closed date in custom lesson with end date

**Preconditions:**

* User has created a custom lesson by end date with skip closed date

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Open a middle lesson in the chain | - | - |
| 2 | Edit lesson date with skip closed date | User does not see the lesson date = closed date follow the new lesson date | - |
| 3 | Check the previous lessons | * User sees the previous lessons has no changes | - |
| 4 | Check the last lesson in the chain | * User sees the last lesson within end date.lesson schedule | - |

---

### TC-9766: Edit lesson date without skip closed date in custom lesson with end date

**Preconditions:**

* User has created a custom lesson by end date with skip closed date

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Open a middle lesson in the chain | - | - |
| 2 | Edit lesson date without skip closed date | User still sees the lesson date = closed date follow the new lesson date | - |
| 3 | Check the previous lessons | * User sees the previous lessons has no changes | - |
| 4 | Check the last lesson in the chain | * User sees the last lesson within end date.lesson schedule | - |

---

### TC-9767: Edit lesson time in custom lesson with end date

**Preconditions:**

* User has created a custom lesson by end date with skip closed date

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Open a middle lesson in the chain | - | - |
| 2 | Increase lesson time with only this | User only sees the lesson time is updated for selected lesson | - |
| 3 | Open lesson before updated lesson | - | - |
| 4 | Decrease lesson time with following lessons | User sees the lesson time is updated for this and the following lessons | - |
| 5 | Check the previous lessons | * User sees the previous lessons has no changes | - |

---

### TC-9768: Edit lesson date after deleting a lesson in custom lesson with end date

**Preconditions:**

* User has created a custom lesson by end date with skip closed date

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Edit lesson date before the deleted lesson with following lessons | * User sees lesson date is recalculated for this and the following lessons follow the new lesson date | - |
| 2 | Edit lesson date after the deleted lesson with following lessons | * User sees lesson date is recalculated for this and the following lessons follow the new lesson date | - |
| 3 | Check the last lesson in the chain | * User sees the last lesson within end date.lesson schedule | - |

---

### TC-9769: Edit all info in custom lesson with end date

**Preconditions:**

* User has created a custom lesson by end date with skip closed date

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Open a middle lesson in the chain | - | - |
| 2 | Edit lesson date&time with only this | User only sees the lesson date&time is updated for selected lesson | - |
| 3 | Open lesson before updated lesson | - | - |
| 4 | Edit all lesson info except lesson date&time with following lessons | User sees the all lesson info is updated for this and the following lessons, except lesson date&time | - |
| 5 | Check the previous lessons | * User sees the previous lessons has no changes | - |

---

### TC-8479: Edit lesson date to another date in custom lesson by end date with following lessons

**Preconditions:**

* User has created a custom lesson by end date with skip closed date

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Open a middle lesson in the chain | - | - |
| 2 | Edit lesson date to another date with following lessons | Show an error message | - |

---

### TC-9778: Edit lesson date to another date in custom lesson by end date with only this

**Description:** * If user select to save Only this lesson
    * Then lesson is saved successfully without error

**Preconditions:**

* User has created a custom lesson by end date with skip closed date

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Open a middle lesson in the chain | - | - |
| 2 | Edit lesson date to another date with only this | * User sees lesson date is updated for the selected lesson | - |

---

### TC-9770: Edit lesson date so that new lesson date < old lesson date in custom lesson with lesson count

**Preconditions:**

* User has created a custom lesson by lesson count without skip closed date

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Open a middle lesson in the chain | - | - |
| 2 | Edit lesson date so that new lesson date < old lesson date | * User sees lesson date of all lessons are recalculated from selected new lesson date | - |
| 3 | Check number of lessons in the chain | * User sees number of lessons has no changes | - |
| 4 | Check end date.lesson schedule | * User sees the end date.lesson schedule = the last lesson in the chain | - |

---

### TC-9771: Edit lesson date so that new lesson date > old lesson date in custom lesson with lesson count

**Preconditions:**

* User has created a custom lesson by lesson count without skip closed date

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Open a middle lesson in the chain | - | - |
| 2 | Edit lesson date so that new lesson date > old lesson date | * User sees lesson date of all lessons are recalculated from selected new lesson date | - |
| 3 | Check the previous lessons | * User sees the previous lessons has no changes | - |
| 4 | Check number of lessons in the chain | * User sees number of lessons has no changes | - |
| 5 | Check end date.lesson schedule | * User sees the end date.lesson schedule = the last lesson in the chain | - |

---

### TC-9772: Edit lesson date with skip closed date in custom lesson with lesson count

**Preconditions:**

* User has created a custom lesson by lesson count without skip closed date

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Open a middle lesson in the chain | - | - |
| 2 | Edit lesson date with skip closed date | User does not see the lesson date = closed date follow the new lesson date | - |
| 3 | Check the previous lessons | * User sees the previous lessons has no changes | - |
| 4 | Check number of lessons in the chain | * User sees number of lessons has no changes | - |
| 5 | Check end date.lesson schedule | * User sees the end date.lesson schedule = the last lesson in the chain | - |

---

### TC-9773: Edit lesson date without skip closed date in custom lesson with lesson count

**Preconditions:**

* User has created a custom lesson by lesson count without skip closed date

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Open a middle lesson in the chain | - | - |
| 2 | Edit lesson date without skip closed date | User still sees the lesson date = closed date follow the new lesson date | - |
| 3 | Check the previous lessons | * User sees the previous lessons has no changes | - |
| 4 | Check number of lessons in the chain | * User sees number of lessons has no changes | - |
| 5 | Check end date.lesson schedule | * User sees the end date.lesson schedule = the last lesson in the chain | - |

---

### TC-9774: Edit lesson time in custom lesson with lesson count

**Preconditions:**

* User has created a custom lesson by lesson count without skip closed date

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Open a middle lesson in the chain | - | - |
| 2 | Decrease lesson time with only this | User only sees the lesson time is updated for selected lesson | - |
| 3 | Open lesson before updated lesson | - | - |
| 4 | Increase lesson time with following lessons | User sees the lesson time is updated for this and the following lessons | - |
| 5 | Check the previous lessons | * User sees the previous lessons has no changes | - |

---

### TC-9775: Edit lesson date after deleting a lesson in custom lesson with lesson count

**Preconditions:**

* User has created a custom lesson by lesson count without skip closed date

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Edit lesson date before the deleted lesson with following lessons | * User sees lesson date is recalculated for this and the following lessons follow the new lesson date | - |
| 2 | Edit lesson date after the deleted lesson with following lessons | * User sees lesson date is recalculated for this and the following lessons follow the new lesson date | - |
| 3 | Check number of lessons in the chain | * User sees number of lessons has no changes | - |
| 4 | Check end date.lesson schedule | * User sees the end date.lesson schedule = the last lesson in the chain | - |

---

### TC-9776: Edit all info in custom lesson with lesson count

**Preconditions:**

* User has created a custom lesson by lesson count without skip closed date

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Open a middle lesson in the chain | - | - |
| 2 | Edit lesson date&time with only this | User only sees the lesson date&time is updated for selected lesson | - |
| 3 | Open lesson before updated lesson | - | - |
| 4 | Edit all lesson info except lesson date&time with following lessons | User sees the all lesson info is updated for this and the following lessons, except lesson date&time | - |
| 5 | Check the previous lessons | * User sees the previous lessons has no changes | - |
| 6 | Check number of lessons in the chain | * User sees number of lessons has no changes | - |
| 7 | Check end date.lesson schedule | * User sees the end date.lesson schedule = the last lesson in the chain | - |

---

### TC-9779: Edit lesson date to another date in custom lesson by lesson count with following lessons

**Preconditions:**

* User has created a custom lesson by lesson count with skip closed date

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Open a middle lesson in the chain | - | - |
| 2 | Edit lesson date to another date with following lessons | Show an error message | - |

---

### TC-9780: Edit lesson date to another date in custom lesson by lesson count with only this

**Description:** * If user select to save Only this lesson
    * Then lesson is saved successfully without error

**Preconditions:**

* User has created a custom lesson by lesson count with skip closed date

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Open a middle lesson in the chain | - | - |
| 2 | Edit lesson date to another date with only this | * User sees lesson date is updated for the selected lesson | - |

---

## Send noti when changing lesson date&time of a published lesson

### TC-11342: Send noti when changing lesson date&time of a published one time lesson

**Preconditions:**

* User has published an one time lesson (refer to [https://app.qase.io/case/PX-1456](https://app.qase.io/case/PX-1456))
* User has added a student to a lesson
* Parent/Student has login Mobile app

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Open the detailed lesson page | - | - |
| 2 | Edit lesson date | Student and Parent sees the reschedule lesson noti and view the lesson detail when clicking the button | - |
| 3 | Edit lesson time | Student and Parent sees the reschedule lesson noti and view the lesson detail when clicking the button | - |
| 4 | Edit lesson date&time | Student and Parent sees the reschedule lesson noti and view the lesson detail when clicking the button | - |

---

### TC-11343: Send noti when changing lesson date&time of a published lesson course schedule

**Preconditions:**

* User has published a lesson course schedule (refer to [https://app.qase.io/case/PX-1016](https://app.qase.io/case/PX-1016))
* User has added a student to a lesson
* Parent/Student has login Mobile app

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Open the detailed lesson page | - | - |
| 2 | Edit lesson date | Student and Parent sees the reschedule lesson noti and view the lesson detail when clicking the button | - |
| 3 | Edit lesson time | Student and Parent sees the reschedule lesson noti and view the lesson detail when clicking the button | - |
| 4 | Edit lesson date&time | Student and Parent sees the reschedule lesson noti and view the lesson detail when clicking the button | - |

---

### TC-11344: Send noti when changing lesson date&time of a published manual lesson

**Preconditions:**

* User has published a manual lesson (refer to [https://app.qase.io/case/PX-1018](https://app.qase.io/case/PX-1018))
* User has added a student to a lesson
* Parent/Student has login Mobile app

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Open the detailed lesson page | - | - |
| 2 | Edit lesson date | Student and Parent sees the reschedule lesson noti and view the lesson detail when clicking the button | - |
| 3 | Edit lesson time | Student and Parent sees the reschedule lesson noti and view the lesson detail when clicking the button | - |
| 4 | Edit lesson date&time | Student and Parent sees the reschedule lesson noti and view the lesson detail when clicking the button | - |

---

### TC-11345: Send noti when changing lesson date&time of a published daily lesson

**Preconditions:**

* User has published a daily lesson (refer to [https://app.qase.io/case/PX-1018](https://app.qase.io/case/PX-1018))
* User has added a student to all lessons in the chain
* Parent/Student has login Mobile app

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Open the detailed lesson page | - | - |
| 2 | Edit lesson date with only this | Student and Parent sees the reschedule lesson noti and view the lesson detail when clicking the button | - |
| 3 | Edit lesson time with only | Student and Parent sees the reschedule lesson noti and view the lesson detail when clicking the button | - |
| 4 | Edit lesson date&time with this and the following | * Student and Parent only sees the reschedule lesson noti of selected lesson<br><br>* Student and Parent can view the lesson detail when clicking the button | - |

---

### TC-11346: Send noti when changing lesson date&time of a published weekly lesson

**Preconditions:**

* User has published a weekly lesson (refer to [https://app.qase.io/case/PX-1018](https://app.qase.io/case/PX-1018))
* User has added a student to all lessons in the chain
* Parent/Student has login Mobile app

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Open the detailed lesson page | - | - |
| 2 | Edit lesson date with only this | Student and Parent sees the reschedule lesson noti and view the lesson detail when clicking the button | - |
| 3 | Edit lesson time with only | Student and Parent sees the reschedule lesson noti and view the lesson detail when clicking the button | - |
| 4 | Edit lesson date&time with this and the following | * Student and Parent only sees the reschedule lesson noti of selected lesson<br><br>* Student and Parent can view the lesson detail when clicking the button | - |

---

### TC-11347: Send noti when changing lesson date&time of a published custom lesson

**Preconditions:**

* User has published a custom lesson (refer to [https://app.qase.io/case/PX-1018](https://app.qase.io/case/PX-1018))
* User has added a student to all lessons in the chain
* Parent/Student has login Mobile app

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Open the detailed lesson page | - | - |
| 2 | Edit lesson date with only this | Student and Parent sees the reschedule lesson noti and view the lesson detail when clicking the button | - |
| 3 | Edit lesson time with only | Student and Parent sees the reschedule lesson noti and view the lesson detail when clicking the button | - |
| 4 | Edit lesson date&time with this and the following | * Student and Parent only sees the reschedule lesson noti of selected lesson<br><br>* Student and Parent can view the lesson detail when clicking the button | - |

---

### TC-11350: Send noti when editing all lesson info

**Preconditions:**

* User has published an one time lesson (refer to [https://app.qase.io/case/PX-1456](https://app.qase.io/case/PX-1456))
* User has added a student to a lesson
* Parent/Student has login Mobile app

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Open the detailed lesson page | - | - |
| 2 | Edit all lesson info | Student and Parent sees the reschedule lesson noti and view the lesson detail when clicking the button | - |

---

### TC-11349: Do not send noti when edit all lesson info exclude lesson date&time

**Preconditions:**

* User has published an one time lesson (refer to [https://app.qase.io/case/PX-1456](https://app.qase.io/case/PX-1456))
* User has added a student to a lesson
* Parent/Student has login Mobile app

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Open the detailed lesson page | - | - |
| 2 | Edit all lesson info exclude lesson date&time | Student and Parent does not see the reschedule lesson noti | - |

---

### TC-11351: Do not send noti when cancelling the confirm popup

**Preconditions:**

* User has published an one time lesson (refer to [https://app.qase.io/case/PX-1456](https://app.qase.io/case/PX-1456))
* User has added a student to a lesson
* Parent/Student has login Mobile app

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Open the detailed lesson page | - | - |
| 2 | * Edit lesson date<br>* Click \"Don't Send\" on the Confirm popup | Student and Parent does not see the reschedule lesson noti | - |

---
