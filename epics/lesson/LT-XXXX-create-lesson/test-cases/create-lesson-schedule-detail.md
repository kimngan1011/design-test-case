# Create Lesson Schedule Detail Test Cases

---

## TC-1017: Verify add lesson form

**Description:** Verify that all related details are properly linked and accessible from the lesson details page.

**Preconditions:**

* User has created a recurring lessons

**Steps:**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open lesson schedule, click \"Add Lesson\" button | Pre-filled and Editable:<br><br>* Date \u2192 Pre-filled by the Lesson Schedule\u2019s end date + 7 days<br>* Lesson Name \u2192 pre-filled by Lesson Schedule\u2019s lesson name<br>* Start Time \u2192 pre-filled by Lesson Schedule\u2019s start time<br>* End Time \u2192 pre-filled by Lesson Schedule\u2019s end time<br>* Day of the Week \u2192 Auto-calculated based on the Date<br>* Duration \u2192 Auto-calculated based on Start Time and End Time<br>* Teaching Medium \u2192 pre-filled by Lesson Schedule\u2019s teaching medium<br>* Classroom \u2192 User can search and select from available classrooms<br><br>Pre-filled and Not Editable<br><br>* Location<br>* Academic Year<br>* Course<br>* Class<br>* Teaching Method<br><br>Default Blank (User Input Required)<br><br>* Lesson Code<br>* Lesson Type<br>* Lesson Capacity (optional) |  |


---

## TC-1018: Create a lesson with lesson date within the lesson schedule duration in daily lesson with end date

**Preconditions:**

* User has created a group daily lesson by end date with Class A

**Steps:**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open lesson schedule<br><br><br> |  |  |
| 2 | Create a lesson with lesson date within the lesson schedule duration | User sees the lesson is created with correct information |  |


---

## TC-8459: Create a lesson with lesson date within the lesson schedule duration in daily lesson with lesson count

**Preconditions:**

* User has created a daily lesson by inputting lesson count

**Steps:**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open lesson schedule<br><br><br> |  |  |
| 2 | Create a lesson with lesson date within the lesson schedule duration | User sees the lesson is created with correct information |  |


---

## TC-9003: Create a lesson with lesson date < start date time.lesson schedule in daily lesson with lesson count

**Description:** Check that the system prevents lesson creation when an invalid date or time is entered.

**Preconditions:**

* User has created a daily lesson by inputting lesson count

**Steps:**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open lesson schedule<br><br><br> |  |  |
| 2 | Create a lesson with lesson date < start date time.lesson schedule | User sees the lesson is created with correct information<br><br><br> |  |
| 3 | Check start date time.lesson schedule | User sees the start date.lesson schedule is updated |  |


---

## TC-9004: Create a lesson with lesson date < start date time.lesson schedule in daily lesson with end date

**Description:** Check that the system prevents lesson creation when an invalid date or time is entered.

**Preconditions:**

* User has created a daily lesson by end date

**Steps:**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open lesson schedule<br><br><br> |  |  |
| 2 | Create a lesson with lesson date < start date time.lesson schedule | User sees the lesson is created with correct information<br><br><br> |  |
| 3 | Check start date time.lesson schedule | User sees the start date.lesson schedule is updated |  |


---

## TC-9008: Create a lesson with lesson date > end date time.lesson schedule in daily lesson with lesson count

**Preconditions:**

* User has created a daily lesson by inputting lesson count

**Steps:**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open lesson schedule<br><br><br> |  |  |
| 2 | Create a lesson with lesson date > end date time.lesson schedule<br><br><br> | User sees the lesson is created with correct information<br><br><br> |  |
| 3 | Check end date time.lesson schedule | User sees the end date.lesson schedule is updated<br><br><br> |  |


---

## TC-9006: Create a lesson with lesson date > end date time.lesson schedule in daily lesson with end date

**Preconditions:**

* User has created a daily lesson by end date

**Steps:**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open lesson schedule<br><br><br> |  |  |
| 2 | Create a lesson with lesson date > end date time.lesson schedule<br><br><br> | User sees the lesson is created with correct information<br><br><br> |  |
| 3 | Check end date time.lesson schedule | User sees the end date.lesson schedule is updated<br><br><br> |  |


