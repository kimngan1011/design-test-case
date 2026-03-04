# Clashing Alert

## Clashing Alert

### TC-4947: Assign a teacher to lesson with L1.start = L2.end

**Description:** Check remark and confirm popup

**Preconditions:**

Create Lesson L1 with a Teacher T1:

* Start date time = 2025/07/11 09:30
* End Date Time = 2025/07/11 11:00

Create Lesson L2 with:

* Start date time = 2025/07/11 08:30
* End Date Time = 2025/07/11 09:30

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Open Lesson L2 | - | - |
| 2 | Add Teacher T1 | User does not see clashing alert with Lesson L1 in Confirm popup | - |
| 3 | Click Save button | User does not see clashing alert with Lesson L1 in Remark field | - |

---

### TC-4946: Assign a teacher to lesson with L1.end = L2.start

**Description:** Check remark and confirm popup

**Preconditions:**

Create Lesson L1 with a Teacher T1:

* Start date time = 2025/07/11 09:30
* End Date Time = 2025/07/11 11:00

Create Lesson L2 with:

* Start date time = 2025/07/11 11:00
* End Date Time = 2025/07/11 13:00

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Open Lesson L2 | - | - |
| 2 | Add Teacher T1 | User does not see clashing alert with Lesson L1 in Confirm popup | - |
| 3 | Click Save button | User does not see clashing alert with Lesson L1 in Remark field | - |

---

### TC-6026: Assign a teacher to lesson with L2.start = L1.start and L2.end < L1.end

**Description:** Check remark and confirm popup

**Preconditions:**

Create Lesson L1 with a Teacher T1:

* Start date time = 2025/07/11 09:30
* End Date Time = 2025/07/11 11:00

Create Lesson L2 with:

* Start date time = 2025/07/11 09:30
* End Date Time = 2025/07/11 10:30

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Open Lesson L2 | - | - |
| 2 | Add Teacher T1 | User sees clashing alert with Lesson L1 in Confirm popup | - |
| 3 | Click Save button | User sees clashing alert with Lesson L1 in Remark field | - |

---

### TC-6027: Assign a teacher to lesson with L2.start = L1.start and L2.end > L1.end

**Description:** Check remark and confirm popup

**Preconditions:**

Create Lesson L1 with a Teacher T1:

* Start date time = 2025/07/11 09:30
* End Date Time = 2025/07/11 11:00

Create Lesson L2 with:

* Start date time = 2025/07/11 09:30
* End Date Time = 2025/07/11 11:30

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Open Lesson L2 | - | - |
| 2 | Add Teacher T1 | User sees clashing alert with Lesson L1 in Confirm popup | - |
| 3 | Click Save button | User sees clashing alert with Lesson L1 in Remark field | - |

---

### TC-6028: Assign a teacher to lesson with L2.start < L1.start and L2.end = L1.end

**Description:** Check remark and confirm popup

**Preconditions:**

Create Lesson L1 with a Teacher T1:

* Start date time = 2025/07/11 09:30
* End Date Time = 2025/07/11 11:00

Create Lesson L2 with:

* Start date time = 2025/07/11 08:30
* End Date Time = 2025/07/11 11:00

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Open Lesson L2 | - | - |
| 2 | Add Teacher T1 | User sees clashing alert with Lesson L1 in Confirm popup | - |
| 3 | Click Save button | User sees clashing alert with Lesson L1 in Remark field | - |

---

### TC-6029: Assign a teacher to lesson with L2.start > L1.start and L2.end = L1.end

**Description:** Check remark and confirm popup

**Preconditions:**

Create Lesson L1 with a Teacher T1:

* Start date time = 2025/07/11 09:30
* End Date Time = 2025/07/11 11:00

Create Lesson L2 with:

