# Import Lesson Test Cases

---

## TC-1031: User imports the one-time lesson

**Preconditions:**

* User has setup Academic Year, Location, Location Course, Class on Manabie Master
* User has prepared the CSV valid with
* 1. Start date = end date = Closed Date
* 2. Teaching method = Individual and Group
* 3. Teacher medium = Offline and Online
* 4. Lesson code

**Steps:**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | * Go to Manabie Lesson -> Lesson tab<br>* Click on \"Import\" button<br><br><br>* Select Lesson Schedule and Add new record<br><br><br>* Select Academic Year Name, Account Name, Class Name, Location Course Name, Program Master Name<br><br><br>* Upload the CSV file and click on \"Next\" button<br><br><br>* Map Start Date = Start Date Time and End Date = End Date Time<br><br><br>* Click on \"Next\" and \"Start Import\" buttton | * User sees the lesson with lesson info that matches the CSV file on the lesson list<br>* User sees the lesson report is auto-created for these lessons |  |
| 2 | Login BO and view this lesson | * User sees the lesson with lesson info that matches the CSV file on the lesson list on BO<br>* User sees the lesson report for these lessons on BO |  |

---

## TC-1034: User import a lesson with a teacher

**Preconditions:**

* User has setup the master data

**Steps:**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Import the CSV valid with <br>+ Start date = end date <br>+ Teaching method = Individual and Group<br>+ The teacher's usename | User sees the teacher is assigned to a lesson |  |
| 2 | Import the CSV valid with <br>+ Start date < end date<br>+ Teaching method = Individual and Group<br>+ Some teacher's usename with multiple roles (HQ Staff, CM, CS, BS, Teacher and PT Teacher) | User sees some teachers are assigned to all lessons in the chain |  |
| 3 | Import the CSV valid with <br>+ Start date = end date <br>+ Teaching method = Individual and Group<br>+ Teacher with eligible subject and teacher without eligible subject | User sees the all teachers are assigned to a lesson |  |
| 4 | Import the CSV valid with <br>+ start date < end date<br>+ Teaching method = Individual and Group<br>+ Teacher, student and parent | User only sees the teacher is assigned to all lessons in the chain |  |
| 5 | Import the CSV valid with <br>+ start date < end date<br>+ Teaching method = Individual and Group<br>+ Empty teacher | User does not see a teacher in all lessons in the chain |  |
| 6 | Login BO and view the teacher in imported lessons | User sees the teacher in imported lessons |  |

---

## TC-1036: User import multiple lessons with valid and invalid data

**Preconditions:**

* User has setup the master data

**Steps:**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | User imports multiple lessons with valid and invalid data | * User sees lesson with valid data is imported successfuly<br>* User sees an error message for invalid data |  |

---

## TC-1033: User imports the group lesson with class that has assigned to the student

**Preconditions:**

* User has setup Academic Year, Location, Location Course, Class on Manabie Master
* User has assigned a active class and a future to the student
* User has prepared the CSV valid with the active class and future class

**Steps:**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | * Go to Manabie Lesson -> Lesson tab<br>* Click on \"Import\" button<br><br><br>* Select Lesson Schedule and Add new record<br><br><br>* Select Academic Year Name, Account Name, Class Name, Location Course Name, Program Master Name<br><br><br>* Upload the CSV file and click on \"Next\" button<br><br><br>* Map Start Date = Start Date Time and End Date = End Date Time<br><br><br>* Click on \"Next\" and \"Start Import\" buttton | * User sees the student auto-assign to the lesson correctly within the active class_member duration and the future class_member duration in detailed lesson page<br>* User sees the lesson report detail is created for the student | EX:<br>\\- Student A have<br>+ Class A (active class) from 1\/5\/2024 to 30\/9\/2024<br>+ Class B (future class) from 1\/10\/2024 to 31\/3\/2025<br>\\- Import the CSV file with Lesson L1 \\- Class A and Lesson L2 \\- Class B from 1\/5\/2024 to 31\/3\/2025<br>-> Student A auto-assign to L1 from 1\/5\/2024 to 30\/9\/2024<br>-> Student A auto-assign to L2 from 1\/10\/2024 to 31\/3\/2025 |
| 2 | Check lesson allocation detail | * User sees the student session is auto-create = assigned lesson<br>* User sees the lesson allocation of the student is updated (Lesson Allocated, Student Schedule, Student Session, Report History) |  |
| 3 | Login BO and view this lesson | * User sees the student in the lesson in detailed lesson page on BO<br>* User sees the lesson report detail is created for the student on BO |  |

---

## TC-1035: User import lessons unsuccessfully

**Preconditions:**

* User has setup the master data

