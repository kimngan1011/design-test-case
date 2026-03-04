# Lesson Status

## Change lesson status in detailed lesson page

### TC-1456: User change lesson status of daily lesson by end date

**Preconditions:**

* User has created a daily lesson by end date in the past with a student
* User has published a lesson report

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Change the status draft -> published<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ Login BO and view the lesson<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ Parent login Mobile | * User sees the lesson status is updated to Published<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ * User sees the lesson's status is Published on BO<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ Parent sees the lesson and lesson report with correct information | - |
| 2 | Change the status published -> completed<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ Login BO and view the lesson<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ Parent login Mobile | * User sees the lesson status is updated to Completed<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ * User sees the lesson's status is Completed on BO<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ Parent sees the lesson and lesson report with correct information | - |
| 3 | Change the status completed -> published | User sees the lesson status is updated to Published | - |
| 4 | * Fill in the Cancellation Reason<br><br>* Change the status published -> cancelled<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ Login BO and view the lesson<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ Parent login Mobile | User sees the lesson status is updated to Cancelled<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ User sees the lesson's status is Cancelled on BO<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ Parent sees the lesson and lesson report with correct information | - |
| 5 | Change the status cancelled -> draft<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ Login BO and view the lesson<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ Parent login Mobile and view the lesson | * User sees the lesson status is updated to Draft<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ User sees the lesson's status is Draft on BO<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ Parent does not see the lesson | - |
| 6 | Change the status draft -> cancelled | User sees the lesson status is updated to Cancelled | - |

---

### TC-9786: User change lesson status of daily lesson by lesson count

**Preconditions:**

* User has created a daily lesson by lesson count in the past with a student
* User has published a lesson report

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Change the status draft -> published<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ Login BO and view the lesson<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ Parent login Mobile | * User sees the lesson status is updated to Published<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ * User sees the lesson's status is Published on BO<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ Parent sees the lesson and lesson report with correct information | - |
| 2 | Change the status published -> completed<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ Login BO and view the lesson<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ Parent login Mobile | * User sees the lesson status is updated to Completed<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ * User sees the lesson's status is Completed on BO<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ Parent sees the lesson and lesson report with correct information | - |
| 3 | Change the status completed -> published | User sees the lesson status is updated to Published | - |
| 4 | * Fill in the Cancellation Reason<br><br>* Change the status published -> cancelled<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ Login BO and view the lesson<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ Parent login Mobile | User sees the lesson status is updated to Cancelled<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ User sees the lesson's status is Cancelled on BO<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ Parent sees the lesson and lesson report with correct information | - |
| 5 | Change the status cancelled -> draft<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ Login BO and view the lesson<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ Parent login Mobile and view the lesson | * User sees the lesson status is updated to Draft<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ User sees the lesson's status is Draft on BO<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ Parent does not see the lesson | - |
| 6 | Change the status draft -> cancelled | User sees the lesson status is updated to Cancelled | - |

---

### TC-9788: User change lesson status of weekly lesson by end date

**Preconditions:**

* User has created a weekly lesson by end date in the past with a student
* User has published a lesson report

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Change the status draft -> published<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ Login BO and view the lesson<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ Parent login Mobile | * User sees the lesson status is updated to Published<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ * User sees the lesson's status is Published on BO<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ Parent sees the lesson and lesson report with correct information | - |
| 2 | Change the status published -> completed<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ Login BO and view the lesson<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ Parent login Mobile | * User sees the lesson status is updated to Completed<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ * User sees the lesson's status is Completed on BO<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ Parent sees the lesson and lesson report with correct information | - |
| 3 | Change the status completed -> published | User sees the lesson status is updated to Published | - |
| 4 | * Fill in the Cancellation Reason<br><br>* Change the status published -> cancelled<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ Login BO and view the lesson<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ Parent login Mobile | User sees the lesson status is updated to Cancelled<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ User sees the lesson's status is Cancelled on BO<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ Parent sees the lesson and lesson report with correct information | - |
| 5 | Change the status cancelled -> draft<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ Login BO and view the lesson<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ Parent login Mobile and view the lesson | * User sees the lesson status is updated to Draft<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ User sees the lesson's status is Draft on BO<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ Parent does not see the lesson | - |
| 6 | Change the status draft -> cancelled | User sees the lesson status is updated to Cancelled | - |