* Start date time = 2025/07/11 10:00
* End Date Time = 2025/07/11 11:00

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Open Lesson L2 | - | - |
| 2 | Add Teacher T1 | User sees clashing alert with Lesson L1 in Confirm popup | - |
| 3 | Click Save button | User sees clashing alert with Lesson L1 in Remark field | - |

---

### TC-4948: Assign a teacher to lesson with L2.start < L1.end and L2.end > L1.end

**Description:** Check remark and confirm popup

**Preconditions:**

Create Lesson L1 with a Teacher T1:

* Start date time = 2025/07/11 9:30
* End Date Time = 2025/07/11 11:00

Create Lesson L2 with:

* Start date time = 2025/07/11 10:30
* End Date Time = 2025/07/11 11:30

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Open Lesson L2 | - | - |
| 2 | Add Teacher T1 | User sees clashing alert with Lesson L1 in Confirm popup | - |
| 3 | Click Save button | User sees clashing alert with Lesson L1 in Remark field | - |

---

### TC-4949: Assign a teacher to lesson with L2.start < L1.start and L2.end < L1.end

**Description:** Check remark and confirm popup

**Preconditions:**

Create Lesson L1 with a Teacher T1:

* Start date time = 2025/07/11 9:30
* End Date Time = 2025/07/11 11:00

Create Lesson L2 with:

* Start date time = 2025/07/11 09:00
* End Date Time = 2025/07/11 10:30

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Open Lesson L2 | - | - |
| 2 | Add Teacher T1 | User sees clashing alert with Lesson L1 in Confirm popup | - |
| 3 | Click Save button | User sees clashing alert with Lesson L1 in Remark field | - |

---

### TC-4950: Assign a teacher to lesson with L2.start < L1.start and L2.end > L1.end

**Description:** Check remark and confirm popup

**Preconditions:**

Create Lesson L1 with a Teacher T1:

* Start date time = 2025/07/11 9:30
* End Date Time = 2025/07/11 11:00

Create Lesson L2 with:

* Start date time = 2025/07/11 08:30
* End Date Time = 2025/07/11 11:30

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Open Lesson L2 | - | - |
| 2 | Add Teacher T1 | User sees clashing alert with Lesson L1 in Confirm popup | - |
| 3 | Click Save button | User sees clashing alert with Lesson L1 in Remark field | - |

---

### TC-4951: Assign a teacher to lesson with L2.start > L1.start and L2.end < L1.end

**Description:** Check remark and confirm popup

**Preconditions:**

Create Lesson L1 with a Teacher T1:

* Start date time = 2025/07/11 9:30
* End Date Time = 2025/07/11 11:00

Create Lesson L2 with:

* Start date time = 2025/07/11 10:00
* End Date Time = 2025/07/11 10:30

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Open Lesson L2 | - | - |
| 2 | Add Teacher T1 | User sees clashing alert with Lesson L1 in Confirm popup | - |
| 3 | Click Save button | User sees clashing alert with Lesson L1 in Remark field | - |

---

### TC-4956: Assign a teacher to a recurring lesson with clashing alert and only this

**Description:** Check remark and confirm popup

**Preconditions:**

Create Recurring Lesson L1 with a Teacher T1 in all lessons

* Start date time = 2025/07/11 09:30
* End Date Time = 2025/09/01 11:00

Create Recurring Lesson L2 with:

* Start date time = 2025/07/11 08:30
* End Date Time = 2025/09/01 11:00

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Open the 1st lesson in Recurring Lesson L2 | - | - |
| 2 | Add Teacher T1 with only this | User sees the 1st lesson in Recurring Lesson L2 clashing alert with the 1st lesson in Recurring Lesson L1 in Confirm popup | - |
| 3 | Click Save button | User sees the 1st lesson in Recurring Lesson L2 clashing alert with the 1st lesson in Recurring Lesson L1 in Remark field | - |

---

### TC-6256: Assign a teacher to a recurring lesson with clashing alert and following lessons

**Description:** Check remark and confirm popup

**Preconditions:**