**Steps:**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | User imports lesson with invalid location | User sees import lesson is failed |  |
| 2 | User imports lesson with start date > end date | User sees import lesson is failed |  |
| 3 | User imports lesson with start time => end date | User sees import lesson is failed |  |
| 4 | User imports lesson with teaching method != \"Individual\" or \"Group\" | User sees import lesson is failed |  |
| 5 | User imports lesson with teaching medium != \"Online\" or \"Offline\" | User sees import lesson is failed |  |
| 6 | User imports group lesson missing location course | User sees import lesson is failed |  |
| 7 | User imports group lesson with location course != location lesson | User sees import lesson is failed |  |
| 8 | User imports group lesson with class does not belong to location course | User sees import lesson is failed |  |
| 9 | User imports with lesson count > 500 lessons | User sees import lesson is failed |  |
| 10 | User imports with lesson count < 2 lessons |  |  |
| 11 | ![image.png](https:\/\/d2cxucsjd6xvsd.cloudfront.net\/public\/team\/b5f684e60ab1a64567fb280d07faed2c4132e041\/attachment\/045d1e1ffbe38a09b925aaaf7e795c50a92c9ee9\/image.png) |  |  |

---

## TC-7169: User imports a weekly individual lesson by selecting the end date with skip closed date

**Description:** Ensure that the system prevents lesson creation when required fields are missing for an individual lesson.

**Preconditions:**

* User has setup Academic Year, Location, Location Course, Class, Closed Date on Manabie Master

**Steps:**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
|  |  |  |  |

---

## TC-7170: User imports a weekly group lesson by selecting the end date without skip closed date

**Description:** Verify that an existing activity lesson can be edited and updated details are saved correctly.

**Preconditions:**

* User has setup Academic Year, Location, Location Course, Class, Closed Date on Manabie Master

**Steps:**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
|  |  |  |  |

---

## TC-7171: User imports a weekly individual lesson by inputting lesson count without skip closed date

**Steps:**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
|  |  |  |  |

---

## TC-7172: User imports a weekly group lesson by inputting lesson count with skip closed date

**Steps:**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
|  |  |  |  |

---

## TC-7173: User imports a daily individual lesson by selecting the end date without skip closed date

**Description:** Ensure that the system prevents lesson creation when required fields are missing for an individual lesson.

**Preconditions:**

* User has setup Academic Year, Location, Location Course, Class, Closed Date on Manabie Master

**Steps:**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | * Go to the Manabie Lesson -> Lesson tab<br><br><br>* Click New button<br><br><br>* Fill in the Lesson details, lesson code and select teaching method = Individual<br><br><br>* Select lesson date = closed date<br><br><br>* Check the Recurring Setting and End Date field<br><br><br>* Select the end date in the recurring setting so that the duration belongs to AY<br><br><br>* Click \"Save\" | * User sees a recurring individual lesson + lesson report are created for all lessons with \"Draft\" status<br><br><br>* User does not see a lesson that has lesson date = closed date<br><br><br>* User sees lesson code +1 for following lessons<br><br><br>* User sees default lesson type = \u901a\u5e38\u7279\u8a13 for all lessons | * Lesson 1 with lesson code = 1<br><br><br>* Lesson 2 with lesson code = 2<br><br> .....<br><br>* Lesson N with lesson code = previous lesson + 1 |
| 2 | Login BO and view this lesson | * User sees a individual lesson chain is created on the selected weekday within the repeat duration with \"Draft\" status on the Lesson list on BO<br><br><br>* User sees the lesson code, lesson type is read-only on BO<br><br><br>* User sees the individual lesson report is created with \"Draft\" status for all lessons in the chain on Lesson detail -> Report tab and Lesson Report list on BO |  |

---

## TC-7174: User imports a daily group lesson by selecting the end date with skip closed date

**Description:** Verify that an existing activity lesson can be edited and updated details are saved correctly.

**Preconditions:**

* User has setup Academic Year, Location, Location Course, Class, Closed Date on Manabie Master

**Steps:**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | * Go to the Manabie Lesson -> Lesson tab<br><br><br>* Click New button<br><br><br>* Fill in the Lesson details, lesson code and select teaching method = Group<br><br><br>* Check the Recurring Setting and End Date field<br><br><br>* Select the end date in the recurring setting so that the lesson in the middle of the chain is closed date and the duration belongs to AY<br><br><br>* Click \"Save\" | * User sees a recurring group lesson + lesson report are created for all lessons with \"Draft\" status<br><br><br>* User does not see a lesson that has lesson date = closed date<br><br><br>* User sees lesson code +1 for following lessons<br><br><br>* User sees default lesson type = \u901a\u5e38\u7279\u8a13 for all lessons | * Lesson 1 with lesson code = 1<br><br><br>* Lesson 2 with lesson code = 2<br><br> .....<br><br>* Lesson N with lesson code = previous lesson + 1 |
| 2 | Login BO and view this lesson | * User sees a group lesson chain is created on the selected weekday within the repeat duration with \"Draft\" status on the Lesson list on BO<br><br><br>* User sees the lesson code, lesson type is read-only on BO<br><br><br>* User sees the group lesson report is created with \"Draft\" status for all lessons in the chain on Lesson detail -> Report tab and Lesson Report list on BO |  |

---

## TC-7175: User imports a daily individual lesson by inputting lesson count with skip closed date

