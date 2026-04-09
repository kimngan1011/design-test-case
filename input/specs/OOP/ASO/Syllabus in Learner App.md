# [Aso] (App) Syllabus in Learner App – Consolidated Spec

- **Jira Epic:** [LT-88822 – [Aso] (App) Syllabus in Learner App](https://manabie.atlassian.net/browse/LT-88822)
- **Project:** LT – Learning and Teaching
- **Issue Type:** Epic
- **Status:** Ready for QA
- **Priority:** Medium
- **Team:** Tech - Scheduling Management
- **Project Type:** Customization
- **Type of System:** ERP
- **Partner Name:** Aso
- **Fix Version:** v2026.03.30
- **Production Release Date:** 2026-03-30

---

## 1. Stakeholders & Roles

- **Reporter:** [The Khuong Dang](/people/600655f5ea0e64006b581903)
- **Assignee:** [Tran Quoc Bao](/people/604f0c7337065a006960d085)
- **Product Manager:** [Maria Nawatani](/people/61c3b17749f195006991f4e0)
- **QA:** [Nguyễn Châu Thùy Linh](/people/712020:669d0243-fd52-475c-9396-4955d8d3b6ea)

---

## 2. Timeline

- **Created:** 2025-11-03T10:58:15.498Z
- **Start date (Dev start):** 2025-12-22
- **Due date (Dev end, excl. QA):** 2026-01-17
- **QA Start Date:** _(empty)_
- **QA Finish Date:** 2026-01-23
- **Internal UAT Date:** 2026-02-02
- **External UAT Date:** 2026-02-02
- **Updated:** 2026-03-03T09:39:16.736Z

> **Explain dev dates**  
> - **Start Date:** day development starts  
> - **Due Date:** date when development is finished, excluding QA

---

## 3. Estimates & Tracking

- **Original estimate:** 288000 seconds
- **Time tracking:** `OriginalEstimate1(timeInSeconds=288000) RemainingEstimate(timeInSeconds=288000) null`
- **Actual DCP:** 0.0
- **Story Points / T-Shirt sizes / QA estimates:** _(not set)_

---

## 4. Functional Overview

### 4.1 Summary

Students can search/filter and see details of their interested/taken syllabus information in the Learner app.

### 4.2 User Story

As a **student** using the **Learner app**:

1. I can open the **“Syllabus” menu** and see the **Syllabus list**.
2. I can **search/filter** all syllabuses and see the results.
3. I can **click and view the details** of each syllabus, then return to the list.
4. I can **open each syllabus detail page from Lesson syllabus**.

### 4.3 External References

- **Detailed Requirements:**  
  https://manabie.atlassian.net/wiki/spaces/PrTi/pages/1515814976/App+Syllabus+view
- **Screen Design (Figma):**  
  https://www.figma.com/design/nVD1dJzgSJd2kAEa3ZkLav/External-Grade-Management?node-id=6436-26900&t=eCc4QK3WPAZHAxZI-0

---

## 5. Business Rules & Behavior

### 5.1 Syllabus Visibility (Slack thread – image1.png)

- **Current issue reported by Aso:**  
  Draft status syllabuses can still be seen in the Learner app.
- **Required behavior:**
  - **Only Published syllabuses** are visible to students in the app.
  - Draft (and any non‑published status) syllabuses **must NOT** be visible in Learner app.
- **Implementation note (from PM–Dev discussion):**
  - It is acceptable to **implement this together with the remaining study goals** changes.

### 5.2 Feature Configuration

- **Feature flag / config:**  
  `lesson.syllabus_master.is_enabled`
- **Comment:** Feature is enabled on **ASO UAT**.

---

## 6. Aso Feedback – Detailed UI / UX Requirements

Source: Slack thread screenshots (image1.png, image2.png, image4.png, image5.png).

### 6.1 Search Filter Behavior

1. **Academic Year & Grade Not Editable**
   - Students **cannot change Academic Year and Grade** on the Syllabus search UI.
   - These fields are **defaulted & non-editable**.
   - Default values:
     - **Academic Year = Current Academic Year**
     - **Grade = Student’s current grade**

2. **Implication on Search UI:**
   - Remove interactive controls for Academic Year and Grade on the student-facing filter.
   - Show them as **read-only values** or omit them visually, as per design, but the backend must always filter using:
     - current academic year of the system, and
     - student’s current grade.

---

### 6.2 JP Label Updates (Syllabus List)

Apply the following Japanese label changes in the **Syllabus list** screen.

1. **Syllabus List title / section:**
   - **AsIs:** シラバス  
   - **ToBe:** 科目一覧

2. **Course section label:**
   - **AsIs:** コース：  
   - **ToBe:** 科目：

(From image2.png: “AsIs シラバス / ToBe 科目一覧“, “AsIs コース: / ToBe 科目:”.)

---

### 6.3 Syllabus Card Updates (List Items)

From image4.png annotations:

1. **Semester vs Academic Year:**
   - Currently shows something equivalent to **“実施年度”** (delivery year / academic year).
   - Aso feedback: Academic year (年度／学年) is assumed and less important; **they prefer to show Semester and Lecturers on the card**.
   - **Change:**
     - Replace the field label/content currently showing **Academic Year / 実施年度** on the card with **“Semester”**.
     - Display the **syllabus’s semester** value instead.

2. **Add Lecturers Below Semester:**
   - Add a **“Lecturers”** line below the Semester on each Syllabus card.
   - Display the lecturer names, e.g.:
     - `Lecturers  Takuya Honma, Koki Misawa`
   - Layout (from top to bottom example):
     - Curriculum / course name
     - Syllabus name
     - **Semester** (instead of Academic Year)
     - **Lecturers** (new line)

3. **Navigation & Header Text:**
   - The Syllabus list page title remains “シラバス” in the app header (as shown at the top of image4.png), unless otherwise specified by design.

---

### 6.4 Syllabus Detail Page

From image2.png + lower part of image4.png.

1. **Page Title**
   - Change the **page header title** to show **“Syllabus Name”** (科目B etc.) instead of the **curriculum subject name**.
   - Example (image4.png):
     - Header: `科目B` (Syllabus Name)
     - Not curriculum subject name.

2. **Field Translations (to check/confirm)**
   - **Lesson Format**
     - Confirm that translation of the field representing lesson format is correct (e.g., “Lecture” as shown in image4.png).
   - **Semester**
     - Confirm the translation for “Semester” (実施時期 / 学期 etc.) is correct.

3. **Field Label Change – 不要 label**
   - For the label **“科目”**, Aso says:  
     “We don’t need ‘科目’ (Label is ok).”
   - Interpretation:
     - Keep the screen content as-is where necessary, but adjust label usage where redundant.
     - Specifically ensure that the Syllabus name in the header stands alone (科目B) without an extra redundant “科目” label preceding it in the detail section, per latest JP wording.

4. **Key Fields on Detail Page (from image4.png visual)**

   Visible main section “科目詳細（かもくしょうさい）” includes, at minimum:

   - 科目名 (Syllabus Name)
   - 必須 / 必須科目 (Required / elective status)
   - 対象学年 (Target Grade) – example: 2年
   - 履修時間 (Credit hours) – example: 15時間
   - 主な授業形態 (Main Lesson Format) – example: Lecture
   - 実施時期 (Semester) – example: First Semester
   - 単位 (Credits) – example: 1単位

   Ensure that:
   - Semester and Lesson Format values & labels match the JP expectations.
   - Layout follows the Figma design.

---

## 7. Data Mapping and Backend Notes

### 7.1 Visibility Logic

- **Filter by status = Published** when fetching syllabuses for the Learner app.
- Ensure that **Draft or other non‑Published** records are never included in:
  - Syllabus list
  - Syllabus detail opened directly or via lesson syllabus.

### 7.2 Feature Toggle

- **Config key:** `lesson.syllabus_master.is_enabled`
- Used to enable/disable the Syllabus feature (confirmed enabled on ASO UAT).

### 7.3 Object Mapping (image5.png)

From the screenshot text:

- **AsIs:** `MANAERP__Teaching_Material__c`
- **ToBe:** `MANAERP__Detail__c`

Implication:

- The **Syllabus / Lesson unit list** in the relevant UI should be backed by **`MANAERP__Detail__c`** instead of **`MANAERP__Teaching_Material__c`**.
- Update any queries, relationships, or mappings that currently reference `MANAERP__Teaching_Material__c` for this screen to use `MANAERP__Detail__c`.

---

## 8. Release Notes

### 8.1 Internal (JP)

- **Description (JP):**  
  Learner appにシラバスメニューを追加  
  区分: 新機能  
  詳細: Learner appにシラバス詳細検索メニューを追加  
  利用方法: Asoのみを想定。開発に要連絡。

- **Description (EN):** _(empty)_
- **Remarks:** _(empty)_

### 8.2 External (JP)

- **Description (JP):** 記載不要

---

## 9. Comments History (Jira)

1. **2026-03-03 – Nguyễn Châu Thùy Linh**  
   - `clarify: https://manabie.slack.com/archives/C037409QQ4S/p1771908406886089`  
   - (Slack thread contains the Aso feedback summarized above.)

2. **2026-02-06 – Tran Quoc Bao**  
   - `enabled on ASO uat`

3. **2026-02-06 – Tran Quoc Bao**  
   - `feature config: lesson.syllabus_master.is_enabled`

---

## 10. Attachments

- **Jira attachment:**  
  `image-20260206-101833.png`  
  https://api.media.atlassian.com/file/5c77bc39-98b7-4616-bade-5910aa447ffa/binary?token=eyJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJkM2FmZWViMi1jZjdkLTQxMjYtYjEyYi00Y2YzYzczN2ExM2EiLCJhY2Nlc3MiOnsidXJuOmZpbGVzdG9yZTpmaWxlOjVjNzdiYzM5LTk4YjctNDYxNi1iYWRlLTU5MTBhYTQ0N2ZmYSI6WyJyZWFkIl19LCJleHAiOjE3NzMxMTcxMjUsIm5iZiI6MTc3MzExNjUyNX0.FnwAmla8dmW0JVYvbbVaakL-Pw95TfSoXI70Z8OdcsE&client=d3afeeb2-cf7d-4126-b12b-4cf3c737a13a&dl=true&name=image-20260206-101833.png

- **Slack-based images used for this spec:**
  - `image1.png` – Slack thread overview (Aso reports Draft visibility issue + feedback intro)
  - `image2.png` – Text list of “Feedback from Aso” items 1–4
  - `image4.png` – Syllabus list & detail UI with JP annotations (Semester & Lecturers, title)
  - `image5.png` – Data mapping AsIs vs ToBe (`MANAERP__Teaching_Material__c` → `MANAERP__Detail__c`)

---

## 11. Open Points / Validation Checklist

Use this as a QA checklist:

1. **Status filter**
   - [ ] Only Published syllabuses appear in Learner app list and detail.
2. **Search filters**
   - [ ] Academic Year defaults to current academic year.
   - [ ] Grade defaults to student’s current grade.
   - [ ] Student cannot modify Academic Year or Grade.
3. **JP labels (list)**
   - [ ] Syllabus list label shows 「科目一覧」 instead of 「シラバス」 where required.
   - [ ] Course label shows 「科目：」 instead of 「コース：」.
4. **Card layout**
   - [ ] Semester is shown instead of Academic Year on each card.
   - [ ] Lecturers line is displayed below Semester with correct names.
5. **Detail page**
   - [ ] Page header shows Syllabus Name (e.g., 科目B), not curriculum subject name.
   - [ ] Lesson Format translation is correct.
   - [ ] Semester translation is correct.
   - [ ] No redundant 「科目」 label where Aso requested removal.
6. **Backend / data**
   - [ ] Visibility and filters correctly applied using Published status.
   - [ ] Feature flag `lesson.syllabus_master.is_enabled` works as expected and is on for Aso.
   - [ ] Object mapping updated from `MANAERP__Teaching_Material__c` to `MANAERP__Detail__c` where specified.