Create Recurring Lesson L1 with a Teacher T1 in all lessons

* Start date time = 2025/07/11 09:30
* End Date Time = 2025/09/01 11:00

Create Recurring Lesson L2 with:

* Start date time = 2025/07/11 08:30
* End Date Time = 2025/09/01 11:00

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Open the 2nd lesson in Recurring Lesson L2 | - | - |
| 2 | Add Teacher T1 with following lessons | User sees the all lessons from the 2nd lesson onward in Recurring Lesson L2 clashing alert with the all lessons from the 2nd lesson onward in Recurring Lesson L1 in Confirm popup | - |
| 3 | Click Save button | User sees the all lessons from the 2nd lesson onward in Recurring Lesson L2 clashing alert with the all lessons from the 2nd lesson onward in Recurring Lesson L1 in Remark field | - |

---

### TC-4959: Assign a teacher to a other location with clashing alert

**Description:** Check remark and confirm popup

**Preconditions:**

Create Lesson L1 with a Teacher T1 at Location L1:

* Start date time = 2025/07/11 09:30
* End Date Time = 2025/07/11 11:00

Create Lesson L2 at Location L2 with:

* Start date time = 2025/07/11 09:30
* End Date Time = 2025/07/11 10:30

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Open Lesson L2 | - | - |
| 2 | Add Teacher T1 | User sees clashing alert with Lesson L1 in Confirm popup | - |
| 3 | Click Save button | User sees clashing alert with Lesson L1 in Remark field | - |

---

### TC-4963: Assign teacher in lesson schedule with clashing alert

**Description:** Check remark and confirm popup

**Preconditions:**

Create Lesson L1 with a Teacher T1:

* Start date time = 2025/07/11 9:30
* End Date Time = 2025/07/11 11:00

Create Lesson L2 with:

* Start date time = 2025/07/11 10:00
* End Date Time = 2025/07/11 10:30

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Open lesson schedule of Lesson L2 | - | - |
| 2 | Add Teacher T1 | - | - |
| 3 | Open Lesson L2 | User sees clashing alert with Lesson L1 in Remark field | - |

---

### TC-4964: Assign teacher to lesson course schedule with clashing alert

**Description:** Check remark and confirm popup

**Preconditions:**

Create Lesson Course Schedule L1 with a Teacher T1 in all lessons

* Start date time = 2025/07/11 09:30
* End Date Time = 2025/09/01 11:00

Create Lesson Course Schedule L2 with:

* Start date time = 2025/07/11 08:30
* End Date Time = 2025/09/01 11:00

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Open the 2nd lesson in Lesson Course Schedule L2 | - | - |
| 2 | Add Teacher T1 with following lessons | User sees the all lessons from the 2nd lesson onward in Lesson Course Schedule L2 clashing alert with the all lessons from the 2nd lesson onward in Lesson Course Schedule L1 in Confirm popup | - |
| 3 | Click Save button | User sees the all lessons from the 2nd lesson onward in Lesson Course Schedule L2 clashing alert with the all lessons from the 2nd lesson onward in Lesson Course Schedule L1 in Remark field | - |

---

### TC-4989: Assign a teacher to lesson with clashing alert on BO

**Preconditions:**

Create Lesson L1 with a Teacher T1:

* Start date time = 2025/07/11 9:30
* End Date Time = 2025/07/11 11:00

Create Lesson L2 with:

* Start date time = 2025/07/11 10:00
* End Date Time = 2025/07/11 10:30

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Login BO and open Lesson L2 | - | - |
| 2 | Add Teacher T1 | - | - |
| 3 | Login SF and open Lesson L2 | User sees clashing alert with Lesson L1 in Remark field | - |

---

### TC-6274: Assign a teacher to a recurring lesson with clashing alert and following lessons on Calendar

**Description:** Check remark and confirm popup

**Preconditions:**

Create Recurring Lesson L1 with a Teacher T1 in all lessons