**Steps:**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Create with 5 lessons |  |  |
| 2 | Create with 50 lessons |  |  |
| 3 | Create with 500 lessons |  |  |

---

## TC-7176: User imports a daily group lesson by inputting lesson count without skip closed date

**Steps:**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Create with 5 lessons |  |  |
| 2 | Create with 50 lessons |  |  |
| 3 | Create with 500 lessons |  |  |

---

## TC-7177: User imports a custom individual lesson by selecting the end date without skip closed date

**Description:** Ensure that the system prevents lesson creation when required fields are missing for an individual lesson.

**Preconditions:**

* User has setup Academic Year, Location, Location Course, Class, Closed Date on Manabie Master

**Steps:**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Check 1 day |  |  |
| 2 | Check 3 days |  |  |
| 3 | Check full days |  |  |

---

## TC-7178: User imports a custom group lesson by selecting the end date with skip closed date

**Description:** Ensure that the system prevents lesson creation when required fields are missing for an individual lesson.

**Preconditions:**

* User has setup Academic Year, Location, Location Course, Class, Closed Date on Manabie Master

**Steps:**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Check 1 day |  |  |
| 2 | Check 3 days |  |  |
| 3 | Check full days |  |  |

---

## TC-7179: User imports a custom individual lesson by inputting the lesson count with skip closed date

**Description:** Ensure that the system prevents lesson creation when required fields are missing for an individual lesson.

**Preconditions:**

* User has setup Academic Year, Location, Location Course, Class, Closed Date on Manabie Master

**Steps:**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | * Check 1 day<br>* Input 5 lessons |  |  |
| 2 | * Check 3 days<br><br><br>* Input 50 lessons |  |  |
| 3 | * Check full days<br><br><br>* Input 500 lessons |  |  |

---

## TC-7180: User imports a custom group lesson by inputting the lesson count without skip closed date

**Description:** Ensure that the system prevents lesson creation when required fields are missing for an individual lesson.

**Preconditions:**

* User has setup Academic Year, Location, Location Course, Class, Closed Date on Manabie Master

**Steps:**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | * Check 1 day<br>* Input 5 lessons |  |  |
| 2 | * Check 3 days<br><br><br>* Input 50 lessons |  |  |
| 3 | * Check full days<br><br><br>* Input 500 lessons |  |  |

---

## TC-8995: User imports a custom lesson by inputting lesson count so that lesson count < selected days

**Steps:**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
|  |  |  |  |

---

## TC-9014: User imports a weekly lesson with the start&end date = closed date

**Steps:**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
|  |  |  |  |

---

## TC-9015: User imports a daily lesson with the start&end date = closed date

**Steps:**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
|  |  |  |  |

---

## TC-9016: Import weekly lesson with start date = end date

**Steps:**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
|  |  |  |  |

---

## TC-9017: Import daily lesson with start date = end date and lesson count

**Steps:**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
|  |  |  |  |

---

## TC-9018: Import with lesson date at beginning and end of day

**Steps:**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
|  |  |  |  |

---

## TC-9019: Import lesson with missing closed date

**Steps:**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
|  |  |  |  |

---

## TC-9020: Import lesson with start date > end date and lesson count

**Steps:**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
|  |  |  |  |

---

## TC-9023: Import lesson with the is_recurring field

**Steps:**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Missing is_recurring and start date = end date | Create an one-time lesson |  |
| 2 | Is_recurring = False and start date = end date | Create an one-time lesson |  |
| 3 | Is_recurring = True and start date = end date | Create a recurring lesson |  |
| 4 | Missing is_recurring and start date < end date | Create a recurring lesson |  |
| 5 | Is_recurring = False and start date < end date | Create a recurring lesson |  |
| 6 | Missing is_recurring and recurrence type = Daily\/Weekly\/Custom with end date | Create a daily\/weekly\/custom lesson with end date |  |
| 7 | Is_recurring = False and recurrence type = Daily\/Weekly\/Custom with end date | Create a daily\/weekly\/custom lesson with end date |  |
| 8 | Is_recurring = False and recurrence type = Daily\/Weekly\/Custom with lesson count | Create a daily\/weekly\/custom lesson with lesson count |  |
| 9 | Missing is_recurring and recurrence type and closed date | Create a weekly lesson with closed date |  |
| 10 | Is_recurring = False and missing recurrence type and closed date | Create a weekly lesson with closed date |  |
| 11 | Is_recurring = True and missing recurrence type and closed date | Create a weekly lesson with closed date |  |
| 12 | Missing is_recurring and recurrence days with custom lesson | Show an error message |  |
| 13 | Is_recurring = False and missing recurrence days with custom lesson | Show an error message |  |
| 14 | Is_recurring = True and missing recurrence days with custom lesson | Show an error message |  |

---

## TC-14896: Import lesson with no access to the location

**Preconditions:**

* CM's affiliation location: Location 1

**Steps:**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Import lesson with Location 2 | Show an error message |  |