---

## TC-1019: Create a lesson with lesson date < start date time.lesson schedule in weekly lesson with lesson count

**Description:** Check that the system prevents lesson creation when an invalid date or time is entered.

**Preconditions:**

* User has created a weekly lesson by inputting lesson count

**Steps:**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open lesson schedule<br><br><br> |  |  |
| 2 | Create a lesson with lesson date < start date time.lesson schedule | User sees the lesson is created with correct information<br><br><br> |  |
| 3 | Check start date time.lesson schedule | User sees the start date.lesson schedule is updated |  |


---

## TC-8460: Create a lesson with lesson date < start date time.lesson schedule in weekly lesson with end date

**Description:** Check that the system prevents lesson creation when an invalid date or time is entered.

**Preconditions:**

* User has created a weekly by end date

**Steps:**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open lesson schedule<br><br><br> |  |  |
| 2 | Create a lesson with lesson date < start date time.lesson schedule | User sees the lesson is created with correct information<br><br><br> |  |
| 3 | Check start date time.lesson schedule | User sees the start date.lesson schedule is updated |  |


---

## TC-8999: Create a lesson with lesson date within the lesson schedule duration in weekly lesson with end date

**Preconditions:**

* User has created a weekly by end date

**Steps:**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open lesson schedule<br><br><br> |  |  |
| 2 | Create a lesson with lesson date within the lesson schedule duration | User sees the lesson is created with correct information |  |


---

## TC-9000: Create a lesson with lesson date within the lesson schedule duration in weekly lesson with lesson count

**Preconditions:**

* User has created a weekly lesson by inputting lesson count

**Steps:**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open lesson schedule<br><br><br> |  |  |
| 2 | Create a lesson with lesson date within the lesson schedule duration | User sees the lesson is created with correct information |  |


---

## TC-9009: Create a lesson with lesson date > end date time.lesson schedule in weekly lesson with end date

**Preconditions:**

* User has created a weekly by end date

**Steps:**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open lesson schedule<br><br><br> |  |  |
| 2 | Create a lesson with lesson date > end date time.lesson schedule<br><br><br> | User sees the lesson is created with correct information<br><br><br> |  |
| 3 | Check end date time.lesson schedule | User sees the end date.lesson schedule is updated<br><br><br> |  |


---

## TC-9010: Create a lesson with lesson date > end date time.lesson schedule in weekly lesson with lesson count

**Preconditions:**

* User has created a weekly lesson by inputting lesson count

**Steps:**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open lesson schedule<br><br><br> |  |  |
| 2 | Create a lesson with lesson date > end date time.lesson schedule<br><br><br> | User sees the lesson is created with correct information<br><br><br> |  |
| 3 | Check end date time.lesson schedule | User sees the end date.lesson schedule is updated<br><br><br> |  |


---

## TC-1020: Create a lesson with lesson date > end date time.lesson schedule in custom lesson with end date

**Preconditions:**

* User has created a custom lesson by end date

**Steps:**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open lesson schedule<br><br><br> |  |  |
| 2 | Create a lesson with lesson date > end date time.lesson schedule<br><br><br> | User sees the lesson is created with correct information<br><br><br> |  |
| 3 | Check end date time.lesson schedule | User sees the end date.lesson schedule is updated<br><br><br> |  |


---

## TC-8461: Create a lesson with lesson date > end date time.lesson schedule in custom lesson with lesson count

**Preconditions:**

* User has created a custom lesson by inputting lesson count

**Steps:**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open lesson schedule<br><br><br> |  |  |
| 2 | Create a lesson with lesson date > end date time.lesson schedule<br><br><br> | User sees the lesson is created with correct information<br><br><br> |  |
| 3 | Check end date time.lesson schedule | User sees the end date.lesson schedule is updated<br><br><br> |  |


---

## TC-9001: Create a lesson with lesson date within the lesson schedule duration in custom lesson with end date

**Preconditions:**

* User has created a custom lesson by end date

