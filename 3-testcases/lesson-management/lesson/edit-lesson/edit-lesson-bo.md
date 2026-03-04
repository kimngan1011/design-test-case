# Lesson Detail

## Lesson Detail

### TC-9811: Verify recurring setting in lesson detail

**Preconditions:** -

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | View lesson with end date | ![image.png](https://d2cxucsjd6xvsd.cloudfront.net/public/team/b5f684e60ab1a64567fb280d07faed2c4132e041/attachment/9acf654ea23e7acab4fd3be03ff4329d205410e9/image.png) | - |
| 2 | View lesson with lesson numbe | ![image.png](https://d2cxucsjd6xvsd.cloudfront.net/public/team/b5f684e60ab1a64567fb280d07faed2c4132e041/attachment/c3b19d61967fe912e78501b382309600e8b975c4/image.png) | - |
| 3 | View custom lesson | ![image.png](https://d2cxucsjd6xvsd.cloudfront.net/public/team/b5f684e60ab1a64567fb280d07faed2c4132e041/attachment/bd4b9ee835d3063584604cb0597ccdad699c85de/image.png)<br>![image.png](https://d2cxucsjd6xvsd.cloudfront.net/public/team/b5f684e60ab1a64567fb280d07faed2c4132e041/attachment/1d570bf30d01168d42b369909a06326ae766c6f9/image.png) | - |
| 4 | View lesson course shedule <br><br>* AC<br>* LAW | - | - |
| 5 | View the one-time lesson | - | - |

---

### TC-1895: Edit an one-time lesson

**Preconditions:**

* User has published the one-time lesson with student

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | * Go to the lesson detail<br>* Click on \"Edit\" button<br>* Edit lesson name, lesson date&time, classroom, lesson capacity<br>* Attach material (pdf and image) to the lesson (only the owner is remove)<br>* Input the Zoom link to Live Streaming link field<br>* Click on \"Save\" button | * User sees the lesson info is updated on BO<br><br>* User preview the material on BO<br><br>* User is redirected to Zoom web/app when click on the Zoom link | - |
| 2 | Student login Mobile | * Student sees the lesson information is changed<br>* Student sees the material | - |
| 3 | Parent login Mobile | * Parent sees the lesson information is changed<br>* Parent sees the material | - |

---

### TC-10709: Edit all info in lesson course schedule

**Preconditions:**

Create a lesson course schedule (refer to TC [https://app.qase.io/case/PX-1015](https://app.qase.io/case/PX-1015))

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | Refer to TC [https://app.qase.io/case/PX-1044](https://app.qase.io/case/PX-1044) | - | - |

---

### TC-1896: Edit all info in daily lesson

**Preconditions:**

* User has published the daily lesson with student

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | * Open the 1st lesson in the chain<br>* Click on \"Edit\" button<br><br>* Edit lesson name, lesson date&time, classroom, lesson capacity<br><br>* Attach material (pdf and image) to the lesson<br><br>* Input the Zoom link to Live Streaming link field<br><br>* Click on \"Save\" button and select \"Only this lesson\"<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ Student login Mobile | * User sees the lesson info is updated for the selected lesson<br>* User preview the material of the selected lesson on BO<br>* User is redirected to Zoom web/app when click on the Zoom link<br>* User sees the other lessons in the chain with no change<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ * Student sees the lesson information is changed<br>* Student sees the material | - |
| 2 | * Open the 2nd lesson in the chain<br><br>* Click on \"Edit\" button<br><br>* Edit lesson name, lesson date&time so that lesson in the middle of the chain is closed date, classroom, lesson capacity<br><br>* Attach material (pdf and image) to the lesson<br><br>* Input the Zoom link to Live Streaming link field<br><br>* Click on \"Save\" button and select \"This and the following lessons\" | * User sees the lesson info is updated for this and the following lessons on BO<br>* User preview the material of the this and the following lesson on BO<br><br>* User is redirected to Zoom web/app when click on the Zoom link | - |

---

### TC-9812: Edit all info in weekly lesson

**Preconditions:**

* User has published the weekly lesson with student

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | * Open the 1st lesson in the chain<br>* Click on \"Edit\" button<br><br>* Edit lesson name, lesson date&time, classroom, lesson capacity<br><br>* Attach material (pdf and image) to the lesson<br><br>* Input the Zoom link to Live Streaming link field<br><br>* Click on \"Save\" button and select \"Only this lesson\"<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ Student login Mobile | * User sees the lesson info is updated for the selected lesson<br>* User preview the material of the selected lesson on BO<br>* User is redirected to Zoom web/app when click on the Zoom link<br>* User sees the other lessons in the chain with no change<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ * Student sees the lesson information is changed<br>* Student sees the material | - |
| 2 | * Open the 2nd lesson in the chain<br><br>* Click on \"Edit\" button<br><br>* Edit lesson name, lesson date&time so that lesson in the middle of the chain is closed date, classroom, lesson capacity<br><br>* Attach material (pdf and image) to the lesson<br><br>* Input the Zoom link to Live Streaming link field<br><br>* Click on \"Save\" button and select \"This and the following lessons\" | * User sees the lesson info is updated for this and the following lessons on BO<br>* User preview the material of the this and the following lesson on BO<br><br>* User is redirected to Zoom web/app when click on the Zoom link | - |

---

### TC-9813: Edit all info in custom lesson

**Preconditions:**

* User has published the weekly lesson with student

| # | Action | Expected Result | Test Data |
|---|--------|----------------|-----------|
| 1 | * Open the 1st lesson in the chain<br>* Click on \"Edit\" button<br><br>* Edit lesson name, lesson date&time, classroom, lesson capacity<br><br>* Attach material (pdf and image) to the lesson<br><br>* Input the Zoom link to Live Streaming link field<br><br>* Click on \"Save\" button and select \"Only this lesson\"<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ Student login Mobile | * User sees the lesson info is updated for the selected lesson<br>* User preview the material of the selected lesson on BO<br>* User is redirected to Zoom web/app when click on the Zoom link<br>* User sees the other lessons in the chain with no change<br>&nbsp;&nbsp;&nbsp;&nbsp;↳ * Student sees the lesson information is changed<br>* Student sees the material | - |
| 2 | * Open the 2nd lesson in the chain<br><br>* Click on \"Edit\" button<br><br>* Edit lesson name, lesson date&time so that lesson in the middle of the chain is closed date, classroom, lesson capacity<br><br>* Attach material (pdf and image) to the lesson<br><br>* Input the Zoom link to Live Streaming link field<br><br>* Click on \"Save\" button and select \"This and the following lessons\" | * User sees the lesson info is updated for this and the following lessons on BO<br>* User preview the material of the this and the following lesson on BO<br><br>* User is redirected to Zoom web/app when click on the Zoom link | - |

---
