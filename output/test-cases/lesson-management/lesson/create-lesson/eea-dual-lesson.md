# EEA Dual Lesson

## Object Setting - LBAC - Translation

### TC-14891: Verify new fields in Lesson Schedule object

**Description:** ![image.png](https://d2cxucsjd6xvsd.cloudfront.net/public/team/b5f684e60ab1a64567fb280d07faed2c4132e041/attachment/6cfd97cdf18cc34f0441082f36cfeb0ef717ba77/image.png)

**Preconditions:** -

_Steps TBD_

---

### TC-14892: HQ Import pair LS with the LS's location != the related LS's location

**Preconditions:**

* CM's affiliation: Location 1

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | HQ Import pair LS with <br><br>* The LS's location = Location 1<br>* The related LS's location = Location 2 | Import successfully | - |
| 2 | CM open lesson schedule detail and view related LS | ? | - |
| 3 | CM open lesson detail and view pair lesson | ? | - |

---

### TC-14894: CM import pair LS but no access to related LS

**Preconditions:**

* CM's affiliation: Location 1
* HQ Staff create related LS at Location 2

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | CM import pair LS with related LS at Location 2 | ? | - |

---

### TC-14895: CM add pair LS manually with the LS's location != the related LS's location

**Preconditions:**

* CM's affiliation: Location 1

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | CM add pair LS manually with<br><br>* The LS's location = Location 1<br>* The related LS's location = Location 2 | Add successfully | - |
| 2 | CM open lesson schedule detail and view related LS | ? | - |
| 3 | CM open lesson detail and view pair lesson | ? | - |

---

### TC-14897: Verify translation

**Preconditions:** -

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Import CSV with JP | - | - |
| 2 | Verify an error message | - | - |
| 3 | Verify UI | - | - |

---

## Set up Paired Lesson Schedules

### TC-14898: CM Import paired LS with valid CSV

**Preconditions:** -

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | CM view Related LS in LS Detail | Create a custom Dual Lesson Schedule related list, including columns:<br><br>* Label: Related Lesson Schedule<br><br><br>* Columns:<br>    * Lesson Schedule Name (hyperlink)<br>    * External_id | - |
| 2 | CM view paired lesson on SF Lesson Detail/Calendar | Show pair lesson correctly | - |
| 3 | Teacher view paired lesson on BO Lesson Detail/Calendar | Show pair lesson correctly | - |

---

### TC-14899: CM Verify Related Lesson Schedule lookup is auto-populated after import

**Preconditions:** -

_Steps TBD_

---

### TC-14900: CM Verify pairing is visible from both Lesson Schedules

**Preconditions:** -

_Steps TBD_

---

### TC-14901: Import Lesson Schedule without Related_Lesson_Schedule_External_ID

**Preconditions:** -

_Steps TBD_

---

### TC-14905: CM import with Related Lesson Schedule Internal ID not found

**Preconditions:** -

_Steps TBD_

---

### TC-14907: CM import with One-sided pairing (LS1->LS2->LS3->LS1)

**Preconditions:** -

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | CM import with One-sided pairing (LS1->LS2->LS3->LS1) | Get latest<br>LS1 <> LS3<br>LS 2 <> () | - |

---

### TC-14902: CM Cannot import duplicate Partner Internal ID

**Preconditions:** -

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | CM Import duplicate Partner Internal ID | * **Error Message:** “Partner Internal ID must be unique. Another record with the same Partner Internal ID already exists.” | - |

---

### TC-14903: CM Cannot Import Partner Internal ID with invalid format

**Preconditions:** -

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | CM Import Partner Internal ID with invalid format | * **Error Message:** “Invalid Internal ID format. External ID must follow the pattern: LSN-#### (e.g. LSN-0001).” | - |

---

### TC-14904: CM Cannot Import Related_Lesson_Schedule_External_ID = Partner_Internal_ID

**Preconditions:** -

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | CM Import Related_Lesson_Schedule_External_ID = Partner_Internal_ID | * **Error Message:** “Lesson Schedule External ID must be different from the record’s External ID.” | - |

---

### TC-14906: CM Cannot import with Multiple related IDs

**Preconditions:** -

_Steps TBD_

---

### TC-14908: CM import with Partial CSV failure

**Preconditions:** -

_Steps TBD_

---

### TC-14909: CM Re-import update pairing

**Preconditions:** -

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | CM Re-import update pairing | * Update Related LS for new LS<br><br><br>* Remove Related LS from old LS | - |
| 2 | Teacher view lesson detail after updating on BO | Pair lesson is updated correctly | - |

---

### TC-14910: Admin Delete Related Lesson Schedule

**Preconditions:** -

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Admin Delete Related Lesson Schedule | Auto-remove related LS that is deleted | - |
| 2 | Teacher view lesson detail after updating on BO | Pair lesson is deleted correctly | - |

---

### TC-14911: CM Verify the related LS list

**Preconditions:** -

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | CM Verify the related LS list | Filter to only show LS that not in the pair Lesson schedule list | - |

---

### TC-14913: CM Add Related Lesson Schedule manually

**Preconditions:** -

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | CM view Related LS in LS Detail | Create a custom Dual Lesson Schedule related list, including columns:<br><br>* Label: Related Lesson Schedule<br><br><br>* Columns:<br>    * Lesson Schedule Name (hyperlink)<br>    * External_id | - |
| 2 | CM view paired lesson on SF Lesson Detail/Calendar | Show pair lesson correctly | - |
| 3 | Teacher view paired lesson on BO Lesson Detail/Calendar | Show pair lesson correctly | - |

---

### TC-14915: CM Remove Related Lesson Schedule

**Preconditions:** -

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | CM view Related LS in LS Detail after deleted | Related LS is deleted | - |
| 2 | CM view paired lesson on SF Lesson Detail/Calendar | Show pair lesson is deleted correctly | - |
| 3 | Teacher view paired lesson on BO Lesson Detail/Calendar | Show pair lesson is deleted correctly | - |

---

### TC-14916: CM Reassign after removal

**Preconditions:** -

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | CM view Related LS in LS Detail | Create a custom Dual Lesson Schedule related list, including columns:<br><br>* Label: Related Lesson Schedule<br><br><br>* Columns:<br>    * Lesson Schedule Name (hyperlink)<br>    * External_id | - |
| 2 | CM view paired lesson on SF Lesson Detail/Calendar | Show pair lesson correctly | - |
| 3 | Teacher view paired lesson on BO Lesson Detail/Calendar | Show pair lesson correctly | - |

---

### TC-14925: CM Edit Related Lesson Schedule

**Preconditions:** -

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | CM view Related LS in LS Detail after updating | Create a custom Dual Lesson Schedule related list, including columns:<br><br>* Label: Related Lesson Schedule<br><br><br>* Columns:<br>    * Lesson Schedule Name (hyperlink)<br>    * External_id | - |
| 2 | CM view paired lesson on SF Lesson Detail/Calendar | Show pair lesson is updated correctly | - |
| 3 | Teacher view paired lesson on BO Lesson Detail/Calendar | Show pair lesson is updated correctly | - |

---

## View Paired Lesson Information

### TC-14917: CM view paired lesson by lesson code on SF Lesson Detail

**Description:** ![image.png](https://d2cxucsjd6xvsd.cloudfront.net/public/team/b5f684e60ab1a64567fb280d07faed2c4132e041/attachment/bd9db11f4c6c9f6e7a3c027cb7da91e50a182eb7/image.png)

**Preconditions:** -

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | CM view paired lesson on SF Lesson Detail | Show pair lesson in right panel<br><br>* Label: Pair Lesson<br><br><br>* Value: Lesson name (hyperlink) | - |

---

### TC-14918: Teacher view paired lesson by lesson code on BO Lesson Detail

**Description:** ![image.png](https://d2cxucsjd6xvsd.cloudfront.net/public/team/b5f684e60ab1a64567fb280d07faed2c4132e041/attachment/bd9db11f4c6c9f6e7a3c027cb7da91e50a182eb7/image.png)

**Preconditions:** -

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Teacher view paired lesson by lesson code on BO Lesson Detail | Display under Lesson Detail header<br><br>* Paired with: Lesson name | - |

---

### TC-14919: CM view paired lesson by lesson code on SF Calendar

**Description:** ![image.png](https://d2cxucsjd6xvsd.cloudfront.net/public/team/b5f684e60ab1a64567fb280d07faed2c4132e041/attachment/bd9db11f4c6c9f6e7a3c027cb7da91e50a182eb7/image.png)

**Preconditions:** -

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | CM view paired lesson on SF Calendar | Show Pair Lesson in related list:<br><br>* Lesson Schedule<br><br><br>* Pair Lesson:<br>    *  Lesson Name (Hyperlink)<br>    * Lesson Date, Lesson time<br>    * Teacher name<br>* Related list | - |

---

### TC-14920: Teacher view paired lesson by lesson code on BO Calendar

**Description:** ![image.png](https://d2cxucsjd6xvsd.cloudfront.net/public/team/b5f684e60ab1a64567fb280d07faed2c4132e041/attachment/bd9db11f4c6c9f6e7a3c027cb7da91e50a182eb7/image.png)

**Preconditions:** -

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Teacher view paired lesson on BO Calendar | Show Pair Lesson in related list:<br><br>* Lesson Schedule<br><br><br>* Pair Lesson:<br>    *  Lesson Name (Hyperlink)<br>    * Lesson Date, Lesson time<br>    * Teacher name<br>* Related list | - |

---

### TC-14921: CM/Teacher view LS without related schedule

**Preconditions:** -

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | CM view LS on SF | No paired lesson displayed | - |
| 2 | Teacher view lesson on BO Calendar | No paired lesson displayed | - |
| 3 | Teacher view lesson on BO Lesson Detail | No paired lesson displayed | - |

---

### TC-14922: CM/Teacher view LS without lesson code

**Preconditions:** -

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | CM view LS on SF | No paired lesson displayed | - |
| 2 | Teacher view lesson on BO Calendar | No paired lesson displayed | - |
| 3 | Teacher view lesson on BO Lesson Detail | No paired lesson displayed | - |

---

### TC-14923: CM/Teacher view LS mismatch lesson code

**Preconditions:** -

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | CM view LS on SF | No paired lesson displayed | - |
| 2 | Teacher view lesson on BO Calendar | No paired lesson displayed | - |
| 3 | Teacher view lesson on BO Lesson Detail | No paired lesson displayed | - |

---

### TC-14924: Multiple lessons under related lesson schedule with same lesson code

**Preconditions:** -

_Steps TBD_

---

## Integration/Regression/Performance

### TC-14914: CM/Teacher view pair lesson after updating lesson code

**Preconditions:** -

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | CM view paired lesson on SF Lesson Detail/Calendar | Show pair lesson is updated correctly | - |
| 2 | Teacher view paired lesson on BO Lesson Detail/Calendar | Show pair lesson is updated correctly | - |

---

### TC-14926: CM/Teacher view pair lesson after deleting pair lesson

**Preconditions:** -

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | CM view paired lesson on SF Lesson Detail/Calendar | Show pair lesson is updated correctly | - |
| 2 | Teacher view paired lesson on BO Lesson Detail/Calendar | Show pair lesson is updated correctly | - |

---

### TC-14927: CM Duplicate a lesson with pair lesson

**Preconditions:** -

_Steps TBD_

---

### TC-14928: CM Assign a teacher and student to pair lesson

**Preconditions:** -

_Steps TBD_

---

### TC-14929: CM update attendance for a student in pair lesson

**Preconditions:** -

_Steps TBD_

---

### TC-14930: CM update report for a student in pair lesson

**Preconditions:** -

_Steps TBD_

---

### TC-14931: Student view pair lesson

**Preconditions:** -

_Steps TBD_

---

### TC-14932: Student update attendance response in pair lesson

**Preconditions:** -

_Steps TBD_

---

### TC-14933: Import large CSV with many paired schedules completes successfully

**Preconditions:** -

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Import 10000 LS with pair lesson | - | - |

---