**Steps:**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open lesson schedule<br><br><br> |  |  |
| 2 | Create a lesson with:<br><br>* Lesson date within the lesson schedule duration<br>* Day of week != selected day of week | User sees the lesson is created with correct information |  |


---

## TC-9002: Create a lesson with lesson date within the lesson schedule duration in custom lesson with lesson count

**Preconditions:**

* User has created a custom lesson by inputting lesson count

**Steps:**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open lesson schedule<br><br><br> |  |  |
| 2 | Create a lesson with lesson date within the lesson schedule duration with a different chain's day of the week | User sees the lesson is created with correct information |  |


---

## TC-9005: Create a lesson with lesson date < start date time.lesson schedule in custom lesson with lesson count

**Description:** Check that the system prevents lesson creation when an invalid date or time is entered.

**Preconditions:**

* User has created a custom lesson by inputting lesson count

**Steps:**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open lesson schedule<br><br><br> |  |  |
| 2 | Create a lesson with lesson date < start date time.lesson schedule | User sees the lesson is created with correct information<br><br><br> |  |
| 3 | Check start date time.lesson schedule | User sees the start date.lesson schedule is updated |  |


---

## TC-9007: Create a lesson with lesson date < start date time.lesson schedule in custom lesson with end date

**Description:** Check that the system prevents lesson creation when an invalid date or time is entered.

**Preconditions:**

* User has created a custom lesson by end date

**Steps:**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open lesson schedule<br><br><br> |  |  |
| 2 | Create a lesson with lesson date < start date time.lesson schedule | User sees the lesson is created with correct information<br><br><br> |  |
| 3 | Check start date time.lesson schedule | User sees the start date.lesson schedule is updated |  |


---

## TC-1021: Create a lesson with lesson date = closed date

**Preconditions:**

* User has created a daily/weekly/custom lesson

**Steps:**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open lesson schedule<br><br><br> |  |  |
| 2 | Create a lesson with lesson date = closed date | User sees the lesson is created with correct information<br><br><br> |  |


---

## TC-1024: Do not allow creating a lesson with lesson date = any lessons in the lesson schedule

**Preconditions:**

* User has created a daily/weekly/custom lesson

**Steps:**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open lesson schedule<br><br><br> |  |  |
| 2 | Create a lesson with lesson date = any lessons in the lesson schedule | Show an error message |  |


---

## TC-1025: Edit lesson manual

**Preconditions:**

* User has created a lesson manual in daily/weekly/custom lesson

**Steps:**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open the lesson, edit lesson info | User sees the lesson info is updated |  |
| 2 | Click on Save button | * User does not see the Recurring popup<br>* User sees the lesson info is updated |  |


---

## TC-8758: Skip duplicate lesson date after editing lesson date in lesson count and recalculation

**Preconditions:**

* User has created a daily/weekly/custom lesson count with skip closed date
* User has created a lesson manual with lesson date = closed date

**Steps:**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open lesson before lesson manual |  |  |
| 2 | Edit lesson date without skip closed date so that the generated lesson = lesson manual | * User does not sees generated lesson = lesson manual is created |  |
| 3 | Check number of lessons in the chain | * User sees number of lessons has no changes |  |


---

## TC-9692: Skip duplicate lesson date after editing lesson date in lesson end date and recalculation

**Preconditions:**

* User has created a daily/weekly/custom lesson end date with skip closed date
* User has created a lesson manual with lesson date = closed date

**Steps:**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open lesson before lesson manual |  |  |
| 2 | Edit lesson date without skip closed date so that the generated lesson = lesson manual | * User does not sees generated lesson = lesson manual is created |  |
| 3 | Check the last lesson in the chain | * User sees the last lesson within end date.lesson schedule |  |


---

## TC-9691: Skip update lesson manual after editing lesson info in lesson count with following lessons

**Preconditions:**

* User has created a daily/weekly/custom lesson count with skip closed date
* User has created a lesson manual

**Steps:**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open lesson before lesson manual |  |  |
| 2 | Edit all information with following lessons | * User sees a lesson manual has no changes |  |
| 3 | Check the number of lessons | * User sees the number of lesson has no changes |  |