---

### TC-9789: User change lesson status of weekly lesson by lesson count

**Preconditions:**

* User has created a weekly lesson by lesson count in the past with a student
* User has published a lesson report

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Change the status draft -> published<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ Login BO and view the lesson<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ Parent login Mobile | * User sees the lesson status is updated to Published<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ * User sees the lesson's status is Published on BO<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ Parent sees the lesson and lesson report with correct information | - |
| 2 | Change the status published -> completed<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ Login BO and view the lesson<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ Parent login Mobile | * User sees the lesson status is updated to Completed<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ * User sees the lesson's status is Completed on BO<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ Parent sees the lesson and lesson report with correct information | - |
| 3 | Change the status completed -> published | User sees the lesson status is updated to Published | - |
| 4 | * Fill in the Cancellation Reason<br><br>* Change the status published -> cancelled<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ Login BO and view the lesson<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ Parent login Mobile | User sees the lesson status is updated to Cancelled<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ User sees the lesson's status is Cancelled on BO<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ Parent sees the lesson and lesson report with correct information | - |
| 5 | Change the status cancelled -> draft<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ Login BO and view the lesson<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ Parent login Mobile and view the lesson | * User sees the lesson status is updated to Draft<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ User sees the lesson's status is Draft on BO<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ Parent does not see the lesson | - |
| 6 | Change the status draft -> cancelled | User sees the lesson status is updated to Cancelled | - |

---

### TC-9790: User change lesson status of custom lesson by end date

**Preconditions:**

* User has created a custom lesson by end date in the past with a student
* User has published a lesson report

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Change the status draft -> published<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ Login BO and view the lesson<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ Parent login Mobile | * User sees the lesson status is updated to Published<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ * User sees the lesson's status is Published on BO<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ Parent sees the lesson and lesson report with correct information | - |
| 2 | Change the status published -> completed<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ Login BO and view the lesson<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ Parent login Mobile | * User sees the lesson status is updated to Completed<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ * User sees the lesson's status is Completed on BO<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ Parent sees the lesson and lesson report with correct information | - |
| 3 | Change the status completed -> published | User sees the lesson status is updated to Published | - |
| 4 | * Fill in the Cancellation Reason<br><br>* Change the status published -> cancelled<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ Login BO and view the lesson<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ Parent login Mobile | User sees the lesson status is updated to Cancelled<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ User sees the lesson's status is Cancelled on BO<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ Parent sees the lesson and lesson report with correct information | - |
| 5 | Change the status cancelled -> draft<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ Login BO and view the lesson<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ Parent login Mobile and view the lesson | * User sees the lesson status is updated to Draft<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ User sees the lesson's status is Draft on BO<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ Parent does not see the lesson | - |
| 6 | Change the status draft -> cancelled | User sees the lesson status is updated to Cancelled | - |

---

### TC-9791: User change lesson status of custom lesson by lesson count

**Preconditions:**

* User has created a custom lesson by lesson count in the past with a student
* User has published a lesson report

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Change the status draft -> published<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ Login BO and view the lesson<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ Parent login Mobile | * User sees the lesson status is updated to Published<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ * User sees the lesson's status is Published on BO<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ Parent sees the lesson and lesson report with correct information | - |
| 2 | Change the status published -> completed<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ Login BO and view the lesson<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ Parent login Mobile | * User sees the lesson status is updated to Completed<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ * User sees the lesson's status is Completed on BO<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ Parent sees the lesson and lesson report with correct information | - |
| 3 | Change the status completed -> published | User sees the lesson status is updated to Published | - |
| 4 | * Fill in the Cancellation Reason<br><br>* Change the status published -> cancelled<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ Login BO and view the lesson<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ Parent login Mobile | User sees the lesson status is updated to Cancelled<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ User sees the lesson's status is Cancelled on BO<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ Parent sees the lesson and lesson report with correct information | - |
| 5 | Change the status cancelled -> draft<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ Login BO and view the lesson<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ Parent login Mobile and view the lesson | * User sees the lesson status is updated to Draft<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ User sees the lesson's status is Draft on BO<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ Parent does not see the lesson | - |
| 6 | Change the status draft -> cancelled | User sees the lesson status is updated to Cancelled | - |

