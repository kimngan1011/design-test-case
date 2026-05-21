# Student - Course Tab: Assign Class

## Single Assign Class

### TC-10533: User creates a lesson and then assign the same class to a student with current date

**Preconditions:**

* User has published a recurring group lesson with Class A
* User has created a lesson allocation in the past for the student with Required Allocation = True (refer to [https://app.qase.io/case/PX-1517](https://app.qase.io/case/PX-1517))

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | * Go to Manabie User -> Student Details -> Course Ta | - | - |
| 2 | * Select a Class A that has been assigned to the lesson<br>* Fill in the effective date = current date<br>* Click \"Save\" | * User sees the class is updated for the student<br>* User sees student is assigned to all lessons in the chain with the lesson date falling within the class_member duration, and the student does not exist in the lesson | - |
| 3 | Check lesson report of added student | * User sees the lesson report detail is auto-created for the student | - |
| 4 | Check lesson allocation | * User sees the student session is auto-created = assigned lessons (no empty student session)<br>* User sees the lesson allocation of the student is updated (Lesson Allocated, Lesson Allocation Status, Report History) | - |
| 5 | Login BO and view the student | * User sees the student in detailed lesson page of the lessons in the chain on BO<br>* User sees the lesson report detail is created for the student on BO | - |
| 6 | Student login Mobile and view the lesson | * Student sees the lesson and lesson report with correct information | - |

---

### TC-11352: User creates a lesson and then assign the same class to a student with future date

**Preconditions:**

* User has published a recurring group lesson with Class A
* User has created a lesson allocation in the past for the student with Required Allocation = True (refer to [https://app.qase.io/case/PX-1517](https://app.qase.io/case/PX-1517))

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | * Go to Manabie User -> Student Details -> Course Ta | - | - |
| 2 | * Select a Class A that has been assigned to the lesson<br>* Fill in the effective date = future<br>* Click \"Save\" | * User sees the class is updated for the student<br>* User sees student is assigned to all lessons in the chain with the lesson date falling within the class_member duration, and the student does not exist in the lesson | - |
| 3 | Check lesson report of added student | * User sees the lesson report detail is auto-created for the student | - |
| 4 | Check lesson allocation | * User sees the student session is auto-created = assigned lessons (no empty student session)<br>* User sees the lesson allocation of the student is updated (Lesson Allocated, Lesson Allocation Status, Report History) | - |

---

### TC-10534: User assigns a class to a student with current date and then creates a lesson

**Preconditions:**

* User has created a lesson allocation in the past for the student with Required Allocation = True (refer to [https://app.qase.io/case/PX-1517](https://app.qase.io/case/PX-1517))

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | * Go to Manabie User -> Student Details -> Course Ta | - | - |
| 2 | * User has assigned Class A to a student with the effective date = current date<br>* Create a recurring group lesson with Class A that has been assigned to the student | * User sees the class is updated for the student<br>* User sees student is assigned to all lessons in the chain with the lesson date falling within the class_member duration, and the student does not exist in the lesson | - |
| 3 | Check lesson report of added student | * User sees the lesson report detail is auto-created for the student | - |
| 4 | Check lesson allocation | * User sees the student session is auto-created = assigned lessons (no empty student session)<br>* User sees the lesson allocation of the student is updated (Lesson Allocated, Lesson Allocation Status, Report History) | - |
| 5 | Login BO and view the student | * User sees the student in detailed lesson page of the lessons in the chain on BO<br>* User sees the lesson report detail is created for the student on BO | - |
| 6 | Student login Mobile and view the lesson | * Student sees the lesson and lesson report with correct information | - |

---

### TC-11353: User assigns a class to a student with future date and then creates a lesson

**Preconditions:**

* User has created a lesson allocation in the future for the student with Required Allocation = True (refer to [https://app.qase.io/case/PX-10453](https://app.qase.io/case/PX-10453))

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | * Go to Manabie User -> Student Details -> Course Ta | - | - |
| 2 | * User has assigned Class A to a student with the effective date = future date<br>* Create a recurring group lesson with Class A that has been assigned to the student | * User sees the class is updated for the student<br>* User sees student is assigned to all lessons in the chain with the lesson date falling within the class_member duration, and the student does not exist in the lesson | - |
| 3 | Check lesson report of added student | * User sees the lesson report detail is auto-created for the student | - |
| 4 | Check lesson allocation | * User sees the student session is auto-created = assigned lessons (no empty student session)<br>* User sees the lesson allocation of the student is updated (Lesson Allocated, Lesson Allocation Status, Report History) | - |

---

### TC-11321: User creates a manual lesson and then assign the same class to a student with current date

**Preconditions:**

* User has published a manual lesson with Class A (refer to [https://app.qase.io/case/PX-1018](https://app.qase.io/case/PX-1018))
* User has created a lesson allocation in the past for the student with Required Allocation = True (refer to [https://app.qase.io/case/PX-1517](https://app.qase.io/case/PX-1517))

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | * Go to Manabie User -> Student Details -> Course Ta | - | - |
| 2 | * Select a Class A that has been assigned to the lesson<br>* Fill in the effective date = current date<br>* Click \"Save\" | * User sees the class is updated for the student<br>* User sees student is assigned to all lessons in the chain with the lesson date falling within the class_member duration, and the student does not exist in the lesson | - |
| 3 | Check lesson report of added student | * User sees the lesson report detail is auto-created for the student | - |
| 4 | Check lesson allocation | * User sees the student session is auto-created = assigned lessons (no empty student session)<br>* User sees the lesson allocation of the student is updated (Lesson Allocated, Lesson Allocation Status, Report History) | - |
| 5 | Login BO and view the student | * User sees the student in detailed lesson page of the lessons in the chain on BO<br>* User sees the lesson report detail is created for the student on BO | - |
| 6 | Student login Mobile and view the lesson | * Student sees the lesson and lesson report with correct information | - |

---

### TC-11322: User assigns a class to a student with future date and then creates a manual lesson

**Preconditions:**

* User has created a lesson allocation in the future for the student with Required Allocation = True (refer to [https://app.qase.io/case/PX-10453](https://app.qase.io/case/PX-10453))

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | * Go to Manabie User -> Student Details -> Course Ta | - | - |
| 2 | * User has assigned Class A to a student with the effective date = future date<br>* Create a recurring group lesson with Class A that has been assigned to the student | * User sees the class is updated for the student<br>* User sees student is assigned to all lessons in the chain with the lesson date falling within the class_member duration, and the student does not exist in the lesson | - |
| 3 | Check lesson report of added student | * User sees the lesson report detail is auto-created for the student | - |
| 4 | Check lesson allocation | * User sees the student session is auto-created = assigned lessons (no empty student session)<br>* User sees the lesson allocation of the student is updated (Lesson Allocated, Lesson Allocation Status, Report History) | - |

---

### TC-10535: User assigns 1 active class and 1 future lesson for the student

**Preconditions:**

* User has created lesson allocation for the student
* User has created a recurring group lesson with Class A
* User has created a recurring group lesson with Class B
* User has assigned Class A to a student with the effective date = current date

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | * Go to Manabie User -> Student Details -> Course Ta | - | - |
| 2 | * User continued to assign Class B for this student with the effective date = future date | * User sees student is assigned to all lessons of Lesson.Class A following the Class A's class_member duration<br>* User sees student is assigned to all lessons of Lesson.Class B following the Class B's class_member duration<br>* User sees the future class update to active class when effective date = current date | - |
| 3 | Check lesson report of added student | * User sees the lesson report detail is auto-created for the student | - |
| 4 | Check lesson allocation | * User sees the student session is auto-created = assigned lessons (no empty student session)<br>* User sees the lesson allocation of the student is updated (Lesson Allocated, Lesson Allocation Status, Report History) | - |
| 5 | Check class info when the effective date.Class B = current date | * User sees update active class = Class B | - |

---

### TC-10536: User changes a active class

**Preconditions:** -

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | * Go to Manabie User -> Student Details -> Course Ta | - | - |
| 2 | * Change to Class B with the effective date = current date | * User sees the student's class is updated to Class B<br>* User sees student is removed from the draft, published, cancelled lesson class A<br>* User still sees the student in the completed lesson class A<br>* User sees the student is assigned to the lesson class B following the class member duration | - |
| 3 | Check lesson report of added student | * User sees the lesson report detail is auto-created for the student | - |
| 4 | Check lesson report of removed student | * User does not see the lesson report detail of the removed student | - |
| 5 | Check lesson allocation | * User sees the student session is auto-created = assigned lessons (no empty student session)<br>* User sees the lesson allocation of the student is updated (Lesson Allocated, Lesson Allocation Status, Report History) | - |

---

### TC-11354: User changes a active class of a LA have multiple classes

**Preconditions:** -

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | * Go to Manabie User -> Student Details -> Course Ta | - | - |
| 2 | * Change to Class C with the effective date = current date | * User sees the student's class is updated to Class C<br>* User sees student is removed from the draft, published, cancelled lesson class A and B<br>* User still sees the student in the completed lesson class A<br>* User sees the student is assigned to the lesson class C following the class member duration | - |
| 3 | Check lesson report of added student | * User sees the lesson report detail is auto-created for the student | - |
| 4 | Check lesson report of removed student | * User does not see the lesson report detail of the removed student | - |
| 5 | Check lesson allocation | * User sees the student session is auto-created = assigned lessons (no empty student session)<br>* User sees the lesson allocation of the student is updated (Lesson Allocated, Lesson Allocation Status, Report History) | - |

---

### TC-10537: User changes a future class

**Preconditions:**

* User has created lesson allocation in the future with the Require Allocation flag = True
* User has assigned Class A to a student with the effective date = future date (refer to [https://app.qase.io/case/PX-11353](https://app.qase.io/case/PX-11353))
* User has completed, published, cancelled some lessons of the student class A

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | * Go to Manabie User -> Student Details -> Course Ta | - | - |
| 2 | * Change to Class B with the effective date > effective date.class A | * User sees the student's class is updated to Class B<br>* User sees student is removed from the draft, published, cancelled lesson class A<br>* User still sees the student in the completed lesson class A<br>* User sees the student is assigned to the lesson class B following the class member duration | - |
| 3 | Check lesson report of added student | * User sees the lesson report detail is auto-created for the student | - |
| 4 | Check lesson report of removed student | * User does not see the lesson report detail of the removed student | - |
| 5 | Check lesson allocation | * User sees the student session is auto-created = assigned lessons (no empty student session)<br>* User sees the lesson allocation of the student is updated (Lesson Allocated, Lesson Allocation Status, Report History) | - |

---

### TC-10538: User changes a past class

**Preconditions:**

* User has created lesson allocation with the Require Allocation flag = True for the student
* User has assigned Class A to a student in the past


* Student has assigned to a lesson

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | * Go to Manabie User -> Student Details -> Course Ta | - | - |
| 2 | * Change to Class B with the effective date = current date | * User sees the student with:<br>    * Class A: Start date in the past - Effective date - 1<br>    * Class B: Effective date - LA's end date<br><br>* User still sees the student in the lesson.class A within class member duration<br>* User sees the student in the lesson.class B within class member duration | Class A: 2025/03/10 0:00 - 2026/01/31 23:59 -> student is assigned to lesson from 2025/03/10 0:00 -> 2026/01/31 23:59<br><br>After that, change to class B với effective date = 2025/03/17<br>Class 1: 2025/03/10 0:00 - 2025/03/16 23:59<br>-> Student is assigned to lesson from 2025/03/10 0:00 -> 2025/03/16 23:59<br>Class 2: 2025/03/17 0:00 - 2026/01/31 23:59<br>-> Student is assigned to lesson from 2025/03/17 0:00 -> 2026/01/31 23:59 |

---

### TC-10539: User cancels a future class in the student that has only 1 future class

**Preconditions:**

* User has created lesson allocation with the Require Allocation flag = True for the student
* User has assigned a class to a student with the effective date = future date
* User has published a recurring group lesson with this class

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | * Go to Manabie User -> Student Details -> Course Ta | - | - |
| 2 | Select a lesson allocation and click \"Cancel Scheduled Class Update\" | * User does not a class in the student<br>* User sees student is removed from the all lessons in the chain | - |
| 3 | Check lesson report of removed student | * User does not see the lesson report detail of the removed student | - |
| 4 | Check lesson allocation | * User sees the student sessions linked to the lessons which the removed student is deleted<br>* User sees the lesson allocation of the student is updated (Lesson Allocated, Lesson Allocation Status, Report History) | - |
| 5 | Student login Mobile | * Student does not see the lesson | - |

---

### TC-10540: User cancels a future class in the student that has 1 active class and 1 future class

**Preconditions:**

* User has created lesson allocation with the Require Allocation flag = True for the student
* User has assigned 1 active class with a start date in the past and 1 future class to a student
* User has created a recurring group lesson with the active class and future class

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | * Go to Manabie User -> Student Details -> Course Ta | - | - |
| 2 | Select a lesson allocation and click \"Cancel Scheduled Class Update\" | * User only sees active class in the student and updates the class_member duration for the active class<br>* User sees the student in the all lessons of the active class with lesson date belongs to the class_member duration of the active class<br>* User sees student is removed from the all lessons of the future class | - |
| 3 | Check lesson report of added student | * User sees the lesson report detail is auto-created for the student | - |
| 4 | Check lesson report of removed student | * User does not see the lesson report detail of the removed student | - |
| 5 | Check lesson allocation | * User sees the student session is auto-created = assigned lessons (no empty student session)<br>* User sees the lesson allocation of the student is updated (Lesson Allocated, Lesson Allocation Status, Report History) | - |

---

### TC-13989: Create past recurring lesson with a class that has lesson and class member in the past

**Preconditions:**

* Class member A: 2025-10-01 - 2026-12-31 has:
    * Lesson Schedule 1: 2025-10-01 - 2026-12-31

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | * Today: 2025-12-18<br>    * Create Lesson Schedule 2 (2025-10-01 - 2026-12-31) with Class A | * Remain a student in the all old lessons<br>* Auto-assign a student to a lesson following class member duration | - |

---

### TC-14231: Create past recurring lesson with a class that has multiple class member

**Preconditions:**

* Lesson Allocation A has:
    * Class Member 1: 2025-10-01 -2025-11-01
    * Class Member 2: 2025-11-02 -2026-11-01

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | * Today: 2025-12-18<br>    * Create Lesson Schedule 2 (2025-10-01 - 2026-12-31) with Class 1 and Class 2 | Auto-assign a student to a lesson following the **<span style=\"color:var(--md-font-color-failed)\">active</span>** class member duration in LA | - |

---

## Bulk Assign Class

### TC-10556: Verify Academic Level field is visible in Student upsert form under General Info section

**Description:** Ensures that the Academic Level field is present and visible when creating or editing a student record.

**Preconditions:**

User has permission to view or edit student records.

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Navigate to the Student upsert form. | The Academic Level field is displayed in the General Info section. | - |

---

### TC-10557: Verify Academic Level field is visible in Class upsert form

**Description:** Checks that the Academic Level field is present and visible when creating or editing a class record.

**Preconditions:**

User has permission to view or edit class records.

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Navigate to the Class upsert form. | The Academic Level field is displayed in the form. | - |

---

### TC-10558: Validate Academic Level picklist values for Student and Class

**Preconditions:**

User is on the Student or Class upsert form.

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Click on the Academic Level picklist. | The picklist displays refer to global picklist | - |

---

### TC-10559: Validate formula checkbox: Student’s Academic Level does not match Class’ Academic Level

**Description:** Ensures the formula checkbox is checked when the Student’s Academic Level is different from the Class’ Academic Level.

**Preconditions:**

A student and class with different Academic Levels exist.

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Add a student with Academic Level 'Rensei (錬成)' to a class with Academic Level 'TOP'. | Formula checkbox is checked indicating mismatch. | - |

---

### TC-10560: User sees the default bulk assign class

**Description:** Verify the bulk assign class popup

**Preconditions:** -

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | * Go to Manabie User -> Student -> Course | * User sees the default as disable | - |

---

### TC-10561: User sees the validation on effective date field

**Preconditions:**

* User has created multiple LAs
    * LA in the past
    * LA in the future

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | * Select multiple LAs in the future (different start date) | * User sees autofill latest LA's start date to the effective date<br><br>* User sees the error message when edit effective date < latest LA's start date | - |
| 2 | * Select multiple LAs in the past and future | * User sees autofill latest LA's start date to the effective date<br>* User sees the error message when edit effective date < latest LA's start date | - |
| 3 | * Select multiple LAs in the future | * User sees autofill LA's start date to the effective date<br><br>* User sees the error message when edit effective date < LA's start date | - |
| 4 | * Select multiple LAs in the past | * User sees autofill current date to the effective date<br><br>* User sees the error message when edit effective date < current date | - |

---

### TC-10562: User sees the alert popup

**Preconditions:**

* User has created the Student AL = TOP

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | * Select class academic level = Rensei | * User sees the alert | - |
| 2 | * Select class academic level = TOP | * User does not see the alert | - |

---

### TC-10564: User sees the default Class Academic Level and Student AL

**Preconditions:**

* User has created the student's academic level in contact

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | * Select 1 LA and open bulk assign class popup | * User sees the Class Academic Level and Student AL = Student's Academic Level in Contact | - |
| 2 | Edit Student AL | Update Class AL | - |
| 3 | Edit Class AL | Retain Student AL | - |

---

### TC-10563: User assigns a class academic level with effective date = current date

**Preconditions:**

* Create a class with class academic level
    * Class 1 - TOP
    * Class 2 - Rensei
    * Class 3 - Select
* Create a recurring group lesson with Class 1
* Create a LA

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Select multiple LAs -> Click \"Bulk Assign Class\" -> Select \"TOP\" | - | - |
| 2 | Fill in an effective date = current date | - | - |
| 3 | Click \"Save\" button | Class 1 is update to LA | - |
| 4 | Check class assignment | Assign a student to a lesson with Class 1 (refer to TC [https://app.qase.io/case/PX-10533](https://app.qase.io/case/PX-10533)) | - |

---

### TC-10565: User assigns a class academic level with effective date = future date

**Preconditions:**

* Create a class with class academic level
    * Class 1 - TOP
    * Class 2 - Rensei
    * Class 3 - Select
* Create a recurring group lesson with Class 2
* Create a LA

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Select multiple LAs -> Click \"Bulk Assign Class\" -> Select \"Rensei\" | - | - |
| 2 | Fill in an effective date = future date | - | - |
| 3 | Click \"Save\" button | Class 2 is update to LA | - |
| 4 | Check class assignment | Assign a student to a lesson with Class 1 (refer to TC [https://app.qase.io/case/PX-11352](https://app.qase.io/case/PX-11352)) | - |

---

### TC-10566: User assigns a class academic level with effective date = current date and future date

**Preconditions:**

* Create a class with class academic level
    * Class 1 - TOP
    * Class 2 - Rensei
    * Class 3 - Select
* Create a recurring group lesson with Class 2
* Create a recurring group lesson with Class 3
* Create a LA

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | * Assign \"Rensei\" with effective date = current date to LA<br>* Assign \"Select\" with effective date = future date to this LA | * Class 2 is update to LA with <br>    * Start date = Current date<br>    * End date = Effective date.Select - 1<br>* Class 2 is update to LA with <br>    * Start date = Effective date.Select<br>    * End date = end date.LA | - |
| 2 | Check class assignment | * Assign a student to a lesson with Class 2 and 3 (refer to TC [https://app.qase.io/case/PX-10535](https://app.qase.io/case/PX-10535)) | - |

---

### TC-10567: User assigns a class academic level to multiple LAs with effective date = current date

**Preconditions:**

* Create a class with class academic level
    * LC 1 - Class 1 - TOP
    * LC 2 - Class 1 - TOP
* Create multiple LAs

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | * Select multiple LAs and assign class academic level \"TOP\" with effective date = current date | * Class 1 is update to LA 1<br>* Class 1 is update to LA 2 | - |
| 2 | * Create a recurring group lesson L1 with LC 1 - Class 1<br>* Create a recurring group lesson L2 with LC 2 - Class 1 | * Assign a student to a lesson L1 and L2 (refer to TC [https://app.qase.io/case/PX-10534](https://app.qase.io/case/PX-10534)) | - |

---

### TC-10568: User assigns a class academic level to multiple LAs with effective date = future date

**Preconditions:**

* Create a class with class academic level
    * LC 1 - Class 1 - TOP
    * LC 2 - Class 1 - TOP
* Create multiple LAs

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | * Select multiple LAs and assign class academic level \"TOP\" with effective date = future date | * Class 1 is update to LA 1<br>* Class 1 is update to LA 2 | - |
| 2 | * Create a recurring group lesson L1 with LC 1 - Class 1<br>* Create a recurring group lesson L2 with LC 2 - Class 1 | * Assign a student to a lesson L1 and L2 (refer to TC [https://app.qase.io/case/PX-11353](https://app.qase.io/case/PX-11353)) | - |

---

### TC-10569: User changes a class academic level with effective date = current date

**Preconditions:**

* Create a class with class academic level
    * Class 1 - TOP
    * Class 2 - Rensei
    * Class 3 - Select
* Create a recurring group lesson with Class 1
* Create a LA

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | User has assigned \"TOP\" with effective date = current date | Refer to TC [ERP-2010](https://app.qase.io/case/ERP-2010) | - |
| 2 | * Create a recurring group lesson with Class 2 | - | - |
| 3 | Change to \"Rensei\" with effective date = current date | Assign Class 2 to LA | - |
| 4 | Check class assignment | Refer to TC [https://app.qase.io/case/PX-10536](https://app.qase.io/case/PX-10536) | - |

---

### TC-10570: User changes a class academic level with effective date = future date

**Preconditions:**

* Create a class with class academic level
    * Class 1 - TOP
    * Class 2 - Rensei
    * Class 3 - Select
* Create a recurring group lesson with Class 1
* Create a LA
* User has assigned "TOP" with effective date = future date 9 (Refer to TC [ERP-2010](https://app.qase.io/case/ERP-2010))

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | * Create a recurring group lesson with Class 2<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ Change to \"Rensei\" with effective date < effective date.TOP<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ Check class assignment | - | - |
| 2 | * Create a recurring group lesson with Class 3<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ Change to \"Select\" with effective date > effective date.TOP<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ Check class assignment | - | - |

---

### TC-10571: User changes a class academic level for a class that is assigned by other cases

**Preconditions:**

* Create a class with class academic level
    * LC 1 - Class 1 - TOP
    * LC 2 - Class 1 - TOP
    * LC 3 - Class 1 - TOP
* Assign Class 1 to LA 1 by assigning class in student-course detail
* Assign Class 2 to LA 2 by assigning class in location course detail
* Assign Class 3 to LA 3 by assigning class in LA detail
* Create lesson L1, L2, L3 with LC 1, LC 2, LC 3 and Class 1

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Select LA1, LA2, LA3 and assign \"TOP\" with effective date = current date | Class is update for each LA | - |
| 2 | Check class assignment | LA1, LA2, LA3 are assigned to Lesson L1, L2, L3 follow to the class member duration | - |

---

### TC-10572: Skip assign a class when having same academic level

**Preconditions:**

* Create a class with class academic level under 1 location course
    * Class 1 - TOP
    * Class 2 - TOP
* Create a recurring group lesson with Class 1
* Create a LA

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Select multiple LAs -> Click \"Bulk Assign Class\" -> Select \"TOP\" | - | - |
| 2 | Fill in an effective date = current date | - | - |
| 3 | Click \"Save\" button | User does not see class in the LA | - |

---

### TC-10573: Skip assign a class when existing in class member table

**Preconditions:**

* Create a class with class academic level under 1 location course
    * Class 1 - TOP
* Create a recurring group lesson with Class 1 and effective date = current date
* Create a LA and assign Class 1 by assigning class in LA detail

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Select multiple LAs -> Click \"Bulk Assign Class\" -> Select \"TOP\" | - | - |
| 2 | Fill in an effective date = future date | - | - |
| 3 | Click \"Save\" button | Retain Class 1 and do not update effective date | - |

---

### TC-10575: Update student's AL in contact after bulk assign class successfully

**Preconditions:**

Create a student with academic level = TOP

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Bulk assign class with Student AL = Select | Update student's academic level in contact = Select | - |

---

### TC-10576: Update success message

**Preconditions:** -

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Bulk assign class | * Update Successul message<br>    * EN: **Class assignment is being processed. Only classes matching the selected academic level will be assigned.**<br>    * JP: **クラスの割り当てを処理中です。選択した学習レベルに一致するクラスのみが割り当てられます。** | - |

---

### TC-10592: Show alert when no classes matching with selected class academic level

**Preconditions:**

* User has created Location Course A has only Class X. Class X’s academic level is `Basic`

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | On Bulk Assign Class, select Advance | Show an error message<br>JP: 選択された学習レベルに対応するクラスが存在しません。他のレベルを選択してください。<br>![image-20250915-043524.png](https://d2cxucsjd6xvsd.cloudfront.net/public/team/b5f684e60ab1a64567fb280d07faed2c4132e041/attachment/181770a3f63ea87694997c217f9a5d5c29e3e1b9/image-20250915-043524.png) | - |

---