---

## TC-9693: Skip update lesson manual after editing lesson info in lesson end date with following lessons

**Preconditions:**

* User has created a daily/weekly/custom lesson end date with skip closed date
* User has created a lesson manual

**Steps:**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open lesson before lesson manual |  |  |
| 2 | Edit all information with following lessons | * User sees a lesson manual has no changes |  |
| 3 | Check the last lesson in the chain | * User sees the last lesson within end date.lesson schedule |  |


---

## TC-9694: Edit lesson date with lesson manual after deleting some lessons in lesson count

**Preconditions:**

* User has created daily/weekly/custom lesson count
* User has created a lesson manual
* User has deleted some lesson in the chain

**Steps:**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | User open lesson before lesson manual |  |  |
| 2 | Edit lesson date with following lesson | * User sees the total number of lessons in the chain = selected lesson count, excluding lesson manual |  |


---

## TC-9695: Edit lesson date with lesson manual after deleting some lessons in lesson end date

**Preconditions:**

* User has created daily/weekly/custom lesson end date
* User has created a lesson manual
* User has deleted some lesson in the chain

**Steps:**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | User open lesson before lesson manual |  |  |
| 2 | Edit lesson date with following lesson | * User sees the last lesson within end date.lesson schedule, excluding lesson manual |  |


---

## TC-8759: Assign a student/teacher to manual lesson with following lesson

**Preconditions:**

* User has created daily/weekly/custom lesson
* User has created a lesson manual and published it

**Steps:**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open lesson manaul |  |  |
| 2 | Assign student A and teacher <br>A with following lessons | * User sees student and teacher is added to lesson manual and following lessons in the chain |  |
| 3 | Check previous lessons | * User sees previous lessons has no change |  |
| 4 | Student A login Mobile | * Student A sees the lesson and lesson report with correct information |  |


---

## TC-9696: Assign a student/teacher to a lesson before lesson manual with following lesson

**Preconditions:**

* User has created daily/weekly/custom lesson
* User has created a lesson manual

**Steps:**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open a lesson before lesson manual |  |  |
| 2 | Assign student and teacher with following lessons | * User sees student and teacher is added to lesson manual and following lessons in the chain |  |
| 3 | Check previous lessons | * User sees previous lessons has no change |  |


---

## TC-9697: Unassign a student/teacher from lesson manual with following lesson

**Preconditions:**

* User has created daily/weekly/custom lesson
* User has created a lesson manual
* User has assigned a student and teacher to lesson manual

**Steps:**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open lesson manaul |  |  |
| 2 | Unassign student and teacher with following lessons | * User does not see a student and teacher in lesson manual and following lessons in the chain |  |
| 3 | Check previous lessons | * User sees previous lessons has no change |  |
| 4 | Check lesson allocation | * User sees the student sessions linked to the lessons which the removed student is deleted<br>* User sees the lesson allocation of the student is updated (Lesson Allocated, Lesson Allocation Status, Report History) |  |


---

## TC-9698: Unassign a student/teacher from a lesson before lesson manual with following lesson

**Preconditions:**

* User has created daily/weekly/custom lesson
* User has created a lesson manual
* User has assigned a student and teacher to lesson before lesson manual

**Steps:**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open lesson before lesson manual |  |  |
| 2 | UnAssign student and teacher with following lessons | * User does not see a student and teacher in lesson manual and following lessons in the chain |  |
| 3 | Check previous lessons | * User sees previous lessons has no change |  |
| 4 | Check lesson allocation | * User sees the student sessions linked to the lessons which the removed student is deleted<br>* User sees the lesson allocation of the student is updated (Lesson Allocated, Lesson Allocation Status, Report History) |  |


---

## TC-1028: Verify the Add Lesson button in the one-time lesson and course schedule lesson

**Preconditions:**

* User has setup the master data

**Steps:**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open lesson schedule of the one-time lesson | User does not see the button |  |
| 2 | Open lesson schedule of the course schedule lesson | User does not see the button |  |


---

## TC-1029: Verify add lesson button with the user has no permission

**Preconditions:**

* User has setup the master data


---