* Start date time = 2025/07/11 09:30
* End Date Time = 2025/09/01 11:00

Create Lesson Course Schedule L2 with:

* Start date time = 2025/07/11 08:30
* End Date Time = 2025/09/01 11:00

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | On Calendar, open the 2nd lesson in Lesson Course Schedule L2 | - | - |
| 2 | Add Teacher T1 with following lessons | - | - |
| 3 | Open lesson detail | User sees the all lessons from the 2nd lesson onward in Lesson Course Schedule L2 clashing alert with the all lessons from the 2nd lesson onward in Recurring Lesson L1 in Remark field | - |

---

### TC-4962: Import lesson teacher with clashing alert

**Description:** Check remark and confirm popup

**Preconditions:**

Create Lesson L1 with a Teacher T1:

* Start date time = 2025/07/11 9:30
* End Date Time = 2025/07/11 11:00

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Import Lesson L2 and Recurring Lesson L3 with Teacher T1:<br><br>* Start date time = 2025/07/11 9:30<br>* End Date Time = 2025/09/01 11:00 | - | - |
| 2 | Open Lesson L2 | User sees clashing alert with Lesson L1 and Lesson L3 in Remark field | - |

---

### TC-4953: Edit lesson time so that L1.start = L2.end

**Description:** Check remark and confirm popup

**Preconditions:**

Create Lesson L1 with a Teacher T1:

* Start date time = 2025/07/11 9:30
* End Date Time = 2025/07/11 11:00

Create Lesson L2 with a Teacher T1:

* Start date time = 2025/07/11 10:00
* End Date Time = 2025/07/11 10:30

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Edit Lesson L2 with<br><br>* Start date time = 2025/07/11 08:00<br>* End Date Time = 2025/07/11 09:30 | User does not sees clashing alert | - |

---

### TC-4952: Edit lesson time so that L1.end = L2.start

**Description:** Check remark and confirm popup

**Preconditions:**

Create Lesson L1 with a Teacher T1:

* Start date time = 2025/07/11 9:30
* End Date Time = 2025/07/11 11:00

Create Lesson L2 with a Teacher T1:

* Start date time = 2025/07/11 10:30
* End Date Time = 2025/07/11 11:30

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Edit Lesson L2 with<br><br>* Start date time = 2025/07/11 11:00<br>* End Date Time = 2025/07/11 11:30 | User does not sees clashing alert | - |

---

### TC-6030: Edit lesson time so that L2.start = L1.start and L2.end < L1.end

**Description:** Check remark and confirm popup

**Preconditions:**

Create Lesson L1 with a Teacher T1:

* Start date time = 2025/07/11 09:30
* End Date Time = 2025/07/11 10:00

Create Lesson L2 with a Teacher T1:

* Start date time = 2025/07/11 08:00
* End Date Time = 2025/07/11 09:30

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Edit Lesson L2 with<br><br>* Start date time = 2025/07/11 09:30<br>* End Date Time = 2025/07/11 09:45 | User sees clashing alert with Lesson L1 | - |

---

### TC-6031: Edit lesson time so that L2.start = L1.start and L2.end > L1.end

**Description:** Check remark and confirm popup

**Preconditions:**

Create Lesson L1 with a Teacher T1:

* Start date time = 2025/07/11 09:30
* End Date Time = 2025/07/11 10:00

Create Lesson L2 with a Teacher T1:

* Start date time = 2025/07/11 10:00
* End Date Time = 2025/07/11 11:30

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Edit Lesson L2 with<br><br>* Start date time = 2025/07/11 09:30<br>* End Date Time = 2025/07/11 11:30 | User sees clashing alert with Lesson L1 | - |

---

### TC-6033: Edit lesson time so that L2.start > L1.start and L2.end = L1.end

**Description:** Check remark and confirm popup

**Preconditions:**

Create Lesson L1 with a Teacher T1:

* Start date time = 2025/07/11 09:30
* End Date Time = 2025/07/11 10:00