---

### TC-1465: User cannot change lesson status

**Preconditions:** -

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Change the status draft -> cancelled | User sees an error message \"Missing cancellation reason\" | - |
| 2 | Change the status draft -> completed | User sees an error message | - |
| 3 | * Create a published lesson in the future <br>* Change the status published -> completed | User sees an error message | - |
| 4 | Change the status published -> cancelled | User sees an error message | - |
| 5 | Change the status completed -> cancelled | User sees an error message | - |
| 6 | Change the status completed -> draft | User sees an error message | - |
| 7 | Change the status cancelled -> published | User sees an error message | - |
| 8 | Change the status cancelled -> completed | User sees an error message | - |

---

## Bulk update lesson status in lesson list

### TC-1469: User uses bulk update draft lesson status

**Preconditions:**

* User has created some daily/weekly/custom by end date/lesson count lessons with a teacher and student

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | * On the lesson list, select a published, completed and cancelled lesson<br>* Click on \"Bulk Update Lesson Status\" button<br><br>* Change lesson status to draft | * User sees the lesson status is updated from published -> draft<br>* User sees the lesson status is updated from cancelled -> draft<br><br>* User sees completed lesson with no change | - |
| 2 | Login BO and view the lesson | * User sees the lesson's status is Draft on BO<br>* User sees completed lesson with no change on BO | - |

---

### TC-1470: User uses bulk update published lesson status

**Preconditions:**

* User has created some daily/weekly/custom by end date/lesson count lessons with a teacher and student

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | * On the lesson list, select a draft, completed and cancelled lesson<br>* Click on \"Bulk Update Lesson Status\" button<br><br>* Change lesson status to published | * User sees the lesson status is updated from draft -> published<br>* User sees the lesson status is updated from completed -> published<br>* User sees cancelled lesson with no change | - |
| 2 | Login BO and view the lesson | * User sees the lesson's status is published on BO<br>* User sees cancelled lesson with no change on BO | - |
| 3 | Parent login Mobile | Parent sees the lesson and lesson report with correct information | - |

---

### TC-1471: User uses bulk update completed lesson status

**Preconditions:**

* User has created some daily/weekly/custom by end date/lesson count lessons with a teacher and student

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | * On the lesson list, select a draft, published and cancelled lesson in the past<br>* Click on \"Bulk Update Lesson Status\" button<br>* Change lesson status to completed | * User sees the lesson status is updated from published -> completed<br>* User sees draft and cancelled lesson with no change | - |
| 2 | Login BO and view the lesson | * User sees the lesson's status is completed on BO<br>* User sees draft and cancelled lesson with no change on BO | - |
| 3 | Parent login Mobile | Parent sees the lesson and lesson report with correct information | - |

---

### TC-1475: User uses bulk update cancelled lesson status

**Preconditions:**

* User has created some daily/weekly/custom by end date/lesson count lessons with a teacher and student

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | * On the lesson list, select a draft, published and completed lesson<br>* Click on \"Bulk Update Lesson Status\" button<br><br>* Change lesson status to cancelled | * User sees the lesson status is updated from draft and published -> cancelled<br>* User sees completed lesson with no change | - |
| 2 | Login BO and view the lesson | * User sees the lesson's status is Cancelled on BO<br>* User sees completed lesson with no change on BO | - |
| 3 | Parent login Mobile | * Parent sees the lesson with Cancelled tag | - |

---

### TC-1476: User cannot use bulk update lesson status

**Preconditions:**

* User has created some daily/weekly/custom by end date/lesson count lessons with a teacher and student

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | * On the lesson list, select a draft, published and completed lesson<br>* Click on \"Bulk Update Lesson Status\" button<br><br>* Change lesson status to cancelled | * User sees an error message \"Missing Cancellation Reason\" | - |
| 2 | * On the lesson list, select a published lesson in the future<br>* Click on \"Bulk Update Lesson Status\" button<br><br>* Change lesson status to completed | * User sees an error message | - |

---
