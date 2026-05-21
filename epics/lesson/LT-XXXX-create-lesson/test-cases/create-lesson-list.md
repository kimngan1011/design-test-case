# Create Lesson Test Cases

---

## TC-5644: User view the create lesson popup

**Preconditions:**

* User has created master data (Location, AY, Course, Class, Closed Date, Academic Calendar)
* User has setup Academic Calendar with Location and Closed Date
* User has gone to Lesson tab
* User has open creating lesson form


**Steps:**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Verify UI | ![image.png](https://d2cxucsjd6xvsd.cloudfront.net/public/team/b5f684e60ab1a64567fb280d07faed2c4132e041/attachment/853ca63ba6258026338f35290fde1b427d44f107/image.png)![image.png](https://d2cxucsjd6xvsd.cloudfront.net/public/team/b5f684e60ab1a64567fb280d07faed2c4132e041/attachment/b91f2c57d12965371e3f3de431a5edd237f88580/image.png)<br>Can see fields:<br><br>* date<br>* lesson name<br>* date off the week (will automatically shown after choose date)<br>* duration (minutes)<br>* start time<br>* end time<br>* teaching medium<br>* teaching method<br>* location<br>* academic year<br>* course<br>* class<br>* classrooms<br>* lesson capacity<br>* lesson code<br>* lesson type<br>* check box recur this lesson<br>* Recurrence Frequency<br>* Course Schedule<br>* Recurrence Type: Daily, Weekly, Custom<br>* End Recurrence: On, After, end date<br>* Checkbox skip closed date<br>* Cancel button<br>* Save button |  |
| 2 | Verify pre-filter data (editable) | * Teaching medium: Offline<br><br><br>* Teaching Method: Individual<br>* AY: Current AY<br>* Course and Classroom: pre-filtered by Location<br>* Class: pre-filtered by Course |  |
| 3 | Verify missing required field | ![image.png](https://d2cxucsjd6xvsd.cloudfront.net/public/team/b5f684e60ab1a64567fb280d07faed2c4132e041/attachment/3b4d4b8a886df9213d55c63c6f1c236daa4bfffb/image.png)![image.png](https://d2cxucsjd6xvsd.cloudfront.net/public/team/b5f684e60ab1a64567fb280d07faed2c4132e041/attachment/45f22be4c584125b0fcfc2dcb0402b004b914ec6/image.png)<br>![image.png](https://d2cxucsjd6xvsd.cloudfront.net/public/team/b5f684e60ab1a64567fb280d07faed2c4132e041/attachment/3c9282fdba31c0a4de1434ab62ee82ae478eb781/image.png) |  |
| 4 | Verify lesson date > end date | ![image.png](https://d2cxucsjd6xvsd.cloudfront.net/public/team/b5f684e60ab1a64567fb280d07faed2c4132e041/attachment/f4a0985d880201b9cf8766252f482c9d6ee5bac9/image.png) |  |
| 5 | Verify start time > end time | ![image.png](https://d2cxucsjd6xvsd.cloudfront.net/public/team/b5f684e60ab1a64567fb280d07faed2c4132e041/attachment/80ddc8e7eef4aed2f11144ef95d075692bec4a3c/image.png) |  |


---

## TC-1022: User creates an one-time individual lesson with closed date

**Preconditions:**

* User has created master data (Location, AY, Course, Class, Closed Date, Academic Calendar)
* User has setup Academic Calendar with Location and Closed Date
* User has gone to the Manabie Lesson -> Lesson tab -> New button


**Steps:**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Fill in the Lesson details, lesson code and select teaching method = Individual |  |  |
| 2 | Create a one-time lesson with lesson date = closed date | * User sees an one-time individual lesson and lesson report is created with Draft status<br><br><br>* User sees lesson info show matches the selected value<br><br><br>* User sees default lesson type = 通常特訓<br><br><br>* User still sees lesson with closed date is created |  |
| 3 | Login BO and view this lesson | * User sees lesson and lesson report on BO<br><br><br>* User sees the lesson code, lesson type is read-only on BO<br><br><br>* User sees the individual lesson report is created with "Draft" status on Lesson detail -> Report tab and Lesson Report list on BO |  |


---

## TC-1023: User creates an one-time group lesson

**Preconditions:**

* User has created master data (Location, AY, Course, Class, Closed Date, Academic Calendar)
* User has setup Academic Calendar with Location and Closed Date
* User has gone to the Manabie Lesson -> Lesson tab -> New button


**Steps:**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Fill in the Lesson details, lesson code and select teaching method = Group |  |  |
| 2 | Fill in the Course and Class |  |  |
| 3 | Click New button | * User sees an one-time group lesson and lesson report is created with Draft status<br>* User sees lesson info show matches the selected value<br>* User sees default lesson type = 通常特訓<br>* User still sees lesson with closed date is created |  |
| 4 | Login BO and view this lesson | * User sees lesson and lesson report on BO<br>* User sees the lesson code, lesson type is read-only on BO<br>* User sees the group lesson report is created with "Draft" status on Lesson detail -> Report tab and Lesson Report list on BO |  |


---

## TC-1013: User creates a weekly individual lesson by selecting the end date with skip closed date

**Description:** Ensure that the system prevents lesson creation when required fields are missing for an individual lesson.

**Preconditions:**

* User has created master data (Location, AY, Course, Class, Closed Date, Academic Calendar)
* User has setup Academic Calendar with Location and Closed Date
* User has gone to the Manabie Lesson -> Lesson tab -> New button


**Steps:**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Input data with:<br><br>* Lesson date: Current date<br>* Lesson time<br>* Lesson name<br>* Location: with AC and Closed Date)<br>* Classrooms<br>* Lesson Capacity<br>* Lesson Code<br>* Check the Recurrence Frequency<br>* Recurrence Type: Weekly<br>* End Recurrence: On<br>* End Date: 31/3/2026<br>* Check the Skip Closed Date<br><br><br>    <br> | ![image.png](https://d2cxucsjd6xvsd.cloudfront.net/public/team/b5f684e60ab1a64567fb280d07faed2c4132e041/attachment/54999a83e9648737372d6bac5a6fcfd1a030db16/image.png) |  |
| 2 | Click on the Save button | * User sees that the weekly individual lesson is created between the lesson start date and end date. | ![image.png](https://d2cxucsjd6xvsd.cloudfront.net/public/team/b5f684e60ab1a64567fb280d07faed2c4132e041/attachment/e9091739eff95b74eb87fd052286a0fb53d63862/image.png) |
| 3 | Check all lessons in the chain | * User sees two consecutive lessons that are 7 days apart.<br>* User sees that the other data is generated for all lessons in the chain.<br><br> | ![image.png](https://d2cxucsjd6xvsd.cloudfront.net/public/team/b5f684e60ab1a64567fb280d07faed2c4132e041/attachment/e9091739eff95b74eb87fd052286a0fb53d63862/image.png) |
| 4 | Check lesson code | * User sees the lesson code gradually increase for each subsequent lesson in the chain. | ![image.png](https://d2cxucsjd6xvsd.cloudfront.net/public/team/b5f684e60ab1a64567fb280d07faed2c4132e041/attachment/e9091739eff95b74eb87fd052286a0fb53d63862/image.png) |
| 5 | Check lesson type | * User sees the default lesson type = 通常特訓 for all lessons. | ![image.png](https://d2cxucsjd6xvsd.cloudfront.net/public/team/b5f684e60ab1a64567fb280d07faed2c4132e041/attachment/672ecc241710950479dadf38add5d25928243319/image.png) |
| 6 | Check closed date | * User does not see any lesson date that matches the closed date in the chain. | ![image.png](https://d2cxucsjd6xvsd.cloudfront.net/public/team/b5f684e60ab1a64567fb280d07faed2c4132e041/attachment/672ecc241710950479dadf38add5d25928243319/image.png) |
| 7 | Check lesson report | * User sees individual lesson report is auto-created for all lessons in the chain | ![image.png](https://d2cxucsjd6xvsd.cloudfront.net/public/team/b5f684e60ab1a64567fb280d07faed2c4132e041/attachment/32f22f769767397d4371943d051939d253e688fe/image.png) |
| 8 | Login BO and view these lessons | * User sees these lessons on BO<br>* User sees the lesson code, lesson type is read-only on BO<br>* User sees the lesson report on Lesson detail -> Report tab and Lesson Report list on BO |  |


---

## TC-1014: User creates a weekly group lesson by selecting the end date without skip closed date

**Description:** Verify that an existing activity lesson can be edited and updated details are saved correctly.

**Preconditions:**

* User has created master data (Location, AY, Course, Class, Closed Date, Academic Calendar)
* User has setup Academic Calendar with Location and Closed Date
* User has gone to the Manabie Lesson -> Lesson tab -> New button


**Steps:**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Input data with:<br><br>* Lesson date: Current date<br>* Lesson time<br>* Lesson name<br>* Location: with AC and Closed Date)<br>* Teaching Method: Group<br>* Course <br>* Classrooms<br>* Lesson Capacity<br>* Lesson Code<br>* Lesson type: 通常特訓（時間変更）<br>* Check the Recurrence Frequency<br>* Recurrence Type: Weekly<br>* End Recurrence: On<br>* End Date: 31/3/2026<br>* Uncheck the Skip Closed Date | ![image.png](https://d2cxucsjd6xvsd.cloudfront.net/public/team/b5f684e60ab1a64567fb280d07faed2c4132e041/attachment/8b7b5f3c79ffd692b0e7de892e9187aef1b531bf/image.png) |  |
| 2 | Click on the Save button | * User sees that the weekly group lesson is created between the lesson start date and end date. | ![image.png](https://d2cxucsjd6xvsd.cloudfront.net/public/team/b5f684e60ab1a64567fb280d07faed2c4132e041/attachment/e9091739eff95b74eb87fd052286a0fb53d63862/image.png) |
| 3 | Check all lessons in the chain | * User sees two consecutive lessons that are 7 days apart.<br>* User sees that the other data is generated for all lessons in the chain.<br><br> | ![image.png](https://d2cxucsjd6xvsd.cloudfront.net/public/team/b5f684e60ab1a64567fb280d07faed2c4132e041/attachment/e9091739eff95b74eb87fd052286a0fb53d63862/image.png) |
| 4 | Check lesson code | * User sees the lesson code gradually increase for each subsequent lesson in the chain. | ![image.png](https://d2cxucsjd6xvsd.cloudfront.net/public/team/b5f684e60ab1a64567fb280d07faed2c4132e041/attachment/e9091739eff95b74eb87fd052286a0fb53d63862/image.png) |
| 5 | Check lesson type | * User sees the default lesson type = 通常特訓 for all lessons. |  |
| 6 | Check closed date | * User still sees lesson date that matches the closed date in the chain. |  |
| 7 | Check lesson report | * User sees group lesson report is auto-created for all lessons in the chain |  |
| 8 | Login BO and view these lessons | * User sees these lessons on BO<br>* User sees the lesson code, lesson type is read-only on BO<br>* User sees the lesson report on Lesson detail -> Report tab and Lesson Report list on BO |  |


---

## TC-6931: User creates a weekly individual lesson by inputting lesson count without skip closed date

**Preconditions:**

* User has created master data (Location, AY, Course, Class, Closed Date, Academic Calendar)
* User has setup Academic Calendar with Location and Closed Date
* User has gone to the Manabie Lesson -> Lesson tab -> New button


**Steps:**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Input data with:<br><br>* Lesson date: Current date<br>* Lesson time<br>* Lesson name<br>* Location: with AC and Closed Date)<br>* Classrooms<br>* Lesson Capacity<br>* Lesson Code<br>* Check the Recurrence Frequency<br>* Recurrence Type: Weekly<br>* End Recurrence: After<br>* Number of Lessons: 5<br>* Uncheck the Skip Closed Date | ![image.png](https://d2cxucsjd6xvsd.cloudfront.net/public/team/b5f684e60ab1a64567fb280d07faed2c4132e041/attachment/5fcc681a8b150c0be501db9e692ff1399c73a362/image.png) |  |
| 2 | Click on the Save button | * User sees that the weekly individual lesson is created = inputted number of lessons<br><br><br><br> |  |
| 3 | Check all lessons in the chain | * User sees two consecutive lessons that are 7 days apart.<br>* User sees that the other data is generated for all lessons in the chain.<br><br> | ![image.png](https://d2cxucsjd6xvsd.cloudfront.net/public/team/b5f684e60ab1a64567fb280d07faed2c4132e041/attachment/e9091739eff95b74eb87fd052286a0fb53d63862/image.png) |
| 4 | Check lesson code | * User sees the lesson code gradually increase for each subsequent lesson in the chain. | ![image.png](https://d2cxucsjd6xvsd.cloudfront.net/public/team/b5f684e60ab1a64567fb280d07faed2c4132e041/attachment/e9091739eff95b74eb87fd052286a0fb53d63862/image.png) |
| 5 | Check lesson type | * User sees the default lesson type = 通常特訓 for all lessons. | ![image.png](https://d2cxucsjd6xvsd.cloudfront.net/public/team/b5f684e60ab1a64567fb280d07faed2c4132e041/attachment/672ecc241710950479dadf38add5d25928243319/image.png) |
| 6 | Check closed date | * User still sees lesson date that matches the closed date in the chain. |  |
| 7 | Check lesson report | * User sees individual lesson report is auto-created for all lessons in the chain | ![image.png](https://d2cxucsjd6xvsd.cloudfront.net/public/team/b5f684e60ab1a64567fb280d07faed2c4132e041/attachment/32f22f769767397d4371943d051939d253e688fe/image.png) |
| 8 | Login BO and view these lessons | * User sees these lessons on BO<br>* User sees the lesson code, lesson type is read-only on BO<br>* User sees the lesson report on Lesson detail -> Report tab and Lesson Report list on BO |  |


---

## TC-9672: User creates a weekly group lesson by inputting lesson count with skip closed date

**Preconditions:**

* User has created master data (Location, AY, Course, Class, Closed Date, Academic Calendar)
* User has setup Academic Calendar with Location and Closed Date
* User has gone to the Manabie Lesson -> Lesson tab -> New button


**Steps:**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Input data with:<br><br>* Lesson date: Current date<br>* Lesson time<br>* Lesson name<br>* Location: with AC and Closed Date)<br>* Teaching Method: Group<br>* Course<br>* Class<br>* Classrooms<br>* Lesson Capacity<br>* Lesson Code<br>* Check the Recurrence Frequency<br>* Recurrence Type: Weekly<br>* End Recurrence: After<br>* Number of Lessons: 50<br>* Check the Skip Closed Date | ![image.png](https://d2cxucsjd6xvsd.cloudfront.net/public/team/b5f684e60ab1a64567fb280d07faed2c4132e041/attachment/5fcc681a8b150c0be501db9e692ff1399c73a362/image.png) |  |
| 2 | Click on the Save button | * User sees that the weekly individual lesson is created = inputted number of lessons<br><br><br><br> |  |
| 3 | Check all lessons in the chain | * User sees two consecutive lessons that are 7 days apart.<br>* User sees that the other data is generated for all lessons in the chain.<br><br> | ![image.png](https://d2cxucsjd6xvsd.cloudfront.net/public/team/b5f684e60ab1a64567fb280d07faed2c4132e041/attachment/e9091739eff95b74eb87fd052286a0fb53d63862/image.png) |
| 4 | Check lesson code | * User sees the lesson code gradually increase for each subsequent lesson in the chain. | ![image.png](https://d2cxucsjd6xvsd.cloudfront.net/public/team/b5f684e60ab1a64567fb280d07faed2c4132e041/attachment/e9091739eff95b74eb87fd052286a0fb53d63862/image.png) |
| 5 | Check lesson type | * User sees the default lesson type = 通常特訓 for all lessons. | ![image.png](https://d2cxucsjd6xvsd.cloudfront.net/public/team/b5f684e60ab1a64567fb280d07faed2c4132e041/attachment/672ecc241710950479dadf38add5d25928243319/image.png) |
| 6 | Check skip closed date | * User does not see any lesson date that matches the closed date in the chain. | ![image.png](https://d2cxucsjd6xvsd.cloudfront.net/public/team/b5f684e60ab1a64567fb280d07faed2c4132e041/attachment/672ecc241710950479dadf38add5d25928243319/image.png) |
| 7 | Check lesson report | * User sees individual lesson report is auto-created for all lessons in the chain | ![image.png](https://d2cxucsjd6xvsd.cloudfront.net/public/team/b5f684e60ab1a64567fb280d07faed2c4132e041/attachment/32f22f769767397d4371943d051939d253e688fe/image.png) |
| 8 | Login BO and view these lessons | * User sees these lessons on BO<br>* User sees the lesson code, lesson type is read-only on BO<br>* User sees the lesson report on Lesson detail -> Report tab and Lesson Report list on BO |  |


---

## TC-9673: User creates a daily individual lesson by selecting the end date without skip closed date

**Description:** Verify that an existing activity lesson can be edited and updated details are saved correctly.

**Preconditions:**

* User has created master data (Location, AY, Course, Class, Closed Date, Academic Calendar)
* User has setup Academic Calendar with Location and Closed Date
* User has gone to the Manabie Lesson -> Lesson tab -> New button


**Steps:**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Input data with:<br><br>* Lesson date: Current date<br>* Lesson time<br>* Lesson name<br>* Location: with AC and Closed Date)<br>* Classrooms<br>* Lesson Capacity<br>* Lesson Code<br>* Lesson type: 通常特訓（時間変更）<br>* Check the Recurrence Frequency<br>* Recurrence Type: Daily<br>* End Recurrence: On<br>* End Date: 31/3/2026<br>* Uncheck the Skip Closed Date | ![image.png](https://d2cxucsjd6xvsd.cloudfront.net/public/team/b5f684e60ab1a64567fb280d07faed2c4132e041/attachment/4722dd56df45331aee61ab418ad3188ce5ad4c17/image.png) |  |
| 2 | Click on the Save button | * User sees that the daily individual lesson is created between the lesson start date and end date. | ![image.png](https://d2cxucsjd6xvsd.cloudfront.net/public/team/b5f684e60ab1a64567fb280d07faed2c4132e041/attachment/e9091739eff95b74eb87fd052286a0fb53d63862/image.png) |
| 3 | Check all lessons in the chain | * User sees two consecutive lessons that are 1 days apart.<br>* User sees that the other data is generated for all lessons in the chain. | ![image.png](https://d2cxucsjd6xvsd.cloudfront.net/public/team/b5f684e60ab1a64567fb280d07faed2c4132e041/attachment/7bba3a73cdcc3909c5b75fe3f87a879bcbced123/image.png) |
| 4 | Check lesson code | * User sees the lesson code gradually increase for each subsequent lesson in the chain. | ![image.png](https://d2cxucsjd6xvsd.cloudfront.net/public/team/b5f684e60ab1a64567fb280d07faed2c4132e041/attachment/e9091739eff95b74eb87fd052286a0fb53d63862/image.png) |
| 5 | Check lesson type | * User sees the default lesson type = 通常特訓 for all lessons. |  |
| 6 | Check closed date | * User still sees lesson date that matches the closed date in the chain. |  |
| 7 | Check lesson report | * User sees individual lesson report is auto-created for all lessons in the chain | ![image.png](https://d2cxucsjd6xvsd.cloudfront.net/public/team/b5f684e60ab1a64567fb280d07faed2c4132e041/attachment/32f22f769767397d4371943d051939d253e688fe/image.png) |
| 8 | Login BO and view these lessons | * User sees these lessons on BO<br>* User sees the lesson code, lesson type is read-only on BO<br>* User sees the lesson report on Lesson detail -> Report tab and Lesson Report list on BO |  |


---

## TC-9674: User creates a daily group lesson by selecting the end date with skip closed date

**Description:** Verify that an existing activity lesson can be edited and updated details are saved correctly.

**Preconditions:**

* User has created master data (Location, AY, Course, Class, Closed Date, Academic Calendar)
* User has setup Academic Calendar with Location and Closed Date
* User has gone to the Manabie Lesson -> Lesson tab -> New button


**Steps:**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Input data with:<br><br>* Lesson date: Current date<br>* Lesson time<br>* Lesson name<br>* Location: with AC and Closed Date)<br>* Teaching Method: Group<br>* Course<br>* Class<br>* Classrooms<br>* Lesson Capacity<br>* Lesson Code<br>* Lesson type: 通常特訓（時間変更）<br>* Check the Recurrence Frequency<br>* Recurrence Type: Daily<br>* End Recurrence: On<br>* End Date: 31/3/2026<br>* Check the Skip Closed Date |  |  |
| 2 | Click on the Save button | * User sees that the daily group lesson is created between the lesson start date and end date. | ![image.png](https://d2cxucsjd6xvsd.cloudfront.net/public/team/b5f684e60ab1a64567fb280d07faed2c4132e041/attachment/e9091739eff95b74eb87fd052286a0fb53d63862/image.png) |
| 3 | Check all lessons in the chain | * User sees two consecutive lessons that are 1 days apart.<br>* User sees that the other data is generated for all lessons in the chain. |  |
| 4 | Check lesson code | * User sees the lesson code gradually increase for each subsequent lesson in the chain. | ![image.png](https://d2cxucsjd6xvsd.cloudfront.net/public/team/b5f684e60ab1a64567fb280d07faed2c4132e041/attachment/e9091739eff95b74eb87fd052286a0fb53d63862/image.png) |
| 5 | Check lesson type | * User sees the default lesson type = 通常特訓（時間変更） for all lessons. |  |
| 6 | Check closed date | * User still sees lesson date that matches the closed date in the chain. |  |
| 7 | Check lesson report | * User sees group lesson report is auto-created for all lessons in the chain |  |
| 8 | Login BO and view these lessons | * User sees these lessons on BO<br>* User sees the lesson code, lesson type is read-only on BO<br>* User sees the lesson report on Lesson detail -> Report tab and Lesson Report list on BO |  |


---

## TC-9675: User creates a daily individual lesson by inputting lesson count with skip closed date

**Preconditions:**

* User has created master data (Location, AY, Course, Class, Closed Date, Academic Calendar)
* User has setup Academic Calendar with Location and Closed Date
* User has gone to the Manabie Lesson -> Lesson tab -> New button


**Steps:**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Input data with:<br><br>* Lesson date: Current date<br>* Lesson time<br>* Lesson name<br>* Location: with AC and Closed Date)<br>* Classrooms<br>* Lesson Capacity<br>* Lesson Code<br>* Check the Recurrence Frequency<br>* Recurrence Type: Daily<br>* End Recurrence: After<br>* Number of Lessons: 10<br>* Check the Skip Closed Date | ![image.png](https://d2cxucsjd6xvsd.cloudfront.net/public/team/b5f684e60ab1a64567fb280d07faed2c4132e041/attachment/5fcc681a8b150c0be501db9e692ff1399c73a362/image.png) |  |
| 2 | Click on the Save button | * User sees that the daily individual lesson is created = inputted number of lessons |  |
| 3 | Check all lessons in the chain | * User sees two consecutive lessons that are 1 days apart.<br>* User sees that the other data is generated for all lessons in the chain. |  |
| 4 | Check lesson code | * User sees the lesson code gradually increase for each subsequent lesson in the chain. | ![image.png](https://d2cxucsjd6xvsd.cloudfront.net/public/team/b5f684e60ab1a64567fb280d07faed2c4132e041/attachment/e9091739eff95b74eb87fd052286a0fb53d63862/image.png) |
| 5 | Check lesson type | * User sees the default lesson type = 通常特訓 for all lessons. | ![image.png](https://d2cxucsjd6xvsd.cloudfront.net/public/team/b5f684e60ab1a64567fb280d07faed2c4132e041/attachment/672ecc241710950479dadf38add5d25928243319/image.png) |
| 6 | Check closed date | * User still sees lesson date that matches the closed date in the chain. |  |
| 7 | Check lesson report | * User sees individual lesson report is auto-created for all lessons in the chain | ![image.png](https://d2cxucsjd6xvsd.cloudfront.net/public/team/b5f684e60ab1a64567fb280d07faed2c4132e041/attachment/32f22f769767397d4371943d051939d253e688fe/image.png) |
| 8 | Login BO and view these lessons | * User sees these lessons on BO<br>* User sees the lesson code, lesson type is read-only on BO<br>* User sees the lesson report on Lesson detail -> Report tab and Lesson Report list on BO |  |


---

## TC-9676: User creates a daily group lesson by inputting lesson count without skip closed date

**Preconditions:**

* User has created master data (Location, AY, Course, Class, Closed Date, Academic Calendar)
* User has setup Academic Calendar with Location and Closed Date
* User has gone to the Manabie Lesson -> Lesson tab -> New button


**Steps:**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Input data with:<br><br>* Lesson date: Current date<br>* Lesson time<br>* Lesson name<br>* Location: with AC and Closed Date)<br>* Teaching Method: Group<br>* Course<br>* Class<br>* Classrooms<br>* Lesson Capacity<br>* Lesson Code<br>* Check the Recurrence Frequency<br>* Recurrence Type: Daily<br>* End Recurrence: After<br>* Number of Lessons: 100<br>* UnCheck the Skip Closed Date | ![image.png](https://d2cxucsjd6xvsd.cloudfront.net/public/team/b5f684e60ab1a64567fb280d07faed2c4132e041/attachment/5fcc681a8b150c0be501db9e692ff1399c73a362/image.png) |  |
| 2 | Click on the Save button | * User sees that the daily group lesson is created = inputted number of lessons |  |
| 3 | Check all lessons in the chain | * User sees two consecutive lessons that are 1 days apart.<br>* User sees that the other data is generated for all lessons in the chain. |  |
| 4 | Check lesson code | * User sees the lesson code gradually increase for each subsequent lesson in the chain. | ![image.png](https://d2cxucsjd6xvsd.cloudfront.net/public/team/b5f684e60ab1a64567fb280d07faed2c4132e041/attachment/e9091739eff95b74eb87fd052286a0fb53d63862/image.png) |
| 5 | Check lesson type | * User sees the default lesson type = 通常特訓 for all lessons. | ![image.png](https://d2cxucsjd6xvsd.cloudfront.net/public/team/b5f684e60ab1a64567fb280d07faed2c4132e041/attachment/672ecc241710950479dadf38add5d25928243319/image.png) |
| 6 | Check closed date | * User still sees lesson date that matches the closed date in the chain. |  |
| 7 | Check lesson report | * User sees group lesson report is auto-created for all lessons in the chain |  |
| 8 | Login BO and view these lessons | * User sees these lessons on BO<br>* User sees the lesson code, lesson type is read-only on BO<br>* User sees the lesson report on Lesson detail -> Report tab and Lesson Report list on BO |  |


---

## TC-9677: User creates a custom individual lesson by end date with skip closed date

**Description:** Verify that an existing activity lesson can be edited and updated details are saved correctly.

**Preconditions:**

* User has created master data (Location, AY, Course, Class, Closed Date, Academic Calendar)
* User has setup Academic Calendar with Location and Closed Date
* User has gone to the Manabie Lesson -> Lesson tab -> New button


**Steps:**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Input data with:<br><br>* Lesson date: Current date<br>* Lesson time<br>* Lesson name<br>* Location: with AC and Closed Date)<br>* Classrooms<br>* Lesson Capacity<br>* Lesson Code<br>* Lesson type: 通常特訓（時間変更）<br>* Check the Recurrence Frequency<br>* Recurrence Type: Custom<br>* Days of Week<br>* End Recurrence: On<br>* End Date: 31/3/2026<br>* Check the Skip Closed Date | ![image.png](https://d2cxucsjd6xvsd.cloudfront.net/public/team/b5f684e60ab1a64567fb280d07faed2c4132e041/attachment/90aa5506741917197f76922922d08ce58b90af0a/image.png) |  |
| 2 | Click on the Save button | * User sees that the custom individual lesson is created between the lesson start date and end date. | ![image.png](https://d2cxucsjd6xvsd.cloudfront.net/public/team/b5f684e60ab1a64567fb280d07faed2c4132e041/attachment/e9091739eff95b74eb87fd052286a0fb53d63862/image.png) |
| 3 | Check all lessons in the chain | * User sees day of week of all lessons in the chain = selected day of week<br>* User sees that the other data is generated for all lessons in the chain. |  |
| 4 | Check lesson code | * User sees the lesson code gradually increase for each subsequent lesson in the chain. | ![image.png](https://d2cxucsjd6xvsd.cloudfront.net/public/team/b5f684e60ab1a64567fb280d07faed2c4132e041/attachment/e9091739eff95b74eb87fd052286a0fb53d63862/image.png) |
| 5 | Check lesson type | * User sees the default lesson type = 通常特訓（時間変更） for all lessons. |  |
| 6 | Check skip closed date | * User does not see any lesson date that matches the closed date in the chain. | ![image.png](https://d2cxucsjd6xvsd.cloudfront.net/public/team/b5f684e60ab1a64567fb280d07faed2c4132e041/attachment/672ecc241710950479dadf38add5d25928243319/image.png) |
| 7 | Check lesson report | * User sees individual lesson report is auto-created for all lessons in the chain | ![image.png](https://d2cxucsjd6xvsd.cloudfront.net/public/team/b5f684e60ab1a64567fb280d07faed2c4132e041/attachment/32f22f769767397d4371943d051939d253e688fe/image.png) |
| 8 | Login BO and view these lessons | * User sees these lessons on BO<br>* User sees the lesson code, lesson type is read-only on BO<br>* User sees the lesson report on Lesson detail -> Report tab and Lesson Report list on BO |  |


---

## TC-9678: User creates a custom group lesson by selecting the end date without skip closed date

**Description:** Verify that an existing activity lesson can be edited and updated details are saved correctly.

**Preconditions:**

* User has created master data (Location, AY, Course, Class, Closed Date, Academic Calendar)
* User has setup Academic Calendar with Location and Closed Date
* User has gone to the Manabie Lesson -> Lesson tab -> New button


**Steps:**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Input data with:<br><br>* Lesson date: Current date<br>* Lesson time<br>* Lesson name<br>* Location: with AC and Closed Date)<br>* Teaching Method: Group<br>* Course<br>* Class<br>* Classrooms<br>* Lesson Capacity<br>* Lesson Code<br>* Lesson type: 通常特訓（時間変更）<br>* Check the Recurrence Frequency<br>* Recurrence Type: Custom<br>* Days of Week<br>* End Recurrence: On<br>* End Date: 31/3/2026<br>* Check the Skip Closed Date | ![image.png](https://d2cxucsjd6xvsd.cloudfront.net/public/team/b5f684e60ab1a64567fb280d07faed2c4132e041/attachment/90aa5506741917197f76922922d08ce58b90af0a/image.png) |  |
| 2 | Click on the Save button | * User sees that the custom group lesson is created between the lesson start date and end date. | ![image.png](https://d2cxucsjd6xvsd.cloudfront.net/public/team/b5f684e60ab1a64567fb280d07faed2c4132e041/attachment/e9091739eff95b74eb87fd052286a0fb53d63862/image.png) |
| 3 | Check all lessons in the chain | * User sees day of week of all lessons in the chain = selected day of week<br>* User sees that the other data is generated for all lessons in the chain. |  |
| 4 | Check lesson code | * User sees the lesson code gradually increase for each subsequent lesson in the chain. | ![image.png](https://d2cxucsjd6xvsd.cloudfront.net/public/team/b5f684e60ab1a64567fb280d07faed2c4132e041/attachment/e9091739eff95b74eb87fd052286a0fb53d63862/image.png) |
| 5 | Check lesson type | * User sees the default lesson type = 通常特訓（時間変更） for all lessons. |  |
| 6 | Check closed date | * User still sees lesson date that matches the closed date in the chain. |  |
| 7 | Check lesson report | * User sees group lesson report is auto-created for all lessons in the chain |  |
| 8 | Login BO and view these lessons | * User sees these lessons on BO<br>* User sees the lesson code, lesson type is read-only on BO<br>* User sees the lesson report on Lesson detail -> Report tab and Lesson Report list on BO |  |


---

## TC-9680: User creates a custom individual lesson by selecting the lesson count without skip closed date

**Description:** Verify that an existing activity lesson can be edited and updated details are saved correctly.

**Preconditions:**

* User has created master data (Location, AY, Course, Class, Closed Date, Academic Calendar)
* User has setup Academic Calendar with Location and Closed Date
* User has gone to the Manabie Lesson -> Lesson tab -> New button


**Steps:**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Input data with:<br><br>* Lesson date: Current date<br>* Lesson time<br>* Lesson name<br>* Location: with AC and Closed Date)<br>* Classrooms<br>* Lesson Capacity<br>* Lesson Code<br>* Lesson type: 通常特訓（時間変更）<br>* Check the Recurrence Frequency<br>* Recurrence Type: Custom<br>* **Days of Week**<br>* End Recurrence: After<br>* Number of Lessons: 500<br>* UnCheck the Skip Closed Date | ![image.png](https://d2cxucsjd6xvsd.cloudfront.net/public/team/b5f684e60ab1a64567fb280d07faed2c4132e041/attachment/90aa5506741917197f76922922d08ce58b90af0a/image.png) |  |
| 2 | Click on the Save button | * User sees that the custom individual lesson is created between the lesson start date and end date. | ![image.png](https://d2cxucsjd6xvsd.cloudfront.net/public/team/b5f684e60ab1a64567fb280d07faed2c4132e041/attachment/e9091739eff95b74eb87fd052286a0fb53d63862/image.png) |
| 3 | Check all lessons in the chain | * User sees day of week of all lessons in the chain = selected day of week<br>* User sees that the other data is generated for all lessons in the chain. |  |
| 4 | Check lesson code | * User sees the lesson code gradually increase for each subsequent lesson in the chain. | ![image.png](https://d2cxucsjd6xvsd.cloudfront.net/public/team/b5f684e60ab1a64567fb280d07faed2c4132e041/attachment/e9091739eff95b74eb87fd052286a0fb53d63862/image.png) |
| 5 | Check lesson type | * User sees the default lesson type = 通常特訓（時間変更） for all lessons. |  |
| 6 | Check closed date | * User still sees lesson date that matches the closed date in the chain. |  |
| 7 | Check lesson report | * User sees individual lesson report is auto-created for all lessons in the chain | ![image.png](https://d2cxucsjd6xvsd.cloudfront.net/public/team/b5f684e60ab1a64567fb280d07faed2c4132e041/attachment/32f22f769767397d4371943d051939d253e688fe/image.png) |
| 8 | Login BO and view these lessons | * User sees these lessons on BO<br>* User sees the lesson code, lesson type is read-only on BO<br>* User sees the lesson report on Lesson detail -> Report tab and Lesson Report list on BO |  |


---

## TC-9681: User creates a custom group lesson by selecting the lesson count with skip closed date

**Description:** Verify that an existing activity lesson can be edited and updated details are saved correctly.

**Preconditions:**

* User has created master data (Location, AY, Course, Class, Closed Date, Academic Calendar)
* User has setup Academic Calendar with Location and Closed Date
* User has gone to the Manabie Lesson -> Lesson tab -> New button


**Steps:**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Input data with:<br><br>* Lesson date: Current date<br>* Lesson time<br>* Lesson name<br>* Location: with AC and Closed Date)<br>* Teaching Method: Group<br>* Course<br>* Class<br>* Classrooms<br>* Lesson Capacity<br>* Lesson Code<br>* Lesson type: 通常特訓（時間変更）<br>* Check the Recurrence Frequency<br>* Recurrence Type: Custom<br>* **Days of Week**<br>* End Recurrence: After<br>* Number of Lessons: 100<br>* UnCheck the Skip Closed Date | ![image.png](https://d2cxucsjd6xvsd.cloudfront.net/public/team/b5f684e60ab1a64567fb280d07faed2c4132e041/attachment/90aa5506741917197f76922922d08ce58b90af0a/image.png) |  |
| 2 | Click on the Save button | * User sees that the custom group lesson is created between the lesson start date and end date. | ![image.png](https://d2cxucsjd6xvsd.cloudfront.net/public/team/b5f684e60ab1a64567fb280d07faed2c4132e041/attachment/e9091739eff95b74eb87fd052286a0fb53d63862/image.png) |
| 3 | Check all lessons in the chain | * User sees day of week of all lessons in the chain = selected day of week<br>* User sees that the other data is generated for all lessons in the chain. |  |
| 4 | Check lesson code | * User sees the lesson code gradually increase for each subsequent lesson in the chain. | ![image.png](https://d2cxucsjd6xvsd.cloudfront.net/public/team/b5f684e60ab1a64567fb280d07faed2c4132e041/attachment/e9091739eff95b74eb87fd052286a0fb53d63862/image.png) |
| 5 | Check lesson type | * User sees the default lesson type = 通常特訓（時間変更） for all lessons. |  |
| 6 | Check skip closed date | * User does not see any lesson date that matches the closed date in the chain. | ![image.png](https://d2cxucsjd6xvsd.cloudfront.net/public/team/b5f684e60ab1a64567fb280d07faed2c4132e041/attachment/672ecc241710950479dadf38add5d25928243319/image.png) |
| 7 | Check lesson report | * User sees group lesson report is auto-created for all lessons in the chain |  |
| 8 | Login BO and view these lessons | * User sees these lessons on BO<br>* User sees the lesson code, lesson type is read-only on BO<br>* User sees the lesson report on Lesson detail -> Report tab and Lesson Report list on BO |  |


---

## TC-1015: User creates a recurring individual lesson by selecting course schedule

**Description:** Ensure that deleting a recurring lesson removes all its instances from the calendar view.

**Preconditions:**

* User has created master data (Location, AY, Course, Class, Closed Date, Academic Calendar)
* User has setup Academic Calendar with Location and Closed Date
* User has gone to the Manabie Lesson -> Lesson tab -> New button


**Steps:**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | * Fill in the Lesson details, lesson code and select teaching method = Individual<br>* Select lesson date = closed date<br>* Check the Recurring Setting and Course Schedule<br>* Select the Program Master that have week order separate (Week 1_Week 3_Week 5_Week 10...)<br>* Click "Save" | * User sees a recurring individual lesson + lesson report are created within week order and selected weekday with "Draft" status<br><br><br>* User does not see a lesson that has lesson date = closed date<br><br><br>* User sees lesson code +1 for following lessons<br><br><br>* User sees default lesson type = 通常特訓 for all lessons | * Lesson 1 belong to Week 1<br><br><br>* Lesson 2 belong to Week 3<br><br><br>* Lesson 3 belong to Week 5<br><br><br>* Lesson 4 belong to Week 10<br><br><br><br> |
| 2 | Login BO and view this lesson | * User sees a individual lesson chain is created on the selected weekday within the program master.location academic week with "Draft" status on the Lesson list on BO<br>* User sees the lesson code, lesson type is read-only on BO<br><br><br>* User sees the individual lesson report is created with "Draft" status on Lesson detail -> Report tab and Lesson Report list on BO |  |


---

## TC-1016: User creates a recurring group lesson by selecting course schedule

**Description:** Check that a one-time lesson moves through the correct status flow (e.g., Scheduled, In Progress, Completed).

**Preconditions:**

* User has created master data (Location, AY, Course, Class, Closed Date, Academic Calendar)
* User has setup Academic Calendar with Location and Closed Date
* User has gone to the Manabie Lesson -> Lesson tab -> New button


**Steps:**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | * Fill in the Lesson details, lesson code and select teaching method = Group<br>* Check the Recurring Setting and Course Schedule so that the lesson in the middle of the chain is closed date<br>* Auto-fill the program master.location academic week of the location course<br>* Click "Save" | * User sees a group lesson chain is created on the selected weekday within the program master.location academic week with "Draft" status<br><br><br>* User does not see a lesson that has lesson date = closed date<br><br><br>* User sees lesson code +1 for following lessons<br><br><br>* User sees the group lesson report is created with "Draft" status<br><br><br>* User sees the lesson schedule is created with lesson schedule info as the same lesson info and contain all lessons in the chain |  |
| 2 | Login BO and view this lesson | * User sees a group lesson chain is created on the selected weekday within the program master.location academic week with "Draft" status on the Lesson list on BO<br><br><br>* User sees the lesson code, lesson type is read-only on BO<br><br><br>* User sees the group lesson report is created with "Draft" status on Lesson detail -> Report tab and Lesson Report list on BO |  |


---

## TC-1260: User cannot create lesson with input > 500 lesson count

**Preconditions:**

* User has created master data (Location, AY, Course, Class, Closed Date, Academic Calendar)
* User has setup Academic Calendar with Location and Closed Date
* User has gone to the Manabie Lesson -> Lesson tab -> New button


**Steps:**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Create a lesson count with number of lessons > 500 | Show an error message |  |


---

## TC-8815: Create a weekly lesson with end date so that the start&end date separated by 1 day of the week

**Preconditions:**

* User has created master data (Location, AY, Course, Class, Closed Date, Academic Calendar)
* User has setup Academic Calendar with Location and Closed Date
* User has gone to the Manabie Lesson -> Lesson tab -> New button


**Steps:**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Create a weekly lesson by end date with:<br><br>* Lesson date falls on Thursday<br>* End date falls on Friday | User sees lesson is created successfully and start&end date of all lessons in the chain in the same day |  |


---

## TC-8856: Create a lesson at beginning and end of day

**Preconditions:**

* User has created master data (Location, AY, Course, Class, Closed Date, Academic Calendar)
* User has setup Academic Calendar with Location and Closed Date
* User has gone to the Manabie Lesson -> Lesson tab -> New button


**Steps:**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Create a lesson at the beginning of day | User sees lesson is created successfully with correct lesson time | Lesson time: 00:00 - 00:15 |
| 2 | Create a lesson at the end of day | User sees lesson is created successfully with correct lesson time | Lesson time: 20:55 - 20:59 |


---

## TC-8994: User creates a custom lesson by inputting lesson count so that lesson count < selected days

**Preconditions:**

* User has created master data (Location, AY, Course, Class, Closed Date, Academic Calendar)
* User has setup Academic Calendar with Location and Closed Date
* User has gone to the Manabie Lesson -> Lesson tab -> New button


**Steps:**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Create a custom lesson with:<br><br>* Day of week: 3 days<br>* Number of lesson: 2 | User sees lesson is created successfully and follows the selected day of week |  |


---

## TC-9634: Create a recurring lesson with end date = lesson date + 1 and same lesson hours

**Preconditions:**

* User has created master data (Location, AY, Course, Class, Closed Date, Academic Calendar)
* User has setup Academic Calendar with Location and Closed Date
* User has gone to the Manabie Lesson -> Lesson tab -> New button


**Steps:**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Create a recurring lesson with:<br><br>* Lesson date: Current date<br>* End date: Tomorrow | * User sees lesson is created between lesson date and end date |  |


---

## TC-8993: Verify lesson schedule lighting record page

**Description:** ![image.png](https://d2cxucsjd6xvsd.cloudfront.net/public/team/b5f684e60ab1a64567fb280d07faed2c4132e041/attachment/9fcc412d6d3b076f1de5e2c5907c51cf9144a2f0/image.png)

**Preconditions:**

* User has created master data (Location, AY, Course, Class, Closed Date, Academic Calendar)
* User has setup Academic Calendar with Location and Closed Date
* User has gone to Lesson tab
* User has create a recurring lesson


**Steps:**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open lesson schedule of weekly lesson by end date | ![image.png](https://d2cxucsjd6xvsd.cloudfront.net/public/team/b5f684e60ab1a64567fb280d07faed2c4132e041/attachment/c30fb0c9ee5dc4c8d184262e0e0f55ce387b6d98/image.png) |  |
| 2 | Open lesson schedule of daily lesson by lesson count | ![image.png](https://d2cxucsjd6xvsd.cloudfront.net/public/team/b5f684e60ab1a64567fb280d07faed2c4132e041/attachment/cb37f0beeecb0b480016add3ef1b7e958578162f/image.png) |  |
| 3 | Open lesson schedule of custom lesson | ![image.png](https://d2cxucsjd6xvsd.cloudfront.net/public/team/b5f684e60ab1a64567fb280d07faed2c4132e041/attachment/9bbef56ceef65e1e04c19d182d9c2124c8236de9/image.png) |  |


---

## TC-8552: Verify data migration for bulk creation

**Preconditions:**

* User has created master data (Location, AY, Course, Class, Closed Date, Academic Calendar)
* User has setup Academic Calendar with Location and Closed Date
* User has gone to Lesson tab
* User has open creating lesson form


---

## TC-9088: Check translation

**Description:** Check number of lesson is required in editing lesson form

**Preconditions:**

* User has created master data (Location, AY, Course, Class, Closed Date, Academic Calendar)
* User has setup Academic Calendar with Location and Closed Date
* User has gone to Lesson tab
* User has open creating lesson form


---

## TC-11197: Validate location field on lesson creation form

**Description:** Locations marked as Closed Down should not appear in location selection: [https://manabie.atlassian.net/browse/LT-86517](https://manabie.atlassian.net/browse/LT-86517)


**Steps:**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Given There are locations in Location Master with multiple statuses |  |  |
| 2 | When User opens the location dropdown in lesson creation form (can open on lesson list page, on lesson calendar) |  |  |
| 3 | Then locations with status "Closed Down" (MANAERP__Status__c = 'Closed Down') are not displayed |  |  |


---

## TC-13875: Create a recurring lesson with location that have multiple ACs and skip closed date


---

## TC-12831: Create lesson with valid Start/End/Duration


---

## TC-12832: Create lesson only with Start+Duration


---

## TC-12833: Create lesson only with End+Duration


---

## TC-12834: Create mismatched Duration


---

## TC-12835: Duration=0 on create


---

## TC-12836: Duration negative, decimal number


---

## TC-12837: Start time and end time can not exceed 24hours of selected lesson date


---

## TC-12838: Start after End


---

## TC-12839: Start equals End


---

## TC-12840: Create recurring + mismatch


---

## TC-12841: Check default value which is set up in custom setting


---

## TC-12842: Create/Edit Duration with selected start time


---

## TC-12843: Edit Start Time with Existing Duration


---

## TC-12844: Edit End Time with Existing Duration


---

## TC-12845: Create/Edit Duration with selected end time


---

## TC-12846: Both Start and End Time Edited Manually


---

## TC-12847: Duration Field Cleared and change another value with selected start time and end time


---

## TC-12848: Edit Duration with selected start time and end time


---

## TC-12849: Duration Field Cleared with selected start time and end time


---

## TC-12850: Duration field cleared with selected start time


---

## TC-12851: Duration field cleared with selected end time


---

## TC-12852: Duration field cleared without selected start time and end time


---

## TC-12853: Auto-adjust End Time to match defined duration when start/end times are provided manually