Create Lesson L2 with a Teacher T1:

* Start date time = 2025/07/11 10:00
* End Date Time = 2025/07/11 11:30

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Edit Lesson L2 with <br><br>* Start date time = 2025/07/11 09:45<br>* End Date Time = 2025/07/11 10:00 | User sees clashing alert with Lesson L1 | - |

---

### TC-6032: Edit lesson time so that L2.start < L1.start and L2.end = L1.end

**Description:** Check remark and confirm popup

**Preconditions:**

Create Lesson L1 with a Teacher T1:

* Start date time = 2025/07/11 09:30
* End Date Time = 2025/07/11 10:00

Create Lesson L2 with a Teacher T1:

* Start date time = 2025/07/11 10:00
* End Date Time = 2025/07/11 11:30

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Edit Lesson L2 with <br><br>* Start date time = 2025/07/11 09:00<br>* End Date Time = 2025/07/11 10:00 | User sees clashing alert with Lesson L1 | - |

---

### TC-4954: Edit lesson time so that L2.start < L1.end and L2.end > L1.end

**Description:** Check remark and confirm popup

**Preconditions:**

Create Lesson L1 with a Teacher T1:

* Start date time = 2025/07/11 10:30
* End Date Time = 2025/07/11 11:00

Create Lesson L2 with a Teacher T1:

* Start date time = 2025/07/11 10:00
* End Date Time = 2025/07/11 10:30

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Edit Lesson L2 with <br><br>* Start date time = 2025/07/11 10:00<br>* End Date Time = 2025/07/11 11:30 | User sees clashing alert with Lesson L1 | - |

---

### TC-4955: Edit lesson time so that L2.start < L1.start and L2.end < L1.end

**Description:** Check remark and confirm popup

**Preconditions:**

Create Lesson L1 with a Teacher T1:

* Start date time = 2025/07/11 10:30
* End Date Time = 2025/07/11 11:00

Create Lesson L2 with a Teacher T1:

* Start date time = 2025/07/11 10:00
* End Date Time = 2025/07/11 10:30

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Edit Lesson L2 with <br><br>* Start date time = 2025/07/11 10:00<br>* End Date Time = 2025/07/11 10:45 | User sees clashing alert with Lesson L1 | - |

---

### TC-4957: Edit lesson time so that L2.start < L1.start and L2.end > L1.end

**Description:** Check remark and confirm popup

**Preconditions:**

Create Lesson L1 with a Teacher T1:

* Start date time = 2025/07/11 10:30
* End Date Time = 2025/07/11 11:00

Create Lesson L2 with a Teacher T1:

* Start date time = 2025/07/11 10:00
* End Date Time = 2025/07/11 10:30

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Edit Lesson L2 with<br><br>* Start date time = 2025/07/11 10:00<br>* End Date Time = 2025/07/11 11:30 | User sees clashing alert with Lesson L1 | - |

---

### TC-4958: Edit lesson time so that L2.start > L1.start and L2.end < L1.end

**Description:** Check remark and confirm popup

**Preconditions:**

Create Lesson L1 with a Teacher T1:

* Start date time = 2025/07/11 10:30
* End Date Time = 2025/07/11 11:00

Create Lesson L2 with a Teacher T1:

* Start date time = 2025/07/11 10:00
* End Date Time = 2025/07/11 10:30

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Edit lesson L2 with<br><br>* Start date time = 2025/07/11 10:35<br>* End Date Time = 2025/07/11 10:55 | User sees clashing alert with Lesson L1 | - |

---

### TC-4960: Edit lesson date with clashing alert

**Description:** Check remark and confirm popup

**Preconditions:**

Create Lesson L1 with a Teacher T1:

* Start date time = 2025/07/12 9:30
* End Date Time = 2025/07/12 11:00

Create Lesson L2 with:

* Start date time = 2025/07/11 10:00
* End Date Time = 2025/07/11 10:30

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Open Lesson L2 | - | - |
| 2 | Edit lesson date <br><br>* Start date time = 2025/07/12 10:00<br>* End Date Time = 2025/07/12 10:30 | User sees clashing alert with Lesson L1 in Confirm popup | - |
| 3 | Click Save button | User sees clashing alert with Lesson L1 in Remark field | - |

---

### TC-4961: Edit lesson date&time for recurring lesson with clashing alert

**Description:** Check remark and confirm popup

**Preconditions:**

Create Lesson L1 with a Teacher T1:

* Start date time = 2025/07/11 9:30
* End Date Time = 2025/07/11 11:00

Create Lesson L2 with:

* Start date time = 2025/07/12 11:00
* End Date Time = 2025/07/12 11:30

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Edit lesson L2 with<br><br>* Start date time = 2025/07/11 10:00<br>* End Date Time = 2025/07/11 13:00 | User sees clashing alert with Lesson L1 | - |

---

### TC-4966: Clashing alert with lesson and event

**Description:** Check remark and confirm popup

**Preconditions:**

Create Event E1 with a Teacher T1:

* Start date time = 2025/07/11 09:30
* End Date Time = 2025/07/11 11:00

Create Lesson L2 with:

* Start date time = 2025/07/11 09:30
* End Date Time = 2025/07/11 10:30

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Open Lesson L2 | - | - |
| 2 | Add Teacher T1 | User sees clashing alert with Event E1 in Confirm popup | - |
| 3 | Click Save button | User sees clashing alert with Event E1 in Remark field | - |

---

### TC-4965: Unassign teacher from lesson with clashing alert

**Description:** Check remark and confirm popup

**Preconditions:**

Create Lesson L1 with a Teacher T1:

* Start date time = 2025/07/11 09:30
* End Date Time = 2025/07/11 11:00

Create Lesson L2 with a Teacher T1:

* Start date time = 2025/07/11 09:30
* End Date Time = 2025/07/11 10:30

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Open Lesson L2 | - | - |
| 2 | Remove Teacher T1 | User does not see clashing alert with Lesson L1 in Remark field | - |
| 3 | Open Lesson L1 | User does not see clashing alert with Lesson L2 in Remark field | - |

---

### TC-6384: Unassign teacher from lesson with clashing alert and only this lesson

**Description:** Check remark and confirm popup

**Preconditions:**

Create Recurring Lesson L1 with a Teacher T1 in all lessons

* Start date time = 2025/07/11 09:30
* End Date Time = 2025/09/01 11:00

Create Recurring Lesson L2 with Teacher T1 in all lessons

* Start date time = 2025/07/11 08:30
* End Date Time = 2025/09/01 11:00

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Open the 2nd lesson | - | - |
| 2 | Remove Teacher T1 with only this | User does not see clashing alert with Lesson L1 in Remark field | - |
| 3 | Check other lessons in Recurring Lesson L2 | User sees other lessons still remain clashing alert with lessons in Recurring Lesson L1 | - |

---

### TC-6385: Unassign teacher from lesson with clashing alert and following lessons

**Description:** Check remark and confirm popup

**Preconditions:**

Create Recurring Lesson L1 with a Teacher T1 in all lessons

* Start date time = 2025/07/11 09:30
* End Date Time = 2025/09/01 11:00

Create Recurring Lesson L2 with Teacher T1 in all lessons

* Start date time = 2025/07/11 08:30
* End Date Time = 2025/09/01 11:00

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Open the 2nd lesson | - | - |
| 2 | Remove Teacher T1 with following lessons | User does not see clashing alert with Lesson L1 in Remark field | - |
| 3 | Check other lessons in Recurring Lesson L2 | User does not see clashing alert in other lessons in Remark field | - |
| 4 | Check the 1st lesson in Recurring Lesson L2 | User still sees clashing alert with Lesson L1 | - |

---
